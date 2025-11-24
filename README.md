\# 💖 Emotional Counseling AI - 恋爱情绪咨询 AI



一个专业的恋爱情绪咨询 AI 助手，提供温暖、专业的情感支持和建议。



\[!\[License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

\[!\[Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

\[!\[React](https://img.shields.io/badge/react-18.2+-61DAFB.svg)](https://reactjs.org/)



\## ✨ 功能特点



\- 🤝 \*\*共情倾听\*\*：理解用户的情感困扰，提供温暖的支持

\- 💡 \*\*专业建议\*\*：基于心理学原理，提供实用的恋爱建议

\- 🔒 \*\*隐私保护\*\*：所有对话内容安全加密，保护用户隐私

\- 🎯 \*\*个性化\*\*：根据用户情况提供定制化的咨询方案

\- 📊 \*\*情绪分析\*\*：智能识别用户情绪状态

\- 🆘 \*\*危机干预\*\*：自动识别危机关键词并提供紧急帮助

\- 🌐 \*\*中英翻译\*\*：支持中英文实时翻译，自动语言检测，打破语言障碍



\## 🚀 快速开始



\### 环境要求



\- Node.js >= 18.0.0

\- Python >= 3.9

\- OpenAI API Key



\### 安装步骤



1\. \*\*克隆仓库\*\*

```bash

git clone https://github.com/wyt666888/emotional-counseling-ai.git

cd emotional-counseling-ai

```



2\. \*\*配置后端\*\*

```bash

cd backend

pip install -r requirements.txt

cp .env.example .env

\# 编辑 .env 文件，填入你的 OPENAI\_API\_KEY

```



3\. \*\*启动后端\*\*

```bash

python app.py

```



4\. \*\*配置前端\*\*（新终端）

```bash

cd frontend

npm install

```



5\. \*\*启动前端\*\*

```bash

npm run dev

```



6\. \*\*开始使用\*\*

打开浏览器访问 `http://localhost:3000`



\## 📁 项目结构



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

```



\## 🌐 翻译功能



\### 功能特性

\- \*\*自动语言检测\*\*：智能识别输入文本是中文还是英文

\- \*\*实时翻译\*\*：对话消息即时翻译显示

\- \*\*双向翻译\*\*：支持中文⇄英文互译

\- \*\*手动选择\*\*：可手动指定目标语言（自动/中文/英文）

\- \*\*优雅显示\*\*：原文和译文同时展示，便于对照



\### 使用方法

1\. 点击界面右上角的 "翻译" 按钮启用翻译功能

2\. 选择目标语言（默认为自动检测）

3\. 发送消息后会自动显示翻译

4\. 启用翻译功能后，历史消息也会被翻译



\### API 使用

详见 [API文档](docs/API.md) 中的翻译接口说明。



\## 🛠️ 技术栈



\- \*\*后端\*\*: Flask, OpenAI API, Python 3.9+, Deep-Translator

\- \*\*前端\*\*: React 18, Vite, Tailwind CSS

\- \*\*翻译服务\*\*: Google Translate API (via deep-translator)



\## ⚠️ 免责声明



本 AI 助手仅供情感支持参考，不能替代专业心理咨询。如遇严重心理问题，请寻求专业帮助。



\*\*24小时心理危机热线\*\*：

\- 中国：400-161-9995

\- 生命热线：400-821-1215



\## 📄 许可证



MIT License



---



⭐ 如果这个项目对你有帮助，请给个 Star！

