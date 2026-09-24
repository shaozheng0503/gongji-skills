# 通过既有任务 Pod 列表接口查询训练实例

> 来源：Apifox 官方文档（实时同步） · 分组：共绩算力 Open API/弹性部署服务/Job批处理节点
> 远端最后更新：2026-09-08T10:29:57.000Z
> 端点：`GET /api/deployment/task/points`

复用原 TaskCenter points 路由、查询参数和 TaskPointsResponse，不注册训练专用 Pod 路由。服务端按 tenant_id+task_id 查询并显式接受 task_type=DistributedTraining；未知任务类型继续失败关闭。公共 PointDto 仅增加可选 role_name/role_index 训练字段，RoleId/TaskIndex 仍是内部关联事实。

## query 参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `tenant_id` | integer | 是 | — |
| `merchant_mark` | string | 否 | — |
| `task_id` | integer | 是 | — |
| `status` | string | 否 | 公开的 task/Pod 状态。任务查询接受以逗号分隔的状态列表。 |
| `regions` | string | 否 | 逗号分隔的 region code；沿用既有 TaskCenter points 查询语义。 |
| `page` | integer | 否 | 沿用既有 TaskCenter points 参数类型和默认值。 |
| `page_size` | integer | 否 | 沿用既有 TaskCenter points 参数类型和默认值；本训练契约不另加专用上限。 |

---
*本文档由 fetch_apifox.py 从 Apifox 分享文档 6aa360d3-d8f2-471e-b841-3a35c33a7b7c 实时同步生成；同步时间见仓库根 .apifox-sync-manifest.json*
