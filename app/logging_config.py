"""Privacy-safe application logging."""

from __future__ import annotations

import logging
from pathlib import Path


def configure_logging(log_dir: Path) -> None:
    """Configure metadata-only logging outside the repository."""
    log_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=log_dir / "application.log",
        filemode="a",
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        level=logging.INFO,
        force=True,
    )

