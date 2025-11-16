import re
import html

def validate_message(data):
    """验证消息格式"""
    if not isinstance(data, dict):
        return False
    if 'message' not in data:
        return False
    return True

def sanitize_input(text):
    """清理用户输入"""
    if not text:
        return ""
    
    # HTML 转义
    text = html.escape(text)
    
    # 移除多余空白
    text = re.sub(r'\s+', ' ', text).strip()
    
    # 限制长度
    max_length = 1000
    if len(text) > max_length:
        text = text[:max_length]
    
    return text

def detect_crisis(message):
    """检测危机关键词"""
    from prompts import CRISIS_KEYWORDS
    
    message_lower = message.lower()
    for keyword in CRISIS_KEYWORDS:
        if keyword in message_lower:
            return True
    return False

def get_crisis_response():
    """返回危机干预回复"""
    return """我注意到你现在可能正在经历非常艰难的时刻，我很担心你。💙

🆘 **请立即寻求专业帮助**：
- 24小时心理危机热线：400-161-9995
- 生命热线：400-821-1215
- 或拨打当地急救电话：120

你的生命很宝贵，现在的痛苦是暂时的。专业的心理咨询师可以提供更好的帮助。

如果方便，也请联系你信任的家人或朋友。你不是一个人在面对这些。"""