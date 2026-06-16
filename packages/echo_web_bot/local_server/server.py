"""Tiny local HTTP server app for public Echo profile responses."""

from __future__ import annotations

from pathlib import Path
from wsgiref.simple_server import make_server


def create_app(public_profile_path: Path):
    def app(environ, start_response):
        if environ.get("PATH_INFO") != "/profile":
            start_response("404 Not Found", [("Content-Type", "application/json")])
            return [b'{"error": "not_found"}']
        payload = public_profile_path.read_text(encoding="utf-8")
        start_response("200 OK", [("Content-Type", "application/json")])
        return [payload.encode("utf-8")]

    return app


def run(public_profile_path: Path, host: str = "127.0.0.1", port: int = 8765) -> None:
    with make_server(host, port, create_app(public_profile_path)) as server:
        server.serve_forever()

