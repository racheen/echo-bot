"""Backward-compatible import for the SQLite profile repository."""

from packages.echo_core.repositories.sqlite.profile_repository import (
    SQLiteProfileRepository,
)

__all__ = ["SQLiteProfileRepository"]
