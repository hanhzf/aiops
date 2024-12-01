# stream-chat

## 前端

```javascript
// 普通模式
async function normalChat() {
  const response = await fetch('/chat', {
    method: 'POST',
    body: JSON.stringify({
      message: '你好',
      stream: false
    })
  });
  const data = await response.json();
  displayMessage(data.content);
}

// 流式模式
function streamChat() {
  const eventSource = new EventSource('/chat/stream');
  let fullContent = '';
  
  // 处理消息事件
  eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);
    fullContent += data.content;
    
    // 实时更新UI
    updateUI(fullContent);
    
    // 如果接收完成,关闭连接
    if (data.done) {
      eventSource.close();
    }
  };

  // 错误处理
  eventSource.onerror = (error) => {
    console.error('Stream error:', error);
    eventSource.close();
  };
}

// React组件示例
function ChatComponent() {
  const [messages, setMessages] = useState([]);
  const [currentMessage, setCurrentMessage] = useState('');

  const handleStream = useCallback((content) => {
    setCurrentMessage(prev => prev + content);
  }, []);

  return (
    <div>
      {messages.map(msg => (
        <div className="message">{msg}</div>
      ))}
      {/* 实时显示正在生成的消息 */}
      {currentMessage && (
        <div className="message generating">
          {currentMessage}
          <span className="cursor">|</span>
        </div>
      )}
    </div>
  );
}

// 后端超时如何处理
const streamChat = () => {
  const eventSource = new EventSource('/chat/completions');
  
  // 设置整体超时
  const timeout = setTimeout(() => {
    eventSource.close();
    handleError('Stream timeout');
  }, 30000); // 30秒超时
  
  eventSource.onmessage = (event) => {
    // 每收到消息重置超时
    clearTimeout(timeout);
    // ... 处理消息
  };
}
```

## 后端

```python
from fastapi import FastAPI
from sse_starlette.sse import EventSourceResponse
import asyncio

app = FastAPI()

@app.post("/chat/stream")
async def chat_stream(request):
    # 如果请求stream=false,使用普通响应
    if not request.stream:
        response = await generate_complete_response()
        return response
    
    # stream=true时使用SSE响应
    async def event_generator():
        # 模拟生成多个内容片段
        for i in range(5):
            # 生成内容片段
            chunk = await generate_chunk()
            
            # 构建SSE消息
            yield {
                "event": "message",
                "data": {
                    "content": chunk,
                    "done": i == 4  # 最后一条标记结束
                }
            }
            await asyncio.sleep(0.5)  # 模拟生成延迟

    return EventSourceResponse(event_generator())
```