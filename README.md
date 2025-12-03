# CX_Conversational_AI

# CX_Conversational_AI

Tagline: A hyper-personalized RAG-based customer support agent combining customer context, PII-safe masking, and Google Generative AI for tailored responses.

## Overview

This repository is a demo of a Retrieval-Augmented Generation (RAG) customer support agent. It demonstrates:

- PII masking before any external LLM call.
- Enriching queries with customer and location context.
- A safe demo retriever (fallback mode) plus an LLM generator using Google Generative AI.
- A CLI demo (`main.py`) and a small Streamlit UI (`streamlit_app.py`).

## Contents (key files)

- `main.py` — CLI demo + interactive mode.
- `streamlit_app.py` — Streamlit demo UI.
- `src/privacy/data_masking.py` — PII masking utilities.
- `src/rag/generator.py` — LLM wrapper (Google generative client).
- `src/rag/retriever_demo.py` — Demo retriever (safe fallback without embeddings).
- `src/core/agent_new.py` — Agent orchestrator.
- `config/config.json` — Configuration (model, data sources, agent settings).
- `.env` — Environment variables (add `GEMINI_API_KEY` here; do not commit secrets).

## Quick start (Windows PowerShell)

Prerequisites

- Python 3.10+ (3.11 recommended)
- Git
- (Optional) Docker

1. Clone the repo

```powershell
git clone https://github.com/adarshkumar3006/CX_Conversational_AI.git
cd CX_Conversational_AI
```

2. Create & activate venv

# 📄 Groq + PDF RAG Demo

**Tagline:** Upload a PDF, ask questions, get answers powered by Groq AI.

## Overview

A simple demo of Retrieval-Augmented Generation (RAG) using:

- **Groq API** for fast LLM inference
- **PyPDF2** for PDF text extraction
- **Streamlit** for interactive web UI
- **Simple in-memory text storage** (no complex embeddings/vector DB for demo)

## Files

- `main.py` — CLI demo (load PDF, ask questions interactively)
- `streamlit_ui.py` — Streamlit web UI (upload PDF, chat interface)
- `rag_groq.py` — Core RAG module (PDF loading, Groq response generation)
- `.env` — API keys (set your Groq API key here)
- `requirements.txt` — Python dependencies

## Quick Start (Windows PowerShell)

### 1) Clone & setup

```powershell
git clone https://github.com/adarshkumar3006/CX_Conversational_AI.git
cd CX_Conversational_AI
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r .\requirements.txt
```

### 2) Add Groq API key

Get your API key from [console.groq.com](https://console.groq.com/keys), then add to `.env`:

```powershell
$env:GROQ_API_KEY = 'your_groq_api_key_here'
```

Or edit `.env` directly:

```dotenv
GROQ_API_KEY=your_groq_api_key_here
```

### 3) Run CLI demo

```powershell
python main.py
```

Commands:

- `load /path/to/file.pdf` — Load a PDF
- Ask any question — Generate response based on PDF
- `clear` — Clear loaded documents
- `exit` — Quit

### 4) Run Streamlit UI (optional)

```powershell
streamlit run streamlit_ui.py
```

Opens browser at `http://localhost:8501`. Upload PDF via sidebar, ask questions in chat.

## How it works

1. **Load PDF** — Extract all text from PDF using PyPDF2
2. **Store** — Keep text in memory (demo only; production would use vector DB)
3. **Query** — User asks a question
4. **Prompt** — Build a prompt with PDF content + question
5. **Groq** — Send to Groq API (Mixtral model) for response generation
6. **Return** — Display answer to user

## Troubleshooting

- **API key error:** Verify `GROQ_API_KEY` is set correctly in `.env` or environment
- **PDF load error:** Check the file path exists and is a valid PDF
- **No Groq response:** Confirm internet connection and API key is active

## Next steps (optional enhancements)

- Add vector embeddings + FAISS for semantic search
- Support multiple PDFs
- Add chat history persistence
- Use advanced prompting (few-shot, chain-of-thought)

---

Enjoy! 🚀
