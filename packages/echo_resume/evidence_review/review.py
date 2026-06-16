"""Manual evidence approval models."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EvidenceApproval:
    approved_fact_ids: tuple[str, ...]

    def is_approved(self, fact_id: str) -> bool:
        return fact_id in self.approved_fact_ids

