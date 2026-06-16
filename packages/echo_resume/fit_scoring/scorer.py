"""Deterministic local fit scoring for the desktop MVP."""

from __future__ import annotations

import re
from dataclasses import dataclass

from packages.echo_core.domain.profile import PersonalFact


@dataclass(frozen=True)
class FitScore:
    score: int
    matched_terms: tuple[str, ...]
    missing_terms: tuple[str, ...]
    strong_evidence: tuple[PersonalFact, ...]
    weak_evidence: tuple[PersonalFact, ...]


STOP_WORDS = {
    "and",
    "are",
    "for",
    "the",
    "with",
    "you",
    "will",
    "this",
    "that",
    "our",
    "your",
    "from",
    "have",
    "has",
    "into",
    "role",
    "team",
    "work",
}

CANONICAL_TERMS = {
    "api",
    "aws",
    "backend",
    "ci/cd",
    "cloud",
    "docker",
    "fastapi",
    "graphql",
    "javascript",
    "kubernetes",
    "latex",
    "machine learning",
    "next.js",
    "postgresql",
    "python",
    "rag",
    "react",
    "sql",
    "typescript",
}


def _tokens(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9+#./-]+", text.lower())
        if len(token) > 2 and token not in STOP_WORDS
    }


def _requirements(job_posting: str) -> set[str]:
    lowered = job_posting.lower()
    terms = {term for term in CANONICAL_TERMS if term in lowered}
    terms.update(token for token in _tokens(job_posting) if token in CANONICAL_TERMS)
    return terms


def score_job_fit(job_posting: str, facts: list[PersonalFact]) -> FitScore:
    requirements = _requirements(job_posting)
    if not requirements:
        return FitScore(0, (), (), (), ())

    fact_matches: dict[str, list[PersonalFact]] = {term: [] for term in requirements}
    for fact in facts:
        text = fact.text.lower()
        for term in requirements:
            if term in text:
                fact_matches[term].append(fact)

    matched = tuple(sorted(term for term, matched_facts in fact_matches.items() if matched_facts))
    missing = tuple(sorted(requirements - set(matched)))
    score = round((len(matched) / len(requirements)) * 100)
    strong = tuple(
        fact
        for term in matched
        for fact in fact_matches[term]
        if len(_tokens(fact.text) & requirements) >= 1
    )
    weak = tuple(fact for fact in facts if fact not in strong)
    return FitScore(score, matched, missing, strong[:10], weak[:5])

