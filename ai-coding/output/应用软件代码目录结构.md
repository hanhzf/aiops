# 代码目录结构

```
project_root/
├── Dockerfile                # Docker构建文件
├── Makefile                 # 构建、测试、打包等命令
├── README.md                # 项目说明文档
├── requirements.txt         # Python依赖包清单
├── setup.py                 # 项目打包配置
├── tox.ini                  # 测试工具配置
├── .gitignore              # Git忽略配置
├── .env.example            # 环境变量示例文件
│
├── config/                  # 配置文件目录
│   ├── __init__.py
│   ├── config.yaml         # 基础配置文件
│   ├── config.prod.yaml    # 生产环境配置
│   └── config.test.yaml    # 测试环境配置
│
├── src/                    # 源代码目录
│   └── app/
│       ├── __init__.py     
│       ├── main.py         # 应用入口文件
│       ├── container.py    # 依赖注入容器
│       │
│       ├── core/           # 核心功能模块
│       │   ├── __init__.py
│       │   ├── exceptions.py      # 自定义异常类
│       │   ├── constants.py       # 常量定义
│       │   └── base/             # 基础类
│       │       ├── __init__.py
│       │       ├── repository.py  # 仓储基类
│       │       ├── service.py     # 服务基类
│       │       └── handler.py     # 处理器基类
│       │
│       ├── models/          # 数据模型
│       │   ├── __init__.py
│       │   ├── chat.py      # 对话相关模型
│       │   ├── order.py     # 订单相关模型
│       │   └── report.py    # 报表相关模型
│       │
│       ├── schemas/         # API模式定义
│       │   ├── __init__.py
│       │   ├── chat.py      # 对话相关校验模式
│       │   ├── order.py     # 订单相关校验模式
│       │   └── report.py    # 报表相关校验模式
│       │
│       ├── handlers/        # HTTP处理器层
│       │   ├── __init__.py
│       │   ├── chat.py      # 对话处理器
│       │   ├── order.py     # 订单处理器
│       │   └── report.py    # 报表处理器
│       │
│       ├── services/        # 业务服务层
│       │   ├── __init__.py
│       │   ├── chat.py      # 对话服务
│       │   ├── order.py     # 订单服务
│       │   └── report.py    # 报表服务
│       │
│       ├── repositories/    # 数据访问层
│       │   ├── __init__.py
│       │   ├── chat.py      # 对话仓储
│       │   ├── order.py     # 订单仓储
│       │   └── report.py    # 报表仓储
│       │
│       ├── infrastructure/  # 基础设施层
│       │   ├── __init__.py
│       │   ├── database.py  # 数据库客户端
│       │   ├── redis.py     # Redis客户端
│       │   ├── storage.py   # 文件存储
│       │   └── events.py    # 事件总线
│       │
│       ├── api/            # API相关
│       │   ├── __init__.py
│       │   ├── routes.py    # 路由定义
│       │   ├── middleware/  # 中间件
│       │   └── deps.py      # 依赖项
│       │
│       ├── websocket/      # WebSocket模块
│       │   ├── __init__.py
│       │   ├── connection.py  # 连接管理
│       │   ├── dispatcher.py  # 消息分发器
│       │   └── handlers.py    # 消息处理器
│       │
│       ├── ai/             # AI能力模块
│       │   ├── __init__.py
│       │   ├── speech.py     # 语音识别
│       │   ├── ocr.py        # 图像识别
│       │   ├── nlp.py        # 自然语言处理
│       │   └── sql_gen.py    # SQL生成器
│       │
│       └── utils/          # 工具函数
│           ├── __init__.py
│           ├── logger.py     # 日志工具
│           ├── security.py   # 安全工具
│           └── validators.py # 验证工具
│
├── tests/                  # 测试目录
│   ├── __init__.py
│   ├── conftest.py         # pytest配置
│   ├── test_handlers/      # Handler层测试
│   ├── test_services/      # Service层测试
│   └── test_repositories/  # Repository层测试
│
└── docs/                   # 文档目录
    ├── api/               # API文档
    ├── architecture/      # 架构文档
    └── deployment/        # 部署文档
```
