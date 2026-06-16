"""SQLite source-of-truth repository for professional facts."""

from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

from packages.echo_core.domain.profile import FactType, PersonalFact, Visibility


class SQLiteProfileRepository:
    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path

    def migrate(self) -> None:
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS personal_facts (
                    id TEXT PRIMARY KEY,
                    fact_type TEXT NOT NULL,
                    text TEXT NOT NULL,
                    verified INTEGER NOT NULL CHECK (verified IN (0, 1)),
                    visibility TEXT NOT NULL,
                    source TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )

    def save(self, fact: PersonalFact) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO personal_facts (
                    id, fact_type, text, verified, visibility, source,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    fact_type = excluded.fact_type,
                    text = excluded.text,
                    verified = excluded.verified,
                    visibility = excluded.visibility,
                    source = excluded.source,
                    updated_at = excluded.updated_at
                """,
                (
                    fact.id,
                    fact.fact_type.value,
                    fact.text,
                    int(fact.verified),
                    fact.visibility.value,
                    fact.source,
                    fact.created_at.isoformat(),
                    fact.updated_at.isoformat(),
                ),
            )

    def get(self, fact_id: str) -> PersonalFact | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM personal_facts WHERE id = ?", (fact_id,)
            ).fetchone()
        return self._from_row(row) if row else None

    def delete(self, fact_id: str) -> None:
        with self._connect() as connection:
            connection.execute("DELETE FROM personal_facts WHERE id = ?", (fact_id,))

    def list_all(self) -> list[PersonalFact]:
        return self._list("SELECT * FROM personal_facts ORDER BY created_at, id")

    def list_verified(self) -> list[PersonalFact]:
        return self._list(
            "SELECT * FROM personal_facts WHERE verified = 1 ORDER BY created_at, id"
        )

    def list_resume_eligible(self) -> list[PersonalFact]:
        return self._list(
            """
            SELECT * FROM personal_facts
            WHERE verified = 1 AND visibility IN (?, ?)
            ORDER BY created_at, id
            """,
            (Visibility.RESUME_ALLOWED.value, Visibility.PUBLIC_ALLOWED.value),
        )

    def list_public(self) -> list[PersonalFact]:
        return self._list(
            """
            SELECT * FROM personal_facts
            WHERE verified = 1 AND visibility = ?
            ORDER BY created_at, id
            """,
            (Visibility.PUBLIC_ALLOWED.value,),
        )

    def _list(
        self, query: str, parameters: tuple[object, ...] = ()
    ) -> list[PersonalFact]:
        with self._connect() as connection:
            rows = connection.execute(query, parameters).fetchall()
        return [self._from_row(row) for row in rows]

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    @staticmethod
    def _from_row(row: sqlite3.Row) -> PersonalFact:
        return PersonalFact(
            id=row["id"],
            fact_type=FactType(row["fact_type"]),
            text=row["text"],
            verified=bool(row["verified"]),
            visibility=Visibility(row["visibility"]),
            source=row["source"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )
