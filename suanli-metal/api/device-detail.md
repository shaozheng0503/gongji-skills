# 设备详情【开机信息】

> 来源：Apifox 官方文档（实时同步） · 分组：共绩算力 Open API/裸金属/已购列表
> 远端最后更新：2026-08-06T07:44:43.000Z
> 端点：`POST /api/output/v2/device_order/get_device_details_v2`

| 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
| --- | --- | --- | --- |
| v1.0.0 | - | 否 | 是 |

### **描述**
获取单个设备的设备详细信息
注意：设备已处在服务中，才会有内网IP\服务暴露端口\SSH开放端口

## 请求体

Content-Type: `application/json`

- `device_id` `integer` **(必填)**：设备ID

**请求示例（示例 1）**：

```json
{
  "device_id": 672
}
```

## 响应（200）

- `code` `string` **(必填)**
- `message` `string` **(必填)**
- `data` `object` **(必填)**
  - `order_details_id` `integer` **(必填)**：订单详情ID
  - `start_time` `null` **(必填)**：服务开始时间
  - `end_time` `null` **(必填)**：服务结束时间
  - `pub_ip` `string` **(必填)**：设备公网IP
  - `inner_ip` `string` **(必填)**：设备内网IP
  - `ssh_port` `null` **(必填)**：设备ssh端口
  - `device_username` `null` **(必填)**：设备登录账号
  - `device_passwd` `null` **(必填)**：设备登录密码
  - `billing_type` `string` **(必填)**：计费方式
  - `network_type` `string` **(必填)**：网络类型
  - `network_name` `string` **(必填)**：网络名称
  - `operating_system` `string` **(必填)**：设备操作系统
  - `cpu_model` `string` **(必填)**：设备CPU型号
  - `memory_size` `integer` **(必填)**：设备内存（单位MB）
  - `gpu_count` `integer` **(必填)**：设备GPU数量
  - `gpu_model` `string` **(必填)**：设备GPU型号
  - `gpu_driver_version` `string` **(必填)**：设备GPU驱动版本
  - `cuda_version` `string` **(必填)**：设备cuda版本
  - `system_disk_size` `integer` **(必填)**：设备硬盘空间（单位MB）
  - `estimated_time` `string` **(必填)**：预计开机时间 — 目前无实际参考意义
  - `expose_ports` `array` **(必填)**：服务暴露端口
    - **array<object>**
      - `local_port` `integer`
      - `mapping_port` `integer`

响应名：成功

**响应示例（成功示例）**：

```json
{
  "code": "0000",
  "message": "success",
  "data": {
    "order_details_id": 1,
    "start_time": null,
    "end_time": null,
    "pub_ip": "183.1.1.1",
    "inner_ip": "172.1.1.1",
    "ssh_port": null,
    "device_username": null,
    "device_passwd": null,
    "billing_type": "Hour",
    "network_type": "NVLinkSwitch",
    "network_name": "NS-test",
    "operating_system": "ubuntu (5.15.0-161-generic)",
    "cpu_model": "Intel(R) Xeon(R) Gold 6133 CPU @ 2.50GHz",
    "memory_size": 515641,
    "gpu_count": 4,
    "gpu_model": "3090",
    "gpu_driver_version": "570.86.10",
    "cuda_version": "12.8",
    "system_disk_size": 4273819,
    "estimated_time": "2026-08-05T09:40:49.818142+08:00",
    "expose_ports": [
      {
        "local_port": 5001,
        "mapping_port": 50050
      }
    ]
  }
}
```

---
*本文档由 fetch_apifox.py 从 Apifox 分享文档 6aa360d3-d8f2-471e-b841-3a35c33a7b7c 实时同步生成；同步时间见仓库根 .apifox-sync-manifest.json*
