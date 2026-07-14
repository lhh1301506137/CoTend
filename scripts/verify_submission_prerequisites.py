from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import verify_plugin_submission_materials as submission  # noqa: E402


PREREQUISITES_PATH = submission.SUBMISSION_PATH.with_name("prerequisites.json")
EXPECTED_DECISION_IDS = [
    "Q01-publisher-mode",
    "Q02-final-plugin-identity",
    "Q03-public-web-presence",
    "Q04-production-logo",
    "Q05-platform-access",
    "Q06-launch-availability",
    "Q07-policy-attestations",
]
EXPECTED_DECISION_DEPENDENCIES = {
    "Q01-publisher-mode": [],
    "Q02-final-plugin-identity": ["Q01-publisher-mode"],
    "Q03-public-web-presence": [
        "Q01-publisher-mode",
        "Q02-final-plugin-identity",
    ],
    "Q04-production-logo": ["Q02-final-plugin-identity"],
    "Q05-platform-access": ["Q01-publisher-mode"],
    "Q06-launch-availability": [
        "Q03-public-web-presence",
        "Q04-production-logo",
        "Q05-platform-access",
    ],
    "Q07-policy-attestations": [
        "Q02-final-plugin-identity",
        "Q03-public-web-presence",
        "Q04-production-logo",
        "Q05-platform-access",
        "Q06-launch-availability",
    ],
}
EXPECTED_DECISION_BLOCKERS = {
    "Q01-publisher-mode": ["verified_publisher_identity"],
    "Q02-final-plugin-identity": ["final_plugin_identity_and_version"],
    "Q03-public-web-presence": [
        "website_url",
        "support_url",
        "privacy_policy_url",
        "terms_url",
    ],
    "Q04-production-logo": ["production_logo"],
    "Q05-platform-access": ["apps_management_write_access"],
    "Q06-launch-availability": ["country_or_region_availability"],
    "Q07-policy-attestations": ["policy_attestations"],
}
EXPECTED_ANSWERED_DECISIONS = {
    "Q01-publisher-mode": {
        "answer": "1",
        "evidence": {
            "evidence_type": "user_explicit",
            "recorded_on": "2026-07-14",
            "scope": "publisher_mode_route_only_not_identity_verification",
        },
    },
    "Q02-final-plugin-identity": {
        "answer": "1",
        "evidence": {
            "evidence_type": "user_explicit",
            "recorded_on": "2026-07-14",
            "scope": (
                "final_plugin_identity_and_version_only_not_submission_or_release"
            ),
        },
    },
    "Q03-public-web-presence": {
        "answer": "1",
        "evidence": {
            "evidence_type": "user_explicit",
            "recorded_on": "2026-07-14",
            "scope": (
                "public_web_presence_hosting_route_only_not_urls_or_publication"
            ),
        },
    },
    "Q04-production-logo": {
        "answer": "1",
        "evidence": {
            "evidence_type": "user_explicit",
            "recorded_on": "2026-07-14",
            "scope": (
                "exact_repository_production_logo_acceptance_not_portal_upload_"
                "or_format_verification"
            ),
        },
    },
    "Q05-platform-access": {
        "answer": "1",
        "evidence": {
            "evidence_type": "user_explicit",
            "recorded_on": "2026-07-14",
            "scope": (
                "platform_access_check_route_only_not_permission_observation_"
                "or_portal_access"
            ),
        },
    },
    "Q06-launch-availability": {
        "answer": "2",
        "evidence": {
            "evidence_type": "user_explicit",
            "recorded_on": "2026-07-15",
            "scope": (
                "global_availability_intent_only_not_exact_country_list_"
                "support_legal_readiness_or_portal_selection"
            ),
        },
    },
}
EXPECTED_RESOLVED_PREREQUISITES = {
    "final_plugin_identity_and_version": submission.EXPECTED_IDENTITY_VALUE,
    "production_logo": submission.EXPECTED_PRODUCTION_LOGO_VALUE,
}
EXPECTED_PREREQUISITE_DECISIONS = {
    blocker_id: decision_id
    for decision_id, blocker_ids in EXPECTED_DECISION_BLOCKERS.items()
    for blocker_id in blocker_ids
}
EXPECTED_PREREQUISITE_DEPENDENCIES = {
    "final_plugin_identity_and_version": [],
    "verified_publisher_identity": [],
    "apps_management_write_access": ["verified_publisher_identity"],
    "production_logo": ["final_plugin_identity_and_version"],
    "website_url": [
        "final_plugin_identity_and_version",
        "verified_publisher_identity",
    ],
    "support_url": [
        "final_plugin_identity_and_version",
        "verified_publisher_identity",
    ],
    "privacy_policy_url": [
        "final_plugin_identity_and_version",
        "verified_publisher_identity",
    ],
    "terms_url": [
        "final_plugin_identity_and_version",
        "verified_publisher_identity",
    ],
    "country_or_region_availability": [
        "apps_management_write_access",
        "production_logo",
        "website_url",
        "support_url",
        "privacy_policy_url",
        "terms_url",
    ],
    "policy_attestations": submission.EXPECTED_BLOCKER_IDS[:-1],
}
EXPECTED_CAPABILITIES = {
    "final_plugin_identity_and_version": (True, False, False, "repository"),
    "verified_publisher_identity": (False, True, True, "openai_platform"),
    "apps_management_write_access": (False, True, True, "openai_platform"),
    "production_logo": (True, False, False, "repository"),
    "website_url": (True, True, False, "public_web"),
    "support_url": (True, True, False, "public_web"),
    "privacy_policy_url": (True, True, False, "public_web"),
    "terms_url": (True, True, False, "public_web"),
    "country_or_region_availability": (
        True,
        False,
        False,
        "repository_decision",
    ),
    "policy_attestations": (False, True, True, "openai_platform"),
}
EXPECTED_AUTHORITY = {
    "repository_preparation_only": True,
    "publisher_mode_selected": True,
    "final_identity_selected": True,
    "production_logo_selected": True,
    "verified_identity_observed": False,
    "apps_management_write_access_observed": False,
    "public_urls_selected": False,
    "regions_selected": False,
    "policy_attestations_completed": False,
    "portal_opened": False,
    "portal_draft_created": False,
    "submitted_for_review": False,
    "approved": False,
    "published": False,
}


