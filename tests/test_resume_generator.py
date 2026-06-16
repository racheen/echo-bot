from unittest import TestCase

from packages.echo_core.domain.profile import FactType, PersonalFact, Visibility
from packages.echo_resume.domain import JobAnalysis
from packages.echo_resume.resume_generator import ResumeGenerator


class ResumeGeneratorTests(TestCase):
    def test_generates_cited_claims_from_approved_facts(self) -> None:
        fact = PersonalFact(
            "Built local RAG systems",
            FactType.PROJECT,
            verified=True,
            visibility=Visibility.RESUME_ALLOWED,
        )
        draft = ResumeGenerator().generate(JobAnalysis("Acme", "Engineer"), [fact])
        self.assertEqual(draft.summary.fact_ids, (fact.id,))
        self.assertEqual(draft.sections[0].claims[0].fact_ids, (fact.id,))

