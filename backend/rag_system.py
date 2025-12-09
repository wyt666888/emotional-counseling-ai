import json
import os
from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings
from embeddings import EmbeddingModel


class RAGSystem:
    """
    Enhanced RAG (Retrieval-Augmented Generation) system using vector embeddings.
    Supports semantic search over emotional counseling knowledge base.
    """
    
    def __init__(
        self, 
        knowledge_base_path: str = 'knowledge_base.json',
        use_vector_db: bool = True,
        similarity_threshold: float = 0.3,
        persist_directory: str = './chroma_db'
    ):
        """
        Initialize RAG system with vector database support.
        
        Args:
            knowledge_base_path: Path to knowledge base JSON file
            use_vector_db: Whether to use vector database (ChromaDB) for retrieval
            similarity_threshold: Minimum similarity score for results (0-1)
            persist_directory: Directory to persist ChromaDB data
        """
        self.knowledge_base_path = knowledge_base_path
        self.use_vector_db = use_vector_db
        self.similarity_threshold = similarity_threshold
        self.persist_directory = persist_directory
        
        # Load knowledge base
        self.knowledge_base = self._load_knowledge_base()
        
        # Initialize vector components if enabled
        self.embedding_model = None
        self.chroma_client = None
        self.collection = None
        self._cache = {}  # Simple cache for frequently retrieved contexts
        
        if self.use_vector_db:
            self._initialize_vector_components()
    
    def _load_knowledge_base(self) -> Dict:
        """Load knowledge base from JSON file"""
        try:
            with open(self.knowledge_base_path, 'r', encoding='utf-8') as f:
                kb = json.load(f)
            print(f"✅ 知识库加载成功，包含 {len(kb)} 个主题")
            return kb
        except Exception as e:
            print(f"⚠️ 知识库加载失败: {str(e)}")
            return {}
    
    def _initialize_vector_components(self):
        """Initialize embedding model and vector database"""
        try:
            # Initialize embedding model
            self.embedding_model = EmbeddingModel()
            
            # Initialize ChromaDB client
            self.chroma_client = chromadb.Client(Settings(
                persist_directory=self.persist_directory,
                anonymized_telemetry=False
            ))
            
            # Get or create collection
            collection_name = "counseling_knowledge"
            try:
                self.collection = self.chroma_client.get_collection(name=collection_name)
                print(f"✅ 使用现有向量数据库，文档数: {self.collection.count()}")
            except:
                self.collection = self.chroma_client.create_collection(
                    name=collection_name,
                    metadata={"description": "Emotional counseling knowledge base"}
                )
                print("✅ 创建新的向量数据库")
                # Ingest knowledge base into vector database
                self._ingest_knowledge_base()
                
        except Exception as e:
            print(f"⚠️ 向量组件初始化失败: {str(e)}")
            print("💡 降级到关键词匹配模式")
            self.use_vector_db = False
    
    def _ingest_knowledge_base(self):
        """Ingest knowledge base documents into vector database"""
        if not self.collection or not self.knowledge_base:
            return
        
        documents = []
        metadatas = []
        ids = []
        
        for topic, data in self.knowledge_base.items():
            # Main content as a document
            doc_id = f"topic_{topic}"
            documents.append(data['content'])
            metadatas.append({
                'topic': topic,
                'type': 'content',
                'keywords': ','.join(data.get('keywords', []))
            })
            ids.append(doc_id)
            
            # Add examples as separate documents if available
            for idx, example in enumerate(data.get('examples', [])):
                ex_doc_id = f"topic_{topic}_example_{idx}"
                documents.append(example)
                metadatas.append({
                    'topic': topic,
                    'type': 'example',
                    'keywords': ','.join(data.get('keywords', []))
                })
                ids.append(ex_doc_id)
        
        try:
            # Generate embeddings and add to collection
            embeddings = self.embedding_model.encode_documents(documents)
            
            self.collection.add(
                embeddings=embeddings.tolist(),
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            print(f"✅ 已导入 {len(documents)} 个文档到向量数据库")
        except Exception as e:
            print(f"⚠️ 文档导入失败: {str(e)}")
    
    def search(self, query: str, top_k: int = 2, use_cache: bool = True) -> List[Dict]:
        """
        Search for relevant knowledge based on query.
        
        Args:
            query: User query text
            top_k: Number of top results to return
            use_cache: Whether to use cached results
            
        Returns:
            List of relevant knowledge items with scores
        """
        # Check cache first
        cache_key = f"{query}_{top_k}"
        if use_cache and cache_key in self._cache:
            return self._cache[cache_key]
        
        # Perform search based on mode
        if self.use_vector_db and self.collection:
            results = self._vector_search(query, top_k)
        else:
            results = self._keyword_search(query, top_k)
        
        # Cache results
        if use_cache and len(results) > 0:
            self._cache[cache_key] = results
            # Limit cache size
            if len(self._cache) > 100:
                # Remove oldest entries
                keys = list(self._cache.keys())
                for key in keys[:20]:
                    del self._cache[key]
        
        return results
    
    def _vector_search(self, query: str, top_k: int) -> List[Dict]:
        """Perform semantic search using vector embeddings"""
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode_query(query)
            
            # Query vector database
            results = self.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=min(top_k * 2, 10)  # Get more results for filtering
            )
            
            # Process and filter results
            processed_results = []
            seen_topics = set()
            
            if results['documents'] and len(results['documents']) > 0:
                for i in range(len(results['documents'][0])):
                    distance = results['distances'][0][i] if results['distances'] else 0
                    # Convert distance to similarity (1 - distance for cosine)
                    similarity = 1 - distance
                    
                    # Filter by similarity threshold
                    if similarity < self.similarity_threshold:
                        continue
                    
                    metadata = results['metadatas'][0][i]
                    topic = metadata['topic']
                    
                    # Avoid duplicate topics in results
                    if topic in seen_topics:
                        continue
                    seen_topics.add(topic)
                    
                    # Get full topic data
                    if topic in self.knowledge_base:
                        topic_data = self.knowledge_base[topic]
                        processed_results.append({
                            'topic': topic,
                            'score': similarity,
                            'content': topic_data['content'],
                            'examples': topic_data.get('examples', []),
                            'keywords': topic_data.get('keywords', [])
                        })
                    
                    if len(processed_results) >= top_k:
                        break
            
            return processed_results
            
        except Exception as e:
            print(f"⚠️ 向量检索失败: {str(e)}")
            # Fallback to keyword search
            return self._keyword_search(query, top_k)
    
    def _keyword_search(self, query: str, top_k: int) -> List[Dict]:
        """Fallback keyword-based search"""
        results = []
        query_lower = query.lower()
        
        for topic, data in self.knowledge_base.items():
            score = self._calculate_keyword_score(query_lower, data['keywords'])
            if score > 0:
                results.append({
                    'topic': topic,
                    'score': score,
                    'content': data['content'],
                    'examples': data.get('examples', []),
                    'keywords': data.get('keywords', [])
                })
        
        # Sort by score
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]
    
    def _calculate_keyword_score(self, query: str, keywords: List[str]) -> float:
        """Calculate keyword match score"""
        score = 0
        for keyword in keywords:
            if keyword in query:
                score += 1
        return score
    
    def format_context(self, search_results: List[Dict]) -> str:
        """
        Format search results into context string for LLM.
        
        Args:
            search_results: List of search result dictionaries
            
        Returns:
            Formatted context string
        """
        if not search_results:
            return ""
        
        context = "以下是相关的专业知识，请参考：\n\n"
        for result in search_results:
            score_str = f"(相关度: {result['score']:.2f})" if result['score'] < 1 else ""
            context += f"【{result['topic']}】{score_str}\n{result['content']}\n\n"
        
        return context
    
    def add_document(self, topic: str, content: str, keywords: List[str], 
                    examples: Optional[List[str]] = None):
        """
        Add a new document to the knowledge base.
        
        Args:
            topic: Topic name/identifier
            content: Document content
            keywords: List of keywords for the topic
            examples: Optional list of example Q&As
        """
        # Add to in-memory knowledge base
        self.knowledge_base[topic] = {
            'content': content,
            'keywords': keywords,
            'examples': examples or []
        }
        
        # Add to vector database if enabled
        if self.use_vector_db and self.collection:
            try:
                doc_id = f"topic_{topic}"
                embedding = self.embedding_model.encode_documents([content])
                
                self.collection.add(
                    embeddings=[embedding[0].tolist()],
                    documents=[content],
                    metadatas=[{
                        'topic': topic,
                        'type': 'content',
                        'keywords': ','.join(keywords)
                    }],
                    ids=[doc_id]
                )
                print(f"✅ 已添加新文档: {topic}")
            except Exception as e:
                print(f"⚠️ 添加文档到向量数据库失败: {str(e)}")
        
        # Clear cache to include new document
        self._cache.clear()
    
    def clear_cache(self):
        """Clear the retrieval cache"""
        self._cache.clear()
        print("✅ 检索缓存已清空")