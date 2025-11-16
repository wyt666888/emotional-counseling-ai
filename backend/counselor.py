import os
import openai
from prompts import SYSTEM_PROMPT, EMOTION_KEYWORDS
from rag_system import RAGSystem
import re

class EmotionalCounselor:
    """恋爱情绪咨询 AI 核心类"""
    
    def __init__(self, api_key, model="deepseek-chat"):
        self.api_key = api_key
        self.model = model
        openai.api_key = api_key
        
        # 配置 DeepSeek API
        openai.api_base = "https://api.deepseek.com/v1"
        
        # 初始化 RAG 系统
        self.rag = RAGSystem()
        
        if api_key and api_key != "your_openai_api_key_here":
            print(f"✅ API Key configured: {api_key[:20]}...")
            print(f"✅ Using model: {model}")
        else:
            print("⚠️ 未配置 API Key，将使用演示模式")
    
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
        
        # 如果没有 API Key，使用演示模式
        if not self.api_key or self.api_key == "your_openai_api_key_here":
            print("💡 使用演示模式回复")
            return self._get_demo_response(user_message, detected_emotion)
        
        # 使用 RAG 检索相关知识
        rag_results = self.rag.search(user_message, top_k=2)
        rag_context = self.rag.format_context(rag_results)
        
        if rag_context:
            print(f"💡 找到 {len(rag_results)} 条相关知识")
        
        # 构建增强后的系统提示词
        enhanced_prompt = SYSTEM_PROMPT
        if rag_context:
            enhanced_prompt += f"\n\n{rag_context}\n请基于以上专业知识，结合用户的具体情况给出建议。"
        
        # 构建消息
        messages = [
            {"role": "system", "content": enhanced_prompt}
        ]
        
        # 添加历史对话（最近10轮）
        messages.extend(conversation_history[-10:])
        
        # 添加当前用户消息
        messages.append({"role": "user", "content": user_message})
        
        try:
            # 调用 DeepSeek API
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
            print(f"⚠️ DeepSeek API Error: {str(e)}")
            print("💡 自动降级到演示模式")
            # API 失败时自动降级到演示模式
            return self._get_demo_response(user_message, detected_emotion)
    
    def _get_demo_response(self, user_message, emotion):
        """演示模式的智能回复"""
        message_lower = user_message.lower()
        
        # 根据关键词匹配回复
        if any(word in message_lower for word in ['表白', '喜欢', '告白', '追', '心动', '暗恋']):
            response = """我理解你现在的心情 💙 喜欢一个人是美好的，同时也会让人感到紧张和不知所措。

关于表白，我想给你一些建议：

1️⃣ **了解对方的感受**：在表白前，可以先观察对方对你的态度，是否也对你有好感的信号。

2️⃣ **选择合适的时机**：找一个轻松、私密的环境，让对方感到舒适和尊重。

3️⃣ **真诚地表达**：不需要华丽的辞藻，真诚地说出你的感受就好，比如"我很喜欢和你在一起的时光，你愿意给我一个机会吗？"

4️⃣ **做好心理准备**：无论结果如何，都要尊重对方的选择。如果对方暂时没有准备好，也不要气馁。

记住，表白的勇气本身就很珍贵 🌸 你想聊聊具体的情况吗？"""
        
        elif any(word in message_lower for word in ['吵架', '争吵', '矛盾', '冷战', '不理我', '生气']):
            response = """我能感受到你现在的难过和焦虑 💙 情侣之间的争执是很常见的，但确实会让人感到不安。

让我们一起来分析和解决：

1️⃣ **冷静下来**：给彼此一些时间和空间冷静，避免情绪化的进一步冲突。

2️⃣ **主动沟通**：等情绪平复后，可以主动找她聊聊。可以说"我们能谈谈吗？我想解决我们之间的问题。"

3️⃣ **倾听对方**：认真听她的感受和想法，不要急于辩解。让她知道你在意她的感受。

4️⃣ **诚恳道歉**：如果确实是你的错，真诚地道歉。如果是误会，耐心解释。

5️⃣ **寻找解决方案**：一起讨论如何避免类似的问题再次发生。

关系中的冲突不可怕，关键是如何处理 🌸 你想聊聊具体发生了什么吗？"""
        
        elif any(word in message_lower for word in ['分手', '失恋', '分开', '走不出', '放不下', '忘不了']):
            response = """我真的很理解你现在的痛苦 💙 失恋是人生中最难熬的经历之一，你的感受完全正常。

请记住这些：

1️⃣ **允许自己悲伤**：不要压抑情绪，哭出来、找朋友倾诉都可以。这是疗愈的必经过程。

2️⃣ **给自己时间**：走出失恋需要时间，不要急于强迫自己"放下"，慢慢来就好。

3️⃣ **照顾好自己**：保持规律作息，做一些让自己开心的事情，比如运动、旅行、学习新技能。

4️⃣ **减少联系**：暂时不要频繁查看对方的社交媒体，给自己空间去疗愈。

5️⃣ **成长和反思**：这段经历会让你更了解自己，也会让未来的你更成熟。

你不是一个人在战斗，我陪着你 🌸 想聊聊你的感受吗？"""
        
        elif any(word in message_lower for word in ['异地', '异地恋', '见不到', '距离', '想念']):
            response = """异地恋确实不容易 💙 距离会带来很多挑战，但也能考验和加深感情。

一些维持异地恋的建议：

1️⃣ **保持沟通**：定期视频通话，分享日常的点滴，让对方参与你的生活。

2️⃣ **制定见面计划**：有明确的见面时间，会让等待更有盼头。

3️⃣ **培养共同爱好**：可以一起看同一部剧、玩游戏，创造共同话题。

4️⃣ **相互信任**：信任是异地恋的基石，给彼此足够的安全感。

5️⃣ **规划未来**：聊聊你们对未来的规划，让彼此知道这份坚持是有方向的。

如果真的觉得太累，也可以重新评估这段关系是否适合继续 🌸 你最近遇到什么困难了吗？"""
        
        elif any(word in message_lower for word in ['困惑', '不知道', '迷茫', '纠结', '矛盾', '犹豫']):
            response = """我能感受到你的迷茫 💭 感情中的困惑是很正常的，说明你在认真思考这段关系。

让我们一起梳理：

1️⃣ **明确你的感受**：你现在最困扰你的是什么？是对对方的感情不确定，还是关系的方向不清晰？

2️⃣ **倾听内心**：问问自己，这段关系让你快乐多还是焦虑多？你期待的是什么？

3️⃣ **沟通很重要**：可以和对方聊聊你的感受和困惑，听听对方的想法。

4️⃣ **给自己时间**：不要急于做决定，可以再观察一段时间。

有时候，把困惑说出来，答案就会慢慢清晰 🌸 你能具体说说你在纠结什么吗？"""
        
        elif any(word in message_lower for word in ['父母', '家人', '反对', '门当户对', '家庭']):
            response = """我理解你面对的压力 💙 来自家人的反对确实会让人感到为难。

一些应对建议：

1️⃣ **理解父母的担心**：他们的反对往往出于对你的关心，试着理解他们的顾虑。

2️⃣ **展示你们的感情**：用行动证明你们的感情是认真的，让家人看到对方的优点。

3️⃣ **耐心沟通**：找合适的时机和父母深入交流，表达你的想法和决心。

4️⃣ **寻求支持**：可以请亲戚朋友帮忙说服，或者让对方主动表现。

5️⃣ **理性评估**：同时也要客观看待父母的意见，有些担忧可能确实值得考虑。

感情和家庭都重要，需要找到平衡点 🌸 具体是什么让家人反对呢？"""
        
        elif any(word in message_lower for word in ['第一次', '初恋', '经验', '不懂']):
            response = """初恋是很美好的经历 💕 没有经验是完全正常的，每个人都是从第一次开始的。

给你一些建议：

1️⃣ **自然相处**：不要过度紧张，保持自己的真实，自然的相处最舒服。

2️⃣ **尊重对方**：注意对方的感受和边界，相互尊重是基础。

3️⃣ **多交流**：有什么想法和感受可以大方说出来，良好的沟通很重要。

4️⃣ **学习成长**：可以多观察、多学习，但不要刻意模仿别人。

5️⃣ **享受过程**：恋爱是美好的体验，放松心情，享受这个过程。

初恋的青涩和美好就在于它的纯真 🌸 有什么具体的困惑吗？"""
        
        else:
            # 默认回复
            response = f"""你好呀，我是心语 💙

我听到你的声音了。无论你现在面对什么样的感情困扰，请记住：

✨ **你的感受是重要的**：不要忽视自己的情绪，它们在告诉你一些重要的信息。

💭 **沟通是关键**：很多问题都可以通过坦诚的沟通来解决。

🌸 **爱自己很重要**：无论是否在恋爱中，首先要学会爱自己、照顾好自己。

你能更具体地说说你的情况吗？我会根据你的情况给出更具体的建议 🌟"""
        
        return {
            'message': response,
            'emotion': emotion,
            'mode': 'demo'
        }