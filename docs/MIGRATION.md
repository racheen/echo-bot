# Echo Migration

## Implemented

- Requested package structure under `packages/`
- Runnable application packages under `apps/echo_desktop` and `apps/echo_web`
- Legacy migration directory under `legacy/streamlit_rag`
- Echo product naming and privacy contract
- Python 3.11 desktop composition root
- Platform-specific private data and log paths
- Loopback-only Ollama configuration and readiness checks
- Echo Core professional-fact domain and visibility policy
- Evidence, job, and conversation domain contracts
- SQLite authoritative profile repository under `repositories/sqlite`
- Deterministic fallback retrieval, chunking, and citation helpers
- Optional local Ollama embeddings and LanceDB adapters
- Echo Resume job analysis, evidence review, deterministic generation, claim
  validation, LaTeX rendering, local compilation, and immutable versioning
- Echo Web Bot public-profile export, guardrails, and local server
- Focused tests for expected structure, retrieval, claim validation, LaTeX
  escaping, immutable versioning, and public exports

## Remaining Work

1. Move the existing root-level legacy Streamlit files fully into
   `legacy/streamlit_rag` once import paths are adapted.
2. Add structured work-history, education, project, skill, achievement, and
   preference tables on top of personal facts.
3. Add PDF import into an unverified Echo Profile draft.
4. Add local Ollama structured-output parsing with Pydantic.
5. Connect LanceDB retrieval to Echo Chat and Echo Resume services.
6. Build profile editing, evidence review, job input, application history, and
   PDF preview screens in PySide6.
7. Add background workers for Ollama, indexing, generation, and LaTeX.
8. Expand claim validation for employers, titles, dates, and skill assertions.
9. Add approved public-profile snapshot signing/versioning.
10. Package independently for macOS and Windows using PyInstaller.
11. Retire legacy Streamlit, OpenSearch, and SentenceTransformers after feature
    parity.
