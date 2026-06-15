from unittest import TestCase
from unittest.mock import patch

from app.integrations.system_checks import CheckStatus, check_executable


class ExecutableCheckTests(TestCase):
    @patch("app.integrations.system_checks.shutil.which", return_value=None)
    def test_reports_missing_executable(self, _which: object) -> None:
        result = check_executable("pdflatex", "LaTeX compiler")
        self.assertIs(result.status, CheckStatus.MISSING)

