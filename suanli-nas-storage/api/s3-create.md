# 创建对象存储互传任务

> 来源：Apifox 官方文档（实时同步） · 分组：共绩算力 Open API/存储/集群存储/S3互传
> 远端最后更新：2026-09-11T08:50:51.000Z
> 端点：`POST /api/storage/nas/v1/encrypt/s3/create`

### **接口说明**

| 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
| --- | --- | --- | --- |
| v1.0.0 | - | 是 | 是 |

### **描述**

在指定卷下创建对象存储互传任务。关联卷必须为 Active。AccessKey 和 SecretKey 仅用于本次请求，不会保存。受理成功后 status 为 Queuing。
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

- `storage_id` `integer` **(必填)**：卷 ID — 必须大于 0，且卷状态为 Active
- `name` `string`：任务名称 — 为空时由系统生成
- `direction` `any` **(必填)**
- `s3_supplier` `string` **(必填)**：对象存储厂商 — 支持的厂商列表：tos (火山引擎),tencent (腾讯云),aliyun (阿里云),huaweicloud (华为云)，s3compatible（MinIO）
- `s3_endpoint` `string` **(必填)**：对象存储 Endpoint
- `s3_access_key` `string` **(必填)**：AccessKey — 仅用于本次请求，不会保存
- `s3_secret_key` `string` **(必填)**：SecretKey — 仅用于本次请求，不会保存
- `s3_bucket` `string` **(必填)**：Bucket 名称
- `s3_prefix` `string | null`：对象前缀 — 为空时默认为根路径
- `nas_path` `string | null`：集群存储路径 — 为空时默认为根路径
- `overwrite_policy` `any`
- `ignore_patterns` `array | null`：忽略规则 — 按文件名后缀过滤，如 .tmp、.log。为空时不同步过滤

**请求示例（示例）**：

```json
{
  "storage_id": 1001,
  "name": "prod-backup-sync",
  "direction": 1,
  "s3_supplier": "tencent",
  "s3_endpoint": "cos.ap-guangzhou.myqcloud.com",
  "s3_access_key": "your-access-key",
  "s3_secret_key": "your-secret-key",
  "s3_bucket": "company-backups",
  "s3_prefix": "nas-sync/",
  "nas_path": "/data/incoming",
  "overwrite_policy": 2,
  "ignore_patterns": [
    ".log",
    ".tmp"
  ]
}
```

## 响应（200）

**响应示例（成功示例）**：

```json
{
  "code": "0000",
  "message": "success",
  "data": {
    "id": 501,
    "status": "Queuing"
  }
}
```

---
*本文档由 fetch_apifox.py 从 Apifox 分享文档 6aa360d3-d8f2-471e-b841-3a35c33a7b7c 实时同步生成；同步时间见仓库根 .apifox-sync-manifest.json*
