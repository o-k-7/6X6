"""Normalize Ollama chat responses without treating reasoning as an answer."""

from __future__ import annotations


class ModelResponseError(ValueError):
    """The transport returned an invalid response envelope."""


def final_content(payload: dict) -> tuple[str, bool]:
    """Return final assistant text and whether a separate reasoning field exists.

    Empty final content remains empty, even when thinking is present. Callers may
    retry with a larger generation budget, but must never release reasoning as a
    substitute for the final answer. No reasoning text is returned or logged.
    """
    if not isinstance(payload, dict):
        raise ModelResponseError("Ollama response must be an object")
    message = payload.get("message")
    if not isinstance(message, dict):
        raise ModelResponseError("Ollama response has no assistant message")
    content = message.get("content", "")
    if content is None:
        content = ""
    if not isinstance(content, str):
        raise ModelResponseError("Ollama final content must be text")
    return content, bool(message.get("thinking"))
