"""RAG-based private career chat orchestration."""

from __future__ import annotations

from typing import Protocol

from packages.echo_core.prompts.chat import build_career_chat_prompt
from packages.echo_core.rag.retrieval import Retriever


class TextGenerator(Protocol):
    def generate(self, prompt: str, temperature: float = 0.2) -> str: ...


class EchoChatService:
    def __init__(self, retriever: Retriever, generator: TextGenerator) -> None:
        self.retriever = retriever
        self.generator = generator

    def answer(self, question: str, evidence_limit: int = 5) -> str:
        results = self.retriever.search(question, limit=evidence_limit)
        prompt = build_career_chat_prompt(
            question, [result.fact for result in results]
        )
        return self.generator.generate(prompt, temperature=0.2)

