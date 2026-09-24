# 单机设备可购列表

> 来源：Apifox 官方文档（实时同步） · 分组：共绩算力 Open API/裸金属/可购列表
> 远端最后更新：2026-08-06T07:38:17.000Z
> 端点：`POST /api/output/v2/device-output/page_list_product_single_v2`

| 当前版本 | 旧版本 | 是否需要加密 | 是否需要加签 |
| --- | --- | --- | --- |
| v1.0.0 | - | 否 | 是 |

### **描述**
获取单机裸金属可购买列表及裸金属基础信息。

## 请求体

Content-Type: `application/json`

- `page` `integer` **(必填)**：页码
- `page_size` `integer` **(必填)**：每页数量
- `conditional` `object` **(必填)**
  - `billing_type` `string` **(必填)**：计费方式，枚举: `Hour`/`Day`/`Week`/`Month`
  - `gpu_models` `array` **(必填)**：卡型集合 — 为空代表全部
    - **array<string>**
  - `zone_id` `integer`：区域ID
  - `gpu_count` `integer`：单机 GPU 数量

**请求示例（示例 1）**：

```json
{
  "page": 1,
  "page_size": 10,
  "conditional": {
    "billing_type": "Day",
    "gpu_models": [
      "4090",
      "5090"
    ],
    "zone_id": 1,
    "gpu_count": 2
  }
}
```

## 响应（200）

- `code` `string` **(必填)**
- `message` `string` **(必填)**
- `data` `object` **(必填)**
  - `count` `integer` **(必填)**
  - `results` `array` **(必填)**
    - **array<object>**
      - `network_type` `string` **(必填)**：网络类型
      - `network_id` `integer` **(必填)**：网络ID
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
      - `idc_name` `string` **(必填)**：设备机房名称
      - `idc_id` `integer` **(必填)**：设备机房ID
      - `zone_name` `string` **(必填)**：设备区域名称
      - `end_time` `string` **(必填)**：设备结束时间
      - `start_time` `string` **(必填)**：设备开始时间
      - `device_id` `integer` **(必填)**：设备ID
      - `hour_price` `integer` **(必填)**：小时时长包价格 — 1000000=1元
      - `day_price` `integer` **(必填)**：24小时时长包价格 — 1000000=1元
      - `week_price` `integer` **(必填)**：7天时长包价格 — 1000000=1元
      - `month_price` `integer` **(必填)**：30天时长包价格 — 1000000=1元
      - `listing_mode` `string` **(必填)**：设备上架模式：Single-单机模式，Proxy-网关代理模式，Direct-网关直连模式
      - `gateway_type` `string` **(必填)**：设备网关类型
      - `hour_price_discount` `null` **(必填)**：租户折扣 - 小时时长包价格 — 1000000=1元
      - `day_price_discount` `null` **(必填)**：租户折扣 - 24小时时长包价格 — 1000000=1元
      - `week_price_discount` `null` **(必填)**：租户折扣 - 7天时长包价格 — 1000000=1元
      - `month_price_discount` `null` **(必填)**：租户折扣 - 30天时长包价格 — 1000000=1元
      - `migration_mode` `null` **(必填)**：设备迁移类型：Flexible-灵活迁移，Fast-快速迁移
      - `cooperation_mode` `string` **(必填)**：设备合作模式：IdleElastic-闲时弹性，IdleFullRent-闲时整租
      - `allow_switch_to_elastic_full_rent` `boolean` **(必填)**：设备允许切换至弹性整租
      - `max_buy_count` `integer` **(必填)**：最多购买数

响应名：成功

**响应示例（成功示例）**：

