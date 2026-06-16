from unittest import TestCase

from packages.echo_core.domain.profile import FactType, PersonalFact, Visibility


class PersonalFactTests(TestCase):
    def test_normalizes_string_enum_values_from_ui(self) -> None:
        fact = PersonalFact(
            text="Built a local RAG system",
            fact_type="project",  # type: ignore[arg-type]
            visibility="resume_allowed",  # type: ignore[arg-type]
        )

        self.assertIs(fact.fact_type, FactType.PROJECT)
        self.assertIs(fact.visibility, Visibility.RESUME_ALLOWED)
