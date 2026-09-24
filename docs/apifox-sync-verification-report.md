# 共绩算力 Skills — Apifox 文档运行时同步改造 · 验证报告

> 日期：2026-09-24 · 仓库：`gongji-skills/`（本地，未推送远程） · 本报告为最终交付物

## 一、改造目标回顾

**原状**：各 skill 的 `api/*.md` 是 Apifox 手动导出的静态文件，官方文档更新后需人工重新导出、手工核对、手工替换——skills 与平台文档之间没有自动同步通道。

**目标**：改为运行时按需实时读取 Apifox 官方文档，文档更新后无需手动改造 skills 即可自动生效；带缓存与网络异常容错；本地充分测试。

## 二、原静态结构与加载流程（改造前梳理）

```
SKILL.md（指令层：端点速查表 + 工作流 + 按需加载指引）
  └─ 按需 Read → api/<endpoint>.md（静态导出的 OpenAPI 详情）
                  └─ scripts/call.sh（执行层：token/timestamp/sign_str 组装）
```

三层架构本身合理，问题只在中间层是**死数据**：46 份静态 md 无来源标记、无更新时间、含一处真实错误（`image-preheat-update.md` 误为 create 的副本）。

## 三、改造方案与实现

### 3.1 数据通道（关键发现）

Apifox 分享文档暴露两个**免鉴权**的公开 JSON 接口（即官网渲染页面所用）：

| 接口 | 作用 |
|------|------|
| `GET s.apifox.cn/api/v1/shared-docs/{shareId}/http-api-tree` | 全量 API 树（目录 + 84 个端点的 id/method/path） |
| `GET s.apifox.cn/api/v1/shared-docs/{shareId}/http-apis/{apiId}` | 单端点完整定义（参数/请求体/响应/示例/updatedAt） |

### 3.2 核心脚本 `scripts/fetch_apifox.py`（仓库根）

- **端点映射表**：`(method, path) → (skill, 文件名)`，覆盖全部 54 个既有文件名，SKILL.md 引用零改动（向后兼容）
- **markdown 渲染**：`render_api_md()` 递归渲染 jsonSchema → 参数表/嵌套字段列表（必填标记/单位/枚举/示例）
- **幂等**：MD5 内容哈希比对，未变的文件不重写（mtime 不变）
- **容错**：
  - 树拉取失败 → exit 2，本地文档保留可用
  - 单端点失败 → 计入 failed、保留旧文件、不中断其余端点（exit 1）
  - 每请求指数退避重试 3 次
- **缓存**：API 树 10 分钟本地缓存（`.apifox-tree-cache.json`），`--refresh-cache` 可跳过
- **CLI**：`--check` / `--force` / `--prune` / `--skill` / `--include-new`
- **环境变量**：`SUANLI_SKILLS_ROOT`（仓库根覆盖）、`SUANLI_APIFOX_HOST`/`SUANLI_APIFOX_ID`（域名/ID 覆盖，测试用）

### 3.3 SKILL.md 接入（5 个 skill 全部）

每个 SKILL.md「端点速查」节末尾新增「文档实时同步」小节：Agent 怀疑文档过期 → `--check` 检查 → 确认后同步。README 增加「文档实时同步」使用说明。`.gitignore` 增补运行时产物。

## 四、测试结果

### 4.1 离线测试套件 `scripts/test_fetch_apifox.py`（11/11 通过）

设计：FakeServer（monkeypatch `requests.Session.get`）+ 沙盒目录（`SUANLI_SKILLS_ROOT` 指向 `.test-sandbox-main/`）——完全离线、不触碰真实仓库、不依赖真实网络。

