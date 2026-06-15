"""Application configuration and private runtime paths."""

from __future__ import annotations

import ipaddress
import os
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

from app.errors import ConfigurationError

APP_NAME = "Echo Bot"
APP_AUTHOR = "Echo"
DEFAULT_OLLAMA_URL = "http://127.0.0.1:11434"


def _user_data_dir() -> Path:
    try:
        from platformdirs import user_data_path
    except ImportError as exc:
        raise ConfigurationError(
            "platformdirs is required to resolve private application storage."
        ) from exc
    return Path(user_data_path(APP_NAME, APP_AUTHOR, ensure_exists=False))


def _user_log_dir() -> Path:
    try:
        from platformdirs import user_log_path
    except ImportError as exc:
        raise ConfigurationError(
            "platformdirs is required to resolve private application logs."
        ) from exc
    return Path(user_log_path(APP_NAME, APP_AUTHOR, ensure_exists=False))


def validate_loopback_url(url: str) -> str:
    """Return a normalized HTTP URL after enforcing a loopback-only host."""
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ConfigurationError("Ollama URL must be an HTTP URL with a host.")

    hostname = parsed.hostname.removesuffix(".")
    if hostname == "localhost":
        return url.rstrip("/")

    try:
        address = ipaddress.ip_address(hostname)
    except ValueError as exc:
        raise ConfigurationError("Ollama URL must use a loopback address.") from exc

    if not address.is_loopback:
        raise ConfigurationError("Ollama URL must use a loopback address.")
    return url.rstrip("/")


@dataclass(frozen=True)
class AppPaths:
    root: Path
    database: Path
    vector_index: Path
    imports: Path
    applications: Path
    logs: Path

    @classmethod
    def default(cls) -> "AppPaths":
        root = _user_data_dir()
        return cls(
            root=root,
            database=root / "resume_tailor.sqlite3",
            vector_index=root / "vector_index",
            imports=root / "imports",
            applications=root / "applications",
            logs=_user_log_dir(),
        )

    def ensure_exists(self) -> None:
        for path in (
            self.root,
            self.vector_index,
            self.imports,
            self.applications,
            self.logs,
        ):
            path.mkdir(parents=True, exist_ok=True)


@dataclass(frozen=True)
class AppConfig:
    paths: AppPaths
    ollama_url: str
    generation_model: str
    embedding_model: str
    latex_command: str

    @classmethod
    def from_environment(cls) -> "AppConfig":
        return cls(
            paths=AppPaths.default(),
            ollama_url=validate_loopback_url(
                os.environ.get("RESUME_TAILOR_OLLAMA_URL", DEFAULT_OLLAMA_URL)
            ),
            generation_model=os.environ.get(
                "RESUME_TAILOR_GENERATION_MODEL", "llama3.2:3b"
            ),
            embedding_model=os.environ.get(
                "RESUME_TAILOR_EMBEDDING_MODEL", "nomic-embed-text"
            ),
            latex_command=os.environ.get("RESUME_TAILOR_LATEX_COMMAND", "pdflatex"),
        )
