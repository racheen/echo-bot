"""Citation helpers for retrieved facts."""

from __future__ import annotations

import re

FACT_CITATION_PATTERN = re.compile(r"\[fact:([A-Za-z0-9_.:-]+)\]")


def render_fact_citation(fact_id: str) -> str:
    return f"[fact:{fact_id}]"


def extract_fact_citations(text: str) -> tuple[str, ...]:
    return tuple(FACT_CITATION_PATTERN.findall(text))

