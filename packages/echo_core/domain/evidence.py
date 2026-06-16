"""Evidence models shared by Echo Chat and Echo Resume."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EvidenceRef:
    fact_id: str
    quote: str
    score: float | None = None


@dataclass(frozen=True)
class EvidenceSet:
    query: str
    evidence: tuple[EvidenceRef, ...]

    @property
    def fact_ids(self) -> tuple[str, ...]:
        return tuple(item.fact_id for item in self.evidence)

