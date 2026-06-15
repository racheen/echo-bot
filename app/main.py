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
        from PySide6.QtWidgets import QApplication, QLabel, QMainWindow
    except ImportError:
        print(
            "PySide6 is not installed. Install the declared local dependencies first.",
            file=sys.stderr,
        )
        return 1

    application = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Echo Bot")
    window.setMinimumSize(960, 640)
    window.setCentralWidget(
        QLabel(
            "Echo Bot\n"
            "Your private, local career assistant\n\n"
            "Echo Profile, Echo Resume, and Echo Chat are being implemented."
        )
    )
    window.show()
    return application.exec()


if __name__ == "__main__":
    raise SystemExit(main())
