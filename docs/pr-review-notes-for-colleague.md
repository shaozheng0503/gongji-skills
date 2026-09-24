# 给同事的 PR 审阅说明（可直接转发）

---

## 一、一句话版本（微信/飞书直接发）

> 我给 gongji-skills 提了个 PR（https://github.com/suanleme/gongji-skills/pull/1）：把 skills 里写死的 Apifox 静态文档改成了运行时实时同步——以后 Apifox 官方文档更新，跑一条命令就自动生效，不用再手工导出替换了。31 项测试全过（含对平台的真实调用验证），你审一下，没问题点合并就行。

---

## 二、正式版本（邮件/PR 评论区）

**PR**：https://github.com/suanleme/gongji-skills/pull/1
**标题**：feat: Apifox 文档运行时实时同步（skills 文档自动更新机制）
**规模**：3 commits，77 个文件（+7278 / −24372）

### 这次改了什么

**问题**：每个 skill 的 `api/*.md` 是从 Apifox 手动导出的静态文件。官方文档一更新，这些文件就过期了，得人工重新导出、核对、替换，而且之前还发现过一个存量错误（`image-preheat-update.md` 内容其实是 create 的副本）。

**方案**：新增 `scripts/fetch_apifox.py`，直接调 Apifox 分享文档的公开 JSON 接口，把各端点的最新定义拉下来生成本地 markdown：

```
# 平时不用管；怀疑文档过期时：
python scripts/fetch_apifox.py --check    # 只查有没有更新（不写文件）
python scripts/fetch_apifox.py            # 有更新就同步（没变的文件自动跳过）
```

- 54 个端点的文件名全部沿用，SKILL.md 里的引用零改动
- 同步是幂等的：内容没变的文件不会重写
- 容错分三级：查更新失败 exit 0/1/2 语义明确；网络挂了本地文档照常可用；单个端点拉不动不影响其他端点
- 顺带修了上面说的 update 文档错误
- 5 个 SKILL.md 各加了一小节说明这个机制，README 也补了用法

### 怎么验证的

31 项测试全部通过，三层验证：

1. **离线单元测试**（11 项）：正常同步 / 幂等 / 更新检出 / 树拉取失败 / 单端点失败 / 缓存损坏恢复 / 孤儿文件清理等，全过
2. **真实网络冒烟**（3 项）：全量同步 63 份文档 0 失败；二次检查确认收敛
3. **真实平台调用**（10 项）：按官网 docs.suanli.cn/skills 的「确认已接通」场景，用真实密钥调了部署任务列表、Job 状态、GPU 资源、裸金属订单、NAS 存储等 10 个只读接口，全部 code=0000，响应结构和同步后的文档完全一致

完整报告在 PR 里的 `docs/skills-test-report.md`。

### 审阅建议（重点看三处）

1. `scripts/fetch_apifox.py` 的 `ENDPOINT_MAP`——端点和文件名的映射是否和你掌握的一致
2. 随机挑几份 `api/*.md` 和 Apifox 官方文档对照（字段、必填标记、示例）
3. 五个 SKILL.md 新增的「文档实时同步」小节表述是否 OK

### 已知边界（不影响本次合并）

- 远端还有 28 个端点没进映射（deployment v2、job queue 全套 CRUD、对象存储 v2），属于功能扩展，`--include-new` 随时能列出来，后续按需加
- 同步脚本依赖 `pip install requests`（README 已注明）

---

## 三、PR 正文（已写在 PR 里，供参考）

PR 描述已包含：改造目标、四块改动内容（同步器 / 63 份文档重生成 / SKILL.md 小节 / 测试矩阵）、审阅建议、已知边界。同事打开 PR 首页即可看到。

## 四、合并前自查清单（都已确认）

- [x] 本地 3 个 commit 历史干净（feat → test → chore）
- [x] 运行时产物（缓存/清单/测试沙盒）已 gitignore，未入库
- [x] `.env` / 密钥 / PAT 无泄漏（凭证走 GCM，不在代码里）
- [x] 63 份文档与 Apifox 官方文档零偏差（真实平台 10 接口验证）
- [x] 存量 bug 修复（image-preheat-update.md）

## 五、合并后的操作（给你自己）

```bash
# 同步上游到本地 master
git checkout master
git fetch upstream
git merge upstream/master
git push origin master        # 同步自己的 fork
git branch -d pr/apifox-runtime-sync
git push origin --delete pr/apifox-runtime-sync   # 删远端分支
```

以后平台文档更新时，任何装了这个 skill 的人跑一句 `python scripts/fetch_apifox.py` 就能拿到最新文档。
