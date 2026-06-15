import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from packages.echo_core.domain.profile import FactType, PersonalFact, Visibility
from packages.echo_web_bot.guardrails.policy import is_public_question_allowed
from packages.echo_web_bot.public_profile_index.exporter import export_public_profile


class FakePublicRepository:
    def __init__(self, facts: list[PersonalFact]) -> None:
        self.facts = facts

    def list_public(self) -> list[PersonalFact]:
        return [fact for fact in self.facts if fact.public_eligible]


class PublicExportTests(TestCase):
    def test_exports_only_public_verified_facts(self) -> None:
        public = PersonalFact(
            "Built Echo",
            FactType.PROJECT,
            verified=True,
            visibility=Visibility.PUBLIC_ALLOWED,
        )
        private = PersonalFact("Private email", FactType.CONTACT, verified=True)
        with TemporaryDirectory() as directory:
            destination = Path(directory) / "public.json"
            export_public_profile(FakePublicRepository([public, private]), destination)
            payload = json.loads(destination.read_text(encoding="utf-8"))
        self.assertEqual([item["id"] for item in payload], [public.id])

    def test_rejects_private_questions(self) -> None:
        self.assertFalse(is_public_question_allowed("What is her personal email?"))
        self.assertTrue(is_public_question_allowed("What projects has she built?"))

