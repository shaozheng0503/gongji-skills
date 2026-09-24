# 创建订单

> 来源：Apifox 官方文档（实时同步） · 分组：共绩算力 Open API/裸金属/创建订单
> 远端最后更新：2026-08-06T07:49:47.000Z
> 端点：`POST /api/output/v2/device_order/buy_v2`

| 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
| --- | --- | --- | --- |
| v1.0.0 | - | 否 | 是 |

### **描述**
创建裸金属订单，需要传入相应的设备ID。
注意：unit_price仅用于页面显示价格与下单那一刻价格不一致的提示。

## 请求体

Content-Type: `application/json`

- `billing_type` `string` **(必填)**：计费方式，枚举: `Hour`/`Day`/`Week`/`Month`
- `buy_count` `integer` **(必填)**：购买数量
- `inner` `array` **(必填)**：购买设备 — 组网设备购买buy_count > 1时传入多个，单机设备购买buy_count > 1时也只传入1个
  - **array<object>**
    - `device_id` `integer` **(必填)**：设备ID
    - `unit_price` `integer` **(必填)**：购买单价 — 1000000=1元，仅用于页面显示价格与下单那一刻价格不一致的提示
- `software_init` `boolean` **(必填)**：是否需要安装部分软件
- `discount_relation_id` `integer | null` **(必填)**：使用算力券的ID

**请求示例（示例 1）**：

```json
// 组网，inner传入object数量根据实际设备数（多个）
// {
//     "billing_type": "Hour",
//     "buy_count": 2,
//     "inner": [
//         {
//             "device_id": 1,
//             "unit_price": 15000000
//         },
//         {
//             "device_id": 2,
//             "unit_price": 15000000
//         }
//     ],
//     "software_init": true,
//     "discount_relation_id": null
// }
// 单机，buy_count为多个时，inner也只传入1个object
{
    "billing_type": "Hour",
    "buy_count": 3,
    "inner": [
        {
            "device_id": 690,
            "unit_price": 15000000
        }
    ],
    "software_init": false,
    "discount_relation_id": null
}
```

## 响应（200）

- `code` `string` **(必填)**
- `message` `string` **(必填)**
- `data` `object` **(必填)**
  - `order_id` `integer` **(必填)**：订单ID

响应名：成功

**响应示例（成功示例）**：

```json
{
  "code": "0000",
  "message": "success",
  "data": {
    "order_id": 1
  }
}
```

---
*本文档由 fetch_apifox.py 从 Apifox 分享文档 6aa360d3-d8f2-471e-b841-3a35c33a7b7c 实时同步生成；同步时间见仓库根 .apifox-sync-manifest.json*
