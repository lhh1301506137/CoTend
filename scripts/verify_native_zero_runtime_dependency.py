from __future__ import annotations

import hashlib
import json
import re
import shutil
import tempfile
from pathlib import Path
from typing import Any

import build_codex_plugin as plugin_package
import build_release_archive as release_archive
import verify_native_negative_recovery_ownership as native_negative_recovery


ROOT = Path(__file__).resolve().parents[1]
DOCUMENT_PATH = ROOT / "docs" / "NATIVE-ZERO-RUNTIME-DEPENDENCY.md"
EVIDENCE_PATH = (
    ROOT / "docs" / "evidence" / "NATIVE-ZERO-RUNTIME-DEPENDENCY-G05.md"
)
CONTRACT_PATH = ROOT / "upstream" / "TRELLIS-DECOUPLING-PLAN.json"
TARGET_LOCK_PATH = ROOT / "delivery" / "codex-artifact.lock.json"
PACKAGE_LOCK_PATH = ROOT / "packaging" / "codex-plugin" / "package.lock.json"

EXPECTED_TARGET_ID = "cotend-codex-r000016"
EXPECTED_TARGET_REVISION = 16
EXPECTED_TARGET_MANIFEST = (
    "a7f7ece2522a5901030e19cd5944359f80c027482f66f822a2053fc5080dcfb5"
)
EXPECTED_R15_MANIFEST = (
    "acc17586cf713acc85fef9e6be02013de6bc012b7864ade22bed495ee68a9e7b"
)
EXPECTED_R14_MANIFEST = (
    "07ac592c82ed87f1759b38f04ed1f453c44e21d454fd12b4ce9eca459e4f3ed4"
)
EXPECTED_R13_MANIFEST = (
    "39e1455b11f482d80d33dff421e0db5c08182f597c175f0391bd679750f903fd"
)
EXPECTED_R12_MANIFEST = (
    "44419b00c17ab0036477c6c3b9843f239a6a567ee714ccf7828b40a4af195276"
)
EXPECTED_R11_MANIFEST = (
    "eac48844295f9ba12d64df469aa25fab9e76a8c9ceb9817857350b5029767627"
)
EXPECTED_R10_MANIFEST = (
    "0715c20f517f906996d4882e47c664449a23cf6f7747b6a2d42835f35591b8a9"
)
EXPECTED_RC2_PACKAGE_MANIFEST = (
    "a61b75d08572c95d2c8593939724b48f1b06dce2aa916bab8fb00b2439d76dc2"
)
EXPECTED_RC2_ZIP_SHA256 = (
    "b28e63c83ad80e5885594574a46b19fb901af92cc38fe2110448d1b8ee122547"
)

EXPECTED_PREDECESSORS = [
    (
        revision,
        manifest,
    )
    for revision, manifest in (
        (15, EXPECTED_R15_MANIFEST),
        (14, EXPECTED_R14_MANIFEST),
        (13, EXPECTED_R13_MANIFEST),
        (12, EXPECTED_R12_MANIFEST),
        (11, EXPECTED_R11_MANIFEST),
        (10, EXPECTED_R10_MANIFEST),
        (9, "32049aa36e25d0a46eacf92ce2cf06c42b688947e93fc3c6d6b1ae478a019072"),
        (8, "84c4c02a2d56502b7ed9457fad23e0077ff8a9cf567c544ea7fdaf54c6a94bc3"),
        (7, "246b16c990a85a2e183e0033c0b3a15a087e793ce0ace1f18e3d736f5a8fd045"),
        (6, "58410dbbf9ab0945af62cea0583938c5f5bc733634a72035c5b06e6c71073271"),
        (5, "319f9f889b400d7a642de6ac81319ceac4aea493209b7b5527dd947f9ccade23"),
        (4, "9b82dc8689e19c9d95c7b867c18adc3b50d32d7c82aa772b6d397aa3a70a4abd"),
        (3, "ae7c033c3038af5de34623d683c60f78370921dd80788785d52257f7c82f4fac"),
        (2, "0f6c8781869a723846394fe9161e01c29793a7b366e9566dba79ae41ed691c1b"),
    )
]

