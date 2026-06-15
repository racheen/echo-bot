"""Echo Chat prompt construction."""

from __future__ import annotations

from packages.echo_core.domain.profile import PersonalFact


def build_career_chat_prompt(question: str, facts: list[PersonalFact]) -> str:
    evidence = "\n".join(f"- [{fact.id}] {fact.text}" for fact in facts)
    return (
        "You are Echo, a private career assistant. Use only the supplied personal "
        "facts for claims about the user. Cite personal fact IDs. Clearly label "
        "general career guidance as general guidance.\n\n"
        f"Verified personal facts:\n{evidence or '- None'}\n\n"
        f"Question: {question}\nAnswer:"
    )

