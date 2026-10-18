import os
from pathlib import Path
from typing import List, Optional

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def _env(name: str, default: str = "") -> str:
    value = os.getenv(name, default)
    return value.strip() if isinstance(value, str) else default


# ── Paths ──────────────────────────────────────────────────────────
STORAGE_DIR: Path = Path(_env("STORAGE_DIR", str(BASE_DIR / "storage")))
CHROMA_DIR: Path = STORAGE_DIR / "chroma_db"
ARXIV_PDFS_DIR: Path = STORAGE_DIR / "arxiv_pdfs"

STORAGE_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_DIR.mkdir(parents=True, exist_ok=True)
ARXIV_PDFS_DIR.mkdir(parents=True, exist_ok=True)

# ── Models ─────────────────────────────────────────────────────────
LLM_BASE_URL: str = _env("LLM_BASE_URL", "http://localhost:11434/v1")
LLM_API_KEY: str = _env("LLM_API_KEY", "ollama")
LLM_MODEL: str = _env("LLM_MODEL", "llama3.2:3b")

EMBEDDING_MODEL: str = _env("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
EMBEDDING_DIMENSION: int = 384
RERANKER_MODEL: Optional[str] = _env("RERANKER_MODEL", "") or None

# ── Retrieval ──────────────────────────────────────────────────────
CHROMA_COLLECTION_NAME: str = "arxiv_papers"
CHUNK_SIZE: int = 500
CHUNK_OVERLAP: int = 100
TOP_K_RETRIEVAL: int = 8
TOP_K_RERANKED: int = 3
ARXIV_MAX_RESULTS: int = 3

# ── Agent/session ──────────────────────────────────────────────────
MAX_HISTORY_TURNS: int = 10

# ── Server ─────────────────────────────────────────────────────────
API_TITLE: str = "PaperPilot"
API_VERSION: str = "0.1.0"
API_HOST: str = _env("API_HOST", "0.0.0.0")
API_PORT: int = int(_env("PORT", "8000"))

ALLOWED_ORIGINS: List[str] = [
    origin.strip()
    for origin in _env(
        "ALLOWED_ORIGINS",
        "http://localhost:5500,http://127.0.0.1:5500",
    ).split(",")
    if origin.strip()
]