REQUIRED_RUNTIME_CAPABILITY_MARKERS = {
    "cotend-semantic-alignment/SKILL.md": (
        "Plan Tree, implementation, verification, semantic implementation closure, formal review, AI UAT, and Done Gate routes",
    ),
    "cotend-collaboration/references/authority-and-triggers.md": (
        "archived external-framework tasks",
        "do not need mechanical renames",
    ),
    "cotend-collaboration/references/framework-change-evaluation.md": (
        "Plan Tree/external-framework/CodeGraph routing",
    ),
    "cotend-collaboration/references/plan-tree.md": (
        "done_gate | external_framework | other",
        "linked active/archived external-framework tasks",
        "Older provider-specific source values remain evidence-only migration inputs",
        "without granting the provider route authority",
    ),
    "cotend-collaboration/references/quality-sentinel.md": (
        "skipped required Skill/module/external-framework phase/review/verification step",
    ),
    "cotend-collaboration/references/upstream-dependency-review.md": (
        "pure external-framework evidence",
        "exact-range disposition override with a non-empty reason",
    ),
}

REQUIRED_DOCUMENT_MARKERS = (
    "# CoTend 第一方运行包零外部开发框架依赖",
    "## 四类零库存",
    "## 能力保留",
    "## r11 与冻结 rc.2",
    "不是 G06",
    "不构建 rc.3",
)
REQUIRED_EVIDENCE_MARKERS = (
    "gate: G05-zero-runtime-dependency",
    "status: complete",
    "source_runtime_mentions: 0",
    "packaged_runtime_mentions: 0",
    "runtime_commands: 0",
    "runtime_state_paths: 0",
    "external_task_spec_authority: 0",
    "retained_capability_surfaces: 7",
    "development_target_artifact: cotend-codex-r000011",
    f"development_target_manifest: {EXPECTED_R11_MANIFEST}",
    "predecessor_target_artifact: cotend-codex-r000010",
    "g02_native_capabilities: 8",
    "g03_cumulative: passed",
    "g04_negative_recovery: passed",
    "real_project_claimed: false",
    "real_user_acceptance_claimed: false",
    "rc3_built: false",
    "public_action: false",
)

NAME_PATTERN = re.compile(r"trellis", re.IGNORECASE)
COMMAND_PATTERN = re.compile(
    r"(?<![A-Za-z0-9_-])(?:[$/])?trellis-[a-z0-9-]+\b",
    re.IGNORECASE,
)
STATE_PATTERNS = (
    re.compile(
        r"(?<![A-Za-z0-9_-])\.trellis(?=[\\/`'\"\s.,;:)]|$)",
        re.IGNORECASE,
    ),
    re.compile(r"\btrellis\.mode\b", re.IGNORECASE),
)
NEGATION_TOKENS = (
    "never",
    "not ",
    "no ",
    "without",
    "cannot",
    "must not",
    "false",
    "evidence-only",
    "reference_only",
    "historical",
    "conflict",
    "does not",
)
CLAUSE_SPLIT_PATTERN = re.compile(r"[.;!?]+")
EXTERNAL_FRAMEWORK_EXPR = (
    r"(?:external-framework|external framework|external_framework)"
    r"(?:\s+(?:task|prd|spec|artifact|state))?"
)
AUTHORITY_NOUN_EXPR = (
    r"(?:binding(?:\s+(?:authority|route owner|task owner|spec owner))?"
    r"|authoritative|highest authority|route owner|task owner|spec owner)"
)
EXTERNAL_AUTHORITY_PATTERNS = (
    re.compile(
        rf"{EXTERNAL_FRAMEWORK_EXPR}.{{0,80}}?\b"
        rf"(?:is|becomes?|remains?|acts?\s+as|serves?\s+as|has|takes?|assumes?)"
        rf"\b.{{0,40}}?{AUTHORITY_NOUN_EXPR}",
        re.IGNORECASE,
    ),
    re.compile(
        rf"{EXTERNAL_FRAMEWORK_EXPR}.{{0,80}}?"
        r"(?:owns?\s+the\s+route|owns?\s+project\s+truth)",
        re.IGNORECASE,
    ),
    re.compile(
        rf"{AUTHORITY_NOUN_EXPR}.{{0,80}}?\b"
        r"(?:is|belongs?\s+to|is\s+(?:assigned|delegated)\s+to|comes?\s+from)"
        rf"\b.{{0,40}}?{EXTERNAL_FRAMEWORK_EXPR}",
        re.IGNORECASE,
    ),
)


