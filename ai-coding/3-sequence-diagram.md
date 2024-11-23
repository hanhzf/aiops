# 系统交互时序图设计

## 1.建立websocket连接

* 前端首次打开即建立WebSocket连接
* 一个WebSocket连接可以处理多个对话

```mermaid
sequenceDiagram
    participant Client
    participant WebSocket

    rect rgb(240, 240, 240)
        Note over Client,WebSocket: WebSocket连接建立流程
        Client->>WebSocket: 建立WebSocket连接
        WebSocket-->>Client: 连接确认
    end
```

## 2.指引场景

* 用户进入首页后通过语音进行功能导航
* 后台处理导航请求并返回目标URL，前端完成功能跳转

```mermaid
sequenceDiagram
    participant Client
    participant WebSocket
    participant HTTP
    participant FileModule
    participant SceneDispatcher
    participant ChatModule
    participant ScenarioModule
    participant AIModule

    %% %% WebSocket连接建立（只需要建立一次）
    %% Client->>WebSocket: 建立WebSocket连接
    %% WebSocket-->>Client: 连接确认

    %% 第一次语音文件上传流程（首页导航请求）
    rect rgb(240, 240, 240)
        Note over Client,AIModule: 首次请求（模糊导航）
        Client->>HTTP: POST /api/v1/chat (创建对话, 场景=help)
        HTTP->>ChatModule: 创建新对话
        ChatModule-->>Client: 返回对话ID
        
        Client->>HTTP: POST /api/v1/files/upload (上传语音文件)
        HTTP->>FileModule: 处理文件上传
        FileModule->>FileModule: 保存文件到OSS
        FileModule-->>Client: 返回文件URL
        
        Client->>WebSocket: 发送消息 {"chatId": "xxx", "scene": "help", "type": "guide", "url": "file_url"}
        WebSocket->>ChatModule: 保存消息记录
        WebSocket->>SceneDispatcher: 转发消息进行场景分发
        SceneDispatcher->>ScenarioModule: 转发指引场景消息
        ScenarioModule->>AIModule: 请求语音识别
        AIModule-->>ScenarioModule: 返回语音识别文本: "我想看报表"
        ScenarioModule->>AIModule: 分析导航意图，生成确认问题
        AIModule-->>ScenarioModule: 返回确认问题
        ScenarioModule->>WebSocket: 发布确认问题 {"chatId": "xxx", "type": "confirm", "content": "请问您是要前往报表生成页面吗？"}
        WebSocket-->>Client: 推送确认问题
    end

    %% 用户确认流程
    rect rgb(240, 250, 240)
        Note over Client,AIModule: 用户确认流程
        Client->>HTTP: POST /api/v1/files/upload (上传确认语音文件)
        HTTP->>FileModule: 处理文件上传
        FileModule->>FileModule: 保存文件到OSS
        FileModule-->>Client: 返回文件URL
        
        Client->>WebSocket: 发送确认消息 {"chatId": "xxx", "scene": "help", "type": "guide", "url": "file_url"}
        WebSocket->>ChatModule: 保存消息记录
        WebSocket->>SceneDispatcher: 转发消息进行场景分发
        SceneDispatcher->>ScenarioModule: 转发指引场景消息
        ScenarioModule->>AIModule: 请求语音识别
        AIModule-->>ScenarioModule: 返回语音识别文本
        ScenarioModule->>AIModule: 解析确认意图
        AIModule-->>ScenarioModule: 返回解析结果
        ScenarioModule->>WebSocket: 发布导航信息 {"chatId": "xxx", "type": "navigation", "url": "/report", "scene": "report"}
        WebSocket-->>Client: 推送导航信息
        Note over Client: 前端根据URL进行页面跳转
    end
```

## 3.智能填单场景

* 创建订单场景的对话
* 通过语音/文字输入订单信息

```mermaid
sequenceDiagram
    participant Client
    participant WebSocket
    participant HTTP
    participant FileModule
    participant SceneDispatcher
    participant ChatModule
    participant OrderModule
    participant AIModule

    %% %% WebSocket连接建立（只需要建立一次）
    %% Client->>WebSocket: 建立WebSocket连接
    %% WebSocket-->>Client: 连接确认

    %% 场景1: 语音文件上传流程
    rect rgb(240, 240, 240)
        Note over Client,OrderModule: 场景1: 语音文件上传
        Client->>HTTP: POST /api/v1/chat (创建对话, 场景=订单)
        HTTP->>ChatModule: 创建新对话
        ChatModule-->>Client: 返回对话ID
        
        Client->>HTTP: POST /api/v1/files/upload (上传语音文件)
        HTTP->>FileModule: 处理文件上传
        FileModule->>FileModule: 保存文件到OSS
        FileModule-->>Client: 返回文件URL
        
        Client->>WebSocket: 发送消息 {"chatId": "xxx", "scene": "order", "type": "voice", "url": "file_url"}
        WebSocket->>ChatModule: 保存消息记录
        WebSocket->>SceneDispatcher: 转发消息进行场景分发
        SceneDispatcher->>OrderModule: 转发订单场景消息
        OrderModule->>AIModule: 请求语音识别
        AIModule-->>OrderModule: 返回语音识别文本
        OrderModule->>AIModule: 请求提取订单信息
        AIModule-->>OrderModule: 返回结构化订单数据
        OrderModule->>WebSocket: 发布处理结果 {"chatId": "xxx", "data": {...}}
        WebSocket-->>Client: 推送消息
    end

    %% 场景2: 直接发送文字流程
    rect rgb(240, 250, 240)
        Note over Client,OrderModule: 场景2: 直接发送文字
        Client->>HTTP: POST /api/v1/chat (创建对话, 场景=订单)
        HTTP->>ChatModule: 创建新对话
        ChatModule-->>Client: 返回对话ID
        
        Client->>WebSocket: 发送消息 {"chatId": "xxx", "scene": "order", "type": "text", "content": "订单内容"}
        WebSocket->>ChatModule: 保存消息记录
        WebSocket->>SceneDispatcher: 转发消息进行场景分发
        SceneDispatcher->>OrderModule: 转发订单场景消息
        OrderModule->>AIModule: 请求提取订单信息
        AIModule-->>OrderModule: 返回结构化订单数据
        OrderModule->>WebSocket: 发布处理结果 {"chatId": "xxx", "data": {...}}
        WebSocket-->>Client: 推送消息
    end
```

