# 订单列表

> 来源：Apifox 官方文档（实时同步） · 分组：共绩算力 Open API/裸金属/订单列表
> 远端最后更新：2026-08-06T07:36:58.000Z
> 端点：`POST /api/output/v2/device_order/get_order_list_v2`

| 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
| --- | --- | --- | --- |
| v1.0.0 | - | 否 | 是 |

### **描述**
获取订单列表及其相关信息。

## 请求体

Content-Type: `application/json`

- `page` `integer` **(必填)**：页码
- `page_size` `integer` **(必填)**：每页数量
- `conditional` `object` **(必填)**：关键词 — 设备型号/订单编号
  - `condition` `string` **(必填)**

**请求示例（示例 1）**：

```json
{
  "page": 1,
  "page_size": 10,
  "conditional": {
    "condition": "123"
  }
}
```

## 响应（200）

- `code` `string` **(必填)**
- `message` `string` **(必填)**
- `data` `object` **(必填)**
  - `count` `integer` **(必填)**
  - `results` `array` **(必填)**
    - **array<object>**
      - `order_id` `integer` **(必填)**：订单ID
      - `order_no` `string` **(必填)**：订单号
      - `status` `string` **(必填)**：订单状态，枚举: `Default`/`Waiting`/`Serving`/`Finished`/`Canceled`
      - `buy_count` `integer` **(必填)**：购买数量
      - `total_price` `integer` **(必填)**：订单金额
      - `create_time` `string` **(必填)**：创建时间
      - `billing_type` `string` **(必填)**：计费方式，枚举: `Hour`/`Day`/`Week`/`Month`
      - `gpu_models` `array` **(必填)**：设备信息
        - **array<object>**
          - `gpu_model` `string` **(必填)**：设备GPU型号
          - `gpu_count` `integer` **(必填)**：设备卡数
          - `order_details_id` `integer` **(必填)**：订单详情ID
          - `order_detail_status` `string` **(必填)**：订单详情状态，枚举: `Default`/`Waiting`/`Serving`/`Finished`/`Canceled`/`CanceledRefunded`
          - `total_price` `integer` **(必填)**：订单详情金额
          - `is_paid` `boolean` **(必填)**：是否支付
      - `discount_total_price` `integer` **(必填)**：订单算力券消费 — 1000000=1元
      - `actually_total_price` `integer` **(必填)**：订单余额消费 — 1000000=1元
      - `cancel_actually_total_price` `integer` **(必填)**：订单余额退款 — 1000000=1元
      - `cancel_discount_total_price` `integer` **(必填)**：订单算力券退款 — 1000000=1元

响应名：成功

**响应示例（成功示例）**：

```json
{
  "code": "0000",
  "message": "success",
  "data": {
    "count": 2,
    "results": [
      {
        "order_id": 1775,
        "order_no": "1785826899729",
        "status": "Waiting",
        "buy_count": 1,
        "device_count": 0,
        "total_price": 28000000,
        "create_time": "2026-08-04T15:01:39.729898+08:00",
        "billing_type": "Hour",
        "gpu_models": [
          {
            "gpu_model": "5090",
            "gpu_count": 8,
            "order_details_id": 1772,
            "order_detail_status": "Waiting",
            "total_price": 28000000,
            "is_paid": true
          }
        ],
        "discount_total_price": 28000000,
        "actually_total_price": 0,
        "cancel_actually_total_price": 0,
        "cancel_discount_total_price": 0
      },
      {
        "order_id": 1703,
        "order_no": "1784512431064",
        "status": "Finished",
        "buy_count": 1,
        "device_count": 0,
        "total_price": 28000000,
        "create_time": "2026-07-20T09:53:51.064032+08:00",
        "billing_type": "Hour",
        "gpu_models": [
          {
            "gpu_model": "5090",
            "gpu_count": 8,
            "order_details_id": 1700,
            "order_detail_status": "Finished",
            "total_price": 28000000,
            "is_paid": true
          }
        ],
        "discount_total_price": 28000000,
        "actually_total_price": 0,
        "cancel_actually_total_price": 0,
        "cancel_discount_total_price": 0
      }
    ]
  }
}
```

---
*本文档由 fetch_apifox.py 从 Apifox 分享文档 6aa360d3-d8f2-471e-b841-3a35c33a7b7c 实时同步生成；同步时间见仓库根 .apifox-sync-manifest.json*
