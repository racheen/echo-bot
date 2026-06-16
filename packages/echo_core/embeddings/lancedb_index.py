"""Optional rebuildable LanceDB index for verified personal facts."""

from __future__ import annotations

from pathlib import Path
from typing import Callable, Sequence

from packages.echo_core.domain.profile import PersonalFact
from packages.echo_core.rag.retrieval import RetrievedFact

EmbeddingFunction = Callable[[Sequence[str]], list[list[float]]]


class LanceDBFactIndex:
    def __init__(self, path: Path, embed: EmbeddingFunction) -> None:
        self.path = path
        self.embed = embed

    def rebuild(self, facts: Sequence[PersonalFact]) -> None:
        try:
            import lancedb
        except ImportError as exc:
            raise RuntimeError("Install lancedb to build the vector index.") from exc
        eligible = [fact for fact in facts if fact.verified]
        if not eligible:
            return
        vectors = self.embed([fact.text for fact in eligible])
        rows = [
            {"id": fact.id, "text": fact.text, "vector": vector}
            for fact, vector in zip(eligible, vectors, strict=True)
        ]
        self.path.mkdir(parents=True, exist_ok=True)
        database = lancedb.connect(self.path)
        database.create_table("personal_facts", data=rows, mode="overwrite")

    def search(
        self, query: str, facts_by_id: dict[str, PersonalFact], limit: int = 5
    ) -> list[RetrievedFact]:
        try:
            import lancedb
        except ImportError as exc:
            raise RuntimeError("Install lancedb to search the vector index.") from exc
        table = lancedb.connect(self.path).open_table("personal_facts")
        rows = table.search(self.embed([query])[0]).limit(limit).to_list()
        return [
            RetrievedFact(fact=facts_by_id[row["id"]], score=float(1 - row["_distance"]))
            for row in rows
            if row["id"] in facts_by_id
        ]

