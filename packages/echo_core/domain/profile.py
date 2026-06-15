"""Professional profile domain models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from uuid import uuid4


class FactType(str, Enum):
    CONTACT = "contact"
    WORK = "work"
    EDUCATION = "education"
    SKILL = "skill"
    PROJECT = "project"
    ACHIEVEMENT = "achievement"
    PREFERENCE = "preference"
    RESUME_BULLET = "resume_bullet"


class Visibility(str, Enum):
    PRIVATE = "private"
    RESUME_ALLOWED = "resume_allowed"
    PUBLIC_ALLOWED = "public_allowed"


@dataclass(frozen=True)
class PersonalFact:
    text: str
    fact_type: FactType
    verified: bool = False
    visibility: Visibility = Visibility.PRIVATE
    source: str | None = None
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        if not self.text.strip():
            raise ValueError("Personal facts must contain text.")

    @property
    def resume_eligible(self) -> bool:
        return self.verified and self.visibility in {
            Visibility.RESUME_ALLOWED,
            Visibility.PUBLIC_ALLOWED,
        }

    @property
    def public_eligible(self) -> bool:
        return self.verified and self.visibility is Visibility.PUBLIC_ALLOWED

