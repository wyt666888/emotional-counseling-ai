# RAG (检索增强生成) 功能详细文档

## 目录
- [概述](#概述)
- [架构设计](#架构设计)
- [核心组件](#核心组件)
- [安装配置](#安装配置)
- [使用指南](#使用指南)
- [性能优化](#性能优化)
- [故障排查](#故障排查)
- [API 参考](#api-参考)

## 概述

RAG (Retrieval-Augmented Generation) 是一种结合信息检索和生成式 AI 的先进技术。在情感咨询 AI 系统中，RAG 能够：

- 📚 **知识增强**：从专业知识库中检索相关内容
- 🎯 **精准回复**：基于检索到的专业知识提供更准确的建议
- 🔄 **动态适应**：根据不同问题检索不同的专业内容
- ⚡ **高效响应**：通过缓存机制保持快速响应

### 为什么需要 RAG？

传统 LLM 的局限：
- 知识截止日期限制
- 缺乏领域专业知识
- 可能产生不准确的信息（幻觉）

RAG 的优势：
- ✅ 实时访问最新的专业知识
- ✅ 提供有据可查的专业建议
- ✅ 降低错误和不准确信息的风险
- ✅ 可以持续更新和扩展知识库

## 架构设计

```
用户查询
    ↓
┌─────────────────┐
│   查询处理      │
│  (Query Input)  │
└─────────────────┘
    ↓
┌─────────────────┐
│   嵌入生成      │
│  (Embeddings)   │ ← Sentence-Transformers
└─────────────────┘
    ↓
┌─────────────────┐
│   向量检索      │
│  (Vector DB)    │ ← ChromaDB
└─────────────────┘
    ↓
┌─────────────────┐
│   相关性过滤     │
│  (Filtering)    │
└─────────────────┘
    ↓
┌─────────────────┐
│   上下文增强     │
│  (Augmentation) │
└─────────────────┘
    ↓
┌─────────────────┐
│   LLM 生成      │
│  (Generation)   │ ← DeepSeek/OpenAI
└─────────────────┘
    ↓
用户回复
```

## 核心组件

### 1. 嵌入模块 (Embeddings Module)

**文件**: `backend/embeddings.py`

**功能**:
- 使用 Sentence-Transformers 生成文本嵌入
- 支持中英文双语
- 提供查询和文档编码接口

**主要类**:
```python
class EmbeddingModel:
    def encode(texts: Union[str, List[str]]) -> np.ndarray
    def encode_query(query: str) -> np.ndarray
    def encode_documents(documents: List[str]) -> np.ndarray
    def similarity(embedding1, embedding2) -> float
```

**使用的模型**:
- `paraphrase-multilingual-MiniLM-L12-v2`
- 支持 50+ 种语言
- 384 维向量
- 高效且准确

### 2. RAG 系统模块 (RAG System)

**文件**: `backend/rag_system.py`

**功能**:
- 管理向量数据库
- 实现语义检索
- 提供缓存机制
- 支持知识库扩展

**主要类**:
```python
class RAGSystem:
    def __init__(
        knowledge_base_path: str,
        use_vector_db: bool = True,
        similarity_threshold: float = 0.3,
        persist_directory: str = './chroma_db'
    )
    
    def search(query: str, top_k: int = 2) -> List[Dict]
    def format_context(search_results: List[Dict]) -> str
    def add_document(topic, content, keywords, examples)
    def clear_cache()
```

### 3. 知识库 (Knowledge Base)

**文件**: `backend/knowledge_base.json`

**结构**:
```json
{
  "主题名称": {
    "keywords": ["关键词列表"],
    "content": "专业建议内容",
    "examples": ["示例问答"]
  }
}
```

**当前主题** (13个):
1. 表白技巧
2. 吵架和解
3. 失恋疗愈
4. 异地恋维持
5. 恋爱沟通
6. 父母反对
7. 信任建立
8. 情绪管理
9. 约会技巧
10. 关系边界
11. 复合建议
12. 性与亲密
13. 婚姻准备

### 4. 向量数据库 (Vector Database)

**技术**: ChromaDB

**特点**:
- 轻量级，易于部署
- 支持本地持久化
- 快速的向量相似度搜索
- 支持元数据过滤

**存储位置**: `./chroma_db/`

## 安装配置

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

关键依赖：
- `chromadb==0.4.22` - 向量数据库
- `sentence-transformers==2.2.2` - 嵌入模型
- `numpy==1.24.3` - 数值计算

### 2. 首次运行

首次启动时，系统会自动：
1. 下载嵌入模型（约 120MB）
2. 创建向量数据库
3. 导入知识库内容
4. 生成文档嵌入

**预期输出**：
```
Loading embedding model: paraphrase-multilingual-MiniLM-L12-v2...
✅ Embedding model loaded successfully
✅ 知识库加载成功，包含 13 个主题
✅ 创建新的向量数据库
✅ 已导入 26 个文档到向量数据库
```

### 3. 环境变量配置

在 `.env` 文件中配置：

```bash
# RAG 基本配置
USE_RAG=true                    # 启用 RAG
RAG_TOP_K=2                     # 检索结果数量
RAG_SIMILARITY_THRESHOLD=0.3    # 相似度阈值

# API 配置
OPENAI_API_KEY=your_key_here
```

### 4. 存储空间要求

- 嵌入模型：~120MB
- ChromaDB 数据：~10MB（取决于知识库大小）
- 总计：~130MB

## 使用指南

### 基础使用

RAG 默认启用，无需额外配置：

```python
from counselor import EmotionalCounselor

counselor = EmotionalCounselor(api_key="your_key")
response = counselor.get_response("我和男朋友吵架了")
# RAG 会自动检索相关知识并增强回复
```

### API 调用

#### 使用默认 RAG 设置
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "异地恋太难了",
    "session_id": "test_session"
  }'
```

#### 临时禁用 RAG
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "你好",
    "session_id": "test_session",
    "use_rag": false
  }'
```

#### 临时启用 RAG（当默认禁用时）
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "如何处理失恋",
    "session_id": "test_session",
    "use_rag": true
  }'
```

### 程序化使用

```python
from rag_system import RAGSystem

# 初始化 RAG 系统
rag = RAGSystem(
    knowledge_base_path='knowledge_base.json',
    use_vector_db=True,
    similarity_threshold=0.3
)

# 搜索相关知识
results = rag.search("异地恋怎么维持", top_k=2)

# 格式化为上下文
context = rag.format_context(results)

# 添加新知识
rag.add_document(
    topic="新主题",
    content="专业建议内容",
    keywords=["关键词1", "关键词2"],
    examples=["示例1", "示例2"]
)
```

### 扩展知识库

#### 方法 1: 编辑 JSON 文件

编辑 `backend/knowledge_base.json`：

```json
{
  "你的新主题": {
    "keywords": ["相关", "关键词"],
    "content": "详细的专业建议内容...",
    "examples": [
      "问：示例问题？",
      "答：示例回答。"
    ]
  }
}
```

重启服务后自动加载。

#### 方法 2: 程序化添加

```python
rag.add_document(
    topic="职场恋情",
    content="职场恋情需要注意的事项：\n1. 保持专业...",
    keywords=["职场", "同事", "办公室恋情"],
    examples=["问：和同事谈恋爱需要注意什么？"]
)
```

## 性能优化

### 1. 缓存机制

RAG 系统内置了缓存机制：

```python
# 缓存会自动管理，最多存储 100 个查询结果
results = rag.search("query", use_cache=True)  # 默认启用

# 手动清空缓存
rag.clear_cache()
```

**缓存策略**：
- LRU (Least Recently Used) 淘汰策略
- 最多缓存 100 个查询
- 自动清理旧条目

### 2. 批量处理

处理多个文档时使用批量编码：

```python
# 高效：批量处理
documents = ["文档1", "文档2", "文档3"]
embeddings = embedding_model.encode_documents(documents)

# 低效：逐个处理
for doc in documents:
    embedding = embedding_model.encode_query(doc)
```

### 3. 相似度阈值调整

调整相似度阈值平衡精确度和召回率：

- **高阈值 (0.5-0.7)**: 更精确，但可能检索不到结果
- **中阈值 (0.3-0.5)**: 平衡精确度和召回率（推荐）
- **低阈值 (0.1-0.3)**: 更多结果，但相关性可能较低

### 4. Top-K 设置

控制返回结果数量：

```bash
# 环境变量
RAG_TOP_K=2  # 推荐：1-3

# API 参数（暂未实现，计划中）
# "rag_config": {"top_k": 3}
```

## 故障排查

### 问题 1: 模型下载失败

**症状**:
```
⚠️ Failed to load embedding model: ...
```

**解决方案**:
1. 检查网络连接
2. 手动下载模型：
   ```bash
   python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')"
   ```
3. 或配置镜像源（国内用户）

### 问题 2: ChromaDB 初始化失败

**症状**:
```
⚠️ 向量组件初始化失败: ...
💡 降级到关键词匹配模式
```

**解决方案**:
1. 检查磁盘空间
2. 确认写入权限
3. 删除 `chroma_db` 目录重新初始化：
   ```bash
   rm -rf backend/chroma_db
   ```

### 问题 3: 检索结果为空

**症状**:
检索不到相关知识

**解决方案**:
1. 降低相似度阈值：
   ```bash
   RAG_SIMILARITY_THRESHOLD=0.2
   ```
2. 增加 top_k 值：
   ```bash
   RAG_TOP_K=3
   ```
3. 检查知识库是否包含相关内容

### 问题 4: 内存占用过高

**症状**:
系统内存占用过大

**解决方案**:
1. 使用更小的嵌入模型
2. 减少缓存大小（修改代码中的 `100` 限制）
3. 定期清理缓存：
   ```python
   rag.clear_cache()
   ```

### 问题 5: 响应速度慢

**症状**:
首次查询响应慢

**原因**:
首次需要加载模型和生成嵌入

**解决方案**:
- 正常现象，后续查询会快速响应
- 利用缓存机制加速常见查询
- 考虑预热（启动时执行几次查询）

## API 参考

### 聊天接口

**端点**: `POST /api/chat`

**请求体**:
```json
{
  "message": "用户消息",
  "session_id": "会话ID",
  "use_rag": true  // 可选，覆盖默认设置
}
```

**响应**:
```json
{
  "message": "AI 回复",
  "emotion": "情绪标签",
  "session_id": "会话ID",
  "rag_enabled": true
}
```

### RAG 系统类

#### `RAGSystem.__init__`

```python
def __init__(
    self,
    knowledge_base_path: str = 'knowledge_base.json',
    use_vector_db: bool = True,
    similarity_threshold: float = 0.3,
    persist_directory: str = './chroma_db'
)
```

#### `RAGSystem.search`

```python
def search(
    self,
    query: str,
    top_k: int = 2,
    use_cache: bool = True
) -> List[Dict]
```

返回格式：
```python
[
    {
        'topic': '主题名称',
        'score': 0.85,  # 相似度分数
        'content': '专业内容',
        'examples': ['示例'],
        'keywords': ['关键词']
    }
]
```

#### `RAGSystem.add_document`

```python
def add_document(
    self,
    topic: str,
    content: str,
    keywords: List[str],
    examples: Optional[List[str]] = None
)
```

### 嵌入模型类

#### `EmbeddingModel.encode`

```python
def encode(
    self,
    texts: Union[str, List[str]],
    batch_size: int = 32
) -> np.ndarray
```

#### `EmbeddingModel.similarity`

```python
def similarity(
    self,
    embedding1: np.ndarray,
    embedding2: np.ndarray
) -> float
```

返回：余弦相似度分数 (-1 到 1)

## 最佳实践

1. **知识库设计**
   - 保持内容专业、准确
   - 使用清晰的结构和分段
   - 提供具体的示例
   - 定期更新和扩充

2. **关键词选择**
   - 包含同义词和变体
   - 考虑用户可能的表达方式
   - 避免过于宽泛的词汇

3. **相似度阈值**
   - 测试不同阈值的效果
   - 根据实际使用反馈调整
   - 考虑知识库大小和质量

4. **监控和维护**
   - 记录检索失败的查询
   - 分析用户反馈
   - 持续优化知识库内容

5. **安全考虑**
   - 确保知识库内容合规
   - 保护用户隐私
   - 避免存储敏感信息

## 未来改进

计划中的功能：
- [ ] 支持更多向量数据库（Pinecone, FAISS）
- [ ] 实现混合检索（向量 + 关键词）
- [ ] 添加重排序机制
- [ ] 支持多模态（图片、音频）
- [ ] 实现增量学习
- [ ] 添加 A/B 测试框架
- [ ] 提供 RAG 性能分析工具

## 参考资源

- [Sentence-Transformers 文档](https://www.sbert.net/)
- [ChromaDB 文档](https://docs.trychroma.com/)
- [RAG 论文](https://arxiv.org/abs/2005.11401)
- [向量检索最佳实践](https://www.pinecone.io/learn/vector-search/)
