# Echo Bot Agent Guide

## Project Purpose

This repository is Echo Bot, a private, cross-platform, local-first career
assistant. It is being migrated from a generic Streamlit/OpenSearch document
chat application.

The product modules are:

- Echo Profile: private professional knowledge base and source of truth.
- Echo Resume: evidence-constrained tailored LaTeX resume generator.
- Echo Chat: AI version of the user for resume and career questions.
- Echo Bot: desktop shell and orchestration layer for the product modules.

Read `docs/PROJECT.md` before making architectural changes and
`docs/ARCHITECTURE.md` and `docs/MIGRATION.md` before continuing implementation.

## Non-Negotiable Rules

- Use Python 3.11 and PySide6 for the desktop application.
- Keep UI, domain logic, services, repositories, and integrations separate.
- SQLite is authoritative. LanceDB is rebuildable derived data.
- Use only locally installed Ollama models.
- Never automatically download or pull models.
- Only connect to explicitly configured loopback addresses.
- Never send or log private resume, profile, job, prompt, or generated content.
- Store private runtime data outside the repository using `platformdirs`.
- Preserve unrelated worktree changes.

## Migration Guidance

New application code belongs under `app/`. Do not add features to the legacy
Streamlit/OpenSearch application. Adapt reusable PDF extraction concepts only
when they fit the new privacy and architecture requirements.

Generated resume claims must cite verified personal-fact IDs and pass
deterministic validation before LaTeX rendering.

Update `docs/MIGRATION.md` as implementation phases materially progress.

## Verification

Prefer focused tests for retrieval, claim validation, immutable versioning,
LaTeX escaping/rendering, configuration, and privacy boundaries.

Use Conventional Commits for commits.
