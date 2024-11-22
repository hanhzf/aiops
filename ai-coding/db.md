# 数据库设计
```sql
-- 对话表：记录所有对话的基本信息
CREATE TABLE chats (
    id SERIAL PRIMARY KEY,                    -- 对话ID
    scene VARCHAR(20) NOT NULL,               -- 场景类型：help/order/report
    creator_id INTEGER NOT NULL,              -- 创建者ID
    create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,  -- 创建时间
    update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP   -- 更新时间
);

-- 消息表：记录对话中的所有消息
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,                    -- 消息ID
    chat_id INTEGER NOT NULL,                 -- 所属对话ID
    msg_type VARCHAR(20) NOT NULL,            -- 消息类型：voice/text/confirm
    content TEXT,                             -- 文本内容（包括用户输入的文本、语音识别的文本、图片识别的文本）
    file_url VARCHAR(255),                    -- 文件URL（可以是语音文件或图片文件的URL）
    sender VARCHAR(20) NOT NULL,              -- 发送方：user/system
    create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,  -- 创建时间
    FOREIGN KEY (chat_id) REFERENCES chats(id)
);

-- 订单信息表：存储从对话中提取的订单信息
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,                    -- 订单ID
    chat_id INTEGER NOT NULL,                 -- 关联的对话ID
    message_id INTEGER NOT NULL,              -- 关联的消息ID
    company_name VARCHAR(100),                -- 公司名称
    content JSONB NOT NULL,                   -- 订单详细信息(JSON格式)
    creator_id INTEGER NOT NULL,              -- 创建者ID
    create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,  -- 创建时间
    update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,  -- 更新时间
    FOREIGN KEY (chat_id) REFERENCES chats(id),
    FOREIGN KEY (message_id) REFERENCES messages(id)
);

-- SQL记录表：存储生成的SQL语句
CREATE TABLE sql_records (
    id SERIAL PRIMARY KEY,                    -- SQL记录ID
    chat_id INTEGER NOT NULL,                 -- 关联的对话ID
    message_id INTEGER NOT NULL,              -- 关联的消息ID
    sql_content TEXT NOT NULL,                -- SQL内容
    params JSONB,                             -- SQL参数(JSON格式)
    creator_id INTEGER NOT NULL,              -- 创建者ID
    create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,  -- 创建时间
    FOREIGN KEY (chat_id) REFERENCES chats(id),
    FOREIGN KEY (message_id) REFERENCES messages(id)
);

-- 报表结果表：存储报表查询结果
CREATE TABLE report_results (
    id SERIAL PRIMARY KEY,                    -- 报表结果ID
    chat_id INTEGER NOT NULL,                 -- 关联的对话ID
    message_id INTEGER NOT NULL,              -- 关联的消息ID
    sql_record_id INTEGER NOT NULL,           -- 关联的SQL记录ID
    result_data JSONB NOT NULL,               -- 查询结果(JSON格式)
    creator_id INTEGER NOT NULL,              -- 创建者ID
    create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,  -- 创建时间
    FOREIGN KEY (chat_id) REFERENCES chats(id),
    FOREIGN KEY (message_id) REFERENCES messages(id),
    FOREIGN KEY (sql_record_id) REFERENCES sql_records(id)
);

-- 报表收藏表：存储用户收藏的报表
CREATE TABLE report_favorites (
    id SERIAL PRIMARY KEY,                    -- 收藏ID
    name VARCHAR(100) NOT NULL,               -- 报表名称
    description TEXT,                         -- 报表描述
    sql_record_id INTEGER NOT NULL,           -- 关联的SQL记录ID
    creator_id INTEGER NOT NULL,              -- 创建者ID
    create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,  -- 创建时间
    update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,  -- 更新时间
    last_view_time TIMESTAMP,                 -- 最后查看时间
    view_count INTEGER DEFAULT 0,             -- 查看次数
    FOREIGN KEY (sql_record_id) REFERENCES sql_records(id)
);
```