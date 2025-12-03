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

## Configuration notes

- Set `GEMINI_API_KEY` via `.env` or environment variable. Do not commit secrets.
- To change the model, update `config/config.json` `llm.model` or set `GEMINI_MODEL` env var.
- The code includes a demo retriever to avoid failing when embeddings or FAISS are not configured. If you want full vector search, I can help enable embeddings and FAISS.

## Troubleshooting

- Model not found / 404: list available models:

```powershell
python -c "import os, google.generativeai as genai; genai.configure(api_key=os.getenv('GEMINI_API_KEY')); print(genai.list_models())"
```

- Dependency build errors (faiss/numpy): upgrade pip/setuptools/wheel and reinstall:

```powershell
python -m pip install --upgrade pip setuptools wheel
pip install -r .\requirements.txt
```

## Need help?

If you'd like I can:

- Run the import smoke-check and fix import issues.
- Enable full embeddings + FAISS and wire persistence.
- Add CI smoke-tests or sample data for demos.

Tell me which next step you'd like me to take.
