"""Loopback-only Ollama client."""

from __future__ import annotations

import json
import urllib.request
from dataclasses import dataclass
from typing import Iterable

from app.config import validate_loopback_url


@dataclass(frozen=True)
class OllamaClient:
    base_url: str
    generation_model: str
    embedding_model: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "base_url", validate_loopback_url(self.base_url))

    def list_models(self) -> set[str]:
        payload = self._request("/api/tags", None)
        return {
            model["name"]
            for model in payload.get("models", [])
            if isinstance(model, dict) and isinstance(model.get("name"), str)
        }

    def embed(self, texts: Iterable[str]) -> list[list[float]]:
        vectors: list[list[float]] = []
        for text in texts:
            payload = self._request(
                "/api/embeddings",
                {"model": self.embedding_model, "prompt": text},
            )
            vectors.append([float(value) for value in payload["embedding"]])
        return vectors

    def generate(self, prompt: str, temperature: float = 0.2) -> str:
        payload = self._request(
            "/api/generate",
            {
                "model": self.generation_model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": temperature},
            },
        )
        return str(payload["response"])

    def _request(self, path: str, body: dict[str, object] | None) -> dict[str, object]:
        data = json.dumps(body).encode("utf-8") if body is not None else None
        request = urllib.request.Request(
            f"{self.base_url}{path}",
            data=data,
            method="POST" if data is not None else "GET",
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )
        with urllib.request.urlopen(request, timeout=120) as response:
            payload = json.load(response)
        if not isinstance(payload, dict):
            raise ValueError("Ollama returned an invalid response.")
        return payload

