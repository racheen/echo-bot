from unittest import TestCase

from packages.echo_core.domain.profile import FactType, PersonalFact, Visibility
from packages.echo_resume.fit_scoring import score_job_fit


class FitScoringTests(TestCase):
    def test_scores_matching_terms_from_resume_facts(self) -> None:
        facts = [
            PersonalFact(
                "Built Python FastAPI services on AWS",
                FactType.WORK,
                verified=True,
                visibility=Visibility.RESUME_ALLOWED,
            )
        ]

        score = score_job_fit("Need Python, FastAPI, AWS, and Docker", facts)

        self.assertEqual(score.score, 80)
        self.assertEqual(score.matched_terms, ("api", "aws", "fastapi", "python"))
        self.assertEqual(score.missing_terms, ("docker",))
