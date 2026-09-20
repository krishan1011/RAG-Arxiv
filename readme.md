# Agentic ArXiv RAG

A local-first research assistant that ingests ArXiv papers, embeds them into a vector store, retrieves the most relevant passages, and answers questions with grounded citations.

## Why this project stands out

Built a retrieval pipeline that narrows the candidate set from 8 semantically similar chunks down to the top 3 reranked results before generating an answer. That gives the system a much cleaner evidence set than plain vector similarity alone and makes each answer traceable to the underlying paper sections.

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
| Retrieval stages | 2-stage (retrieve → rerank) |

In practical terms, the app does not answer from a broad unfiltered vector dump. It retrieves a shortlist, reranks it, and then answers with the strongest evidence first.

## What I built

- ArXiv ingestion by paper ID or keyword search
- Local PDF upload ingestion
- Semantic search over a local Chroma vector store
- Cross-encoder style reranking for better relevance control
- Agentic question answering with session memory
- Lightweight frontend for browsing papers and answers

## Tech stack

- Backend: FastAPI + Uvicorn
- Embeddings: SentenceTransformers
- Vector DB: ChromaDB
- Retrieval: cosine similarity + reranking
- LLM layer: OpenRouter-compatible model access
- Frontend: vanilla HTML, CSS, and JavaScript

## Architecture

```txt
RAG-Arxiv/
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
├── .gitignore
├── readme.md
└── LICENSE
```

## Project highlights

### 1) Retrieval that is grounded in evidence
The system stores metadata such as `arxiv_id`, `title`, `authors`, and `page_number` alongside each chunk. That makes answer citations easy to trace to the exact paper section.

### 2) Duplicate-safe ingestion
Before adding a paper, the app checks whether the `arxiv_id` is already present. Before adding each chunk, it checks the generated chunk ID. This keeps repeated ingestion runs stable instead of duplicating data.

### 3) Lightweight deployment design
The embedding model and reranker are initialized lazily, which is helpful for constrained hosting environments and keeps the local prototype easy to run without heavy runtime overhead.

### 4) Simple extension path
The code is intentionally direct: retrieval logic, ingestion logic, and the agent loop are each separated so it is easy to add new tools, models, or retrieval strategies later.

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
OPENROUTER_API_KEY=your_key_here
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

---

<div align="center">
  Built by <b>Krishan Kumar</b>
</div>
