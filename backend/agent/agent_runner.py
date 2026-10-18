import json
import logging
from typing import Dict, Any, List

import httpx
import openai
from openai import OpenAI

from config import LLM_BASE_URL, LLM_API_KEY, LLM_MODEL
from agent.prompts import (
    AGENT_SYSTEM_PROMPT,
    ANSWER_GENERATION_PROMPT,
)
from agent.tools.vectorstore_tool import (
    search_vectorstore,
    format_context,
)
from agent.tools.arxiv_tool import (
    fetch_and_ingest_arxiv,
)
from agent.tools.summarize_tool import (
    summarize_paper,
)
from memory.session_store import (
    get_history,
    add_turn,
)

logger = logging.getLogger(__name__)

_client = None

GREETING_WORDS = {
    "hi", "hello", "hey", "greetings", "good morning", "good afternoon",
    "good evening", "howdy", "sup", "yo"
}


def _is_short_greeting(text: str) -> bool:
    cleaned = text.strip().lower().rstrip("!.,?")
    words = cleaned.split()
    if len(words) <= 4:
        if cleaned in GREETING_WORDS or any(w in GREETING_WORDS for w in words):
            return True
    return False


def _get_client():
    global _client

    if _client is None:
        _client = OpenAI(
            api_key=LLM_API_KEY,
            base_url=LLM_BASE_URL,
            timeout=120,
        )

    return _client


def _llm(prompt: str) -> str:
    try:
        client = _get_client()

        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.3,
            timeout=120,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        err_msg = str(e).lower()
        if (
            isinstance(e, (openai.APIConnectionError, httpx.ConnectError, httpx.TimeoutException))
            or "connection" in err_msg
            or "connect" in err_msg
            or "refused" in err_msg
            or "unreachable" in err_msg
        ):
            return f"LLM Error: cannot reach the local model. Start Ollama and run: ollama pull {LLM_MODEL}"
        return f"LLM Error: {str(e)}"


def _parse_tool_call(raw: str) -> dict | None:
    try:
        start = raw.find("{")
        end = raw.rfind("}") + 1

        if start == -1 or end == 0:
            raise ValueError("No JSON found")

        parsed = json.loads(raw[start:end])
        if not isinstance(parsed, dict) or "tool" not in parsed:
            raise ValueError("Invalid tool call JSON structure")

        return parsed

    except Exception:
        return None


def run_agent(query: str, session_id: str) -> dict:
    history = get_history(session_id)
    history_text = ""

    if history:
        history_text = "\n".join(
            f"{turn['role'].capitalize()}: {turn['content']}"
            for turn in history[-6:]
        )

    routing_prompt = f"""
{AGENT_SYSTEM_PROMPT}

Conversation so far:
{history_text}

User question:
{query}
"""

    raw_decision = _llm(routing_prompt)
    decision = _parse_tool_call(raw_decision)

    if decision is None:
        logger.warning(
            "Router tool call parsing fallback on raw decision: %r. Query: %r",
            raw_decision,
            query,
        )
        if _is_short_greeting(query):
            decision = {
                "tool": "answer_directly",
                "input": "Hello! How can I help you explore your research papers today?",
            }
        else:
            decision = {
                "tool": "search_vectorstore",
                "input": query,
            }

    tool = decision.get("tool", "search_vectorstore")
    tool_input = decision.get("input", query)

    sources: List[Dict[str, Any]] = []
    context = ""
    direct_answer = None

    try:
        if tool == "search_vectorstore":
            chunks = search_vectorstore(tool_input)
            context = format_context(chunks)
            sources = _extract_sources(chunks)

        elif tool == "fetch_and_ingest_arxiv":
            result = fetch_and_ingest_arxiv(tool_input)
            if result.get("status") == "error":
                direct_answer = result.get("message", "Error fetching arXiv paper.")
            else:
                chunks = search_vectorstore(query)
                context = format_context(chunks)
                sources = _extract_sources(chunks)

        elif tool == "summarize_paper":
            result = summarize_paper(tool_input, _llm)
            if result.get("status") == "error":
                direct_answer = result.get("message", "Error summarizing paper.")
            else:
                direct_answer = result.get("summary", "")
                sources = [
                    {
                        "title": result.get("title", ""),
                        "authors": result.get("authors", ""),
                    }
                ]

        elif tool == "answer_directly":
            direct_answer = tool_input

        else:
            direct_answer = "Unknown tool selected."

        if direct_answer is None:
            if not context:
                answer = "I could not find sufficient information in the ingested papers."
            else:
                answer_prompt = ANSWER_GENERATION_PROMPT.format(
                    context=context,
                    history=history_text,
                    question=query,
                )
                answer = _llm(answer_prompt)
        else:
            answer = direct_answer

    except Exception as e:
        answer = f"Agent execution error: {str(e)}"

    add_turn(session_id, "user", query)
    add_turn(session_id, "assistant", answer)

    safe_sources = list(sources) if isinstance(sources, (list, tuple)) else []

    return {
        "answer": answer,
        "tool_used": tool,
        "sources": safe_sources,
        "session_id": session_id,
    }


def _extract_sources(chunks: list) -> list:
    seen = set()
    sources = []

    for chunk in chunks:
        key = chunk.get("arxiv_id") or chunk.get("source", "")
        if key and key not in seen:
            seen.add(key)
            sources.append(
                {
                    "title": chunk.get("title", ""),
                    "authors": chunk.get("authors", ""),
                    "arxiv_id": chunk.get("arxiv_id", ""),
                    "page_number": chunk.get("page_number", ""),
                }
            )

    return sources