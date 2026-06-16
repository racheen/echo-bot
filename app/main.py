"""Desktop application entry point."""

from __future__ import annotations

import sys

from app.config import AppConfig
from app.errors import ConfigurationError
from app.logging_config import configure_logging


def main() -> int:
    try:
        config = AppConfig.from_environment()
    except ConfigurationError as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 1

    config.paths.ensure_exists()
    configure_logging(config.paths.logs)

    try:
        from PySide6.QtWidgets import QApplication
    except ImportError:
        print(
            "PySide6 is not installed. Install the declared local dependencies first.",
            file=sys.stderr,
        )
        return 1

    from packages.echo_core.repositories.sqlite import SQLiteProfileRepository
    from packages.echo_resume.desktop_app.main_window import EchoMainWindow

    repository = SQLiteProfileRepository(config.paths.database)
    repository.migrate()

    application = QApplication(sys.argv)
    window = EchoMainWindow(repository, config.paths.root)
    window.show()
    return application.exec()


if __name__ == "__main__":
    raise SystemExit(main())
