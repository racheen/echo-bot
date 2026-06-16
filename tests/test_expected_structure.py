from pathlib import Path
from unittest import TestCase


class ExpectedStructureTests(TestCase):
    def test_requested_directories_exist(self) -> None:
        expected = [
            "packages/echo_core/domain/profile.py",
            "packages/echo_core/domain/evidence.py",
            "packages/echo_core/domain/job.py",
            "packages/echo_core/domain/conversation.py",
            "packages/echo_core/rag/retrieval.py",
            "packages/echo_core/rag/chunking.py",
            "packages/echo_core/rag/citations.py",
            "packages/echo_core/embeddings/ollama_embeddings.py",
            "packages/echo_core/embeddings/lancedb_index.py",
            "packages/echo_core/prompts",
            "packages/echo_core/profile_schema",
            "packages/echo_core/repositories/sqlite",
            "packages/echo_core/integrations/ollama.py",
            "packages/echo_core/evaluation",
            "packages/echo_resume/desktop_app",
            "packages/echo_resume/latex_generator",
            "packages/echo_resume/job_analyzer",
            "packages/echo_resume/evidence_review",
            "packages/echo_resume/resume_generator",
            "packages/echo_resume/claim_validator",
            "packages/echo_resume/pdf_compiler",
            "packages/echo_web_bot/public_chat_widget",
            "packages/echo_web_bot/public_profile_index",
            "packages/echo_web_bot/guardrails",
            "packages/echo_web_bot/local_server",
            "apps/echo_desktop",
            "apps/echo_web",
            "legacy/streamlit_rag",
        ]
        for path in expected:
            self.assertTrue(Path(path).exists(), path)

