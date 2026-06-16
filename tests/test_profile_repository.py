from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from packages.echo_core.domain.profile import FactType, PersonalFact, Visibility
from packages.echo_core.repositories.sqlite_profile import SQLiteProfileRepository


class SQLiteProfileRepositoryTests(TestCase):
    def test_filters_verified_resume_and_public_facts(self) -> None:
        with TemporaryDirectory() as directory:
            repository = SQLiteProfileRepository(Path(directory) / "echo.sqlite3")
            repository.migrate()
            facts = [
                PersonalFact("Private draft", FactType.WORK),
                PersonalFact(
                    "Resume fact",
                    FactType.WORK,
                    verified=True,
                    visibility=Visibility.RESUME_ALLOWED,
                ),
                PersonalFact(
                    "Public fact",
                    FactType.PROJECT,
                    verified=True,
                    visibility=Visibility.PUBLIC_ALLOWED,
                ),
            ]
            for fact in facts:
                repository.save(fact)

            self.assertEqual(len(repository.list_verified()), 2)
            self.assertEqual(len(repository.list_resume_eligible()), 2)
            self.assertEqual(repository.list_public(), [facts[2]])

    def test_updates_and_deletes_imported_fact(self) -> None:
        with TemporaryDirectory() as directory:
            repository = SQLiteProfileRepository(Path(directory) / "echo.sqlite3")
            repository.migrate()
            draft = PersonalFact("Imported draft bullet for review", FactType.RESUME_BULLET)
            repository.save(draft)

            verified = PersonalFact(
                id=draft.id,
                text="Verified resume bullet for review",
                fact_type=FactType.RESUME_BULLET,
                verified=True,
                visibility=Visibility.RESUME_ALLOWED,
                source=draft.source,
                created_at=draft.created_at,
            )
            repository.save(verified)

            saved = repository.get(draft.id)
            self.assertIsNotNone(saved)
            self.assertTrue(saved.verified)  # type: ignore[union-attr]
            self.assertEqual(saved.visibility, Visibility.RESUME_ALLOWED)  # type: ignore[union-attr]

            repository.delete(draft.id)
            self.assertIsNone(repository.get(draft.id))
