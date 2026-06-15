from unittest import TestCase

from packages.echo_core.chat import EchoChatService
from packages.echo_core.domain.profile import FactType, PersonalFact
from packages.echo_core.rag.retrieval import RetrievedFact


class FakeRetriever:
    def __init__(self, fact: PersonalFact) -> None:
        self.fact = fact

    def search(self, query: str, limit: int = 5) -> list[RetrievedFact]:
        return [RetrievedFact(self.fact, 1.0)]


class FakeGenerator:
    def __init__(self) -> None:
        self.prompt = ""

    def generate(self, prompt: str, temperature: float = 0.2) -> str:
        self.prompt = prompt
        return "Supported answer"


class EchoChatServiceTests(TestCase):
    def test_answers_with_retrieved_fact_citations_in_prompt(self) -> None:
        fact = PersonalFact("Built Echo", FactType.PROJECT, verified=True)
        generator = FakeGenerator()
        service = EchoChatService(FakeRetriever(fact), generator)

        self.assertEqual(service.answer("What did I build?"), "Supported answer")
        self.assertIn(fact.id, generator.prompt)
        self.assertIn("Built Echo", generator.prompt)
