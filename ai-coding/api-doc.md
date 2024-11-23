# 文件上传 API 文档

## 基本信息
- API 名称：单文件上传接口
- 功能描述：用于上传单个图片、文档等文件到系统
- 基础 URL：/api/v1
- 接口 URL：/api/v1/file/upload
- 请求方法：POST

## 认证信息
所有 API 请求都需要在 Header 中包含认证信息：
```
X-Auth-Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## 请求格式
### Content-Type
```
Content-Type: multipart/form-data
```

### 请求参数
| 参数名 | 参数类型 | 是否必需 | 说明 |
|--------|----------|----------|------|
| file | file | 是 | 要上传的文件 |
| type | string | 否 | 文件类型分类：'voice'(音频),'image'(普通图片) |
| description | string | 否 | 文件描述信息 |

### 支持的文件类型
- 图片：jpg, jpeg, png, gif
- 音频：mp3, wav

### 文件限制
- 最大 20MB

## 响应格式
### 成功响应
```json
{
    "data": {
        "fileUrl": "https://example.com/files/f12345.jpg",
        "fileSize": 1024000,
        "mimeType": "image/jpeg",
        "uploadTime": "2024-01-01 12:00:00",
        "type": "avatar",
    },
    "message": ""
}
```

### 错误响应
```json
{
    "data": null,
    "message": "文件大小超过限制"
}
```

## HTTP 状态码
- 200 OK：上传成功
- 400 Bad Request：请求参数错误
- 401 Unauthorized：认证失败
- 413 Payload Too Large：文件太大
- 415 Unsupported Media Type：不支持的文件类型
- 500 Internal Server Error：服务器内部错误

## 错误说明
| HTTP 状态码 | 错误信息 | 说明 |
|------------|----------|------|
| 400 | Invalid file type | 不支持的文件类型 |
| 400 | File is empty | 文件内容为空 |
| 400 | File is required | 未上传文件 |
| 413 | File size exceeds limit | 文件大小超过限制 |
| 415 | Unsupported file type | 不支持的文件类型 |

## 使用示例
### 请求示例
```bash
curl -X POST "https://api.example.com/api/v1/file/upload" \
     -H "X-Auth-Token: your-token-here" \
     -F "file=@/path/to/profile.jpg" \
     -F "type=avatar" \
     -F "description=用户头像"
```


## 注意事项

* 文件上传后保存到本地临时目录