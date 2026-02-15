# ERF-DocIntel
ERF Document Intelligence - A comprehensive document processing pipeline that combines OCR, semantic chunking, hierarchical summarization, and multilingual RAG (Retrieval-Augmented Generation) to enable intelligent Q&amp;A on PDFs, DOCX, and images. Built with Streamlit, LangChain, and Ollama.

<p align="center"> <img src="https://img.shields.io/badge/Python-3.9+-blue?logo=python" alt="Python"> <img src="https://img.shields.io/badge/LangChain-🦜🔗-brightgreen" alt="LangChain"> <img src="https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit" alt="Streamlit"> <img src="https://img.shields.io/badge/Ollama-000000?logo=ollama" alt="Ollama"> <img src="https://img.shields.io/badge/Multilingual-🌐-blue" alt="Multilingual"> <img src="https://img.shields.io/badge/RAG-⚡-orange" alt="RAG"> </p><p align="center"> <b>🧠 Intelligent document Q&A with multilingual support (English, فارسی, العربية)</b> </p>
✨ Features

    📁 Multi-format Support - PDF, DOCX, TXT, Images (with OCR)

    🌍 Multilingual - Ask questions in English, Persian, or Arabic

    🔄 Smart Translation - Auto-detects language with LLM supervision

    🎯 9 Prompt Strategies - Chain-of-Thought, Few-Shot, Decomposition, etc.

    📊 Structured Extraction - JSON schemas for contracts, proposals, policies

    📈 Hierarchical Summaries - 4 levels of detail (chunk → section → doc → executive)

    💬 Beautiful Chat UI - Streamlit interface with full RTL support

    🔍 Source Citations - Shows which documents were used

🚀 Quick Start
bash

# Clone
git clone https://github.com/yourusername/DocuMind.git
cd DocuMind

# Install
pip install -r requirements.txt

# Run
streamlit run app.py

Visit http://localhost:8501
🏗️ Architecture
text

Upload → OCR → Chunking → Vector Store → RAG → Response
                    ↓                      ↑
                 Summaries              Query
                    ↓                      ↑
                Extraction              Streamlit UI

🖼️ Screenshots

[Add screenshots of your app here]
📝 License

MIT © [Your Name]
<p align="center"> Made with ❤️ for the ERFDoc Platform </p>