```json
{
  "count": 13,
  "results": [
    {
      "network_type": null,
      "network_id": null,
      "cores": 128,
      "cpu_model": "INTEL(R) XEON(R) GOLD 6530",
      "gpu_model": "5090",
      "gpu_count": 8,
      "gpu_memory": 32607,
      "memory_size": 515610,
      "gpu_driver_version": "580.105.08",
      "cuda_version": "13.0",
      "operating_system": "ubuntu (5.15.0-179-generic)",
      "system_disk_size": 15566270,
      "system_disk_type": "NVMe",
      "idc_name": "测试一区机房",
      "idc_id": 1,
      "zone_name": "测试一区",
      "end_time": "2031-07-31T00:00:00+08:00",
      "start_time": "2026-07-17T00:00:00+08:00",
      "device_id": 1,
      "hour_price": 28000000,
      "day_price": 638000000,
      "week_price": 4245000000,
      "month_price": 17285000000,
      "listing_mode": "Direct",
      "gateway_type": "Direct",
      "hour_price_discount": null,
      "day_price_discount": null,
      "week_price_discount": null,
      "month_price_discount": null,
      "migration_mode": null,
      "cooperation_mode": "IdleFullRent",
      "allow_switch_to_elastic_full_rent": false,
      "max_buy_count": 43717
    },
    {
      "network_type": null,
      "network_id": null,
      "cores": 128,
      "cpu_model": "INTEL(R) XEON(R) GOLD 6530",
      "gpu_model": "5090",
      "gpu_count": 8,
      "gpu_memory": 32607,
      "memory_size": 515610,
      "gpu_driver_version": "580.82.07",
      "cuda_version": "13.0",
      "operating_system": "ubuntu (5.15.0-181-generic)",
      "system_disk_size": 15566999,
      "system_disk_type": "NVMe",
      "idc_name": "测试一区机房",
      "idc_id": 1,
      "zone_name": "测试一区",
      "end_time": "2028-07-31T00:00:00+08:00",
      "start_time": "2026-07-17T00:00:00+08:00",
      "device_id": 1,
      "hour_price": 28000000,
      "day_price": 638000000,
      "week_price": 4245000000,
      "month_price": 17285000000,
      "listing_mode": "Direct",
      "gateway_type": "Direct",
      "hour_price_discount": null,
      "day_price_discount": null,
      "week_price_discount": null,
      "month_price_discount": null,
      "migration_mode": null,
      "cooperation_mode": "IdleFullRent",
      "allow_switch_to_elastic_full_rent": false,
      "max_buy_count": 17437
    },
    {
      "network_type": null,
      "network_id": null,
      "cores": 128,
      "cpu_model": "INTEL(R) XEON(R) GOLD 6530",
      "gpu_model": "5090",
      "gpu_count": 8,
      "gpu_memory": 32607,
      "memory_size": 515610,
      "gpu_driver_version": "580.142",
      "cuda_version": "13.0",
      "operating_system": "ubuntu (5.15.0-94-generic)",
      "system_disk_size": 15566065,
      "system_disk_type": "NVMe",
      "idc_name": "测试一区机房",
      "idc_id": 1,
      "zone_name": "测试一区",
      "end_time": "2028-07-31T00:00:00+08:00",
      "start_time": "2026-07-17T00:00:00+08:00",
      "device_id": 1,
      "hour_price": 28000000,
      "day_price": 638000000,
      "week_price": 4245000000,
      "month_price": 17285000000,
      "listing_mode": "Direct",
      "gateway_type": "Direct",
      "hour_price_discount": null,
      "day_price_discount": null,
      "week_price_discount": null,
      "month_price_discount": null,
      "migration_mode": null,
      "cooperation_mode": "IdleFullRent",
      "allow_switch_to_elastic_full_rent": false,
      "max_buy_count": 17437
    },
    {
      "network_type": null,
      "network_id": null,
      "cores": 128,
      "cpu_model": "INTEL(R) XEON(R) GOLD 6530",
      "gpu_model": "5090",
      "gpu_count": 8,
      "gpu_memory": 32607,
      "memory_size": 515611,
      "gpu_driver_version": "580.82.07",
      "cuda_version": "13.0",
      "operating_system": "ubuntu (5.15.0-94-generic)",
      "system_disk_size": 15566931,
      "system_disk_type": "NVMe",
      "idc_name": "测试一区机房",
      "idc_id": 1,
      "zone_name": "测试一区",
      "end_time": "2028-07-31T00:00:00+08:00",
      "start_time": "2026-07-17T00:00:00+08:00",
      "device_id": 1,
      "hour_price": 28000000,
      "day_price": 638000000,
      "week_price": 4245000000,
      "month_price": 17285000000,
      "listing_mode": "Direct",
      "gateway_type": "Direct",
      "hour_price_discount": null,
      "day_price_discount": null,
      "week_price_discount": null,
      "month_price_discount": null,
      "migration_mode": null,
      "cooperation_mode": "IdleFullRent",
      "allow_switch_to_elastic_full_rent": false,
      "max_buy_count": 17437
    },
    {
      "network_type": null,
      "network_id": null,
      "cores": 128,
      "cpu_model": "INTEL(R) XEON(R) GOLD 6530",
      "gpu_model": "5090",
      "gpu_count": 8,
      "gpu_memory": 32607,
      "memory_size": 515610,
      "gpu_driver_version": "580.82.07",
      "cuda_version": "13.0",
      "operating_system": "ubuntu (5.15.0-181-generic)",
      "system_disk_size": 15566897,
      "system_disk_type": "NVMe",
      "idc_name": "测试一区机房",
      "idc_id": 1,
      "zone_name": "测试一区",
      "end_time": "2028-07-31T00:00:00+08:00",
      "start_time": "2026-07-17T00:00:00+08:00",
      "device_id": 1,
      "hour_price": 28000000,
      "day_price": 638000000,
      "week_price": 4245000000,
      "month_price": 17285000000,
      "listing_mode": "Direct",
      "gateway_type": "Direct",
      "hour_price_discount": null,
      "day_price_discount": null,
      "week_price_discount": null,
      "month_price_discount": null,
      "migration_mode": null,
      "cooperation_mode": "IdleFullRent",
      "allow_switch_to_elastic_full_rent": false,
      "max_buy_count": 17437
    },
    {
      "network_type": null,
      "network_id": null,
      "cores": 128,
      "cpu_model": "INTEL(R) XEON(R) GOLD 6530",
      "gpu_model": "5090",
      "gpu_count": 8,
      "gpu_memory": 32607,
      "memory_size": 515610,
      "gpu_driver_version": "580.82.07",
      "cuda_version": "13.0",
      "operating_system": "ubuntu (5.15.0-181-generic)",
      "system_disk_size": 15566897,
      "system_disk_type": "NVMe",
      "idc_name": "测试一区机房",
      "idc_id": 1,
      "zone_name": "测试一区",
      "end_time": "2028-07-31T00:00:00+08:00",
      "start_time": "2026-07-17T00:00:00+08:00",
      "device_id": 1,
      "hour_price": 28000000,
      "day_price": 638000000,
      "week_price": 4245000000,
      "month_price": 17285000000,
      "listing_mode": "Direct",
      "gateway_type": "Direct",
      "hour_price_discount": null,
      "day_price_discount": null,
      "week_price_discount": null,
      "month_price_discount": null,
      "migration_mode": null,
      "cooperation_mode": "IdleFullRent",
      "allow_switch_to_elastic_full_rent": false,
      "max_buy_count": 17437
    },
    {
      "network_type": null,
      "network_id": null,
      "cores": 128,
      "cpu_model": "INTEL(R) XEON(R) GOLD 6530",
      "gpu_model": "5090",
      "gpu_count": 8,
      "gpu_memory": 32607,
      "memory_size": 515610,
      "gpu_driver_version": "580.82.07",
      "cuda_version": "13.0",
      "operating_system": "ubuntu (5.15.0-181-generic)",
      "system_disk_size": 15566950,
      "system_disk_type": "NVMe",
      "idc_name": "测试一区机房",
      "idc_id": 1,
      "zone_name": "测试一区",
      "end_time": "2028-07-31T00:00:00+08:00",
      "start_time": "2026-07-17T00:00:00+08:00",
      "device_id": 1,
      "hour_price": 28000000,
      "day_price": 638000000,
      "week_price": 4245000000,
      "month_price": 17285000000,
      "listing_mode": "Direct",
      "gateway_type": "Direct",
      "hour_price_discount": null,
      "day_price_discount": null,
      "week_price_discount": null,
      "month_price_discount": null,
      "migration_mode": null,
      "cooperation_mode": "IdleFullRent",
      "allow_switch_to_elastic_full_rent": false,
      "max_buy_count": 17437
    },
    {
      "network_type": null,
      "network_id": null,
      "cores": 128,
      "cpu_model": "INTEL(R) XEON(R) GOLD 6530",
      "gpu_model": "5090",
      "gpu_count": 8,
      "gpu_memory": 32607,
      "memory_size": 515610,
      "gpu_driver_version": "580.82.07",
      "cuda_version": "13.0",
      "operating_system": "ubuntu (5.15.0-181-generic)",
      "system_disk_size": 15566950,
      "system_disk_type": "NVMe",
      "idc_name": "测试一区机房",
      "idc_id": 1,
      "zone_name": "测试一区",
      "end_time": "2028-07-31T00:00:00+08:00",
      "start_time": "2026-07-17T00:00:00+08:00",
      "device_id": 1,
      "hour_price": 28000000,
      "day_price": 638000000,
      "week_price": 4245000000,
      "month_price": 17285000000,
      "listing_mode": "Direct",
      "gateway_type": "Direct",
      "hour_price_discount": null,
      "day_price_discount": null,
      "week_price_discount": null,
      "month_price_discount": null,
      "migration_mode": null,
      "cooperation_mode": "IdleFullRent",
      "allow_switch_to_elastic_full_rent": false,
      "max_buy_count": 17437
    },
    {
      "network_type": null,
      "network_id": null,
      "cores": 128,
      "cpu_model": "INTEL(R) XEON(R) GOLD 6530",
      "gpu_model": "5090",
      "gpu_count": 8,
      "gpu_memory": 32607,
      "memory_size": 515610,
      "gpu_driver_version": "580.82.07",
      "cuda_version": "13.0",
      "operating_system": "ubuntu (5.15.0-181-generic)",
      "system_disk_size": 15566897,
      "system_disk_type": "NVMe",
      "idc_name": "测试一区机房",
      "idc_id": 1,
      "zone_name": "测试一区",
      "end_time": "2028-07-31T00:00:00+08:00",
      "start_time": "2026-07-17T00:00:00+08:00",
      "device_id": 1,
      "hour_price": 28000000,
      "day_price": 638000000,
      "week_price": 4245000000,
      "month_price": 17285000000,
      "listing_mode": "Direct",
      "gateway_type": "Direct",
      "hour_price_discount": null,
      "day_price_discount": null,
      "week_price_discount": null,
      "month_price_discount": null,
      "migration_mode": null,
      "cooperation_mode": "IdleFullRent",
      "allow_switch_to_elastic_full_rent": false,
      "max_buy_count": 17437
    },
    {
      "network_type": null,
      "network_id": null,
      "cores": 128,
      "cpu_model": "INTEL(R) XEON(R) GOLD 6530",
      "gpu_model": "5090",
      "gpu_count": 8,
      "gpu_memory": 32607,
      "memory_size": 515610,
      "gpu_driver_version": "580.105.08",
      "cuda_version": "13.0",
      "operating_system": "ubuntu (5.15.0-181-generic)",
      "system_disk_size": 15566382,
      "system_disk_type": "NVMe",
      "idc_name": "测试一区机房",
      "idc_id": 1,
      "zone_name": "测试一区",
      "end_time": "2027-06-07T00:00:00+08:00",
      "start_time": "2026-07-22T00:00:00+08:00",
      "device_id": 1,
      "hour_price": 28000000,
      "day_price": 638000000,
      "week_price": 4245000000,
      "month_price": 17285000000,
      "listing_mode": "Direct",
      "gateway_type": "Direct",
      "hour_price_discount": null,
      "day_price_discount": null,
      "week_price_discount": null,
      "month_price_discount": null,
      "migration_mode": null,
      "cooperation_mode": "IdleFullRent",
      "allow_switch_to_elastic_full_rent": false,
      "max_buy_count": 7357
    }
  ]
}
```

---
*本文档由 fetch_apifox.py 从 Apifox 分享文档 6aa360d3-d8f2-471e-b841-3a35c33a7b7c 实时同步生成；同步时间见仓库根 .apifox-sync-manifest.json*
