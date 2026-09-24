#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_fetch_apifox.py — fetch_apifox.py 的本地测试套件

覆盖三大类场景（对应需求：正常读取 / 文档更新后的数据刷新 / 异常场景）：

  T0  语法检查（py_compile）
  T1  正常同步（全量拉取 + 写盘）                     —— 首次运行
  T2  幂等性（内容未变时二次同步全部跳过、mtime 不变）
  T3  --check 与 sync 结果一致（内容最新时 check exit 0）
  T4  文档更新后数据刷新（模拟远端内容变化 → 检出并重写）
  T5  树拉取失败 → exit 2 + 本地文档保留完整
  T6  单端点失败 → 计入 failed、其余端点正常、旧文件保留
  T7  树缓存损坏 → 自动重新拉取恢复
  T8  树缓存有效期内 → 不发树请求（用缓存）
  T9  孤儿文件清理（--prune）
  T10 render_api_md 纯函数单测（不依赖网络）

运行：python test_fetch_apifox.py
结果：控制台输出 + 写 test-report.json / test-report.md 到本目录
说明：T1-T9 全部运行在离线沙盒（FakeServer mock 网络 + SUANLI_SKILLS_ROOT
     指向 .test-sandbox-main/），不触碰真实仓库、不依赖真实网络。
