# 镜像预热任务更新接口

> 来源：Apifox 官方文档（实时同步） · 分组：共绩算力 Open API/镜像预热任务(申请开通)
> 远端最后更新：2026-08-06T09:10:56.000Z
> 端点：`POST /api/task/image_preheat/update`

| 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
| --- | --- | --- | --- |
| v1.0.0 | - | 否 | 是 |

### **描述**
更新镜像预热任务节点数量。
加签详见：[加签流程](https://suanli.cn/docs/platform/openapi/m3p6whioxidzwaksughc4gfhnro/#45-%E5%8A%A0%E7%AD%BE%E6%B5%81%E7%A8%8B)

## header 参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `token` | string | 是 | 请填入您在平台内创建的 API 密钥，获取路径为：右上角头像 → API 密钥。 |
| `timestamp` | integer | 是 | 时间戳（示例：{{$date.millisecondsTimestamp}}） |
| `version` | string | 是 | 固定值（示例：1.0.0） |
| `sign_str` | string | 否 | 如果token为简易模式则无需填写此字段 |

## 请求体

Content-Type: `application/json`

- `task_id` `integer` **(必填)**：任务id
- `points` `integer` **(必填)**：节点数量

## 响应（200）

- `code` `string` **(必填)**：响应码 — 当code≠0000时，data必为null。，枚举: `0000`/`C999`/`C001`/`C002`/`C004`/`C005`/`C006`/`C007`/`C008`/`C009`/`C010`/`Z001`
- `message` `string | null` **(必填)**：响应信息
- `data` `null` **(必填)**

响应名：成功

**响应示例（示例）**：

```json
{
  "code": "0000",
  "message": "success",
  "data": null
}
```

---
*本文档由 fetch_apifox.py 从 Apifox 分享文档 6aa360d3-d8f2-471e-b841-3a35c33a7b7c 实时同步生成；同步时间见仓库根 .apifox-sync-manifest.json*
