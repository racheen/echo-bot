"""Filesystem-backed immutable application versions."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from packages.echo_resume.domain import ResumeDraft


class ImmutableVersionStore:
    def __init__(self, root: Path) -> None:
        self.root = root

    def save(self, application_id: str, version: int, draft: ResumeDraft) -> Path:
        version_path = self.root / application_id / f"v{version:04d}"
        version_path.mkdir(parents=True, exist_ok=False)
        (version_path / "draft.json").write_text(
            json.dumps(asdict(draft), default=str, indent=2),
            encoding="utf-8",
        )
        return version_path

