from unittest import TestCase

from packages.echo_core.rag.chunking import chunk_text, clean_text
from packages.echo_core.rag.citations import extract_fact_citations, render_fact_citation


class RagHelpersTests(TestCase):
    def test_chunking_uses_requested_module(self) -> None:
        self.assertEqual(clean_text("hello-\nworld"), "helloworld")
        self.assertEqual(
            chunk_text("one two three four", chunk_size=2, overlap=1),
            ["one two", "two three", "three four", "four"],
        )

    def test_fact_citation_round_trip(self) -> None:
        citation = render_fact_citation("fact-1")
        self.assertEqual(extract_fact_citations(f"Used {citation}"), ("fact-1",))

