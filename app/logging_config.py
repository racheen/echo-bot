"""Privacy-safe application logging."""

from __future__ import annotations

import logging
import sys
from pathlib import Path


def configure_logging(log_dir: Path) -> None:
    """Configure metadata-only logging outside the repository."""
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
        handler: logging.Handler = logging.FileHandler(
            log_dir / "application.log", mode="a"
        )
    except OSError:
        handler = logging.StreamHandler(sys.stderr)

    logging.basicConfig(
        handlers=[handler],
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        level=logging.INFO,
        force=True,
    )
