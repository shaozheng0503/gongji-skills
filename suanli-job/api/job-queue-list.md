# Job任务队列任务组列表查询接口

> 来源：Apifox 官方文档（实时同步） · 分组：共绩算力 Open API/Job批处理任务队列
> 远端最后更新：2026-07-03T04:04:55.000Z
> 端点：`GET /api/job/queue/group/search`

| 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
| --- | --- | --- | --- |
| v1.0.0 | - | 否 | 是 |

### **描述**
获取指定Job任务队列下的任务组列表。
加签详见：[加签流程](https://suanli.cn/docs/platform/openapi/m3p6whioxidzwaksughc4gfhnro/#45-%E5%8A%A0%E7%AD%BE%E6%B5%81%E7%A8%8B)

## query 参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `queue_id` | integer | 是 | 队列id |
| `status` | string | 否 | 组状态。如果有多个值，请使用英文逗号（,）分隔（示例：Running,Waiting） |
| `search_value` | string | 否 | 组名称(URL编码) |
| `page` | integer | 否 | 页码（示例：1） |
| `page_size` | integer | 否 | 每页数量，备注：page_size范围1~50（示例：默认:10） |

## header 参数

| 参数 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `token` | string | 是 | 请填入您在平台内创建的 API 密钥，获取路径为：右上角头像 → API 密钥。 |
| `timestamp` | integer | 是 | 时间戳（示例：{{$date.millisecondsTimestamp}}） |
| `version` | string | 是 | 固定值（示例：1.0.0） |
| `sign_str` | string | 否 | 如果token为简易模式则无需填写此字段 |

## 响应（200）

- `code` `string` **(必填)**：响应码 — 当code≠0000时，data必为null。，枚举: `0000`/`C999`/`C001`/`C002`/`C004`/`C005`/`C006`/`C007`/`C008`/`C009`/`C010`/`Z001`
- `message` `string | null` **(必填)**：响应信息
- `data` `object | null` **(必填)**
  - `count` `integer` **(必填)**
  - `results` `object` **(必填)**
    - `queue_id` `integer` **(必填)**：队列id
    - `queue_name` `string` **(必填)**：队列名称
    - `group_id` `integer` **(必填)**：组id
    - `group_name` `string` **(必填)**：组名称
    - `group_count` `integer` **(必填)**：组内任务总数 — 该任务组将包含的子任务总数，定义该任务组内一共需要执行多少个子任务
    - `task_parallel_limit` `integer` **(必填)**：组内并发任务上限 — 允许同时运行的最大子任务数目，控制该任务组在执行阶段的任务并发上限
    - `status` `string` **(必填)**：组状态，枚举: `Running`/`Waiting`/`End`
    - `billing_value` `integer` **(必填)**：累计费用(积分)
    - `task_status_capacity` `object` **(必填)**：任务状态队列
      - `Pending` `integer`：等待中任务数量
      - `Running` `integer`：运行中任务数量
      - `Paused` `integer`：已暂停任务数量
      - `End` `integer`：已停止任务数量
    - `create_time` `string` **(必填)**：创建时间
    - `task_dto` `object` **(必填)**：job任务资源
      - `task_name` `string` **(必填)**：任务名
      - `sub_type` `string | null`：子类型 — 传null或不传表示OnDemand任务，传Spot表示Spot任务。，枚举: `Spot`
      - `resources` `array` **(必填)**：资源列表
        - **array<object>**
          - `resource` `any`：资源信息
          - `region_name` `string`：区域名称
          - `mark` `string` **(必填)**：资源唯一标识
          - `weight` `integer | null`
      - `share_disk_volumes` `array | null`：共享磁盘卷 — 声明共享磁盘卷，需在services中配置对应的share_disk_config进行卷挂载。
      - `share_mem_volumes` `array | null`：共享内存卷 — 声明共享内存卷，需在services中配置对应的share_mem_config进行卷挂载。
      - `task_qos` `object | null`：CPU独占
        - `class` `string` **(必填)**，枚举: `Guaranteed`
      - `points` `integer` **(必填)**：完成节点数量 — 任务需要成功完成的总次数。对应K8s参数：spec.completions
      - `task_tags` `array | null`：任务标识 — 目前仅限标识是否为自带SSH的公有镜像
      - `job_support` `object` **(必填)**：Job支持
        - `estimated_exec_sec` `integer | null`：单元运行时间(秒) — 任务运行完成的预估时间，系统将基于此时间寻找最稳定的资源窗口。该字段仅在 Job 批处理任务的 sub_type 为 Spot 时生效且必填；其他 sub_type 类型下不生效。该值应比任务真正运行完成时间略长，比任务超时时间略短。
        - `timeout_sec` `integer` **(必填)**：任务超时时间(秒) — 任务从开始运行到结束的最长物理时间，超时系统将强制终止任务。
        - `parallelism` `integer` **(必填)**：并行节点数
        - `mod_param` `any` **(必填)**：完成模式参数 — 对于多节点并行任务，建议使用索引模式
      - `termination_grace_period_seconds` `integer | null`：优雅退出时间
      - `services` `array` **(必填)**：服务列表
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
      - `init_services` `array | null`

响应名：成功

---
*本文档由 fetch_apifox.py 从 Apifox 分享文档 6aa360d3-d8f2-471e-b841-3a35c33a7b7c 实时同步生成；同步时间见仓库根 .apifox-sync-manifest.json*
