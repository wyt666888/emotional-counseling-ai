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



### 5. 翻译文本

**POST** `/api/translate`

**请求体**:
```json
{
  "text": "我很开心",
  "target_lang": "en",  // 可选：'zh-CN' 或 'en'，不提供则自动检测并翻译到相反语言
  "source_lang": "zh-CN" // 可选：源语言代码
}
```

**响应示例**:
```json
{
  "translated_text": "I'm very happy",
  "source_lang": "zh-CN",
  "target_lang": "en",
  "original_text": "我很开心"
}
```

**错误响应示例**:
```json
{
  "translated_text": "我很开心",
  "source_lang": "zh-CN",
  "target_lang": "en",
  "original_text": "我很开心",
  "error": "Translation service error message"
}
```

### 6. 检测语言

**POST** `/api/translate/detect`

**请求体**:
```json
{
  "text": "Hello, how are you?"
}
```

**响应示例**:
```json
{
  "detected_language": "en",
  "text": "Hello, how are you?"
}
```

## 翻译功能说明

### 支持的语言
- **中文**: `zh-CN`
- **英文**: `en`

### 自动语言检测
当不指定 `target_lang` 时，系统会：
1. 自动检测输入文本的语言
2. 将其翻译为相反的语言（中文→英文，英文→中文）

### 语言检测原理
使用基于字符的启发式方法：
- 统计文本中的中文字符（CJK统一表意文字）比例
- 如果中文字符占比超过30%，判定为中文
- 否则判定为英文

### 使用示例

#### 自动检测并翻译
```bash
curl -X POST http://localhost:5000/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "你好，世界"}'
# 自动检测为中文，翻译为英文
```

#### 指定目标语言
```bash
curl -X POST http://localhost:5000/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, world", "target_lang": "zh-CN"}'
# 翻译为中文
```

#### 仅检测语言
```bash
curl -X POST http://localhost:5000/api/translate/detect \
  -H "Content-Type: application/json" \
  -d '{"text": "你好"}'
```

