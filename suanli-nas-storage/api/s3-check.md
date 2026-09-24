# 校验对象存储连接

> 来源：Apifox 官方文档（实时同步） · 分组：共绩算力 Open API/存储/集群存储/S3互传
> 远端最后更新：2026-09-11T08:48:50.000Z
> 端点：`POST /api/storage/nas/v1/encrypt/s3/check`

### **接口说明**

| 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
| --- | --- | --- | --- |
| v1.0.0 | - | 是 | 是 |

### **描述**

校验对象存储连接是否可用。AccessKey 和 SecretKey 仅用于本次请求，不会保存。接口成功时请以 data.pass 判断连接是否通过。
加签和加密详见：[加签流程](https://suanli.cn/docs/platform/openapi/m3p6whioxidzwaksughc4gfhnro/#45-%E5%8A%A0%E7%AD%BE%E6%B5%81%E7%A8%8B)和[加密流程](https://suanli.cn/docs/platform/openapi/m3p6whioxidzwaksughc4gfhnro/#46-%E5%8A%A0%E5%AF%86%E6%B5%81%E7%A8%8B)

## header 参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `token` | string | 是 | 请填入您在平台内创建的 API 密钥，获取路径为：右上角头像 → API 密钥。（示例：a69abd35-1df0-4c21-9c2b-82a20a72d3b2-20260417200925） |
| `timestamp` | integer | 是 | 时间戳（示例：{{$date.millisecondsTimestamp}}） |
| `version` | string | 是 | 固定值（示例：1.0.0） |
| `sign_str` | string | 否 | 如果token为简易模式则无需填写此字段 |

## 请求体

Content-Type: `application/json`

- `supplier` `string` **(必填)**：对象存储厂商 — 如 tencent、aws、aliyun、minio
- `endpoint` `string` **(必填)**：对象存储 Endpoint
- `ak` `string` **(必填)**：AccessKey — 仅用于本次请求，不会保存
- `sk` `string` **(必填)**：SecretKey — 仅用于本次请求，不会保存
- `bucket` `string` **(必填)**：Bucket 名称
- `prefix` `string` **(必填)**：对象前缀

**请求示例（示例）**：

```json
{
  "supplier": "tencent",
  "endpoint": "cos.ap-guangzhou.myqcloud.com",
  "ak": "your-access-key",
  "sk": "your-secret-key",
  "bucket": "my-bucket",
  "prefix": "/data/"
}
```

## 响应（200）

- `data` `object` **(必填)**
  - `pass` `boolean` **(必填)**：是否通过
  - `message` `string | null`：说明
- `code` `any` **(必填)**
- `message` `string | null` **(必填)**：响应信息

**响应示例（成功示例）**：

```json
{
  "code": "0000",
  "message": "success",
  "data": {
    "pass": true,
    "message": null
  }
}
```

---
*本文档由 fetch_apifox.py 从 Apifox 分享文档 6aa360d3-d8f2-471e-b841-3a35c33a7b7c 实时同步生成；同步时间见仓库根 .apifox-sync-manifest.json*
