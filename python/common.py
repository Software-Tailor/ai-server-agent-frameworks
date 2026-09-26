"""Shared settings for every framework example — the same three variables as all AI Server samples."""
import os
import sys

BASE_URL = os.environ.get("AISERVER_BASE_URL", "http://localhost:11436/v1")  # must end in /v1
API_KEY = os.environ.get("AISERVER_API_KEY") or "none"                         # required on network servers
MODEL = os.environ.get("AISERVER_MODEL") or sys.exit("Set AISERVER_MODEL to a tool-capable model id (GET /v1/models).")

QUESTION = "What is the weather in Dublin right now? Use the tool, then answer in one sentence."

# The tool returns a unique token. If the final answer contains it, the whole loop worked: the model made a
# structured tool call, the framework executed it, sent the result back, and the model used it.
TOKEN = "ZEPHYR-42"


def weather(city: str) -> str:
    """Stub weather service — replace with a real API."""
    return f"{city}: 14°C, light rain, forecast code {TOKEN}"


def report(framework: str, answer: str) -> None:
    ok = TOKEN in (answer or "")
    print(f"[{'PASS' if ok else 'FAIL'}] {framework}: {answer.strip() if answer else '(no answer)'}")
    if not ok:
        sys.exit(1)
