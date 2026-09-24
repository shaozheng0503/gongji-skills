# 任务修改接口

> 来源：Apifox 官方文档（实时同步） · 分组：共绩算力 Open API/弹性部署服务任务
> 远端最后更新：2026-08-28T08:05:43.000Z
> 端点：`POST /api/deployment/task/update`

| 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
| --- | --- | --- | --- |
| v1.0.0 | - | 否 | 是 |

### **描述**
更新已有任务配置。

修改接口将对原有配置**整体覆盖更新**，不支持局部字段修改。

因此，调用接口时，请求数据结构必须与 [任务详情查询接口](apifox://link/endpoint/296882076) 响应中的任务配置在结构上保持**完全一致**。

同时，由于接口文档在一定情况下可能存在滞后，或任务配置中可能包含系统依赖字段。为了避免因字段缺失等导致校验异常，所以代码编写时应基于 [任务详情查询接口](apifox://link/endpoint/296882076) 返回的完整配置进行**修改后回传**。

## header 参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `token` | string | 是 | 请填入您在平台内创建的 API 密钥，获取路径为：右上角头像 → API 密钥。 |
| `timestamp` | number | 是 | 时间戳（示例：1770194570564） |
| `version` | string | 是 | 固定值（示例：1.0.0） |

## 请求体

Content-Type: `application/json`

- `task_id` `number | null`：任务id
- `task_type` `string | null`：任务类型
- `task_name` `string` **(必填)**：任务名称
- `namespace` `string | null`：命名空间
- `repository_username` `string | null`：私有仓库用户名 — 为仅写字段（write-only），仅在提交请求时生效，查询接口不返回。 暂不支持创建后更新。
- `repository_password` `string | null`：私有仓库密码 — 为仅写字段（write-only），仅在提交请求时生效，查询接口不返回。 暂不支持创建后更新。
- `status` `string | null`：任务状态，枚举: `Pending`/`Running`/`Paused`/`End`/`Other`
- `points` `number | null`：节点数量
- `runing_points` `number | null`：运行中节点数
- `billing_points` `number | null`：计费中节点数
- `billing_value` `number | null`：累计花费金额
- `forecast_value` `number | null`：实时花费金额
- `scheduler_strategy` `object | null`：跨区调度
  - `mode` `string` **(必填)**
- `task_qos` `object | null`：CPU独占
  - `class` `string` **(必填)**
- `load_balance` `object | null`：负载均衡
  - `type` `string` **(必填)**：负载均衡策略，枚举: `LeastConnection`/`RoundRobin`/`Random`/`IpHash`/`HeaderHash`/`CookieHash`
  - `params` `object | null`：负载均衡策略参数
    - `header` `string | null` **(必填)**：HTTP Header 名称 — 仅当 type 为 HeaderHash
    - `cookie` `string | null` **(必填)**：Cookie 名称 — 仅当 type 为 CookieHash
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
    - `resource` `object | null`：资源信息
      - `device_name` `string` **(必填)**：设备名称
      - `region` `string` **(必填)**：区域唯一标识
      - `gpu_name` `string | null`：GPU名称
      - `gpu_count` `integer` **(必填)**：GPU数量
      - `gpu_memory` `integer` **(必填)**：GPU显存
      - `memory` `integer` **(必填)**：内存
      - `cpu_cores` `integer` **(必填)**：CPU核数
    - `region_name` `string | null`：地区名称
    - `mark` `string` **(必填)**：资源唯一标识
- `services` `array` **(必填)**
  - **array<object>**
    - `service_id` `number | null`：服务id
    - `service_name` `string` **(必填)**：服务名称
    - `service_image` `string` **(必填)**：服务镜像
    - `env` `string | null`：环境变量
    - `shared_mem_size` `number | null`：共享内存
    - `storage_config` `array | null`：s3存储配置
    - `share_storage_config` `array | null`：共享存储配置
    - `remote_ports` `array` **(必填)**：服务端口暴露列表
      - **array<object>**
        - `url` `string | null`：服务回传链接
        - `service_port` `integer` **(必填)**：服务端口暴露
    - `health_checks` `object` **(必填)**：健康检查
      - `liveness_probe` `object` **(必填)**：存活探针
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

## 响应（200）

- `data` `null` **(必填)**

响应名：成功

**响应示例（成功示例）**：

```json
{
  "code": "0000",
  "message": "success",
  "data": null
}
```

---
*本文档由 fetch_apifox.py 从 Apifox 分享文档 6aa360d3-d8f2-471e-b841-3a35c33a7b7c 实时同步生成；同步时间见仓库根 .apifox-sync-manifest.json*
