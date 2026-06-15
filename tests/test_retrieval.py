from unittest import TestCase

from packages.echo_core.domain.profile import FactType, PersonalFact, Visibility
from packages.echo_core.rag.retrieval import KeywordFactRetriever


class FakeRepository:
    def __init__(self, facts: list[PersonalFact]) -> None:
        self.facts = facts

    def list_verified(self) -> list[PersonalFact]:
        return [fact for fact in self.facts if fact.verified]


class KeywordFactRetrieverTests(TestCase):
    def test_returns_only_relevant_verified_facts(self) -> None:
        relevant = PersonalFact(
            "Built Python APIs and PostgreSQL services",
            FactType.WORK,
            verified=True,
            visibility=Visibility.RESUME_ALLOWED,
        )
        unverified = PersonalFact("Python Kubernetes expert", FactType.SKILL)
        retriever = KeywordFactRetriever(FakeRepository([relevant, unverified]))

        results = retriever.search("Python PostgreSQL")

        self.assertEqual([result.fact for result in results], [relevant])

