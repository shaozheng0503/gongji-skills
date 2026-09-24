#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
e2e_platform_test.py — 按官网场景对共绩算力平台做真实端到端调用测试

场景来源：https://docs.suanli.cn/skills
  「确认已接通」：列出弹性部署任务 / 查 Job 批处理任务状态
  + 5 个 skill 各取代表性只读端点

只做只读操作（GET / 查询类 POST），不创建、不停止、不删除任何资源。
凭证：SUANLI_TOKEN（简易模式，平台 API 密钥）。

用法：
  set SUANLI_TOKEN=xxx
  python e2e_platform_test.py
结果：写 e2e-report.json 到本目录，控制台输出摘要。
"""

import json
import os
import sys
import time
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent
BASE = os.environ.get("SUANLI_BASE_URL", "https://openapi.suanli.cn")
TOKEN = os.environ.get("SUANLI_TOKEN") or ""
REPO = HERE.parent

UA = "suanli-skills-e2e/1.0"


def call(method, path, query=None, body=None, extra_headers=None):
    """简易模式（Token）调用。返回 (status_code, json_or_text, elapsed_ms)。"""
    url = BASE + "/api" + path
    headers = {
        "token": TOKEN,
        "timestamp": str(int(time.time() * 1000)),
        "version": "1.0.0",
        "User-Agent": UA,
    }
    if extra_headers:
        headers.update(extra_headers)
    if method == "GET":
        r = requests.get(url, params=query, headers=headers, timeout=30)
    else:
        headers["Content-Type"] = "application/json"
        r = requests.post(url, json=body, headers=headers, timeout=30)
    try:
        data = r.json()
    except ValueError:
        data = {"_raw": r.text[:500]}
    return r.status_code, data, int(r.elapsed.total_seconds() * 1000)


def check_response(res, scenario, skill, endpoint_doc):
    """统一判定：HTTP 200 + code=0000（或 data 非 null）→ 通过。"""
    status, data, ms = res
    code = data.get("code") if isinstance(data, dict) else None
    ok = status == 200 and str(code) == "0000"
    # data 摘要（截断，避免报告过大）
    d = data.get("data") if isinstance(data, dict) else None
    summary = ""
    if isinstance(d, dict):
        summary = json.dumps({k: (f"<{type(v).__name__} len={len(v)}>" if isinstance(v, (list, dict)) else v)
                              for k, v in list(d.items())[:6]}, ensure_ascii=False)
    elif isinstance(d, list):
        summary = f"list len={len(d)}"
    return {
        "scenario": scenario, "skill": skill, "endpoint": endpoint_doc,
        "ok": ok, "http": status, "code": code, "elapsed_ms": ms,
        "message": (data.get("message") if isinstance(data, dict) else "")[:120],
        "data_summary": summary[:300],
    }


def main():
    if not TOKEN:
        print("[FATAL] 未设置 SUANLI_TOKEN 环境变量")
        sys.exit(3)

    results = []
    t0 = time.time()

    # ---- 场景 0：凭证与连通性（官网「确认已接通」前置）----
    r = call("GET", "/deployment/task/search", query={"page": 1, "page_size": 5})
    results.append(check_response(r, "官网·确认已接通：列出弹性部署任务（GET /deployment/task/search）",
                                  "suanli-deployment", "api/task-list.md"))

    r = call("GET", "/task/job/search", query={"page": 1, "page_size": 5})
    results.append(check_response(r, "官网·确认已接通：查 Job 批处理任务状态（GET /task/job/search）",
                                  "suanli-job", "api/job-tasks.md"))

    # ---- suanli-deployment：资源查询（只读）----
    r = call("GET", "/deployment/resource/search",
             query={"task_type": "Deployment", "device_type": "GpuDevice"})
    results.append(check_response(r, "弹性部署·查资源（GET /deployment/resource/search）",
                                  "suanli-deployment", "api/resource.md"))

    # ---- suanli-deployment：节点列表（查第一页，无 task_id 则用空任务列表跳过）----
    # （task/points 需要 task_id；从上一步任务列表里取一个，没有就标记 SKIP）
    r_tasks = call("GET", "/deployment/task/search", query={"page": 1, "page_size": 5})
    task_list = []
    try:
        task_list = (((r_tasks[1] or {}).get("data") or {}).get("results") or [])
    except Exception:
        pass
    if task_list:
        tid = task_list[0].get("task_id") or task_list[0].get("id")
        r = call("GET", "/deployment/task/points", query={"task_id": tid, "page": 1, "page_size": 5})
        results.append(check_response(r, f"弹性部署·查节点列表（GET /deployment/task/points?task_id={tid}）",
                                      "suanli-deployment", "api/node-list.md"))
    else:
        results.append({"scenario": "弹性部署·查节点列表（无任务可查，跳过）", "skill": "suanli-deployment",
                        "endpoint": "api/node-list.md", "ok": None, "http": None, "code": None,
                        "elapsed_ms": None, "message": "账户下无部署任务，跳过节点查询", "data_summary": ""})

    # ---- suanli-job：任务队列（只读）----
    r = call("GET", "/job/queue/group/search", query={"queue_id": 1, "page": 1, "page_size": 5})
    results.append(check_response(r, "Job·查任务队列组（GET /job/queue/group/search）",
                                  "suanli-job", "api/job-queue-list.md"))

    # ---- suanli-metal：裸金属订单列表（查询类 POST，只读）----
    r = call("POST", "/output/v2/device_order/get_order_list_v2",
             body={"page": 1, "page_size": 5, "conditional": {"condition": ""}})
    results.append(check_response(r, "裸金属·查订单列表（POST get_order_list_v2）",
                                  "suanli-metal", "api/order-list.md"))

    # ---- suanli-nas-storage：存储用量概览 + 卷列表（只读）----
    r = call("GET", "/storage/nas/v1/summary")
    results.append(check_response(r, "集群存储·用量概览（GET /storage/nas/v1/summary）",
                                  "suanli-nas-storage", "api/nas-summary.md"))

    r = call("GET", "/storage/nas/v1/list", query={"page": 1, "page_size": 5})
    results.append(check_response(r, "集群存储·卷列表（GET /storage/nas/v1/list）",
                                  "suanli-nas-storage", "api/nas-list.md"))

    # ---- suanli-image-preheat：镜像预热区域 + 任务列表（只读）----
    r = call("GET", "/task/image_preheat/get_regions")
    results.append(check_response(r, "镜像预热·查区域（GET /task/image_preheat/get_regions）",
                                  "suanli-image-preheat", "api/region-query.md"))

    r = call("GET", "/task/image_preheat/search", query={"page": 1, "page_size": 5})
    results.append(check_response(r, "镜像预热·查任务列表（GET /task/image_preheat/search）",
                                  "suanli-image-preheat", "api/image-preheat-list.md"))

    # ---- 汇总 ----
    passed = [x for x in results if x["ok"] is True]
    failed = [x for x in results if x["ok"] is False]
    skipped = [x for x in results if x["ok"] is None]

    report = {
        "time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "base_url": BASE,
        "total_elapsed_ms": int((time.time() - t0) * 1000),
        "passed": len(passed), "failed": len(failed), "skipped": len(skipped),
        "results": results,
    }
    (HERE / "e2e-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print("=" * 70)
    print("共绩算力平台端到端测试（官网场景）")
    print("=" * 70)
    for x in results:
        if x["ok"] is True:
            print(f"  [PASS] {x['scenario']}  ({x['elapsed_ms']}ms, code={x['code']})")
        elif x["ok"] is None:
            print(f"  [SKIP] {x['scenario']}  ({x['message']})")
        else:
            print(f"  [FAIL] {x['scenario']}  (http={x['http']}, code={x['code']}, msg={x['message']})")
    print("-" * 70)
    print(f"通过 {len(passed)} / 失败 {len(failed)} / 跳过 {len(skipped)} · 总耗时 {report['total_elapsed_ms']}ms")
    print(f"报告：{HERE / 'e2e-report.json'}")
    sys.exit(0 if not failed else 1)


if __name__ == "__main__":
    main()
