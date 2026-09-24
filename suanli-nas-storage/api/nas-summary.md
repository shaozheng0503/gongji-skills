# 查询集群存储用量概览

> 来源：Apifox 官方文档（实时同步） · 分组：共绩算力 Open API/存储/集群存储/存储卷
> 远端最后更新：2026-09-11T08:55:53.000Z
> 端点：`GET /api/storage/nas/v1/summary`

### **接口说明**

| 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
| --- | --- | --- | --- |
| v1.0.0 | - | 否 | 是 |

### **描述**

查询当前租户集群存储卷的数量、容量、已用量和预估费用。仅统计创建中、可用、扩容中的卷。
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
  - `volume_count` `integer` **(必填)**：卷数量 — 仅统计 Creating、Active、Expanding
  - `total_size` `integer` **(必填)**：总容量 — 单位为字节
  - `used_size` `integer` **(必填)**：已使用容量，负数时表示存在不支持获取已用容量的存储配置 — 单位为字节
  - `estimated_price` `integer | null`：预估每10分钟单价，积分/10分钟/GB — 有效卷单价的算术平均。无卷时为 null，单位：积分/10分钟/GB
  - `coin_sum_slice` `integer` **(必填)**：预估每10分钟总价，积分/10分钟/GB — 每 10 分钟预估消耗，单位为积分
- `code` `any` **(必填)**
- `message` `string | null` **(必填)**：响应信息

**响应示例（成功示例）**：

```json
{
  "code": "0000",
  "message": "success",
  "data": {
    "volume_count": 3,
    "total_size": 3221225472,
    "used_size": 1073741824,
    "estimated_price": 120,
    "coin_sum_slice": 360
  }
}
```

---
*本文档由 fetch_apifox.py 从 Apifox 分享文档 6aa360d3-d8f2-471e-b841-3a35c33a7b7c 实时同步生成；同步时间见仓库根 .apifox-sync-manifest.json*
