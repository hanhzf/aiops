# API接口设计文档

## 基本信息
- 基础 URL：`/api/v1`
- 认证方式：所有接口需要在Header中携带认证信息
```
X-Auth-Token: [认证令牌]
```

## 通用响应格式
```json
{
    "data": {},  // 成功时包含实际数据,失败时为null
    "message": "" // 成功时为空,失败时包含错误信息
}
```

## HTTP状态码说明
- 200 OK：请求成功
- 400 Bad Request：客户端请求错误（参数错误、格式错误等）
- 401 Unauthorized：认证失败
- 500 Internal Server Error：服务器内部错误

## API接口列表

### 1. 文件处理接口

#### 1.1 上传文件
- URL：`/files/upload`
- 方法：POST
- 描述：上传语音或图片文件
- 请求体：
    ```
    Content-Type: multipart/form-data
    file: [文件内容]
    type: [file_type] // audio或image
    ```
- 响应：
    ```json
    {
        "data": {
            "id": "550e8400-e29b-41d4-a716-446655440000",
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
- URL：`/chats`
- 方法：POST
- 描述：创建新的对话会话
- 请求体：
    ```json
    {
        "scene": "order" // order或report
    }
    ```
- 响应：
    ```json
    {
        "data": {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "created_at": "2024-01-01T12:00:00Z"
        },
        "message": ""
    }
    ```

#### 2.2 获取对话历史清单
- URL：`/chats`
- 方法：GET
- 描述：获取对话清单
- 查询参数：
  - page：页码，默认1
  - size：每页数量，默认20
- 响应：
    ```json
    {
        "data": {
            "items": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "scene": "report",
                    "created_at": "2024-01-01T12:00:00Z",
                    "updated_at": "2024-01-01T12:00:00Z"
                }
            ],
            "pagination": {
                "page": 1,
                "size": 20,
                "total": 100,
                "total_pages": 5
            }
        },
        "message": ""
    }
    ```

#### 2.3 获取对话详情
- URL：`/chats/{chat_id}`
- 方法：GET
- 描述：获取指定对话的详情
- 响应：
    ```json
    {
        "data": {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "scene": "report",
            "created_at": "2024-01-01T12:00:00Z",
            "updated_at": "2024-01-01T12:00:00Z"
        },
        "message": ""
    }
    ```

#### 2.4 获取对话历史消息
- URL：`/chats/{chat_id}/messages`
- 方法：GET
- 描述：获取指定对话的历史消息
- 查询参数：
  - page：页码，默认1
  - size：每页数量，默认20
  - index：获取某个index后的消息
- 响应：
    ```json
    {
        "data": {
            "items": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
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
            ],
            "pagination": {
                "page": 1,
                "size": 20,
                "total": 100,
                "total_pages": 5
            }
        },
        "message": ""
    }
    ```

#### 2.5 发送消息
- URL：`/chats/{chat_id}/completion`
- 方法：POST
- 描述：在指定对话中发送消息
- 请求体：
    ```json
    {
        "prompt": "请描述你的需求", // 可选，但prompt和attachments不可全为空
        "parent_message_id": "661a9432-e29b-41d4-a716-123456229921",
        "stream": "true", // 是否启用流式响应
        "attachments": ["550e8400-e29b-41d4-a716-446655440000"] // 可选,关联的文件ID
    }
    ```
- 响应(stream=false)：
    ```json
    {
        "data": {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "chat_id": "550e8400-e29b-41d4-a716-446655440000",
            "index": 1,
            "sender": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "消息内容"
                }
            ],
            "attachments": [],
            "created_at": "2024-01-01T12:00:00Z"
        },
        "message": ""
    }
    ```

- 响应(stream=true)：
    * API 会按照流式的格式对结果进行返回，也即后台会按照如下格式返回多个message，直到done。
    * 客户端需要根据 event 的类型来判断该消息返回是否结束。
    * 当 event 是 message_delta 时，表示消息的发送结束。
    * 当 event 是 message_done 时，说明正在发送过程中。

    ```json
    {
        "data": {
            "event_type": "delta",
            "index": 1, // message的索引号
            "type": "text", // 文字
            "content": "好的，这就为您设计"
        }
    }

    {
        "data": {
            "event_type": "delta",
            "index": 1,
            "type": "pwchart", // chart
            "content": "<pwchart></pwchart>"
        }
    }

    {
        "data": {
            "event_type": "done",
        }
    }
    ```

#### 2.6 获取最新的消息
- URL：`/chats/{chat_id}/messages/latest`
- 方法：GET
- 描述：获取最新的消息
- 响应：
    ```json
    {
        "data": {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "chat_id": "550e8400-e29b-41d4-a716-446655440000",
            "index": 1,
            "sender": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "消息内容"
                }
            ],
            "attachments": [],
            "created_at": "2024-01-01T12:00:00Z"
        },
        "message": ""
    }
    ```

### 3. 订单处理接口

#### 3.1 创建订单
- URL：`/orders`
- 方法：POST
- 描述：创建新订单
- 请求体：
    ```json
    {
        "transport_info": {
            "sales_name": "李四",
            "created_time": "2024-10-22",
            "cargo_type": "普货",
            "transport_type": "汽运",
            "delivery_type": "送货上门",
            "payment_type": "月付",
            "delivery_route": "",
            "delivery_plan": "",
            "vehicle_number": "",
            "remarks": "轻拿轻放"
        },
        "cargo_info": {
            "quantity": 15,
            "unit": "托",
            "weight": 23.00,
            "volume": 3.20,
            "unit_type": "重量",
            "value": 125000
        },
        "pickup_info": {
            "customer_name": "XX制造公司",
            "customer_id": "cm-123",
            "area": "江苏省苏州市",
            "address": "工业园区科技路88号",
            "address_info": {
                "province": "江苏省",
                "city": "苏州市",
                "district": "工业园区",
                "town": "湖东",
                "industrial_park": "科技园",
                "street": "科技路",
                "number": "88号",
                "building": "A座",
                "company": "XX制造公司"
            },
            "contact_person": "王五",
            "contact_phone": "13900139000",
            "pickup_date": "2024-10-23",
            "pickup_time": "14:30"
        },
        "delivery_info": {
            "customer_name": "XX物流公司",
            "customer_id": "cm-123",
            "area": "浙江省杭州市",
            "address": "滨江区长河路100号",
            "address_info": {
                "province": "浙江省",
                "city": "杭州市",
                "district": "滨江区",
                "town": "长河街道",
                "industrial_park": "科技园",
                "street": "长河路",
                "number": "100号",
                "building": "B座",
                "company": "XX物流公司"
            },
            "contact_person": "赵六",
            "contact_phone": "13800138000",
            "delivery_date": "2024-10-24",
            "delivery_time": "16:00"
        }
    }
    ```
- 响应：
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
- URL：`/orders`
- 方法：GET
- 描述：获取订单列表
- 查询参数：
  - page：页码，默认1
  - size：每页数量，默认20
- 响应：
    ```json
    {
        "data": {
            "items": [
                {
                    "order_id": "550e8400-e29b-41d4-a716-446655440000",
                    "from_customer": "发货客户",
                    "from_address": "发货地址",
                    "to_customer": "收货客户",
                    "to_address": "收货地址",
                    "created_at": "2024-01-01T12:00:00Z"
                }
            ],
            "pagination": {
                "page": 1,
                "size": 20,
                "total": 100,
                "total_pages": 5
            }
        },
        "message": ""
    }
    ```

#### 3.3 获取订单详情
- URL：`/orders/{order_id}`
- 方法：GET
- 描述：获取订单详情
- 响应：
    ```json
    {
        "data": {
            "transport_info": {
                "sales_name": "李四",
                "created_time": "2024-10-22",
                "cargo_type": "普货",
                "transport_type": "汽运",
                "delivery_type": "送货上门",
                "payment_type": "月付",
                "delivery_route": "",
                "delivery_plan": "",
                "vehicle_number": "",
                "remarks": "轻拿轻放"
            },
            "cargo_info": {
                "quantity": 15,
                "unit": "托",
                "weight": 23.00,
                "volume": 3.20,
                "unit_type": "重量",
                "value": 125000
            },
            "pickup_info": {
                "customer_name": "XX制造公司",
                "customer_id": "cm-123",
                "area": "江苏省苏州市",
                "address": "工业园区科技路88号",
                "address_info": {
                    "province": "江苏省",
                    "city": "苏州市",
                    "district": "工业园区",
                    "town": "湖东",
                    "industrial_park": "科技园",
                    "street": "科技路",
                    "number": "88号",
                    "building": "A座",
                    "company": "XX制造公司"
                },
                "contact_person": "王五",
                "contact_phone": "13900139000",
                "pickup_date": "2024-10-23",
                "pickup_time": "14:30"
            },
            "delivery_info": {
                "customer_name": "XX物流公司",
                "customer_id": "cm-123",
                "area": "浙江省杭州市",
                "address": "滨江区长河路100号",
                "address_info": {
                    "province": "浙江省",
                    "city": "杭州市",
                    "district": "滨江区",
                    "town": "长河街道",
                    "industrial_park": "科技园",
                    "street": "长河路",
                    "number": "100号",
                    "building": "B座",
                    "company": "XX物流公司"
                },
                "contact_person": "赵六",
                "contact_phone": "13800138000",
                "delivery_date": "2024-10-24",
                "delivery_time": "16:00"
            }
        },
        "message": ""
    }
    ```

### 4. 报表管理接口

#### 4.1 收藏报表
- URL：`/reports`
- 方法：POST
- 描述：收藏报表
- 请求体：
    ```json
    {
        "message_id": "550e8400-e29b-41d4-a716-446655440000",
        "message_content_index": 3,
        "name": "报表名称"
    }
    ```
- 响应：
    ```json
    {
        "data": {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "created_at": "2024-01-01T12:00:00Z"
        },
        "message": ""
    }
    ```

#### 4.2 获取收藏报表列表
- URL：`/reports`
- 方法：GET
- 描述：获取收藏的报表列表
- 查询参数：
  - page：页码，默认1
  - size：每页数量，默认20
- 响应：
    ```json
    {
        "data": {
            "items": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "name": "报表名称",
                    "usage_count": 10,
                    "last_executed": "2024-01-01T12:00:00Z",
                    "created_at": "2024-01-01T12:00:00Z",
                    "updated_at": "2024-01-01T12:00:00Z"
                }
            ],
            "pagination": {
                "page": 1,
                "size": 20,
                "total": 100,
                "total_pages": 5
            }
        },
        "message": ""
    }
    ```

#### 4.3 执行收藏报表
- URL：`/reports/{report_id}/execute`
- 方法：POST
- 描述：执行收藏的报表
- 请求体：
    ```json
    {
        "parameters": {
            "start_date": "2024-01-01",
            "end_date": "2024-01-31",
            "region": "苏州"
        }
    }
    ```
- 响应：
    ```json
    {
        "data": {
            "x_axis": {
                "type": "category",
                "data": ["第1周", "第2周", "第3周", "第4周"]
            },
            "series": [
                {
                    "name": "姑苏区",
                    "type": "line",
                    "data": [2.5, 2.8, 3.1, 3.4]
                },
                {
                    "name": "工业园区",
                    "type": "line",
                    "data": [4.2, 4.0, 3.9, 3.8]
                }
            ]
        },
        "message": ""
    }
    ```

## 使用示例

### 1. 创建对话并发送消息
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
curl -X POST "http://example.com/api/v1/chats/{chat_id}/completion" \
     -H "Content-Type: application/json" \
     -H "X-Auth-Token: your-token" \
     -d '{
           "prompt": "我想创建一个订单",
           "attachments": ["file-id-123"]
         }'
```

### 2. 收藏并执行报表
```bash
# 1. 收藏报表
curl -X POST "http://example.com/api/v1/reports" \
     -H "Content-Type: application/json" \
     -H "X-Auth-Token: your-token" \
     -d '{
           "message_id": "msg-id-123",
           "message_content_index": 3,
           "name": "销量周报"
         }'

# 2. 执行报表
curl -X POST "http://example.com/api/v1/reports/{report_id}/execute" \
     -H "Content-Type: application/json" \
     -H "X-Auth-Token: your-token" \
     -d '{
           "parameters": {
             "start_date": "2024-01-01",
             "end_date": "2024-01-31"
           }
         }'
```