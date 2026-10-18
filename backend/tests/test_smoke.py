from openai import OpenAI

from app.main import create_app
from config import LLM_BASE_URL, LLM_API_KEY, LLM_MODEL, API_TITLE


def test_config_smoke():
    assert API_TITLE == "PaperPilot"
    assert LLM_BASE_URL.startswith("http")
    assert LLM_MODEL != ""


def test_openai_client_smoke():
    client = OpenAI(
        api_key=LLM_API_KEY,
        base_url=LLM_BASE_URL,
        timeout=10,
    )
    assert client.base_url is not None


def test_app_creation_smoke():
    app = create_app()
    assert app.title == "PaperPilot"

