"""Job-posting domain models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4


@dataclass(frozen=True)
class JobPosting:
    raw_text: str
    company: str = ""
    role: str = ""
    id: str = ""
    created_at: datetime | None = None

    def __post_init__(self) -> None:
        if not self.raw_text.strip():
            raise ValueError("Job postings must contain text.")
        if not self.id:
            object.__setattr__(self, "id", str(uuid4()))
        if self.created_at is None:
            object.__setattr__(self, "created_at", datetime.now(UTC))

