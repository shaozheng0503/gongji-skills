# 弹性部署/云主机-时间维度计费查询接口

> 来源：Apifox 官方文档（实时同步） · 分组：共绩算力 Open API/费用
> 远端最后更新：2026-06-30T09:52:23.000Z
> 端点：`GET /api/billing/get_billing_record`

| 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
| --- | --- | --- | --- |
| v1.0.0 | - | 否 | 是 |

### **描述**
查询弹性部署/云主机的计费信息。

## query 参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `range` | string | 是 | 时间粒度（示例：day） |
| `start_time` | string | 否 | 开始时间(RFC3339格式)（示例：2026-01-01T00:00:00+08:00） |
| `end_time` | string | 否 | 结束时间(RFC3339格式)（示例：2026-01-02T23:59:59+08:00） |
| `task_ids` | string | 否 | 任务ID列表(空字符串表示全部任务)（示例：1,2,3,4） |
| `page` | number | 否 | 页码 |
| `page_size` | number | 否 | 每页条数 |

## header 参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `token` | string | 是 | 请填入您在平台内创建的 API 密钥，获取路径为：右上角头像 → API 密钥。 |
| `timestamp` | number | 是 | 时间戳（示例：1770194570564） |
| `version` | string | 是 | 固定值（示例：1.0.0） |

## 响应（200）

- `data` `object | null` **(必填)**
  - `count` `number` **(必填)**
  - `results` `array` **(必填)**
    - **array<object>**
      - `billing_coin` `number` **(必填)**：总账，虚拟积分，计算方式：1(人民币)元=100000积分
      - `discount_coin` `number` **(必填)**：优惠抵扣，虚拟积分，计算方式：1(人民币)元=100000积分
      - `start_time` `string` **(必填)**：开始时间
      - `end_time` `string` **(必填)**：结束时间

响应名：成功

---
*本文档由 fetch_apifox.py 从 Apifox 分享文档 6aa360d3-d8f2-471e-b841-3a35c33a7b7c 实时同步生成；同步时间见仓库根 .apifox-sync-manifest.json*
