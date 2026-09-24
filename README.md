# 共绩算力 Agent Skills

通过共绩算力（[suanli.cn](https://suanli.cn)）Open API 管理弹性部署、Job 批处理、裸金属、集群存储与镜像预热。

[![skills.sh](https://skills.sh/b/suanleme/gongji-skills)](https://skills.sh/suanleme/gongji-skills)

线上仓库：[github.com/suanleme/gongji-skills](https://github.com/suanleme/gongji-skills)

## 安装

```bash
npx skills add suanleme/gongji-skills
```

CLI 会把 skill 装到当前 Agent 对应目录。Cursor 项目级默认 `.agents/skills/`，全局为 `~/.cursor/skills/`。

### 常用变体

```bash
# 列出仓库内 skill，不安装
npx skills add suanleme/gongji-skills --list

# 只装某一个
npx skills add suanleme/gongji-skills --skill suanli-deployment

# 全局安装（跨项目可用）
npx skills add suanleme/gongji-skills -g

# 装全部 skill 到已检测到的 Agent
npx skills add suanleme/gongji-skills --all
```

本地开发可直接指向本目录：

```bash
npx skills add . --list
```

## Skills

| Skill | 说明 |
|-------|------|
| [suanli-deployment](suanli-deployment/) | 弹性部署任务全生命周期、节点、计费、对象存储与 NAS 挂载 |
| [suanli-job](suanli-job/) | Job 批处理：创建 / 查询 / 停止、任务队列、资源与计费 |
| [suanli-metal](suanli-metal/) | 裸金属机器、订单与计费 |
| [suanli-nas-storage](suanli-nas-storage/) | 集群存储卷、SFTP、S3 互传 |
| [suanli-image-preheat](suanli-image-preheat/) | 镜像预热任务：创建 / 查询 / 更新 / 停止 |

## 凭证

安装后进入对应 skill 目录，复制模板再填密钥（**不要提交 `.env`**）：

```bash
cp .env.example .env
```

必填 `SUANLI_TOKEN`（平台右上角头像 → **API 密钥**，推荐简易模式）。可选 `SUANLI_BASE_URL`、`SUANLI_RSA_PRIVATE_KEY`。`suanli-nas-storage` 在 S3 创建 / 重试 / 校验时还需要 `SUANLI_PLATFORM_PUBLIC_KEY`。

## 更新

```bash
npx skills update
```

## 文档实时同步（Apifox）

各 skill 的 `api/*.md` 已改为由 [`scripts/fetch_apifox.py`](scripts/fetch_apifox.py) 从 Apifox 官方分享文档（[s.apifox.cn/6aa360d3…](https://s.apifox.cn/6aa360d3-d8f2-471e-b841-3a35c33a7b7c)）**运行时实时同步**生成，不再是写死的静态导出——官方文档更新后，重跑同步即可生效，无需手工改 skill。

```bash
# 检查远端是否有更新（不写文件）
python scripts/fetch_apifox.py --check

# 同步全部 skill（内容未变的文件自动跳过）
python scripts/fetch_apifox.py

# 只同步某个 skill / 强制重写 / 刷新树缓存 / 清理孤儿文件
python scripts/fetch_apifox.py --skill suanli-job
python scripts/fetch_apifox.py --force
python scripts/fetch_apifox.py --refresh-cache
python scripts/fetch_apifox.py --prune
```

退出码约定：`0` 成功/全部最新；`1` 有更新可拉取（check 模式）或部分端点失败；`2` API 树拉取失败（网络异常，本地文档保留可用）。依赖：Python 3.8+ 与 `requests`。

测试：`python scripts/test_fetch_apifox.py`（离线沙盒，11 个用例，报告写入 `scripts/test-report.md`）。
