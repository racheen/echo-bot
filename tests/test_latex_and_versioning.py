from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from packages.echo_resume.domain import ResumeClaim, ResumeDraft, ResumeSection
from packages.echo_resume.latex_generator import escape_latex, render_resume
from packages.echo_resume.versioning import ImmutableVersionStore


class LatexTests(TestCase):
    def test_escapes_reserved_characters(self) -> None:
        self.assertEqual(escape_latex("R&D 25%"), r"R\&D 25\%")

    def test_renders_controlled_resume(self) -> None:
        claim = ResumeClaim("Built R&D systems", ("fact-1",))
        draft = ResumeDraft("Example", "Engineer", claim, (ResumeSection("Work", (claim,)),))
        rendered = render_resume(draft)
        self.assertIn(r"R\&D", rendered)
        self.assertIn(r"\documentclass", rendered)


class VersioningTests(TestCase):
    def test_versions_are_immutable(self) -> None:
        claim = ResumeClaim("Built systems", ("fact-1",))
        draft = ResumeDraft("Example", "Engineer", claim, ())
        with TemporaryDirectory() as directory:
            store = ImmutableVersionStore(Path(directory))
            store.save("application-1", 1, draft)
            with self.assertRaises(FileExistsError):
                store.save("application-1", 1, draft)