## 4.智能报表场景

* 创建报表场景的对话
* 语音/文字描述报表需求
* 支持模糊请求的二次确认

```mermaid
sequenceDiagram
    participant Client
    participant WebSocket
    participant HTTP
    participant FileModule
    participant SceneDispatcher
    participant ChatModule
    participant ReportModule
    participant AIModule
    participant DBModule

    %% %% WebSocket连接建立（只需要建立一次）
    %% Client->>WebSocket: 建立WebSocket连接
    %% WebSocket-->>Client: 连接确认

    %% 第一次语音文件上传流程（模糊请求）
    rect rgb(240, 240, 240)
        Note over Client,DBModule: 第一次语音上传（模糊请求）
        Client->>HTTP: POST /api/v1/chat (创建对话, 场景=报表)
        HTTP->>ChatModule: 创建新对话
        ChatModule-->>Client: 返回对话ID
        
        Client->>HTTP: POST /api/v1/files/upload (上传语音文件)
        HTTP->>FileModule: 处理文件上传
        FileModule->>FileModule: 保存文件到OSS
        FileModule-->>Client: 返回文件URL
        
        Client->>WebSocket: 发送消息 {"chatId": "xxx", "scene": "report", "type": "voice", "url": "file_url"}
        WebSocket->>ChatModule: 保存消息记录
        WebSocket->>SceneDispatcher: 转发消息进行场景分发
        SceneDispatcher->>ReportModule: 转发报表场景消息
        ReportModule->>AIModule: 请求语音识别
        AIModule-->>ReportModule: 返回语音识别文本: "帮我查询今天的收入"
        ReportModule->>AIModule: 分析意图，生成确认问题
        AIModule-->>ReportModule: 返回确认问题
        ReportModule->>WebSocket: 发布确认问题 {"chatId": "xxx", "type": "confirm", "content": "请问您是不是要查询今天的所有订单的收入金额的总和？"}
        WebSocket-->>Client: 推送确认问题
    end

    %% 用户确认流程
    rect rgb(240, 250, 240)
        Note over Client,DBModule: 用户确认流程
        Client->>HTTP: POST /api/v1/files/upload (上传确认语音文件)
        HTTP->>FileModule: 处理文件上传
        FileModule->>FileModule: 保存文件到OSS
        FileModule-->>Client: 返回文件URL
        
        Client->>WebSocket: 发送确认消息 {"chatId": "xxx", "scene": "report", "type": "voice", "url": "file_url"}
        WebSocket->>ChatModule: 保存消息记录
        WebSocket->>SceneDispatcher: 转发消息进行场景分发
        SceneDispatcher->>ReportModule: 转发报表场景消息
        ReportModule->>AIModule: 请求语音识别
        AIModule-->>ReportModule: 返回语音识别文本
        ReportModule->>AIModule: 请求生成SQL语句
        AIModule-->>ReportModule: 返回生成的SQL
        ReportModule->>DBModule: 执行SQL查询
        DBModule-->>ReportModule: 返回查询结果
        ReportModule->>WebSocket: 发布处理结果 {"chatId": "xxx", "data": {...}, "sql": "..."}
        WebSocket-->>Client: 推送消息
    end
```

## 5.报表收藏时序

```mermaid
sequenceDiagram
    participant Client
    participant HTTP
    participant ReportModule
    participant DBModule

    rect rgb(240, 240, 240)
        Note over Client,DBModule: 报表收藏流程
        
        Note over Client,ReportModule: 用户对当前会话中的报表结果进行收藏
        Client->>HTTP: POST /api/v1/reports/favorites {"chatId": "xxx", "reportId": "xxx"}
        HTTP->>ReportModule: 转发收藏请求
        ReportModule->>ReportModule: 获取报表信息(SQL/查询参数等)
        ReportModule->>DBModule: 保存收藏信息
        ReportModule-->>Client: 返回收藏结果
    end

    rect rgb(240, 250, 240)
        Note over Client,DBModule: 查看收藏报表流程
        
        Client->>HTTP: GET /api/v1/reports/favorites (获取收藏列表)
        HTTP->>ReportModule: 请求收藏报表列表
        ReportModule->>DBModule: 查询收藏报表数据
        DBModule-->>ReportModule: 返回收藏列表
        ReportModule-->>Client: 返回收藏报表列表
        
        Note over Client,ReportModule: 用户点击查看某个收藏报表
        Client->>HTTP: GET /api/v1/reports/favorites/{id}/data
        HTTP->>ReportModule: 转发查看请求
        ReportModule->>DBModule: 获取收藏的SQL和参数
        DBModule-->>ReportModule: 返回SQL和参数
        ReportModule->>DBModule: 执行SQL查询
        DBModule-->>ReportModule: 返回查询结果
        ReportModule-->>Client: 返回报表数据
    end
```