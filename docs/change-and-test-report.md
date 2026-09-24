# gongji-skills 改造说明与测试报告

> **PR**：https://github.com/suanleme/gongji-skills/pull/1
> **规模**：4 commits，77 个文件（+7278 / −24372）
> **一句话**：把 skills 里写死的 Apifox 静态文档，改成运行时实时同步——以后官方文档更新，跑一条命令就自动生效，不用再手工导出替换。

---

## 一、背景问题

每个 skill 的 `api/*.md` 是从 Apifox 手动导出的静态文件：

1. 官方文档一更新就过期，要人工导出、核对、替换
2. 无来源标记、无更新时间，过期了也看不出来
3. 藏着一个存量错误：`image-preheat-update.md` 的内容其实是 create 接口的副本（update 端点一直没接对）

## 二、改造内容

### 1. 新增核心脚本 `scripts/fetch_apifox.py`

直接调 Apifox 分享文档的公开 JSON 接口（免鉴权），拉取最新端点定义生成本地 markdown：

```bash
python scripts/fetch_apifox.py --check   # 只查远端有没有更新（不写文件）
python scripts/fetch_apifox.py           # 同步（内容没变的文件自动跳过）
```

| 特性 | 说明 |
|------|------|
| 端点映射 | 54 个端点的文件名全部沿用，SKILL.md 引用零改动 |
| 幂等 | MD5 内容哈希比对，没变的文件不重写 |
| 容错 | 树拉取失败 exit 2（本地文档保留可用）；单端点失败保留旧文件、不中断其他端点；每请求重试 3 次 |
| 缓存 | API 树 10 分钟本地缓存（已 gitignore） |
| 退出码 | 0 = 全部最新 / 1 = 有更新或部分失败 / 2 = 网络异常 |

### 2. 重生成全部 63 份 `api/*.md`

- 54 个端点 + 9 份 job 侧共享副本，每份带来源标记和远端更新时间
- 顺带修复了上述 `image-preheat-update.md` 的存量错误

### 3. 五个 SKILL.md 各加「文档实时同步」小节

Agent 怀疑文档过期时按 `--check` → 同步的流程走；README 补充了完整用法；`.gitignore` 排除运行时产物。

## 三、测试报告（31/31 通过）

| 测试层 | 用例数 | 结果 | 内容 |
|--------|--------|------|------|
| 离线单元测试 | 11 | ✅ 全过 | 正常同步 / 幂等 / 更新检出 / 树拉取失败 / 单端点失败 / 缓存损坏恢复 / 缓存命中 / 孤儿文件清理 / 渲染正确性 |
| 真实网络冒烟 | 3 | ✅ 全过 | 全量同步 63 份文档 0 失败；二次检查确认收敛；存量 bug 修复确认 |
| 真实平台调用 | 10 | ✅ 全过 | 按官网 docs.suanli.cn/skills「确认已接通」场景，用真实密钥调 10 个只读接口 |
| 结构与鉴权 | 7 | ✅ 全过 | 5 个 skill 目录完整 / SKILL.md 引用无断链 / 简易模式鉴权有效 |

**真实平台调用明细**（均返回 code=0000，平均延迟约 350ms）：

| 接口 | 实测数据 |
|------|----------|
| 弹性部署任务列表 | 696 个任务 |
| Job 批处理状态 | 248 个任务 |
| GPU 资源查询 | 72 条 |
| 裸金属订单 | 8 笔 |
| NAS 存储概览 | 4 个卷 / 115GB |
| 镜像预热区域 / 任务 | 6 个区域 / 32 个任务 |

所有响应结构与同步后的 `api/*.md` 完全一致，即文档与平台实际行为零偏差。

测试可复跑：`python scripts/test_fetch_apifox.py`（离线）、`python scripts/e2e_platform_test.py`（需 `SUANLI_TOKEN`）。

## 四、审阅建议（重点三处）

1. `scripts/fetch_apifox.py` 的 `ENDPOINT_MAP`——端点与文件名映射是否正确
2. 随机挑几份 `api/*.md` 和 Apifox 官方文档对照（字段、必填标记、示例）
3. SKILL.md 新增小节的表述

## 五、已知边界（不影响合并）

- 远端 84 个端点中 28 个未收录映射（deployment v2、job queue 全套 CRUD、对象存储 v2 套件），属后续功能扩展，`--include-new` 可随时列出
- 同步脚本依赖 `pip install requests`（README 已注明）
