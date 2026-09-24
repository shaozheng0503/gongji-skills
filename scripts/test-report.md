# fetch_apifox.py 本地测试报告

- 时间：2026-09-24 12:16:23
- 被测脚本：`C:\Users\huangshaozheng\WorkBuddy\2026-09-24-11-01-02\gongji-skills\scripts\fetch_apifox.py`
- 测试方式：离线沙盒（FakeServer mock 网络 + SUANLI_SKILLS_ROOT 隔离，不触碰真实仓库）

## 结果：11/11 通过

| # | 用例 | 结果 | 说明 |
| --- | --- | --- | --- |
| T0 | T0 语法检查 | ✅ | py_compile 通过 |
| T1 | T1 正常同步（全量拉取写盘） | ✅ | exit=0, 6 个映射文件全部落盘 |
| T2 | T2 幂等（内容一致跳过、mtime 不变） | ✅ | exit=0, mtime 不变, 输出含 更新0/失败0/跳过6 |
| T3 | T3 --check 无误报（最新时 exit 0） | ✅ | exit=0 |
| T4 | T4 文档更新后数据刷新（check 检出 + sync 重写） | ✅ | check exit=1 检出更新, sync exit=0 新内容落盘 |
| T5 | T5 树拉取失败（exit 2 + 本地文档保留） | ✅ | exit=2, 文档未被触碰 |
| T6 | T6 单端点失败（failed 列出、旧文件保留、exit 1） | ✅ | exit=1, job-tasks.md 保留旧内容, failed 已列出, 其余端点正常 |
| T7 | T7 缓存损坏自动恢复 | ✅ | exit=0, 缓存重写有效, 树请求 1 次 |
| T8 | T8 缓存命中（不发树请求） | ✅ | exit=0, 树请求 0 次（用缓存） |
| T9 | T9 孤儿文件清理（--prune） | ✅ | exit=0, orphan-old.md 已删除, 保留 6 个映射文件 |
| T10 | T10 render_api_md 单测（10 项断言） | ✅ | 全部通过 |
