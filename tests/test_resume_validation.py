from unittest import TestCase

from packages.echo_core.domain.profile import FactType, PersonalFact, Visibility
from packages.echo_resume.claim_validator import ClaimValidationError, validate_draft
from packages.echo_resume.domain import ResumeClaim, ResumeDraft, ResumeSection


class ResumeValidationTests(TestCase):
    def setUp(self) -> None:
        self.fact = PersonalFact(
            "Improved API response time by 25%",
            FactType.ACHIEVEMENT,
            verified=True,
            visibility=Visibility.RESUME_ALLOWED,
        )

    def test_accepts_cited_supported_claim(self) -> None:
        draft = self._draft("Improved API response time by 25%", (self.fact.id,))
        validate_draft(draft, [self.fact])

    def test_rejects_unsupported_number(self) -> None:
        draft = self._draft("Improved API response time by 80%", (self.fact.id,))
        with self.assertRaises(ClaimValidationError):
            validate_draft(draft, [self.fact])

    def test_rejects_claim_without_citation(self) -> None:
        with self.assertRaises(ClaimValidationError):
            validate_draft(self._draft("Built APIs", ()), [self.fact])

    @staticmethod
    def _draft(text: str, fact_ids: tuple[str, ...]) -> ResumeDraft:
        claim = ResumeClaim(text, fact_ids)
        return ResumeDraft("Example", "Engineer", claim, (ResumeSection("Work", ()),))

