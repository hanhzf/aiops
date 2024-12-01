# API接口设计文档

# API接口设计文档

## 基础信息
- 基础 URL: `/api/v1`
- 认证方式: 所有接口需要在Header中携带认证信息
```
X-Auth-Token: [认证令牌]
```

## 通用响应格式
```json
{
    "data": {}, // 成功时包含实际数据,失败时为null
    "message": "" // 成功时为空,失败时包含错误信息
}
```

## HTTP状态码说明
- 200 OK: 请求成功
- 400 Bad Request: 客户端请求错误
- 401 Unauthorized: 认证失败
- 500 Internal Server Error: 服务器内部错误

## API接口列表

### 1. 文件处理接口

#### 1.1 上传文件
- URL: `/files/upload`
- 方法: POST
- 描述: 上传语音或图片文件
- 请求体:
    ```
    Content-Type: multipart/form-data
    file: [文件内容]
    type: [file_type] // audio或image
    ```
- 响应:
    ```json
    {
        "data": {
            "file_id": "550e8400-e29b-41d4-a716-446655440000",
            "name": "example.mp3",
            "size": 1024,
            "type": "audio",
            "extracted_content": "转写的文本内容",
            "created_at": "2024-01-01T12:00:00Z"
        },
        "message": ""
    }
    ```

### 2. 对话管理接口

#### 2.1 创建对话
- URL: `/chats`
- 方法: POST
- 描述: 创建新的对话会话
- 请求体:
    ```json
    {
        "scene": "order" // order或report
    }
    ```
- 响应:
    ```json
    {
        "data": {
            "chat_id": "550e8400-e29b-41d4-a716-446655440000",
            "created_at": "2024-01-01T12:00:00Z"
        },
        "message": ""
    }
    ```

#### 2.2 获取对话历史清单
- URL: `/chats`
- 方法: GET
- 描述: 获取对话清单
- 查询参数:
  - page: 页码,默认1
  - size: 每页数量,默认20
- 响应:
    ```json
    {
        "data": {
            "total": 100,
            "items": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "name": "获取今日的订单金额汇总",
                    "scene": "report",
                    "created_at": "2024-01-01T12:00:00Z"
                }
            ]
        },
        "message": ""
    }
    ```

#### 2.3 获取对话详情
- URL: `/chats/{chat_id}`
- 方法: GET
- 描述: 获取指定对话的详情（包含历史消息）
- 响应:
    ```json
    {
        "data": {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "name": "获取今日的订单金额汇总",
            "scene": "report",
            "created_at": "2024-01-01T12:00:00Z"
        },
        "message": ""
    }
    ```

#### 2.4 获取对话历史消息
- URL: `/chats/{chat_id}/messages`
- 方法: GET
- 描述: 获取指定对话的历史消息
- 查询参数:
  - page: 页码,默认1
  - size: 每页数量,默认20
  - index: 获取某个index后的消息
- 响应:
    ```json
    {
        "data": {
            "total": 100,
            "items": [
                {
                    "message_id": "550e8400-e29b-41d4-a716-446655440000",
                    "chat_id": "550e8400-e29b-41d4-a716-446655440000",
                    "index": 1,
                    "sender": "user",
                    "content": [
                        {
                        "type": "text",
                        "text": "消息内容"
                        }
                    ],
                    "attachments": ["550e8400-e29b-41d4-a716-446655440000"],
                    "created_at": "2024-01-01T12:00:00Z"
                }
            ]
        },
        "message": ""
    }
    ```

#### 2.5 发送消息
- URL: `/chats/{chat_id}/completion`
- 方法: POST
- 描述: 在指定对话中发送消息
- 请求体:
    ```json
    {
        "prompt": "请描述你的需求", // 可选，但 prompt 和 attachments 不可全为空
        "parent_message_id": "661a9432-e29b-41d4-a716-123456229921",
        "stream": "true", // 是否启用流式响应设计 
        "attachments": ["550e8400-e29b-41d4-a716-446655440000"] // 可选,关联的文件ID
    }
    ```
