from __future__ import annotations

import argparse
from collections import Counter, deque
import hashlib
import json
import os
import queue
import re
import signal
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any, Callable, TextIO

import verify_isolated_codex_plugin as plugin_boundary


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from cotend_delivery.core import Artifact, DeliveryError, DeliveryManager  # noqa: E402


TEMPLATE_ROOT = ROOT / "tests" / "fixtures" / "g06-retained-project"
LANGUAGE_ACCEPTANCE_CONTRACT = (
    ROOT / "tests" / "fixtures" / "g06-retained-project.acceptance.json"
)
R10_COMMIT = "f2ed9cf35351e2f93c28bbcdc2691841073203c9"
R10_ID = "cotend-codex-r000010"
R10_REVISION = 10
R10_MANIFEST = "0715c20f517f906996d4882e47c664449a23cf6f7747b6a2d42835f35591b8a9"
R11_COMMIT = "13c2f51868a554c7568892c4aeaefa2fd814cb26"
R11_ID = "cotend-codex-r000011"
R11_REVISION = 11
R11_MANIFEST = "eac48844295f9ba12d64df469aa25fab9e76a8c9ceb9817857350b5029767627"
R11_SOURCE = ROOT / ".private-provenance" / "G06-real-project" / "r11-repository"
R12_ID = "cotend-codex-r000012"
R12_REVISION = 12
R12_MANIFEST = "44419b00c17ab0036477c6c3b9843f239a6a567ee714ccf7828b40a4af195276"
LEGACY_RELEASE_ID = "2026.07.23.2"
LEGACY_PROTOCOL = "cotend-collaboration-v1.65"
RELEASE_ID = "2026.07.28.1"
PROTOCOL = "cotend-collaboration-v1.66"
MODEL = "gpt-5.4-mini"
REASONING_EFFORT = "medium"
WORKSPACE_PERMISSION_CONFIG = 'default_permissions=":workspace"'
INIT_SCHEMA = "G06-INIT-RESULT.schema.json"
INIT_SKILL = ".agents/skills/cotend-init/SKILL.md"
SAFE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
WSL_USER = "cotend"
WSL_CODEX = "/usr/local/bin/codex"
WSL_CODEX_VERSION = "codex-cli 0.145.0"
WSL_RUNTIME_PARENT = PurePosixPath("/home/cotend")
WSL_SECRET_ENV_KEYS = (
    "OPENAI_API_KEY",
    "CODEX_API_KEY",
    "AZURE_OPENAI_API_KEY",
    "OPENAI_ORG_ID",
    "OPENAI_PROJECT_ID",
)
CODEX_TOTAL_TIMEOUT_SECONDS = 900.0
CODEX_INACTIVITY_TIMEOUT_SECONDS = 300.0
CODEX_EVENT_JOURNAL_LIMIT = 256
CODEX_CAPTURE_LIMIT = 1_000_000
BOUNDARY_DIFF_LIMIT = 64
SNAPSHOT_EXCLUDES = {".agents", ".git", ".codegraph", "__pycache__", ".pytest_cache"}
INIT_ALLOWED_FILES = {
    "STATUS.md",
    "REVIEW-LOG.md",
    "QUALITY-SIGNALS.md",
    "PROJECT-DECISION-LOG.md",
    "PROJECT-PLAN-TREE.md",
    "PROJECT-KNOWLEDGE-CHANGELOG.md",
}
INIT_ALLOWED_DIRECTORIES = {
    "PROJECT-PLAN-NODES",
    "PROJECT-UNDERSTANDING",
}
CJK_PATTERN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
LATIN_PATTERN = re.compile(r"[A-Za-z]")
ISOLATED_NETWORK_ENV_KEYS = {
    "ALL_PROXY",
    "CURL_CA_BUNDLE",
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "NO_PROXY",
    "REQUESTS_CA_BUNDLE",
    "SSL_CERT_DIR",
    "SSL_CERT_FILE",
}


class RealProjectAcceptanceError(RuntimeError):
    pass


class CodexProcessTimeout(RealProjectAcceptanceError):
    def __init__(self, timeout_kind: str, summary: dict[str, Any]) -> None:
        self.timeout_kind = timeout_kind
        self.summary = summary
        super().__init__(
            "Codex Init process timed out: "
            + json.dumps(summary, ensure_ascii=True, sort_keys=True)
        )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def reject_link_tree(root: Path) -> None:
    if root.is_symlink():
        raise RealProjectAcceptanceError(f"linked root is not allowed: {root}")
    if not root.exists():
        return
    for path in root.rglob("*"):
        if path.is_symlink():
            raise RealProjectAcceptanceError(f"linked project path is not allowed: {path}")


def guarded_project(project: Path, allowed_root: Path) -> Path:
    allowed = allowed_root.expanduser().resolve()
    if not allowed.is_dir() or allowed.is_symlink():
        raise RealProjectAcceptanceError("allowed project root is missing or linked")
    candidate = project.expanduser().resolve()
    try:
        relative = candidate.relative_to(allowed)
    except ValueError as exc:
        raise RealProjectAcceptanceError("project must stay under the allowed root") from exc
    if len(relative.parts) != 1 or not SAFE_NAME.fullmatch(relative.name):
        raise RealProjectAcceptanceError("project must be one safe direct child of the allowed root")
    reject_link_tree(candidate)
    return candidate


def guarded_private_source(path: Path) -> Path:
    private_root = (ROOT / ".private-provenance").resolve()
    candidate = path.expanduser().resolve()
    try:
        relative = candidate.relative_to(private_root)
    except ValueError as exc:
        raise RealProjectAcceptanceError("r10 source must stay under .private-provenance") from exc
    if not relative.parts or len(relative.parts) > 3:
        raise RealProjectAcceptanceError("r10 source path depth is invalid")
    reject_link_tree(candidate)
    return candidate


def guarded_private_runtime(path: Path) -> Path:
    private_root = (ROOT / ".private-provenance").resolve()
    candidate = path.expanduser().resolve()
    try:
        relative = candidate.relative_to(private_root)
    except ValueError as exc:
        raise RealProjectAcceptanceError(
            "isolated runtime must stay under .private-provenance"
        ) from exc
    if not relative.parts:
        raise RealProjectAcceptanceError(
            "isolated runtime cannot be the private provenance root"
        )
    reject_link_tree(candidate)
    return candidate


def pure_windows_path_to_wsl(value: str) -> str:
    candidate = PureWindowsPath(value)
    if (
        not candidate.is_absolute()
        or not re.fullmatch(r"[A-Za-z]:", candidate.drive)
        or any(part in {"", ".", ".."} for part in candidate.parts[1:])
    ):
        raise RealProjectAcceptanceError(
            "WSL path mapping requires an absolute local Windows drive path"
        )
    suffix = "/".join(candidate.parts[1:])
    return f"/mnt/{candidate.drive[0].lower()}/{suffix}"


def windows_path_to_wsl(path: Path) -> str:
    if os.name != "nt":
        raise RealProjectAcceptanceError(
            "WSL carrier path mapping is only available from Windows"
        )
    return pure_windows_path_to_wsl(str(path.expanduser().resolve()))


def guarded_wsl_runtime_root(value: str) -> PurePosixPath:
    candidate = PurePosixPath(value)
    if (
        not candidate.is_absolute()
        or candidate.parent != WSL_RUNTIME_PARENT
        or not re.fullmatch(r"g06-runtime-[A-Za-z0-9._-]+", candidate.name)
        or any(part in {"", ".", ".."} for part in candidate.parts)
    ):
        raise RealProjectAcceptanceError(
            "WSL runtime must be one g06-runtime-* child of /home/cotend"
        )
    return candidate


def wsl_runtime_environment(runtime_root: str) -> dict[str, str]:
    root = guarded_wsl_runtime_root(runtime_root)
    process_home = root / "process-home"
    return {
        "HOME": str(process_home),
        "CODEX_HOME": str(root / "codex-home"),
        "TMPDIR": str(root / "temp"),
        "XDG_CACHE_HOME": str(root / "cache" / "xdg"),
        "XDG_CONFIG_HOME": str(root / "config" / "xdg"),
        "XDG_DATA_HOME": str(root / "data" / "xdg"),
        "XDG_STATE_HOME": str(root / "state" / "xdg"),
        "NPM_CONFIG_CACHE": str(root / "cache" / "npm"),
        "PYTHONPYCACHEPREFIX": str(root / "cache" / "pycache"),
        "CI": "true",
        "DO_NOT_TRACK": "1",
        "OTEL_SDK_DISABLED": "true",
        "PYTHONIOENCODING": "utf-8",
        "PYTHONUTF8": "1",
    }


def resolve_wsl_executable(explicit: str | None = None) -> str:
    executable = explicit or shutil.which("wsl.exe")
    if executable is None:
        raise RealProjectAcceptanceError("wsl.exe is unavailable")
    return executable


def build_wsl_process_command(
    distribution: str,
    command: list[str],
    *,
    user: str = WSL_USER,
    wsl_executable: str | None = None,
) -> list[str]:
    if not SAFE_NAME.fullmatch(distribution):
        raise RealProjectAcceptanceError("WSL distribution name is unsafe")
    if not SAFE_NAME.fullmatch(user):
        raise RealProjectAcceptanceError("WSL user name is unsafe")
    if not command or any("\x00" in value for value in command):
        raise RealProjectAcceptanceError("WSL command is empty or invalid")
    return [
        resolve_wsl_executable(wsl_executable),
        "-d",
        distribution,
        "-u",
        user,
        "--",
        *command,
    ]


def run_wsl_process(
    distribution: str,
    command: list[str],
    *,
    user: str = WSL_USER,
    wsl_executable: str | None = None,
    runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    timeout: int = 60,
) -> subprocess.CompletedProcess[str]:
    return runner(
        build_wsl_process_command(
            distribution,
            command,
            user=user,
            wsl_executable=wsl_executable,
        ),
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )


def require_wsl_success(
    completed: subprocess.CompletedProcess[str],
    label: str,
) -> subprocess.CompletedProcess[str]:
    if completed.returncode != 0:
        raise RealProjectAcceptanceError(
            f"{label} failed with {completed.returncode}: "
            + redact_runtime_text(completed.stderr[-800:])
        )
    return completed


def decode_wsl_cli_output(value: bytes | str) -> str:
    if isinstance(value, str):
        return value.replace("\x00", "")
    if value.startswith((b"\xff\xfe", b"\xfe\xff")):
        return value.decode("utf-16", errors="replace")
    if b"\x00" in value[:64]:
        return value.decode("utf-16-le", errors="replace")
    return value.decode("utf-8", errors="replace")


def parse_wsl_verbose_output(value: bytes | str) -> list[dict[str, Any]]:
    distributions: list[dict[str, Any]] = []
    for raw_line in decode_wsl_cli_output(value).splitlines():
        match = re.fullmatch(
            r"\s*(?P<default>\*\s*)?(?P<name>.+?)\s{2,}"
            r"(?P<state>\S+)\s+(?P<version>[12])\s*",
            raw_line,
        )
        if match is None:
            continue
        distributions.append(
            {
                "name": match.group("name").strip(),
                "state": match.group("state"),
                "version": int(match.group("version")),
                "default_marker": match.group("default") is not None,
            }
        )
    if not distributions:
        raise RealProjectAcceptanceError("WSL distribution inventory is unreadable")
    names = [item["name"].casefold() for item in distributions]
    if len(names) != len(set(names)):
        raise RealProjectAcceptanceError("WSL distribution inventory has duplicates")
    return sorted(distributions, key=lambda item: item["name"].casefold())


def wsl_registry_defaults() -> dict[str, Any]:
    if os.name != "nt":
        raise RealProjectAcceptanceError(
            "WSL registry boundaries are only available from Windows"
        )
    import winreg

    registry_path = r"Software\Microsoft\Windows\CurrentVersion\Lxss"
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path) as key:
            default_id = str(winreg.QueryValueEx(key, "DefaultDistribution")[0])
            default_version = int(winreg.QueryValueEx(key, "DefaultVersion")[0])
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            registry_path + "\\" + default_id,
        ) as default_key:
            default_name = str(
                winreg.QueryValueEx(default_key, "DistributionName")[0]
            )
    except (FileNotFoundError, OSError, ValueError) as exc:
        raise RealProjectAcceptanceError(
            "WSL default distribution registry boundary is unreadable"
        ) from exc
    return {
        "default_distribution_id": default_id,
        "default_distribution_name": default_name,
        "default_version": default_version,
    }


