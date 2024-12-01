# 应用软件分层架构E-R图


```mermaid
classDiagram
    %% HTTP Handlers
    class HTTPHandler {
        +handle_request()
    }
    
    class ChatHandler {
        +get_chat(chat_id)
        +query_chats(chat_id)
        +create_chat()
        +delete_chat()
        +chat_completion()
        +get_latest_message()
    }
    
    class OrderHandler {
        +query_orders()
        +get_order(order_id)
        +create_order(order_data)
    }
    
    class ReportHandler {
        +get_favorite_report()
        +create_favorite_report()
        +query_favorite_reports()
    }

    class FileHandler {
        +upload_file()
        +get_file(file_id)
    }

    %% Services
    class DispatcherService {
        +run()
        +dispatch(message)
    }

    class ChatService {
        +get_chat(chat_id)
        +query_chats()
        +create_chat()
        +delete_chat()
        +create_message()
        +get_latest_message()
    }

    class OrderService {
        +handle_message()
        +get_order(order_id)
        +create_order(order_data)
        -_refactor_company_name()
        -_refactor_address()
        -_parse_order_info()
    }

    class ReportService {
        +handle_message()
        +get_favorite_report()
        +create_favorite_report()
        +query_favorite_reports()
        +_get_report_sql()
    }

    class FileService {
        +upload(file)
        +get_file(file_id)
        -_validate_file(file)
        -_store_file(file)
    }

    class AIService {
        +asr(audio_file)
        +ocr(image_file) 
        +call(prompt)
    }

    class External_TmsService {
        +create_order(order_data)
        +get_order_status(order_id)
    }

    %% Infrastructure
    class DBClient {
        +execute_query()
        +execute_transaction()
    }

    class Repository {
        <<interface>>
        +find_one()
        +find_many()
        +create()
        +update()
        +delete()
    }

    class ChatRepository {
        +get_chat(chat_id)
        +query_chats()
        +create_chat()
        +delete_chat()
        +create_message()
        +get_message()
    }

    class OrderRepository {
        +get_order()
        +query_orders()
        +create_order()
    }

    class ReportRepository {
        +create_favorite_report()
        +get_favorite_report()
        +query_favorite_reports()
    }

    %% Dependencies
    HTTPHandler ..> ChatHandler
    HTTPHandler ..> OrderHandler
    HTTPHandler ..> ReportHandler
    HTTPHandler ..> FileHandler
    
    ChatHandler ..> DispatcherService

    DispatcherService ..> OrderService
    DispatcherService ..> ChatService
    DispatcherService ..> ReportService
    
    ChatHandler ..> ChatService
    OrderHandler ..> OrderService
    ReportHandler ..> ReportService
    FileHandler ..> FileService
    
    ChatService ..> ChatRepository
    OrderService ..> OrderRepository
    OrderHandler ..> External_TmsService
    OrderService ..> AIService
    ReportService ..> ReportRepository
    ReportService ..> AIService
    
    Repository <|.. ChatRepository
    Repository <|.. OrderRepository
    Repository <|.. ReportRepository
    
    ChatRepository ..> DBClient
    OrderRepository ..> DBClient
    ReportRepository ..> DBClient
```

暂时不用 `Websocket`，以下内容暂不启动:

```
class External_WssService {
    +on_connect()
    +on_message()
    +on_disconnect()
}

class WebSocketHandler {
    +publish(topic, message)
    +subscribe(topic, callback)
    +unsubscribe(topic)
    +keep_alive()
    +get_topics()
    +get_connections()
}
```