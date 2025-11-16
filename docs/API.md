\# API 文档



\## 基础信息



\- \*\*Base URL\*\*: `http://localhost:5000/api`

\- \*\*Content-Type\*\*: `application/json`



\## 端点



\### 1. 健康检查



\*\*GET\*\* `/api/health`



\*\*响应示例\*\*:

```json

{

&nbsp; "status": "ok",

&nbsp; "message": "Emotional Counseling AI is running"

}

```



\### 2. 发送消息



\*\*POST\*\* `/api/chat`



\*\*请求体\*\*:

```json

{

&nbsp; "message": "我和男朋友吵架了",

&nbsp; "session\_id": "optional-session-id"

}

```



\*\*响应示例\*\*:

```json

{

&nbsp; "message": "我能理解你现在的心情💙...",

&nbsp; "emotion": "sad",

&nbsp; "session\_id": "abc-123"

}

```



\### 3. 创建新会话



\*\*POST\*\* `/api/session/new`



\*\*响应示例\*\*:

```json

{

&nbsp; "session\_id": "550e8400-e29b-41d4-a716-446655440000"

}

```



\### 4. 删除会话



\*\*DELETE\*\* `/api/session/{session\_id}`



\*\*响应示例\*\*:

```json

{

&nbsp; "message": "会话已删除"

}

```