def snapshot_wsl_host(
    *,
    wsl_executable: str | None = None,
    runner: Callable[..., subprocess.CompletedProcess[bytes]] = subprocess.run,
) -> dict[str, Any]:
    executable = resolve_wsl_executable(wsl_executable)
    completed = runner(
        [executable, "--list", "--verbose"],
        check=False,
        capture_output=True,
        timeout=30,
    )
    if completed.returncode != 0:
        stderr = redact_runtime_text(decode_wsl_cli_output(completed.stderr))
        raise RealProjectAcceptanceError(
            f"WSL host inventory failed with {completed.returncode}: {stderr[-800:]}"
        )
    return {
        **wsl_registry_defaults(),
        "distributions": parse_wsl_verbose_output(completed.stdout),
    }


def require_wsl_host_baseline(
    snapshot: dict[str, Any],
    distribution: str,
) -> None:
    matches = [
        item
        for item in snapshot["distributions"]
        if item["name"].casefold() == distribution.casefold()
    ]
    if len(matches) != 1:
        raise RealProjectAcceptanceError(
            "WSL carrier is absent or ambiguous in the host inventory"
        )
    carrier = matches[0]
    if carrier["state"].casefold() != "stopped" or carrier["version"] != 2:
        raise RealProjectAcceptanceError(
            "WSL carrier must begin as one stopped WSL2 distribution"
        )


def terminate_wsl_distribution(
    distribution: str,
    *,
    wsl_executable: str | None = None,
    runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
) -> None:
    executable = resolve_wsl_executable(wsl_executable)
    terminated = runner(
        [executable, "--terminate", distribution],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
    )
    require_wsl_success(terminated, "WSL distribution termination")


def probe_wsl_carrier(
    distribution: str,
    project: Path,
    *,
    wsl_executable: str | None = None,
    runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    path_mapper: Callable[[Path], str] = windows_path_to_wsl,
) -> dict[str, Any]:
    identity = require_wsl_success(
        run_wsl_process(
            distribution,
            ["/usr/bin/id", "-u"],
            wsl_executable=wsl_executable,
            runner=runner,
        ),
        "WSL identity probe",
    ).stdout.strip()
    if identity != "1000":
        raise RealProjectAcceptanceError(
            f"WSL carrier must run as uid 1000, got {identity!r}"
        )
    version = require_wsl_success(
        run_wsl_process(
            distribution,
            [WSL_CODEX, "--version"],
            wsl_executable=wsl_executable,
            runner=runner,
        ),
        "WSL Codex version probe",
    ).stdout.strip()
    if version != WSL_CODEX_VERSION:
        raise RealProjectAcceptanceError(
            f"WSL Codex version drifted: {version!r}"
        )
    linux_project = path_mapper(project)
    require_wsl_success(
        run_wsl_process(
            distribution,
            ["/usr/bin/test", "-r", f"{linux_project}/{INIT_SKILL}"],
            wsl_executable=wsl_executable,
            runner=runner,
        ),
        "WSL project Skill readability probe",
    )
    return {
        "distribution": distribution,
        "user": WSL_USER,
        "uid": 1000,
        "codex_path": WSL_CODEX,
        "codex_version": version,
        "project_path": linux_project,
    }


def prepare_wsl_runtime(
    distribution: str,
    runtime_root: str,
    auth_source: Path,
    *,
    wsl_executable: str | None = None,
    runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    path_mapper: Callable[[Path], str] = windows_path_to_wsl,
) -> dict[str, Any]:
    root = guarded_wsl_runtime_root(runtime_root)
    source = auth_source.expanduser().resolve()
    if not source.is_file() or source.is_symlink():
        raise RealProjectAcceptanceError(
            "WSL runtime requires a regular auth source file"
        )
    source_stat = source.stat()
    if source_stat.st_size <= 0:
        raise RealProjectAcceptanceError("auth source file is empty")
    absent = run_wsl_process(
        distribution,
        ["/usr/bin/test", "!", "-e", str(root)],
        wsl_executable=wsl_executable,
        runner=runner,
    )
    require_wsl_success(absent, "WSL runtime absence check")
    directories = [
        root,
        root / "codex-home",
        root / "process-home",
        root / "temp",
        root / "cache" / "xdg",
        root / "cache" / "npm",
        root / "cache" / "pycache",
        root / "config" / "xdg",
        root / "data" / "xdg",
        root / "state" / "xdg",
    ]
    require_wsl_success(
        run_wsl_process(
            distribution,
            [
                "/usr/bin/install",
                "-d",
                "-m",
                "700",
                *[str(path) for path in directories],
            ],
            wsl_executable=wsl_executable,
            runner=runner,
        ),
        "WSL runtime directory creation",
    )
    destination = root / "codex-home" / "auth.json"
    require_wsl_success(
        run_wsl_process(
            distribution,
            [
                "/usr/bin/cp",
                "--no-preserve=mode,ownership,timestamps",
                "--",
                path_mapper(source),
                str(destination),
            ],
            wsl_executable=wsl_executable,
            runner=runner,
        ),
        "WSL auth byte copy",
    )
    require_wsl_success(
        run_wsl_process(
            distribution,
            ["/usr/bin/chmod", "600", str(destination)],
            wsl_executable=wsl_executable,
            runner=runner,
        ),
        "WSL auth permission setup",
    )
    copied_size = require_wsl_success(
        run_wsl_process(
            distribution,
            ["/usr/bin/stat", "-c", "%s", str(destination)],
            wsl_executable=wsl_executable,
            runner=runner,
        ),
        "WSL auth size check",
    ).stdout.strip()
    if copied_size != str(source_stat.st_size):
        raise RealProjectAcceptanceError(
            "WSL auth copy size differs from the source"
        )
    forbidden = (
        root / "codex-home" / "config.toml",
        root / "codex-home" / "models_cache.json",
        root / "codex-home" / "plugins",
        root / "codex-home" / "skills",
        root / "process-home" / ".agents",
    )
    for path in forbidden:
        require_wsl_success(
            run_wsl_process(
                distribution,
                ["/usr/bin/test", "!", "-e", str(path)],
                wsl_executable=wsl_executable,
                runner=runner,
            ),
            f"WSL forbidden runtime source check for {path.name}",
        )
    return {
        "runtime_root": str(root),
        "auth_source_size": source_stat.st_size,
        "auth_source_mtime_ns": source_stat.st_mtime_ns,
        "auth_destination": str(destination),
        "auth_destination_size": int(copied_size),
        "auth_contents_read_by_verifier": False,
    }


def cleanup_wsl_runtime(
    distribution: str,
    runtime_root: str,
    *,
    wsl_executable: str | None = None,
    runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
) -> dict[str, Any]:
    root = guarded_wsl_runtime_root(runtime_root)
    pre_cleanup_termination_error: Exception | None = None
    try:
        terminate_wsl_distribution(
            distribution,
            wsl_executable=wsl_executable,
            runner=runner,
        )
    except Exception as exc:
        pre_cleanup_termination_error = exc
    cleanup_error: Exception | None = None
    if pre_cleanup_termination_error is None:
        try:
            resolved = require_wsl_success(
                run_wsl_process(
                    distribution,
                    ["/usr/bin/realpath", "-m", str(root)],
                    user="root",
                    wsl_executable=wsl_executable,
                    runner=runner,
                ),
                "WSL runtime realpath check",
            ).stdout.strip()
            if resolved != str(root):
                raise RealProjectAcceptanceError(
                    f"WSL runtime cleanup target drifted: {resolved!r}"
                )
            require_wsl_success(
                run_wsl_process(
                    distribution,
                    ["/usr/bin/rm", "-rf", "--", str(root)],
                    user="root",
                    wsl_executable=wsl_executable,
                    runner=runner,
                ),
                "WSL runtime cleanup",
            )
            require_wsl_success(
                run_wsl_process(
                    distribution,
                    ["/usr/bin/test", "!", "-e", str(root)],
                    user="root",
                    wsl_executable=wsl_executable,
                    runner=runner,
                ),
                "WSL runtime cleanup verification",
            )
        except Exception as exc:
            cleanup_error = exc
    post_cleanup_termination_error: Exception | None = None
    try:
        terminate_wsl_distribution(
            distribution,
            wsl_executable=wsl_executable,
            runner=runner,
        )
    except Exception as exc:
        post_cleanup_termination_error = exc
    if (
        pre_cleanup_termination_error is not None
        or cleanup_error is not None
        or post_cleanup_termination_error is not None
    ):
        errors = [
            str(error)
            for error in (
                pre_cleanup_termination_error,
                cleanup_error,
                post_cleanup_termination_error,
            )
            if error is not None
        ]
        raise RealProjectAcceptanceError("; ".join(errors))
    return {
        "runtime_root_removed": True,
        "pre_cleanup_distribution_terminated": True,
        "distribution_terminated": True,
    }


def build_isolated_runtime_env(runtime_root: Path) -> dict[str, str]:
    runtime = guarded_private_runtime(runtime_root)
    codex_home = runtime / "codex-home"
    process_home = runtime / "process-home"
    mappings = {
        "CODEX_HOME": codex_home,
        "HOME": process_home,
        "USERPROFILE": process_home,
        "TEMP": runtime / "temp",
        "TMP": runtime / "temp",
        "TMPDIR": runtime / "temp",
        "APPDATA": process_home / "AppData" / "Roaming",
        "LOCALAPPDATA": process_home / "AppData" / "Local",
        "XDG_CACHE_HOME": runtime / "cache" / "xdg",
        "XDG_CONFIG_HOME": runtime / "config" / "xdg",
        "XDG_DATA_HOME": runtime / "data" / "xdg",
        "XDG_STATE_HOME": runtime / "state" / "xdg",
        "NPM_CONFIG_CACHE": runtime / "cache" / "npm",
        "PIP_CACHE_DIR": runtime / "cache" / "pip",
        "PYTHONPYCACHEPREFIX": runtime / "cache" / "pycache",
    }
    allowed = {
        key.upper()
        for key in plugin_boundary.SAFE_INHERITED_ENV_KEYS
        | ISOLATED_NETWORK_ENV_KEYS
    }
    env = {
        key: value
        for key, value in os.environ.items()
        if key.upper() in allowed
    }
    env.update({key: str(path) for key, path in mappings.items()})
    if process_home.drive:
        env["HOMEDRIVE"] = process_home.drive
        env["HOMEPATH"] = str(process_home)[len(process_home.drive) :]
    env.update(
        {
            "CI": "true",
            "DO_NOT_TRACK": "1",
            "OTEL_SDK_DISABLED": "true",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONUTF8": "1",
        }
    )
    for path in mappings.values():
        path.mkdir(parents=True, exist_ok=True)
    auth = codex_home / "auth.json"
    if not auth.is_file() or auth.is_symlink():
        raise RealProjectAcceptanceError(
            "isolated runtime requires a regular codex-home/auth.json"
        )
    forbidden_sources = (
        codex_home / "config.toml",
        codex_home / "models_cache.json",
        codex_home / "plugins",
        codex_home / "skills",
        process_home / ".agents",
    )
    present = [
        path.relative_to(runtime).as_posix()
        for path in forbidden_sources
        if path.exists() or path.is_symlink()
    ]
    if present:
        raise RealProjectAcceptanceError(
            "isolated runtime contains forbidden global sources: "
            + ", ".join(present)
        )
    return env


def file_manifest(root: Path, *, excludes: set[str] | None = None) -> dict[str, str]:
    omitted = excludes or set()
    return {
        path.relative_to(root).as_posix(): sha256(path)
        for path in sorted(root.rglob("*"))
        if path.is_file()
        and not any(part in omitted for part in path.relative_to(root).parts)
    }


def changed_paths(before: dict[str, str], after: dict[str, str]) -> set[str]:
    return {path for path in before.keys() | after.keys() if before.get(path) != after.get(path)}


def normalize_boundary_path(path: Path) -> Path:
    value = str(path)
    if os.name == "nt":
        if value.startswith("\\\\?\\UNC\\"):
            value = "\\\\" + value[8:]
        elif value.startswith("\\\\?\\"):
            value = value[4:]
    return Path(value).resolve(strict=False)


