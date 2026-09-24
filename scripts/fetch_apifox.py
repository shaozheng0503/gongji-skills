#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_apifox.py — 共绩算力 Open API skills 的 Apifox 文档运行时同步器

将 Apifox 分享文档（s.apifox.cn）的实时内容拉取为本地 api/*.md，
替代手动导出的静态文件。Apifox 官方文档更新后无需手动改造 skills。

数据源（Apifox 官网渲染分享页所用公开 JSON 接口，无需鉴权）：
  GET {SHARE_HOST}/api/v1/shared-docs/{shareId}/http-api-tree     → API 树
  GET {SHARE_HOST}/api/v1/shared-docs/{shareId}/http-apis/{apiId}  → 端点详情

用法：
  python fetch_apifox.py                    # 同步本 skill（或 --all 全部）
  python fetch_apifox.py --check            # 只检查远端是否有更新（不写文件）
  python fetch_apifox.py --force            # 强制重写全部（忽略内容哈希比对）
  python fetch_apifox.py --refresh-cache    # 忽略本地树缓存，重新拉取 API 树
  python fetch_apifox.py --prune            # 删除映射表之外、不再被远端引用的本地 md

环境变量（可选，正常无需设置）：
  SUANLI_SKILLS_ROOT     覆盖 skills 仓库根目录（默认按脚本位置自动推断）
  SUANLI_APIFOX_HOST     覆盖分享文档域名（代理/测试用）
  SUANLI_APIFOX_ID       覆盖分享文档 ID

容错设计：
  - 树拉取失败            → 打印告警，exit 2（保留本地现有文档，本次中止）
  - 单个端点详情拉取失败  → 保留该端点旧文件，计入 failed 列表，不中断其余端点（exit 1）
  - 网络重试              → 每个请求指数退避重试（默认 3 次）
  - 内容哈希              → 远端内容与本地一致时跳过写入（mtime 不变，幂等）
  - --check               → 有更新或失败 exit 1，全部最新 exit 0
"""

import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path
from urllib.parse import urljoin

import requests

# ---------------------------------------------------------------- 常量

# 环境变量可覆盖（主要用于异常场景测试 / 代理切换，正常无需设置）
SHARE_HOST = os.environ.get("SUANLI_APIFOX_HOST", "https://s.apifox.cn")
SHARE_ID = os.environ.get(
    "SUANLI_APIFOX_ID", "6aa360d3-d8f2-471e-b841-3a35c33a7b7c"
)  # 共绩算力 Open API 分享文档
API_VERSION_HEADER = "1.0.0"

RETRY_TIMES = 3          # 单请求重试次数
RETRY_BACKOFF = 1.5      # 指数退避基数（秒）
TIMEOUT = 30             # 单请求超时（秒）

TREE_CACHE = ".apifox-tree-cache.json"   # 树缓存文件名（存于仓库根）
MANIFEST = ".apifox-sync-manifest.json"  # 同步清单（记录每次同步结果）

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) suanli-skills-sync/1.0"

# ---------------------------------------------------------------- 端点映射表
# (method, path) → 该 skill 下 api/ 中的文件名。
# 映射表覆盖所有 5 个 skill 的既有静态文件名，保持 SKILL.md 引用向后兼容。
# 值为 None 表示远端存在但本地 skill 从未收录（同步时可选拉取，--include-new 控制）。

ENDPOINT_MAP = {
    # ---- suanli-deployment / suanli-job 共享 ----
    ("get", "/api/deployment/resource/search"): ("suanli-deployment", "resource.md"),
    ("get", "/api/storage/get_storage"): ("suanli-deployment", "object-storage.md"),
    ("get", "/api/billing/get_billing_record"): ("suanli-deployment", "fee-time-query.md"),
    ("get", "/api/billing/get_task_billing_record"): ("suanli-deployment", "fee-task-query.md"),
    ("get", "/api/deployment/task/points"): ("suanli-deployment", "node-list.md"),
    ("get", "/api/deployment/task/point_log"): ("suanli-deployment", "node-log.md"),
    ("get", "/api/deployment/task/pod_event"): ("suanli-deployment", "node-event.md"),
    ("post", "/api/deployment/task/delete_pod"): ("suanli-deployment", "node-delete.md"),
    ("post", "/api/deployment/task/change_points"): ("suanli-deployment", "node-num-edit.md"),

    # ---- suanli-deployment 独有 ----
    ("get", "/api/deployment/task/search"): ("suanli-deployment", "task-list.md"),
    ("get", "/api/deployment/task/detail"): ("suanli-deployment", "task-detail.md"),
    ("post", "/api/deployment/task/create"): ("suanli-deployment", "task-create.md"),
    ("post", "/api/deployment/task/update"): ("suanli-deployment", "task-edit.md"),
    ("post", "/api/deployment/task/pause"): ("suanli-deployment", "task-puase.md"),  # 历史拼写保留
    ("post", "/api/deployment/task/recover"): ("suanli-deployment", "task-recover.md"),
    ("post", "/api/deployment/task/stop"): ("suanli-deployment", "task-stop.md"),

    # ---- suanli-job 独有 ----
    ("get", "/api/task/job/search"): ("suanli-job", "job-tasks.md"),
    ("get", "/api/task/job/detail"): ("suanli-job", "job-detail.md"),
    ("post", "/api/task/job/create"): ("suanli-job", "job-create.md"),
    ("post", "/api/task/job/stop"): ("suanli-job", "job-stop.md"),
    ("get", "/api/job/queue/group/search"): ("suanli-job", "job-queue-list.md"),
    ("get", "/api/job/queue/group/detail"): ("suanli-job", "job-queue-detail.md"),

    # ---- suanli-metal ----
    ("post", "/api/output/v2/device-output/page_list_product_single_v2"): ("suanli-metal", "single-product-list.md"),
    ("post", "/api/output/v2/device-output/page_list_product_network_v2"): ("suanli-metal", "group-product-list.md"),
    ("post", "/api/output/v2/device_order/buy_v2"): ("suanli-metal", "order-create.md"),
    ("post", "/api/output/v2/device_order/get_order_list_v2"): ("suanli-metal", "order-list.md"),
    ("post", "/api/output/v2/device-output/list_rent_device_single_v2"): ("suanli-metal", "rent-single-device-list.md"),
    ("post", "/api/output/v2/device-output/list_rent_device_network_v2"): ("suanli-metal", "rent-group-device-list.md"),
    ("post", "/api/output/v2/device_order/get_device_details_v2"): ("suanli-metal", "device-detail.md"),
    ("post", "/api/output/v2/auto_renew_device_config/set_auto_renew_config"): ("suanli-metal", "auto-renew.md"),
    ("post", "/api/output/v2/auto_renew_device_config/delete_auto_renew_config"): ("suanli-metal", "cancel-auto-renew.md"),

    # ---- suanli-nas-storage ----
    ("get", "/api/storage/nas/v1/summary"): ("suanli-nas-storage", "nas-summary.md"),
    ("get", "/api/storage/nas/v1/dictionaries"): ("suanli-nas-storage", "nas-dictionaries.md"),
    ("get", "/api/storage/nas/v1/pre-create"): ("suanli-nas-storage", "nas-pre-create.md"),
    ("get", "/api/storage/nas/v1/list"): ("suanli-nas-storage", "nas-list.md"),
    ("post", "/api/storage/nas/v1/create"): ("suanli-nas-storage", "nas-create.md"),
    ("post", "/api/storage/nas/v1/expand"): ("suanli-nas-storage", "nas-expand.md"),
    ("post", "/api/storage/nas/v1/delete"): ("suanli-nas-storage", "nas-delete.md"),
    ("post", "/api/storage/nas/v1/rename"): ("suanli-nas-storage", "nas-rename.md"),
    ("get", "/api/storage/nas/v1/s3/list"): ("suanli-nas-storage", "s3-list.md"),
    ("get", "/api/storage/nas/v1/s3/detail"): ("suanli-nas-storage", "s3-detail.md"),
    ("post", "/api/storage/nas/v1/encrypt/s3/create"): ("suanli-nas-storage", "s3-create.md"),
    ("post", "/api/storage/nas/v1/encrypt/s3/retry"): ("suanli-nas-storage", "s3-retry.md"),
    ("post", "/api/storage/nas/v1/s3/delete"): ("suanli-nas-storage", "s3-delete.md"),
    ("post", "/api/storage/nas/v1/s3/stop"): ("suanli-nas-storage", "s3-stop.md"),
    ("post", "/api/storage/nas/v1/encrypt/s3/check"): ("suanli-nas-storage", "s3-check.md"),
    ("post", "/api/storage/nas/v1/sftp/obtain"): ("suanli-nas-storage", "sftp-obtain.md"),
    ("post", "/api/storage/nas/v1/sftp/destroy"): ("suanli-nas-storage", "sftp-destroy.md"),

    # ---- suanli-image-preheat ----
    ("get", "/api/task/image_preheat/get_regions"): ("suanli-image-preheat", "region-query.md"),
    ("get", "/api/task/image_preheat/search"): ("suanli-image-preheat", "image-preheat-list.md"),
    ("get", "/api/task/image_preheat/detail"): ("suanli-image-preheat", "image-preheat-detail.md"),
    ("post", "/api/task/image_preheat/create"): ("suanli-image-preheat", "image-preheat-create.md"),
    ("post", "/api/task/image_preheat/update"): ("suanli-image-preheat", "image-preheat-update.md"),  # 静态版曾误为 create 副本，此处接真正的 update
    ("post", "/api/task/image_preheat/stop"): ("suanli-image-preheat", "image-preheat-stop.md"),
}

# deployment 与 job 共享的 9 份文档：同步 deployment 侧后复制到 job 侧
SHARED_TO_JOB = [
    "resource.md", "object-storage.md", "fee-time-query.md", "fee-task-query.md",
    "node-list.md", "node-log.md", "node-event.md", "node-delete.md", "node-num-edit.md",
]

SKILLS = ["suanli-deployment", "suanli-job", "suanli-metal", "suanli-nas-storage", "suanli-image-preheat"]

# ---------------------------------------------------------------- HTTP 层

_session = requests.Session()
_session.headers.update({"Accept": "application/json", "User-Agent": UA})


def _get_json(url: str, params: dict = None) -> dict:
    """带重试的 GET，返回 JSON dict；重试耗尽抛出最后异常。"""
    last_exc = None
    for attempt in range(1, RETRY_TIMES + 1):
        try:
            r = _session.get(url, params=params, timeout=TIMEOUT)
            r.raise_for_status()
            return r.json()
        except (requests.RequestException, ValueError) as exc:
            last_exc = exc
            if attempt < RETRY_TIMES:
                time.sleep(RETRY_BACKOFF ** attempt)
    raise last_exc


# ---------------------------------------------------------------- 树拉取与缓存

def fetch_tree(cache_path: Path, refresh: bool, max_age_sec: int = 600) -> list:
    """拉取 API 树。优先用 10 分钟内的本地缓存；refresh=True 或缓存失效时重新拉取。"""
    if not refresh and cache_path.exists():
        try:
            cache = json.loads(cache_path.read_text(encoding="utf-8"))
            if time.time() - cache.get("fetched_at", 0) < max_age_sec:
                return cache["tree"]
        except (json.JSONDecodeError, KeyError, OSError):
            pass  # 缓存损坏 → 重新拉取

    url = f"{SHARE_HOST}/api/v1/shared-docs/{SHARE_ID}/http-api-tree"
    payload = _get_json(url)
    if not payload.get("success"):
        raise RuntimeError(f"API 树拉取失败: {payload}")
    tree = payload["data"]

    try:
        cache_path.write_text(
            json.dumps({"fetched_at": time.time(), "tree": tree}, ensure_ascii=False),
            encoding="utf-8",
        )
    except OSError:
        pass  # 缓存写失败不影响主流程
    return tree


def flatten_tree(tree: list) -> list:
    """树 → [(api_id, method, path, name, folder_path)] 扁平列表。"""
    out = []

    def walk(nodes, prefix):
        for n in nodes or []:
            ntype = n.get("type")
            if ntype == "apiDetailFolder":
                walk(n.get("children"), prefix + [n.get("name", "")])
            elif ntype == "apiDetail":
                api = n.get("api") or {}
                out.append({
                    "id": api.get("id"),
                    "method": (api.get("method") or "").lower(),
                    "path": api.get("path") or "",
                    "name": api.get("name") or "",
                    "folder": "/".join(prefix),
                })

    walk(tree, [])
    return out


# ---------------------------------------------------------------- markdown 生成

def _schema_to_md_lines(schema: dict, indent: int = 0) -> list:
    """把 Apifox jsonSchema 结构转成 markdown 嵌套列表（精简字段视图）。"""
    lines = []
    pad = "  " * indent
    if not isinstance(schema, dict):
        return lines
    stype = schema.get("type")
    if isinstance(stype, list):
        stype = " | ".join(str(t) for t in stype)
    if stype == "array":
        item = schema.get("items", {})
        lines.append(f"{pad}- **array<{_simple_type(item)}>**")
        lines.extend(_schema_to_md_lines(item, indent + 1))
        return lines
    if stype == "object" or "properties" in schema:
        props = schema.get("properties", {})
        order = schema.get("x-apifox-orders") or list(props.keys())
        required = set(schema.get("required") or [])
        for key in order:
            if key not in props:
                continue
            sub = props[key]
            sub_type = _simple_type(sub)
            req = " **(必填)**" if key in required else ""
            title = sub.get("title") or ""
            desc = (sub.get("description") or "").strip().replace("\n", " ")
            enum = sub.get("enum")
            enum_str = ""
            if isinstance(enum, list):
                enum_str = f"，枚举: `{'`/`'.join(str(e) for e in enum[:12])}`"
            meta = " — ".join(x for x in [title, desc] if x)
            meta = (f"：{meta}" if meta else "")
            lines.append(f"{pad}- `{key}` `{sub_type}`{req}{meta}{enum_str}")
            lines.extend(_schema_to_md_lines(sub, indent + 1))
        return lines
    # 叶子节点
    return lines


def _simple_type(schema: dict) -> str:
    if not isinstance(schema, dict):
        return "any"
    t = schema.get("type")
    if isinstance(t, list):
        t = " | ".join(str(x) for x in t)
    return str(t or "any")


def render_api_md(detail: dict, folder: str) -> str:
    """把 Apifox 端点详情 JSON 渲染为 markdown 文档（与旧静态版同结构的信息量）。"""
    method = (detail.get("method") or "").upper()
    path = detail.get("path") or ""
    name = detail.get("name") or ""
    desc = (detail.get("description") or "").strip()
    updated = detail.get("updatedAt") or ""

    lines = [f"# {name}", ""]
    lines.append(f"> 来源：Apifox 官方文档（实时同步） · 分组：{folder}")
    if updated:
        lines.append(f"> 远端最后更新：{updated}")
    lines.append(f"> 端点：`{method} {path}`")
    lines.append("")
    if desc:
        lines.append(desc)
        lines.append("")

    # 请求参数
    params = detail.get("parameters") or {}
    for loc in ("query", "header", "path", "cookie"):
        items = params.get(loc) or []
        if not items:
            continue
        lines.append(f"## {loc} 参数")
        lines.append("")
        lines.append("| 参数 | 类型 | 必填 | 说明 |")
        lines.append("| --- | --- | --- | --- |")
        for p in items:
            ptype = p.get("type") or _simple_type(p.get("schema") or {})
            req = "是" if p.get("required") else "否"
            pdesc = (p.get("description") or "").strip().replace("\n", " ")
            sample = p.get("sampleValue")
            if sample not in (None, ""):
                pdesc = f"{pdesc}（示例：{sample}）".strip()
            lines.append(f"| `{p.get('name')}` | {ptype} | {req} | {pdesc or '—'} |")
        lines.append("")

    # 请求体
    body = detail.get("requestBody") or {}
    if body.get("type") not in (None, "none"):
        lines.append("## 请求体")
        lines.append("")
        lines.append(f"Content-Type: `{body.get('type')}`")
        lines.append("")
        js = body.get("jsonSchema")
        if js:
            schema_lines = _schema_to_md_lines(js)
            if schema_lines:
                lines.extend(schema_lines)
                lines.append("")
        examples = body.get("examples") or []
        for ex in examples:
            lines.append(f"**请求示例（{ex.get('name') or '示例'}）**：")
            lines.append("")
            lines.append("```json")
            try:
                parsed = json.loads(ex.get("value") or "{}")
                lines.append(json.dumps(parsed, ensure_ascii=False, indent=2))
            except (json.JSONDecodeError, TypeError):
                lines.append(str(ex.get("value") or ""))
            lines.append("```")
            lines.append("")

    # 响应
    responses = detail.get("responses") or []
    for resp in responses:
        code = resp.get("code")
        lines.append(f"## 响应（{code}）")
        lines.append("")
        rjs = resp.get("jsonSchema")
        if rjs:
            schema_lines = _schema_to_md_lines(rjs)
            if schema_lines:
                lines.extend(schema_lines)
                lines.append("")
        name_ = resp.get("name")
        if name_:
            lines.append(f"响应名：{name_}")
            lines.append("")

    response_examples = detail.get("responseExamples") or []
    for rex in response_examples:
        lines.append(f"**响应示例（{rex.get('name') or '示例'}）**：")
        lines.append("")
        lines.append("```json")
        try:
            parsed = json.loads(rex.get("data") or "{}")
            lines.append(json.dumps(parsed, ensure_ascii=False, indent=2))
        except (json.JSONDecodeError, TypeError):
            lines.append(str(rex.get("data") or ""))
        lines.append("```")
        lines.append("")

    # 元信息脚注（不含本地生成时间戳——内容需确定性，否则哈希幂等比对永远失败）
    lines.append("---")
    lines.append(f"*本文档由 fetch_apifox.py 从 Apifox 分享文档 {SHARE_ID} 实时同步生成；"
                 f"同步时间见仓库根 {MANIFEST}*")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------- 同步主流程

def _md5(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def sync(repo_root: Path, skill: str, tree_flat: list, check_only: bool = False,
         force: bool = False, include_new: bool = False) -> dict:
    """
    同步一个 skill 的 api/*.md。
    返回 {written: [...], skipped: [...], failed: [...], new_remote: [...]}。
    check_only=True 时只比对不写盘。
    """
    result = {"written": [], "skipped": [], "failed": [], "new_remote": []}
    by_key = {(a["method"], a["path"]): a for a in tree_flat}

    # 该 skill 涉及的 (endpoint → 文件) 映射
    targets = {k: v for k, v in ENDPOINT_MAP.items() if v[0] == skill}

    for (method, path), (_skill, filename) in sorted(targets.items(), key=lambda kv: kv[1][1]):
        api_meta = by_key.get((method, path))
        if api_meta is None:
            result["failed"].append(f"{method} {path} → 远端 API 树中不存在")
            continue
        try:
            detail = _get_json(
                f"{SHARE_HOST}/api/v1/shared-docs/{SHARE_ID}/http-apis/{api_meta['id']}"
            )["data"]
        except Exception as exc:  # 单端点失败 → 保留旧文件
            result["failed"].append(f"{method} {path} → {type(exc).__name__}: {exc}")
            continue

        md = render_api_md(detail, api_meta["folder"])
        out_path = repo_root / _skill / "api" / filename

        if not check_only:
            if not force and out_path.exists():
                try:
                    existing = out_path.read_text(encoding="utf-8")
                except (OSError, UnicodeDecodeError):
                    existing = None
                if existing is not None and _md5(existing) == _md5(md):
                    result["skipped"].append(f"{filename}（内容一致）")
                    continue
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(md, encoding="utf-8", newline="\n")
            result["written"].append(filename)
        else:
            # check 模式：与本地文件比对，输出有无差异
            if out_path.exists():
                existing = out_path.read_text(encoding="utf-8")
                if _md5(existing) == _md5(md):
                    result["skipped"].append(f"{filename}")
                else:
                    result["written"].append(f"{filename}（远端有更新）")
            else:
                result["written"].append(f"{filename}（本地缺失）")

    # 共享文档复制：deployment 侧同步后复制到 job 侧（仅当 job skill 同仓库存在时）
    if skill == "suanli-deployment" and not check_only and (repo_root / "suanli-job").is_dir():
        for shared in SHARED_TO_JOB:
            src = repo_root / "suanli-deployment" / "api" / shared
            dst = repo_root / "suanli-job" / "api" / shared
            if src.exists():
                try:
                    content = src.read_text(encoding="utf-8")
                    if not dst.exists() or _md5(dst.read_text(encoding="utf-8")) != _md5(content):
                        dst.parent.mkdir(parents=True, exist_ok=True)
                        dst.write_text(content, encoding="utf-8", newline="\n")
                        result["written"].append(f"suanli-job/api/{shared}（共享复制）")
                    else:
                        result["skipped"].append(f"suanli-job/api/{shared}（内容一致）")
                except OSError as exc:
                    result["failed"].append(f"共享复制 {shared} → {exc}")

    # 提示远端新增端点（映射表未收录）
    if include_new:
        mapped = set(ENDPOINT_MAP.keys())
        for a in tree_flat:
            if (a["method"], a["path"]) not in mapped:
                result["new_remote"].append(f"{a['method']} {a['path']} — {a['name']}")
    return result


def prune(repo_root: Path) -> list:
    """删除映射表覆盖不到的本地 api/*.md（防止改名后残留孤儿文件）。返回删除列表。"""
    removed = []
    protected = {v[1] for v in ENDPOINT_MAP.values()}
    protected.add(".apifox-tree-cache.json")
    for skill in SKILLS:
        api_dir = repo_root / skill / "api"
        if not api_dir.is_dir():
            continue
        for f in api_dir.glob("*.md"):
            if f.name not in protected:
                f.unlink()
                removed.append(f"{skill}/api/{f.name}")
    return removed


def main():
    ap = argparse.ArgumentParser(description="Apifox → skills api/*.md 运行时同步器")
    ap.add_argument("--skill", choices=SKILLS, help="只同步指定 skill（默认全部）")
    ap.add_argument("--all", action="store_true", help="同步全部 skill（默认行为）")
    ap.add_argument("--check", action="store_true", help="只检查更新，不写文件")
    ap.add_argument("--force", action="store_true", help="忽略哈希比对强制重写")
    ap.add_argument("--refresh-cache", action="store_true", help="忽略本地树缓存重新拉取")
    ap.add_argument("--include-new", action="store_true", help="列出远端新增、映射未收录的端点")
    ap.add_argument("--prune", action="store_true", help="删除映射外孤儿 md 文件")
    args = ap.parse_args()

    # 仓库根：环境变量优先；否则按脚本位置推断
    env_root = os.environ.get("SUANLI_SKILLS_ROOT")
    if env_root:
        repo_root = Path(env_root)
        target_skills = [args.skill] if args.skill else SKILLS
    else:
        repo_root = Path(__file__).resolve().parent.parent
        # 兼容两种部署位置：skill 内 scripts/（repo_root=单 skill）或仓库根 scripts/（repo_root=仓库）
        # 通过探测目录名自动判断
        if repo_root.name in SKILLS:
            target_skills = [repo_root.name]
            repo_root = repo_root.parent
        else:
            target_skills = [args.skill] if args.skill else SKILLS

    cache_path = repo_root / TREE_CACHE

    try:
        tree = fetch_tree(cache_path, refresh=args.refresh_cache)
    except Exception as exc:
        print(f"[WARN] API 树拉取失败：{type(exc).__name__}: {exc}")
        print("[INFO] 保留本地现有文档，本次同步中止。可稍后重试或检查网络。")
        sys.exit(2)

    tree_flat = flatten_tree(tree)
    print(f"[INFO] Apifox 树已加载：{len(tree_flat)} 个端点"
          f"（缓存：{cache_path.name}）")

    if args.prune:
        removed = prune(repo_root)
        print(f"[PRUNE] 删除孤儿文件 {len(removed)} 个：{removed or '无'}")

    all_failed = []
    any_written = False
    manifest = {"time": time.strftime("%Y-%m-%d %H:%M:%S"), "mode": "check" if args.check else "sync", "skills": {}}

    for skill in target_skills:
        r = sync(repo_root, skill, tree_flat, check_only=args.check,
                 force=args.force, include_new=args.include_new)
        manifest["skills"][skill] = {k: len(v) for k, v in r.items()}
        all_failed.extend(r["failed"])
        status = "check" if args.check else "sync"
        print(f"[{status}] {skill}: 更新 {len(r['written'])} / 跳过 {len(r['skipped'])} / 失败 {len(r['failed'])}")
        for w in r["written"]:
            print(f"    W {w}")
        for f in r["failed"]:
            print(f"    F {f}")
        if r["new_remote"]:
            print(f"    [NEW] 远端未收录端点 {len(r['new_remote'])} 个（--include-new 查看）")
            for n in r["new_remote"]:
                print(f"    N {n}")
        if r["written"]:
            any_written = True

    # 落 manifest（同步模式）
    if not args.check:
        try:
            (repo_root / MANIFEST).write_text(
                json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        except OSError:
            pass

    if all_failed:
        print(f"[WARN] {len(all_failed)} 个端点同步失败（本地旧文档保留可用）")
        sys.exit(1)
    if args.check:
        print(f"[CHECK] {'有更新可拉取' if any_written else '全部文档均为最新'}")
        sys.exit(1 if any_written else 0)
    print("[DONE] 同步完成")


if __name__ == "__main__":
    main()
