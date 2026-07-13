from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .core import DeliveryError, OPERATIONS
from .production_resolver import (
    inspect_production_user_layout,
    resolve_production_user_layout,
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="cotend-user-delivery",
        description=(
            "Resolve and inspect the production user layout without changing it. "
            "Production apply is not available in this build."
        ),
    )
    parser.add_argument(
        "operation",
        choices=sorted(OPERATIONS),
        nargs="?",
        default="inspect",
    )
    parser.add_argument("--home", type=Path)
    parser.add_argument("--codex-home", type=Path)
    parser.add_argument(
        "--expected-layout-fingerprint",
        help="Compare a previously recorded layout identity without changing state",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Reserved for a future separately authorized production lifecycle",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.apply:
            raise DeliveryError(
                "production_apply_forbidden",
                "Production user delivery is read-only in this build",
            )
        layout = resolve_production_user_layout(
            home=args.home,
            codex_home=args.codex_home,
        )
        result = inspect_production_user_layout(
            layout,
            expected_layout_fingerprint=args.expected_layout_fingerprint,
        )
        result.update(
            {
                "status": "preview",
                "operation": args.operation,
                "apply": False,
            }
        )
    except DeliveryError as exc:
        print(json.dumps(exc.as_dict(), indent=2, ensure_ascii=False), file=sys.stderr)
        return 2
    except OSError as exc:
        error = DeliveryError(
            "filesystem_error",
            f"The read-only production preflight could not access the filesystem: {exc}",
        )
        print(json.dumps(error.as_dict(), indent=2, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0
