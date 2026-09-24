# 查询对象存储互传任务详情

> 来源：Apifox 官方文档（实时同步） · 分组：共绩算力 Open API/存储/集群存储/S3互传
> 远端最后更新：2026-09-11T08:51:08.000Z
> 端点：`GET /api/storage/nas/v1/s3/detail`

### **接口说明**

| 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
| --- | --- | --- | --- |
| v1.0.0 | - | 否 | 是 |

### **描述**

按任务 ID 查询对象存储互传详情。应答字段与列表项一致，不含 AccessKey 和 SecretKey。
加签详见：[加签流程](https://suanli.cn/docs/platform/openapi/m3p6whioxidzwaksughc4gfhnro/#45-%E5%8A%A0%E7%AD%BE%E6%B5%81%E7%A8%8B)

## query 参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `id` | integer | 是 | 任务 ID，必须大于 0（示例：501） |

## header 参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `token` | string | 是 | 请填入您在平台内创建的 API 密钥，获取路径为：右上角头像 → API 密钥。（示例：a69abd35-1df0-4c21-9c2b-82a20a72d3b2-20260417200925） |
| `timestamp` | integer | 是 | 时间戳（示例：{{$date.millisecondsTimestamp}}） |
| `version` | string | 是 | 固定值（示例：1.0.0） |
| `sign_str` | string | 否 | 如果token为简易模式则无需填写此字段 |

## 响应（200）

- `data` `null` **(必填)**
- `code` `any` **(必填)**
- `message` `string | null` **(必填)**：响应信息

**响应示例（成功示例）**：

```json
{
  "code": "0000",
  "message": "success",
  "data": {
    "id": 501,
    "name": "s3-sync-demo",
    "ready_files": 15,
    "total_files": 100,
    "transferred_bytes": 5242880,
    "total_bytes": 104857600,
    "create_time": "2026-07-05 10:00:00",
    "end_time": null,
    "status": "Exception",
    "direction": 1,
    "remaining_seconds": 0,
    "speed": "5MB/s",
    "bps": 5242880,
    "last_update_time": "2026-07-05 10:30:00",
    "storage_id": 1001,
    "s3_supplier": "tencent",
    "s3_endpoint": "cos.ap-guangzhou.myqcloud.com",
    "s3_bucket": "my-backup-bucket",
    "s3_prefix": "project/data/",
    "nas_path": "/data/backup",
    "overwrite_policy": 2,
    "ignore_patterns": [
      ".tmp",
      ".log"
    ],
    "error_code": "S410",
    "error_message": "S3 任务创建失败",
    "storage_name": "my-volume"
  }
}
```

---
*本文档由 fetch_apifox.py 从 Apifox 分享文档 6aa360d3-d8f2-471e-b841-3a35c33a7b7c 实时同步生成；同步时间见仓库根 .apifox-sync-manifest.json*
