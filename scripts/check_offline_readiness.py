"""Print local dependency and model readiness without downloading anything."""

from __future__ import annotations

from app.config import AppConfig
from app.errors import ConfigurationError
from app.integrations.system_checks import CheckStatus, run_readiness_checks


def main() -> int:
    try:
        config = AppConfig.from_environment()
    except ConfigurationError as exc:
        print(f"[MISSING] Configuration bootstrap: {exc}")
        print("Install the declared local dependencies, then run this check again.")
        return 1

    checks = run_readiness_checks(config)
    for check in checks:
        print(f"[{check.status.value.upper():7}] {check.name}: {check.message}")
    return 0 if all(check.status is CheckStatus.READY for check in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
