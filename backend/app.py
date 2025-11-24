from flask import Flask, request, jsonify
from flask_cors import CORS
from counselor import EmotionalCounselor
from utils import validate_message, sanitize_input
from translator import TranslationService
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# 初始化咨询师
counselor = EmotionalCounselor(api_key=os.getenv('OPENAI_API_KEY'))

# 初始化翻译服务
translation_service = TranslationService()

# 存储会话（生产环境建议使用 Redis）
sessions = {}

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({'status': 'ok', 'message': 'Emotional Counseling AI is running'})

@app.route('/api/chat', methods=['POST'])
def chat():
    """处理聊天请求"""
    try:
        data = request.json
        
        # 验证输入
        if not validate_message(data):
            return jsonify({'error': '无效的请求格式'}), 400
        
        user_message = sanitize_input(data.get('message', ''))
        session_id = data.get('session_id', 'default')
        
        if not user_message:
            return jsonify({'error': '消息不能为空'}), 400
        
        # 获取或创建会话历史
        if session_id not in sessions:
            sessions[session_id] = []
        
        conversation_history = sessions[session_id]
        
        # 获取 AI 回复
        response = counselor.get_response(
            user_message=user_message,
            conversation_history=conversation_history
        )
        
        # 更新会话历史
        conversation_history.append({'role': 'user', 'content': user_message})
        conversation_history.append({'role': 'assistant', 'content': response['message']})
        
        # 限制历史记录长度
        if len(conversation_history) > 20:
            conversation_history = conversation_history[-20:]
        
        sessions[session_id] = conversation_history
        
        return jsonify({
            'message': response['message'],
            'emotion': response.get('emotion', 'neutral'),
            'session_id': session_id
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': '服务暂时不可用，请稍后重试'}), 500

@app.route('/api/session/new', methods=['POST'])
def new_session():
    """创建新会话"""
    import uuid
    session_id = str(uuid.uuid4())
    sessions[session_id] = []
    return jsonify({'session_id': session_id})

@app.route('/api/session/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    """删除会话"""
    if session_id in sessions:
        del sessions[session_id]
        return jsonify({'message': '会话已删除'})
    return jsonify({'error': '会话不存在'}), 404

@app.route('/api/translate', methods=['POST'])
def translate():
    """翻译文本"""
    try:
        data = request.json
        
        # 验证输入
        if not data or 'text' not in data:
            return jsonify({'error': '缺少文本参数'}), 400
        
        text = data.get('text', '').strip()
        target_lang = data.get('target_lang')  # 可选：'zh-cn' 或 'en'
        source_lang = data.get('source_lang')  # 可选：源语言
        
        if not text:
            return jsonify({'error': '文本不能为空'}), 400
        
        # 执行翻译
        result = translation_service.translate(
            text=text,
            target_lang=target_lang,
            source_lang=source_lang
        )
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Translation API error: {str(e)}")
        return jsonify({'error': '翻译服务暂时不可用'}), 500

@app.route('/api/translate/detect', methods=['POST'])
def detect_language():
    """检测文本语言"""
    try:
        data = request.json
        
        if not data or 'text' not in data:
            return jsonify({'error': '缺少文本参数'}), 400
        
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': '文本不能为空'}), 400
        
        detected_lang = translation_service.detect_language(text)
        
        return jsonify({
            'detected_language': detected_lang,
            'text': text
        })
        
    except Exception as e:
        print(f"Language detection API error: {str(e)}")
        return jsonify({'error': '语言检测服务暂时不可用'}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)