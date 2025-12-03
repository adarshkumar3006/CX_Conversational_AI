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

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies

```powershell
pip install -r .\requirements.txt
```

4. Add your Gemini / Vertex API key (for current session)

```powershell
$env:GEMINI_API_KEY = 'your_key_here'
```

5. Optional: quick import smoke-check

```powershell
python -c "from src.core.agent_new import CustomerSupportAgent; from src.rag.generator import ResponseGenerator; from src.rag.retriever_demo import DemoRetriever; from src.privacy.data_masking import DataMasker; print('IMPORTS_OK')"
```

6. Run CLI demo

```powershell
python main.py
```

7. Run Streamlit UI (optional)

```powershell
streamlit run streamlit_app.py
```

## Configuration notes

- Set `GEMINI_API_KEY` via `.env` or environment variable. Do not commit secrets.
- To change the model, update `config/config.json` `llm.model` or set `GEMINI_MODEL` env var.


