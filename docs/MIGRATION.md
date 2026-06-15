# Echo Migration

## Implemented

- Echo product naming and privacy contract
- Python 3.11 desktop composition root
- Platform-specific private data and log paths
- Loopback-only Ollama configuration and readiness checks
- Echo Core professional-fact domain and visibility policy
- SQLite authoritative profile repository
- Deterministic fallback retrieval and text processing
- Optional local Ollama and LanceDB adapters
- Echo Chat controlled prompt foundation
- Echo Resume job analysis, cited draft model, claim validation, LaTeX
  rendering, local compilation, and immutable versioning
- Echo Web Bot public-profile export and initial guardrails
- Focused tests for configuration, profile filtering, retrieval, claim
  validation, LaTeX escaping, immutable versioning, and public exports

## Build-on-Top Strategy

The legacy Streamlit RAG application is preserved during migration. Its useful
PDF extraction, chat streaming, and retrieval concepts will be adapted behind
Echo Core interfaces. New functionality must not add new dependencies on
OpenSearch, SentenceTransformers, or Streamlit.

## Remaining Work

1. Add structured work-history, education, project, skill, achievement, and
   preference tables on top of personal facts.
2. Add PDF import into an unverified Echo Profile draft.
3. Add local Ollama structured-output parsing with Pydantic.
4. Connect LanceDB retrieval to Echo Chat and Echo Resume services.
5. Build profile editing, evidence review, job input, application history, and
   PDF preview screens in PySide6.
6. Add background workers for Ollama, indexing, generation, and LaTeX.
7. Expand claim validation for employers, titles, dates, and skill assertions.
8. Add approved public-profile snapshot signing/versioning.
9. Package independently for macOS and Windows using PyInstaller.
10. Retire legacy Streamlit, OpenSearch, and SentenceTransformers after feature
    parity.
