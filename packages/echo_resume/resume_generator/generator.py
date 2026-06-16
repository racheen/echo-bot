"""Evidence-constrained resume draft generation."""

from __future__ import annotations

from packages.echo_core.domain.profile import PersonalFact
from packages.echo_resume.domain import JobAnalysis, ResumeClaim, ResumeDraft, ResumeSection


class ResumeGenerator:
    """Deterministic baseline generator used before local LLM generation is wired in."""

    def generate(
        self, job: JobAnalysis, approved_facts: list[PersonalFact]
    ) -> ResumeDraft:
        if not approved_facts:
            raise ValueError("At least one approved fact is required.")

        summary_fact = approved_facts[0]
        claims = tuple(
            ResumeClaim(text=fact.text, fact_ids=(fact.id,)) for fact in approved_facts
        )
        return ResumeDraft(
            target_company=job.company,
            target_role=job.role,
            summary=ResumeClaim(summary_fact.text, (summary_fact.id,)),
            sections=(ResumeSection("Relevant Experience", claims),),
        )

