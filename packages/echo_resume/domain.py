"""Echo Resume domain models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4


@dataclass(frozen=True)
class JobAnalysis:
    company: str
    role: str
    seniority: str | None = None
    required_skills: tuple[str, ...] = ()
    preferred_skills: tuple[str, ...] = ()
    responsibilities: tuple[str, ...] = ()
    keywords: tuple[str, ...] = ()
    company_context: str | None = None


@dataclass(frozen=True)
class ResumeClaim:
    text: str
    fact_ids: tuple[str, ...]


@dataclass(frozen=True)
class ResumeSection:
    title: str
    claims: tuple[ResumeClaim, ...]


@dataclass(frozen=True)
class ResumeDraft:
    target_company: str
    target_role: str
    summary: ResumeClaim
    sections: tuple[ResumeSection, ...]
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def claims(self) -> list[ResumeClaim]:
        return [self.summary] + [
            claim for section in self.sections for claim in section.claims
        ]

