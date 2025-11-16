import json
import re
from typing import List, Dict, Tuple

class RAGSystem:
    """简单的 RAG 检索系统"""
    
    def __init__(self, knowledge_base_path='knowledge_base.json'):
        """初始化 RAG 系统"""
        try:
            with open(knowledge_base_path, 'r', encoding='utf-8') as f:
                self.knowledge_base = json.load(f)
            print(f"✅ 知识库加载成功，包含 {len(self.knowledge_base)} 个主题")
        except Exception as e:
            print(f"⚠️ 知识库加载失败: {str(e)}")
            self.knowledge_base = {}
    
    def search(self, query: str, top_k: int = 2) -> List[Dict]:
        """
        搜索相关知识
        
        Args:
            query: 用户查询
            top_k: 返回前 k 个结果
            
        Returns:
            相关知识列表
        """
        results = []
        query_lower = query.lower()
        
        for topic, data in self.knowledge_base.items():
            score = self._calculate_score(query_lower, data['keywords'])
            if score > 0:
                results.append({
                    'topic': topic,
                    'score': score,
                    'content': data['content'],
                    'examples': data.get('examples', [])
                })
        
        # 按分数排序
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return results[:top_k]
    
    def _calculate_score(self, query: str, keywords: List[str]) -> float:
        """计算查询和关键词的匹配分数"""
        score = 0
        for keyword in keywords:
            if keyword in query:
                score += 1
        return score
    
    def format_context(self, search_results: List[Dict]) -> str:
        """格式化检索结果为上下文"""
        if not search_results:
            return ""
        
        context = "以下是相关的专业知识，请参考：\n\n"
        for i, result in enumerate(search_results, 1):
            context += f"【{result['topic']}】\n{result['content']}\n\n"
        
        return context