import openai
from prompts import SYSTEM_PROMPT, EMOTION_KEYWORDS
import re

class EmotionalCounselor:
    """恋爱情绪咨询 AI 核心类"""
    
    def __init__(self, api_key, model="gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        openai.api_key = api_key
    
    def detect_emotion(self, message):
        """检测用户情绪"""
        message_lower = message.lower()
        
        for emotion, keywords in EMOTION_KEYWORDS.items():
            for keyword in keywords:
                if keyword in message_lower:
                    return emotion
        
        return 'neutral'
    
    def get_response(self, user_message, conversation_history=None):
        """
        获取 AI 回复
        
        Args:
            user_message: 用户消息
            conversation_history: 对话历史
            
        Returns:
            dict: 包含回复消息和情绪分析
        """
        if conversation_history is None:
            conversation_history = []
        
        # 检测情绪
        detected_emotion = self.detect_emotion(user_message)
        
        # 构建消息
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
        
        # 添加历史对话（最近10轮）
        messages.extend(conversation_history[-10:])
        
        # 添加当前用户消息
        messages.append({"role": "user", "content": user_message})
        
        try:
            # 调用 OpenAI API
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500,
                top_p=0.9,
                frequency_penalty=0.3,
                presence_penalty=0.3
            )
            
            ai_message = response.choices[0].message.content.strip()
            
            return {
                'message': ai_message,
                'emotion': detected_emotion,
                'tokens_used': response.usage.total_tokens
            }
            
        except Exception as e:
            print(f"OpenAI API Error: {str(e)}")
            return {
                'message': '抱歉，我现在遇到了一些技术问题。请稍后再试，或者你可以换个方式描述你的困扰。',
                'emotion': detected_emotion,
                'error': str(e)
            }