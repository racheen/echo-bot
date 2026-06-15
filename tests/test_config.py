from pathlib import Path
from unittest import TestCase

from app.config import AppPaths, validate_loopback_url
from app.errors import ConfigurationError


class LoopbackUrlTests(TestCase):
    def test_accepts_loopback_addresses(self) -> None:
        self.assertEqual(
            validate_loopback_url("http://127.0.0.1:11434"),
            "http://127.0.0.1:11434",
        )
        self.assertEqual(
            validate_loopback_url("http://localhost:11434/"),
            "http://localhost:11434",
        )

    def test_rejects_remote_hosts(self) -> None:
        with self.assertRaises(ConfigurationError):
            validate_loopback_url("https://example.com")


class AppPathsTests(TestCase):
    def test_paths_are_grouped_under_private_root(self) -> None:
        paths = AppPaths(
            root=Path("/private/app"),
            database=Path("/private/app/app.sqlite3"),
            vector_index=Path("/private/app/vectors"),
            imports=Path("/private/app/imports"),
            applications=Path("/private/app/applications"),
            logs=Path("/private/logs"),
        )
        self.assertTrue(paths.database.is_relative_to(paths.root))
        self.assertTrue(paths.vector_index.is_relative_to(paths.root))
        self.assertTrue(paths.imports.is_relative_to(paths.root))
        self.assertTrue(paths.applications.is_relative_to(paths.root))

