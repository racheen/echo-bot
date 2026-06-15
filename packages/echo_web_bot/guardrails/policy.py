"""Simple public-profile question guardrails."""

from __future__ import annotations

PRIVATE_TERMS = {
    "address",
    "phone number",
    "salary",
    "private",
    "personal email",
}


def is_public_question_allowed(question: str) -> bool:
    lowered = question.lower()
    return not any(term in lowered for term in PRIVATE_TERMS)

