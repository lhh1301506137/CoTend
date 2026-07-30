#!/usr/bin/env python3
"""Deterministically maintain the CoTend router block in project AGENTS.md."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


CONTRACT = "cotend.project-router.v1"
START_MARKER = "<!-- COTEND:PROJECT-ROUTER:START -->"
END_MARKER = "<!-- COTEND:PROJECT-ROUTER:END -->"
TAG_RE = re.compile(r"^[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*$")
UTF8_BOM = b"\xef\xbb\xbf"


class RouterError(ValueError):
    """Fail-closed input or managed-block error."""


@dataclass(frozen=True)
class Document:
    text: str
    newline: str
    bom: bool


def normalize_tag(raw: str) -> str:
    value = raw.strip().replace("_", "-")
    if not TAG_RE.fullmatch(value):
        raise RouterError(f"invalid_normalized_tag:{raw}")
    parts = value.split("-")
    normalized = [parts[0].lower()]
    for part in parts[1:]:
        if len(part) == 4 and part.isalpha():
            normalized.append(part.title())
        elif (len(part) == 2 and part.isalpha()) or (
            len(part) == 3 and part.isdigit()
        ):
            normalized.append(part.upper())
        else:
            normalized.append(part.lower())
    result = "-".join(normalized)
    if result != raw:
        raise RouterError(f"normalized_tag_not_canonical:{raw}")
    return result


def detect_newline(text: str) -> str:
    first_lf = text.find("\n")
    if first_lf > 0 and text[first_lf - 1] == "\r":
        return "\r\n"
    return "\n"


def decode_document(data: bytes) -> Document:
    bom = data.startswith(UTF8_BOM)
    payload = data[len(UTF8_BOM) :] if bom else data
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RouterError("agents_invalid_utf8") from exc
    return Document(text=text, newline=detect_newline(text), bom=bom)


def encode_document(document: Document, text: str) -> bytes:
    payload = text.encode("utf-8")
    return (UTF8_BOM + payload) if document.bom else payload


def render_router_block(normalized_tag: str, newline: str = "\n") -> str:
    tag = normalize_tag(normalized_tag)
    if tag.casefold().startswith("zh"):
        rows = (
            START_MARKER,
            "## CoTend 项目路由",
            "",
            f"- 路由合同：`{CONTRACT}`。",
            "- 在会话首次进入、恢复或收到 `继续`，以及处理 L0-L2/主链语义、验收/完成/发布/风险、路线重基、审查、无人值守或多模型工作时，先加载 `$cotend-collaboration`，再按其单层路由读取必要模块。",
            "- 已确认路线内、范围明确且孤立的 L3/L4 工作可保持轻路径，不要求加载全部 CoTend 协议。",
            "- 对显式专用 Skill（例如 `$cotend-session-handoff`）的自然语言近似请求，只提示用户输入字面调用；不得加载其工作流、读取项目或生成产物。",
            END_MARKER,
        )
    else:
        rows = (
            START_MARKER,
            "## CoTend Project Routing",
            "",
            f"- Routing contract: `{CONTRACT}`.",
            "- At first session entry, resume, or `继续`, and for L0-L2/main-chain semantics, acceptance/completion/release/risk, route rebase, review, unattended, or multi-model work, load `$cotend-collaboration` first and then only its triggered one-level modules.",
            "- Ordinary isolated L3/L4 work inside a confirmed route may stay lightweight; do not preload the full CoTend protocol.",
            "- For a natural-language approximation of an explicit-only Skill such as `$cotend-session-handoff`, only suggest its literal invocation; do not load its workflow, inspect the project, or generate artifacts.",
            END_MARKER,
        )
    return newline.join(rows)


def replace_or_append(text: str, normalized_tag: str, newline: str) -> str:
    start_count = text.count(START_MARKER)
    end_count = text.count(END_MARKER)
    if start_count != end_count:
        raise RouterError("managed_marker_pair_incomplete")
    if start_count > 1:
        raise RouterError("managed_marker_pair_duplicate")

    block = render_router_block(normalized_tag, newline)
    if start_count == 1:
        start = text.index(START_MARKER)
        end_start = text.index(END_MARKER)
        if end_start < start:
            raise RouterError("managed_marker_order_invalid")
        end = end_start + len(END_MARKER)
        return text[:start] + block + text[end:]

    if not text:
        return block + newline
    if text.endswith(newline * 2):
        separator = ""
    elif text.endswith(newline):
        separator = newline
    else:
        separator = newline * 2
    return text + separator + block + newline


def load_document(path: Path) -> tuple[Document, bool]:
    if path.is_symlink():
        raise RouterError("agents_symlink_forbidden")
    if not path.exists():
        return Document(text="", newline="\n", bom=False), False
    if not path.is_file():
        raise RouterError("agents_not_regular_file")
    return decode_document(path.read_bytes()), True


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile(
        mode="wb",
        prefix=f".{path.name}.cotend-router.",
        suffix=".tmp",
        dir=path.parent,
        delete=False,
    )
    temporary = Path(handle.name)
    try:
        with handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def update_agents(
    project_root: Path, normalized_tag: str, *, apply: bool
) -> dict[str, object]:
    root = project_root.resolve()
    if not root.is_dir():
        raise RouterError("project_root_missing_or_not_directory")
    path = root / "AGENTS.md"
    document, existed = load_document(path)
    updated = replace_or_append(document.text, normalized_tag, document.newline)
    current_bytes = encode_document(document, document.text)
    updated_bytes = encode_document(document, updated)
    changed = updated_bytes != current_bytes

    if apply and changed:
        atomic_write(path, updated_bytes)

    result = (
        "created"
        if apply and changed and not existed
        else "updated"
        if apply and changed
        else "unchanged"
        if not changed
        else "drift"
    )
    return {
        "contract": CONTRACT,
        "result": result,
        "path": "AGENTS.md",
        "normalized_tag": normalized_tag,
        "changed": changed,
        "sha256": hashlib.sha256(updated_bytes).hexdigest(),
        "byte_count": len(updated_bytes),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Maintain or check the project-root CoTend AGENTS router block."
    )
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--normalized-tag", required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        normalized_tag = normalize_tag(args.normalized_tag)
        packet = update_agents(
            Path(args.project_root), normalized_tag, apply=bool(args.apply)
        )
    except (OSError, RouterError) as exc:
        packet = {
            "contract": CONTRACT,
            "result": "blocked",
            "reason": str(exc),
        }
        sys.stdout.write(json.dumps(packet, ensure_ascii=False, sort_keys=True) + "\n")
        return 3

    sys.stdout.write(json.dumps(packet, ensure_ascii=False, sort_keys=True) + "\n")
    return 2 if args.check and packet["result"] == "drift" else 0


if __name__ == "__main__":
    raise SystemExit(main())
