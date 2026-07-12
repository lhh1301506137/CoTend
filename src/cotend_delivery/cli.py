from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .core import Artifact, DeliveryError, DeliveryManager, OPERATIONS


CANDIDATE_REQUIRED_OPERATIONS = {"install", "update", "repair", "migrate_identity"}


def repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="cotend-delivery",
        description=(
            "Preview or apply the project-scoped CoTend delivery lifecycle. "
            "Mutation commands are dry-run unless --apply is provided."
        ),
    )
    parser.add_argument("operation", choices=sorted(OPERATIONS))
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument(
        "--repository",
        type=Path,
        default=repository_root(),
        help="CoTend repository containing codex-skills and framework.lock.json",
    )
    parser.add_argument("--source", type=Path)
    parser.add_argument("--source-release-id")
    parser.add_argument("--artifact-id")
    parser.add_argument("--revision", type=int)
    parser.add_argument("--protocol")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply the exact printed plan; without this flag no files are changed",
    )
    return parser.parse_args(argv)


def candidate_from_args(args: argparse.Namespace) -> Artifact:
    if args.source is None:
        return Artifact.from_repository(args.repository)
    if (
        not args.source_release_id
        or not args.artifact_id
        or args.revision is None
        or not args.protocol
    ):
        raise DeliveryError(
            "candidate_identity_required",
            "--source requires --source-release-id, --artifact-id, --revision, and --protocol",
        )
    return Artifact.from_directory(
        args.source,
        source_release_id=args.source_release_id,
        artifact_id=args.artifact_id,
        revision=args.revision,
        protocol=args.protocol,
    )


def candidate_for_operation(args: argparse.Namespace) -> Artifact | None:
    if args.source is not None:
        return candidate_from_args(args)
    if args.source_release_id or args.artifact_id or args.revision is not None or args.protocol:
        raise DeliveryError(
            "candidate_source_required",
            "Candidate identity arguments can only be used with --source",
        )
    if args.operation in CANDIDATE_REQUIRED_OPERATIONS | {"inspect"}:
        return candidate_from_args(args)
    return None


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        candidate_diagnostic: dict[str, object] | None = None
        try:
            candidate = candidate_for_operation(args)
        except DeliveryError as exc:
            if args.operation != "inspect" or args.source is not None:
                raise
            candidate = None
            candidate_diagnostic = exc.as_dict()
        manager = DeliveryManager(args.project)
        result = manager.execute(
            args.operation,
            candidate,
            apply=args.apply,
        )
        if candidate_diagnostic is not None:
            result["candidate_diagnostic"] = candidate_diagnostic
    except DeliveryError as exc:
        print(json.dumps(exc.as_dict(), indent=2, ensure_ascii=False), file=sys.stderr)
        return 2
    except OSError as exc:
        error = DeliveryError(
            "filesystem_error",
            f"The delivery operation could not access the filesystem: {exc}",
        )
        print(json.dumps(error.as_dict(), indent=2, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0
