# 任务创建接口

> 来源：Apifox 官方文档（实时同步） · 分组：共绩算力 Open API/弹性部署服务任务
> 远端最后更新：2026-07-15T07:14:18.000Z
> 端点：`POST /api/deployment/task/create`

| 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
| --- | --- | --- | --- |
| v1.0.0 | - | 否 | 是 |

### **描述**
创建弹性部署任务。

数据结构中的 `resources.item.mark(资源唯一标识)` 需要从 [获取设备资源列表](apifox://link/endpoint/296881020) 接口获取

## header 参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `token` | string | 是 | 请填入您在平台内创建的 API 密钥，获取路径为：右上角头像 → API 密钥。 |
| `timestamp` | number | 是 | 时间戳（示例：1770194570564） |
| `version` | string | 是 | 固定值（示例：1.0.0） |

## 请求体

Content-Type: `application/json`

- `task_type` `string | null`：任务类型
- `task_name` `string` **(必填)**：任务名称
- `repository_username` `string | null`：私有仓库用户名 — 为仅写字段（write-only），仅在提交请求时生效，查询接口不返回。 暂不支持创建后更新。
- `repository_password` `string | null`：私有仓库密码 — 为仅写字段（write-only），仅在提交请求时生效，查询接口不返回。 暂不支持创建后更新。
- `points` `number | null`：节点数量
- `scheduler_strategy` `object | null`：跨区调度
  - `mode` `string` **(必填)**
- `task_qos` `object | null`：CPU独占
  - `class` `string` **(必填)**
- `load_balance` `object | null`：负载均衡
  - `type` `string` **(必填)**：负载均衡策略 — 负载均衡类型，枚举: `LeastConnection`/`RoundRobin`/`Random`/`IpHash`/`HeaderHash`/`CookieHash`
  - `params` `object | null`：负载均衡策略参数
    - `header` `string | null`：HTTP Header 名称 — 仅当 type 为 HeaderHash
    - `cookie` `string | null`：Cookie 名称 — 仅当 type 为 CookieHash
- `dynamic_pod_strategy` `object | null`：弹性扩缩容
  - `min_workers` `number` **(必填)**：最小节点数
  - `max_workers` `number` **(必填)**：最大节点数
  - `idle_timeout` `number` **(必填)**：空闲超时时间
  - `execution_timeout` `number` **(必填)**：执行超时时间
  - `switch` `boolean` **(必填)**：开关
  - `benchmark` `array` **(必填)**：策略配置
    - **array<any>**
- `resources` `array` **(必填)**：资源列表
  - **array<object>**
- `services` `array` **(必填)**
  - **array<object>**
    - `service_name` `string` **(必填)**：服务名称
    - `service_image` `string` **(必填)**：服务镜像
    - `env` `string | null`：环境变量
    - `shared_mem_size` `number | null`：共享内存
    - `storage_config` `array | null`：s3存储配置
    - `share_storage_config` `array | null`：共享存储配置
    - `remote_ports` `array` **(必填)**：服务端口暴露列表
      - **array<object>**
        - `service_port` `integer` **(必填)**：服务端口暴露
    - `health_checks` `object | null`：健康检查
      - `liveness_probe` `any` **(必填)**：存活探针
        - `switch` `boolean` **(必填)**
        - `probe_type` `string` **(必填)**
        - `path` `string` **(必填)**
        - `port` `integer` **(必填)**
        - `initial_delay_seconds` `integer` **(必填)**
        - `period_seconds` `integer` **(必填)**
        - `timeout_seconds` `integer` **(必填)**
        - `failure_threshold` `integer` **(必填)**
      - `startup_probe` `any` **(必填)**：启动探针
      - `readiness_probe` `any` **(必填)**：就绪探针
    - `start_script_v2` `object | null`：启动命令
      - `command` `string | null`：命令
      - `args` `array` **(必填)**：参数列表
        - **array<string>**

**请求示例（最小示例）**：

```json
{
  "task_name": "d01081829-dailyhot10",
  "points": 1,
  "resources": [
    {
      "resource": {
        "device_name": "4090",
        "region": "beijing-jxq-p1",
        "gpu_name": "4090",
        "gpu_count": 1,
        "gpu_memory": 24560,
        "memory": 64512,
        "cpu_cores": 16
      },
      "region_name": "北京一区",
      "mark": "ha8GDGEAORN3a9Hhu7X+W/lveP9CW2eBkI+oB/QJLRcesfjQPO8rxr2V1LKPDHtvkAVlHT+6KSnXs0L1NxKyB6VS154UUBlufO9OrkJD9pAYRniwik7PgmExT5DghxIFTa4H6X/kCUuRlEn6BifjmItnR2CnXtghNqSTEUWVvy+bUdznvFvFJIycQ8SoQCNugw=="
    }
  ],
  "services": [
    {
      "remote_ports": [
        {
          "service_port": 6688
        },
        {
          "service_port": 80
        }
      ],
      "service_image": "harbor.suanleme.cn/public-hub/dailyhot:1.0",
      "env": null,
      "start_script_v2": {
        "args": [],
        "command": null
      },
      "service_name": "d1767868176690-5675100"
    }
  ]
}
```

## 响应（200）

- `data` `object | null` **(必填)**
  - `task_id` `number` **(必填)**

响应名：成功

**响应示例（Success）**：

```json
{
  "code": "0000",
  "message": "success",
  "data": {
    "task_id": 1
  }
}
```

---
*本文档由 fetch_apifox.py 从 Apifox 分享文档 6aa360d3-d8f2-471e-b841-3a35c33a7b7c 实时同步生成；同步时间见仓库根 .apifox-sync-manifest.json*
