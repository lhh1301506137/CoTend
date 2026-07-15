from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import build_codex_plugin as package  # noqa: E402


SUBMISSION_PATH = (
    ROOT / "packaging" / "codex-plugin" / "submission-materials" / "submission.json"
)
REVIEWER_TESTS_PATH = SUBMISSION_PATH.with_name("reviewer-tests.json")
REVIEWER_FIXTURES_PATH = SUBMISSION_PATH.with_name("reviewer-fixtures.json")
OFFICIAL_SUBMISSION_URL = "https://developers.openai.com/codex/submit-plugins"
REPOSITORY_URL = "https://github.com/lhh1301506137/CoTend"
EXPECTED_POSITIVE_IDS = [f"P{number:02d}" for number in range(1, 6)]
EXPECTED_NEGATIVE_IDS = [f"N{number:02d}" for number in range(1, 4)]
EXPECTED_BLOCKER_IDS = [
    "final_plugin_identity_and_version",
    "verified_publisher_identity",
    "apps_management_write_access",
    "production_logo",
    "website_url",
    "support_url",
    "privacy_policy_url",
    "terms_url",
    "country_or_region_availability",
    "policy_attestations",
]
EXPECTED_IDENTITY_VALUE = {
    "plugin_id": "cotend",
    "version": "0.1.0-rc.1",
    "package_digest": "18f0b62852ebe1f7afbd43bcbff50706aacd1d66ae6edeb4c5b133d53fdd858f",
    "confirmed_on": "2026-07-14",
    "confirmation_scope": (
        "initial_submission_identity_not_release_or_platform_acceptance"
    ),
    "platform_prerelease_acceptance": "not_verified_reopen_q02_if_rejected",
}
EXPECTED_PRODUCTION_LOGO_VALUE = {
    "source_asset_path": "assets/cotend-mark.svg",
    "source_sha256": "27c5a8566bb4d7800f9250715aef649adf5806b35784955a093cc37cf477238a",
    "dark_source_asset_path": "assets/cotend-mark-dark.svg",
    "dark_source_sha256": (
        "63e1f28fee998a7d3a7d39a381d2990132ed5f9c63a70a10fd533ef2dbb1afac"
    ),
    "primary_asset_path": "assets/cotend-logo.png",
    "primary_sha256": "3a39de1b6c956b37a5e6efc0fb616a06104ce9d9417d3157ab5c5a002af72d49",
    "dark_asset_path": "assets/cotend-logo-dark.png",
    "dark_sha256": "dc495bcbdba3c35f32e60a7f4d250593007de3e5620431f3b780d98a5e4c46fe",
    "user_confirmed_on": "2026-07-14",
    "confirmation_scope": (
        "repository_production_asset_not_portal_upload_or_format_verification"
    ),
    "portal_exact_format": "not_verified",
}
EXPECTED_RESOLVED_BLOCKER_VALUES = {
    "final_plugin_identity_and_version": EXPECTED_IDENTITY_VALUE,
    "production_logo": EXPECTED_PRODUCTION_LOGO_VALUE,
}
EXPECTED_UNRESOLVED_BLOCKER_IDS = [
    blocker_id
    for blocker_id in EXPECTED_BLOCKER_IDS
    if blocker_id not in EXPECTED_RESOLVED_BLOCKER_VALUES
]
EXPECTED_AUTHORITY = {
    "repository_contract_only": True,
    "portal_opened": False,
    "portal_draft_created": False,
    "submitted_for_review": False,
    "approved": False,
    "published": False,
    "release_authorized": False,
    "push_authorized": False,
}
EXPECTED_REVIEW_CONTEXT = {
    "plugin_specific_authentication_required": False,
    "plugin_specific_account_required": False,
    "plugin_backend_required": False,
    "api_key_required": False,
    "demo_credentials_required": False,
    "private_network_required": False,
    "fixture_policy": (
        "Use a disposable local Git repository containing only the files "
        "described by each case."
    ),
}
EXPECTED_FIXTURE_KIT = {
    "file": REVIEWER_FIXTURES_PATH.relative_to(ROOT).as_posix(),
    "status": "repository_fixture_kit_ready_model_execution_not_run",
    "materializer": "scripts/prepare_reviewer_fixtures.py",
    "case_count": 8,
    "preflight_count": 5,
}
ALLOWED_PUBLIC_URLS = {OFFICIAL_SUBMISSION_URL, REPOSITORY_URL}
PRIVATE_TEXT_MARKERS = (
    ".private-provenance",
    "PROJECT-DECISION-LOG",
    "PROJECT-KNOWLEDGE-CHANGELOG",
    "PROJECT-PLAN-NODES",
    "REVIEW-LOG",
)


