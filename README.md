# 🔬 LLM Research Assistant

An AI-powered research assistant that lets you upload academic papers and 
chat with them using Claude (Anthropic). Built with Python, Streamlit, and the Anthropic API.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red)
![Claude](https://img.shields.io/badge/Claude-Sonnet-orange)
![License](https://img.shields.io/badge/License-MIT-green)

## 📸 Demo

> Upload a research paper → ask questions → get precise, context-aware answers

![demo screenshot](docs/demo.png)

## ✨ Features

- 📄 Upload any research paper as PDF and chat with its contents
- 🧠 Maintains full conversation history for follow-up questions
- 🔍 Extracts and chunks PDF text for accurate context loading
- 💡 Suggested questions to guide exploration
- 🗑️ Clear conversation and load a new document anytime

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| AI Model | Claude Sonnet (Anthropic API) |
| UI | Streamlit |
| PDF Parsing | pypdf |
| Language | Python 3.12 |
| Workflow | Built with Claude Code |

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- Anthropic API key ([get one here](https://console.anthropic.com))

### Installation

```bash
# Clone the repo
git clone https://github.com/Sgin0630/llm-research-assistant.git
cd llm-research-assistant

# Create and activate virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

### Configuration

Create a `.env` file in the root folder:

ANTHROPIC_API_KEY=your_api_key_here


### Run

```bash
PYTHONPATH=. streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

## 📁 Project Structure
llm-research-assistant/
├── src/
│   ├── assistant.py      # Claude API integration & conversation management
│   └── pdf_reader.py     # PDF text extraction and chunking
├── app.py                # Streamlit UI
├── tests/                # Unit tests
├── requirements.txt
└── README.md

## 🔧 Development

This project was built using [Claude Code](https://claude.ai/code) as an 
AI pair programmer — used for code review, feature iteration, and debugging.

## 📄 License

MIT
