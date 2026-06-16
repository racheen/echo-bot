import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from packages.echo_core.domain.profile import FactType, Visibility
from packages.echo_core.profile_schema import import_profile_json


class ProfileJsonImporterTests(TestCase):
    def test_imports_known_sections_as_typed_draft_facts(self) -> None:
        with TemporaryDirectory() as directory:
            path = Path(directory) / "profile.json"
            path.write_text(
                json.dumps(
                    {
                        "education": [
                            {"school": "Example University", "degree": "BSc"}
                        ],
                        "work_history": [
                            {
                                "title": "Backend Engineer",
                                "company": "Acme",
                                "bullets": ["Built FastAPI services"],
                            }
                        ],
                        "projects": ["Echo local career assistant"],
                        "skills": ["Python", "FastAPI"],
                    }
                ),
                encoding="utf-8",
            )

            facts = import_profile_json(path)

        self.assertEqual(
            [fact.fact_type for fact in facts],
            [
                FactType.EDUCATION,
                FactType.WORK,
                FactType.PROJECT,
                FactType.SKILL,
                FactType.SKILL,
            ],
        )
        self.assertTrue(all(not fact.verified for fact in facts))
        self.assertTrue(all(fact.visibility is Visibility.PRIVATE for fact in facts))

