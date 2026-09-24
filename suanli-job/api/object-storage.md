# 查询对象存储列表

> 来源：Apifox 官方文档（实时同步） · 分组：共绩算力 Open API/存储/对象存储
> 远端最后更新：2026-07-15T11:48:22.000Z
> 端点：`GET /api/storage/get_storage`

| 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
| --- | --- | --- | --- |
| v1.0.0 | - | 否 | 是 |

### **描述**
分页查询租户下的对象存储列表，可按对象存储状态筛选。返回对象存储基础信息、激活区域、关联部署、同步状态和错误信息。
加签详见：[加签流程](https://suanli.cn/docs/platform/openapi/m3p6whioxidzwaksughc4gfhnro/#45-%E5%8A%A0%E7%AD%BE%E6%B5%81%E7%A8%8B)

## query 参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `storage_type` | string | 否 | 存储类型；对象存储场景传 Juicefs，不传时默认 Juicefs |
| `status` | string | 否 | 对象存储状态，多个状态使用英文逗号分隔，例如 Activate,Unactivated；可选值：Activate（已激活）、Unactivated（未激活）、Delete（已删除）。 |
| `page` | integer | 否 | 页码，从 1 开始；需要与 page_size 同时传入 |
| `page_size` | integer | 否 | 每页数量；需要与 page 同时传入 |

## header 参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `token` | string | 是 | 请填入您在平台内创建的 API 密钥，获取路径为：右上角头像 → API 密钥。（示例：a69abd35-1df0-4c21-9c2b-82a20a72d3b2-20260417200925） |
| `timestamp` | integer | 是 | 时间戳（示例：{{$date.millisecondsTimestamp}}） |
| `version` | string | 是 | 固定值（示例：1.0.0） |
| `sign_str` | string | 否 | 如果token为简易模式则无需填写此字段 |

## 响应（200）

- `data` `object` **(必填)**
  - `count` `integer` **(必填)**：总数
  - `results` `array` **(必填)**：对象存储列表
    - **array<object>**
      - `storage_id` `integer` **(必填)**：对象存储 ID
      - `storage_type` `string | null`：storage_type：存储类型；Juicefs（对象存储）、ShareStorage（共享存储）
      - `juicefs_region_id` `integer` **(必填)**：OSS 供应商区域 ID
      - `juicefs_file_system_name` `string`：Juicefs文件系统名
      - `storage_name` `string` **(必填)**：对象存储名称
      - `k3s_cloud_name` `string` **(必填)**：OSS 供应商名称
      - `k3s_region_name` `string` **(必填)**：OSS 供应商区域名称
      - `regions` `array | null`：支持区域
      - `activate_regions` `array | null`：已激活区域
      - `bucket` `string` **(必填)**：桶名称
      - `size` `integer | null`：容量
      - `dir` `string` **(必填)**：目录前缀
      - `endpoint` `string` **(必填)**：Endpoint
      - `status` `string` **(必填)**：status：存储状态；Activate（已激活）、Unactivated（未激活）、Delete（已删除）。
      - `last_sync_time` `string | null`：最后同步时间
      - `deployments` `array | null`：关联部署
      - `remark` `string | null`：备注
      - `use_size` `integer | null`：已使用容量
      - `create_time` `string` **(必填)**：创建时间
      - `share_storage_type` `string | null`：share_storage_type：共享存储类型；Single（单区域）、Multiple（多区域）
      - `syncing_regions` `array | null`：同步中区域
      - `storage_error` `object`
        - `stage` `string` **(必填)**：阶段 — 例如 activate、sync
        - `operation` `string` **(必填)**：操作 — 例如 volume_create、volume_sync
        - `code` `string` **(必填)**：错误码
        - `message` `string | null`：错误信息
        - `last_update_time` `string` **(必填)**：最后更新时间
      - `regions_status` `array | null`：区域状态
      - `syncing_metadata_status` `object`
        - `type` `string` **(必填)**：type：同步类型；Import（导入）、Delete（删除）
        - `status` `string` **(必填)**：status：同步状态；success（成功）、failed（失败）
        - `task_id` `string` **(必填)**：任务 ID
        - `progress` `integer | null`：同步进度
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
        "storage_id": 33,
        "storage_type": "Juicefs",
        "juicefs_region_id": 22,
        "juicefs_file_system_name": "tos-45-20260514015999",
        "storage_name": "火山引擎",
        "k3s_cloud_name": "火山引擎",
        "k3s_region_name": "华北2 - 北京",
        "regions": [
          {
            "tag": "cn-fujian-5",
            "name": "福建五区"
          },
          {
            "tag": "cn-shanghai-4",
            "name": "上海四区"
          }
        ],
        "activate_regions": [
          {
            "tag": "cn-fujian-5",
            "name": "福建五区"
          },
          {
            "tag": "cn-shanghai-4",
            "name": "上海四区"
          },
          {
            "tag": "cn-sichuan-5",
            "name": "四川五区"
          }
        ],
        "bucket": "go11jing",
        "size": 6407213056,
        "dir": "/11",
        "endpoint": "https://tos-s3-323com",
        "status": "Activate",
        "last_sync_time": "2026-07-14T16:52:18.565370+08:00",
        "deployments": null,
        "remark": null,
        "use_size": 6407213056,
        "create_time": "2026-05-14T09:50:18.231650+08:00",
        "share_storage_type": null,
        "syncing_regions": null,
        "storage_error": null,
        "regions_status": [
          {
            "status": "Activate",
            "progress": 100,
            "region": "cn-fujian-5",
            "region_name": "福建五区",
            "last_completed_time": null
          },
          {
            "status": "Activate",
            "progress": 100,
            "region": "fjsq",
            "region_name": "福建四区",
            "last_completed_time": null
          },
          {
            "status": "Error",
            "progress": null,
            "region": "guangdong",
            "region_name": "广东一区",
            "last_completed_time": null
          }
        ],
        "syncing_metadata_status": null
      }
    ]
  }
}
```

---
*本文档由 fetch_apifox.py 从 Apifox 分享文档 6aa360d3-d8f2-471e-b841-3a35c33a7b7c 实时同步生成；同步时间见仓库根 .apifox-sync-manifest.json*
