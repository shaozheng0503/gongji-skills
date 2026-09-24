# 查询可创建的存储配置

> 来源：Apifox 官方文档（实时同步） · 分组：共绩算力 Open API/存储/集群存储/存储卷
> 远端最后更新：2026-09-11T08:55:01.000Z
> 端点：`GET /api/storage/nas/v1/pre-create`

### **接口说明**

| 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
| --- | --- | --- | --- |
| v1.0.0 | - | 否 | 是 |

### **描述**

查询当前租户可用于创建卷的存储配置。Unavailable 表示暂不可选，不会返回已下线配置。
加签详见：[加签流程](https://suanli.cn/docs/platform/openapi/m3p6whioxidzwaksughc4gfhnro/#45-%E5%8A%A0%E7%AD%BE%E6%B5%81%E7%A8%8B)

## header 参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `token` | string | 是 | 请填入您在平台内创建的 API 密钥，获取路径为：右上角头像 → API 密钥。（示例：a69abd35-1df0-4c21-9c2b-82a20a72d3b2-20260417200925） |
| `timestamp` | integer | 是 | 时间戳（示例：{{$date.millisecondsTimestamp}}） |
| `version` | string | 是 | 固定值（示例：1.0.0） |
| `sign_str` | string | 否 | 如果token为简易模式则无需填写此字段 |

## 响应（200）

- `data` `object | null` **(必填)**
  - `configs` `array` **(必填)**：存储配置列表
    - **array<object>**
      - `id` `integer` **(必填)**：配置 ID
      - `name` `string` **(必填)**：配置名称
      - `description` `string | null`：配置说明
      - `region` `object` **(必填)**
        - `tag` `string` **(必填)**：地域标识
        - `name` `string` **(必填)**：地域名称
      - `storage_class` `string` **(必填)**：规格标识
      - `storage_class_name` `string` **(必填)**：规格名称
      - `total_capacity` `integer` **(必填)**：集群总容量 — 单位为字节
      - `allocated_capacity` `integer` **(必填)**：已分配容量 — 单位为字节
      - `used_capacity` `integer` **(必填)**：已使用容量 — 单位为字节
      - `unit_price` `integer` **(必填)**：单价 — 单位为积分每 GB 每 10 分钟
      - `display_unit_price` `string` **(必填)**：展示单价 — 单位为元每 GB 每月
      - `status` `any` **(必填)**
- `code` `any` **(必填)**
- `message` `string | null` **(必填)**：响应信息

**响应示例（成功示例）**：

```json
{
  "code": "0000",
  "message": "success",
  "data": {
    "configs": [
      {
        "id": 10,
        "name": "北京标准型",
        "description": null,
        "region": {
          "tag": "bj-001",
          "name": "北京一区"
        },
        "storage_class": "nfs-standard",
        "storage_class_name": "标准型",
        "total_capacity": 1099511627776,
        "allocated_capacity": 107374182400,
        "used_capacity": 53687091200,
        "unit_price": 120,
        "display_unit_price": "0.36",
        "status": "Available"
      }
    ]
  }
}
```

---
*本文档由 fetch_apifox.py 从 Apifox 分享文档 6aa360d3-d8f2-471e-b841-3a35c33a7b7c 实时同步生成；同步时间见仓库根 .apifox-sync-manifest.json*
