"""Gateway compatibility wrapper around the managed local runtime."""

from __future__ import annotations

import sys

from scripts.runtime_ctl import main as runtime_main


def main() -> int:
    argv = sys.argv[1:]
    if not argv:
        print("Usage: python -m scripts.gateway_ctl <start|stop|restart|status>")
        return 1

    command = argv[0]
    if command not in {"start", "stop", "restart", "status"}:
        print("Usage: python -m scripts.gateway_ctl <start|stop|restart|status>")
        return 1

    return runtime_main([command, "--component", "gateway"])


if __name__ == "__main__":
    raise SystemExit(main())
