"""Export only verified facts explicitly approved for public use."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Protocol

from packages.echo_core.domain.profile import PersonalFact


class PublicFactRepository(Protocol):
    def list_public(self) -> list[PersonalFact]: ...


def export_public_profile(repository: PublicFactRepository, destination: Path) -> Path:
    facts = repository.list_public()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(
            [{"id": fact.id, "type": fact.fact_type.value, "text": fact.text} for fact in facts],
            indent=2,
        ),
        encoding="utf-8",
    )
    return destination

