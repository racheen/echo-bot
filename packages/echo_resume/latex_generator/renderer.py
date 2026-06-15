"""Controlled resume LaTeX renderer."""

from __future__ import annotations

from packages.echo_resume.domain import ResumeDraft

LATEX_ESCAPES = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def escape_latex(value: str) -> str:
    return "".join(LATEX_ESCAPES.get(character, character) for character in value)


def render_resume(draft: ResumeDraft) -> str:
    sections = []
    for section in draft.sections:
        claims = "\n".join(
            rf"\item {escape_latex(claim.text)}" for claim in section.claims
        )
        sections.append(
            rf"\section*{{{escape_latex(section.title)}}}"
            "\n\\begin{itemize}\n"
            f"{claims}\n"
            "\\end{itemize}"
        )
    return (
        "\\documentclass[11pt]{article}\n"
        "\\usepackage[margin=0.7in]{geometry}\n"
        "\\begin{document}\n"
        f"\\section*{{{escape_latex(draft.target_role)}}}\n"
        f"{escape_latex(draft.summary.text)}\n"
        f"{chr(10).join(sections)}\n"
        "\\end{document}\n"
    )

