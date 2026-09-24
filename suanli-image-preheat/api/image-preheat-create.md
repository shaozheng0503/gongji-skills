# 镜像预热任务创建接口

> 来源：Apifox 官方文档（实时同步） · 分组：共绩算力 Open API/镜像预热任务(申请开通)
> 远端最后更新：2026-08-06T09:09:38.000Z
> 端点：`POST /api/task/image_preheat/create`

| 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
| --- | --- | --- | --- |
| v1.0.0 | - | 否 | 是 |

### **描述**
# 镜像预热任务

## 功能描述

镜像预热任务用于提前将服务镜像缓存到指定的集群区域或资源节点，以减少后续任务启动时拉取镜像所需的时间。

创建镜像预热任务时支持以下两种预热类型：

- **仅集群预热**：将镜像预热到所选区域的集群级镜像缓存中。该模式按区域执行，不指定具体资源规格、节点数量和调度策略。
- **节点预热**：根据指定的资源规格和节点数量创建预热任务，将镜像预热到对应的资源节点。该模式支持配置跨区调度策略。

接口没有单独的预热类型字段，而是根据 `regions` 和 `resources` 判断预热类型。两个字段必须二选一，不能同时传入，也不能同时为空。

## 创建接口

```text
POST /api/task/image_preheat/create
```

加密创建接口：

```text
POST /api/task/image_preheat/encrypt/create
```

加密接口解密后的业务字段及校验规则与普通创建接口一致。

## 字段要求

| 字段 | 类型 | 仅集群预热 | 节点预热 | 说明 |
| --- | --- | --- | --- | --- |
| `task_name` | `string` | 必填 | 必填 | 任务名称，不能为空。 |
| `resources` | `ResourceMark[] \| null` | 必须为 `null` 或不传 | 必填 | 节点预热资源列表，至少包含一项。 |
| `regions` | `ImagePreheatRegionDto[] \| null` | 必填 | 必须为 `null` 或不传 | 集群预热区域列表，至少包含一个有效区域。 |
| `scheduler_strategy` | `TaskSchedulerStrategy \| null` | 必须为 `null` 或不传 | 可选 | 节点预热的调度策略。 |
| `points` | `integer \| null` | 必须为 `null` 或不传 | 必填 | 节点数量，必须大于等于 `1`。 |
| `services` | `ImagePreheatServiceDto[]` | 必填 | 必填 | 待预热的服务镜像列表，至少包含一项。 |

节点预热：resources[].mark 需通过资源列表接口 GET /api/deployment/resource/search?task_type=ImagePreHeat 获取，不能自行构造；同时必须传 points。

仅集群预热：regions 需通过区域列表接口 GET /api/task/image_preheat/get_regions 获取；无需传 resources、scheduler_strategy 和 points。
加签详见：[加签流程](https://suanli.cn/docs/platform/openapi/m3p6whioxidzwaksughc4gfhnro/#45-%E5%8A%A0%E7%AD%BE%E6%B5%81%E7%A8%8B)

## header 参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `token` | string | 是 | 请填入您在平台内创建的 API 密钥，获取路径为：右上角头像 → API 密钥。 |
| `timestamp` | integer | 是 | 时间戳（示例：{{$date.millisecondsTimestamp}}） |
| `version` | string | 是 | 固定值（示例：1.0.0） |
| `sign_str` | string | 否 | 如果token为简易模式则无需填写此字段 |

## 请求体

Content-Type: `application/json`

- `task_name` `string` **(必填)**：任务名
- `resources` `array | null`：资源列表
- `regions` `array | null`
- `scheduler_strategy` `object | null`：跨区调度
  - `mode` `string` **(必填)**，枚举: `Unrestricted`
- `points` `integer | null`：节点数量
- `create_time` `string | null`：创建时间
- `services` `array` **(必填)**
  - **array<object>**
    - `service_name` `string` **(必填)**：服务名称
    - `service_image` `string` **(必填)**：服务镜像
    - `repository_account` `any`：私有仓库账号
    - `is_update_repository` `boolean | null`：是否更新私有仓库账号
- `region_point_usage` `object | null`：集群使用节点数
  - `北京酒仙桥t1(备注：该字段为预热节点所在集群的region_name)` `object` **(必填)**
    - `used_points` `integer` **(必填)**：已用节点数
    - `available_points` `integer` **(必填)**：可用节点数
  - `北京酒仙桥t2(备注：该字段为预热节点所在集群的region_name)` `object` **(必填)**
    - `used_points` `integer` **(必填)**：已用节点数
    - `available_points` `integer` **(必填)**：可用节点数

**请求示例（示例）**：

```json
{
  "task_name": "镜像预热任务",
  "scheduler_strategy": {
    "mode": "Unrestricted"
  },
  "points": 2,
  "services": [
    {
      "service_name": "d1779468791353-35628",
      "service_image": "harbor.sxxxe.cn/public-hub/dailyhot:1.0",
      "repository_account": null,
      "is_update_repository": null
    }
  ],
  "create_time": null,
  "resources": [
    {
      "mark": "J19Cg02JMM7pVim3XPCik/U6sbaBl/dYKodWFvzjPWWGJInsPwDdSxdy9/JlWA4GfzNWzeJB/tuGhCNTWLu4QY8g8FizMIgdNVGZh8Tp8XOEbxyOnOH7pHbI7WIUdbCUx1Wo8rderOCHwBwAq/QkIQAAU7hOXN4TgAK1tggieTos7TE9on7i2i"
    },
    {
      "mark": "J19Cg02JMM7pVim3XPCik/U6vLaBl/dYKodWFvzjPWWGJInsPwDdSxdy9/JlWA4GfzNWzeJB/tuGiSNTWLu4QY8g8FizMIg3a51r+dNVGZh8Tp8XOEbxyOrKGLhZHlg4Esc7duvMDmQPgRm6aH4cHRIt1f3G6zhb1SUj+0tzZr/5UPLBduBg"
    }
  ]
}
```

## 响应（200）

- `data` `object | null` **(必填)**
  - `task_id` `integer` **(必填)**：任务id

响应名：成功

**响应示例（示例）**：

```json
{
  "code": "0000",
  "message": "success",
  "data": {
    "task_id": 38116
  }
}
```

---
*本文档由 fetch_apifox.py 从 Apifox 分享文档 6aa360d3-d8f2-471e-b841-3a35c33a7b7c 实时同步生成；同步时间见仓库根 .apifox-sync-manifest.json*
