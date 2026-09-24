# 已购设备取消自动续费

> 来源：Apifox 官方文档（实时同步） · 分组：共绩算力 Open API/裸金属/创建订单
> 远端最后更新：2026-08-06T07:41:23.000Z
> 端点：`POST /api/output/v2/auto_renew_device_config/delete_auto_renew_config`

| 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
| --- | --- | --- | --- |
| v1.0.0 | - | 否 | 是 |

### **描述**
已购买设备取消自动续费。

## 请求体

Content-Type: `application/json`

- `device_id` `integer` **(必填)**：设备ID

**请求示例（示例 1）**：

```json
{
  "device_id": 250
}
```

## 响应（200）

- `code` `string` **(必填)**
- `message` `string` **(必填)**
- `data` `null` **(必填)**

响应名：成功

**响应示例（成功示例）**：

```json
{
  "code": "0000",
  "message": "success",
  "data": null
}
```

---
*本文档由 fetch_apifox.py 从 Apifox 分享文档 6aa360d3-d8f2-471e-b841-3a35c33a7b7c 实时同步生成；同步时间见仓库根 .apifox-sync-manifest.json*
