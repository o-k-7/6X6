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
    thinking = message.get("thinking")
    return content, isinstance(thinking, str) and bool(thinking.strip())


def model_identity(payload: dict) -> tuple[str, str | None]:
    """Extract the model identifier and optional digest without guessing."""
    if not isinstance(payload, dict):
        raise ModelResponseError("Ollama response must be an object")
    model = payload.get("model")
    if not isinstance(model, str) or not model.strip():
        raise ModelResponseError("Ollama response has no model identifier")
    digest = payload.get("digest")
    if digest is not None and not isinstance(digest, str):
        raise ModelResponseError("Ollama digest must be text when present")
    return model, digest