class NativeZeroRuntimeDependencyError(ValueError):
    pass


def _load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise NativeZeroRuntimeDependencyError(
            f"{label} is not readable JSON"
        ) from exc
    if not isinstance(value, dict):
        raise NativeZeroRuntimeDependencyError(f"{label} must be a JSON object")
    return value


def _require_markers(text: str, markers: tuple[str, ...], label: str) -> None:
    missing = [marker for marker in markers if marker not in text]
    if missing:
        raise NativeZeroRuntimeDependencyError(
            f"{label} is missing required markers: {', '.join(missing)}"
        )


def _line_hits(relative: str, text: str, pattern: re.Pattern[str]) -> list[str]:
    return [
        f"{relative}:{line_number}:{line.strip()}"
        for line_number, line in enumerate(text.splitlines(), start=1)
        if pattern.search(line)
    ]


def _external_authority_hits(relative: str, text: str) -> list[str]:
    findings: list[str] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for clause in CLAUSE_SPLIT_PATTERN.split(line):
            for pattern in EXTERNAL_AUTHORITY_PATTERNS:
                match = pattern.search(clause)
                if match is None:
                    continue
                if any(token in match.group(0).lower() for token in NEGATION_TOKENS):
                    continue
                findings.append(f"{relative}:{line_number}:{line.strip()}")
                break
            else:
                continue
            break
    return findings


def scan_runtime(skills_root: Path) -> dict[str, list[str]]:
    result = {
        "name_hits": [],
        "command_hits": [],
        "state_path_hits": [],
        "external_authority_hits": [],
        "missing_capability_markers": [],
    }
    texts: dict[str, str] = {}
    for path in sorted(skills_root.rglob("*")):
        if (
            not path.is_file()
            or "__pycache__" in path.parts
            or path.suffix == ".pyc"
        ):
            continue
        relative = path.relative_to(skills_root).as_posix()
        text = path.read_text(encoding="utf-8")
        texts[relative] = text
        result["name_hits"].extend(_line_hits(relative, text, NAME_PATTERN))
        result["command_hits"].extend(_line_hits(relative, text, COMMAND_PATTERN))
        for pattern in STATE_PATTERNS:
            result["state_path_hits"].extend(
                _line_hits(relative, text, pattern)
            )
        result["external_authority_hits"].extend(
            _external_authority_hits(relative, text)
        )

    for relative, markers in REQUIRED_RUNTIME_CAPABILITY_MARKERS.items():
        text = texts.get(relative)
        if text is None:
            result["missing_capability_markers"].append(f"missing-file:{relative}")
            continue
        for marker in markers:
            if marker not in text:
                result["missing_capability_markers"].append(
                    f"{relative}:{marker}"
                )
    return result


def assert_runtime_scan_clean(scan: dict[str, list[str]], label: str) -> None:
    failures = {
        key: values
        for key, values in scan.items()
        if values
    }
    if failures:
        details = "; ".join(
            f"{key}={values[0]}" for key, values in failures.items()
        )
        raise NativeZeroRuntimeDependencyError(f"{label} failed: {details}")