- 响应 stream=false:
    ```json
    {
        "data": {
            "message_id": "550e8400-e29b-41d4-a716-446655440000",
            "chat_id": "550e8400-e29b-41d4-a716-446655440000",
            "index": 1,
            "sender": "user",
            "content": [
                {
                "type": "text",
                "text": "消息内容"
                }
            ],
            "attachments": ["550e8400-e29b-41d4-a716-446655440000"],
            "created_at": "2024-01-01T12:00:00Z"
        },
        "message": ""
    }
    ```

- 响应 stream=true 流式返回:
    * API 会按照流式的格式对结果进行返回，也即后台会按照如下格式返回多个message，直到done。
    * 客户端需要根据 event 的类型来判断该消息返回是否结束。
    * 当 event 是 message_delta 时，表示消息的发送结束。
    * 当 event 是 message_done 时，说明正在发送过程中。

    ```json
    {
        "event": "message_delta", 
        "data": {
            "index": 1, // message的索引号
            "type": "text", // 文字
            "content": "好的，这就为您设计"
        }
    }

    {
        "event": "message_delta", 
        "data": {
            "index": 1,
            "type": "pwchart", // chart
            "content": "<pwchart></pwchart>"
        }
    }

    {
        "event": "message_done",
        "data": {
            "index": 1
        }
    }
    ```

#### 2.3 获取最新的消息
- URL: `/chats/{chat_id}/messages/latest`
- 方法: GET
- 描述: 获取最新的消息。当completion接口没有及时返回消息时，前端可通过此接口获取最新的返回。

- 响应:
    ```json
    {
        "data": {
            "message_id": "550e8400-e29b-41d4-a716-446655440000",
            "chat_id": "550e8400-e29b-41d4-a716-446655440000",
            "index": 1,
            "sender": "user",
            "content": [
                {
                "type": "text",
                "text": "消息内容"
                }
            ],
            "attachments": ["550e8400-e29b-41d4-a716-446655440000"],
            "created_at": "2024-01-01T12:00:00Z"
        },
        "message": ""
    }
    ```

### 3. 订单处理接口

#### 3.1 创建订单
- URL: `/orders`
- 方法: POST
- 描述: 创建新订单
- 请求体:
    ```json
    {
        "transportInfo": {
            "salesName": "李四",                   // 销售专员姓名
            "createdTime": "2024-10-22",          // 订单创建时间
            "cargoType": "普货",                   // 货物类型：普货/危险品/温控等
            "transportType": "汽运",               // 运输方式：汽运/铁路/空运等
            "deliveryType": "送货上门",            // 交付方式：送货上门/自提等
            "paymentType": "月付",                 // 付款方式：月付/现付/提付等
            "deliveryRoute": "",                  // 运输路线编号
            "deliveryPlan": "",                   // 配送计划编号
            "vehicleNumber": "",                  // 承运车辆编号
            "remarks": "轻拿轻放"                  // 运输特殊说明和备注
        },
        // 货物信息：描述货物的具体规格、数量等属性
        "cargoInfo": {
            "quantity": 15,                       // 货物数量
            "unit": "托",                         // 计量单位：托/箱/件等
            "weight": 23.00,                      // 货物重量，单位：吨
            "volume": 3.20,                       // 货物体积，单位：立方米
            "unitType": "重量",                   // 计费单位类型：重量/体积
            "value": 125000                         // 货物声明价值，单位：元
        },

        // 提货信息：包含提货地点、联系人等提货相关信息
        "pickupInfo": {
            "customerName": "XX制造公司",          // 提货方公司名称
            "customerId": "cm-123",              // 提货方客户编号
            "area": "江苏省苏州市",               // 提货区域
            "address": "工业园区科技路88号",       // 提货详细地址
            "addressInfo": {
                "province": "江苏省",             // 省份
                "city": "苏州市",                 // 城市
                "district": "工业园区",           // 区县
                "town": "湖东",                   // 街道/镇
                "industrialPark": "科技园",       // 工业园区
                "street": "科技路",               // 街道名
                "number": "88号",                 // 门牌号
                "building": "A座",                // 楼栋号
                "company": "XX制造公司"           // 公司名称
            },
            "contactPerson": "王五",              // 提货联系人姓名
            "contactPhone": "13900139000",       // 提货联系人电话
            "pickupDate": "2024-10-23",          // 预约提货日期
            "pickupTime": "14:30"                // 预约提货时间
        },    
        // 送货信息：包含收货地点、联系人等送货相关信息
        "deliveryInfo": {
            "customerName": "XX物流公司",          // 收货方公司名称
            "customerId": "cm-123",              // 收货方客户编号
            "area": "浙江省杭州市",               // 送货区域
            "address": "滨江区长河路100号",        // 送货详细地址
            "addressInfo": {
                "province": "浙江省",             // 省份
                "city": "杭州市",                 // 城市
                "district": "滨江区",             // 区县
                "town": "长河街道",               // 街道/镇
                "industrialPark": "科技园",       // 工业园区
                "street": "长河路",               // 街道名
                "number": "100号",                // 门牌号
                "building": "B座",                // 楼栋号
                "company": "XX物流公司"           // 公司名称
            },
            "contactPerson": "赵六",              // 收货联系人姓名
            "contactPhone": "13800138000",       // 收货联系人电话
            "deliveryDate": "2024-10-24",        // 预约送达日期
            "deliveryTime": "16:00"              // 预约送达时间
        }
    }
    ```

