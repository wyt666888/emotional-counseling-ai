# 💖 Emotional Counseling AI - 恋爱情绪咨询 AI

一个专业的恋爱情绪咨询 AI 助手，提供温暖、专业的情感支持和建议。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/react-18.2+-61DAFB.svg)](https://reactjs.org/)

## ✨ 功能特点

- 🤝 **共情倾听**：理解用户的情感困扰，提供温暖的支持
- 💡 **专业建议**：基于心理学原理，提供实用的恋爱建议
- 🔒 **隐私保护**：所有对话内容安全加密，保护用户隐私
- 🎯 **个性化**：根据用户情况提供定制化的咨询方案
- 📊 **情绪分析**：智能识别用户情绪状态
- 🆘 **危机干预**：自动识别危机关键词并提供紧急帮助
- 🌐 **中英翻译**：支持中英文实时翻译，自动语言检测，打破语言障碍
- 🧠 **RAG 增强**：使用检索增强生成技术，提供更准确、更专业的咨询建议

## 🚀 快速开始

### 环境要求

- Node.js >= 18.0.0
- Python >= 3.9
- OpenAI API Key
- **翻译功能要求**：
  - 稳定的互联网连接（用于访问 Google Translate）
  - 无需额外的 API Key（使用 deep-translator 免费服务）
  - 中国大陆用户可能需要配置网络代理

### 安装步骤

1. **克隆仓库**
```bash
git clone https://github.com/wyt666888/emotional-counseling-ai.git
cd emotional-counseling-ai
```

2. **配置后端**
```bash
cd backend
pip install -r requirements.txt  # 会自动安装 deep-translator 等所有依赖
cp .env.example .env
# 编辑 .env 文件，填入你的 OPENAI_API_KEY

# （可选）如果需要配置代理访问 Google Translate，可在 .env 中添加：
# HTTP_PROXY=http://your-proxy:port
# HTTPS_PROXY=https://your-proxy:port
```

> 💡 **提示**：`requirements.txt` 已包含 `deep-translator`，无需单独安装

3. **启动后端**
```bash
python app.py
```

4. **配置前端**（新终端）
```bash
cd frontend
npm install
```

5. **启动前端**
```bash
npm run dev
```

6. **开始使用**
打开浏览器访问 `http://localhost:3000`

### 🪟 Windows 一键启动

Windows 用户可以使用一键启动脚本，自动完成所有启动步骤：

#### 首次使用准备

1. 确保已安装 [Python 3.9+](https://www.python.org/downloads/) 和 [Node.js 18+](https://nodejs.org/)
2. 配置后端环境变量：
   ```bash
   cd backend
   pip install -r requirements.txt
   copy .env.example .env
   # 编辑 .env 文件，填入你的 OPENAI_API_KEY
   ```

#### 启动服务

双击运行项目根目录下的 `start.bat`，脚本将自动：
- ✅ 检查 Python 和 Node.js 环境
- ✅ 安装前端依赖（首次运行时）
- ✅ 启动后端 Flask 服务（端口 5000）
- ✅ 启动前端 Vite 开发服务器（智能检测端口）
- ✅ 自动打开浏览器访问应用（正确的端口）

> 💡 **注意**：如果端口 3000 被占用，Vite 会自动切换到 3001 或其他可用端口，启动脚本会自动检测实际使用的端口。

#### 停止服务

双击运行 `stop.bat`，脚本将：
- 🛑 关闭后端 Python 服务（端口 5000）
- 🛑 关闭前端 Node.js 服务（端口 3000/3001/3002/5173）
- 🧹 清理端口占用

> 💡 **提示**：也可以直接关闭服务窗口来停止对应的服务

#### 手动启动

**后端：**
```cmd
cd backend
python app.py
```

**前端：**
```cmd
cd frontend
npm install  # 首次运行
npm run dev
```

#### 故障排除

如果自动启动失败：
1. 检查 Python 和 Node.js 是否正确安装
2. 查看服务窗口的错误信息
3. 尝试使用 `start-simple.bat` 手动启动
4. 前端实际端口请查看 Frontend 窗口输出

## 📁 项目结构

```
emotional-counseling-ai/
├── README.md
├── LICENSE
├── backend/                # Python/Flask 后端
│   ├── app.py
│   ├── counselor.py
│   ├── prompts.py
│   ├── utils.py
│   ├── translator.py       # 翻译服务模块
│   ├── requirements.txt
│   └── .env.example
├── frontend/              # React 前端
│   ├── src/
│   ├── package.json
│   └── vite.config.js
└── docs/
    ├── API.md              # API 文档
    └── TRANSLATION_FEATURE.md  # 翻译功能详细文档
```

## 🌐 翻译功能

### 功能特性
- **自动语言检测**：智能识别输入文本是中文还是英文
- **实时翻译**：对话消息即时翻译显示
- **双向翻译**：支持中文⇄英文互译
- **手动选择**：可手动指定目标语言（自动/中文/英文）
- **优雅显示**：原文和译文同时展示，便于对照
- **批量翻译**：优化性能，支持历史消息批量翻译
- **免费无限制**：使用 Google Translate，无需 API Key

### 使用方法
1. 点击界面右上角的 "翻译" 按钮启用翻译功能
2. 选择目标语言（默认为自动检测）
3. 发送消息后会自动显示翻译
4. 启用翻译功能后，历史消息也会被翻译

### 配置说明

#### 依赖安装
翻译功能使用 `deep-translator` 库，已包含在 `requirements.txt` 中：
```bash
# 自动安装（推荐）
pip install -r requirements.txt

# 或单独安装
pip install deep-translator
```

#### 网络要求
- ✅ **免费服务**：无需申请 API Key
- ✅ **简单配置**：开箱即用
- ⚠️ **网络连接**：需要能够访问 Google Translate 服务
- ⚠️ **中国大陆用户**：如无法访问，可在 `.env` 中配置代理

#### 代理配置（可选）
如果需要通过代理访问 Google Translate，在 `.env` 文件中添加：
```bash
HTTP_PROXY=http://your-proxy:port
HTTPS_PROXY=https://your-proxy:port
```

### 测试翻译功能

```bash
# 测试后端翻译服务
cd backend
python -c "
from translator import TranslationService
service = TranslationService()

# 测试语言检测
print('中文检测:', service.detect_language('你好世界'))  # 应输出: zh-CN
print('英文检测:', service.detect_language('Hello World'))  # 应输出: en

# 测试翻译
result = service.translate('我很开心')
print('翻译结果:', result['translated_text'])  # 应输出英文翻译
"
```

### API 使用
详见 [API文档](docs/API.md) 中的翻译接口说明。

完整的翻译功能文档请查看 [TRANSLATION_FEATURE.md](docs/TRANSLATION_FEATURE.md)

## 🧠 RAG (检索增强生成) 功能

### 什么是 RAG？
RAG (Retrieval-Augmented Generation) 是一种结合信息检索和生成式 AI 的技术，通过从知识库中检索相关信息来增强 AI 的回复质量。

### 功能特性
- **语义搜索**：使用向量嵌入实现智能语义匹配，而非简单的关键词匹配
- **专业知识库**：包含情感咨询、恋爱技巧、心理学原理等专业内容
- **动态检索**：根据用户问题动态检索最相关的咨询知识
- **上下文增强**：将检索到的专业知识融入 AI 回复，提供更准确的建议
- **缓存优化**：对频繁检索的内容进行缓存，提升响应速度

### 技术实现
- **向量数据库**：使用 ChromaDB 存储和检索文档向量
- **嵌入模型**：使用 Sentence-Transformers 生成多语言嵌入
- **相似度计算**：基于余弦相似度进行语义匹配

### 配置说明

RAG 功能通过环境变量配置，在 `.env` 文件中设置：

```bash
# 启用/禁用 RAG（默认：启用）
USE_RAG=true

# 检索结果数量（默认：2）
RAG_TOP_K=2

# 相似度阈值，0-1 之间（默认：0.3）
RAG_SIMILARITY_THRESHOLD=0.3
```

### 使用示例

#### 启用 RAG（默认）
```bash
# 在 API 请求中不需要额外参数，RAG 会自动工作
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "我和男朋友吵架了", "session_id": "test"}'
```

#### 临时禁用 RAG
```bash
# 在特定请求中禁用 RAG
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "你好", "session_id": "test", "use_rag": false}'
```

### RAG 如何提升回复质量

**不使用 RAG：**
AI 仅基于通用训练知识回答，可能缺乏针对性。

**使用 RAG：**
1. 用户提问："我和男朋友吵架后他不理我怎么办？"
2. 系统从知识库检索相关内容（如"吵架和解"主题）
3. AI 结合检索到的专业知识给出建议
4. 回复更具针对性、更专业、更实用

### 知识库内容

当前知识库包含以下主题：
- 表白技巧
- 吵架和解
- 失恋疗愈
- 异地恋维持
- 恋爱沟通
- 父母反对
- 信任建立
- 情绪管理
- 约会技巧
- 关系边界
- 复合建议
- 性与亲密
- 婚姻准备

### 扩展知识库

开发者可以通过编辑 `backend/knowledge_base.json` 添加新的咨询主题：

```json
{
  "主题名称": {
    "keywords": ["关键词1", "关键词2"],
    "content": "专业建议内容...",
    "examples": ["示例问答..."]
  }
}
```

添加新内容后，重启服务即可自动加载。

## 🛠️ 技术栈

- **后端**: Flask, OpenAI API, Python 3.9+, Deep-Translator
- **前端**: React 18, Vite, Tailwind CSS, Lucide React
- **翻译服务**: Google Translate API (via deep-translator)
- **RAG 技术**: ChromaDB, Sentence-Transformers, Vector Embeddings

## ⚠️ 免责声明

本 AI 助手仅供情感支持参考，不能替代专业心理咨询。如遇严重心理问题，请寻求专业帮助。

**24小时心理危机热线**：
- 中国：400-161-9995
- 生命热线：400-821-1215

## 📄 许可证

MIT License

---

⭐ 如果这个项目对你有帮助，请给个 Star！