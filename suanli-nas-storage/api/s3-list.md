# 查询对象存储互传任务列表

> 来源：Apifox 官方文档（实时同步） · 分组：共绩算力 Open API/存储/集群存储/S3互传
> 远端最后更新：2026-09-11T08:51:51.000Z
> 端点：`GET /api/storage/nas/v1/s3/list`

### **接口说明**

| 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
| --- | --- | --- | --- |
| v1.0.0 | - | 否 | 是 |

### **描述**

分页查询当前租户的对象存储互传任务。
加签详见：[加签流程](https://suanli.cn/docs/platform/openapi/m3p6whioxidzwaksughc4gfhnro/#45-%E5%8A%A0%E7%AD%BE%E6%B5%81%E7%A8%8B)

## query 参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `storage_id` | integer | 否 | 关联卷 ID。不传或小于等于 0 时查询全部任务（示例：1001） |
| `statuses` | string | 否 | 任务状态，多个值用英文逗号分隔。可选值 Queuing（排队中）、Pending（处理中）、Running（运行中）、Stopped（已停止）、Completed（已完成）、Error（失败）、Exception（异常）（示例：Running,Exception） |
| `page` | integer | 否 | 页码，从 1 开始。小于等于 0 时按 1 处理（示例：1） |
| `page_size` | integer | 否 | 每页条数。小于等于 0 时按 10 处理，最大 100（示例：10） |

## header 参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `token` | string | 是 | 请填入您在平台内创建的 API 密钥，获取路径为：右上角头像 → API 密钥。（示例：a69abd35-1df0-4c21-9c2b-82a20a72d3b2-20260417200925） |
| `timestamp` | integer | 是 | 时间戳（示例：{{$date.millisecondsTimestamp}}） |
| `version` | string | 是 | 固定值（示例：1.0.0） |
| `sign_str` | string | 否 | 如果token为简易模式则无需填写此字段 |

## 响应（200）

- `data` `object | null` **(必填)**
  - `count` `integer` **(必填)**：总条数 — 受 statuses 和 storage_id 筛选影响
  - `status_counts` `object` **(必填)**
    - `pending` `integer` **(必填)**：处理中数量
    - `running` `integer` **(必填)**：运行中数量
    - `stopped` `integer` **(必填)**：已停止数量
    - `completed` `integer` **(必填)**：已完成数量
    - `error` `integer` **(必填)**：失败数量
    - `exception` `integer` **(必填)**：异常数量
    - `queuing` `integer` **(必填)**：排队中数量
  - `results` `array` **(必填)**：当前页数据
    - **array<object>**
      - `id` `integer` **(必填)**：任务 ID
      - `name` `string` **(必填)**：任务名称
      - `ready_files` `integer` **(必填)**：已传输文件数
      - `total_files` `integer` **(必填)**：总文件数 — 尚未统计完成时可能为 0
      - `transferred_bytes` `integer` **(必填)**：已传输字节数
      - `total_bytes` `integer` **(必填)**：总字节数 — 尚未统计完成时可能为 0
      - `create_time` `string` **(必填)**：创建时间 — 格式 yyyy-MM-dd HH:mm:ss
      - `end_time` `string | null`：结束时间 — 进行中为 null。格式 yyyy-MM-dd HH:mm:ss
      - `status` `any` **(必填)**
      - `direction` `any` **(必填)**
      - `remaining_seconds` `integer` **(必填)**：预估剩余秒数 — 无法估算或已结束时为 0
      - `speed` `string` **(必填)**：传输速率展示 — 已废弃，请使用 bps
      - `bps` `integer` **(必填)**：传输速率 — 单位为字节每秒。无法计算或已结束时为 0
      - `last_update_time` `string` **(必填)**：更新时间 — 格式 yyyy-MM-dd HH:mm:ss
      - `storage_id` `integer` **(必填)**：卷 ID
      - `s3_supplier` `string` **(必填)**：对象存储厂商
      - `s3_endpoint` `string` **(必填)**：对象存储 Endpoint
      - `s3_bucket` `string` **(必填)**：Bucket 名称
      - `s3_prefix` `string` **(必填)**：对象前缀
      - `nas_path` `string` **(必填)**：集群存储路径
      - `overwrite_policy` `any` **(必填)**
      - `error_code` `string | null`：错误码
      - `error_message` `string | null`：错误信息
      - `ignore_patterns` `array` **(必填)**：忽略规则
        - **array<string>**
      - `storage_name` `string` **(必填)**：卷名称
- `code` `any` **(必填)**
- `message` `string | null` **(必填)**：响应信息

**响应示例（成功示例）**：

```json
{
  "code": "0000",
  "message": "success",
  "data": {
    "count": 2,
    "status_counts": {
      "pending": 1,
      "running": 1,
      "stopped": 0,
      "completed": 0,
      "error": 0,
      "exception": 0,
      "queuing": 0
    },
    "results": [
      {
        "id": 501,
        "name": "s3-sync-demo",
        "ready_files": 42,
        "total_files": 100,
        "transferred_bytes": 20971520,
        "total_bytes": 104857600,
        "create_time": "2026-07-05 10:00:00",
        "end_time": null,
        "status": "Running",
        "direction": 1,
        "remaining_seconds": 360,
        "speed": "20MB/s",
        "bps": 20971520,
        "last_update_time": "2026-07-05 10:05:00",
        "storage_id": 1001,
        "s3_supplier": "tencent",
        "s3_endpoint": "cos.ap-guangzhou.myqcloud.com",
        "s3_bucket": "my-backup-bucket",
        "s3_prefix": "project/data/",
        "nas_path": "/data/backup",
        "overwrite_policy": 2,
        "error_code": null,
        "error_message": null,
        "ignore_patterns": [
          ".tmp"
        ],
        "storage_name": "my-volume"
      }
    ]
  }
}
```

---
*本文档由 fetch_apifox.py 从 Apifox 分享文档 6aa360d3-d8f2-471e-b841-3a35c33a7b7c 实时同步生成；同步时间见仓库根 .apifox-sync-manifest.json*
