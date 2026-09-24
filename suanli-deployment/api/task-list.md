# 任务列表查询接口

> 来源：Apifox 官方文档（实时同步） · 分组：共绩算力 Open API/弹性部署服务任务
> 远端最后更新：2026-07-15T07:14:26.000Z
> 端点：`GET /api/deployment/task/search`

| 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
| --- | --- | --- | --- |
| v1.0.0 | - | 否 |是 |

### **描述**
获取弹性部署任务列表及其相关信息。
支持按状态、任务名等条件查询。

## query 参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `type` | string | 否 | 任务类型。如果有多个值，请使用英文逗号（,）分隔（示例：Deployment） |
| `status` | string | 否 | 任务状态。如果有多个值，请使用英文逗号（,）分隔（示例：Running,Pending,Paused） |
| `search_value` | string | 否 | 任务名 |
| `page` | integer | 否 | 页码（示例：1） |
| `page_size` | integer | 否 | 每页数量（示例：10） |

## header 参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `token` | string | 是 | 请填入您在平台内创建的 API 密钥，获取路径为：右上角头像 → API 密钥。 |
| `timestamp` | number | 是 | 时间戳（示例：1770194570564） |
| `version` | string | 是 | 固定值（示例：1.0.0） |

## 响应（200）

- `data` `object | null` **(必填)**
  - `count` `integer` **(必填)**
  - `results` `array` **(必填)**
    - **array<object>**
      - `task_id` `integer | null` **(必填)**：任务id
      - `task_name` `string` **(必填)**：任务名称
      - `status` `string | null` **(必填)**：任务状态，枚举: `Pending`/`Running`/`Paused`/`End`/`Other`
      - `points` `integer | null` **(必填)**：节点数量
      - `runing_points` `integer | null` **(必填)**：运行中节点数
      - `billing_value` `integer | null` **(必填)**：累计花费金额
      - `resources` `array` **(必填)**：资源列表
        - **array<any>**
          - `resource` `object` **(必填)**：资源信息
            - `device_name` `string` **(必填)**：设备名称
            - `region` `string` **(必填)**：区域唯一标识
            - `gpu_name` `string` **(必填)**：GPU名称
            - `gpu_count` `integer` **(必填)**：GPU数量
            - `gpu_memory` `integer` **(必填)**：GPU显存
            - `memory` `integer` **(必填)**：内存
            - `cpu_cores` `integer` **(必填)**：CPU核数
          - `region_name` `string` **(必填)**：地区名称
          - `mark` `string` **(必填)**：资源唯一标识
      - `services` `array` **(必填)**：服务列表
        - **array<object>**
          - `service_id` `integer | null` **(必填)**：服务id
          - `service_name` `string` **(必填)**：服务名称
          - `service_image` `string` **(必填)**：服务镜像
          - `remote_ports` `array` **(必填)**：服务端口暴露列表
            - **array<object>**
              - `url` `string | null` **(必填)**：服务回传链接
              - `service_port` `integer` **(必填)**：服务端口暴露

响应名：成功

**响应示例（成功示例）**：

```json
{
  "code": "0000",
  "message": "success",
  "data": {
    "count": 1,
    "results": [
      {
        "task_id": 1229831,
        "status": "Pending",
        "task_name": "任务名称",
        "points": 1,
        "runing_points": 0,
        "billing_value": 0,
        "forecast_value": 0,
        "resources": [
          {
            "resource": {
              "device_name": "4090",
              "region": "guangdong",
              "gpu_name": "4090",
              "gpu_count": 1,
              "gpu_memory": 24560,
              "memory": 64512,
              "cpu_cores": 16
            },
            "region_name": "广东一区",
            "mark": "ha8GDGEAORN3a9Hhu7X+W/lveP9CW2eBkI+oB/QJLRcbofDUMuUjhbDPib2YTSwc3AN4DULuanCCqEj1LwDsR/IhlpYRSzIvKasM+AcJsuNXRGWqp1qI1Tx3A4TqmQRdHvNEuWujXhLX2FryHDG12cwUBmylTvRgY+fAH8DR5OFKDtPL3G2IOAu8+D4=",
            "weight": null
          },
          {
            "resource": {
              "device_name": "4090",
              "region": "beijing-jxq-p1",
              "gpu_name": "4090",
              "gpu_count": 1,
              "gpu_memory": 24560,
              "memory": 64512,
              "cpu_cores": 16
            },
            "region_name": "北京一区",
            "mark": "ha8GDGEAORN3a9Hhu7X+W/lveP9CW2eBkI+oB/QJLRcesfjQPO8rxr2V1LKPDHtvkAVlHT+6KSnXs0L1NxKyB6VS154UUBlufO9OrkJD9pAYRniwik7PgmExT5DghxIFTa4H6X/kCUuRlEn6BifjmItnR2CnXtghNqSTEUWVvy+bUdznvFvFJIycQ8SoQCNugw==",
            "weight": null
          }
        ],
        "create_time": "2026-01-01T11:27:57.653136+08:00",
        "services": [
          {
            "service_id": 1229930,
            "service_name": "d1767756476463-64661100",
            "service_image": "harbor.suanleme.cn/public-hub/dailyhot:1.0",
            "remote_ports": []
          }
        ]
      }
    ]
  }
}
```

---
*本文档由 fetch_apifox.py 从 Apifox 分享文档 6aa360d3-d8f2-471e-b841-3a35c33a7b7c 实时同步生成；同步时间见仓库根 .apifox-sync-manifest.json*
