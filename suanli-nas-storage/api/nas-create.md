# 创建集群存储卷

> 来源：Apifox 官方文档（实时同步） · 分组：共绩算力 Open API/存储/集群存储/存储卷
> 远端最后更新：2026-09-11T08:53:33.000Z
> 端点：`POST /api/storage/nas/v1/create`

### **接口说明**

| 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
| --- | --- | --- | --- |
| v1.0.0 | - | 否 | 是 |

### **描述**

创建集群存储卷。受理成功后 status 为 Creating，开通完成后变为 Active。
加签详见：[加签流程](https://suanli.cn/docs/platform/openapi/m3p6whioxidzwaksughc4gfhnro/#45-%E5%8A%A0%E7%AD%BE%E6%B5%81%E7%A8%8B)

## header 参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `token` | string | 是 | 请填入您在平台内创建的 API 密钥，获取路径为：右上角头像 → API 密钥。（示例：a69abd35-1df0-4c21-9c2b-82a20a72d3b2-20260417200925） |
| `timestamp` | integer | 是 | 时间戳（示例：{{$date.millisecondsTimestamp}}） |
| `version` | string | 是 | 固定值（示例：1.0.0） |
| `sign_str` | string | 否 | 如果token为简易模式则无需填写此字段 |

## 请求体

Content-Type: `application/json`

- `name` `string` **(必填)**：卷名称 — 去除首尾空格后长度为 1 至 32 个字符
- `nas_config_id` `integer` **(必填)**：存储配置 ID
- `total_size` `integer` **(必填)**：容量 — 单位为字节，必须大于 0

**请求示例（示例）**：

```json
{
  "name": "my-volume",
  "nas_config_id": 10,
  "total_size": 1073741824
}
```

## 响应（200）

**响应示例（成功示例）**：

```json
{
  "code": "0000",
  "message": "success",
  "data": {
    "storage_id": 1001,
    "status": "Creating",
    "message": null
  }
}
```

---
*本文档由 fetch_apifox.py 从 Apifox 分享文档 6aa360d3-d8f2-471e-b841-3a35c33a7b7c 实时同步生成；同步时间见仓库根 .apifox-sync-manifest.json*
