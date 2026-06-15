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

