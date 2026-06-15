"""Fact-aware retrieval contracts and deterministic fallback retrieval."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Protocol, Sequence

from packages.echo_core.domain.profile import PersonalFact


@dataclass(frozen=True)
class RetrievedFact:
    fact: PersonalFact
    score: float


class FactRepository(Protocol):
    def list_verified(self) -> list[PersonalFact]: ...


class Retriever(Protocol):
    def search(self, query: str, limit: int = 5) -> list[RetrievedFact]: ...


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9+#.]+", text.lower()))


class KeywordFactRetriever:
    """Deterministic local fallback used for tests and index recovery."""

    def __init__(self, repository: FactRepository) -> None:
        self.repository = repository

    def search(self, query: str, limit: int = 5) -> list[RetrievedFact]:
        query_tokens = _tokens(query)
        if not query_tokens:
            return []

        results: list[RetrievedFact] = []
        for fact in self.repository.list_verified():
            fact_tokens = _tokens(fact.text)
            score = len(query_tokens & fact_tokens) / len(query_tokens)
            if score:
                results.append(RetrievedFact(fact=fact, score=score))
        return sorted(results, key=lambda result: (-result.score, result.fact.id))[
            :limit
        ]


def fact_ids(results: Sequence[RetrievedFact]) -> list[str]:
    return [result.fact.id for result in results]

