"""Citation evaluation helpers."""

from __future__ import annotations


def citation_coverage(claim_citations: list[list[str]]) -> float:
    if not claim_citations:
        return 1.0
    supported = sum(bool(citations) for citations in claim_citations)
    return supported / len(claim_citations)

