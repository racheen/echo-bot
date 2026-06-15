"""Offline-readiness checks that never install or download dependencies."""

from __future__ import annotations

import importlib.util
import json
import shutil
import urllib.error
import urllib.request
from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from app.config import AppConfig


class CheckStatus(str, Enum):
    READY = "ready"
    MISSING = "missing"
    ERROR = "error"


@dataclass(frozen=True)
class ReadinessCheck:
    name: str
    status: CheckStatus
    message: str


def check_python_packages(packages: Iterable[str]) -> list[ReadinessCheck]:
    return [
        ReadinessCheck(
            name=f"Python package: {package}",
            status=(
                CheckStatus.READY
                if importlib.util.find_spec(package) is not None
                else CheckStatus.MISSING
            ),
            message=(
                "Installed."
                if importlib.util.find_spec(package) is not None
                else "Install the declared local dependency."
            ),
        )
        for package in packages
    ]


def check_executable(command: str, display_name: str) -> ReadinessCheck:
    if shutil.which(command):
        return ReadinessCheck(display_name, CheckStatus.READY, "Available locally.")
    return ReadinessCheck(
        display_name, CheckStatus.MISSING, f"Install '{command}' locally and retry."
    )


def check_ollama(config: AppConfig, timeout_seconds: float = 2.0) -> list[ReadinessCheck]:
    request = urllib.request.Request(
        f"{config.ollama_url}/api/tags",
        method="GET",
        headers={"Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            payload = json.load(response)
    except (OSError, urllib.error.URLError, json.JSONDecodeError) as exc:
        return [
            ReadinessCheck(
                "Ollama service",
                CheckStatus.ERROR,
                f"Could not inspect the configured loopback Ollama service: {exc}",
            )
        ]

    model_names = {
        model.get("name")
        for model in payload.get("models", [])
        if isinstance(model, dict)
    }
    checks = [
        ReadinessCheck("Ollama service", CheckStatus.READY, "Available on loopback.")
    ]
    for purpose, model in (
        ("generation", config.generation_model),
        ("embedding", config.embedding_model),
    ):
        checks.append(
            ReadinessCheck(
                f"Ollama {purpose} model",
                CheckStatus.READY if model in model_names else CheckStatus.MISSING,
                (
                    f"Model '{model}' is installed."
                    if model in model_names
                    else f"Install model '{model}' manually with Ollama."
                ),
            )
        )
    return checks


def run_readiness_checks(config: AppConfig) -> list[ReadinessCheck]:
    checks = check_python_packages(
        ("PySide6", "pydantic", "platformdirs", "lancedb", "jinja2", "ollama")
    )
    checks.append(check_executable(config.latex_command, "LaTeX compiler"))
    checks.extend(check_ollama(config))
    return checks

