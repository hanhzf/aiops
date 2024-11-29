# 逻辑模型E-R图

```mermaid
erDiagram
    User ||--o{ Chat : creates
    User ||--o{ Message : sends
    User ||--o{ Order : creates
    User ||--o{ Report : creates

    Chat ||--o{ Message : contains
    Message ||--o{ Attachment : has
    Message ||--o{ MessageContent : contains
    
    Chat {
        id uuid PK
        status string
        scene string
        created_at timestamp
        updated_at timestamp
        creator_id uuid FK
    }

    Message {
        id uuid PK
        chat_id uuid FK
        parent_id uuid FK
        index int
        sender string
        attachments string
        created_at timestamp
    }

    MessageContent {
        id uuid PK
        message_id uuid FK
        type string
        data string
        sql_text string
    }

    Attachment {
        id uuid PK
        name string 
        size int
        type string
        created_at timestamp
        extracted_content string
    }

    Order {
        id uuid PK
        chat_id uuid FK
        from_customer string
        from_address string
        to_customer string
        to_address string
        content jsonb
        created_at timestamp
    }

    Report {
        id uuid PK
        message_id uuid FK
        name string
        sql_text string
        description string 
        usage_count int
        last_executed timestamp
        created_at timestamp
        updated_at timestamp
    }

    User {
        id uuid PK
        name string
        phone string
        created_at timestamp
    }
```

* 用户信息从 TMS 系统同步过来
* order 信息在 content 中通过 JSON 的形式记录订单全部信息。 
* report 表格记录的是用户收藏的报表信息。 * message 所关联的 MessageContent 在实际实现时可在 message 表中增加一个 JSONB 的 content 字段
* attachment 用来保存用户上传的图片或者语音以及系统所生成的 SVG 图片等。