# Migration Plan

## Product Boundaries

- Echo Bot is the private local desktop shell and orchestration layer.
- Echo Profile owns verified professional facts and is the source of truth.
- Echo Resume owns job analysis, evidence review, constrained generation,
  validation, LaTeX rendering, and application versions.
- Echo Chat owns private career and resume conversations grounded in approved
  Echo Profile facts.

## Current Status

Phase 1 inspection is complete. Phase 2 foundations are in progress.

Implemented foundations:

- Python 3.11-compatible `app/` package and desktop entry point
- private runtime paths through `platformdirs`
- loopback-only Ollama URL validation
- readiness checks that never install or download models
- typed base errors
- metadata-only logging outside the repository
- initial privacy-focused ignores and tests

The current Python 3.11 virtual environment still needs the newly declared
desktop dependencies installed. Until migration parity is reached, the legacy
dependencies remain declared so existing work is not broken.

## Remaining Phases

1. Add SQLite schema, migrations, repositories, and profile-management UI.
2. Add resume PDF import into an unverified draft profile.
3. Add Ollama embeddings and rebuildable LanceDB retrieval.
4. Add job-posting input and validated structured analysis.
5. Add evidence review and evidence-constrained generation.
6. Add deterministic claim validation.
7. Add controlled LaTeX rendering, compilation, and PDF preview.
8. Add immutable application versioning.
9. Complete focused tests, privacy hardening, documentation, and PyInstaller
   packaging for Windows and macOS.

## Legacy Replacement Map

- `Welcome.py` and `pages/`: replace with PySide6 UI under `app/ui/`.
- `src/chat.py`: replace with constrained generation services and local Ollama
  integration.
- `src/embeddings.py`: replace with Ollama embeddings.
- `src/opensearch.py` and `src/ingestion.py`: replace with SQLite repositories
  and LanceDB.
- `src/ocr.py` and text cleaning concepts: adapt into local PDF import services.
