# 查询集群存储卷列表

> 来源：Apifox 官方文档（实时同步） · 分组：共绩算力 Open API/存储/集群存储/存储卷
> 远端最后更新：2026-09-11T08:54:25.000Z
> 端点：`GET /api/storage/nas/v1/list`

### **接口说明**

| 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
| --- | --- | --- | --- |
| v1.0.0 | - | 否 | 是 |

### **描述**

分页查询当前租户的集群存储卷。statuses 中的 Deleted 会被忽略。
加签详见：[加签流程](https://suanli.cn/docs/platform/openapi/m3p6whioxidzwaksughc4gfhnro/#45-%E5%8A%A0%E7%AD%BE%E6%B5%81%E7%A8%8B)

## query 参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `regions` | string | 否 | 地域标识，多个值用英文逗号分隔（示例：bj-001,sh-001） |
| `storage_class` | string | 否 | 存储规格标识，多个值用英文逗号分隔（示例：nfs-standard） |
| `statuses` | string | 否 | 卷状态，多个值用英文逗号分隔。可选值 Creating（创建中）、Active（可用）、Expanding（扩容中）、Deleting（删除中）、Exception（异常）。Deleted 会被忽略。（示例：Creating,Active） |
| `storage_ids` | string | 否 | 卷 ID，多个值用英文逗号分隔（示例：1001,1002） |
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
  - `count` `integer` **(必填)**：总条数
  - `results` `array` **(必填)**：当前页数据
    - **array<object>**
      - `storage_id` `integer` **(必填)**：卷 ID
      - `name` `string` **(必填)**：卷名称
      - `region` `object` **(必填)**
        - `tag` `string` **(必填)**：地域标识
        - `name` `string` **(必填)**：地域名称
      - `storage_class` `string` **(必填)**：规格标识
      - `storage_class_name` `string` **(必填)**：规格名称
      - `unit_price` `integer` **(必填)**：单价 — 单位为积分每 GB 每 10 分钟
      - `display_unit_price` `string` **(必填)**：展示单价 — 单位为元每 GB 每月
      - `total_size` `integer` **(必填)**：总容量 — 单位为字节
      - `used_size` `integer` **(必填)**：已使用容量，负数表示该存储后端暂未接入容量统计，已用容量信息不可用，存储功能不受影响 — 单位为字节
      - `status` `any` **(必填)**
      - `namespace` `string` **(必填)**：命名空间
      - `claim_name` `string` **(必填)**：存储声明名称
      - `instance_count` `integer` **(必填)**：挂载实例数
      - `instances` `array` **(必填)**：挂载实例列表
        - **array<object>**
          - `instance_id` `integer`：实例 ID
          - `instance_name` `string`：实例名称
          - `instance_type` `string`：实例类型
          - `mount_path` `string`：挂载路径
      - `create_time` `string` **(必填)**：创建时间 — 格式 yyyy-MM-dd HH:mm:ss
      - `last_update_time` `string` **(必填)**：更新时间 — 格式 yyyy-MM-dd HH:mm:ss
      - `error_code` `string | null`：错误码
      - `error_message` `string | null`：错误信息
- `code` `any` **(必填)**
- `message` `string | null` **(必填)**：响应信息

**响应示例（成功示例）**：

```json
{
  "code": "0000",
  "message": "success",
  "data": {
    "count": 1,
    "results": [
      {
        "storage_id": 1001,
        "name": "my-volume",
        "region": {
          "tag": "bj-001",
          "name": "北京一区"
        },
        "storage_class": "nfs-standard",
        "storage_class_name": "标准型",
        "unit_price": 120,
        "display_unit_price": "0.36",
        "total_size": 1073741824,
        "used_size": 268435456,
        "status": "Active",
        "namespace": "tenant-ns",
        "claim_name": "pvc-1001",
        "instance_count": 1,
        "instances": [
          {
            "instance_id": 2001,
            "instance_name": "training-job-1",
            "instance_type": "deployment",
            "mount_path": "/data/nas"
          }
        ],
        "create_time": "2026-06-12 10:00:00",
        "last_update_time": "2026-06-12 12:30:00",
        "error_code": null,
        "error_message": null
      }
    ]
  }
}
```

---
*本文档由 fetch_apifox.py 从 Apifox 分享文档 6aa360d3-d8f2-471e-b841-3a35c33a7b7c 实时同步生成；同步时间见仓库根 .apifox-sync-manifest.json*
