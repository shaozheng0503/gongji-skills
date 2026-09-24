# 已购单机设备列表

> 来源：Apifox 官方文档（实时同步） · 分组：共绩算力 Open API/裸金属/已购列表
> 远端最后更新：2026-08-06T07:42:54.000Z
> 端点：`POST /api/output/v2/device-output/list_rent_device_single_v2`

| 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
| --- | --- | --- | --- |
| v1.0.0 | - | 否 | 是 |

### **描述**
获取已购买且订单没有结束的单机设备列表

## 请求体

Content-Type: `application/json`

## 响应（200）

- `code` `string` **(必填)**
- `message` `string` **(必填)**
- `data` `array` **(必填)**
  - **array<object>**
    - `billing_type` `string` **(必填)**：计费方式，枚举: `Hour`/`Day`/`Week`/`Month`
    - `intranet_ip` `string` **(必填)**：设备内网IP
    - `extranet_ip` `string` **(必填)**：设备公网IP
    - `cores` `integer` **(必填)**：设备核数
    - `cpu_model` `string` **(必填)**：设备CPU型号
    - `gpu_model` `string` **(必填)**：设备GPU型号
    - `gpu_count` `integer` **(必填)**：设备GPU数量
    - `gpu_memory` `integer` **(必填)**：设备GPU显存（单位MB）
    - `memory_size` `integer` **(必填)**：设备内存（单位MB）
    - `gpu_driver_version` `string` **(必填)**：设备GPU驱动版本
    - `cuda_version` `string` **(必填)**：设备cuda版本
    - `operating_system` `string` **(必填)**：设备操作系统
    - `system_disk_size` `integer` **(必填)**：设备硬盘空间（单位MB）
    - `system_disk_type` `string` **(必填)**：硬盘类型：NVMe,SSD,HDD,SCSI
    - `use_end_time` `string` **(必填)**：订单结束时间
    - `use_start_time` `string` **(必填)**：订单开始时间
    - `idc_name` `string` **(必填)**：设备机房名称
    - `order_id` `integer` **(必填)**：订单ID
    - `order_details_id` `integer` **(必填)**：订单详情ID
    - `zone_name` `string` **(必填)**：设备区域名称
    - `device_id` `integer` **(必填)**：设备ID
    - `order_detail_status` `string` **(必填)**：订单详情状态，枚举: `Default`/`Waiting`/`Serving`/`Finished`/`Canceled`/`CanceledRefunded`
    - `create_channel` `string` **(必填)**：订单创建渠道，枚举: `OutputPlatform`/`MiddlePlatform`

响应名：成功

**响应示例（成功示例）**：

```json
{
  "code": "0000",
  "message": "success",
  "data": [
    {
      "billing_type": "Hour",
      "intranet_ip": "172.31.0.68",
      "extranet_ip": "183.222.164.60",
      "cores": 80,
      "cpu_model": "Intel(R) Xeon(R) Gold 6133 CPU @ 2.50GHz",
      "gpu_model": "3090",
      "gpu_count": 4,
      "gpu_memory": 24576,
      "memory_size": 515641,
      "gpu_driver_version": "570.86.10",
      "cuda_version": "12.8",
      "operating_system": "ubuntu (5.15.0-161-generic)",
      "system_disk_size": 4273819,
      "system_disk_type": "NVMe",
      "use_end_time": "2026-08-04T14:58:36.787964+08:00",
      "use_start_time": "2026-08-04T13:58:36.787964+08:00",
      "idc_name": "cn-xinan-7test",
      "order_id": 1163,
      "order_details_id": 1212,
      "zone_name": "安徽区域",
      "device_id": 672,
      "order_detail_status": "Serving",
      "auto_renew_type": "Hour",
      "create_channel": "OutputPlatform"
    },
    {
      "billing_type": "Hour",
      "intranet_ip": "172.31.0.68",
      "extranet_ip": "183.222.164.60",
      "cores": 80,
      "cpu_model": "Intel(R) Xeon(R) Gold 6133 CPU @ 2.50GHz",
      "gpu_model": "3090",
      "gpu_count": 4,
      "gpu_memory": 24576,
      "memory_size": 515641,
      "gpu_driver_version": "570.86.10",
      "cuda_version": "12.8",
      "operating_system": "ubuntu (5.15.0-161-generic)",
      "system_disk_size": 4273819,
      "system_disk_type": "NVMe",
      "use_end_time": "2026-08-04T13:58:36.787964+08:00",
      "use_start_time": "2026-08-04T11:58:36.787964+08:00",
      "idc_name": "cn-xinan-7test",
      "order_id": 1162,
      "order_details_id": 1211,
      "zone_name": "安徽区域",
      "device_id": 672,
      "order_detail_status": "Finished",
      "auto_renew_type": "Hour",
      "create_channel": "OutputPlatform"
    }
  ]
}
```

---
*本文档由 fetch_apifox.py 从 Apifox 分享文档 6aa360d3-d8f2-471e-b841-3a35c33a7b7c 实时同步生成；同步时间见仓库根 .apifox-sync-manifest.json*