def _manifest(root: Path) -> tuple[dict[str, str], str]:
    files = {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
    }
    digest = hashlib.sha256(
        json.dumps(
            files,
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()
    return files, digest


def validate_target_lock(
    lock: dict[str, Any], *, manifest_sha256: str, skill_file_count: int
) -> None:
    expected_source = {
        "framework_lock": "upstream/framework.lock.json",
        "release_id": (
            "exact-source:c14d4133bf0438d435048858554c88c89a7870a3"
        ),
        "carrier": "skills/",
        "framework_protocol": "cotend-collaboration-v1.79",
    }
    expected_target = {
        "platform": "Codex",
        "lineage": "cotend-codex",
        "artifact_id": EXPECTED_TARGET_ID,
        "revision": EXPECTED_TARGET_REVISION,
        "manifest_sha256": manifest_sha256,
    }
    if (
        lock.get("schema") != "cotend.target-artifact-lock"
        or lock.get("schema_version") != 1
        or lock.get("status") != "verified"
        or lock.get("source") != expected_source
        or lock.get("target") != expected_target
        or lock.get("product") != {"version": None}
        or lock.get("skill_count") != 10
        or lock.get("skill_file_count") != skill_file_count
    ):
        raise NativeZeroRuntimeDependencyError("r16 target lock envelope drifted")

    expected_predecessors = [
        {
            "platform": "Codex",
            "lineage": "cotend-codex",
            "artifact_id": f"cotend-codex-r{revision:06d}",
            "revision": revision,
            "source_release_id": (
                "exact-source:774aab64e778d2e3a57b66cfd65d808ac8235e14"
                if revision == 15
                else "exact-source:9e6bbeeb4b91f98406e60dcbced923b3e1dd6826"
                if revision == 14
                else "2026.07.28.2"
                if revision == 13
                else "2026.07.28.1"
                if revision == 12
                else "2026.07.23.2"
            ),
            "framework_protocol": (
                "cotend-collaboration-v1.76"
                if revision == 15
                else "cotend-collaboration-v1.71"
                if revision == 14
                else "cotend-collaboration-v1.67"
                if revision == 13
                else "cotend-collaboration-v1.66"
                if revision == 12
                else "cotend-collaboration-v1.65"
            ),
            "manifest_sha256": manifest,
        }
        for revision, manifest in EXPECTED_PREDECESSORS
    ]
    if lock.get("predecessor_targets") != expected_predecessors:
        raise NativeZeroRuntimeDependencyError(
            "r15-r2 predecessor identity chain drifted"
        )


def validate_frozen_rc2_lock(lock: dict[str, Any]) -> None:
    plugin = lock.get("plugin")
    source = lock.get("source")
    package = lock.get("package")
    build = lock.get("build")
    authority = lock.get("authority")
    if (
        lock.get("schema") != "cotend.codex-plugin-package-lock"
        or lock.get("schema_version") != 2
        or lock.get("status") != "production_candidate_not_published"
        or not isinstance(plugin, dict)
        or plugin.get("name") != "cotend"
        or plugin.get("version") != "0.1.0-rc.2"
        or not isinstance(source, dict)
        or source.get("source_commit")
        != "37e657f0a1e2ddb7b2094f8e4708c2b7563380c1"
        or source.get("artifact_id") != "cotend-codex-r000002"
        or source.get("revision") != 2
        or source.get("target_manifest_sha256")
        != "0f6c8781869a723846394fe9161e01c29793a7b366e9566dba79ae41ed691c1b"
        or source.get("skill_count") != 8
        or source.get("skill_file_count") != 37
        or not isinstance(package, dict)
        or package.get("file_count") != 48
        or package.get("path_hash_manifest_sha256")
        != EXPECTED_RC2_PACKAGE_MANIFEST
        or not isinstance(build, dict)
        or build.get("network_required") is not False
        or build.get("plugin_installation_performed") is not False
        or not isinstance(authority, dict)
        or authority.get("release_or_publish_authorized") is not False
    ):
        raise NativeZeroRuntimeDependencyError("frozen rc.2 package lock drifted")


def validate_decoupling_contract(contract: dict[str, Any]) -> None:
    gates = contract.get("gates")
    if not isinstance(gates, list):
        raise NativeZeroRuntimeDependencyError("decoupling gates are missing")
    statuses = {
        gate.get("id"): gate.get("status")
        for gate in gates
        if isinstance(gate, dict)
    }
    if any(
        statuses.get(f"G{number:02d}-" + suffix) != "complete"
        for number, suffix in (
            (1, "baseline-freeze"),
            (2, "per-capability-native-parity"),
            (3, "cumulative-main-journey"),
            (4, "negative-recovery-and-ownership"),
            (5, "zero-runtime-dependency"),
        )
    ):
        raise NativeZeroRuntimeDependencyError("G01-G05 are not complete")
    if (
        contract.get("development_target_artifact") != EXPECTED_TARGET_ID
        or contract.get("current_runtime")
        != {
            "scope": "skills/",
            "case_insensitive_term": "trellis",
            "mention_count": 0,
            "file_count": 0,
            "file_mentions": {},
        }
    ):
        raise NativeZeroRuntimeDependencyError("G05 runtime contract drifted")

    historical_g05_slice = {
        "skill_behavior_changed": True,
        "trellis_route_removed": True,
        "removed_capability_ids": [],
        "target_artifact_changed": True,
        "package_identity_changed": False,
        "push_release_submission_or_publish": False,
        "validation_gate_completed": "G05-zero-runtime-dependency",
    }
    current_r16_slice = {
        "skill_behavior_changed": True,
        "trellis_route_removed": False,
        "removed_capability_ids": [],
        "target_artifact_changed": True,
        "package_identity_changed": False,
        "push_release_submission_or_publish": False,
        "validation_gate_completed": "G01-G05-regression-for-r16",
        "g06_current_target_status": "not_rerun_frozen_r13_evidence",
    }
    lifecycle = (
        statuses.get("G06-real-project-and-rollback"),
        contract.get("status"),
        contract.get("this_slice"),
    )
    if lifecycle not in (
        (
            "not_started",
            "native_runtime_decoupled_waiting_real_project",
            historical_g05_slice,
        ),
        (
            "complete",
            "native_runtime_decoupled_real_project_verified",
            current_r16_slice,
        ),
    ):
        raise NativeZeroRuntimeDependencyError(
            "G05/G06 machine-contract lifecycle drifted"
        )


def verify_disposable_runtime(root: Path = ROOT) -> dict[str, Any]:
    source_files, source_digest = _manifest(root / "skills")
    with tempfile.TemporaryDirectory(prefix="cotend-g05-runtime-") as temporary:
        packaged_skills = Path(temporary) / "skills"
        shutil.copytree(root / "skills", packaged_skills)
        packaged_files, packaged_digest = _manifest(packaged_skills)
        if packaged_files != source_files or packaged_digest != source_digest:
            raise NativeZeroRuntimeDependencyError(
                "disposable runtime copy differs from current Skills"
            )
        packaged_scan = scan_runtime(packaged_skills)
        assert_runtime_scan_clean(packaged_scan, "disposable packaged runtime")
    return {
        "skill_files": len(source_files),
        "manifest_sha256": source_digest,
        "packaged_runtime_mentions": 0,
    }


def verify_frozen_rc2(root: Path = ROOT) -> dict[str, Any]:
    validate_frozen_rc2_lock(_load_json(root / PACKAGE_LOCK_PATH.relative_to(ROOT), "rc.2 lock"))
    contract = plugin_package.validate_contract()
    if (
        len(contract["source_manifest"]) != 37
        or contract["source_commit"]
        != "37e657f0a1e2ddb7b2094f8e4708c2b7563380c1"
        or contract["source_manifest"] == contract["repository_source_manifest"]
    ):
        raise NativeZeroRuntimeDependencyError("rc.2 historical source boundary drifted")

    dist_root = root / "dist"
    dist_root.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=".g05-rc2-", dir=dist_root))
    try:
        archive = release_archive.build_release_archive(temporary)
    finally:
        shutil.rmtree(temporary)
    if (
        archive.get("package_manifest_sha256") != EXPECTED_RC2_PACKAGE_MANIFEST
        or archive.get("archive_sha256") != EXPECTED_RC2_ZIP_SHA256
        or archive.get("package_files") != 48
    ):
        raise NativeZeroRuntimeDependencyError("frozen rc.2 archive drifted")
    return {
        "package_files": 48,
        "package_manifest_sha256": EXPECTED_RC2_PACKAGE_MANIFEST,
        "archive_sha256": EXPECTED_RC2_ZIP_SHA256,
    }


