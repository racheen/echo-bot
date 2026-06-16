"""Ollama embedding adapter."""

from __future__ import annotations

from collections.abc import Sequence

from packages.echo_core.integrations.ollama import OllamaClient


class OllamaEmbeddingService:
    def __init__(self, client: OllamaClient) -> None:
        self.client = client

    def embed_texts(self, texts: Sequence[str]) -> list[list[float]]:
        return self.client.embed(texts)

