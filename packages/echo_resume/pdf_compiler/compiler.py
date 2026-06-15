"""Compile controlled LaTeX locally without shell execution."""

from __future__ import annotations

import subprocess
from pathlib import Path


def compile_pdf(tex_path: Path, latex_command: str = "pdflatex") -> Path:
    result = subprocess.run(
        [
            latex_command,
            "-interaction=nonstopmode",
            "-halt-on-error",
            tex_path.name,
        ],
        cwd=tex_path.parent,
        capture_output=True,
        text=True,
        check=False,
        timeout=120,
    )
    if result.returncode != 0:
        raise RuntimeError("Local LaTeX compilation failed.")
    pdf_path = tex_path.with_suffix(".pdf")
    if not pdf_path.exists():
        raise RuntimeError("Local LaTeX compilation did not produce a PDF.")
    return pdf_path

