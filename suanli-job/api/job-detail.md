# Job任务详情查询接口

> 来源：Apifox 官方文档（实时同步） · 分组：共绩算力 Open API/Job批处理任务
> 远端最后更新：2026-07-03T03:56:30.000Z
> 端点：`GET /api/task/job/detail`

| 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
| --- | --- | --- | --- |
| v1.0.0 | - | 否 | 是 |

### **描述**
获取Job批处理任务详情。
加签详见：[加签流程](https://suanli.cn/docs/platform/openapi/m3p6whioxidzwaksughc4gfhnro/#45-%E5%8A%A0%E7%AD%BE%E6%B5%81%E7%A8%8B)

## query 参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `task_id` | integer | 是 | 任务id（示例：1） |

## header 参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `token` | string | 是 | 请填入您在平台内创建的 API 密钥，获取路径为：右上角头像 → API 密钥。 |
| `timestamp` | integer | 是 | 时间戳（示例：{{$date.millisecondsTimestamp}}） |
| `version` | string | 是 | 固定值（示例：1.0.0） |
| `sign_str` | string | 否 | 如果token为简易模式则无需填写此字段 |

## 响应（200）

- `data` `object | null` **(必填)**
  - `task_id` `integer` **(必填)**：任务id
  - `task_name` `string` **(必填)**：任务名
  - `sub_type` `string | null`：子类型，枚举: `Spot`
  - `schedule_status` `string | null`：调度状态，枚举: `Scheduled`/`Queued`
  - `deployment_name` `string` **(必填)**
  - `resources` `array` **(必填)**：资源列表
    - **array<object>**
      - `resource` `object`：资源信息
        - `device_name` `string` **(必填)**：设备信息
        - `region` `string` **(必填)**：区域唯一标识
        - `gpu_name` `string | null`：GPU名称
        - `gpu_count` `integer` **(必填)**：GPU卡数
        - `gpu_memory` `integer` **(必填)**：GPU显存 — 单位为二进制兆字节(Mi)
        - `memory` `integer` **(必填)**：内存 — 单位为二进制兆字节(Mi)
        - `cpu_cores` `integer` **(必填)**：CPU核数 — 单位为核(CPU)
      - `region_name` `string`：区域名称
      - `mark` `string` **(必填)**：资源唯一标识
      - `weight` `integer | null`
  - `status` `string` **(必填)**，枚举: `Running`/`Pending`/`Paused`/`End`
  - `points` `integer` **(必填)**
  - `runing_points` `integer` **(必填)**
  - `billing_points` `integer` **(必填)**
  - `billing_time` `integer` **(必填)**
  - `billing_value` `integer` **(必填)**
  - `forecast_value` `integer` **(必填)**
  - `task_tags` `array | null`
  - `share_disk_volumes` `array | null`：声明共享磁盘卷，需在services中配置对应的share_disk_config进行卷挂载。
  - `share_mem_volumes` `array | null`：声明共享内存卷，需在services中配置对应的share_mem_config进行卷挂载。
  - `task_qos` `object | null`：CPU独占
    - `class` `string` **(必填)**，枚举: `Guaranteed`
  - `job_support` `object` **(必填)**
    - `estimated_exec_sec` `integer | null`：单元运行时间(秒) — 任务运行完成的预估时间，系统将基于此时间寻找最稳定的资源窗口。该字段仅在 Job 批处理任务的 sub_type 为 Spot 时生效且必填；其他 sub_type 类型下不生效。该值应比任务真正运行完成时间略长，比任务超时时间略短。
    - `timeout_sec` `integer` **(必填)**：任务超时时间(秒) — 任务从开始运行到结束的最长物理时间，超时系统将强制终止任务。
    - `parallelism` `integer` **(必填)**：并行节点数
    - `mod_param` `any` **(必填)**：完成模式参数 — 对于多节点并行任务，建议使用索引模式
  - `job_status` `object` **(必填)**
    - `create_time` `string | null`
    - `status` `string` **(必填)**，枚举: `Pending`/`Manual`/`Running`/`Complete`/`Failed`
    - `completion_time` `string | null`
    - `active_pods` `integer | null`
    - `succeeded_pods` `integer` **(必填)**
    - `failed_pods` `integer` **(必填)**
    - `completion_mode` `string | null`，枚举: `NonIndexed`
  - `job_group` `object | null`
    - `queue_id` `integer | null`：队列id
    - `queue_name` `string | null`：队列名称
    - `group_id` `integer` **(必填)**：组id
    - `group_name` `string` **(必填)**：组名称
  - `create_time` `string` **(必填)**
  - `last_update_time` `string` **(必填)**
  - `termination_grace_period_seconds` `integer | null`：优雅退出时间
  - `services` `array` **(必填)**
    - **array<object>**
      - `service_id` `integer | null`：服务id
      - `service_name` `string` **(必填)**：服务名
      - `service_image` `string` **(必填)**：服务镜像
      - `resource_weight` `object` **(必填)**：资源权重
        - `cpu_weight` `integer` **(必填)**：CPU权重 — CPU分配最小单位为豪核(m)，CPU权重需大于0
        - `mem_weight` `integer` **(必填)**：内存权重 — 内存分配最小单位为二进制兆字节(Mi)，内存权重需大于0
        - `gpu_weight` `integer` **(必填)**：GPU权重 — GPU分配最小单位为卡数，为防止GPU分配有剩余，各容器GPU权重之和需大于0且整除所选资源GPU卡数的最大公约数
      - `health_checks` `object | null`：健康检查
        - `liveness_probe` `object` **(必填)**：存活探针
          - `switch` `boolean` **(必填)**：开关
          - `probe_type` `string` **(必填)**：检查类型，枚举: `httpGet`/`tcpSocket`
          - `path` `string`：路径
          - `port` `integer` **(必填)**：服务端口
          - `initial_delay_seconds` `integer` **(必填)**：初始延迟 — 单位为秒
          - `period_seconds` `integer` **(必填)**：检查周期 — 单位为秒
          - `timeout_seconds` `integer` **(必填)**：超时时间 — 单位为秒
          - `failure_threshold` `integer` **(必填)**：失败阈值
        - `startup_probe` `object` **(必填)**：启动探针
          - `switch` `boolean` **(必填)**：开关
          - `probe_type` `string` **(必填)**：检查类型，枚举: `httpGet`/`tcpSocket`
          - `path` `string`：路径
          - `port` `integer` **(必填)**：服务端口
          - `initial_delay_seconds` `integer` **(必填)**：初始延迟 — 单位为秒
          - `period_seconds` `integer` **(必填)**：检查周期 — 单位为秒
          - `timeout_seconds` `integer` **(必填)**：超时时间 — 单位为秒
          - `failure_threshold` `integer` **(必填)**：失败阈值
        - `readiness_probe` `object` **(必填)**：就绪探针
          - `switch` `boolean` **(必填)**：开关
          - `probe_type` `string` **(必填)**：检查类型，枚举: `httpGet`/`tcpSocket`
          - `path` `string`：路径
          - `port` `integer` **(必填)**：服务端口
          - `initial_delay_seconds` `integer` **(必填)**：初始延迟 — 单位为秒
          - `period_seconds` `integer` **(必填)**：检查周期 — 单位为秒
          - `timeout_seconds` `integer` **(必填)**：超时时间 — 单位为秒
          - `failure_threshold` `integer` **(必填)**：失败阈值
      - `remote_ports` `array | null`：服务七层暴露(服务回传)端口列表
      - `storage_config` `array | null`：对象存储加速配置
      - `share_storage_config` `array | null`：共享存储配置
      - `nas_storage_config` `array | null`：NAS存储配置
      - `share_mem_config` `array | null`：共享内存配置 — 挂载共享内存卷，需在外层中声明对应的share_mem_volumes。
      - `share_disk_config` `array | null`：共享磁盘配置 — 挂载共享磁盘卷，需在外层中声明对应的share_disk_volumes。
      - `env` `array | null`：环境变量
      - `start_script` `object | null`：启动命令
        - `command` `array` **(必填)**：命令
          - **array<string>**
        - `args` `array` **(必填)**：参数
          - **array<string>**
      - `repository_account` `object | null`：私有仓库账号
        - `repository_username` `string` **(必填)**：私有仓库用户名
        - `repository_password` `string | null`：私有仓库密码
      - `is_update_repository` `string | null`：是否更新私有仓库账号
      - `registered_ports` `array | null`：服务四层暴露(SSH)端口列表 — 目前仅限云主机

响应名：成功

**响应示例（成功示例）**：

```json
{
  "code": "0000",
  "message": "success",
  "data": {
    "task_id": 1962285,
    "task_name": "job-202604210858",
    "sub_type": null,
    "schedule_status": null,
    "deployment_name": "job-11391-olueehus",
    "resources": [
      {
        "resource": {
          "device_name": "4090",
          "region": "chengde-p1",
          "gpu_name": "4090",
          "gpu_count": 1,
          "gpu_memory": 24560,
          "memory": 64512,
          "cpu_cores": 16
        },
        "region_name": "河北六区",
        "mark": "ha8GDGEAORN3a9Hhu7X+W/lveP9CW2eBkI+oB/QJLRcfvPTUMuUpxqfch7PdWik27Qx0BQX2cmaGoUHnIQ6pUPcLqpoLUCh5MaAR9kIet8llTG2oulHTzTRxAofshQoSFvtGpGD4Rh7V2V7xAj/0ysk+OmC4WeIxe+zHVBoYCehyTVGCyFygp1QeqGCp",
        "weight": null
      }
    ],
    "status": "Running",
    "points": 1,
    "runing_points": 1,
    "billing_points": 1,
    "billing_time": 0,
    "billing_value": 0,
    "forecast_value": 466,
    "services": [
      {
        "service_id": 1963001,
        "service_name": "container-01",
        "service_image": "harbor.suanleme.cn/trsnls6j/ubuntu:22.04",
        "remote_ports": [
          {
            "url": "https://job-11391-olueehus-80.550w.link",
            "service_port": 80
          }
        ],
        "health_checks": {
          "liveness_probe": {
            "switch": false,
            "probe_type": "httpGet",
            "path": "/live",
            "port": 80,
            "initial_delay_seconds": 0,
            "period_seconds": 10,
            "timeout_seconds": 1,
            "failure_threshold": 3
          },
          "startup_probe": {
            "switch": false,
            "probe_type": "httpGet",
            "path": "/health",
            "port": 80,
            "initial_delay_seconds": 0,
            "period_seconds": 10,
            "timeout_seconds": 1,
            "failure_threshold": 3
          },
          "readiness_probe": {
            "switch": false,
            "probe_type": "httpGet",
            "path": "/ready",
            "port": 80,
            "initial_delay_seconds": 0,
            "period_seconds": 10,
            "timeout_seconds": 1,
            "failure_threshold": 3
          }
        },
        "storage_config": [
          {
            "storage_id": 2038,
            "target_dir": "/root/s3"
          }
        ],
        "share_storage_config": [
          {
            "storage_id": 2037,
            "target_dir": "/root/share"
          }
        ],
        "share_mem_config": [
          {
            "target_dir": "/dev/shm",
            "volume_name": "mem-default"
          }
        ],
        "share_disk_config": [
          {
            "target_dir": "/dev/shd",
            "volume_name": "share-disk"
          }
        ],
        "env": [
          {
            "name": "key1",
            "value": "value1",
            "value_from": null
          }
        ],
        "start_script": {
          "command": [
            "sleep"
          ],
          "args": [
            "300"
          ]
        },
        "repository_account": null,
        "is_update_repository": null,
        "resource_weight": {
          "cpu_weight": 1,
          "mem_weight": 1,
          "gpu_weight": 1
        },
        "registered_ports": null
      }
    ],
    "task_tags": null,
    "share_disk_volumes": [
      {
        "name": "share-disk"
      }
    ],
    "share_mem_volumes": [
      {
        "name": "mem-default",
        "size_limit": 32768
      }
    ],
    "job_support": {
      "estimated_exec_sec": null,
      "timeout_sec": 1200,
      "parallelism": 1,
      "mod_param": {
        "default": {
          "backoff_limit": 3,
          "restart_policy": "OnFailure"
        },
        "index": null
      }
    },
    "job_status": {
      "create_time": "2026-04-21T01:01:23Z",
      "status": "Running",
      "completion_time": null,
      "active_pods": 1,
      "succeeded_pods": 0,
      "failed_pods": 0,
      "completion_mode": "NonIndexed"
    },
    "create_time": "2026-04-21T09:01:23.441992+08:00",
    "last_update_time": "2026-04-21T09:01:53.523971+08:00"
  }
}
```

---
*本文档由 fetch_apifox.py 从 Apifox 分享文档 6aa360d3-d8f2-471e-b841-3a35c33a7b7c 实时同步生成；同步时间见仓库根 .apifox-sync-manifest.json*
