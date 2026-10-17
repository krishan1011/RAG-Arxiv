import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def _env(name: str, default: str = "") -> str:
    value = os.getenv(name, default)
    return value.strip() if isinstance(value, str) else default


STORAGE_DIR = BASE_DIR / "storage"
CHROMA_DIR = STORAGE_DIR / "chroma_db"
STORAGE_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_DIR.mkdir(parents=True, exist_ok=True)

OPENROUTER_API_KEY = _env("OPENROUTER_API_KEY", "")
GEMINI_MODEL = _env("GEMINI_MODEL", "")
EMBEDDING_MODEL = _env("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

EMBEDDING_DIMENSION = 384
RERANKER_MODEL = _env("RERANKER_MODEL", "") or None

CHROMA_COLLECTION_NAME = "arxiv_papers"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
TOP_K_RETRIEVAL = 8
TOP_K_RERANKED = 3
ARXIV_MAX_RESULTS = 3
MAX_HISTORY_TURNS = 10

API_TITLE = "PaperPilot"
API_VERSION = "0.1.0"
API_HOST = _env("API_HOST", "0.0.0.0")
API_PORT = int(_env("PORT", "8000"))

ALLOWED_ORIGINS = [
    origin.strip()
    for origin in _env(
        "ALLOWED_ORIGINS",
        "http://localhost:5500,http://127.0.0.1:5500",
    ).split(",")
    if origin.strip()
]