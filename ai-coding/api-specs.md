# API 设计提示语模板

## 基本信息
- API 名称：[填写 API 名称]
- 功能描述：[详细描述 API 的主要功能和用途]
- 基础 URL：[填写基础 URL，例如 /api/v1/]
- 接口 URL：[填写具体接口 URL]
- 请求方法：[GET/POST/PUT/DELETE]

## 认证信息
所有 API 请求都需要在 Header 中包含认证信息：
```
X-Auth-Token: [认证令牌]
```

## 请求参数
### GET 方法
如果是 GET 请求，参数应该遵循以下格式：
```
URL: /api/v1/resource?param1=value1&param2=value2

参数说明：
- param1：[参数说明]
  - 类型：[string/int/boolean等]
  - 是否必需：[是/否]
  - 示例值：[示例]
  - 说明：[详细说明]
```

### POST/PUT 方法
如果是 POST/PUT 请求，请求体应该遵循以下 JSON 格式：
```json
{
    "field1": "value1",
    "field2": "value2"
}

参数说明：
- field1：[参数说明]
  - 类型：[string/int/boolean等]
  - 是否必需：[是/否]
  - 示例值：[示例]
  - 说明：[详细说明]
```

## 响应格式
所有响应都使用统一的格式：
```json
{
    "data": {}, // 成功时包含实际的业务数据，失败时为 null
    "message": "" // 成功时为空，失败时包含错误信息
}
```

### 成功响应
```json
{
    "data": {
        "id": 12345,
        "name": "示例数据",
        "createTime": "2024-01-01 12:00:00"
    },
    "message": ""
}
```

### 错误响应
```json
{
    "data": null,
    "message": "具体的错误信息"
}
```

## HTTP 状态码说明
- 200 OK：请求成功
- 400 Bad Request：客户端请求错误（参数错误、格式错误等）
- 401 Unauthorized：认证失败
- 500 Internal Server Error：服务器内部错误

## 使用示例
### 请求示例
```bash
# GET 请求示例
curl -X GET "http://api.example.com/api/v1/resource?param1=value1" \
     -H "X-Auth-Token: your-token-here"

# POST 请求示例
curl -X POST "http://api.example.com/api/v1/resource" \
     -H "Content-Type: application/json" \
     -H "X-Auth-Token: your-token-here" \
     -d '{"field1": "value1"}'
```

### 响应示例
#### 成功响应（查询单个资源）
```json
{
    "data": {
        "id": 12345,
        "name": "示例数据",
        "createTime": "2024-01-01 12:00:00"
    },
    "message": ""
}
```

#### 成功响应（查询列表）
```json
{
    "data": {
        "total": 100,
        "items": [
            {
                "id": 12345,
                "name": "示例数据1",
                "createTime": "2024-01-01 12:00:00"
            },
            {
                "id": 12346,
                "name": "示例数据2",
                "createTime": "2024-01-01 12:01:00"
            }
        ]
    },
    "message": ""
}
```

#### 错误响应
```json
{
    "data": null,
    "message": "无效的认证令牌"
}
```