- 响应:
    ```json
    {
        "data": {
            "order_id": "550e8400-e29b-41d4-a716-446655440000",
            "created_at": "2024-01-01T12:00:00Z"
        },
        "message": ""
    }
    ```

#### 3.2 获取订单列表
- URL: `/orders`
- 方法: GET
- 描述: 获取订单列表
- 查询参数:
  - page: 页码,默认1
  - size: 每页数量,默认20
- 响应:

    ```json
    {
        "data": {
            "total": 100,
            "items": [{
                "order_id": "550e8400-e29b-41d4-a716-446655440000",
                "from_customer": "发货客户",
                "from_address": "发货地址", 
                "to_customer": "收货客户",
                "to_address": "收货地址",
                "created_at": "2024-01-01T12:00:00Z"
            }]
        },
        "message": ""
    }
    ```


#### 3.3 订单详情
- URL: `/orders/{id}`
- 方法: GET
- 描述: 获取订单详情
- 请求体:

    ```json
    {
        "transportInfo": {
            "salesName": "李四",                   // 销售专员姓名
            "createdTime": "2024-10-22",          // 订单创建时间
            "cargoType": "普货",                   // 货物类型：普货/危险品/温控等
            "transportType": "汽运",               // 运输方式：汽运/铁路/空运等
            "deliveryType": "送货上门",            // 交付方式：送货上门/自提等
            "paymentType": "月付",                 // 付款方式：月付/现付/提付等
            "deliveryRoute": "",                  // 运输路线编号
            "deliveryPlan": "",                   // 配送计划编号
            "vehicleNumber": "",                  // 承运车辆编号
            "remarks": "轻拿轻放"                  // 运输特殊说明和备注
        },
        // 货物信息：描述货物的具体规格、数量等属性
        "cargoInfo": {
            "quantity": 15,                       // 货物数量
            "unit": "托",                         // 计量单位：托/箱/件等
            "weight": 23.00,                      // 货物重量，单位：吨
            "volume": 3.20,                       // 货物体积，单位：立方米
            "unitType": "重量",                   // 计费单位类型：重量/体积
            "value": 125000                         // 货物声明价值，单位：元
        },

        // 提货信息：包含提货地点、联系人等提货相关信息
        "pickupInfo": {
            "customerName": "XX制造公司",          // 提货方公司名称
            "customerId": "cm-123",              // 提货方客户编号
            "area": "江苏省苏州市",               // 提货区域
            "address": "工业园区科技路88号",       // 提货详细地址
            "addressInfo": {
                "province": "江苏省",             // 省份
                "city": "苏州市",                 // 城市
                "district": "工业园区",           // 区县
                "town": "湖东",                   // 街道/镇
                "industrialPark": "科技园",       // 工业园区
                "street": "科技路",               // 街道名
                "number": "88号",                 // 门牌号
                "building": "A座",                // 楼栋号
                "company": "XX制造公司"           // 公司名称
            },
            "contactPerson": "王五",              // 提货联系人姓名
            "contactPhone": "13900139000",       // 提货联系人电话
            "pickupDate": "2024-10-23",          // 预约提货日期
            "pickupTime": "14:30"                // 预约提货时间
        },    
        // 送货信息：包含收货地点、联系人等送货相关信息
        "deliveryInfo": {
            "customerName": "XX物流公司",          // 收货方公司名称
            "customerId": "cm-123",              // 收货方客户编号
            "area": "浙江省杭州市",               // 送货区域
            "address": "滨江区长河路100号",        // 送货详细地址
            "addressInfo": {
                "province": "浙江省",             // 省份
                "city": "杭州市",                 // 城市
                "district": "滨江区",             // 区县
                "town": "长河街道",               // 街道/镇
                "industrialPark": "科技园",       // 工业园区
                "street": "长河路",               // 街道名
                "number": "100号",                // 门牌号
                "building": "B座",                // 楼栋号
                "company": "XX物流公司"           // 公司名称
            },
            "contactPerson": "赵六",              // 收货联系人姓名
            "contactPhone": "13800138000",       // 收货联系人电话
            "deliveryDate": "2024-10-24",        // 预约送达日期
            "deliveryTime": "16:00"              // 预约送达时间
        }
    }
    ```

