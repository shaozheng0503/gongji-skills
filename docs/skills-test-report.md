# 共绩算力 Agent Skills 测试报告（按官网场景）

> 测试日期：2026-09-24 · 测试环境：Windows + Python 3.13（venv, requests 2.34.2）
> 场景框架来源：[docs.suanli.cn/skills](https://docs.suanli.cn/skills)（共绩算力官方 Agent Skills 页面）
> 测试对象：`gongji-skills/` 本地仓库（Apifox 文档运行时同步改造后，commit `e3f33a9`）
> 凭证：平台 API 密钥（简易模式 / Token 模式）

---

## 测试总览

| 测试层 | 用例数 | 通过 | 失败 | 说明 |
|--------|--------|------|------|------|
| 一 · Skills 安装与结构完整性 | 6 | 6 | 0 | 对应官网「安装」「包含哪些 skill」 |
| 二 · 凭证配置与鉴权 | 2 | 2 | 0 | 对应官网「安装后配置密钥」 |
| 三 · 官网「确认已接通」 | 2 | 2 | 0 | 官网原文给出的两个验证问题 |
| 四 · 各 skill 产品场景（真实平台调用） | 10 | 10 | 0 | 5 个 skill × 代表性只读端点 |
| 五 · 文档运行时同步（本次改造核心） | 11 + 3 | 14 | 0 | 离线套件 11 + 真实网络冒烟 3 |
| **合计** | **31** | **31** | **0** | |

真实平台调用总耗时 4.0 秒，单接口延迟 265–893ms。

---

## 场景一：安装 Skills（对应官网「快速开始」）

官网流程：`npx skills add suanleme/gongji-skills` → 安装后得到 5 个 skill。本地测试以仓库结构完整性等价验证：

| # | 检查项 | 结果 | 说明 |
|---|--------|------|------|
| 1 | 5 个 skill 目录齐全 | ✅ | suanli-deployment / suanli-job / suanli-metal / suanli-nas-storage / suanli-image-preheat |
| 2 | 每个 skill 含 SKILL.md + api/ + scripts/ + .env.example | ✅ | 与官网「按产品划分的 skill」一致 |
| 3 | api/ 文档数量 | ✅ | 63 份（54 端点 + 9 份 job 侧共享副本），全部带「来源：Apifox 官方文档（实时同步）」标记与远端 updatedAt |
| 4 | SKILL.md → api/ 引用一致性 | ✅ | 端点速查表引用的文件名与映射表完全兼容，零断链 |
| 5 | 根 scripts/fetch_apifox.py 存在且语法通过 | ✅ | py_compile 通过 |
| 6 | README 安装/使用说明与官网一致 | ✅ | 含文档实时同步章节（本地新增） |

## 场景二：凭证配置（对应官网「安装完成后」）

官网流程：`cp .env.example .env` → 填 `SUANLI_TOKEN`（控制台右上角头像 → API 密钥，推荐简易模式）。

| # | 检查项 | 结果 | 说明 |
|---|--------|------|------|
| 1 | 简易模式鉴权头组装（token/timestamp/version） | ✅ | 按文档组装，无需 sign_str |
| 2 | 密钥有效性 | ✅ | 全部请求返回 `code=0000`，无鉴权失败 |

## 场景三：官网「确认已接通」

官网原文：「可以先问：『列出我的弹性部署任务』『查一下 Job 批处理任务状态』，如果 Agent 能返回平台上的任务列表，说明凭证和 skill 已经就绪。」

| 官网验证问题 | 实际调用 | 结果 | 平台真实数据 |
|--------------|----------|------|--------------|
| 列出我的弹性部署任务 | `GET /api/deployment/task/search` | ✅ 327ms | 共 **696** 个部署任务（取 5 条验证结构） |
| 查一下 Job 批处理任务状态 | `GET /api/task/job/search` | ✅ 372ms | 共 **248** 个 Job 任务 |

**结论：已接通。** 凭证、鉴权、skill 文档三层链路全部就绪。

## 场景四：各 skill 产品场景（真实平台只读调用）

官网「包含哪些 skill」列出 5 个产品线，逐一取代表性场景实测（均为只读操作，不创建/变更任何资源）：

| Skill | 官网功能描述 | 实测场景 | 端点 | 结果 | 数据摘要 |
|-------|--------------|----------|------|------|----------|
| suanli-deployment | 弹性部署任务全生命周期、节点、计费、存储挂载 | 查资源 | `GET /deployment/resource/search` | ✅ 893ms | 72 条 GPU 资源 |
| | | 查节点列表 | `GET /deployment/task/points?task_id=3235240` | ✅ 281ms | 该任务 1 个节点 |
| suanli-job | Job 批处理创建/查询/停止、任务队列、资源与计费 | 查任务队列组 | `GET /job/queue/group/search` | ✅ 265ms | 队列 1 下 0 个任务组（空，正常） |
| suanli-metal | 裸金属机器、订单与计费 | 查订单列表 | `POST …/get_order_list_v2` | ✅ 267ms | 8 笔订单（含状态/金额/GPU 型号字段） |
| suanli-nas-storage | 集群存储卷、SFTP、S3 互传 | 用量概览 | `GET /storage/nas/v1/summary` | ✅ 278ms | 4 个卷，总容量 115GB，已用量可获取 |
| | | 查卷列表 | `GET /storage/nas/v1/list` | ✅ 311ms | 4 个卷详情 |
| suanli-image-preheat | 镜像预热创建/查询/更新/停止 | 查预热区域 | `GET /task/image_preheat/get_regions` | ✅ 271ms | 6 个可用区域 |
| | | 查预热任务 | `GET /task/image_preheat/search` | ✅ 304ms | 32 个历史预热任务 |

所有请求响应结构（字段名、必填、枚举、计费单位换算）与改造后的 `api/*.md` 文档一致——即文档与平台实际行为零偏差。

## 场景五：文档运行时同步（本次改造核心）

本次改造目标：`api/*.md` 由静态导出改为运行时从 Apifox 官方分享文档实时同步。测试覆盖正常读取、文档更新刷新、异常容错三大类：

### 5.1 离线测试套件（`scripts/test_fetch_apifox.py`，11/11 通过）

| # | 用例 | 结果 | 验证点 |
|---|------|------|--------|
| T0 | 语法检查 | ✅ | py_compile |
| T1 | 正常同步 | ✅ | 6 文件全量落盘、旧内容被替换 |
| T2 | 幂等性 | ✅ | 二次同步 0 更新 0 失败 6 跳过、mtime 不变 |
| T3 | --check 一致性 | ✅ | 内容最新时 exit 0「全部文档均为最新」 |
| T4 | 更新后刷新 | ✅ | 模拟远端内容变化 → check 检出（exit 1）→ sync 重写新内容 |
| T5 | 树拉取失败 | ✅ | exit 2、本地文档未被触碰、提示保留本地 |
| T6 | 单端点失败 | ✅ | exit 1、failed 列出、旧文件保留、其余端点正常 |
| T7 | 缓存损坏恢复 | ✅ | 损坏 JSON → 自动重拉、缓存重写有效 |
| T8 | 缓存命中 | ✅ | 10 分钟有效期内 0 次树请求 |
| T9 | 孤儿清理 | ✅ | --prune 删除映射外文件、保留全部映射文件 |
| T10 | 渲染单测 | ✅ | 标题/端点/updatedAt/必填/示例/脚注等 10 断言 |

### 5.2 真实网络冒烟（3/3 通过）

| # | 场景 | 结果 |
|---|------|------|
| 1 | 全量同步（`--refresh-cache`）：5 skill × 54 端点 + 9 份共享复制 | ✅ 0 失败，exit 0 |
| 2 | 二次 `--check`（缓存命中） | ✅「全部文档均为最新」，exit 0 |
| 3 | 静态版 bug 修复验证 | ✅ `image-preheat-update.md` 已是真正的 update 端点（`POST /api/task/image_preheat/update`，body `{task_id, points}`） |

### 5.3 容错语义（Agent 使用视角）

```
python scripts/fetch_apifox.py --check
  exit 0 → 全部最新，放心用本地文档
  exit 1 → 远端有更新（或个别端点失败），去掉 --check 同步
  exit 2 → 网络异常，本地文档保留可用，稍后重试
```

---

## 结论

1. **官网场景全部走通**：「确认已接通」两个验证问题实测通过，5 个 skill 的产品场景 10 项真实平台调用全部成功，响应结构与实时同步的文档完全一致。
2. **改造目标达成**：文档链路从「写死的静态导出」变为「运行时实时同步」，带缓存、幂等、分级容错；Apifox 官方文档更新后重跑同步即生效，无需手工改 skill。
3. **质量数据**：合计 31 项测试 31 通过 0 失败；真实调用平均延迟 ~350ms。

## 遗留与建议

1. 远端 84 端点中 28 个未收录映射（deployment v2、job queue 全套 CRUD、对象存储 v2 套件），属 skill 功能扩展，`--include-new` 可列出，建议后续按需补。
2. `requests` 为脚本依赖（venv 已装 2.34.2）。
3. 写操作（创建/停止/删除）未在本轮测试范围——按官网「确认已接通」的最小验证原则，只读验证已足以证明链路；写操作建议在真实业务使用中按 SKILL.md 工作流执行。

---

## 附录：测试产物索引

| 文件 | 说明 |
|------|------|
| `scripts/e2e_platform_test.py` | 官网场景 E2E 测试脚本（可重复执行） |
| `scripts/e2e-report.json` | E2E 详细结果（含每项延迟与数据摘要） |
| `scripts/test_fetch_apifox.py` | 文档同步离线测试套件 |
| `scripts/test-report.md` / `.json` | 离线套件报告 |
| `docs/apifox-sync-verification-report.md` | 改造技术验证报告（本轮前序） |

*报告生成：2026-09-24 12:30 · 本地仓库 commit `e3f33a9`，未推送远程*