class SubmissionPrerequisiteError(ValueError):
    pass


def load_json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SubmissionPrerequisiteError(f"{label} is not readable JSON") from exc
    if not isinstance(payload, dict):
        raise SubmissionPrerequisiteError(f"{label} must be a JSON object")
    return payload


def _exact_keys(value: Any, expected: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != expected:
        raise SubmissionPrerequisiteError(f"{label} fields drifted")
    return value


def _non_empty_chinese(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SubmissionPrerequisiteError(f"{label} must be non-empty text")
    if not re.search(r"[\u3400-\u9fff]", value):
        raise SubmissionPrerequisiteError(f"{label} must remain user-readable Chinese")
    return value


def _expected_package(contract: dict[str, Any]) -> dict[str, Any]:
    package = contract["package"]
    return {
        "plugin_id": package["plugin_id"],
        "version": package["version"],
        "file_count": package["file_count"],
        "path_hash_manifest_sha256": package["path_hash_manifest_sha256"],
        "source_skill_manifest_sha256": package["source_skill_manifest_sha256"],
        "identity_authority": "initial_submission_identity_confirmed_not_release",
    }


def _validate_decisions(decisions: Any) -> None:
    if (
        not isinstance(decisions, list)
        or [item.get("id") for item in decisions if isinstance(item, dict)]
        != EXPECTED_DECISION_IDS
    ):
        raise SubmissionPrerequisiteError("decision inventory or order drifted")

    decision_keys = {
        "id",
        "sequence",
        "status",
        "decision_authority",
        "depends_on",
        "blocker_ids",
        "question_zh",
        "why_it_matters_zh",
        "recommended_option_id",
        "options",
        "answer",
        "evidence",
    }
    option_keys = {"id", "label_zh", "impact_zh"}
    seen: set[str] = set()
    awaiting: list[str] = []
    covered_blockers: list[str] = []
    for expected_sequence, decision in enumerate(decisions, start=1):
        decision = _exact_keys(decision, decision_keys, "decision")
        decision_id = decision["id"]
        if decision["sequence"] != expected_sequence:
            raise SubmissionPrerequisiteError("decision sequence drifted")
        if decision["decision_authority"] != "publisher":
            raise SubmissionPrerequisiteError("decision authority drifted")
        if decision["depends_on"] != EXPECTED_DECISION_DEPENDENCIES[decision_id]:
            raise SubmissionPrerequisiteError("decision dependency graph drifted")
        if any(dependency not in seen for dependency in decision["depends_on"]):
            raise SubmissionPrerequisiteError(
                "decision dependency graph is not acyclic"
            )
        if decision["blocker_ids"] != EXPECTED_DECISION_BLOCKERS[decision_id]:
            raise SubmissionPrerequisiteError("decision-to-blocker mapping drifted")
        covered_blockers.extend(decision["blocker_ids"])
        if decision_id in EXPECTED_ANSWERED_DECISIONS:
            expected_status = "answered"
        else:
            expected_status = "blocked_by_dependencies"
        if decision["status"] != expected_status:
            raise SubmissionPrerequisiteError("one-at-a-time decision state drifted")
        if decision["status"] == "awaiting_user_decision":
            awaiting.append(decision_id)
        expected_answer = EXPECTED_ANSWERED_DECISIONS.get(decision_id)
        if expected_answer is None:
            if decision["answer"] is not None or decision["evidence"] is not None:
                raise SubmissionPrerequisiteError(
                    "owner decision was filled without evidence"
                )
        elif {
            "answer": decision["answer"],
            "evidence": decision["evidence"],
        } != expected_answer:
            raise SubmissionPrerequisiteError(
                "recorded owner decision or evidence drifted"
            )
        _non_empty_chinese(decision["question_zh"], "decision question")
        _non_empty_chinese(decision["why_it_matters_zh"], "decision rationale")
        if decision["recommended_option_id"] != "1":
            raise SubmissionPrerequisiteError("recommended option must remain option 1")
        options = decision["options"]
        if not isinstance(options, list) or [
            option.get("id") for option in options if isinstance(option, dict)
        ] != ["1", "2", "3"]:
            raise SubmissionPrerequisiteError("decision options drifted")
        for option in options:
            option = _exact_keys(option, option_keys, "decision option")
            _non_empty_chinese(option["label_zh"], "decision option label")
            _non_empty_chinese(option["impact_zh"], "decision option impact")
        seen.add(decision_id)

    if awaiting:
        raise SubmissionPrerequisiteError(
            "no decision may be active until prerequisites are resolved"
        )
    if sorted(covered_blockers) != sorted(submission.EXPECTED_BLOCKER_IDS):
        raise SubmissionPrerequisiteError(
            "decisions do not cover every blocker exactly once"
        )


def _validate_prerequisites(
    prerequisites: Any, submission_contract: dict[str, Any]
) -> None:
    canonical_ids = [blocker["id"] for blocker in submission_contract["blockers"]]
    if (
        not isinstance(prerequisites, list)
        or [item.get("id") for item in prerequisites if isinstance(item, dict)]
        != canonical_ids
    ):
        raise SubmissionPrerequisiteError(
            "prerequisites do not exactly match the submission blocker inventory"
        )

    prerequisite_keys = {
        "id",
        "sequence",
        "phase",
        "status",
        "value",
        "decision_authority",
        "execution_owner",
        "decision_id",
        "depends_on",
        "repository_can_prepare",
        "external_action_required",
        "openai_platform_required",
        "completion_location",
        "completion_evidence_zh",
        "boundary_zh",
    }
    known = set(canonical_ids)
    submission_by_id = {
        blocker["id"]: blocker for blocker in submission_contract["blockers"]
    }
    for expected_sequence, prerequisite in enumerate(prerequisites, start=1):
        prerequisite = _exact_keys(
            prerequisite, prerequisite_keys, "submission prerequisite"
        )
        prerequisite_id = prerequisite["id"]
        if prerequisite["sequence"] != expected_sequence:
            raise SubmissionPrerequisiteError("prerequisite sequence drifted")
        expected_value = EXPECTED_RESOLVED_PREREQUISITES.get(prerequisite_id)
        if expected_value is None:
            if (
                prerequisite["status"] != "unresolved"
                or prerequisite["value"] is not None
            ):
                raise SubmissionPrerequisiteError(
                    "prerequisite was resolved without owner or Platform evidence"
                )
        elif (
            prerequisite["status"] != "resolved"
            or prerequisite["value"] != expected_value
        ):
            raise SubmissionPrerequisiteError(
                "confirmed repository prerequisite evidence drifted"
            )
        if {
            "status": prerequisite["status"],
            "value": prerequisite["value"],
        } != {
            "status": submission_by_id[prerequisite_id]["status"],
            "value": submission_by_id[prerequisite_id]["value"],
        }:
            raise SubmissionPrerequisiteError(
                "prerequisite and submission blocker state drifted"
            )
        if prerequisite["decision_authority"] != "publisher":
            raise SubmissionPrerequisiteError("prerequisite authority drifted")
        if not isinstance(prerequisite["execution_owner"], str):
            raise SubmissionPrerequisiteError("prerequisite execution owner drifted")
        if (
            prerequisite["decision_id"]
            != EXPECTED_PREREQUISITE_DECISIONS[prerequisite_id]
        ):
            raise SubmissionPrerequisiteError("prerequisite decision mapping drifted")
        if prerequisite["depends_on"] != EXPECTED_PREREQUISITE_DEPENDENCIES[
            prerequisite_id
        ] or any(dependency not in known for dependency in prerequisite["depends_on"]):
            raise SubmissionPrerequisiteError("prerequisite dependency graph drifted")
        capabilities = (
            prerequisite["repository_can_prepare"],
            prerequisite["external_action_required"],
            prerequisite["openai_platform_required"],
            prerequisite["completion_location"],
        )
        if capabilities != EXPECTED_CAPABILITIES[prerequisite_id]:
            raise SubmissionPrerequisiteError(
                "repository, external, or Portal responsibility drifted"
            )
        evidence = prerequisite["completion_evidence_zh"]
        if not isinstance(evidence, list) or len(evidence) < 2:
            raise SubmissionPrerequisiteError("completion evidence is incomplete")
        for statement in evidence:
            _non_empty_chinese(statement, "completion evidence")
        _non_empty_chinese(prerequisite["boundary_zh"], "prerequisite boundary")

    policy = prerequisites[-1]
    if (
        policy["id"] != "policy_attestations"
        or policy["depends_on"] != canonical_ids[:-1]
    ):
        raise SubmissionPrerequisiteError(
            "policy attestations must remain the final gate"
        )


def validate_submission_prerequisites(
    packet: dict[str, Any] | None = None,
    submission_contract: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if packet is None:
        packet = load_json_object(PREREQUISITES_PATH, "prerequisite packet")
    if submission_contract is None:
        submission_contract = submission.load_json_object(
            submission.SUBMISSION_PATH, "submission contract"
        )
    reviewer_tests = submission.load_json_object(
        submission.REVIEWER_TESTS_PATH, "reviewer test contract"
    )
    submission.validate_submission_materials(submission_contract, reviewer_tests)

    _exact_keys(
        packet,
        {
            "schema",
            "schema_version",
            "status",
            "official_requirements",
            "submission_contract",
            "package",
            "decision_policy",
            "authority",
            "decisions",
            "prerequisites",
            "next_action",
        },
        "prerequisite packet",
    )
    if packet["schema"] != "cotend.codex-plugin-submission-prerequisites":
        raise SubmissionPrerequisiteError("prerequisite schema drifted")
    if (
        packet["schema_version"] != 1
        or packet["status"] != "prerequisite_resolution_required"
    ):
        raise SubmissionPrerequisiteError(
            "prerequisite packet must remain prerequisite-resolution v1"
        )
    if packet["official_requirements"] != {
        "source": submission.OFFICIAL_SUBMISSION_URL,
        "checked_on": "2026-07-15",
        "scope": "pre_submission_decisions_and_external_evidence",
    }:
        raise SubmissionPrerequisiteError("official requirement anchor drifted")
    if packet["submission_contract"] != {
        "path": submission.SUBMISSION_PATH.relative_to(ROOT).as_posix(),
        "status": submission_contract["status"],
        "readiness": submission_contract["readiness"]["status"],
    }:
        raise SubmissionPrerequisiteError("submission contract binding drifted")
    if packet["package"] != _expected_package(submission_contract):
        raise SubmissionPrerequisiteError("package binding drifted")
    if packet["decision_policy"] != {
        "mode": "one_at_a_time",
        "current_decision_id": None,
        "current_decision_status": "blocked_until_prerequisites_resolved",
        "ordinary_continue_answers_decision": False,
        "auto_fill_owner_facts": False,
        "advance_only_after_explicit_answer": True,
    }:
        raise SubmissionPrerequisiteError("decision policy drifted")
    if packet["authority"] != EXPECTED_AUTHORITY:
        raise SubmissionPrerequisiteError("repository or external authority drifted")

    _validate_decisions(packet["decisions"])
    _validate_prerequisites(packet["prerequisites"], submission_contract)
    if packet["next_action"] != {
        "action": "resolve_prerequisites_before_q07",
        "decision_id": "Q07-policy-attestations",
        "expected_answer": None,
        "external_action_permitted": False,
        "ordinary_continue_answers_decision": False,
    }:
        raise SubmissionPrerequisiteError(
            "next action must remain the prerequisite-resolution gate"
        )

    return {
        "status": packet["status"],
        "prerequisites": len(packet["prerequisites"]),
        "decisions": len(packet["decisions"]),
        "active_decision": packet["decision_policy"]["current_decision_id"]
        or "none",
        "blocked_decision": "Q07-policy-attestations",
        "package_digest": packet["package"]["path_hash_manifest_sha256"],
    }


def main() -> int:
    try:
        result = validate_submission_prerequisites()
    except (
        SubmissionPrerequisiteError,
        submission.SubmissionMaterialError,
        submission.package.PluginPackageError,
    ) as exc:
        print(f"SUBMISSION_PREREQUISITES_FAILED reason={exc}", file=sys.stderr)
        return 1
    print(
        "SUBMISSION_PREREQUISITES_OK "
        f"status={result['status']} prerequisites={result['prerequisites']} "
        f"decisions={result['decisions']} active={result['active_decision']} "
        f"blocked={result['blocked_decision']} "
        f"digest={result['package_digest']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
