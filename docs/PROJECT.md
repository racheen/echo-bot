# Echo Bot

## Product Summary

Echo Bot is a private, cross-platform, local-first desktop career assistant. It
runs locally with Python 3.11 and PySide6 and uses only locally installed Ollama
models.

## Product Modules

### Echo Profile

The user's private professional knowledge base and authoritative source of
verified career facts. It stores structured contact details, work history,
education, skills, projects, accomplishments, and verified resume bullets.

### Echo Resume

An evidence-constrained tailored LaTeX resume generator. It analyzes local job
postings, retrieves approved facts from Echo Profile, requires citations for
every generated claim, validates the draft, and creates immutable PDF versions.

### Echo Chat

An AI version of the user for private resume and career questions. It answers
using approved Echo Profile facts and must distinguish supported personal facts
from general career guidance.

### Echo Bot

The desktop shell and local orchestration layer that connects Echo Profile,
Echo Resume, Echo Chat, Ollama, SQLite, LanceDB, and local LaTeX tooling.

Echo Bot stores structured profile and application data in SQLite.
Verified personal facts can be embedded into LanceDB for local retrieval. The
vector index is derived data and must always be rebuildable from SQLite.

## Privacy Contract

- Never send profile, resume, job-posting, prompt, or generated data externally.
- Only connect to explicitly configured loopback Ollama addresses.
- Never automatically pull or download models.
- Never use remote APIs, analytics, telemetry, CDNs, or remote fonts.
- Never log private content, prompts, or model responses.
- Store private runtime data outside the repository using `platformdirs`.

## Core Workflow

1. Create or import a structured profile.
2. Manually verify imported facts.
3. Save and analyze a job posting locally.
4. Retrieve relevant verified personal facts.
5. Review and approve evidence.
6. Generate a structured resume with evidence citations.
7. Reject unsupported claims deterministically.
8. Render and compile a controlled local LaTeX template.
9. Save an immutable application version and PDF.

## Architecture

The new application lives under `app/`. UI code, domain logic, services,
repositories, vector storage, and local-system integrations must remain
separate. The old Streamlit/OpenSearch application remains temporarily during
the migration and should not be extended.

See `docs/MIGRATION.md` for implementation status and sequencing.
