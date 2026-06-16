"""Import structured profile JSON into draft personal facts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from packages.echo_core.domain.profile import FactType, PersonalFact, Visibility

SECTION_TYPES = {
    "achievements": FactType.ACHIEVEMENT,
    "accomplishments": FactType.ACHIEVEMENT,
    "education": FactType.EDUCATION,
    "preferences": FactType.PREFERENCE,
    "projects": FactType.PROJECT,
    "skills": FactType.SKILL,
    "work": FactType.WORK,
    "work_experience": FactType.WORK,
    "work_history": FactType.WORK,
}


def import_profile_json(path: Path) -> list[PersonalFact]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Profile JSON must be an object with profile sections.")

    facts: list[PersonalFact] = []
    for key, value in payload.items():
        fact_type = SECTION_TYPES.get(key.lower())
        if fact_type is None:
            continue
        facts.extend(_facts_from_value(value, fact_type, f"json:{path.name}:{key}"))
    return facts


def _facts_from_value(value: Any, fact_type: FactType, source: str) -> list[PersonalFact]:
    if isinstance(value, list):
        facts: list[PersonalFact] = []
        for item in value:
            facts.extend(_facts_from_value(item, fact_type, source))
        return facts
    if isinstance(value, dict):
        return [PersonalFact(_dict_to_fact_text(value), fact_type, source=source)]
    if isinstance(value, str) and value.strip():
        return [PersonalFact(value.strip(), fact_type, source=source)]
    return []


def _dict_to_fact_text(value: dict[str, Any]) -> str:
    fields: list[str] = []
    for key, item in value.items():
        if item in (None, "", [], {}):
            continue
        label = key.replace("_", " ").strip().title()
        if isinstance(item, list):
            rendered = "; ".join(str(entry) for entry in item if entry)
        elif isinstance(item, dict):
            rendered = "; ".join(
                f"{child_key}: {child_value}"
                for child_key, child_value in item.items()
                if child_value
            )
        else:
            rendered = str(item)
        fields.append(f"{label}: {rendered}")
    return " | ".join(fields)

