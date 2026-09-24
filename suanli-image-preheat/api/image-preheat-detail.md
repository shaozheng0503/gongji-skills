# 镜像预热任务详情查询接口

> 来源：Apifox 官方文档（实时同步） · 分组：共绩算力 Open API/镜像预热任务(申请开通)
> 远端最后更新：2026-08-10T01:37:09.000Z
> 端点：`GET /api/task/image_preheat/detail`

| 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
| --- | --- | --- | --- |
| v1.0.0 | - | 否 | 是 |

### **描述**
获取指定镜像预热任务详情。
加签详见：[加签流程](https://suanli.cn/docs/platform/openapi/m3p6whioxidzwaksughc4gfhnro/#45-%E5%8A%A0%E7%AD%BE%E6%B5%81%E7%A8%8B)

## query 参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `task_id` | integer | 是 | 任务id（示例：1） |

## header 参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `token` | string | 是 | 请填入您在平台内创建的 API 密钥，获取路径为：右上角头像 → API 密钥。 |
| `timestamp` | integer | 是 | 时间戳（示例：{{$date.millisecondsTimestamp}}） |
| `version` | string | 是 | 固定值（示例：1.0.0） |
| `sign_str` | string | 否 | 如果token为简易模式则无需填写此字段 |

## 响应（200）

- `code` `string` **(必填)**：响应码 — 当code≠0000时，data必为null。，枚举: `0000`/`C999`/`C001`/`C002`/`C004`/`C005`/`C006`/`C007`/`C008`/`C009`/`C010`/`Z001`
- `message` `string | null` **(必填)**：响应信息
- `data` `object | null` **(必填)**
  - `task_id` `integer | null`：任务id
  - `task_type` `string | null`：任务类型，枚举: `ImagePreHeat`
  - `task_name` `string` **(必填)**：任务名
  - `resources` `array | null`：资源列表
  - `regions` `array | null`
  - `scheduler_strategy` `object | null`：跨区调度
    - `mode` `string` **(必填)**，枚举: `Unrestricted`
  - `scheduler_resources` `array | null`：跨区调度资源列表
  - `status` `string | null`：任务状态，枚举: `Pending`/`Running`/`Paused`/`End`
  - `points` `integer | null`：节点数量
  - `used_points` `integer | null`：使用中节点数
  - `available_points` `integer | null`：可用节点数
  - `scheduling_template` `object | null`：调度模板
    - `template` `string` **(必填)**：调度模板唯一标识
  - `create_time` `string | null`：创建时间
  - `region_cache_info` `array | null`：集群预热信息
  - `services` `array` **(必填)**：服务列表
    - **array<object>**
      - `service_id` `string | null`：服务id
      - `service_name` `string` **(必填)**：服务名称
      - `service_image` `string` **(必填)**：服务镜像
      - `repository_account` `object | null`：私有仓库账号
        - `repository_username` `string` **(必填)**：私有仓库用户名
        - `repository_password` `string | null`：私有仓库密码
      - `is_update_repository` `boolean | null`：是否更新私有仓库账号
  - `region_point_usage` `object | null`：集群使用节点数
    - `北京酒仙桥t1(备注：该字段为预热节点所在集群的region_name)` `object` **(必填)**
      - `used_points` `integer` **(必填)**：已用节点数
      - `available_points` `integer` **(必填)**：可用节点数
    - `北京酒仙桥t2(备注：该字段为预热节点所在集群的region_name)` `object` **(必填)**
      - `used_points` `integer` **(必填)**：已用节点数
      - `available_points` `integer` **(必填)**：可用节点数

响应名：成功

**响应示例（示例）**：

```json
{
  "code": "0000",
  "message": "success",
  "data": {
    "task_id": 38646,
    "task_type": "ImagePreHeat",
    "task_name": "镜像预热任务",
    "resources": [
      {
        "resource": {
          "device_name": "4040",
          "region": "bj-jxq-t2",
          "gpu_name": "4040",
          "gpu_count": 1,
          "gpu_memory": 10240000,
          "memory": 1024,
          "cpu_cores": 2
        },
        "region_name": "北京酒仙桥t2",
        "mark": "J19CgPCik/U6sbaBl/dYKodWFvzjPWWGJInsPwDdSxdy9/JlWA4GfzNWzeJB/tuGhCNTWLu4QY8g8FizMIg3a51r+dNVGZh8Tp8XOEbxyOnOH7pHbI7WIUdbCUx1Wo8rderOCHwBwAq/QkIQAAU7hOXN4TgAK1tggieTos7TE9on7i2i",
        "weight": null
      },
      {
        "resource": {
          "device_name": "4090",
          "region": "bj-jxq-t2",
          "gpu_name": "4090",
          "gpu_count": 1,
          "gpu_memory": 24560,
          "memory": 129024,
          "cpu_cores": 18
        },
        "region_name": "北京酒仙桥t2",
        "mark": "J19CLaBl/dYKodWFvzjPWWGJInsPwDdSxdy9/JlWA4GfzNWzeJB/tuGiSNTWLu4QY8g8FizMIg3a51r+dNVGZh8Tp8XOEbxyOrKGLhHcJyLaAhZHlg4Esc7duvMDmQPgRm6aH4cHRIt1f3G6zhb1SUj+0tzZr/5UPLBduBg",
        "weight": null
      }
    ],
    "regions": null,
    "scheduler_strategy": {
      "mode": "Unrestricted"
    },
    "scheduler_resources": null,
    "status": "Running",
    "points": 2,
    "used_points": null,
    "available_points": null,
    "region_point_usage": null,
    "scheduling_template": {
      "template": "RgqRYUviwatEqgE2dgmDX9yiTp"
    },
    "services": [
      {
        "service_id": 47659,
        "service_name": "d1779468791353-35628",
        "service_image": "harbor.xxx.cn/public-hub/dailyhot:1.0",
        "repository_account": null,
        "is_update_repository": null
      }
    ],
    "create_time": "2026-07-22T00:58:23.942014+08:00",
    "user_info": {
      "nickname": "183****1111",
      "tenant_nickname": null
    },
    "region_cache_info": null
  }
}
```

---
*本文档由 fetch_apifox.py 从 Apifox 分享文档 6aa360d3-d8f2-471e-b841-3a35c33a7b7c 实时同步生成；同步时间见仓库根 .apifox-sync-manifest.json*
