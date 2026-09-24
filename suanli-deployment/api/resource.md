# 获取设备资源列表

> 来源：Apifox 官方文档（实时同步） · 分组：共绩算力 Open API/资源
> 远端最后更新：2026-07-15T07:14:43.000Z
> 端点：`GET /api/deployment/resource/search`

| 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
| --- | --- | --- | --- |
| v1.0.0 | - | 否 | 是 |

### **描述**
获取设备资源列表及其相关信息。

## query 参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `task_type` | string | 否 | 如果有多个值，请使用英文逗号（,）分隔（示例：Deployment） |
| `device_type` | string | 否 | 如果有多个值，请使用英文逗号（,）分隔（示例：GpuDevice） |

## header 参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `token` | string | 是 | 请填入您在平台内创建的 API 密钥，获取路径为：右上角头像 → API 密钥。 |
| `timestamp` | number | 是 | 时间戳（示例：1770194570564） |
| `version` | string | 是 | 固定值（示例：1.0.0） |

## 响应（200）

- `data` `object | null` **(必填)**
  - `count` `number` **(必填)**
  - `results` `array` **(必填)**
    - **array<object>**
      - `device_name` `string` **(必填)**：设备名称
      - `regions` `array` **(必填)**：资源所属区域列表
        - **array<object>**
          - `region` `string` **(必填)**：区域唯一标识
          - `region_name` `string` **(必填)**：区域名称
          - `mark` `object` **(必填)**
            - `resource` `object` **(必填)**：资源信息
              - `device_name` `string` **(必填)**：设备名称
              - `region` `string` **(必填)**：区域tag
              - `gpu_name` `string | null` **(必填)**：GPU名称
              - `gpu_count` `integer` **(必填)**：GPU数量
              - `gpu_memory` `integer` **(必填)**：GPU显存
              - `memory` `integer` **(必填)**：内存
              - `cpu_cores` `integer` **(必填)**：CPU核数
            - `mark` `string` **(必填)**：设备唯一标识
          - `price` `integer | null` **(必填)**：设备价格
          - `discount_price` `integer | null` **(必填)**：折扣价格
          - `inventory` `integer` **(必填)**：库存数
      - `gpu_name` `string` **(必填)**：GPU名称
      - `gpu_memory` `integer` **(必填)**：GPU显存
      - `gpu_count` `integer` **(必填)**：GPU数量
      - `memory` `integer` **(必填)**：内存
      - `cpu_cores` `integer` **(必填)**：CPU核数
      - `disk_size` `integer` **(必填)**：硬盘类型
      - `disk_type` `string` **(必填)**：硬盘大小

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
        "device_name": "H20 x 8",
        "regions": [
          {
            "region": "hebeif-1",
            "region_name": "河北一区",
            "mark": {
              "resource": {
                "device_name": "H20 x 8",
                "region": "hebeif-1",
                "gpu_name": "H20",
                "gpu_count": 8,
                "gpu_memory": 786432,
                "memory": 1572864,
                "cpu_cores": 192
              },
              "region_name": null,
              "mark": "ha8GDGEAORN3a9Hhu7X+W4Vtce8YV33R2cqzDf1CeFte7rPSMOMpgrHAlL3THz4zxz17CQ2xan6Q2UrnIQ6pUPcLqpoLUCh5MaAY9kIet8llTG2oulHTzTR0DoTuhhQcWfNOpn3zHQbZ3F73AivgnZVpBnOidOQtK7OFQF2etyubD5p/9khWFNjEhW7QZGN49g=="
            },
            "price": 16416,
            "discount_price": 16416,
            "inventory": 0
          },
          {
            "region": "xingjiangf-1",
            "region_name": "新疆一区",
            "mark": {
              "resource": {
                "device_name": "H20 x 8",
                "region": "xingjiangf-1",
                "gpu_name": "H20",
                "gpu_count": 8,
                "gpu_memory": 786432,
                "memory": 1572864,
                "cpu_cores": 192
              },
              "mark": "ha8GDGEAORN3a9Hhu7X+W4Vtce8YV33R2cqzDf1CeFte7rPCPO8rgb6My/iZEGhhnkByGBWLJiXf9FrtIWq5B6VS154UUBlufO9OrkJD/5AYRniwik7PgmExT5Dggh4GT60Z5zDsAUmMnxLiCiLjnotzUzf7CeQyLImVDRXK/TvcZdwJCgWWDknwrBCDIAAVli9FdX8="
            },
            "price": 16416,
            "discount_price": 16416,
            "inventory": 0
          }
        ],
        "gpu_name": "H20",
        "gpu_memory": 786432,
        "gpu_count": 8,
        "memory": 1572864,
        "cpu_cores": 192,
        "disk_size": 81920,
        "disk_type": "HDD"
      }
    ]
  }
}
```

---
*本文档由 fetch_apifox.py 从 Apifox 分享文档 6aa360d3-d8f2-471e-b841-3a35c33a7b7c 实时同步生成；同步时间见仓库根 .apifox-sync-manifest.json*
