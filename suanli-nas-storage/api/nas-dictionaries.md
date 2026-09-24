# 查询集群存储字典

> 来源：Apifox 官方文档（实时同步） · 分组：共绩算力 Open API/存储/集群存储/存储卷
> 远端最后更新：2026-09-11T08:55:26.000Z
> 端点：`GET /api/storage/nas/v1/dictionaries`

### **接口说明**

| 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
| --- | --- | --- | --- |
| v1.0.0 | - | 否 | 是 |

### **描述**

查询当前租户可选的地域和存储规格。
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
  - `regions` `array` **(必填)**：地域列表
    - **array<object>**
      - `tag` `string` **(必填)**：地域标识
      - `name` `string` **(必填)**：地域名称
  - `storage_classes` `array` **(必填)**：存储规格列表
    - **array<object>**
      - `storage_class` `string` **(必填)**：规格标识
      - `storage_class_name` `string` **(必填)**：规格名称
- `code` `any` **(必填)**
- `message` `string | null` **(必填)**：响应信息

**响应示例（成功示例）**：

```json
{
  "code": "0000",
  "message": "success",
  "data": {
    "regions": [
      {
        "tag": "bj-001",
        "name": "北京一区"
      },
      {
        "tag": "sh-001",
        "name": "上海一区"
      }
    ],
    "storage_classes": [
      {
        "storage_class": "nfs-standard",
        "storage_class_name": "标准型"
      },
      {
        "storage_class": "nfs-premium",
        "storage_class_name": "高性能型"
      }
    ]
  }
}
```

---
*本文档由 fetch_apifox.py 从 Apifox 分享文档 6aa360d3-d8f2-471e-b841-3a35c33a7b7c 实时同步生成；同步时间见仓库根 .apifox-sync-manifest.json*