"""

import json
import shutil
import subprocess
import sys
import time
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "fetch_apifox.py"

# 测试环境：真实的 venv python（含 requests）
PY = r"C:\Users\huangshaozheng\.workbuddy\binaries\python\envs\default\Scripts\python.exe"

# suanli-job 在 ENDPOINT_MAP 中的全部 6 个端点（测试树必须齐全，否则报"树中不存在"）
JOB_ENDPOINTS = [
    # (id, method, path, name, 本地文件名)
    (468648941, "post", "/api/task/job/create", "创建任务", "job-create.md"),
    (999000112, "get", "/api/task/job/search", "任务列表查询", "job-tasks.md"),
    (999000113, "get", "/api/task/job/detail", "任务详情查询", "job-detail.md"),
    (999000114, "post", "/api/task/job/stop", "停止任务", "job-stop.md"),
    (999000115, "get", "/api/job/queue/group/search", "任务队列组列表", "job-queue-list.md"),
    (999000116, "get", "/api/job/queue/group/detail", "任务队列组详情", "job-queue-detail.md"),
]

# 主样板：POST /api/task/job/create 的完整真实结构快照
SAMPLE_DETAIL = {
    "id": 468648941,
    "method": "POST",
    "path": "/api/task/job/create",
    "name": "创建任务",
    "description": "创建批处理任务。**注意**：points 数量上限 1000。",
    "updatedAt": "2026-09-01T10:00:00.000Z",
    "parameters": {
        "header": [
            {"name": "token", "type": "string", "required": True,
             "description": "平台 API Key", "sampleValue": "xxx-yyy"}
        ]
    },
    "requestBody": {
        "type": "application/json",
        "jsonSchema": {
            "type": "object",
            "required": ["deployment_task_id", "points"],
            "properties": {
                "deployment_task_id": {"type": "string", "title": "部署任务ID",
                                       "description": "关联的部署任务"},
                "points": {"type": "integer", "title": "节点数量", "description": "1-1000"},
                "env": {"type": "object", "title": "环境变量", "properties": {
                    "K1": {"type": "string"}}},
                "tags": {"type": "array", "items": {"type": "string"}, "title": "标签"}
            },
        },
        "examples": [{"name": "默认", "value": "{\"deployment_task_id\":\"d-1\",\"points\":2}"}],
    },
    "responses": [
        {"code": 200, "name": "OK", "jsonSchema": {
            "type": "object",
            "properties": {"code": {"type": "integer"}, "msg": {"type": "string"},
                           "data": {"type": "object", "properties": {
                               "task_id": {"type": "string"}}}}
        }}
    ],
    "responseExamples": [
        {"name": "成功", "data": "{\"code\":200,\"msg\":\"ok\",\"data\":{\"task_id\":\"j-123\"}}"}
    ],
}


def _make_detail(api_id, method, path, name):
    """从主样板派生其他端点的详情（结构一致，仅元信息不同）。"""
    d = json.loads(json.dumps(SAMPLE_DETAIL))
    d.update({"id": api_id, "method": method.upper(), "path": path, "name": name,
              "description": f"{name}接口（测试桩）"})
    if method.lower() == "get":
        d["requestBody"] = {}
    return d


def default_details():
    return {aid: _make_detail(aid, m, p, n) for aid, m, p, n, _ in JOB_ENDPOINTS}


SAMPLE_TREE = [
    {"type": "apiDetailFolder", "name": "任务管理",
     "children": [
         {"type": "apiDetail", "api": {"id": aid, "method": m, "path": p, "name": n}}
         for aid, m, p, n, _ in JOB_ENDPOINTS
     ]},
]


# ---------------------------------------------------------------- 工具

class FakeServer:
    """monkeypatch 掉 requests.Session.get，完全离线的可控测试服务器。"""

    def __init__(self, tree=None, details=None, fail_tree=False):
        self.tree = tree if tree is not None else SAMPLE_TREE
        self.details = details if details is not None else default_details()
        self.fail_tree = fail_tree
        self.tree_requests = 0

    def handler(self, url, params=None, timeout=None):
        class FakeResp:
            def __init__(self, payload, status=200):
                self._payload = payload
                self.status_code = status
                self.text = json.dumps(payload)

            def raise_for_status(self):
                if self.status_code >= 400:
                    raise RuntimeError(f"HTTP {self.status_code}")

            def json(self):
                if self.status_code >= 400:
                    raise ValueError("not json")
                return self._payload

        if "http-api-tree" in url:
            self.tree_requests += 1
            if self.fail_tree:
                return FakeResp({"success": False, "error": "simulated"}, 500)
            return FakeResp({"success": True, "data": self.tree})
        for part in url.split("/"):
            if part.isdigit():
                api_id = int(part)
                if api_id in self.details:
                    return FakeResp({"success": True, "data": self.details[api_id]})
        return FakeResp({"success": False, "error": "not found"}, 404)


class PersistFailSrv(FakeServer):
    """指定 id 的详情请求持续失败（重试耗尽）。"""

    def __init__(self, fail_ids, **kw):
        super().__init__(**kw)
        self.fail_ids = set(fail_ids)

    def handler(self, url, params=None, timeout=None):
        for part in url.split("/"):
            if part.isdigit() and int(part) in self.fail_ids:
                class R:
                    status_code = 503
                    def raise_for_status(self):
                        raise RuntimeError("HTTP 503 simulated")
                    def json(self):
                        raise ValueError()
                return R()
        return FakeServer.handler(self, url, params, timeout)


def inproc_run(args, server):
    """在本进程内 monkeypatch _session.get 后直接调 fa.main()，捕获 stdout。

    通过 SUANLI_SKILLS_ROOT 环境变量把仓库根定向到沙盒，确保不触碰真实仓库。
    """
    import fetch_apifox as fa
    import importlib
    import io
    import contextlib
    importlib.reload(fa)  # 重置模块级状态（重新读取环境变量）
    orig_get = fa._session.get
    fa._session.get = server.handler
    orig_argv, orig_exit = sys.argv, sys.exit

    class ExitErr(Exception):
        pass

    def fake_exit(code=0):
        raise ExitErr(code)

    sys.argv = ["fetch_apifox.py"] + args
    sys.exit = fake_exit
    sb_root = os.environ.get("SUANLI_SKILLS_ROOT")
    assert sb_root, "inproc_run 需先设置 SUANLI_SKILLS_ROOT 环境变量"
    exit_code = 0
    try:
        with contextlib.redirect_stdout(io.StringIO()) as so, \
                contextlib.redirect_stderr(io.StringIO()) as se:
            try:
                fa.main()
            except ExitErr as e:
                exit_code = int(e.args[0] or 0)
        return exit_code, so.getvalue(), se.getvalue()
    finally:
        sys.argv, sys.exit = orig_argv, orig_exit
        fa._session.get = orig_get


# ---------------------------------------------------------------- 沙盒工作区

def make_sandbox(name):
    """创建微型 skills 仓库沙盒（仅 suanli-job），并把 SUANLI_SKILLS_ROOT 指向它。"""
    sb = HERE / f".test-sandbox-{name}"
    if sb.exists():
        shutil.rmtree(sb)
    sb.mkdir()
    (sb / "scripts").mkdir()
    shutil.copy2(SCRIPT, sb / "scripts" / "fetch_apifox.py")
    (sb / "suanli-job" / "api").mkdir(parents=True)
    # 预置一个"旧版"文档，验证更新检出
    (sb / "suanli-job" / "api" / "job-create.md").write_text(
        "# 创建任务\n\n旧版静态内容（v1）\n", encoding="utf-8")
    # 预置一个孤儿文件，验证 prune
    (sb / "suanli-job" / "api" / "orphan-old.md").write_text(
        "# 孤儿文件\n", encoding="utf-8")
    os.environ["SUANLI_SKILLS_ROOT"] = str(sb)
    return sb


# ---------------------------------------------------------------- 测试用例

RESULTS = []


def record(name, passed, detail):
    RESULTS.append({"name": name, "passed": passed, "detail": detail})
    print(f"  [{'PASS' if passed else 'FAIL'}] {name} — {detail}")


def test_t1_normal_sync(sb):
    """T1 正常同步：全量拉取 6 端点 + 写盘 + 旧内容被替换。"""
    srv = FakeServer()
    code, out, _ = inproc_run(["--skill", "suanli-job"], srv)
    f = sb / "suanli-job" / "api" / "job-create.md"
    content = f.read_text(encoding="utf-8") if f.exists() else ""
    # 6 个映射文件必须全部落盘（orphan-old.md 此时仍在——prune 在 T9 才执行）
    expected = {fn for _, _, _, _, fn in JOB_ENDPOINTS}
    got = {p.name for p in (sb / "suanli-job" / "api").glob("*.md")}
    ok = (code == 0 and expected <= got
          and "旧版静态内容" not in content
          and "POST /api/task/job/create" in content)
    record("T1 正常同步（全量拉取写盘）", ok,
           f"exit={code}, 6 个映射文件全部落盘" if ok
           else f"exit={code}, missing={expected - got}, out={out[:300]}")


def test_t2_idempotent(sb):
    """T2 幂等：同内容二次同步全部 skip，mtime 不变。"""
    f = sb / "suanli-job" / "api" / "job-create.md"
    m1 = f.stat().st_mtime_ns
    time.sleep(0.05)
    srv = FakeServer()
    code, out, _ = inproc_run(["--skill", "suanli-job"], srv)
    m2 = f.stat().st_mtime_ns
    ok = code == 0 and m1 == m2 and "更新 0" in out and "失败 0" in out and "跳过 6" in out
    record("T2 幂等（内容一致跳过、mtime 不变）", ok,
           f"exit={code}, mtime 不变, 输出含 更新0/失败0/跳过6" if ok
           else f"exit={code}, mtime {m1}→{m2}, out={out[:300]}")


def test_t3_check_consistency(sb):
    """T3 --check 与 sync 一致：内容已最新时 check 报无更新 exit 0。"""
    srv = FakeServer()
    code, out, _ = inproc_run(["--skill", "suanli-job", "--check"], srv)
    ok = code == 0 and "全部文档均为最新" in out
    record("T3 --check 无误报（最新时 exit 0）", ok,
           f"exit={code}" if ok else f"exit={code}, out={out[:300]}")


def test_t4_refresh_on_change(sb):
    """T4 文档更新刷新：远端内容变化 → check 检出 → sync 重写。"""
    f = sb / "suanli-job" / "api" / "job-create.md"

    # 模拟远端更新：改 detail 的 description
    updated = default_details()
    updated[468648941]["description"] = "创建批处理任务。**v2 更新**：points 上限调整为 2000。"
    srv = FakeServer(details=updated)
    code1, out1, _ = inproc_run(["--skill", "suanli-job", "--check", "--refresh-cache"], srv)
    detected = code1 == 1 and "远端有更新" in out1

    code2, out2, _ = inproc_run(["--skill", "suanli-job", "--refresh-cache"], srv)
    new_content = f.read_text(encoding="utf-8")
    refreshed = code2 == 0 and "2000" in new_content

    ok = detected and refreshed
    record("T4 文档更新后数据刷新（check 检出 + sync 重写）", ok,
           f"check exit={code1} 检出更新, sync exit={code2} 新内容落盘" if ok
           else f"check exit={code1} out1={out1[:200]} sync exit={code2} out2={out2[:200]}")


def test_t5_tree_failure(sb):
    """T5 树拉取失败 → exit 2 + 本地文档保留。"""
    f = sb / "suanli-job" / "api" / "job-create.md"
    before = f.read_text(encoding="utf-8")
    m_before = f.stat().st_mtime_ns
    cache = sb / ".apifox-tree-cache.json"
    if cache.exists():
        cache.unlink()
    srv = FakeServer(fail_tree=True)
    code, out, _ = inproc_run(["--skill", "suanli-job", "--refresh-cache"], srv)
    after = f.read_text(encoding="utf-8")
    ok = (code == 2 and before == after
          and f.stat().st_mtime_ns == m_before
          and "保留本地现有文档" in out)
    record("T5 树拉取失败（exit 2 + 本地文档保留）", ok,
           f"exit={code}, 文档未被触碰" if ok else f"exit={code}, out={out[:300]}")


def test_t6_single_endpoint_failure(sb):
    """T6 单端点失败 → failed 列出、其余正常、旧文件保留。"""
    f_search = sb / "suanli-job" / "api" / "job-tasks.md"
    good_content = f_search.read_text(encoding="utf-8")
    m_good = f_search.stat().st_mtime_ns

    # job/search（999000112）详情持续 503；其余 5 个正常。
    # 注意：T4 曾把 job-create.md 同步成 v2 变体内容，此处远端桩是原版 →
    # job-create 会被"更新"回原版属预期行为，不计失败。
    time.sleep(0.05)
    srv_bad = PersistFailSrv(fail_ids={999000112})
    code, out, _ = inproc_run(["--skill", "suanli-job", "--refresh-cache"], srv_bad)
    preserve_ok = (f_search.read_text(encoding="utf-8") == good_content
                   and f_search.stat().st_mtime_ns == m_good)
    failed_listed = ("get /api/task/job/search" in out) and ("失败 1" in out)
    ok = code == 1 and preserve_ok and failed_listed
    record("T6 单端点失败（failed 列出、旧文件保留、exit 1）", ok,
           f"exit={code}, job-tasks.md 保留旧内容, failed 已列出, 其余端点正常" if ok
           else f"exit={code}, preserve={preserve_ok}, listed={failed_listed}, out={out[:400]}")


def test_t7_cache_corruption(sb):
    """T7 树缓存损坏 → 自动重拉恢复。"""
    cache = sb / ".apifox-tree-cache.json"
    cache.write_text("{ broken json !!!", encoding="utf-8")
    srv = FakeServer()
    code, out, _ = inproc_run(["--skill", "suanli-job"], srv)
    cache_ok = False
    try:
        data = json.loads(cache.read_text(encoding="utf-8"))
        cache_ok = bool(data.get("tree"))
    except Exception:
        pass
    ok = code == 0 and cache_ok and srv.tree_requests >= 1
    record("T7 缓存损坏自动恢复", ok,
           f"exit={code}, 缓存重写有效, 树请求 {srv.tree_requests} 次" if ok
           else f"exit={code}, cache_ok={cache_ok}, out={out[:300]}")


def test_t8_cache_hit(sb):
    """T8 缓存命中：10 分钟内不重复拉树。"""
    srv = FakeServer()
    code, out, _ = inproc_run(["--skill", "suanli-job"], srv)  # 应命中 T7 刚写的缓存
    ok = code == 0 and srv.tree_requests == 0
    record("T8 缓存命中（不发树请求）", ok,
           f"exit={code}, 树请求 0 次（用缓存）" if ok
           else f"exit={code}, 树请求 {srv.tree_requests} 次, out={out[:300]}")


def test_t9_prune(sb):
    """T9 孤儿文件清理。"""
    # 先重建孤儿文件（前面测试不会删它）
    orphan = sb / "suanli-job" / "api" / "orphan-old.md"
    orphan.write_text("# 孤儿文件\n", encoding="utf-8")
    srv = FakeServer()
    code, out, _ = inproc_run(["--skill", "suanli-job", "--prune"], srv)
    kept = sorted(p.name for p in (sb / "suanli-job" / "api").glob("*.md"))
    ok = code == 0 and not orphan.exists() and "orphan-old.md" in out and len(kept) == 6
    record("T9 孤儿文件清理（--prune）", ok,
           f"exit={code}, orphan-old.md 已删除, 保留 6 个映射文件" if ok
           else f"exit={code}, kept={kept}, out={out[:300]}")


def test_t10_render_unit():
    """T10 render_api_md 纯函数单测。"""
    import fetch_apifox as fa
    md = fa.render_api_md(SAMPLE_DETAIL, "任务管理")
    checks = [
        ("# 创建任务" in md, "标题"),
        ("POST /api/task/job/create" in md, "端点"),
        ("2026-09-01T10:00:00.000Z" in md, "updatedAt"),
        ("`deployment_task_id` `string` **(必填)**" in md, "必填字段"),
        ("`points` `integer`" in md, "字段类型"),
        ("deployment_task_id" in md.split("请求示例")[1] if "请求示例" in md else False, "请求示例"),
        ("task_id" in md.split("响应示例")[1] if "响应示例" in md else False, "响应示例"),
        ("fetch_apifox.py" in md, "脚注"),
        ("header 参数" in md, "header 参数表"),
        ("2026-09-24" not in md.split("来源")[0], "无本地时间戳污染正文"),
    ]
    failed = [label for ok_, label in checks if not ok_]
    record("T10 render_api_md 单测（10 项断言）", not failed,
           "全部通过" if not failed else f"失败项: {failed}")


# ---------------------------------------------------------------- 主流程

def main():
    print("=" * 70)
    print("fetch_apifox.py 测试套件")
    print("=" * 70)

    # 语法检查
    p = subprocess.run([PY, "-m", "py_compile", str(SCRIPT)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        print(f"[FAIL] 语法检查未通过：\n{p.stderr}")
        record("T0 语法检查", False, p.stderr[:200])
    else:
        record("T0 语法检查", True, "py_compile 通过")

    # 离线沙盒测试（T1-T9，全部走 FakeServer，不依赖真实网络、不触碰真实仓库）
    sb = make_sandbox("main")
    sys.path.insert(0, str(SCRIPT.parent))
    try:
        test_t1_normal_sync(sb)
        test_t2_idempotent(sb)
        test_t3_check_consistency(sb)
        test_t4_refresh_on_change(sb)
        test_t5_tree_failure(sb)
        test_t6_single_endpoint_failure(sb)
        test_t7_cache_corruption(sb)
        test_t8_cache_hit(sb)
        test_t9_prune(sb)
        test_t10_render_unit()
    finally:
        os.environ.pop("SUANLI_SKILLS_ROOT", None)  # 清理：避免影响后续真实运行

    # 汇总
    passed = sum(1 for r in RESULTS if r["passed"])
    total = len(RESULTS)
    print("\n" + "=" * 70)
    print(f"结果：{passed}/{total} 通过")
    print("=" * 70)

    # 报告落盘
    report = {
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "script": str(SCRIPT),
        "python": PY,
        "mode": "offline-sandbox（FakeServer mock，沙盒目录隔离）",
        "passed": passed,
        "total": total,
        "cases": RESULTS,
    }
    (HERE / "test-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = ["# fetch_apifox.py 本地测试报告", "",
             f"- 时间：{report['time']}",
             f"- 被测脚本：`{SCRIPT}`",
             f"- 测试方式：离线沙盒（FakeServer mock 网络 + SUANLI_SKILLS_ROOT 隔离，不触碰真实仓库）", "",
             f"## 结果：{passed}/{total} 通过", "",
             "| # | 用例 | 结果 | 说明 |", "| --- | --- | --- | --- |"]
    for i, r in enumerate(RESULTS, 1):
        lines.append(f"| T{i-1} | {r['name']} | {'✅' if r['passed'] else '❌'} | {r['detail']} |")
    (HERE / "test-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"报告已写入: {HERE / 'test-report.md'}")

    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
