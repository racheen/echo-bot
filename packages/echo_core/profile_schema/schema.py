"""Structured private professional profile schema."""

from __future__ import annotations

from dataclasses import dataclass

from packages.echo_core.domain.profile import PersonalFact


@dataclass(frozen=True)
class StructuredProfile:
    contact: tuple[PersonalFact, ...] = ()
    work_history: tuple[PersonalFact, ...] = ()
    education: tuple[PersonalFact, ...] = ()
    skills: tuple[PersonalFact, ...] = ()
    projects: tuple[PersonalFact, ...] = ()
    achievements: tuple[PersonalFact, ...] = ()
    preferences: tuple[PersonalFact, ...] = ()

    def facts(self) -> tuple[PersonalFact, ...]:
        return (
            self.contact
            + self.work_history
            + self.education
            + self.skills
            + self.projects
            + self.achievements
            + self.preferences
        )