def content_tree_digest(root: Path) -> dict[str, Any]:
    boundary_root = normalize_boundary_path(root.expanduser())
    manifest = hashlib.sha256()
    file_count = 0
    directory_count = 0
    link_count = 0
    total_bytes = 0

    def add_record(record: dict[str, Any]) -> None:
        manifest.update(
            (
                json.dumps(
                    record,
                    ensure_ascii=True,
                    separators=(",", ":"),
                    sort_keys=True,
                )
                + "\n"
            ).encode("utf-8")
        )

    def visit(path: Path, relative: str) -> None:
        nonlocal file_count, directory_count, link_count, total_bytes
        try:
            metadata = path.lstat()
        except FileNotFoundError:
            if relative == ".":
                add_record({"kind": "missing", "path": relative})
                return
            raise RealProjectAcceptanceError(
                f"Plugin content boundary disappeared during scan: {relative}"
            )
        except OSError as exc:
            raise RealProjectAcceptanceError(
                f"Plugin content boundary is unreadable at {relative}: {exc.errno}"
            ) from exc
        is_junction = getattr(path, "is_junction", lambda: False)
        if path.is_symlink() or is_junction():
            if relative == ".":
                raise RealProjectAcceptanceError(
                    "Plugin content boundary root cannot be linked"
                )
            link_count += 1
            try:
                raw_target = Path(os.readlink(path))
                target = (
                    raw_target
                    if raw_target.is_absolute()
                    else path.parent / raw_target
                )
                target = normalize_boundary_path(target)
                target_relative = target.relative_to(boundary_root).as_posix()
            except ValueError as exc:
                raise RealProjectAcceptanceError(
                    f"Plugin content boundary link escapes its root: {relative}"
                ) from exc
            except OSError as exc:
                raise RealProjectAcceptanceError(
                    f"Plugin content boundary link is unreadable: {relative}"
                ) from exc
            add_record(
                {
                    "kind": "link",
                    "path": relative,
                    "target": target_relative,
                }
            )
            return
        if path.is_file():
            file_count += 1
            total_bytes += metadata.st_size
            add_record(
                {
                    "kind": "file",
                    "path": relative,
                    "size": metadata.st_size,
                    "sha256": sha256(path),
                }
            )
            return
        if path.is_dir():
            directory_count += 1
            add_record({"kind": "directory", "path": relative})
            try:
                with os.scandir(path) as iterator:
                    entries = sorted(
                        iterator,
                        key=lambda entry: entry.name.casefold(),
                    )
            except OSError as exc:
                raise RealProjectAcceptanceError(
                    f"Plugin content boundary cannot be listed at {relative}: "
                    f"{exc.errno}"
                ) from exc
            for entry in entries:
                child_relative = (
                    entry.name
                    if relative == "."
                    else f"{relative}/{entry.name}"
                )
                visit(Path(entry.path), child_relative)
            return
        add_record({"kind": "special", "path": relative})

    visit(root, ".")
    return {
        "file_count": file_count,
        "directory_count": directory_count,
        "link_count": link_count,
        "total_bytes": total_bytes,
        "manifest_sha256": manifest.hexdigest(),
    }


def protected_plugin_content_snapshot() -> dict[str, dict[str, Any]]:
    return {
        f"global:{label}": content_tree_digest(path)
        for label, path in plugin_boundary.protected_user_paths().items()
        if label.endswith("_plugins")
    }


def stat_only_tree(root: Path) -> tuple[tuple[str, str, int, int, int], ...]:
    records: list[tuple[str, str, int, int, int]] = []

    def visit(path: Path, relative: str) -> None:
        try:
            metadata = path.lstat()
        except FileNotFoundError:
            records.append((relative, "missing", 0, 0, 0))
            return
        except OSError as exc:
            records.append((relative, f"error:{exc.errno}", 0, 0, 0))
            return
        is_junction = getattr(path, "is_junction", lambda: False)
        if path.is_symlink() or is_junction():
            kind = "link"
        elif path.is_dir():
            kind = "directory"
        elif path.is_file():
            kind = "file"
        else:
            kind = "special"
        records.append(
            (
                relative,
                kind,
                metadata.st_mode,
                metadata.st_size if kind == "file" else 0,
                metadata.st_mtime_ns,
            )
        )
        if kind != "directory":
            return
        try:
            entries = sorted(os.scandir(path), key=lambda entry: entry.name)
        except OSError as exc:
            records.append((f"{relative}/<scan>", f"error:{exc.errno}", 0, 0, 0))
            return
        for entry in entries:
            child_relative = f"{relative}/{entry.name}" if relative != "." else entry.name
            visit(Path(entry.path), child_relative)

    visit(root, ".")
    return tuple(records)


def protected_boundary_paths(
    project: Path,
    allowed_root: Path,
    extra_paths: tuple[Path, ...] = (),
) -> dict[str, Path]:
    project = project.expanduser().resolve()
    paths = {
        f"global:{label}": path
        for label, path in plugin_boundary.protected_user_paths().items()
        if not label.endswith("_root")
    }
    for index, raw_path in enumerate(extra_paths, start=1):
        path = raw_path.expanduser().resolve()
        if path == project or project in path.parents or path in project.parents:
            raise RealProjectAcceptanceError("protected path overlaps the writable project")
        paths[f"extra:{index}"] = path
    return paths


def observed_live_boundary_paths(
    project: Path,
    allowed_root: Path,
    extra_paths: tuple[Path, ...] = (),
) -> dict[str, Path]:
    project = project.expanduser().resolve()
    allowed = allowed_root.expanduser().resolve()
    paths = {
        f"uat_sibling:{child.name}": child
        for child in sorted(allowed.iterdir(), key=lambda path: path.name.casefold())
        if child.resolve() != project
    }
    for index, raw_path in enumerate(extra_paths, start=1):
        path = raw_path.expanduser().resolve()
        if path == project or project in path.parents or path in project.parents:
            raise RealProjectAcceptanceError(
                "observed path overlaps the writable project"
            )
        paths[f"observed:{index}"] = path
    return paths


def protected_boundary_snapshot(
    project: Path,
    allowed_root: Path,
    extra_paths: tuple[Path, ...] = (),
) -> dict[str, tuple[tuple[str, str, int, int, int], ...]]:
    return {
        label: stat_only_tree(path)
        for label, path in protected_boundary_paths(project, allowed_root, extra_paths).items()
    }


def observed_live_boundary_snapshot(
    project: Path,
    allowed_root: Path,
    extra_paths: tuple[Path, ...] = (),
) -> dict[str, tuple[tuple[str, str, int, int, int], ...]]:
    return {
        label: stat_only_tree(path)
        for label, path in observed_live_boundary_paths(
            project,
            allowed_root,
            extra_paths,
        ).items()
    }


def changed_boundary_labels(
    expected: dict[str, tuple[tuple[str, str, int, int, int], ...]],
    actual: dict[str, tuple[tuple[str, str, int, int, int], ...]],
) -> list[str]:
    return boundary_snapshot_differences(expected, actual)["changed_labels"]


def boundary_snapshot_differences(
    expected: dict[str, tuple[tuple[str, str, int, int, int], ...]],
    actual: dict[str, tuple[tuple[str, str, int, int, int], ...]],
    *,
    limit: int = BOUNDARY_DIFF_LIMIT,
) -> dict[str, Any]:
    if limit < 1:
        raise ValueError("boundary difference limit must be positive")
    differences: list[dict[str, Any]] = []
    difference_count = 0
    changed_labels: list[str] = []
    fields = ("kind", "mode", "size", "mtime_ns")

    def payload(
        record: tuple[str, str, int, int, int] | None,
    ) -> dict[str, Any] | None:
        if record is None:
            return None
        return dict(zip(fields, record[1:], strict=True))

    for label in sorted(expected.keys() | actual.keys()):
        before_records = {
            record[0]: record
            for record in expected.get(label, ())
        }
        after_records = {
            record[0]: record
            for record in actual.get(label, ())
        }
        label_changed = False
        for path in sorted(before_records.keys() | after_records.keys()):
            before = before_records.get(path)
            after = after_records.get(path)
            if before == after:
                continue
            label_changed = True
            difference_count += 1
            if before is None or after is None:
                changed_fields = ["presence"]
            else:
                changed_fields = [
                    field
                    for index, field in enumerate(fields, start=1)
                    if before[index] != after[index]
                ]
            if len(differences) < limit:
                differences.append(
                    {
                        "label": label,
                        "path": path,
                        "changed_fields": changed_fields,
                        "before": payload(before),
                        "after": payload(after),
                    }
                )
        if label_changed:
            changed_labels.append(label)
    return {
        "changed_labels": changed_labels,
        "difference_count": difference_count,
        "truncated": difference_count > len(differences),
        "differences": differences,
    }


def assert_protected_boundaries_unchanged(
    expected: dict[str, tuple[tuple[str, str, int, int, int], ...]],
    project: Path,
    allowed_root: Path,
    extra_paths: tuple[Path, ...] = (),
) -> None:
    actual = protected_boundary_snapshot(project, allowed_root, extra_paths)
    differences = boundary_snapshot_differences(expected, actual)
    if differences["difference_count"]:
        raise RealProjectAcceptanceError(
            "protected boundary metadata changed: "
            + json.dumps(
                differences,
                ensure_ascii=True,
                sort_keys=True,
            )
        )


def git(project: Path, *args: str, binary: bool = False) -> subprocess.CompletedProcess[Any]:
    return subprocess.run(
        ["git", *args],
        cwd=project,
        check=True,
        capture_output=True,
        text=not binary,
        encoding=None if binary else "utf-8",
        errors=None if binary else "replace",
    )


def git_head(project: Path) -> str:
    return git(project, "rev-parse", "HEAD").stdout.strip()


def git_status(project: Path) -> str:
    return git(project, "status", "--porcelain").stdout


def r10_artifact(source: Path) -> Artifact:
    artifact = Artifact.from_directory(
        source,
        source_release_id=LEGACY_RELEASE_ID,
        artifact_id=R10_ID,
        revision=R10_REVISION,
        protocol=LEGACY_PROTOCOL,
    )
    if artifact.manifest_sha256 != R10_MANIFEST:
        raise RealProjectAcceptanceError("r10 manifest differs from the frozen predecessor")
    return artifact


def validated_r11_artifact(source: Path) -> Artifact:
    artifact = Artifact.from_repository(source)
    if artifact.artifact_id != R11_ID or artifact.manifest_sha256 != R11_MANIFEST:
        raise RealProjectAcceptanceError("materialized repository does not match frozen r11")
    return artifact


