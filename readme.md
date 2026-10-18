# PaperPilot

![PaperPilot Interface](docs/screenshot.png)

PaperPilot is an intelligent, local-first research copilot designed to explore, ingest, and analyze scientific papers from arXiv and local PDFs. By combining dense semantic search, optional cross-encoder reranking, and an autonomous agent reasoning loop with conversational session memory, PaperPilot produces precise, evidence-grounded answers cited directly to source papers and pages.

## Why this project stands out

Unlike naive RAG systems that blindly dump unfiltered vector similarity matches into a prompt, PaperPilot structures paper analysis with high precision. Candidate passages are retrieved from an embedded corpus, and when a cross-encoder model is configured (`RERANKER_MODEL`), candidates are dynamically reranked before answer generation. This delivers an accurate, focused evidence set where every answer remains directly traceable to underlying paper sections.

## Results snapshot

This project is designed around concrete, measurable retrieval behavior. The pipeline is configured and implemented with these verified system metrics:

| Metric | Value |
|---|---:|
| Embedding dimension | 384 |
| Retrieval candidates per query | 8 |
| Final reranked passages returned | 3 |
| Chunk size | 500 tokens |
| Chunk overlap | 100 tokens |
| Max chat history per session | 10 turns |
| Duplicate-safe ingestion checks | arXiv ID + chunk ID |
| Retrieval stages | 2-stage (dense retrieve → rerank when `RERANKER_MODEL` is configured; default in Phase 5) |

In practical terms, the app avoids broad, unverified vector dumps. It surfaces relevant passages, applies reranking when enabled, and synthesizes answers backed by concrete evidence.

## What I built

- **ArXiv Paper Ingestion**: Direct fetching and parsing by arXiv ID or topic keyword.
- **Local PDF Upload**: Multipart file ingestion with text extraction and layout-aware chunking.
- **Vector Retrieval**: Local ChromaDB embedding store using SentenceTransformers.
- **Context Reranking**: Cross-encoder reranking pipeline that executes when `RERANKER_MODEL` is set (to be enabled by default in Phase 5).
- **Agentic Reasoning Loop**: Autonomous research router that selects appropriate tools and generates answers with conversational memory.
- **Responsive Dashboard**: Dark-themed, modern interface for browsing papers and interacting with the agent.

## Tech stack

- Backend: FastAPI + Uvicorn
- Embeddings: SentenceTransformers (`all-MiniLM-L6-v2`)
- Vector DB: ChromaDB
- Retrieval: Cosine similarity + cross-encoder reranking
- LLM layer: Local Ollama (`llama3.2:3b`)
- Frontend: Vanilla HTML, CSS, and JavaScript

## Architecture

```txt
PaperPilot/
├── backend/
│   ├── app/
│   │   └── main.py
│   ├── agent/
│   │   ├── agent_runner.py
│   │   ├── prompts.py
│   │   └── tools/
│   ├── api/
│   │   └── routes/
│   ├── ingestion/
│   │   ├── arxiv_fetcher.py
│   │   ├── embedder.py
│   │   └── pdf_loader.py
│   ├── memory/
│   │   └── session_store.py
│   ├── retrieval/
│   │   ├── reranker.py
│   │   └── vectorstore.py
│   ├── config.py
│   ├── main.py
│   ├── requirements.txt
│   └── test.py
├── frontend/
│   ├── app.js
│   ├── index.html
│   └── style.css
├── docs/
│   └── screenshot.png
├── .gitignore
├── readme.md
└── LICENSE
```

## Project highlights

### 1) Retrieval grounded in evidence
The system stores metadata such as `arxiv_id`, `title`, `authors`, and `page_number` alongside each chunk. That makes answer citations easy to trace to the exact paper section.

### 2) Duplicate-safe ingestion
Before adding a paper, the app checks whether the `arxiv_id` is already present. Before adding each chunk, it checks the generated chunk ID. This keeps repeated ingestion runs stable instead of duplicating data.

### 3) Lightweight deployment design
The embedding model and reranker are initialized lazily, which is helpful for constrained hosting environments and keeps the local prototype easy to run without heavy runtime overhead.

### 4) Simple extension path
The code is intentionally modular: retrieval logic, ingestion logic, and the agent loop are each separated so it is easy to add new tools, models, or retrieval strategies later.

## Local setup

### 1) Create the environment

```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Configure environment variables

Create a local `.env` file from the example and add your keys:

```bash
copy .env.example .env
```

Example:

```env
LLM_BASE_URL=http://localhost:11434/v1
LLM_API_KEY=ollama
LLM_MODEL=llama3.2:3b
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
RERANKER_MODEL=
API_HOST=0.0.0.0
PORT=8000
ALLOWED_ORIGINS=http://localhost:5500,http://127.0.0.1:5500
```

### 3) Run the backend

```bash
python main.py
```

API endpoints are available at:
- http://localhost:8000
- http://localhost:8000/docs

### 4) Run the frontend

```bash
cd ../frontend
python -m http.server 5500
```

Then open: http://localhost:5500

## API overview

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/ingest/pdf` | Upload and ingest a local PDF |
| POST | `/ingest/arxiv` | Ingest by ArXiv ID or keyword |
| GET | `/ingest/list` | List ingested papers |
| POST | `/query/` | Retrieve relevant chunks |
| POST | `/query/agent` | Run agentic Q&A with session memory |
| POST | `/query/session/new` | Start a new session |
| GET | `/session/{session_id}` | Fetch session memory |
| DELETE | `/session/{session_id}` | Clear a session |
| GET | `/health` | Health check |

## Note on evaluation data

There is no dedicated evaluation notebook or benchmark report currently checked into this repository, so this README intentionally uses the metrics that are directly defined in the project implementation rather than inventing model-accuracy numbers.

## License

MIT

## Acknowledgements

Original baseline created by [Krishan Kumar](https://github.com/krishan1011) ([RAG-Arxiv](https://github.com/krishan1011/RAG-Arxiv)).

---

<div align="center">
  Maintained by <b>PaperPilot Contributors</b> • Originally built by <b>Krishan Kumar</b>
</div>
