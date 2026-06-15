# Echo

Echo is a private, local-first AI career assistant built on top of the original
Echo Bot and local RAG prototypes.

Echo contains three product surfaces:

- Echo Core provides the private professional profile, RAG, prompts, local
  integrations, repositories, and evaluation contracts.
- Echo Resume creates evidence-constrained tailored LaTeX resumes from local job
  postings.
- Echo Web Bot exposes an explicitly approved public-profile snapshot and can
  never access the private profile database.

The legacy Streamlit and OpenSearch application remains available while its
useful behavior is migrated into Echo Core. New features should use the package
architecture rather than extending `src/` or `pages/`.

## Privacy Contract

- All private inference uses locally installed Ollama models.
- Ollama connections are restricted to explicitly configured loopback URLs.
- Models are never downloaded or pulled automatically.
- SQLite is the authoritative private data store.
- LanceDB is a rebuildable local vector index.
- Private profile content, prompts, job postings, and generated responses are
  never written to application logs.
- Private runtime data is stored outside the repository.
- Public web exports contain only verified facts explicitly marked
  `public_allowed`.

## Repository Structure

```text
app/
  Desktop composition root, configuration, readiness checks, and logging.

packages/
  echo_core/
    Shared profile domain, SQLite repository, RAG, prompts, Ollama adapter,
    LanceDB adapter, and evaluation helpers.
  echo_resume/
    Job analysis, claim validation, LaTeX rendering, PDF compilation,
    immutable versions, and desktop UI boundary.
  echo_web_bot/
    Public-profile export, public chat boundary, and guardrails.

src/ and pages/
  Legacy Streamlit/OpenSearch prototype retained during migration.

tests/
  Focused privacy, retrieval, validation, rendering, and versioning tests.
```

## Setup

Echo requires Python 3.11.

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m scripts.check_offline_readiness
```

Install the configured Ollama generation and embedding models manually. Echo
will report missing models but will not download them.

Run the desktop shell:

```bash
python -m app.main
```

Run the test suite:

```bash
python -m unittest discover -s tests -v
```

## Configuration

Echo recognizes these environment variables:

```text
ECHO_OLLAMA_URL=http://127.0.0.1:11434
ECHO_GENERATION_MODEL=llama3.2:3b
ECHO_EMBEDDING_MODEL=nomic-embed-text
ECHO_LATEX_COMMAND=pdflatex
```

The older `RESUME_TAILOR_*` names remain temporary fallbacks during migration.

## Documentation

- `docs/PROJECT.md` describes the product and privacy contract.
- `docs/ARCHITECTURE.md` defines module ownership and dependency direction.
- `docs/MIGRATION.md` tracks migration status and remaining work.
- `AGENTS.md` contains repository guidance for coding agents.