class SubmissionMaterialError(ValueError):
    pass


def load_json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SubmissionMaterialError(f"{label} is not readable JSON") from exc
    if not isinstance(payload, dict):
        raise SubmissionMaterialError(f"{label} must be a JSON object")
    return payload


def _exact_keys(value: Any, expected: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != expected:
        raise SubmissionMaterialError(f"{label} fields drifted")
    return value


def _non_empty_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SubmissionMaterialError(f"{label} must be non-empty text")
    return value


def _iter_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [text for item in value for text in _iter_strings(item)]
    if isinstance(value, dict):
        return [text for item in value.values() for text in _iter_strings(item)]
    return []


def _validate_public_text(*payloads: dict[str, Any]) -> None:
    for text in _iter_strings(list(payloads)):
        if re.search(r"[\u3400-\u9fff]", text):
            raise SubmissionMaterialError("submission-facing text must be English")
        if re.search(r"\b[A-Za-z]:[\\/]", text) or text.startswith(
            ("/home/", "/Users/")
        ):
            raise SubmissionMaterialError(
                "submission materials contain an absolute local path"
            )
        if any(marker.lower() in text.lower() for marker in PRIVATE_TEXT_MARKERS):
            raise SubmissionMaterialError(
                "submission materials contain private governance context"
            )
        if re.search(
            r"\b(?:TBD|TODO)\b|placeholder|example\.com|localhost|file://", text, re.I
        ):
            raise SubmissionMaterialError(
                "submission materials contain a placeholder value"
            )
        urls = re.findall(r"https?://[^\s\"'<>]+", text)
        if any(url not in ALLOWED_PUBLIC_URLS for url in urls):
            raise SubmissionMaterialError(
                "submission materials contain an unapproved URL"
            )


def _expected_package_binding(contract: dict[str, Any]) -> dict[str, Any]:
    manifest = contract["manifest"]
    lock = contract["lock"]
    expected_manifest = contract["expected_package_manifest"]
    return {
        "plugin_id": manifest["name"],
        "version": manifest["version"],
        "package_status": lock["status"],
        "package_lock": "packaging/codex-plugin/package.lock.json",
        "manifest": lock["plugin"]["manifest"],
        "manifest_sha256": lock["plugin"]["manifest_sha256"],
        "file_count": len(expected_manifest),
        "path_hash_manifest_sha256": package.path_hash_manifest_sha256(
            expected_manifest
        ),
        "skill_count": lock["source"]["skill_count"],
        "skill_file_count": lock["source"]["skill_file_count"],
        "source_skill_manifest_sha256": lock["source"]["path_hash_manifest_sha256"],
        "identity_authority": "initial_submission_identity_confirmed_not_release",
        "final_identity_confirmed": lock["authority"][
            "final_plugin_identity_confirmed"
        ],
    }


def _validate_submission(
    submission: dict[str, Any],
    reviewer_tests: dict[str, Any],
    package_contract: dict[str, Any],
) -> None:
    _exact_keys(
        submission,
        {
            "schema",
            "schema_version",
            "status",
            "official_requirements",
            "package",
            "listing",
            "publisher",
            "skills",
            "starter_prompts",
            "reviewer_tests",
            "availability",
            "release_notes",
            "policy_attestations",
            "blockers",
            "readiness",
            "authority",
        },
        "submission contract",
    )
    if submission["schema"] != "cotend.codex-plugin-submission-materials":
        raise SubmissionMaterialError("submission schema drifted")
    if (
        submission["schema_version"] != 1
        or submission["status"] != "draft_not_submitted"
    ):
        raise SubmissionMaterialError("submission must remain a non-submitted v1 draft")
    if submission["official_requirements"] != {
        "source": OFFICIAL_SUBMISSION_URL,
        "checked_on": "2026-07-14",
        "submission_type": "skills_only",
    }:
        raise SubmissionMaterialError("official requirement anchor drifted")

    expected_package = _expected_package_binding(package_contract)
    if submission["package"] != expected_package:
        raise SubmissionMaterialError("submission package binding drifted")

    manifest = package_contract["manifest"]
    interface = manifest["interface"]
    listing = submission["listing"]
    if listing != {
        "plugin_name": interface["displayName"],
        "short_description": interface["shortDescription"],
        "long_description": interface["longDescription"],
        "category": interface["category"],
        "candidate_developer_name": interface["developerName"],
        "source_repository_url": manifest["repository"],
        "logo": {
            "status": "repository_asset_ready_portal_format_not_verified",
            "asset_path": interface["logo"].removeprefix("./"),
        },
        "public_urls": {
            "website_url": None,
            "support_url": None,
            "privacy_policy_url": None,
            "terms_url": None,
        },
    }:
        raise SubmissionMaterialError("listing copy or required gaps drifted")

    if submission["publisher"] != {
        "candidate_display_name": interface["developerName"],
        "verified_identity": None,
        "verification_status": "not_verified_or_selected",
        "apps_management_write_access": "not_checked",
    }:
        raise SubmissionMaterialError("publisher identity boundary drifted")
    if submission["skills"] != {
        "bundle_type": "skills_only",
        "bundle_status": "production_candidate_locally_verified",
        "bundle_source": "packaging/codex-plugin/package.lock.json",
        "skill_count": 7,
        "skill_file_count": 30,
        "upload_performed": False,
        "mcp_server_required": False,
    }:
        raise SubmissionMaterialError("skills-only bundle state drifted")
    if submission["starter_prompts"] != interface["defaultPrompt"]:
        raise SubmissionMaterialError("starter prompts differ from the Plugin manifest")
    if len(submission["starter_prompts"]) != 3 or any(
        len(prompt) > 128 for prompt in submission["starter_prompts"]
    ):
        raise SubmissionMaterialError("starter prompt count or length drifted")

    if submission["reviewer_tests"] != {
        "file": REVIEWER_TESTS_PATH.relative_to(ROOT).as_posix(),
        "positive_count": 5,
        "negative_count": 3,
        "execution_status": "contract_only_not_run",
        "fixture_kit": REVIEWER_FIXTURES_PATH.relative_to(ROOT).as_posix(),
        "fixture_kit_status": "repository_fixture_kit_ready_model_execution_not_run",
    }:
        raise SubmissionMaterialError("reviewer test summary drifted")
    if submission["availability"] != {
        "status": "not_selected",
        "countries_or_regions": [],
    }:
        raise SubmissionMaterialError("availability must remain unselected")
    if submission["policy_attestations"] != {
        "status": "not_completed",
        "attestations": [],
    }:
        raise SubmissionMaterialError("policy attestations must remain incomplete")

    release_notes = _exact_keys(
        submission["release_notes"],
        {
            "status",
            "submission_kind",
            "what_plugin_does",
            "initial_or_update",
            "changes_since_prior_submitted_version",
            "reviewer_setup",
        },
        "release notes",
    )
    if release_notes["status"] != "draft_not_submitted":
        raise SubmissionMaterialError("release notes must remain a draft")
    if release_notes["submission_kind"] != "initial_submission":
        raise SubmissionMaterialError(
            "release notes must describe an initial submission"
        )
    for key in (
        "what_plugin_does",
        "initial_or_update",
        "changes_since_prior_submitted_version",
        "reviewer_setup",
    ):
        _non_empty_text(release_notes[key], f"release notes {key}")

    blockers = submission["blockers"]
    if (
        not isinstance(blockers, list)
        or [item.get("id") for item in blockers if isinstance(item, dict)]
        != EXPECTED_BLOCKER_IDS
    ):
        raise SubmissionMaterialError("submission blocker inventory drifted")
    expected_blocker_keys = {"id", "status", "value", "required_before", "owner"}
    for blocker in blockers:
        _exact_keys(blocker, expected_blocker_keys, "submission blocker")
        expected_value = EXPECTED_RESOLVED_BLOCKER_VALUES.get(blocker["id"])
        if expected_value is not None:
            if (
                blocker["status"] != "resolved"
                or blocker["value"] != expected_value
            ):
                raise SubmissionMaterialError(
                    "confirmed repository blocker evidence drifted"
                )
        elif blocker["status"] != "unresolved" or blocker["value"] is not None:
            raise SubmissionMaterialError(
                "submission blocker was resolved without evidence"
            )
        if (
            blocker["required_before"] != "portal_submission"
            or blocker["owner"] != "publisher"
        ):
            raise SubmissionMaterialError("submission blocker ownership drifted")
    if submission["readiness"] != {
        "status": "blocked_not_ready_for_portal_submission",
        "unresolved_blocker_ids": EXPECTED_UNRESOLVED_BLOCKER_IDS,
        "portal_submission_ready": False,
    }:
        raise SubmissionMaterialError(
            "submission readiness overstates current evidence"
        )
    if submission["authority"] != EXPECTED_AUTHORITY:
        raise SubmissionMaterialError("submission or publication authority drifted")

    review_package = reviewer_tests.get("package")
    if review_package != {
        "plugin_id": expected_package["plugin_id"],
        "version": expected_package["version"],
        "path_hash_manifest_sha256": expected_package["path_hash_manifest_sha256"],
    }:
        raise SubmissionMaterialError(
            "reviewer tests are not bound to the same package"
        )


def _validate_fixture(value: Any, label: str) -> None:
    fixture = _exact_keys(
        value,
        {
            "name",
            "setup",
            "plugin_specific_authentication_required",
            "external_fixture_network_required",
            "private_context_required",
        },
        label,
    )
    _non_empty_text(fixture["name"], f"{label} name")
    _non_empty_text(fixture["setup"], f"{label} setup")
    for key in (
        "plugin_specific_authentication_required",
        "external_fixture_network_required",
        "private_context_required",
    ):
        if fixture[key] is not False:
            raise SubmissionMaterialError(
                f"{label} must remain public and self-contained"
            )


def _validate_reviewer_tests(reviewer_tests: dict[str, Any]) -> None:
    _exact_keys(
        reviewer_tests,
        {
            "schema",
            "schema_version",
            "status",
            "package",
            "reviewer_context",
            "fixture_kit",
            "positive_cases",
            "negative_cases",
        },
        "reviewer test contract",
    )
    if reviewer_tests["schema"] != "cotend.codex-plugin-reviewer-tests":
        raise SubmissionMaterialError("reviewer test schema drifted")
    if (
        reviewer_tests["schema_version"] != 1
        or reviewer_tests["status"] != "contract_only_not_run"
    ):
        raise SubmissionMaterialError(
            "reviewer tests must remain an unexecuted v1 contract"
        )
    if reviewer_tests["reviewer_context"] != EXPECTED_REVIEW_CONTEXT:
        raise SubmissionMaterialError(
            "reviewer context must be public and self-contained"
        )
    if reviewer_tests["fixture_kit"] != EXPECTED_FIXTURE_KIT:
        raise SubmissionMaterialError("reviewer fixture kit binding drifted")
    if not REVIEWER_FIXTURES_PATH.is_file():
        raise SubmissionMaterialError("reviewer fixture kit is missing")

    positive = reviewer_tests["positive_cases"]
    negative = reviewer_tests["negative_cases"]
    if (
        not isinstance(positive, list)
        or [case.get("id") for case in positive if isinstance(case, dict)]
        != EXPECTED_POSITIVE_IDS
    ):
        raise SubmissionMaterialError(
            "reviewer contract must contain exactly five positive cases"
        )
    if (
        not isinstance(negative, list)
        or [case.get("id") for case in negative if isinstance(case, dict)]
        != EXPECTED_NEGATIVE_IDS
    ):
        raise SubmissionMaterialError(
            "reviewer contract must contain exactly three negative cases"
        )

    positive_keys = {
        "id",
        "title",
        "execution_status",
        "expected_skill_or_workflow",
        "user_prompt",
        "expected_workflow_behavior",
        "expected_result_shape",
        "fixture",
    }
    for case in positive:
        case = _exact_keys(case, positive_keys, "positive reviewer case")
        if case["execution_status"] != "contract_only_not_run":
            raise SubmissionMaterialError("positive reviewer case overstates execution")
        for key in positive_keys - {"fixture"}:
            _non_empty_text(case[key], f"positive reviewer case {key}")
        _validate_fixture(
            case["fixture"], f"positive reviewer case {case['id']} fixture"
        )

    negative_keys = {
        "id",
        "title",
        "execution_status",
        "guard",
        "user_prompt_or_scenario",
        "expected_safe_behavior",
        "why_not_complete",
        "fixture",
    }
    for case in negative:
        case = _exact_keys(case, negative_keys, "negative reviewer case")
        if case["execution_status"] != "contract_only_not_run":
            raise SubmissionMaterialError("negative reviewer case overstates execution")
        for key in negative_keys - {"fixture"}:
            _non_empty_text(case[key], f"negative reviewer case {key}")
        _validate_fixture(
            case["fixture"], f"negative reviewer case {case['id']} fixture"
        )


def validate_submission_materials(
    submission: dict[str, Any] | None = None,
    reviewer_tests: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if submission is None:
        submission = load_json_object(SUBMISSION_PATH, "submission contract")
    if reviewer_tests is None:
        reviewer_tests = load_json_object(REVIEWER_TESTS_PATH, "reviewer test contract")
    package_contract = package.validate_contract()
    _validate_reviewer_tests(reviewer_tests)
    _validate_submission(submission, reviewer_tests, package_contract)
    _validate_public_text(submission, reviewer_tests)
    return {
        "status": submission["status"],
        "positive_cases": len(reviewer_tests["positive_cases"]),
        "negative_cases": len(reviewer_tests["negative_cases"]),
        "starter_prompts": len(submission["starter_prompts"]),
        "unresolved_blockers": sum(
            blocker["status"] == "unresolved" for blocker in submission["blockers"]
        ),
        "package_digest": submission["package"]["path_hash_manifest_sha256"],
    }


def main() -> int:
    try:
        result = validate_submission_materials()
    except (SubmissionMaterialError, package.PluginPackageError) as exc:
        print(f"PLUGIN_SUBMISSION_MATERIALS_FAILED reason={exc}", file=sys.stderr)
        return 1
    print(
        "PLUGIN_SUBMISSION_MATERIALS_OK "
        f"status={result['status']} prompts={result['starter_prompts']} "
        f"positive={result['positive_cases']} negative={result['negative_cases']} "
        f"blockers={result['unresolved_blockers']} "
        f"digest={result['package_digest']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
