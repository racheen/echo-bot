# Echo Architecture

## Product Boundaries

Echo is organized as a Python monorepo that builds on the existing repository.
The legacy Streamlit application remains operational while shared behavior is
extracted into product packages.

```text
Echo desktop application
  -> Echo Resume and Echo Chat services
    -> Echo Core domain and interfaces
      -> SQLite, LanceDB, Ollama, and local LaTeX adapters

Echo Web Bot
  -> exported public-profile snapshot only
```

## Package Ownership

### Echo Core

`packages/echo_core` owns:

- Professional facts, verification state, and visibility policy
- SQLite profile repository
- Text normalization, chunking, retrieval contracts, and prompts
- Loopback-only Ollama adapter
- Rebuildable LanceDB adapter
- Retrieval and citation evaluation helpers

SQLite is authoritative. LanceDB stores only derived embeddings referencing
stable SQLite fact IDs.

### Echo Resume

`packages/echo_resume` owns:

- Job-posting analysis
- Evidence selection
- Structured resume drafts and cited claims
- Deterministic claim validation
- Controlled LaTeX rendering
- Local PDF compilation
- Immutable application versions
- Resume-specific desktop UI

Every generated personal claim must cite one or more verified facts approved for
resume use.

### Echo Web Bot

`packages/echo_web_bot` owns:

- Explicit public-profile export
- Public chat widget integration boundary
- Public question and response guardrails

The web bot must never open the private SQLite database or private LanceDB
index. It consumes only an exported snapshot of verified `public_allowed`
facts.

### Application Shell

`app` owns desktop startup, configuration, dependency readiness, privacy-safe
logging, background-worker composition, and user-facing errors.

## Legacy Compatibility

`src`, `pages`, and `Welcome.py` remain the legacy prototype. Reusable concepts
are extracted into packages before legacy dependencies are removed. OpenSearch,
SentenceTransformers, Streamlit, and automatic Ollama model pulling are not part
of the target architecture.
