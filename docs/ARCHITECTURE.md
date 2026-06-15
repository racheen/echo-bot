# Echo Architecture

## Dependency Direction

Echo Bot is the desktop composition root. Product modules depend on shared
domain contracts, not on UI widgets or concrete infrastructure.

```text
Echo Bot UI
  -> application services
    -> Echo Profile / Echo Resume / Echo Chat domain contracts
      -> repository and integration interfaces
        -> SQLite / LanceDB / Ollama / LaTeX implementations
```

## Module Ownership

### Echo Profile

- Owns structured professional facts and verification status.
- Stores authoritative data in SQLite.
- Publishes verified fact IDs for retrieval and citation.
- Rebuilds its LanceDB projection from SQLite.

### Echo Resume

- Owns job postings, structured job analysis, evidence selection, resume
  drafts, claim validation, LaTeX rendering, and immutable output versions.
- May only generate personal claims from approved Echo Profile fact IDs.

### Echo Chat

- Owns private career and resume conversations.
- Grounds personal answers in approved Echo Profile facts.
- Keeps general career guidance clearly separate from personal claims.

### Echo Bot

- Owns navigation, configuration, background workers, dependency readiness,
  and user-facing error presentation.
- Does not own professional facts or generated resume content.

## Infrastructure Rules

- SQLite is authoritative; LanceDB is disposable derived data.
- Ollama connections must use explicitly configured loopback addresses.
- Models are inspected but never pulled automatically.
- LaTeX compilation runs locally in an isolated application output directory.
- Private content is never included in application logs.
