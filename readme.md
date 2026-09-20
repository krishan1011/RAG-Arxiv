# RAG-Arxiv

A FastAPI-based research assistant for ArXiv papers with local vector search, reranking, and an agentic query workflow.

## Overview

This project lets you:
- ingest ArXiv papers by ID or keyword
- upload local PDF files
- query the embedded corpus with semantic retrieval
- rerank top papers for higher precision
- ask questions through an LLM agent with session memory
- browse the result from a lightweight frontend

## Tech stack

- Backend: FastAPI + Uvicorn
- LLM: OpenRouter-compatible models
- Embeddings: SentenceTransformers
- Vector database: ChromaDB
- Retrieval: cosine similarity + reranking
- Frontend: vanilla HTML/CSS/JS

## Project structure

```txt
RAG-Arxiv/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── agent/
│   │   ├── prompts.py
│   │   ├── agent_runner.py
│   │   └── tools/
│   ├── api/
│   │   ├── dependencies.py
│   │   └── routes/
│   ├── ingestion/
│   │   ├── arxiv_fetcher.py
│   │   ├── embedder.py
│   │   ├── pdf_loader.py
│   │   └── __init__.py
│   ├── memory/
│   │   └── session_store.py
│   ├── retrieval/
│   │   ├── reranker.py
│   │   ├── vectorstore.py
│   │   └── __init__.py
│   ├── tests/
│   │   └── test_config.py
│   ├── .env.example
│   ├── config.py
│   ├── main.py
│   ├── requirements.txt
│   └── test.py
├── frontend/
│   ├── app.js
│   ├── index.html
│   └── style.css
├── .gitignore
├── readme.md
└── LICENSE
```

## Local setup

### 1) Create environment

```bash
cd RAG-Arxiv/backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Configure environment variables

Copy the example file and fill in your keys:

```bash
copy .env.example .env
```

Then set values like:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
GEMINI_MODEL=openai/gpt-oss-120b:free
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
API_HOST=0.0.0.0
PORT=8000
ALLOWED_ORIGINS=http://localhost:5500,http://127.0.0.1:5500
```

### 3) Run the backend

```bash
python main.py
```

The API will be available at:
- http://localhost:8000
- http://localhost:8000/docs

### 4) Run the frontend

Open the HTML file in the browser or use a local static server:

```bash
cd ../frontend
python -m http.server 5500
```

Then open:
- http://localhost:5500

## API endpoints

- POST /ingest/pdf
- POST /ingest/arxiv
- GET /ingest/list
- POST /query/
- POST /query/agent
- POST /query/session/new
- GET /session/{session_id}
- DELETE /session/{session_id}
- GET /health

## Notes

This app is intentionally lightweight and transparent: no heavy framework, no hidden magic, and the retrieval flow is easy to debug. The project is structured to be easy to extend and deploy.

## License

MIT

---

## API reference

| Method | Endpoint | |
|--------|----------|-|
| `POST` | `/ingest/pdf` | Upload a PDF |
| `POST` | `/ingest/arxiv` | Ingest by Arxiv ID or keyword |
| `GET` | `/ingest/list` | List ingested papers |
| `POST` | `/query/agent` | Agentic query with session memory |
| `POST` | `/query/` | Plain retrieval, no LLM |
| `POST` | `/query/session/new` | New session |
| `GET` | `/session/{id}` | Conversation history |
| `DELETE` | `/session/{id}` | Clear session |
| `GET` | `/health` | Health check |

---

## Design decisions worth noting

**No frameworks.** Retrieval, chunking, and agent logic are all written directly. Easier to debug, no version conflicts, no magic happening somewhere in a dependency chain.

**Lazy model loading.** Embedding model and reranker initialize on first request, not at startup. This keeps memory under Render's 512MB free-tier limit — a constraint that kills most deployed demos.

**Metadata-rich chunks.** Every chunk carries `arxiv_id`, `title`, `authors`, and `page_number`. Cited answers come for free, no post-processing needed.

**Duplicate-safe ingestion.** Papers are checked by `arxiv_id` before download. Chunks are checked by UUID before embedding. Call ingest multiple times without thinking about it.

---

## Project structure

```
RAG-Arxiv/
├── backend/
│   ├── ingestion/
│   │   ├── pdf_loader.py          PDF parsing + chunking
│   │   ├── embedder.py            SentenceTransformer singleton
│   │   └── arxiv_fetcher.py       Arxiv API + PDF downloader
│   ├── retrieval/
│   │   ├── vectorstore.py         ChromaDB add / query / list
│   │   └── reranker.py            Cross-encoder reranking
│   ├── memory/
│   │   └── session_store.py       In-memory conversation history
│   ├── agent/
│   │   ├── agent_runner.py        Two-step LLM loop
│   │   ├── prompts.py             System prompts + templates
│   │   └── tools/
│   │       ├── vectorstore_tool.py
│   │       ├── arxiv_tool.py
│   │       └── summarize_tool.py
│   └── api/
│       └── routes/
│           ├── ingest.py          POST /ingest/*
│           ├── query.py           POST /query/*
│           └── session.py         GET | DELETE /session/*
└── frontend/
    ├── index.html
    ├── style.css
    └── app.js
```

---

<div align="center">
  Built by <b>Krishan Kumar</b> • 
  <a href="https://www.linkedin.com/in/krishan1011/" target="_blank">
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linkedin/linkedin-original.svg" 
         width="18" 
         height="18"
         alt="LinkedIn"
         style="vertical-align: middle;"/>
  </a>
</div>