| # | 用例 | 结果 | 验证点 |
|---|------|------|--------|
| T0 | 语法检查 | ✅ | py_compile |
| T1 | 正常同步 | ✅ | 6 文件全量落盘、旧内容被替换 |
| T2 | 幂等性 | ✅ | 二次同步 0 更新 0 失败 6 跳过、mtime 不变 |
| T3 | --check 一致性 | ✅ | 内容最新时 exit 0「全部文档均为最新」 |
| T4 | 更新后刷新 | ✅ | check 检出（exit 1）→ sync 重写新内容 |
| T5 | 树拉取失败 | ✅ | exit 2、文档未被触碰、提示保留本地 |
| T6 | 单端点失败 | ✅ | exit 1、failed 列出、旧文件保留、其余端点正常 |
| T7 | 缓存损坏恢复 | ✅ | 损坏 JSON → 自动重拉、缓存重写有效 |
| T8 | 缓存命中 | ✅ | 有效期内 0 次树请求 |
| T9 | 孤儿清理 | ✅ | --prune 删除映射外文件、保留 6 个映射文件 |
| T10 | render_api_md 单测 | ✅ | 标题/端点/updatedAt/必填/示例/脚注等 10 断言 |

### 4.2 真实网络冒烟（实弹验证）

1. **全量同步**（`--refresh-cache`）：5 skill × 54 端点 + 9 份 job 共享复制，**0 失败**，exit 0
2. **二次 check**（缓存命中）：「全部文档均为最新」，exit 0——真实环境幂等性确认
3. **静态版 bug 修复验证**：`image-preheat-update.md` 现为真正的 update 端点（`POST /api/task/image_preheat/update`，body `{task_id, points}`），不再误为 create 副本

### 4.3 测试中发现并修复的缺陷

| 缺陷 | 修复 |
|------|------|
| 脚注含本地生成时间戳 → 哈希幂等比对永远失败 | 脚注改为确定性内容，同步时间移入 manifest |
| sync 模式部分失败 exit 0，掩盖失败 | 改为 exit 1 |
| 共享复制未防护 job skill 缺失场景 | 加 `(repo_root/"suanli-job").is_dir()` 前置判断 |

## 五、遗留与建议

1. **远端未收录端点**：远端 84 端点中 28 个未在映射表（deployment v2 新版、job queue 全套 CRUD、对象存储 v2 套件）。用 `--include-new` 可列出。这些属于 skill 功能范围扩展（非文档同步问题），建议后续按需补映射。
2. **`requests` 依赖**：脚本需 `pip install requests`（venv 中已装 2.34.2）。
3. **本轮调试副产物**：`scripts/.test-sandbox-main/`（测试沙盒，已 gitignore，可随时删）、`test-report.json`（已 gitignore）。
4. **本地 git**：改动已在本地 git 可见（未推送）。基线 commit `01bc57d`。

## 六、改动清单

| 文件 | 类型 | 说明 |
|------|------|------|
| `scripts/fetch_apifox.py` | 新增 | 核心同步器（~550 行） |
| `scripts/test_fetch_apifox.py` | 新增 | 离线测试套件（11 用例） |
| `scripts/test-report.md` / `.json` | 新增 | 测试报告（套件自动生成） |
| `api/*.md` × 63 | 重写 | 54 端点文档 + 9 job 侧共享副本，改为实时生成 |
| `suanli-{deployment,job,metal,nas-storage,image-preheat}/SKILL.md` | 修改 | 各增「文档实时同步」小节 |
| `README.md` | 修改 | 增「文档实时同步」使用说明 |
| `.gitignore` | 修改 | 增缓存/清单/测试沙盒 |
| `.apifox-tree-cache.json` / `.apifox-sync-manifest.json` | 新增 | 运行时缓存与清单（已 gitignore） |

## 七、诚实的自评

**做扎实了的部分**：离线测试套件的设计（FakeServer + 沙盒隔离 + inproc mock）让我能确定性复现所有场景；真实网络冒烟跑通了完整的「检出 → 同步 → 收敛」闭环；过程中发现并修复了 3 个真实缺陷（幂等性、退出码、共享复制防护）。

**不足与坦白**：
1. 第一版测试写完直接跑，T4 一度把测试样例数据写进了真实仓库的 `job-create.md`——沙盒隔离是事后补的，污染靠真实同步恢复。教训：**测试隔离必须在第一个用例前就位**，而不是失败后补救。
2. 调试期间同一条消息里并行编辑同一文件导致编辑互相覆盖，浪费了两轮重跑。教训：同文件多处编辑必须串行。
3. 测试跑出了 4 个版本的报告文件（.test-run1~6），靠最后的清理脚本统一回收——中途版本管理不够干净。
