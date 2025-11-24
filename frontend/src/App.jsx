import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Heart, Send, RefreshCw, Languages } from 'lucide-react';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState('default');
  const [translationEnabled, setTranslationEnabled] = useState(false);
  const [targetLanguage, setTargetLanguage] = useState('auto'); // 'auto', 'zh-CN', 'en'
  const [translatedMessages, setTranslatedMessages] = useState({}); // Store translations by message index
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // 初始欢迎消息
    setMessages([
      {
        role: 'assistant',
        content: '你好呀！我是心语，你的情感咨询助手 💙\n\n无论是恋爱中的困惑、关系里的矛盾，还是分手后的疗愈，我都在这里陪伴你、倾听你。\n\n请放心分享你的感受，这里是安全的空间。你想聊些什么呢？',
      },
    ]);
  }, []);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = {
      role: 'user',
      content: inputMessage,
    };

    setMessages((prev) => {
      const newMessages = [...prev, userMessage];
      // Translate user message if translation is enabled
      if (translationEnabled) {
        const newIndex = newMessages.length - 1;
        translateMessage(userMessage.content, newIndex);
      }
      return newMessages;
    });
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await axios.post('/api/chat', {
        message: inputMessage,
        session_id: sessionId,
      });

      const assistantMessage = {
        role: 'assistant',
        content: response.data.message,
        emotion: response.data.emotion,
      };

      setMessages((prev) => {
        const newMessages = [...prev, assistantMessage];
        // Translate new messages if translation is enabled
        if (translationEnabled) {
          const newIndex = newMessages.length - 1;
          translateMessage(assistantMessage.content, newIndex);
        }
        return newMessages;
      });
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: '抱歉，我现在遇到了一些技术问题 😔 请稍后再试。',
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewSession = async () => {
    try {
      const response = await axios.post('/api/session/new');
      setSessionId(response.data.session_id);
      setMessages([
        {
          role: 'assistant',
          content: '新的对话开始了 🌸 有什么想聊的吗？',
        },
      ]);
      setTranslatedMessages({});
    } catch (error) {
      console.error('Error creating new session:', error);
    }
  };

  const translateMessage = async (text, index) => {
    try {
      const response = await axios.post('/api/translate', {
        text,
        target_lang: targetLanguage === 'auto' ? null : targetLanguage,
      });

      if (response.data.translated_text) {
        setTranslatedMessages((prev) => ({
          ...prev,
          [index]: {
            translatedText: response.data.translated_text,
            sourceLang: response.data.source_lang,
            targetLang: response.data.target_lang,
          },
        }));
      }
    } catch (error) {
      console.error('Error translating message:', error);
    }
  };

  const handleToggleTranslation = () => {
    setTranslationEnabled(!translationEnabled);
    if (!translationEnabled) {
      // When enabling translation, translate messages in batches to avoid rate limiting
      // Translate in batches of 3 messages at a time with 500ms delay between batches
      const batchSize = 3;
      const delay = 500;
      
      for (let i = 0; i < messages.length; i += batchSize) {
        const batch = messages.slice(i, i + batchSize);
        setTimeout(() => {
          batch.forEach((msg, batchIndex) => {
            const actualIndex = i + batchIndex;
            if (!translatedMessages[actualIndex]) {
              translateMessage(msg.content, actualIndex);
            }
          });
        }, (i / batchSize) * delay);
      }
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 via-purple-50 to-blue-50">
      {/* Header */}
      <header className="bg-white shadow-md">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Heart className="text-primary" size={32} fill="currentColor" />
            <div>
              <h1 className="text-2xl font-bold text-gray-800">心语咨询室</h1>
              <p className="text-sm text-gray-500">专业恋爱情绪咨询 AI</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            {/* Translation Controls */}
            <div className="flex items-center gap-2">
              <button
                onClick={handleToggleTranslation}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg transition ${
                  translationEnabled
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
                title="Toggle translation"
              >
                <Languages size={18} />
                <span className="text-sm">
                  {translationEnabled ? '翻译中' : '翻译'}
                </span>
              </button>
              {translationEnabled && (
                <select
                  value={targetLanguage}
                  onChange={(e) => {
                    setTargetLanguage(e.target.value);
                    setTranslatedMessages({});
                  }}
                  className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary"
                >
                  <option value="auto">自动检测</option>
                  <option value="zh-CN">中文</option>
                  <option value="en">English</option>
                </select>
              )}
            </div>
            <button
              onClick={handleNewSession}
              className="flex items-center gap-2 px-4 py-2 bg-primary text-white rounded-lg hover:bg-secondary transition"
            >
              <RefreshCw size={18} />
              <span>新对话</span>
            </button>
          </div>
        </div>
      </header>

      {/* Chat Container */}
      <main className="max-w-4xl mx-auto px-4 py-6">
        <div className="bg-white rounded-2xl shadow-xl h-[calc(100vh-200px)] flex flex-col">
          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {messages.map((message, index) => {
              const translation = translatedMessages[index];
              const showTranslation = translationEnabled && translation;

              return (
                <div
                  key={index}
                  className={`message-animation flex ${
                    message.role === 'user' ? 'justify-end' : 'justify-start'
                  }`}
                >
                  <div
                    className={`max-w-[75%] rounded-2xl px-5 py-3 ${
                      message.role === 'user'
                        ? 'bg-primary text-white'
                        : 'bg-gray-100 text-gray-800'
                    }`}
                  >
                    <p className="whitespace-pre-wrap leading-relaxed">
                      {message.content}
                    </p>
                    {showTranslation && !translation.skipped && (
                      <div
                        className={`mt-2 pt-2 border-t ${
                          message.role === 'user'
                            ? 'border-blue-300'
                            : 'border-gray-300'
                        }`}
                      >
                        <p
                          className={`text-sm ${
                            message.role === 'user'
                              ? 'text-blue-100'
                              : 'text-gray-600'
                          } italic`}
                        >
                          {translation.translatedText}
                        </p>
                        <p
                          className={`text-xs mt-1 ${
                            message.role === 'user'
                              ? 'text-blue-200'
                              : 'text-gray-400'
                          }`}
                        >
                          {translation.sourceLang} → {translation.targetLang}
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-gray-100 rounded-2xl px-5 py-3">
                  <div className="flex gap-2">
                    <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></span>
                    <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100"></span>
                    <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200"></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="border-t p-4">
            <div className="flex gap-3">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                placeholder="分享你的感受..."
                className="flex-1 px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
                disabled={isLoading}
              />
              <button
                onClick={handleSendMessage}
                disabled={isLoading || !inputMessage.trim()}
                className="px-6 py-3 bg-primary text-white rounded-xl hover:bg-secondary transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
              >
                <Send size={20} />
                <span>发送</span>
              </button>
            </div>
            <p className="text-xs text-gray-400 mt-2 text-center">
              本 AI 助手仅供情感支持参考，不能替代专业心理咨询
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;