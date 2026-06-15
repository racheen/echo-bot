"""Deterministic baseline job-posting analyzer."""

from __future__ import annotations

import re

from packages.echo_resume.domain import JobAnalysis


def analyze_job_posting(text: str, company: str = "", role: str = "") -> JobAnalysis:
    lowered = text.lower()
    skill_terms = (
        "python",
        "typescript",
        "javascript",
        "react",
        "next.js",
        "sql",
        "postgresql",
        "aws",
        "docker",
        "kubernetes",
        "machine learning",
    )
    skills = tuple(skill for skill in skill_terms if skill in lowered)
    keywords = tuple(
        sorted(
            {
                match.group(0).lower()
                for match in re.finditer(r"\b[A-Z][A-Za-z0-9.+#-]{2,}\b", text)
            }
        )
    )
    return JobAnalysis(
        company=company,
        role=role,
        required_skills=skills,
        keywords=keywords,
    )

