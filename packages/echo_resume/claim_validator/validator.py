"""Deterministic evidence validation for generated resume claims."""

from __future__ import annotations

import re

from packages.echo_core.domain.profile import PersonalFact
from packages.echo_resume.domain import ResumeDraft


class ClaimValidationError(ValueError):
    pass


def _numbers(text: str) -> set[str]:
    return set(re.findall(r"\b\d+(?:\.\d+)?%?\b", text))


def validate_draft(draft: ResumeDraft, facts: list[PersonalFact]) -> None:
    facts_by_id = {fact.id: fact for fact in facts}
    errors: list[str] = []

    for claim in draft.claims():
        if not claim.fact_ids:
            errors.append(f"Claim has no citations: {claim.text}")
            continue
        cited_facts = [facts_by_id.get(fact_id) for fact_id in claim.fact_ids]
        if any(fact is None for fact in cited_facts):
            errors.append(f"Claim cites unknown facts: {claim.text}")
            continue
        if any(not fact.resume_eligible for fact in cited_facts if fact is not None):
            errors.append(f"Claim cites facts not approved for resumes: {claim.text}")
            continue
        supported_numbers = {
            number
            for fact in cited_facts
            if fact is not None
            for number in _numbers(fact.text)
        }
        unsupported_numbers = _numbers(claim.text) - supported_numbers
        if unsupported_numbers:
            errors.append(
                f"Claim contains unsupported numbers {sorted(unsupported_numbers)}: "
                f"{claim.text}"
            )

    if errors:
        raise ClaimValidationError("\n".join(errors))

