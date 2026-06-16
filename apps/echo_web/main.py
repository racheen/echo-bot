"""Local Echo Web Bot server entry point."""

from __future__ import annotations

import argparse
from pathlib import Path

from packages.echo_web_bot.local_server.server import run


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the local Echo public-profile server.")
    parser.add_argument("public_profile", type=Path)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8765, type=int)
    args = parser.parse_args()
    run(args.public_profile, args.host, args.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