def verify_no_regression(root: Path = ROOT) -> dict[str, Any]:
    result = native_negative_recovery.verify_repository(root)
    if (
        result.get("status") != "native_negative_recovery_ownership_verified"
        or result.get("native_capabilities_composed") != 8
        or result.get("dual_capability_baseline") != 19
        or result.get("mapped_skill_roles") != 10
        or result.get("target_artifact") != EXPECTED_TARGET_ID
        or result.get("target_manifest_sha256") != EXPECTED_TARGET_MANIFEST
        or result.get("real_project_claimed") is not False
        or result.get("real_user_acceptance_claimed") is not False
    ):
        raise NativeZeroRuntimeDependencyError(
            "C01-C19, ten Skills, or G02-G04 regressed"
        )
    return result


def verify_repository(root: Path = ROOT) -> dict[str, Any]:
    _require_markers(
        (root / DOCUMENT_PATH.relative_to(ROOT)).read_text(encoding="utf-8"),
        REQUIRED_DOCUMENT_MARKERS,
        "native zero-runtime document",
    )
    _require_markers(
        (root / EVIDENCE_PATH.relative_to(ROOT)).read_text(encoding="utf-8"),
        REQUIRED_EVIDENCE_MARKERS,
        "native zero-runtime evidence",
    )

    source_scan = scan_runtime(root / "skills")
    assert_runtime_scan_clean(source_scan, "source runtime")
    runtime = verify_disposable_runtime(root)
    if (
        runtime["skill_files"] != 71
        or runtime["manifest_sha256"] != EXPECTED_TARGET_MANIFEST
    ):
        raise NativeZeroRuntimeDependencyError("r16 Skill manifest drifted")

    lock = _load_json(root / TARGET_LOCK_PATH.relative_to(ROOT), "target lock")
    validate_target_lock(
        lock,
        manifest_sha256=runtime["manifest_sha256"],
        skill_file_count=runtime["skill_files"],
    )
    validate_decoupling_contract(
        _load_json(root / CONTRACT_PATH.relative_to(ROOT), "decoupling contract")
    )
    try:
        regression = verify_no_regression(root)
        frozen = verify_frozen_rc2(root)
    except NativeZeroRuntimeDependencyError:
        raise
    except (
        native_negative_recovery.NativeNegativeRecoveryError,
        plugin_package.PluginPackageError,
        release_archive.ReleaseArchiveError,
    ) as exc:
        raise NativeZeroRuntimeDependencyError(
            f"nested G05 verification failed: {exc}"
        ) from exc

    return {
        "status": "native_zero_runtime_dependency_verified",
        "gate": "G05-zero-runtime-dependency",
        "source_runtime_mentions": 0,
        "packaged_runtime_mentions": 0,
        "runtime_commands": 0,
        "runtime_state_paths": 0,
        "external_task_spec_authority": 0,
        "retained_capability_surfaces": len(REQUIRED_RUNTIME_CAPABILITY_MARKERS) + 1,
        "native_capabilities": regression["native_capabilities_composed"],
        "dual_capabilities": regression["dual_capability_baseline"],
        "mapped_skill_roles": regression["mapped_skill_roles"],
        "target_artifact": EXPECTED_TARGET_ID,
        "target_manifest_sha256": EXPECTED_TARGET_MANIFEST,
        "predecessor_target": "cotend-codex-r000015",
        "frozen_rc2": frozen,
        "real_project_claimed": False,
        "real_user_acceptance_claimed": False,
        "rc3_built": False,
        "public_action": False,
    }


def main() -> int:
    try:
        result = verify_repository()
    except (
        OSError,
        NativeZeroRuntimeDependencyError,
        native_negative_recovery.NativeNegativeRecoveryError,
        plugin_package.PluginPackageError,
        release_archive.ReleaseArchiveError,
    ) as exc:
        print("NATIVE_ZERO_RUNTIME_DEPENDENCY_FAILED")
        print(f"- {exc}")
        return 1
    print(
        "NATIVE_ZERO_RUNTIME_DEPENDENCY_OK "
        f"gate={result['gate']} mentions=0 commands=0 state_paths=0 "
        f"authority=0 capabilities={result['native_capabilities']} "
        f"target={result['target_artifact']} rc3_built=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