### 4. 报表管理接口

#### 4.1 收藏报表
- URL: `/reports`
- 方法: POST
- 描述: 收藏报表
- 请求体:

    ```json
    {
        "message_id": "550e8400-e29b-41d4-a716-446655440000",
        "name": "报表名称",
        "sql_text": "SELECT ...",
        "description": "报表描述"
    }
    ```
- 响应:

    ```json
    {
        "data": {
            "report_id": "550e8400-e29b-41d4-a716-446655440000",
            "message_id": "550e8400-e29b-41d4-a716-446655440000",
            "name": "报表名称",
            "sql_text": "SELECT ...",
            "description": "报表描述",
            "usage_count": 0,
            "created_at": "2024-01-01T12:00:00Z",
            "updated_at": "2024-01-01T12:00:00Z"
        },
        "message": ""
    }
    ```

#### 4.2 获取收藏报表列表
- URL: `/reports`
- 方法: GET
- 描述: 获取收藏的报表列表
- 查询参数:
  - page: 页码,默认1
  - size: 每页数量,默认20
- 响应:

    ```json
    {
        "data": {
            "total": 100,
            "items": [{
                "report_id": "550e8400-e29b-41d4-a716-446655440000",
                "message_id": "550e8400-e29b-41d4-a716-446655440000",
                "name": "报表名称",
                "sql_text": "SELECT ...",
                "description": "报表描述",
                "usage_count": 10,
                "last_executed": "2024-01-01T12:00:00Z",
                "created_at": "2024-01-01T12:00:00Z",
                "updated_at": "2024-01-01T12:00:00Z"
            }]
        },
        "message": ""
    }
```

#### 4.3 执行收藏报表
- URL: `/reports/{report_id}/execute`
- 方法: POST
- 描述: 执行收藏的报表
- 请求体:
    ```json
    {
        "parameters": {} // 报表参数
    }
    ```
- 响应:

    ```json
    {
        "data": {
            "columns": ["column1", "column2"],
            "rows": [
                ["value1", "value2"],
                ["value3", "value4"]
            ]
        },
        "message": ""
    }
    ```

## 错误码说明

| 错误码 | 说明 |
|--------|------|
| 400001 | 无效的请求参数 |
| 400002 | 文件格式不支持 |
| 400003 | 文件大小超限 |
| 401001 | 认证令牌无效 |
| 401002 | 认证令牌过期 |
| 500001 | 数据库操作失败 |
| 500002 | 文件处理失败 |

## 使用示例

### 创建对话并发送消息
```bash
# 1. 创建对话
curl -X POST "http://example.com/api/v1/chats" \
     -H "Content-Type: application/json" \
     -H "X-Auth-Token: your-token" \
     -d '{"scene":"order"}'

# 2. 上传语音文件
curl -X POST "http://example.com/api/v1/files/upload" \
     -H "X-Auth-Token: your-token" \
     -F "file=@order.mp3" \
     -F "type=audio"

# 3. 发送消息
curl -X POST "http://example.com/api/v1/chats/{chat_id}/messages" \
     -H "Content-Type: application/json" \
     -H "X-Auth-Token: your-token" \
     -d '{
         "content": {"type":"text", "text":"订单内容"},
         "attachments": ["file_id"]
     }'
```