def extract_r11_source(destination: Path = R11_SOURCE) -> Artifact:
    destination = guarded_private_source(destination)
    if destination.exists():
        return validated_r11_artifact(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = destination.with_name(destination.name + f".staging-{os.getpid()}")
    if staging.exists():
        raise RealProjectAcceptanceError("r11 staging path already exists")
    staging.mkdir()
    required_files = {
        "delivery/codex-artifact.lock.json",
        "upstream/framework.lock.json",
    }
    try:
        listing = git(
            ROOT,
            "ls-tree",
            "-r",
            "--name-only",
            R11_COMMIT,
            "--",
            "skills",
            *sorted(required_files),
        ).stdout
        paths = [path for path in listing.splitlines() if path]
        inventory = set(paths)
        if (
            not any(path.startswith("skills/") for path in paths)
            or required_files - inventory
            or any(
                (
                    PurePosixPath(path).is_absolute()
                    or ".." in PurePosixPath(path).parts
                    or (
                        not path.startswith("skills/")
                        and path not in required_files
                    )
                )
                for path in paths
            )
        ):
            raise RealProjectAcceptanceError("trusted r11 repository inventory is invalid")
        for repository_path in paths:
            target = staging.joinpath(*PurePosixPath(repository_path).parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            payload = git(
                ROOT,
                "show",
                f"{R11_COMMIT}:{repository_path}",
                binary=True,
            ).stdout
            target.write_bytes(payload)
        validated_r11_artifact(staging)
        staging.replace(destination)
        return validated_r11_artifact(destination)
    except Exception:
        if staging.exists():
            shutil.rmtree(staging)
        raise


def r11_artifact() -> Artifact:
    return extract_r11_source()


def r12_artifact() -> Artifact:
    artifact = Artifact.from_repository(ROOT)
    if (
        artifact.source_release_id != RELEASE_ID
        or artifact.protocol != PROTOCOL
        or artifact.artifact_id != R12_ID
        or artifact.revision != R12_REVISION
        or artifact.manifest_sha256 != R12_MANIFEST
    ):
        raise RealProjectAcceptanceError(
            "current repository does not match the frozen r12 target"
        )
    return artifact


def extract_r10_source(destination: Path) -> Artifact:
    destination = guarded_private_source(destination)
    if destination.exists():
        return r10_artifact(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = destination.with_name(destination.name + f".staging-{os.getpid()}")
    if staging.exists():
        raise RealProjectAcceptanceError("r10 staging path already exists")
    staging.mkdir()
    try:
        listing = git(ROOT, "ls-tree", "-r", "--name-only", R10_COMMIT, "--", "skills").stdout
        paths = [PurePath for PurePath in listing.splitlines() if PurePath]
        if not paths or any(not path.startswith("skills/") or ".." in Path(path).parts for path in paths):
            raise RealProjectAcceptanceError("trusted r10 Skill inventory is invalid")
        for repository_path in paths:
            relative = Path(repository_path).relative_to("skills")
            target = staging / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            payload = git(ROOT, "show", f"{R10_COMMIT}:{repository_path}", binary=True).stdout
            target.write_bytes(payload)
        artifact = r10_artifact(staging)
        staging.replace(destination)
        return Artifact.from_directory(
            destination,
            source_release_id=artifact.source_release_id,
            artifact_id=artifact.artifact_id,
            revision=artifact.revision,
            protocol=artifact.protocol,
        )
    except Exception:
        if staging.exists():
            shutil.rmtree(staging)
        raise


def prepare_project(
    project: Path,
    allowed_root: Path,
    *,
    protected_paths: tuple[Path, ...] = (),
) -> dict[str, Any]:
    project = guarded_project(project, allowed_root)
    if project.exists():
        raise RealProjectAcceptanceError("retained project already exists")
    protected = protected_boundary_snapshot(project, allowed_root, protected_paths)
    try:
        shutil.copytree(TEMPLATE_ROOT, project)
        git(project.parent, "init", "--quiet", "--initial-branch=main", str(project))
        git(project, "config", "user.name", "CoTend G06 UAT")
        git(project, "config", "user.email", "g06-uat@example.invalid")
        git(project, "add", "--all")
        git(project, "commit", "--quiet", "-m", "chore: establish G06 project brief")
        if git_status(project):
            raise RealProjectAcceptanceError("prepared retained project is not clean")
    finally:
        assert_protected_boundaries_unchanged(
            protected,
            project,
            allowed_root,
            protected_paths,
        )
    return {
        "project": str(project),
        "git_head": git_head(project),
        "brief_sha256": sha256(project / "PROJECT-BRIEF.md"),
        "baseline_files": len(file_manifest(project, excludes={".git"})),
    }


def recover_prepared_project(
    project: Path,
    allowed_root: Path,
    *,
    protected_paths: tuple[Path, ...] = (),
) -> dict[str, Any]:
    project = guarded_project(project, allowed_root)
    if not project.is_dir():
        raise RealProjectAcceptanceError("retained project is missing for prepare recovery")
    protected = protected_boundary_snapshot(project, allowed_root, protected_paths)
    try:
        actual = file_manifest(project, excludes={".git"})
        expected = file_manifest(TEMPLATE_ROOT)
        if actual != expected:
            raise RealProjectAcceptanceError("prepared project differs from the frozen template")
        if git_status(project):
            raise RealProjectAcceptanceError("prepared project is not clean")
        if git(project, "rev-list", "--count", "HEAD").stdout.strip() != "1":
            raise RealProjectAcceptanceError("prepared project does not have one baseline commit")
        if git(project, "show", "-s", "--format=%s", "HEAD").stdout.strip() != "chore: establish G06 project brief":
            raise RealProjectAcceptanceError("prepared project baseline commit message drifted")
    finally:
        assert_protected_boundaries_unchanged(
            protected,
            project,
            allowed_root,
            protected_paths,
        )
    return {
        "status": "pass",
        "recovery": "validated_existing_prepare_after_failed_boundary_check",
        "prior_attempt": "failed_closed_without_evidence_write",
        "project": str(project),
        "git_head": git_head(project),
        "brief_sha256": sha256(project / "PROJECT-BRIEF.md"),
        "baseline_files": len(actual),
    }


def require_delivery_state(
    manager: DeliveryManager,
    candidate: Artifact,
    expected_id: str,
) -> dict[str, Any]:
    state = manager.inspect(candidate)
    if (
        state.get("installation") != "complete"
        or state.get("enablement") != "enabled"
        or state.get("artifact_id") != expected_id
        or state.get("unexpected")
        or state.get("missing")
        or state.get("modified")
    ):
        raise RealProjectAcceptanceError(f"delivery state is not exact: {state}")
    return state


def deliver_r10_to_r11(
    project: Path,
    allowed_root: Path,
    source: Path,
    *,
    protected_paths: tuple[Path, ...] = (),
) -> dict[str, Any]:
    project = guarded_project(project, allowed_root)
    predecessor = r10_artifact(guarded_private_source(source))
    current = r11_artifact()
    manager = DeliveryManager(project)
    unmanaged = file_manifest(project, excludes=SNAPSHOT_EXCLUDES)
    head = git_head(project)
    protected = protected_boundary_snapshot(project, allowed_root, protected_paths)
    try:
        all_before = file_manifest(project, excludes={".git"})
        install_preview = manager.execute("install", predecessor)
        if install_preview.get("status") != "planned" or file_manifest(project, excludes={".git"}) != all_before:
            raise RealProjectAcceptanceError("r10 install preview mutated the project")
        manager.execute("install", predecessor, apply=True)
        require_delivery_state(manager, predecessor, R10_ID)
        update_before = file_manifest(project, excludes={".git"})
        update_preview = manager.execute("update", current)
        if update_preview.get("status") != "planned" or file_manifest(project, excludes={".git"}) != update_before:
            raise RealProjectAcceptanceError("r11 update preview mutated the project")
        manager.execute("update", current, apply=True)
        state = require_delivery_state(manager, current, R11_ID)
        if file_manifest(project, excludes=SNAPSHOT_EXCLUDES) != unmanaged or git_head(project) != head:
            raise RealProjectAcceptanceError("project-owned files changed during framework delivery")
        if git_status(project):
            raise RealProjectAcceptanceError("project Git became dirty during ignored delivery")
    finally:
        assert_protected_boundaries_unchanged(
            protected,
            project,
            allowed_root,
            protected_paths,
        )
    return {
        "status": "pass",
        "project_git_head": head,
        "r10_manifest": predecessor.manifest_sha256,
        "r11_manifest": current.manifest_sha256,
        "installed_artifact": state["artifact_id"],
        "managed_skills": len(current.skills),
        "managed_files": len(current.files),
        "protected_user_boundaries": len(protected),
    }


def deliver_r11_to_r12(
    project: Path,
    allowed_root: Path,
    source: Path,
    *,
    protected_paths: tuple[Path, ...] = (),
) -> dict[str, Any]:
    project = guarded_project(project, allowed_root)
    predecessor = validated_r11_artifact(guarded_private_source(source))
    current = r12_artifact()
    manager = DeliveryManager(project)
    unmanaged = file_manifest(project, excludes=SNAPSHOT_EXCLUDES)
    head = git_head(project)
    protected = protected_boundary_snapshot(project, allowed_root, protected_paths)
    try:
        all_before = file_manifest(project, excludes={".git"})
        install_preview = manager.execute("install", predecessor)
        if (
            install_preview.get("status") != "planned"
            or file_manifest(project, excludes={".git"}) != all_before
        ):
            raise RealProjectAcceptanceError("r11 install preview mutated the project")
        manager.execute("install", predecessor, apply=True)
        require_delivery_state(manager, predecessor, R11_ID)
        update_before = file_manifest(project, excludes={".git"})
        update_preview = manager.execute("update", current)
        if (
            update_preview.get("status") != "planned"
            or file_manifest(project, excludes={".git"}) != update_before
        ):
            raise RealProjectAcceptanceError("r12 update preview mutated the project")
        manager.execute("update", current, apply=True)
        state = require_delivery_state(manager, current, R12_ID)
        if (
            file_manifest(project, excludes=SNAPSHOT_EXCLUDES) != unmanaged
            or git_head(project) != head
        ):
            raise RealProjectAcceptanceError(
                "project-owned files changed during framework delivery"
            )
        if git_status(project):
            raise RealProjectAcceptanceError(
                "project Git became dirty during ignored delivery"
            )
    finally:
        assert_protected_boundaries_unchanged(
            protected,
            project,
            allowed_root,
            protected_paths,
        )
    return {
        "status": "pass",
        "project_git_head": head,
        "r11_manifest": predecessor.manifest_sha256,
        "r12_manifest": current.manifest_sha256,
        "installed_artifact": state["artifact_id"],
        "managed_skills": len(current.skills),
        "managed_files": len(current.files),
        "protected_user_boundaries": len(protected),
    }


def _build_codex_command(
    executable: str,
    project: str,
    output_schema: str,
    output: str,
    *,
    model: str,
    reasoning_effort: str,
) -> list[str]:
    return [
        executable,
        "--ask-for-approval",
        "never",
        "-c",
        WORKSPACE_PERMISSION_CONFIG,
        "--disable",
        "plugins",
        "--disable",
        "remote_plugin",
        "-c",
        f'model_reasoning_effort="{reasoning_effort}"',
        "--model",
        model,
        "exec",
        "--ephemeral",
        "--ignore-user-config",
        "--ignore-rules",
        "--json",
        "--color",
        "never",
        "--cd",
        project,
        "--output-schema",
        output_schema,
        "--output-last-message",
        output,
        "-",
    ]


def build_codex_command(
    project: Path,
    output: Path,
    *,
    model: str = MODEL,
    reasoning_effort: str = REASONING_EFFORT,
) -> list[str]:
    executable = shutil.which("codex")
    if executable is None:
        raise RealProjectAcceptanceError("Codex CLI is unavailable")
    return _build_codex_command(
        executable,
        str(project),
        str(project / INIT_SCHEMA),
        str(output),
        model=model,
        reasoning_effort=reasoning_effort,
    )


def build_wsl_codex_command(
    project: str,
    output: str,
    distribution: str,
    runtime_root: str,
    *,
    model: str = MODEL,
    reasoning_effort: str = REASONING_EFFORT,
    wsl_executable: str | None = None,
) -> list[str]:
    root = guarded_wsl_runtime_root(runtime_root)
    if not PurePosixPath(project).is_absolute() or not PurePosixPath(output).is_absolute():
        raise RealProjectAcceptanceError(
            "WSL Codex project and output paths must be absolute"
        )
    environment = wsl_runtime_environment(str(root))
    env_command = ["/usr/bin/env"]
    for name in WSL_SECRET_ENV_KEYS:
        env_command.extend(("-u", name))
    env_command.extend(f"{name}={value}" for name, value in environment.items())
    codex = _build_codex_command(
        WSL_CODEX,
        project,
        f"{project}/{INIT_SCHEMA}",
        output,
        model=model,
        reasoning_effort=reasoning_effort,
    )
    return build_wsl_process_command(
        distribution,
        [*env_command, *codex],
        wsl_executable=wsl_executable,
    )


def validate_codex_command(
    command: list[str],
    project: Path,
    *,
    carrier: str = "native",
    expected_project: str | None = None,
    expected_output: str | None = None,
    expected_model: str = MODEL,
    expected_reasoning_effort: str = REASONING_EFFORT,
    wsl_distribution: str | None = None,
    wsl_runtime_root: str | None = None,
) -> None:
    if carrier not in {"native", "wsl2"}:
        raise RealProjectAcceptanceError("Codex command carrier is invalid")
    required = {
        "--ask-for-approval",
        "--cd",
        "--ephemeral",
        "--ignore-user-config",
        "--ignore-rules",
        "--output-schema",
        "--output-last-message",
    }
    if required - set(command):
        raise RealProjectAcceptanceError("Codex command is missing isolation flags")
    forbidden = {
        "--add-dir",
        "--dangerously-bypass-approvals-and-sandbox",
        "--profile",
        "--sandbox",
        "-p",
        "-s",
        "danger-full-access",
        "workspace-write",
        ":danger-no-sandbox",
    }
    if forbidden & set(command):
        raise RealProjectAcceptanceError("Codex command widens the project boundary")
    if command[command.index("--ask-for-approval") + 1] != "never":
        raise RealProjectAcceptanceError("Codex command approval mode drifted")
    config_values = [
        command[index + 1]
        for index, value in enumerate(command[:-1])
        if value in {"-c", "--config"}
    ]
    permission_values = [
        value
        for value in config_values
        if value.startswith("default_permissions=")
    ]
    if permission_values != [WORKSPACE_PERMISSION_CONFIG]:
        raise RealProjectAcceptanceError("Codex command permission profile drifted")
    reasoning_values = [
        value
        for value in config_values
        if value.startswith("model_reasoning_effort=")
    ]
    expected_reasoning_config = (
        f'model_reasoning_effort="{expected_reasoning_effort}"'
    )
    if reasoning_values != [expected_reasoning_config]:
        raise RealProjectAcceptanceError("Codex command reasoning effort drifted")
    if "--model" not in command:
        raise RealProjectAcceptanceError("Codex command model is missing")
    if command[command.index("--model") + 1] != expected_model:
        raise RealProjectAcceptanceError("Codex command model drifted")
    command_project = expected_project or str(project)
    if command[command.index("--cd") + 1] != command_project:
        raise RealProjectAcceptanceError("Codex command project root drifted")
    expected_schema = (
        f"{command_project}/{INIT_SCHEMA}"
        if carrier == "wsl2"
        else str(project / INIT_SCHEMA)
    )
    if command[command.index("--output-schema") + 1] != expected_schema:
        raise RealProjectAcceptanceError("Codex command response schema path drifted")
    if (
        expected_output is not None
        and command[command.index("--output-last-message") + 1] != expected_output
    ):
        raise RealProjectAcceptanceError("Codex command output path drifted")
    disabled = {
        command[index + 1]
        for index, value in enumerate(command[:-1])
        if value == "--disable"
    }
    if {"plugins", "remote_plugin"} - disabled:
        raise RealProjectAcceptanceError(
            "Codex command did not disable unrelated Plugin sources"
        )
    if carrier == "wsl2":
        if wsl_distribution is None or wsl_runtime_root is None:
            raise RealProjectAcceptanceError(
                "WSL Codex command validation requires its carrier identity"
            )
        if (
            Path(command[0]).name.casefold() != "wsl.exe"
            or command[1:7]
            != ["-d", wsl_distribution, "-u", WSL_USER, "--", "/usr/bin/env"]
        ):
            raise RealProjectAcceptanceError("WSL Codex command prefix drifted")
        if WSL_CODEX not in command:
            raise RealProjectAcceptanceError("WSL Codex executable path drifted")
        codex_index = command.index(WSL_CODEX)
        if codex_index < 7:
            raise RealProjectAcceptanceError("WSL Codex environment boundary is missing")
        for name in WSL_SECRET_ENV_KEYS:
            if not any(
                command[index : index + 2] == ["-u", name]
                for index in range(7, max(7, codex_index - 1))
            ):
                raise RealProjectAcceptanceError(
                    f"WSL Codex command did not clear {name}"
                )
            if any(value.startswith(f"{name}=") for value in command):
                raise RealProjectAcceptanceError(
                    f"WSL Codex command exposed {name}"
                )
        environment = wsl_runtime_environment(wsl_runtime_root)
        for name, value in environment.items():
            if f"{name}={value}" not in command[7:codex_index]:
                raise RealProjectAcceptanceError(
                    f"WSL Codex command environment drifted for {name}"
                )


def validate_response_schema(path: Path) -> dict[str, Any]:
    try:
        schema = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RealProjectAcceptanceError("Init response schema is unreadable") from exc
    if not isinstance(schema, dict) or schema.get("type") != "object":
        raise RealProjectAcceptanceError("Init response schema must be an object")
    properties = schema.get("properties")
    required = schema.get("required")
    if not isinstance(properties, dict) or not properties:
        raise RealProjectAcceptanceError(
            "Init response schema must declare properties"
        )
    if (
        not isinstance(required, list)
        or any(not isinstance(value, str) for value in required)
        or set(required) != set(properties)
    ):
        raise RealProjectAcceptanceError(
            "Init response schema required fields must match properties"
        )
    if schema.get("additionalProperties") is not False:
        raise RealProjectAcceptanceError(
            "Init response schema must reject additional properties"
        )

    def require_types(value: Any, context: tuple[str, ...]) -> None:
        if not isinstance(value, dict):
            raise RealProjectAcceptanceError(
                "Init response schema node is invalid: " + ".".join(context)
            )
        if "type" not in value:
            raise RealProjectAcceptanceError(
                "Init response schema node lacks type: " + ".".join(context)
            )
        nested = value.get("properties")
        if nested is not None:
            if not isinstance(nested, dict):
                raise RealProjectAcceptanceError(
                    "Init response schema properties are invalid: "
                    + ".".join(context)
                )
            for name, child in nested.items():
                require_types(child, (*context, str(name)))
        if value.get("type") == "array":
            require_types(value.get("items"), (*context, "items"))

    require_types(schema, ("root",))
    return schema


def load_language_acceptance_contract(
    path: Path = LANGUAGE_ACCEPTANCE_CONTRACT,
) -> dict[str, Any]:
    try:
        contract = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RealProjectAcceptanceError(
            "governance language acceptance contract is unreadable"
        ) from exc
    expected_keys = {
        "schema",
        "schema_version",
        "scenario_id",
        "expected_language",
        "status_path",
        "status_field",
        "minimum_cjk_characters_per_changed_document",
        "minimum_cjk_to_latin_ratio",
    }
    if not isinstance(contract, dict) or set(contract) != expected_keys:
        raise RealProjectAcceptanceError(
            "governance language acceptance contract fields drifted"
        )
    exact = {
        "schema": "cotend.g06-governance-language-acceptance",
        "schema_version": 1,
        "scenario_id": "g06-real-fresh-init",
        "expected_language": "zh-CN",
        "status_path": "STATUS.md",
        "status_field": "user_facing_language_resolution.normalized_tag",
    }
    mismatches = {
        key: {"expected": value, "actual": contract.get(key)}
        for key, value in exact.items()
        if contract.get(key) != value
    }
    if mismatches:
        raise RealProjectAcceptanceError(
            f"governance language acceptance contract mismatch: {mismatches}"
        )
    minimum_cjk = contract["minimum_cjk_characters_per_changed_document"]
    minimum_ratio = contract["minimum_cjk_to_latin_ratio"]
    if not isinstance(minimum_cjk, int) or isinstance(minimum_cjk, bool):
        raise RealProjectAcceptanceError(
            "governance language minimum CJK count is invalid"
        )
    if minimum_cjk < 8:
        raise RealProjectAcceptanceError(
            "governance language minimum CJK count is too weak"
        )
    if (
        not isinstance(minimum_ratio, (int, float))
        or isinstance(minimum_ratio, bool)
        or not 0.01 <= float(minimum_ratio) <= 1.0
    ):
        raise RealProjectAcceptanceError(
            "governance language CJK-to-Latin ratio is invalid"
        )
    return contract


def normalize_language_tag(value: str) -> str:
    parts = value.strip().replace("_", "-").split("-")
    if not parts or any(not part for part in parts):
        return value.strip()
    normalized = [parts[0].lower()]
    for part in parts[1:]:
        normalized.append(part.upper() if len(part) == 2 else part)
    return "-".join(normalized)


def validate_governance_language(
    project: Path,
    changed_governance_paths: list[str],
    *,
    contract_path: Path = LANGUAGE_ACCEPTANCE_CONTRACT,
) -> dict[str, Any]:
    contract = load_language_acceptance_contract(contract_path)
    status_relative = str(contract["status_path"])
    if status_relative not in changed_governance_paths:
        raise RealProjectAcceptanceError(
            "fresh Init did not create or update the language-bearing STATUS.md"
        )
    status_path = project / status_relative
    if not status_path.is_file() or status_path.is_symlink():
        raise RealProjectAcceptanceError(
            "language-bearing STATUS.md is missing or linked"
        )
    status_text = status_path.read_text(encoding="utf-8")
    declarations: list[str] = []
    lines = status_text.splitlines()
    for index, line in enumerate(lines):
        match = re.fullmatch(
            r"(?P<indent>[ \t]*)user_facing_language_resolution[ \t]*:[ \t]*",
            line,
        )
        if match is None:
            continue
        parent_indent = len(match.group("indent").expandtabs(2))
        for child in lines[index + 1 :]:
            if not child.strip():
                continue
            child_prefix = child[: len(child) - len(child.lstrip(" \t"))]
            child_indent = len(child_prefix.expandtabs(2))
            if child_indent <= parent_indent:
                break
            normalized = re.fullmatch(
                r"[ \t]*normalized_tag[ \t]*:[ \t]*[\"'`]?"
                r"([^\"'`#\s]+)[\"'`]?[ \t]*",
                child,
            )
            if normalized is not None:
                declarations.append(normalized.group(1))
    if not declarations:
        raise RealProjectAcceptanceError(
            "STATUS.md does not declare "
            "user_facing_language_resolution.normalized_tag"
        )
    normalized = sorted({normalize_language_tag(value) for value in declarations})
    expected = normalize_language_tag(str(contract["expected_language"]))
    if normalized != [expected]:
        raise RealProjectAcceptanceError(
            "STATUS.md governance language differs from the acceptance contract: "
            f"expected={expected!r}, observed={normalized!r}"
        )

    minimum_cjk = int(contract["minimum_cjk_characters_per_changed_document"])
    minimum_ratio = float(contract["minimum_cjk_to_latin_ratio"])
    markdown_paths = sorted(
        path
        for path in changed_governance_paths
        if PurePosixPath(path).suffix.lower() == ".md"
    )
    if not markdown_paths:
        raise RealProjectAcceptanceError(
            "Init produced no changed Markdown governance documents"
        )
    document_evidence: list[dict[str, Any]] = []
    for relative in markdown_paths:
        path = project / PurePosixPath(relative)
        if not path.is_file() or path.is_symlink():
            raise RealProjectAcceptanceError(
                f"changed governance document is missing or linked: {relative}"
            )
        text = path.read_text(encoding="utf-8")
        cjk_count = len(CJK_PATTERN.findall(text))
        latin_count = len(LATIN_PATTERN.findall(text))
        ratio = cjk_count / max(1, latin_count)
        if cjk_count < minimum_cjk or ratio < minimum_ratio:
            raise RealProjectAcceptanceError(
                "changed governance document does not satisfy the Chinese "
                f"content oracle: {relative} "
                f"(cjk={cjk_count}, latin={latin_count}, ratio={ratio:.4f})"
            )
        document_evidence.append(
            {
                "path": relative,
                "cjk_characters": cjk_count,
                "latin_characters": latin_count,
                "cjk_to_latin_ratio": round(ratio, 6),
            }
        )
    return {
        "status": "pass",
        "expected_language": expected,
        "status_path": status_relative,
        "status_field": contract["status_field"],
        "changed_documents": document_evidence,
    }


def redact_runtime_text(value: str) -> str:
    redacted = re.sub(
        r"(?i)(bearer\s+)[^\s,\"']+",
        r"\1<redacted>",
        value,
    )
    redacted = re.sub(
        r"""(?ix)
        (
          ["']?
          (?:
            (?:access|refresh|id|session)_token
            | token
            | api_key
            | authorization
            | client_secret
            | password
          )
          ["']?
          \s*[=:]\s*
        )
        (["']?)
        [^\s,"'}]+
        """,
        r"\1\2<redacted>",
        redacted,
    )
    redacted = re.sub(
        r"(?<![A-Za-z0-9_-])sk-[A-Za-z0-9_*-]{4,}(?![A-Za-z0-9_-])",
        "<redacted-api-key>",
        redacted,
    )
    redacted = re.sub(
        r"\beyJ[A-Za-z0-9_-]{20,}(?:\.[A-Za-z0-9_-]{10,}){1,2}\b",
        "<redacted-jwt>",
        redacted,
    )
    return re.sub(
        r"\b(?=[A-Za-z0-9_-]*[A-Za-z])(?=[A-Za-z0-9_-]*[0-9])"
        r"[A-Za-z0-9_-]{40,}\b",
        "<redacted-opaque>",
        redacted,
    )


def _runtime_error_messages(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        messages: list[str] = []
        for key in ("message", "detail", "reason", "error"):
            if key in value:
                messages.extend(_runtime_error_messages(value[key]))
        return messages
    if isinstance(value, list):
        messages = []
        for item in value:
            messages.extend(_runtime_error_messages(item))
        return messages
    return []


def codex_failure_summary(stdout: str, stderr: str) -> dict[str, Any]:
    events: list[dict[str, Any]] = []
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict):
            continue
        event_type = str(event.get("type", ""))
        if "error" not in event_type.casefold() and "failed" not in event_type.casefold():
            continue
        messages = []
        for key in ("message", "detail", "reason", "error"):
            if key in event:
                messages.extend(_runtime_error_messages(event[key]))
        events.append(
            {
                "type": event_type or "unknown_error_event",
                "messages": [
                    redact_runtime_text(message)[:800]
                    for message in messages
                    if message
                ][:4],
            }
        )
    return {
        "json_error_events": events[-4:],
        "stderr_tail": redact_runtime_text(stderr[-1200:]),
    }


def _safe_event_identifier(value: Any) -> str:
    candidate = str(value)
    if re.fullmatch(r"[A-Za-z0-9_.:-]{1,80}", candidate):
        return candidate
    return "unknown"


def _safe_runtime_message(value: str) -> str:
    return re.sub(r"\s+", " ", redact_runtime_text(value)).strip()[:600]


def safe_codex_event(line: str, sequence: int, elapsed_ms: int) -> dict[str, Any] | None:
    if len(line) > CODEX_CAPTURE_LIMIT:
        return None
    try:
        value = json.loads(line)
    except json.JSONDecodeError:
        return None
    if not isinstance(value, dict):
        return None
    event_type = _safe_event_identifier(value.get("type", "unknown"))
    event: dict[str, Any] = {
        "sequence": sequence,
        "elapsed_ms": elapsed_ms,
        "type": event_type,
    }
    item = value.get("item")
    if isinstance(item, dict) and "type" in item:
        event["item_type"] = _safe_event_identifier(item["type"])
    if (
        "error" in event_type.casefold()
        or "failed" in event_type.casefold()
        or "error" in value
    ):
        messages: list[str] = []
        for key in ("message", "detail", "reason", "error"):
            if key in value:
                messages.extend(_runtime_error_messages(value[key]))
        safe_messages = [
            _safe_runtime_message(message)
            for message in messages
            if message
        ][:4]
        if safe_messages:
            event["messages"] = safe_messages
    return event


class CodexEventJournal:
    def __init__(self, limit: int = CODEX_EVENT_JOURNAL_LIMIT) -> None:
        if limit <= 0:
            raise RealProjectAcceptanceError("Codex event journal limit must be positive")
        self._events: deque[dict[str, Any]] = deque(maxlen=limit)
        self._type_counts: Counter[str] = Counter()
        self.stdout_lines_seen = 0
        self.json_events_seen = 0
        self.invalid_json_lines_seen = 0
        self.stderr_lines_seen = 0
        self.last_event_type: str | None = None

    def record_stdout(self, line: str, elapsed_ms: int) -> None:
        self.stdout_lines_seen += 1
        event = safe_codex_event(
            line,
            self.stdout_lines_seen,
            elapsed_ms,
        )
        if event is None:
            self.invalid_json_lines_seen += 1
            return
        self.json_events_seen += 1
        event_type = str(event["type"])
        self.last_event_type = event_type
        self._type_counts[event_type] += 1
        self._events.append(event)

    def record_stderr(self) -> None:
        self.stderr_lines_seen += 1

    def snapshot(
        self,
        status: str,
        elapsed_ms: int,
        **extra: Any,
    ) -> dict[str, Any]:
        return {
            "status": status,
            "elapsed_ms": elapsed_ms,
            "stdout_lines_seen": self.stdout_lines_seen,
            "json_events_seen": self.json_events_seen,
            "invalid_json_lines_seen": self.invalid_json_lines_seen,
            "stderr_lines_seen": self.stderr_lines_seen,
            "last_event_type": self.last_event_type,
            "event_type_counts": dict(sorted(self._type_counts.items())),
            "events_retained": list(self._events),
            "events_dropped": max(
                0,
                self.json_events_seen - len(self._events),
            ),
            **extra,
        }


class BoundedTextCapture:
    def __init__(self, limit: int = CODEX_CAPTURE_LIMIT) -> None:
        if limit <= 0:
            raise RealProjectAcceptanceError("stream capture limit must be positive")
        self.limit = limit
        self._chunks: deque[str] = deque()
        self._size = 0

    def append(self, value: str) -> None:
        if len(value) >= self.limit:
            self._chunks.clear()
            self._chunks.append(value[-self.limit :])
            self._size = self.limit
            return
        self._chunks.append(value)
        self._size += len(value)
        while self._size > self.limit and self._chunks:
            removed = self._chunks.popleft()
            self._size -= len(removed)

    def value(self) -> str:
        return "".join(self._chunks)


def terminate_process_tree(
    process: subprocess.Popen[str],
    *,
    taskkill_runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
) -> dict[str, Any]:
    if process.poll() is not None:
        return {
            "method": "already_exited",
            "terminated": True,
            "tree_termination_confirmed": True,
            "returncode": process.returncode,
        }
    method = "process_kill"
    primary_returncode: int | None = None
    if os.name == "nt":
        method = "taskkill_tree"
        taskkill = shutil.which("taskkill.exe") or "taskkill.exe"
        completed = taskkill_runner(
            [taskkill, "/PID", str(process.pid), "/T", "/F"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
        )
        primary_returncode = completed.returncode
    else:
        method = "process_group"
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            primary_returncode = 0
        except ProcessLookupError:
            primary_returncode = 0
        except OSError:
            primary_returncode = 1
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        if os.name != "nt":
            try:
                os.killpg(os.getpgid(process.pid), signal.SIGKILL)
            except (OSError, ProcessLookupError):
                process.kill()
        else:
            process.kill()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            return {
                "method": method,
                "primary_returncode": primary_returncode,
                "terminated": False,
                "tree_termination_confirmed": False,
                "returncode": None,
            }
    tree_termination_confirmed = (
        process.poll() is not None
        and (os.name != "nt" or primary_returncode == 0)
    )
    return {
        "method": method,
        "primary_returncode": primary_returncode,
        "terminated": process.poll() is not None,
        "tree_termination_confirmed": tree_termination_confirmed,
        "returncode": process.returncode,
    }


def _pump_process_stream(
    name: str,
    stream: TextIO,
    events: queue.Queue[tuple[str, str | None]],
) -> None:
    try:
        for line in iter(stream.readline, ""):
            events.put((name, line))
    finally:
        events.put((name, None))


def run_codex_streaming(
    command: list[str],
    *,
    cwd: Path,
    input_text: str,
    env: dict[str, str] | None = None,
    event_checkpoint: Callable[[dict[str, Any]], None] | None = None,
    total_timeout_seconds: float = CODEX_TOTAL_TIMEOUT_SECONDS,
    inactivity_timeout_seconds: float = CODEX_INACTIVITY_TIMEOUT_SECONDS,
    popen_factory: Callable[..., subprocess.Popen[str]] = subprocess.Popen,
    tree_terminator: Callable[[subprocess.Popen[str]], dict[str, Any]] = (
        terminate_process_tree
    ),
) -> subprocess.CompletedProcess[str]:
    if (
        total_timeout_seconds <= 0
        or inactivity_timeout_seconds <= 0
        or inactivity_timeout_seconds > total_timeout_seconds
    ):
        raise RealProjectAcceptanceError("Codex streaming timeout settings are invalid")
    journal = CodexEventJournal()
    stdout_capture = BoundedTextCapture()
    stderr_capture = BoundedTextCapture()
    started = time.monotonic()

    def elapsed_ms() -> int:
        return max(0, int((time.monotonic() - started) * 1000))

    def checkpoint(status: str, **extra: Any) -> None:
        if event_checkpoint is not None:
            event_checkpoint(journal.snapshot(status, elapsed_ms(), **extra))

    checkpoint(
        "starting",
        total_timeout_seconds=total_timeout_seconds,
        inactivity_timeout_seconds=inactivity_timeout_seconds,
    )
    popen_kwargs: dict[str, Any] = {
        "cwd": cwd,
        "stdin": subprocess.PIPE,
        "stdout": subprocess.PIPE,
        "stderr": subprocess.PIPE,
        "text": True,
        "encoding": "utf-8",
        "errors": "replace",
        "bufsize": 1,
    }
    if env is not None:
        popen_kwargs["env"] = env
    if os.name == "nt":
        popen_kwargs["creationflags"] = getattr(
            subprocess,
            "CREATE_NEW_PROCESS_GROUP",
            0,
        )
    else:
        popen_kwargs["start_new_session"] = True
    try:
        process = popen_factory(command, **popen_kwargs)
    except Exception:
        checkpoint("start_failed")
        raise

    def stop_process() -> dict[str, Any]:
        try:
            return tree_terminator(process)
        except Exception as exc:
            try:
                process.kill()
                process.wait(timeout=5)
            except (OSError, subprocess.SubprocessError):
                pass
            return {
                "method": "terminator_failed",
                "error_type": type(exc).__name__,
                "terminated": process.poll() is not None,
                "tree_termination_confirmed": False,
                "returncode": process.returncode,
            }

    def close_process_streams() -> None:
        for stream in (process.stdin, process.stdout, process.stderr):
            if stream is None or stream.closed:
                continue
            try:
                stream.close()
            except OSError:
                pass

    try:
        if process.stdin is None or process.stdout is None or process.stderr is None:
            raise RealProjectAcceptanceError(
                "Codex streaming process did not expose all required pipes"
            )
        try:
            process.stdin.write(input_text)
            process.stdin.close()
        except (BrokenPipeError, OSError) as exc:
            raise RealProjectAcceptanceError(
                "Codex streaming process rejected its input"
            ) from exc

        stream_events: queue.Queue[tuple[str, str | None]] = queue.Queue()
        threads = [
            threading.Thread(
                target=_pump_process_stream,
                args=("stdout", process.stdout, stream_events),
                daemon=True,
            ),
            threading.Thread(
                target=_pump_process_stream,
                args=("stderr", process.stderr, stream_events),
                daemon=True,
            ),
        ]
        for thread in threads:
            thread.start()
        checkpoint("running")
        eof: set[str] = set()
        last_activity = time.monotonic()
        timeout_kind: str | None = None

        def consume(name: str, line: str | None) -> None:
            nonlocal last_activity
            if line is None:
                eof.add(name)
                return
            last_activity = time.monotonic()
            if name == "stdout":
                stdout_capture.append(line)
                journal.record_stdout(line, elapsed_ms())
                checkpoint("running")
            else:
                stderr_capture.append(line)
                journal.record_stderr()

        while True:
            now = time.monotonic()
            if process.poll() is not None and eof == {"stdout", "stderr"}:
                break
            if now - started >= total_timeout_seconds:
                timeout_kind = "total"
                break
            if now - last_activity >= inactivity_timeout_seconds:
                timeout_kind = "inactivity"
                break
            wait_for = min(
                0.25,
                max(0.01, total_timeout_seconds - (now - started)),
                max(0.01, inactivity_timeout_seconds - (now - last_activity)),
            )
            try:
                consume(*stream_events.get(timeout=wait_for))
            except queue.Empty:
                continue

        if timeout_kind is not None:
            termination = stop_process()
            drain_until = time.monotonic() + 2
            while time.monotonic() < drain_until and eof != {"stdout", "stderr"}:
                try:
                    consume(*stream_events.get(timeout=0.05))
                except queue.Empty:
                    if process.poll() is not None:
                        break
            for thread in threads:
                thread.join(timeout=0.25)
            close_process_streams()
            summary = journal.snapshot(
                "timed_out",
                elapsed_ms(),
                timeout_kind=timeout_kind,
                process_tree=termination,
            )
            checkpoint(
                "timed_out",
                timeout_kind=timeout_kind,
                process_tree=termination,
            )
            if (
                not termination.get("terminated")
                or not termination.get("tree_termination_confirmed")
            ):
                raise RealProjectAcceptanceError(
                    "Codex Init timed out without confirmed process-tree cleanup"
                )
            raise CodexProcessTimeout(timeout_kind, summary)

        returncode = process.wait(timeout=5)
        for thread in threads:
            thread.join(timeout=0.25)
        close_process_streams()
        checkpoint("completed", returncode=returncode)
        return subprocess.CompletedProcess(
            command,
            returncode,
            stdout_capture.value(),
            stderr_capture.value(),
        )
    except CodexProcessTimeout:
        raise
    except Exception:
        termination = stop_process()
        close_process_streams()
        try:
            checkpoint("runner_failed", process_tree=termination)
        except Exception:
            pass
        raise


def validate_init_result(
    project: Path,
    result: dict[str, Any],
    *,
    expected_skill_sha256: str | None = None,
) -> None:
    expected_hash = expected_skill_sha256 or sha256(project / INIT_SKILL)
    exact = {
        "scenario_id": "g06-real-fresh-init",
        "invoked_skill": "cotend-init",
        "skill_source_path": INIT_SKILL,
        "skill_source_sha256": expected_hash,
        "runtime_profile": "full",
        "product_implementation_started": False,
        "protected_product_files_modified": False,
        "git_commit_created": False,
        "handback_required": True,
    }
    mismatches = {key: {"expected": value, "actual": result.get(key)} for key, value in exact.items() if result.get(key) != value}
    if mismatches:
        raise RealProjectAcceptanceError(f"Init result contract mismatch: {mismatches}")
    if result.get("auto_mode") not in {"fresh_init", "legacy_update"}:
        raise RealProjectAcceptanceError("Init Auto Mode is invalid")
    if result.get("readiness") not in {"continue_ready", "human_needed"}:
        raise RealProjectAcceptanceError("Init readiness is invalid")
    if result.get("adoption_profile") not in {"standard", "full"}:
        raise RealProjectAcceptanceError("Init adoption profile is invalid")


def _init_change_allowed(path: str) -> bool:
    candidate = PurePosixPath(path)
    if len(candidate.parts) == 1:
        return candidate.name in INIT_ALLOWED_FILES
    return (
        candidate.parts[0] in INIT_ALLOWED_DIRECTORIES
        and candidate.suffix.lower() == ".md"
        and ".." not in candidate.parts
    )


def validate_init_change_report(
    result: dict[str, Any],
    before: dict[str, str],
    after: dict[str, str],
) -> tuple[list[str], list[str]]:
    created = sorted(after.keys() - before.keys())
    deleted = sorted(before.keys() - after.keys())
    updated = sorted(path for path in before.keys() & after.keys() if before[path] != after[path])
    if deleted:
        raise RealProjectAcceptanceError("Init deleted governance files: " + ", ".join(deleted))

    def reported(key: str) -> list[str]:
        values = result.get(key)
        if not isinstance(values, list) or any(not isinstance(value, str) for value in values):
            raise RealProjectAcceptanceError(f"Init result {key} is invalid")
        normalized = [PurePosixPath(value.replace("\\", "/")).as_posix() for value in values]
        if any(value.startswith("/") or ".." in PurePosixPath(value).parts for value in normalized):
            raise RealProjectAcceptanceError(f"Init result {key} contains an unsafe path")
        if len(normalized) != len(set(normalized)):
            raise RealProjectAcceptanceError(f"Init result {key} contains duplicate paths")
        return sorted(normalized)

    reported_created = reported("durable_files_created")
    reported_updated = reported("durable_files_updated")
    if reported_created != created or reported_updated != updated:
        raise RealProjectAcceptanceError(
            "Init durable-file report differs from the filesystem: "
            f"created={reported_created!r}/{created!r}, updated={reported_updated!r}/{updated!r}"
        )
    return created, updated


def run_real_init(
    project: Path,
    allowed_root: Path,
    output: Path,
    *,
    model: str = MODEL,
    reasoning_effort: str = REASONING_EFFORT,
    protected_paths: tuple[Path, ...] = (),
    observed_paths: tuple[Path, ...] = (),
    isolated_runtime_root: Path | None = None,
    carrier: str = "native",
    wsl_distribution: str | None = None,
    wsl_runtime_root: str | None = None,
    wsl_executable: str | None = None,
    path_mapper: Callable[[Path], str] = windows_path_to_wsl,
    runner: Any = None,
    event_checkpoint: Callable[[dict[str, Any]], None] | None = None,
) -> dict[str, Any]:
    project = guarded_project(project, allowed_root)
    current = r12_artifact()
    require_delivery_state(DeliveryManager(project), current, R12_ID)
    output = output.expanduser().resolve()
    private_root = (ROOT / ".private-provenance").resolve()
    try:
        output.relative_to(private_root)
    except ValueError as exc:
        raise RealProjectAcceptanceError("Init output must stay under .private-provenance") from exc
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        raise RealProjectAcceptanceError("Init output already exists")
    if carrier == "wsl2":
        if (
            wsl_distribution is None
            or wsl_runtime_root is None
            or isolated_runtime_root is not None
        ):
            raise RealProjectAcceptanceError(
                "WSL Init requires its distribution/runtime and no native runtime"
            )
        command_project = path_mapper(project)
        command_output = path_mapper(output)
        command = build_wsl_codex_command(
            command_project,
            command_output,
            wsl_distribution,
            wsl_runtime_root,
            model=model,
            reasoning_effort=reasoning_effort,
            wsl_executable=wsl_executable,
        )
        validate_codex_command(
            command,
            project,
            carrier=carrier,
            expected_project=command_project,
            expected_output=command_output,
            expected_model=model,
            expected_reasoning_effort=reasoning_effort,
            wsl_distribution=wsl_distribution,
            wsl_runtime_root=wsl_runtime_root,
        )
        runtime_env = None
    elif carrier == "native":
        if wsl_distribution is not None or wsl_runtime_root is not None:
            raise RealProjectAcceptanceError(
                "native Init cannot use WSL carrier settings"
            )
        command = build_codex_command(
            project,
            output,
            model=model,
            reasoning_effort=reasoning_effort,
        )
        validate_codex_command(
            command,
            project,
            carrier=carrier,
            expected_output=str(output),
            expected_model=model,
            expected_reasoning_effort=reasoning_effort,
        )
        runtime_env = (
            build_isolated_runtime_env(isolated_runtime_root)
            if isolated_runtime_root is not None
            else None
        )
    else:
        raise RealProjectAcceptanceError("Init carrier is invalid")
    validate_response_schema(project / INIT_SCHEMA)
    before = file_manifest(project, excludes=SNAPSHOT_EXCLUDES)
    before_head = git_head(project)
    skill_sha256_before = sha256(project / INIT_SKILL)
    protected = protected_boundary_snapshot(project, allowed_root, protected_paths)
    observed_before = observed_live_boundary_snapshot(
        project,
        allowed_root,
        observed_paths,
    )
    prompt = (
        "$cotend-init\n\n"
        "Initialize this retained local project from PROJECT-BRIEF.md using the project-local CoTend r12 Skills. "
        "Use the standard adoption profile and Full runtime profile. Before acting, read .agents/skills/cotend-init/SKILL.md "
        "and compute its SHA-256. Create only the minimum durable governance records, run consistency checks, report readiness, "
        "and stop for the owner's next instruction. Do not create expense_splitter.py, tests, any product implementation, or a Git commit. "
        "Do not read or modify global Skills, Plugin state, config/auth, other projects, or files outside this repository. "
        "List every created or updated durable governance file as an exact project-relative path. "
        "Set scenario_id to g06-real-fresh-init and return only the requested JSON after filesystem work is complete."
    )
    completed: subprocess.CompletedProcess[str] | None = None
    runner_error: Exception | None = None
    try:
        if runner is None:
            completed = run_codex_streaming(
                command,
                cwd=project,
                input_text=prompt,
                env=runtime_env,
                event_checkpoint=event_checkpoint,
            )
        else:
            runner_kwargs: dict[str, Any] = {
                "cwd": project,
                "input": prompt,
                "check": False,
                "capture_output": True,
                "text": True,
                "encoding": "utf-8",
                "errors": "replace",
                "timeout": CODEX_TOTAL_TIMEOUT_SECONDS,
            }
            if runtime_env is not None:
                runner_kwargs["env"] = runtime_env
            completed = runner(command, **runner_kwargs)
    except Exception as exc:  # Preserve runtime failures until boundary checks finish.
        runner_error = exc

    boundary_errors: list[Exception] = []
    try:
        assert_protected_boundaries_unchanged(
            protected,
            project,
            allowed_root,
            protected_paths,
        )
    except (RealProjectAcceptanceError, OSError) as exc:
        boundary_errors.append(exc)
    try:
        require_delivery_state(DeliveryManager(project), current, R12_ID)
    except (RealProjectAcceptanceError, DeliveryError, OSError) as exc:
        boundary_errors.append(exc)
    try:
        if sha256(project / INIT_SKILL) != skill_sha256_before:
            raise RealProjectAcceptanceError("project-local Init Skill changed during execution")
    except (RealProjectAcceptanceError, OSError) as exc:
        boundary_errors.append(exc)
    observed_after = observed_live_boundary_snapshot(
        project,
        allowed_root,
        observed_paths,
    )
    observed_change_details = boundary_snapshot_differences(
        observed_before,
        observed_after,
    )
    observed_changes = observed_change_details["changed_labels"]

    if boundary_errors:
        runtime = (
            "command="
            + json.dumps(
                {
                    "returncode": completed.returncode,
                    "failure": codex_failure_summary(
                        completed.stdout,
                        completed.stderr,
                    ),
                    "observed_live_boundary_changes": observed_changes,
                    "observed_live_boundary_details": observed_change_details,
                },
                ensure_ascii=True,
            )
            if completed is not None
            else f"runner_error={runner_error!r}"
        )
        raise RealProjectAcceptanceError(
            "; ".join(str(error) for error in boundary_errors) + "; " + runtime
        ) from boundary_errors[0]
    if runner_error is not None:
        raise runner_error
    if completed is None:
        raise RealProjectAcceptanceError("Codex Init runner returned no result")
    if completed.returncode != 0:
        failure = codex_failure_summary(completed.stdout, completed.stderr)
        failure["observed_live_boundary_changes"] = observed_changes
        failure["observed_live_boundary_details"] = observed_change_details
        raise RealProjectAcceptanceError(
            f"Codex Init failed with exit {completed.returncode}: "
            + json.dumps(failure, ensure_ascii=True)
        )
    if not output.is_file():
        raise RealProjectAcceptanceError("Codex Init did not write a final structured result")
    result = json.loads(output.read_text(encoding="utf-8"))
    if not isinstance(result, dict):
        raise RealProjectAcceptanceError("Codex Init result is not an object")
    validate_init_result(
        project,
        result,
        expected_skill_sha256=skill_sha256_before,
    )
    reject_link_tree(project)
    after = file_manifest(project, excludes=SNAPSHOT_EXCLUDES)
    unexpected = sorted(path for path in changed_paths(before, after) if not _init_change_allowed(path))
    if unexpected:
        raise RealProjectAcceptanceError("Init changed non-governance files: " + ", ".join(unexpected))
    created, updated = validate_init_change_report(result, before, after)
    language_acceptance = validate_governance_language(
        project,
        [*created, *updated],
    )
    if git_head(project) != before_head:
        raise RealProjectAcceptanceError("Init created or changed the project Git commit")
    if git(project, "diff", "--cached", "--name-only").stdout.strip():
        raise RealProjectAcceptanceError("Init staged project files")
    return {
        "status": "pass",
        "carrier": carrier,
        "model": model,
        "reasoning_effort": reasoning_effort,
        "skill_source_path": result["skill_source_path"],
        "skill_source_sha256": result["skill_source_sha256"],
        "auto_mode": result["auto_mode"],
        "readiness": result["readiness"],
        "adoption_profile": result["adoption_profile"],
        "runtime_profile": result["runtime_profile"],
        "created_governance_paths": created,
        "updated_governance_paths": updated,
        "governance_language_acceptance": language_acceptance,
        "project_git_head_unchanged": True,
        "protected_user_boundaries": len(protected),
        "observed_live_boundary_changes": observed_changes,
        "observed_live_boundary_details": observed_change_details,
        "isolated_runtime": runtime_env is not None or carrier == "wsl2",
        "handback_required": True,
    }


def run_real_init_wsl(
    project: Path,
    allowed_root: Path,
    output: Path,
    *,
    distribution: str,
    runtime_root: str,
    auth_source: Path,
    evidence: Path | None = None,
    model: str = MODEL,
    reasoning_effort: str = REASONING_EFFORT,
    protected_paths: tuple[Path, ...] = (),
    observed_paths: tuple[Path, ...] = (),
    wsl_executable: str | None = None,
    runner: Any = None,
    lifecycle_runner: Callable[..., subprocess.CompletedProcess[str]] = subprocess.run,
    path_mapper: Callable[[Path], str] = windows_path_to_wsl,
) -> dict[str, Any]:
    project = guarded_project(project, allowed_root)
    guarded_wsl_runtime_root(runtime_root)
    source = auth_source.expanduser().resolve()
    protected_with_auth = (*protected_paths, source)
    protected_before = protected_boundary_snapshot(
        project,
        allowed_root,
        protected_with_auth,
    )
    result: dict[str, Any] | None = None
    primary_error: Exception | None = None
    cleanup_errors: list[Exception] = []
    evidence_errors: list[Exception] = []
    probe: dict[str, Any] | None = None
    preparation: dict[str, Any] | None = None
    cleanup: dict[str, Any] | None = None
    host_before: dict[str, Any] | None = None
    host_after: dict[str, Any] | None = None
    plugin_content_before: dict[str, dict[str, Any]] | None = None
    plugin_content_after: dict[str, dict[str, Any]] | None = None
    stage = "host-boundary"
    carrier_may_be_running = False
    preparation_attempted = False
    model_call_may_have_been_consumed = False

    def record_evidence(
        phase: str,
        payload: dict[str, Any],
    ) -> None:
        try:
            write_evidence(evidence, phase, payload)
        except Exception as exc:
            evidence_errors.append(exc)

    try:
        stage = "plugin-content-boundary"
        plugin_content_before = protected_plugin_content_snapshot()
        write_evidence(
            evidence,
            "run-init-wsl-content-boundary",
            {
                "status": "starting",
                "before": plugin_content_before,
                "auth_content_read": False,
            },
        )
        host_before = snapshot_wsl_host(wsl_executable=wsl_executable)
        require_wsl_host_baseline(host_before, distribution)
        carrier_may_be_running = True
        probe = probe_wsl_carrier(
            distribution,
            project,
            wsl_executable=wsl_executable,
            runner=lifecycle_runner,
            path_mapper=path_mapper,
        )
        stage = "probe-evidence"
        write_evidence(
            evidence,
            "run-init-wsl-probe",
            {
                "status": "pass",
                "host_before": host_before,
                **probe,
            },
        )
        stage = "runtime-prepare"
        preparation_attempted = True
        preparation = prepare_wsl_runtime(
            distribution,
            runtime_root,
            source,
            wsl_executable=wsl_executable,
            runner=lifecycle_runner,
            path_mapper=path_mapper,
        )
        stage = "runtime-prepare-evidence"
        write_evidence(
            evidence,
            "run-init-wsl-prepare",
            {"status": "pass", **preparation},
        )
        stage = "model-call-evidence"
        write_evidence(
            evidence,
            "run-init-wsl-call",
            {
                "status": "starting",
                "authorized_model_calls": 1,
                "model": model,
                "reasoning_effort": reasoning_effort,
            },
        )
        stage = "model-call"
        model_call_may_have_been_consumed = True
        result = run_real_init(
            project,
            allowed_root,
            output,
            model=model,
            reasoning_effort=reasoning_effort,
            protected_paths=protected_with_auth,
            observed_paths=observed_paths,
            carrier="wsl2",
            wsl_distribution=distribution,
            wsl_runtime_root=runtime_root,
            wsl_executable=wsl_executable,
            path_mapper=path_mapper,
            runner=runner,
            event_checkpoint=lambda payload: write_evidence(
                evidence,
                "run-init-wsl-events",
                payload,
            ),
        )
        stage = "model-call-result-evidence"
        write_evidence(
            evidence,
            "run-init-wsl-call",
            {
                "status": "pass",
                "model_calls_consumed": 1,
                "model": model,
                "reasoning_effort": reasoning_effort,
                "result": result,
            },
        )
    except Exception as exc:  # Preserve the first failure through cleanup.
        primary_error = exc
        record_evidence(
            "run-init-wsl-failure",
            {
                "status": "failed",
                "failed_stage": stage,
                "model_call_may_have_been_consumed": (
                    model_call_may_have_been_consumed
                ),
                "error": redact_runtime_text(str(exc))[:2400],
            },
        )
    finally:
        if preparation_attempted:
            try:
                cleanup = cleanup_wsl_runtime(
                    distribution,
                    runtime_root,
                    wsl_executable=wsl_executable,
                    runner=lifecycle_runner,
                )
            except Exception as exc:
                cleanup_errors.append(exc)
        elif carrier_may_be_running:
            try:
                terminate_wsl_distribution(
                    distribution,
                    wsl_executable=wsl_executable,
                    runner=lifecycle_runner,
                )
                cleanup = {
                    "runtime_root_removed": "not_created",
                    "distribution_terminated": True,
                }
            except Exception as exc:
                cleanup_errors.append(exc)
        if host_before is not None:
            try:
                host_after = snapshot_wsl_host(wsl_executable=wsl_executable)
                if host_after != host_before:
                    raise RealProjectAcceptanceError(
                        "WSL host inventory or defaults changed during Init"
                    )
            except Exception as exc:
                cleanup_errors.append(exc)
        if plugin_content_before is not None:
            try:
                plugin_content_after = protected_plugin_content_snapshot()
                if plugin_content_after != plugin_content_before:
                    raise RealProjectAcceptanceError(
                        "protected Plugin content changed during Init"
                    )
            except Exception as exc:
                cleanup_errors.append(exc)
        try:
            assert_protected_boundaries_unchanged(
                protected_before,
                project,
                allowed_root,
                protected_with_auth,
            )
        except Exception as exc:
            cleanup_errors.append(exc)
        record_evidence(
            "run-init-wsl-content-boundary",
            {
                "status": (
                    "pass"
                    if (
                        plugin_content_before is not None
                        and plugin_content_after == plugin_content_before
                    )
                    else "failed"
                ),
                "before": plugin_content_before,
                "after": plugin_content_after,
                "auth_content_read": False,
            },
        )
        record_evidence(
            "run-init-wsl-cleanup",
            {
                "status": (
                    "pass"
                    if not cleanup_errors and not evidence_errors
                    else "failed"
                ),
                "cleanup": cleanup,
                "host_after": host_after,
                "errors": [
                    redact_runtime_text(str(error))[:1200]
                    for error in [*cleanup_errors, *evidence_errors]
                ],
            },
        )
    if primary_error is not None or cleanup_errors or evidence_errors:
        messages = []
        if primary_error is not None:
            messages.append(str(primary_error))
        messages.extend(str(error) for error in cleanup_errors)
        messages.extend(str(error) for error in evidence_errors)
        raise RealProjectAcceptanceError("; ".join(messages))
    if (
        result is None
        or probe is None
        or preparation is None
        or cleanup is None
        or host_before is None
        or host_after is None
        or plugin_content_before is None
        or plugin_content_after is None
    ):
        raise RealProjectAcceptanceError(
            "WSL Init lifecycle completed without a full result"
        )
    return {
        **result,
        "wsl_probe": probe,
        "wsl_runtime": preparation,
        "wsl_cleanup": cleanup,
        "wsl_host_boundary_unchanged": True,
        "plugin_content_boundary_unchanged": True,
    }


def run_product_checks(project: Path) -> dict[str, Any]:
    commands = [
        [sys.executable, "-m", "py_compile", "expense_splitter.py", "tests/test_expense_splitter.py"],
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
    ]
    for command in commands:
        subprocess.run(command, cwd=project, check=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
    samples: dict[str, dict[str, Any]] = {}
    for key, args in {
        "even": ["10.00", "4"],
        "remainder": ["10.00", "3"],
        "invalid": ["10.001", "3"],
    }.items():
        completed = subprocess.run(
            [sys.executable, "expense_splitter.py", *args],
            cwd=project,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        samples[key] = {"returncode": completed.returncode, "stdout": completed.stdout, "stderr": completed.stderr}
    if samples["even"]["returncode"] != 0 or samples["remainder"]["returncode"] != 0 or samples["invalid"]["returncode"] == 0:
        raise RealProjectAcceptanceError("product acceptance samples failed")
    return {"automated": "passed", "samples": samples}


def rollback_restore(
    project: Path,
    allowed_root: Path,
    source: Path,
    *,
    require_product: bool = True,
    protected_paths: tuple[Path, ...] = (),
) -> dict[str, Any]:
    project = guarded_project(project, allowed_root)
    predecessor = validated_r11_artifact(guarded_private_source(source))
    current = r12_artifact()
    manager = DeliveryManager(project)
    require_delivery_state(manager, current, R12_ID)
    before = file_manifest(project, excludes=SNAPSHOT_EXCLUDES)
    head = git_head(project)
    protected = protected_boundary_snapshot(project, allowed_root, protected_paths)
    try:
        preview = manager.execute("rollback", current)
        if preview.get("status") != "planned" or file_manifest(project, excludes=SNAPSHOT_EXCLUDES) != before:
            raise RealProjectAcceptanceError("rollback preview changed non-delivery files")
        manager.execute("rollback", current, apply=True)
        require_delivery_state(manager, predecessor, R11_ID)
        r11_checks = run_product_checks(project) if require_product else {"automated": "not_required"}
        manager.execute("update", current, apply=True)
        require_delivery_state(manager, current, R12_ID)
        r12_checks = run_product_checks(project) if require_product else {"automated": "not_required"}
        if file_manifest(project, excludes=SNAPSHOT_EXCLUDES) != before or git_head(project) != head:
            raise RealProjectAcceptanceError("framework rollback or restore changed project-owned files")
    finally:
        assert_protected_boundaries_unchanged(
            protected,
            project,
            allowed_root,
            protected_paths,
        )
    return {
        "status": "pass",
        "rollback_target": R11_ID,
        "restored_target": R12_ID,
        "project_git_head": head,
        "non_delivery_files_unchanged": True,
        "protected_user_boundaries": len(protected),
        "r11_product_checks": r11_checks,
        "r12_product_checks": r12_checks,
    }


def write_evidence(path: Path | None, phase: str, payload: dict[str, Any]) -> None:
    if path is None:
        return
    target = path.expanduser().resolve()
    private_root = (ROOT / ".private-provenance").resolve()
    try:
        target.relative_to(private_root)
    except ValueError as exc:
        raise RealProjectAcceptanceError("evidence must stay under .private-provenance") from exc
    target.parent.mkdir(parents=True, exist_ok=True)
    evidence: dict[str, Any] = {}
    if target.exists():
        value = json.loads(target.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise RealProjectAcceptanceError("existing evidence is not an object")
        evidence = value
    evidence[phase] = payload
    temporary = target.with_name(target.name + f".tmp-{os.getpid()}")
    if temporary.exists():
        raise RealProjectAcceptanceError("evidence staging path already exists")
    try:
        temporary.write_text(
            json.dumps(evidence, indent=2, ensure_ascii=True) + "\n",
            encoding="utf-8",
        )
        os.replace(temporary, target)
    finally:
        if temporary.exists():
            temporary.unlink()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate CoTend G06 against a retained real local project")
    parser.add_argument(
        "phase",
        choices=(
            "prepare",
            "recover-prepare",
            "deliver",
            "run-init",
            "inspect",
            "rollback-restore",
        ),
    )
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--allowed-root", type=Path, required=True)
    parser.add_argument("--r11-source", type=Path, required=True)
    parser.add_argument("--evidence", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--model", default=MODEL)
    parser.add_argument("--reasoning-effort", default=REASONING_EFFORT)
    parser.add_argument("--protected-path", type=Path, action="append", default=[])
    parser.add_argument("--observed-path", type=Path, action="append", default=[])
    parser.add_argument("--isolated-runtime-root", type=Path)
    parser.add_argument("--carrier", choices=("native", "wsl2"), default="native")
    parser.add_argument("--wsl-distribution")
    parser.add_argument("--wsl-runtime-root")
    parser.add_argument("--auth-source", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        protected_paths = tuple(args.protected_path)
        source = extract_r11_source(args.r11_source)
        if args.phase == "prepare":
            result = prepare_project(
                args.project,
                args.allowed_root,
                protected_paths=protected_paths,
            )
            result["r11_manifest"] = source.manifest_sha256
            result["r12_manifest"] = r12_artifact().manifest_sha256
        elif args.phase == "recover-prepare":
            result = recover_prepared_project(
                args.project,
                args.allowed_root,
                protected_paths=protected_paths,
            )
            result["r11_manifest"] = source.manifest_sha256
            result["r12_manifest"] = r12_artifact().manifest_sha256
        elif args.phase == "deliver":
            result = deliver_r11_to_r12(
                args.project,
                args.allowed_root,
                args.r11_source,
                protected_paths=protected_paths,
            )
        elif args.phase == "run-init":
            if args.output is None:
                raise RealProjectAcceptanceError("run-init requires --output")
            if args.carrier == "wsl2":
                if (
                    args.wsl_distribution is None
                    or args.wsl_runtime_root is None
                    or args.auth_source is None
                    or args.isolated_runtime_root is not None
                ):
                    raise RealProjectAcceptanceError(
                        "WSL run-init requires --wsl-distribution, "
                        "--wsl-runtime-root, and --auth-source only"
                    )
                result = run_real_init_wsl(
                    args.project,
                    args.allowed_root,
                    args.output,
                    distribution=args.wsl_distribution,
                    runtime_root=args.wsl_runtime_root,
                    auth_source=args.auth_source,
                    evidence=args.evidence,
                    model=args.model,
                    reasoning_effort=args.reasoning_effort,
                    protected_paths=protected_paths,
                    observed_paths=tuple(args.observed_path),
                )
            else:
                if (
                    args.wsl_distribution is not None
                    or args.wsl_runtime_root is not None
                    or args.auth_source is not None
                ):
                    raise RealProjectAcceptanceError(
                        "native run-init cannot use WSL carrier arguments"
                    )
                result = run_real_init(
                    args.project,
                    args.allowed_root,
                    args.output,
                    model=args.model,
                    reasoning_effort=args.reasoning_effort,
                    protected_paths=protected_paths,
                    observed_paths=tuple(args.observed_path),
                    isolated_runtime_root=args.isolated_runtime_root,
                )
        elif args.phase == "rollback-restore":
            result = rollback_restore(
                args.project,
                args.allowed_root,
                args.r11_source,
                protected_paths=protected_paths,
            )
        else:
            project = guarded_project(args.project, args.allowed_root)
            current = r12_artifact()
            state = require_delivery_state(DeliveryManager(project), current, R12_ID)
            validate_response_schema(project / INIT_SCHEMA)
            result = {
                "status": "pass",
                "artifact_id": state["artifact_id"],
                "project_git_head": git_head(project),
                "response_schema_sha256": sha256(project / INIT_SCHEMA),
            }
        write_evidence(args.evidence, args.phase, result)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except (
        RealProjectAcceptanceError,
        DeliveryError,
        OSError,
        subprocess.SubprocessError,
        json.JSONDecodeError,
    ) as exc:
        print("NATIVE_REAL_PROJECT_ACCEPTANCE_FAILED", file=sys.stderr)
        print(f"- {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
