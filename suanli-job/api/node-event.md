# 节点事件查询接口

> 来源：Apifox 官方文档（实时同步） · 分组：共绩算力 Open API/弹性部署服务/Job批处理节点
> 远端最后更新：2026-06-13T11:17:03.000Z
> 端点：`GET /api/deployment/task/pod_event`

| 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
| --- | --- | --- | --- |
| v1.0.0 | - | 否 | 是 |

### **描述**
获取弹性部署任务节点的事件信息。

## query 参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `point_id` | number | 是 | 节点ID（示例：1） |

## header 参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `token` | string | 是 | 请填入您在平台内创建的 API 密钥，获取路径为：右上角头像 → API 密钥。 |
| `timestamp` | number | 是 | 时间戳（示例：1770194570564） |
| `version` | string | 是 | 固定值（示例：1.0.0） |

## 响应（200）

- `data` `object | null` **(必填)**
  - `events` `array` **(必填)**
    - **array<object>**
      - `reason` `string` **(必填)**
      - `message` `string` **(必填)**
      - `type` `string` **(必填)**
      - `event_time` `string` **(必填)**
      - `service` `string | null` **(必填)**

响应名：成功

---
*本文档由 fetch_apifox.py 从 Apifox 分享文档 6aa360d3-d8f2-471e-b841-3a35c33a7b7c 实时同步生成；同步时间见仓库根 .apifox-sync-manifest.json*
