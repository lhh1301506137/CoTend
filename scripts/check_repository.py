from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_CAPABILITIES = {f"C{number:02d}" for number in range(1, 20)}
EXPECTED_JOURNEYS = [f"J{number}" for number in range(1, 7)]
EXPECTED_NOVICE_STATUSES = {
    "draft_for_review",
    "reviewed_pending_user_confirmation",
    "active_user_confirmed",
}
EXPECTED_INTERFACE_DESIGN_STATUSES = {
    "unconfirmed",
    "baseline_user_confirmed",
}
EXPECTED_JOURNEY_RESULTS = [
    "success",
    "blocked",
    "failure",
    "deferred",
    "interrupted",
    "recovery_required",
]
EXPECTED_NOVICE_FIXTURES = {
    "F01": ("start", "question_or_confirmation", "yes", "framework"),
    "F02": ("start", "question_or_confirmation", "yes", "framework"),
    "F03": ("start", "question_or_confirmation", "yes", "framework"),
    "F04": ("start", "readiness_report", "no", "framework"),
    "F05": ("continue", "work_checkpoint", "no", "framework"),
    "F06": ("continue", "blocked_decision", "yes", "framework"),
    "F07": ("continue", "work_checkpoint", "yes", "framework"),
    "F08": ("continue", "failure_containment", "no", "framework"),
    "F09": ("change", "change_disposition", "yes", "framework"),
    "F10": ("change", "change_disposition", "no", "framework"),
    "F11": ("change", "interruption_checkpoint", "yes", "framework"),
    "F12": ("change", "change_disposition", "no", "framework"),
    "F13": ("recover", "recovery_report", "no", "framework"),
    "F14": ("recover", "recovery_report", "yes", "framework"),
    "F15": ("recover", "handoff_readiness", "no", "framework"),
    "F16": ("recover", "recovery_report", "no", "framework"),
    "F17": ("evaluate", "acceptance_walkthrough", "yes", "framework"),
    "F18": ("evaluate", "done_gate", "yes", "framework"),
    "F19": ("evaluate", "blocked_decision", "yes", "framework"),
    "F20": ("advanced", "diagnosis_report", "yes", "framework"),
    "F21": ("advanced", "model_options", "yes", "framework"),
    "F22": ("advanced", "learning_proposal", "yes", "framework"),
    "F23": ("advanced", "release_readiness", "yes", "framework"),
    "F24": ("advanced", "delivery_preflight", "yes", "framework"),
}
EXPECTED_NOVICE_PROMPT_SHA256 = "6852cad0c78a44e33b7f784e107165e6a59cb7f4afd04a52732d4efc4a3ba0f7"
EXPECTED_INTERFACE_GATES = [f"H{number}" for number in range(1, 9)]
EXPECTED_INTERFACE_CANDIDATES = [f"I{number}" for number in range(1, 7)]
EXPECTED_CONFIRMED_INTERFACE_CATALOG_SHA256 = (
    "0136eba98238743d9780f428a7acff03a26a8e211ebfb795ee0c68f754a20091"
)
EXPECTED_INTERFACE_DESTINATIONS = {
    "start": ("core", ("first", "confirmed", "route")),
    "continue": ("core", ("already current", "failure", "bounded", "verified")),
    "change": ("core", ("user correction", "new idea", "priority", "stop")),
    "recover": ("core", ("resume", "project truth", "hand")),
    "evaluate": ("core", ("test", "user's decision", "without implying acceptance")),
    "advanced:diagnosis": ("contextual", ("without editing", "repair", "user-authorized")),
    "advanced:model_roles": ("contextual", ("advice", "takeovers", "rollback", "cost", "data")),
    "advanced:framework_learning": (
        "contextual",
        ("repeated failures", "reversible", "improvement proposal"),
    ),
    "advanced:release": (
        "contextual",
        ("before", "push", "without performing the external action"),
    ),
    "advanced:platform_delivery": (
        "contextual",
        ("install", "update", "permissions", "state retention", "rollback"),
    ),
}
EXPECTED_INTERFACE_FIXTURE_DESTINATIONS = {
    **{f"F{number:02d}": "start" for number in range(1, 5)},
    **{f"F{number:02d}": "continue" for number in range(5, 9)},
    **{f"F{number:02d}": "change" for number in range(9, 13)},
    **{f"F{number:02d}": "recover" for number in range(13, 17)},
    **{f"F{number:02d}": "evaluate" for number in range(17, 20)},
    "F20": "advanced:diagnosis",
    "F21": "advanced:model_roles",
    "F22": "advanced:framework_learning",
    "F23": "advanced:release",
    "F24": "advanced:platform_delivery",
}
EXPECTED_PLATFORM_CLAIMS = [f"P{number:02d}" for number in range(1, 10)]
EXPECTED_REFERENCE_SOURCES = {
    "RF01": (
        "https://github.com/obra/superpowers",
        "d884ae04edebef577e82ff7c4e143debd0bbec99",
        "MIT",
    ),
    "RF02": (
        "https://github.com/mindfold-ai/trellis",
        "bde902cad75813c73f1413bf8da581168a835b37",
        "AGPL-3.0",
    ),
    "RF03": (
        "https://github.com/github/spec-kit",
        "1be42992e64b08ff0dce3d7a914eaabf04284ffb",
        "MIT",
    ),
    "RF04": (
        "https://github.com/Fission-AI/OpenSpec",
        "0a99f410457271aa773d8b106f03f637f7c6b3c0",
        "MIT",
    ),
    "RF05": (
        "https://github.com/open-gsd/gsd-core",
        "e3a8c063b8f6059aa4c0214302aec51615a4f831",
        "MIT",
    ),
    "RF06": (
        "https://github.com/bmad-code-org/BMAD-METHOD",
        "49069b8b5276afd21402bc3b978b69ad78a7d2ef",
        "MIT",
    ),
}
EXPECTED_CODEX_CARRIER_FIXTURE_FILES = {
    "AGENTS.md",
    "README.md",
    "live-scenarios.json",
    "scenarios/diagnose/calculator.py",
    "scenarios/fresh/README.md",
    "scenarios/pending-decision/STATUS.md",
    "schemas/diagnose-only.schema.json",
    "schemas/init-delegation.schema.json",
    "schemas/pending-decision.schema.json",
}
EXPECTED_PLUGIN_FIXTURE_FILES = {
    "docs/evidence/ISOLATED-CODEX-PLUGIN-FIXTURE.md",
    "scripts/verify_isolated_codex_plugin.py",
    "tests/test_isolated_codex_plugin.py",
}
EXPECTED_PLUGIN_FIXTURE_TESTS = {
    "test_fixture_guard_rejects_private_root_and_escape",
    "test_fixture_manifest_is_skills_only_and_non_release",
    "test_isolated_environment_redirects_every_write_root",
    "test_plugin_list_contract_requires_exact_install_state",
    "test_stat_only_snapshot_never_contains_content_digest",
    "test_static_fixture_and_twelve_negative_mutations",
}
EXPECTED_PLUGIN_NAMESPACE_FILES = {
    "docs/CODEX-PLUGIN-NAMESPACE-EVALUATION.md",
    "docs/evidence/CODEX-DESKTOP-PLUGIN-SURFACE.md",
    "docs/evidence/CODEX-PLUGIN-NAMESPACE-CANDIDATES.md",
    "scripts/evaluate_plugin_namespace_candidates.py",
    "tests/test_plugin_namespace_candidates.py",
}
EXPECTED_PLUGIN_NAMESPACE_TESTS = {
    "test_candidate_state_and_write_roots_are_independent",
    "test_display_led_overlay_reuses_n1_bytes_and_marks_limits",
    "test_identifier_categories_distinguish_reference_shapes",
    "test_protected_boundary_excludes_only_codex_container_metadata",
    "test_remove_payloads_require_exact_candidate_identity",
    "test_short_name_map_preserves_companion_names",
    "test_source_identifier_inventory_is_exact",
    "test_static_candidates_quantify_transform_and_residual_debt",
}
EXPECTED_PLUGIN_PACKAGE_FILES = {
    "docs/evidence/ISOLATED-CODEX-PLUGIN-PRODUCTION-PACKAGE.md",
    "packaging/codex-plugin/cotend/.codex-plugin/plugin.json",
    "packaging/codex-plugin/cotend/assets/cotend-mark.svg",
    "packaging/codex-plugin/cotend/assets/cotend-mark-dark.svg",
    "packaging/codex-plugin/cotend/assets/cotend-logo.png",
    "packaging/codex-plugin/cotend/assets/cotend-logo-dark.png",
    "packaging/codex-plugin/package.lock.json",
    "scripts/build_codex_plugin.py",
    "scripts/verify_codex_plugin_package.py",
    "tests/test_codex_plugin_package.py",
}
EXPECTED_PLUGIN_PACKAGE_TESTS = {
    "test_existing_invalid_output_is_not_overwritten",
    "test_linklike_package_member_is_rejected",
    "test_manifest_and_lock_define_skills_candidate_with_brand_assets",
    "test_n3_display_metadata_and_prompt_limits_are_preserved",
    "test_output_must_stay_in_repository_build_roots",
    "test_package_drift_is_rejected",
    "test_two_builds_are_byte_deterministic",
    "test_valid_existing_output_rebuild_is_idempotent",
}
EXPECTED_PLUGIN_LIFECYCLE_FILES = {
    "docs/evidence/ISOLATED-CODEX-PLUGIN-PRODUCTION-LIFECYCLE.md",
    "scripts/verify_production_plugin_lifecycle.py",
    "tests/test_production_plugin_lifecycle.py",
}
EXPECTED_PLUGIN_LIFECYCLE_TESTS = {
    "test_fail_after_plugin_add_is_deterministic",
    "test_l46_root_guard_rejects_other_private_directory",
    "test_marketplace_is_local_only_and_not_part_of_package",
    "test_materialized_package_matches_l44_digest",
    "test_parameterized_payload_rejects_fixture_identity",
    "test_production_identity_is_separate_from_fixture_default",
    "test_purge_removes_only_isolated_runtime_roots",
}
EXPECTED_GITHUB_MARKETPLACE_CARRIER_FILES = {
    ".agents/plugins/marketplace.json",
    ".codex-plugin/plugin.json",
    "docs/evidence/GITHUB-MARKETPLACE-ROOT-CARRIER.md",
    "scripts/verify_github_marketplace_carrier.py",
    "tests/test_github_marketplace_carrier.py",
}
EXPECTED_GITHUB_MARKETPLACE_CARRIER_TESTS = {
    "test_boundary_change_summary_never_includes_metadata_values",
    "test_carrier_manifest_is_exact_path_only_transform",
    "test_cleanup_removes_readonly_git_objects_inside_fixture",
    "test_external_project_cleanup_retries_windows_handle_release",
    "test_external_project_root_is_exact_temp_child_and_removable",
    "test_git_environment_is_isolated_and_forces_lf",
    "test_l54_root_guard_rejects_other_private_directory",
    "test_marketplace_uses_repository_root_url_source",
    "test_materialized_carrier_has_one_skill_source_and_locked_assets",
    "test_repeat_add_and_local_refresh_require_known_outcomes",
    "test_repository_carrier_requires_both_root_files",
    "test_root_source_validation_rejects_nested_package_source",
}
EXPECTED_PLUGIN_SUBMISSION_FILES = {
    "docs/evidence/CODEX-PLUGIN-SUBMISSION-MATERIAL-CONTRACT.md",
    "packaging/codex-plugin/submission-materials/submission.json",
    "packaging/codex-plugin/submission-materials/reviewer-tests.json",
    "scripts/verify_plugin_submission_materials.py",
    "tests/test_plugin_submission_materials.py",
}
EXPECTED_PLUGIN_SUBMISSION_TESTS = {
    "test_valid_contract_binds_exact_production_candidate",
    "test_listing_and_starter_prompts_match_plugin_manifest",
    "test_reviewer_contract_has_exact_five_positive_three_negative",
    "test_reviewer_fixtures_are_public_and_self_contained",
    "test_external_requirements_remain_real_blockers",
    "test_release_notes_are_initial_draft_not_submission_claim",
    "test_seventeen_negative_mutations_are_rejected",
}
EXPECTED_SUBMISSION_PREREQUISITE_FILES = {
    "docs/evidence/SUBMISSION-PREREQUISITE-DECISION-PACKET.md",
    "packaging/codex-plugin/submission-materials/prerequisites.json",
    "scripts/verify_submission_prerequisites.py",
    "tests/test_submission_prerequisites.py",
}
EXPECTED_SUBMISSION_PREREQUISITE_TESTS = {
    "test_valid_packet_binds_exact_candidate_and_submission_contract",
    "test_prerequisites_exactly_map_ten_canonical_blockers",
    "test_decision_graph_is_acyclic_and_one_at_a_time",
    "test_policy_attestations_are_the_final_gate",
    "test_repository_and_external_responsibilities_are_explicit",
    "test_confirmed_routes_do_not_set_external_authority",
    "test_q01_explains_publisher_mode_tradeoff_in_chinese",
    "test_eighteen_negative_mutations_are_rejected",
}
EXPECTED_PUBLIC_README_FILES = {
    "README.md",
    "docs/evidence/PUBLIC-REPOSITORY-ONBOARDING.md",
    "tests/test_public_readme.py",
}
EXPECTED_PUBLIC_README_TESTS = {
    "test_readme_is_english_and_novice_first",
    "test_readme_declares_pre_release_and_no_public_install",
    "test_readme_skill_catalog_matches_seven_packaged_skills",
    "test_readme_starter_prompts_match_submission_contract",
    "test_readme_relative_links_resolve",
    "test_readme_maintainer_commands_are_safe_and_real",
}
EXPECTED_DELIVERY_PRODUCT_FILES = {
    "delivery/codex-artifact.lock.json",
    "scripts/cotend_delivery.py",
    "scripts/cotend_user_delivery.py",
    "scripts/verify_delivery_lifecycle.py",
    "scripts/verify_production_user_resolver.py",
    "scripts/verify_production_user_receipt.py",
    "scripts/verify_user_skill_delivery.py",
    "src/cotend_delivery/__init__.py",
    "src/cotend_delivery/__main__.py",
    "src/cotend_delivery/cli.py",
    "src/cotend_delivery/core.py",
    "src/cotend_delivery/production_cli.py",
    "src/cotend_delivery/production_resolver.py",
    "src/cotend_delivery/production_scope.py",
    "src/cotend_delivery/user_scope.py",
    "tests/test_cotend_delivery.py",
    "tests/test_production_user_resolver.py",
    "tests/test_production_user_receipt.py",
    "tests/test_user_skill_delivery.py",
    "docs/evidence/ISOLATED-USER-SKILL-DELIVERY.md",
    "docs/evidence/PRODUCTION-USER-LAYOUT-RESOLVER.md",
    "docs/evidence/ISOLATED-PRODUCTION-USER-RECEIPT.md",
}
EXPECTED_DELIVERY_OPERATIONS = {
    "inspect",
    "install",
    "update",
    "repair",
    "migrate_identity",
    "enable",
    "disable",
    "uninstall",
    "rollback",
    "recover",
}
EXPECTED_DELIVERY_TESTS = {
    "test_artifact_identity_dry_run_and_idempotent_install",
    "test_cli_defaults_to_dry_run",
    "test_commit_cleanup_failure_restores_prior_state",
    "test_candidate_free_operations_ignore_missing_repository",
    "test_corrupt_checkpoint_is_rejected_before_mutation",
    "test_damaged_mapped_legacy_receipt_repairs_and_migrates",
    "test_disable_enable_preserves_unrelated_project_content",
    "test_disabled_lifecycle_preserves_enablement",
    "test_failed_update_restores_prior_state_and_prior_rollback",
    "test_invalid_disabled_carrier_boundary_is_rejected",
    "test_invalid_receipt_blocks_mutation_but_allows_rollback",
    "test_legacy_identity_migration_is_receipt_only_and_reversible",
    "test_legacy_checkpoint_rejects_schema_v2_operation",
    "test_legacy_receipt_rejects_schema_v2_identity_fields",
    "test_legacy_snapshot_checkpoint_remains_readable",
    "test_lower_revision_is_not_mislabeled_as_update",
    "test_preserved_migration_checkpoint_rejects_payload_drift",
    "test_protocol_change_is_incompatible_even_at_higher_revision",
    "test_restored_rollback_phase_failure_retains_lock_without_false_double_failure",
    "test_inspect_reports_current_state_when_repository_is_missing",
    "test_repair_failure_restores_exact_damaged_state",
    "test_repair_rollback_restores_exact_damaged_state",
    "test_repair_restores_modified_and_missing_owned_files",
    "test_same_artifact_id_with_different_bytes_is_blocked",
    "test_schema_v2_checkpoint_requires_explicit_payload_mode",
    "test_shadow_payload_blocks_mutation",
    "test_unexpected_file_blocks_repair_and_uninstall",
    "test_uninstall_removes_only_owned_files_and_can_rollback",
    "test_unmapped_legacy_identity_cannot_migrate_or_repair",
    "test_unowned_collision_blocks_install",
    "test_unowned_delivery_state_blocks_install",
    "test_update_and_one_step_rollback",
    "test_active_mutation_lock_blocks_competing_write_without_changes",
    "test_invalid_mutation_lock_metadata_blocks_without_cleanup",
    "test_locked_replan_failure_releases_unmutated_lock",
    "test_locked_replan_observes_state_changed_before_acquire",
    "test_mutation_lock_owner_mismatch_prevents_release",
    "test_stale_interrupted_lock_is_reported_and_never_auto_removed",
    "test_transition_and_rollback_failure_retains_recovery_lock",
    "test_recovery_preview_requires_exact_confirmation_before_any_write",
    "test_recovery_never_overrides_active_or_unknown_owner",
    "test_recovery_rolls_back_interrupted_update_and_reinstates_prior_checkpoint",
    "test_stale_recovery_plan_is_rejected_without_recovery_lock_write",
    "test_recovery_blocks_corrupt_checkpoint_and_unexpected_managed_content",
    "test_recovery_verification_failure_retains_checkpoint_and_both_locks",
    "test_active_recovery_lock_blocks_second_recovery_and_normal_mutation",
}
EXPECTED_USER_DELIVERY_TESTS = {
    "test_absent_companions_are_owned_through_full_lifecycle",
    "test_compatible_existing_companions_are_external_and_preserved",
    "test_mixed_owned_and_external_companions_are_recorded_per_component",
    "test_portable_bom_and_crlf_companion_is_compatible",
    "test_compatible_duplicate_warns_without_creating_third_copy",
    "test_incompatible_companion_blocks_before_any_write",
    "test_extra_companion_file_blocks_before_any_write",
    "test_first_party_collision_in_compatibility_root_blocks",
    "test_external_shared_disappearance_blocks_mutation_without_takeover",
    "test_external_shared_candidate_version_drift_blocks_update",
    "test_failed_repair_rolls_back_owned_payload_and_preserves_external",
    "test_mutation_lock_blocks_second_user_scope_writer",
    "test_recovery_restores_interrupted_user_update_without_touching_external",
    "test_recovery_blocks_external_drift_before_owned_payload_write",
    "test_user_receipt_ownership_tamper_is_rejected",
    "test_layout_rejects_escape_and_live_home",
    "test_layout_rejects_linked_user_root",
    "test_layout_rejects_state_and_skill_root_overlap",
    "test_linked_companion_is_rejected_when_platform_allows_link_creation",
}
EXPECTED_PRODUCTION_RESOLVER_TESTS = {
    "test_resolves_official_roots_and_home_owned_state",
    "test_same_home_multiple_codex_home_shares_installation_identity",
    "test_identity_does_not_expose_user_or_absolute_path",
    "test_environment_codex_home_is_used_when_not_injected",
    "test_relative_empty_and_overlapping_roots_are_rejected",
    "test_linked_codex_home_is_rejected",
    "test_resolve_and_absent_inspection_are_zero_write",
    "test_cli_dry_run_is_structured_and_zero_write",
    "test_cli_apply_rejects_before_path_resolution_and_zero_write",
    "test_schema_v3_receipt_requires_explicit_migration",
    "test_unknown_state_blocks_without_cleanup",
    "test_first_party_compatibility_residue_requires_migration",
    "test_unowned_canonical_residue_requires_migration",
}
EXPECTED_PRODUCTION_RECEIPT_TESTS = {
    "test_fresh_install_writes_schema_v4_bound_to_resolved_identity",
    "test_schema_v4_full_lifecycle_preserves_external_companions",
    "test_schema_v3_migration_is_previewable_receipt_only_and_reversible",
    "test_schema_v3_ownership_tamper_is_rejected_before_migration",
    "test_schema_v3_payload_drift_blocks_migration_and_combined_repair",
    "test_schema_v3_external_shared_drift_blocks_migration_without_takeover",
    "test_schema_v3_hybrid_production_identity_fields_are_rejected",
    "test_schema_v4_installation_identity_tamper_is_rejected",
    "test_layout_context_rebind_is_receipt_only_and_reversible",
    "test_layout_context_change_blocks_artifact_update_until_rebound",
    "test_production_bridge_is_hard_disabled_and_never_creates_state",
    "test_isolated_production_manager_rejects_escape_and_simulated_live_home",
    "test_resolver_recognizes_current_changed_and_foreign_v4_envelopes",
}

# checker-self-scan-allowlist-start
LOCAL_ONLY_PATHS = {
    "STATUS.md",
    "PROJECT-PLAN-NODES",
    "REVIEW-LOG.md",
    "docs/COMMAND-CONTRACTS.md",
    "QUALITY-SIGNALS.md",
    "PROJECT-UNDERSTANDING",
    "PROJECT-DECISION-LOG.md",
    "docs/V1-ARCHITECTURE.md",
    "PROJECT-KNOWLEDGE-CHANGELOG.md",
    "docs/PROJECT-STATE-CONTRACT.md",
    "PROJECT-PLAN-TREE.md",
}
FORBIDDEN_PUBLIC_PATTERNS = {
    "private upstream identifier": re.compile(r"\bstartskills\b", re.IGNORECASE),
    "internal AI protocol": re.compile(r"dual-ai-collaboration-v", re.IGNORECASE),
    "local decision ID": re.compile(r"DEC-\d{8}-\d+"),
    "local decision log reference": re.compile(r"PROJECT-DECISION-LOG\.md", re.IGNORECASE),
    "internal authority label": re.compile(r"\bprimary_ai_(?:auto|observed|proposed)\w*", re.IGNORECASE),
    "absolute Windows path": re.compile(r"\b[A-Z]:[\\/]", re.IGNORECASE),
}
FRAMEWORK_SOURCE_ALLOWED_PATTERN_LABELS = {
    "local decision log reference",
    "internal authority label",
}
FORBIDDEN_SKILL_MAINTAINER_PATTERNS = {
    "personal maintainer profile": re.compile(r"\bthis user's\b", re.IGNORECASE),
    "machine-specific instruction": re.compile(
        r"\bon this machine\b|codegraph-mcp\.ps1", re.IGNORECASE
    ),
    "private short decision ID": re.compile(r"\bDEC-\d{3}\b"),
    "private legacy sync version": re.compile(r"\bv1\.50\b", re.IGNORECASE),
    "private adapter sync layout": re.compile(
        r"skills-backup|SKILLS-INDEX|command-backups", re.IGNORECASE
    ),
    "forced maintainer language": re.compile(
        r"report in Chinese|written in Chinese|must be Chinese|^\s*language:\s*zh-CN\s*$",
        re.IGNORECASE | re.MULTILINE,
    ),
}
FORBIDDEN_UNCONFIRMED_PRD_PATTERNS = {
    "fixed project-state path": re.compile(r"\.cotend[\\/]", re.IGNORECASE),
    "fixed invocation namespace": re.compile(r"\$cotend:|(?<![\w/])\/cot\b", re.IGNORECASE),
    "fixed plugin and skill bundle": re.compile(
        r"\bPlugin\b.{0,80}\b(?:6|six)\b.{0,40}\bSkills?\b|"
        r"\b(?:6|six)\b.{0,40}\bSkills?\b.{0,80}\bPlugin\b",
        re.IGNORECASE | re.DOTALL,
    ),
    "fixed plugin namespace field": re.compile(r"\bplugin_namespace\b", re.IGNORECASE),
}
# checker-self-scan-allowlist-end


def git_candidates() -> set[str]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return {
        value.decode("utf-8").replace("\\", "/")
        for value in result.stdout.split(b"\0")
        if value
    }


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def table_capabilities(relative_path: str) -> set[str]:
    return set(re.findall(r"^\| (C\d{2}) \|", read(relative_path), re.MULTILINE))


def public_inputs(spec_text: str) -> list[str]:
    match = re.search(
        r"^  public_inputs:\s*$\n(?P<body>(?:^    - .+$\n?)+)",
        spec_text,
        re.MULTILINE,
    )
    if not match:
        return []
    return [line.removeprefix("    - ").strip() for line in match.group("body").splitlines()]


def metadata_values(text: str, key: str) -> set[str]:
    return set(re.findall(rf"^\s*{re.escape(key)}:\s*([^\s#]+)", text, re.MULTILINE))


def metadata_list(text: str, key: str) -> list[str] | None:
    match = re.search(
        rf"^{re.escape(key)}:\s*(?P<inline>\[[^\n]*\])?\s*$",
        text,
        re.MULTILINE,
    )
    if not match:
        return None
    inline = match.group("inline")
    if inline is not None:
        content = inline[1:-1].strip()
        return [] if not content else [value.strip() for value in content.split(",")]

    values: list[str] = []
    for line in text[match.end() :].splitlines():
        if not line.strip():
            continue
        item = re.match(r"^  -\s+(.+?)\s*$", line)
        if not item:
            break
        values.append(item.group(1))
    return values


def index_dependencies(index_text: str) -> dict[str, list[str]]:
    dependencies: dict[str, list[str]] = {}
    for line in index_text.splitlines():
        if not re.match(r"^\| C\d{2} \|", line):
            continue
        cells = [value.strip() for value in line.strip("|").split("|")]
        dependencies[cells[0]] = (
            [] if cells[3] == "none" else [value.strip() for value in cells[3].split(",")]
        )
    return dependencies


def marked_section(text: str, start: str, end: str) -> str | None:
    pattern = re.compile(
        rf"<!-- {re.escape(start)} -->(?P<body>.*?)<!-- {re.escape(end)} -->",
        re.DOTALL,
    )
    match = pattern.search(text)
    return None if match is None else match.group("body")


def novice_journey_errors(journey_text: str) -> list[str]:
    errors: list[str] = []

    journey_statuses = metadata_values(journey_text, "status")
    if len(journey_statuses) != 1 or not journey_statuses <= EXPECTED_NOVICE_STATUSES:
        errors.append("novice journey status is not an allowed lifecycle state")
    try:
        journey_text.encode("ascii")
    except UnicodeEncodeError:
        errors.append("novice journey public text must remain ASCII English")

    for marker in (
        "novice-guide-start",
        "novice-guide-end",
        "fixture-prompts-start",
        "fixture-prompts-end",
    ):
        if journey_text.count(f"<!-- {marker} -->") != 1:
            errors.append(f"novice journey marker must appear exactly once: {marker}")

    interface_design_statuses = metadata_values(journey_text, "interface_design_status")
    if (
        len(interface_design_statuses) != 1
        or interface_design_statuses - EXPECTED_INTERFACE_DESIGN_STATUSES
    ):
        errors.append("novice journeys interface_design_status is not allowed")

    for key in (
        "architecture_design_status",
        "project_state_layout_status",
        "distribution_design_status",
    ):
        if metadata_values(journey_text, key) != {"unconfirmed"}:
            errors.append(f"novice journeys {key} must remain unconfirmed")

    if metadata_values(journey_text, "product_baseline_version") != {"0.1.0"}:
        errors.append("novice journey product baseline must be 0.1.0")
    if metadata_values(journey_text, "phase") != {"P2_design_novice_product_surface"}:
        errors.append("novice journey phase must remain P2 design")
    if metadata_values(journey_text, "public_language") != {"en"}:
        errors.append("novice journey public language must be en")
    if metadata_values(journey_text, "fixture_corpus_version") != {"3"}:
        errors.append("novice journey fixture corpus version must be 3")
    if metadata_values(journey_text, "fixture_count") != {"24"}:
        errors.append("novice journey fixture count must be 24")
    if metadata_values(journey_text, "fixture_prompt_sha256") != {
        EXPECTED_NOVICE_PROMPT_SHA256
    }:
        errors.append("novice journey prompt hash metadata does not match corpus version 3")

    guide_section = marked_section(journey_text, "novice-guide-start", "novice-guide-end")
    if guide_section is None:
        errors.append("novice guide packet markers are missing or out of order")
        guide_section = ""
    journey_ids = re.findall(r"^## (J\d+)\b", guide_section, re.MULTILINE)
    if journey_ids != EXPECTED_JOURNEYS:
        errors.append(f"evaluator-visible novice journey IDs must be J1-J6 in order: {journey_ids}")
    all_journey_ids = re.findall(r"^## (J\d+)\b", journey_text, re.MULTILINE)
    if all_journey_ids != EXPECTED_JOURNEYS:
        errors.append(f"novice journey IDs outside the evaluator packet are not allowed: {all_journey_ids}")

    journey_matches = list(re.finditer(r"^## (J\d+)\b", guide_section, re.MULTILINE))
    for index, match in enumerate(journey_matches):
        end = journey_matches[index + 1].start() if index + 1 < len(journey_matches) else len(guide_section)
        body = guide_section[match.start() : end]
        results = re.findall(
            r"^\| `(success|blocked|failure|deferred|interrupted|recovery_required)` \|",
            body,
            re.MULTILINE,
        )
        if results != EXPECTED_JOURNEY_RESULTS:
            errors.append(f"{match.group(1)} result map is incomplete or out of order: {results}")

    capability_rows = re.findall(r"^\| (C\d{2}) \|", journey_text, re.MULTILINE)
    expected_capability_rows = [f"C{number:02d}" for number in range(1, 20)]
    if capability_rows != expected_capability_rows:
        errors.append(
            "novice journey capability matrix must contain C01-C19 exactly once and in order"
        )

    prompt_section = marked_section(journey_text, "fixture-prompts-start", "fixture-prompts-end")
    if prompt_section is None:
        errors.append("novice journey fixture prompt markers are missing")
    else:
        prompt_hash = hashlib.sha256(prompt_section.encode("utf-8")).hexdigest()
        if prompt_hash != EXPECTED_NOVICE_PROMPT_SHA256:
            errors.append(f"novice journey prompt corpus hash mismatch: {prompt_hash}")
        prompt_ids = re.findall(r"^\| (F\d{2}) \|", prompt_section, re.MULTILINE)
        if prompt_ids != list(EXPECTED_NOVICE_FIXTURES):
            errors.append(f"novice journey prompts must be frozen F01-F24: {prompt_ids}")

    answer_match = re.search(
        r"^### Frozen Answer Key\s*$\n(?P<body>.*?)(?=^### Pass Criteria\s*$)",
        journey_text,
        re.MULTILINE | re.DOTALL,
    )
    if answer_match is None:
        errors.append("novice journey answer key is missing")
    else:
        answer_rows = re.findall(
            r"^\| (F\d{2}) \| `([a-z_]+)` \| `([a-z_]+)` \| `(yes|no)` \| `(framework|downstream_project|unclear)` \|$",
            answer_match.group("body"),
            re.MULTILINE,
        )
        answer_ids = [fixture_id for fixture_id, _, _, _, _ in answer_rows]
        if answer_ids != list(EXPECTED_NOVICE_FIXTURES):
            errors.append(f"novice journey answers must be frozen F01-F24: {answer_ids}")
        actual_answers = {
            fixture_id: (entry_class, next_outcome, decision, cotend_role)
            for fixture_id, entry_class, next_outcome, decision, cotend_role in answer_rows
        }
        if actual_answers != EXPECTED_NOVICE_FIXTURES:
            errors.append("novice journey frozen answer key does not match corpus version 3")

    if "CoTend is the product." not in journey_text:
        errors.append("novice journeys must preserve the framework product boundary")
    if "The downstream software used in this proof is a fixture." not in journey_text:
        errors.append("novice journeys must preserve the downstream fixture boundary")

    return errors


def interface_evidence_errors(
    evidence_text: str,
    interface_text: str,
    journey_text: str,
    expected_mapping: dict[str, tuple[str, str]],
    catalog_skill_ids: set[str],
) -> list[str]:
    errors: list[str] = []
    try:
        evidence_text.encode("ascii")
    except UnicodeEncodeError:
        errors.append("interface evidence must remain ASCII English")

    exact_metadata = {
        "status": {"executed_public_safe"},
        "source_document": {"docs/INTERFACE-CANDIDATE-EVALUATION.md"},
        "journey_prompt_sha256": {EXPECTED_NOVICE_PROMPT_SHA256},
        "repository_access": {"none"},
        "tool_use": {"none"},
        "expected_rows": {"24"},
        "exact_rows": {"24"},
        "correct_decision_flags": {"24"},
        "required_user_stops": {"16_of_16"},
        "verdict": {"pass"},
    }
    for key, expected in exact_metadata.items():
        if metadata_values(evidence_text, key) != expected:
            errors.append(f"interface evidence metadata mismatch: {key}")

    interface_versions = metadata_values(interface_text, "interface_mapping_version")
    if metadata_values(evidence_text, "evaluation_version") != interface_versions:
        errors.append("interface evidence version does not match the candidate packet")
    catalog_hashes = metadata_values(interface_text, "interface_catalog_sha256")
    if metadata_values(evidence_text, "catalog_sha256") != catalog_hashes:
        errors.append("interface evidence catalog hash does not match the candidate packet")
    if len(metadata_values(evidence_text, "evaluator_surface")) != 1:
        errors.append("interface evidence must record one evaluator surface")
    if len(metadata_values(evidence_text, "evaluator_model")) != 1:
        errors.append("interface evidence must record one evaluator model label")
    evaluator_cli = metadata_values(evidence_text, "evaluator_cli")
    if len(evaluator_cli) != 1 or not re.fullmatch(r"\d+\.\d+\.\d+", next(iter(evaluator_cli), "")):
        errors.append("interface evidence must record one semantic CLI version")

    for marker in (
        "evaluator-rules-start",
        "evaluator-rules-end",
        "evaluator-output-start",
        "evaluator-output-end",
    ):
        if evidence_text.count(f"<!-- {marker} -->") != 1:
            errors.append(f"interface evidence marker must appear exactly once: {marker}")

    rules = marked_section(evidence_text, "evaluator-rules-start", "evaluator-rules-end") or ""
    catalog = marked_section(interface_text, "interface-catalog-start", "interface-catalog-end") or ""
    prompts = marked_section(journey_text, "fixture-prompts-start", "fixture-prompts-end") or ""
    packet_hash = hashlib.sha256((rules + catalog + prompts).encode("utf-8")).hexdigest()
    if metadata_values(evidence_text, "packet_sha256") != {packet_hash}:
        errors.append("interface evidence packet hash mismatch")

    output = marked_section(evidence_text, "evaluator-output-start", "evaluator-output-end") or ""
    output_hash = hashlib.sha256(output.encode("utf-8")).hexdigest()
    if metadata_values(evidence_text, "raw_output_sha256") != {output_hash}:
        errors.append("interface evidence raw-output hash mismatch")
    output_block = re.fullmatch(r"\s*```text\n(?P<rows>.*?)\n```\s*", output, re.DOTALL)
    if output_block is None:
        errors.append("interface evidence output must contain exactly one text block")
        output_rows: list[tuple[str, str, str]] = []
    else:
        rows_text = output_block.group("rows")
        output_rows = re.findall(
            r"^(F\d{2}) \| (\$cotend-[a-z0-9-]+) \| (yes|no)$",
            rows_text,
            re.MULTILINE,
        )
        if len(output_rows) != len(rows_text.splitlines()):
            errors.append("interface evidence output contains an unexpected line")

    output_ids = [fixture_id for fixture_id, _, _ in output_rows]
    if output_ids != list(expected_mapping):
        errors.append(f"interface evidence output must contain F01-F24 in order: {output_ids}")
    actual_output = {
        fixture_id: (skill_id, decision)
        for fixture_id, skill_id, decision in output_rows
    }
    if actual_output != expected_mapping:
        errors.append("interface evidence output does not score 24 of 24")
    if {skill_id for _, skill_id, _ in output_rows} != catalog_skill_ids:
        errors.append("interface evidence does not exercise every catalog entry")

    return errors


def interface_candidate_errors(
    interface_text: str,
    journey_text: str,
    evidence_text: str | None = None,
) -> list[str]:
    errors: list[str] = []

    statuses = metadata_values(interface_text, "status")
    if len(statuses) != 1 or statuses - EXPECTED_NOVICE_STATUSES:
        errors.append("interface evaluation must declare one allowed lifecycle status")
    try:
        interface_text.encode("ascii")
    except UnicodeEncodeError:
        errors.append("interface evaluation public text must remain ASCII English")

    exact_metadata = {
        "product_baseline_version": {"0.1.0"},
        "phase": {"P2_design_novice_product_surface"},
        "public_language": {"en"},
        "launch_platform": {"Codex"},
        "architecture_design_status": {"unconfirmed"},
        "project_state_layout_status": {"unconfirmed"},
        "distribution_design_status": {"unconfirmed"},
        "fixture_source": {"docs/NOVICE-JOURNEYS.md"},
        "fixture_source_version": {"3"},
        "fixture_source_prompt_sha256": {EXPECTED_NOVICE_PROMPT_SHA256},
        "interface_mapping_count": {"24"},
        "blind_exact_rows": {"24_of_24"},
        "blind_user_stops": {"16_of_16"},
        "blind_result": {"pass"},
    }
    for key, expected in exact_metadata.items():
        if metadata_values(interface_text, key) != expected:
            errors.append(f"interface evaluation metadata mismatch: {key}")

    lifecycle = next(iter(statuses), "") if len(statuses) == 1 else ""
    expected_authority_state = {
        "draft_for_review": ("pending_user_confirmation", "unconfirmed"),
        "reviewed_pending_user_confirmation": (
            "pending_user_confirmation",
            "unconfirmed",
        ),
        "active_user_confirmed": (
            "active_user_confirmed",
            "baseline_user_confirmed",
        ),
    }.get(lifecycle)
    if expected_authority_state is not None:
        recommendation_status, interface_design_status = expected_authority_state
        if metadata_values(interface_text, "recommendation_status") != {
            recommendation_status
        }:
            errors.append("interface recommendation authority does not match lifecycle")
        if metadata_values(interface_text, "interface_design_status") != {
            interface_design_status
        }:
            errors.append("interface design authority does not match lifecycle")

    if lifecycle == "active_user_confirmed":
        if metadata_values(interface_text, "recommendation_candidate") != {"I6"}:
            errors.append("active interface baseline must preserve confirmed candidate I6")
        if metadata_values(interface_text, "recommendation_strategy") != {
            "layered_common_prefix"
        }:
            errors.append(
                "active interface baseline must preserve the confirmed strategy"
            )
        if metadata_values(interface_text, "interface_catalog_sha256") != {
            EXPECTED_CONFIRMED_INTERFACE_CATALOG_SHA256
        }:
            errors.append("active interface baseline catalog differs from user confirmation")
        for required_text in (
            "The user has confirmed this recommendation as the P2 interface baseline.",
            "## Confirmed Interface Baseline",
            "Recommend, user confirmed.",
        ):
            if required_text not in interface_text:
                errors.append(
                    f"active interface baseline is missing confirmation text: {required_text}"
                )
        for stale_text in (
            "candidate awaiting user confirmation",
            "Recommend, pending user confirmation.",
            "subject to user confirmation",
            "The user is being asked to confirm",
            "does not activate the recommendation",
        ):
            if stale_text in interface_text:
                errors.append(
                    f"active interface baseline retains pending text: {stale_text}"
                )

    recommendation_candidates = metadata_values(interface_text, "recommendation_candidate")
    recommendation_strategies = metadata_values(interface_text, "recommendation_strategy")
    if len(recommendation_candidates) != 1:
        errors.append("interface evaluation must name one recommendation candidate")
    if len(recommendation_strategies) != 1 or not re.fullmatch(
        r"[a-z][a-z0-9_]+", next(iter(recommendation_strategies), "")
    ):
        errors.append("interface evaluation must name one recommendation strategy")
    mapping_versions = metadata_values(interface_text, "interface_mapping_version")
    if len(mapping_versions) != 1 or not next(iter(mapping_versions), "").isdigit():
        errors.append("interface mapping version must be a positive integer")

    for marker in (
        "platform-evidence-start",
        "platform-evidence-end",
        "interface-catalog-start",
        "interface-catalog-end",
    ):
        if interface_text.count(f"<!-- {marker} -->") != 1:
            errors.append(f"interface marker must appear exactly once: {marker}")

    gate_ids = re.findall(r"^\| (H\d+) \|", interface_text, re.MULTILINE)
    if gate_ids != EXPECTED_INTERFACE_GATES:
        errors.append(f"interface hard gates must be H1-H8 in order: {gate_ids}")

    candidate_rows = re.findall(
        r"^\| (I\d+) \| (?P<candidate>[^|]+) \| (?P<strength>[^|]+) \| "
        r"(?P<weakness>[^|]+) \| (?P<disposition>[^|]+) \|$",
        interface_text,
        re.MULTILINE,
    )
    candidate_ids = [row[0] for row in candidate_rows]
    if candidate_ids != EXPECTED_INTERFACE_CANDIDATES:
        errors.append(f"interface candidates must be I1-I6 in order: {candidate_ids}")
    recommendation_candidate = next(iter(recommendation_candidates), "")
    dispositions = {row[0]: row[4].strip() for row in candidate_rows}
    if recommendation_candidate not in dispositions or not dispositions.get(
        recommendation_candidate, ""
    ).startswith("Recommend"):
        errors.append("the metadata recommendation must match the recommended candidate row")

    platform_evidence = marked_section(
        interface_text, "platform-evidence-start", "platform-evidence-end"
    ) or ""
    platform_hash = hashlib.sha256(platform_evidence.encode("utf-8")).hexdigest()
    if metadata_values(interface_text, "platform_evidence_sha256") != {platform_hash}:
        errors.append("platform evidence table hash mismatch")
    platform_rows = re.findall(
        r"^\| (P\d{2}) \| ([^|]+) \| \[[^\]]+\]"
        r"\((https://learn\.chatgpt\.com/[^)]+)\) \| (\d{4}-\d{2}-\d{2}) \| ([^|]+) \|$",
        platform_evidence,
        re.MULTILINE,
    )
    platform_ids = [claim_id for claim_id, _, _, _, _ in platform_rows]
    if platform_ids != EXPECTED_PLATFORM_CLAIMS:
        errors.append(f"platform evidence claims must be P01-P09 in order: {platform_ids}")
    evidence_dates = metadata_values(interface_text, "platform_evidence_date")
    if len(evidence_dates) != 1 or any(row[3] not in evidence_dates for row in platform_rows):
        errors.append("platform evidence rows must use the recorded access date")
    for claim_id, claim, _, _, boundary in platform_rows:
        if len(claim.strip()) < 24 or len(boundary.strip()) < 24:
            errors.append(f"platform evidence claim is not bounded enough: {claim_id}")
    p04_boundary = next((row[4].casefold() for row in platform_rows if row[0] == "P04"), "")
    if "vary" not in p04_boundary or "verify" not in p04_boundary:
        errors.append("slash-list evidence must disclose environment variation and re-verification")

    catalog = marked_section(interface_text, "interface-catalog-start", "interface-catalog-end") or ""
    catalog_hash = hashlib.sha256(catalog.encode("utf-8")).hexdigest()
    if metadata_values(interface_text, "interface_catalog_sha256") != {catalog_hash}:
        errors.append("interface catalog metadata hash mismatch")
    catalog_rows = re.findall(
        r"^\| `([^`]+)` \| `([^`]+)` \| (core|contextual) \| `([^`]+)` \| ([^|]+) \|$",
        catalog,
        re.MULTILINE,
    )
    if len(catalog_rows) != len(EXPECTED_INTERFACE_DESTINATIONS):
        errors.append("interface catalog must contain ten unique semantic destinations")
    actual_entries = {
        skill_id: (display_name, layer, destination, description.strip())
        for skill_id, display_name, layer, destination, description in catalog_rows
    }
    if len(actual_entries) != len(catalog_rows):
        errors.append("interface catalog Skill IDs must be unique")
    if len({row[1] for row in catalog_rows}) != len(catalog_rows):
        errors.append("interface catalog display names must be unique")
    destination_to_skill = {destination: skill_id for skill_id, _, _, destination, _ in catalog_rows}
    if set(destination_to_skill) != set(EXPECTED_INTERFACE_DESTINATIONS):
        errors.append("interface catalog semantic destinations are incomplete or duplicated")
    for skill_id, (display_name, layer, destination, description) in actual_entries.items():
        if not skill_id.startswith("$cotend-"):
            errors.append(f"interface Skill ID lacks the cotend- prefix: {skill_id}")
        if not display_name.startswith("CoTend "):
            errors.append(f"interface display name lacks the CoTend prefix: {display_name}")
        expected_layer, required_terms = EXPECTED_INTERFACE_DESTINATIONS.get(
            destination, (None, ())
        )
        if layer != expected_layer:
            errors.append(f"interface destination has the wrong surface layer: {destination}")
        description_text = description.casefold()
        missing_terms = [term for term in required_terms if term not in description_text]
        if missing_terms:
            errors.append(f"interface description is incomplete for {destination}: {missing_terms}")
    if "$cotend-advanced" in actual_entries or any(
        display_name == "CoTend Advanced"
        for display_name, _, _, _ in actual_entries.values()
    ):
        errors.append("a generic advanced entry is not allowed")

    expected_mapping = {
        fixture_id: (
            destination_to_skill.get(destination, ""),
            EXPECTED_NOVICE_FIXTURES[fixture_id][2],
        )
        for fixture_id, destination in EXPECTED_INTERFACE_FIXTURE_DESTINATIONS.items()
    }
    mapping_match = re.search(
        r"^### Frozen Interface Mapping\s*$\n(?P<body>.*?)(?=^### Pass Criteria\s*$)",
        interface_text,
        re.MULTILINE | re.DOTALL,
    )
    if mapping_match is None:
        errors.append("frozen interface mapping is missing")
    else:
        mapping_rows = re.findall(
            r"^\| (F\d{2}) \| `([^`]+)` \| `(yes|no)` \|$",
            mapping_match.group("body"),
            re.MULTILINE,
        )
        mapping_ids = [fixture_id for fixture_id, _, _ in mapping_rows]
        if mapping_ids != list(expected_mapping):
            errors.append(f"interface mapping must contain F01-F24 in order: {mapping_ids}")
        actual_mapping = {
            fixture_id: (skill_id, decision)
            for fixture_id, skill_id, decision in mapping_rows
        }
        if actual_mapping != expected_mapping:
            errors.append("interface frozen mapping does not match its semantic catalog")

    evidence_paths = metadata_values(interface_text, "blind_evidence")
    if len(evidence_paths) != 1 or not next(iter(evidence_paths), "").startswith("docs/evidence/"):
        errors.append("interface evaluation must name one public-safe blind evidence file")
    elif evidence_text is None:
        errors.append("interface blind evidence file is missing")
    else:
        errors.extend(
            interface_evidence_errors(
                evidence_text,
                interface_text,
                journey_text,
                expected_mapping,
                set(actual_entries),
            )
        )

    if "docs/COMMAND-CONTRACTS.md" in interface_text:
        errors.append("interface evaluation must not use ignored design history as a public source")
    if "CoTend is the product:" not in interface_text:
        errors.append("interface evaluation must preserve the framework product boundary")
    if "There is no generic `CoTend Advanced` entry" not in interface_text:
        errors.append("interface evaluation must reject a generic advanced placeholder")
    if metadata_values(journey_text, "fixture_prompt_sha256") != {
        EXPECTED_NOVICE_PROMPT_SHA256
    }:
        errors.append("interface evaluation fixture source no longer matches the journey corpus")

    return errors


def interface_authority_errors(
    interface_text: str,
    journey_text: str,
    prd_text: str,
    interface_path: str,
) -> list[str]:
    errors: list[str] = []
    interface_design_status = metadata_values(interface_text, "interface_design_status")
    for source_path, source_text in (
        ("docs/NOVICE-JOURNEYS.md", journey_text),
        ("docs/PRODUCT-PRD.md", prd_text),
    ):
        if metadata_values(source_text, "interface_design_status") != (
            interface_design_status
        ):
            errors.append(f"interface design authority drift: {source_path}")

    if interface_design_status == {"baseline_user_confirmed"}:
        if metadata_values(prd_text, "interface_baseline") != {interface_path}:
            errors.append("PRD must link the active interface baseline")
        if metadata_values(prd_text, "stage") != {"novice_product_surface_design"}:
            errors.append("PRD stage must match the active P2 interface baseline")
        if re.search(
            r"公开入口.{0,20}架构.{0,20}状态布局.{0,20}安装渠道.{0,40}另行决定",
            prd_text,
        ):
            errors.append("PRD retains stale unconfirmed-interface prose")

    return errors


def checker_self_scan_errors(checker_text: str) -> list[str]:
    errors: list[str] = []
    starts = list(
        re.finditer(r"^# checker-self-scan-allowlist-start$", checker_text, re.MULTILINE)
    )
    ends = list(
        re.finditer(r"^# checker-self-scan-allowlist-end$", checker_text, re.MULTILINE)
    )
    if len(starts) != 1 or len(ends) != 1 or starts[0].start() >= ends[0].end():
        return ["checker self-scan allowlist markers are invalid"]
    reduced = checker_text[: starts[0].start()] + checker_text[ends[0].end() :]
    for label, pattern in FORBIDDEN_PUBLIC_PATTERNS.items():
        if pattern.search(reduced):
            errors.append(f"scripts/check_repository.py: {label} outside the policy allowlist")
    return errors


def reference_study_errors(study_text: str, registry_text: str) -> list[str]:
    errors: list[str] = []

    exact_study_metadata = {
        "status": {"research_evidence"},
        "authority": {"design_input_only"},
        "sample": {"four_core_plus_two_selective"},
        "source_registry": {"../UPSTREAM-SOURCES.md"},
        "architecture_design_status": {"unconfirmed"},
        "project_state_layout_status": {"unconfirmed"},
        "distribution_design_status": {"unconfirmed"},
        "execution_evidence": {"none"},
        "source_copying": {"none"},
    }
    for key, expected in exact_study_metadata.items():
        if metadata_values(study_text, key) != expected:
            errors.append(f"reference study metadata mismatch: {key}")

    if metadata_values(registry_text, "implementation_dependency") != {
        "pinned_dual_ai_release_2026_07_11_3"
    }:
        errors.append("upstream registry must pin the adopted primary productization source")
    if metadata_values(registry_text, "source_copying") != {
        "scoped_5_adapted_plus_2_byte_identical_skills"
    }:
        errors.append("upstream registry must record the scoped primary-source adoption")

    blocks = list(
        re.finditer(
            r"^## (RF\d{2}) [^\n]+\n(?P<body>.*?)(?=^## RF\d{2} |^## 审查控制|\Z)",
            registry_text,
            re.MULTILINE | re.DOTALL,
        )
    )
    source_ids = [match.group(1) for match in blocks]
    if source_ids != list(EXPECTED_REFERENCE_SOURCES):
        errors.append(f"upstream source IDs must be RF01-RF06 in order: {source_ids}")

    for match in blocks:
        source_id = match.group(1)
        expected = EXPECTED_REFERENCE_SOURCES.get(source_id)
        if expected is None:
            continue
        body = match.group("body")
        expected_source, expected_commit, expected_license = expected
        exact_values = {
            "source": expected_source,
            "reviewed_commit": expected_commit,
            "declared_license": expected_license,
            "adoption_status": "no_source_adoption",
        }
        for key, value in exact_values.items():
            if metadata_values(body, key) != {value}:
                errors.append(f"{source_id}: upstream registry mismatch for {key}")

    required_findings = (
        "语义入口不等于实体 Skill",
        "项目真相必须独立于适配器",
        "生成文件所有权需要确定性证据",
        "Hook 是可选增强，不是 MVP 前提",
        "安装本身就是小白产品的一部分",
        "本研究不批准任何架构",
    )
    for finding in required_findings:
        if finding not in study_text:
            errors.append(f"reference study is missing a required boundary: {finding}")

    return errors


def owner_document_language_errors(
    prd_text: str,
    analysis_documents: dict[str, str],
) -> list[str]:
    errors: list[str] = []
    exact_language_metadata = {
        "launch_language": {"en"},
        "launch_localization_mode": {"english_only"},
        "canonical_interface_language": {"en"},
        "analysis_document_language": {"zh-CN"},
        "analysis_document_language_authority": {"product_owner_confirmed"},
    }
    for key, expected in exact_language_metadata.items():
        if metadata_values(prd_text, key) != expected:
            errors.append(f"PRD language policy mismatch: {key}")

    for required_boundary in (
        "面向产品 owner 的分析、研究、比较、评估和审查说明正文默认使用简体中文",
        "首发产品表面、安装说明和面向最终用户的产品文档继续使用英文",
    ):
        if required_boundary not in prd_text:
            errors.append(f"PRD language boundary is missing: {required_boundary}")

    expected_analysis_paths = (
        "docs/MARKET-LANDSCAPE.md",
        "docs/REFERENCE-FRAMEWORK-IMPLEMENTATION-STUDY.md",
        "UPSTREAM-SOURCES.md",
        "upstream/FRAMEWORK-ADOPTION-PROPOSAL.md",
        "upstream/FRAMEWORK-ADOPTION-PLAN.md",
        "FRAMEWORK-CHANGE-EVAL.md",
    )
    for path in expected_analysis_paths:
        text = analysis_documents.get(path)
        if text is None:
            errors.append(f"owner-facing analysis is missing or ignored: {path}")
            continue
        prose = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        prose = re.sub(r"`[^`\n]+`", "", prose)
        prose = re.sub(r"\]\([^)]+\)", "]", prose)
        cjk_count = len(re.findall(r"[\u4e00-\u9fff]", prose))
        latin_count = len(re.findall(r"[A-Za-z]", prose))
        if cjk_count == 0 or cjk_count < latin_count:
            errors.append(
                f"{path}: owner-facing prose must be predominantly Chinese "
                f"(cjk={cjk_count}, latin={latin_count})"
            )

    return errors


def productization_truth_errors(
    prd_text: str,
    clean_room_text: str,
    coverage_text: str,
    roadmap_text: str,
    behavior_standard_text: str,
    registry_text: str,
    capability_map_text: str,
    specs: dict[str, str],
    journey_text: str,
    interface_text: str,
    interface_evidence_text: str | None,
) -> list[str]:
    errors: list[str] = []

    exact_prd_metadata = {
        "productization_source": {"dual-ai"},
        "productization_default": {"rename_first_preserve_first"},
        "upstream_adoption_status": {"adopted_verified_repository_source"},
        "interface_design_status": {"unconfirmed"},
        "interface_revalidation_reason": {
            "desktop_selector_and_implicit_discovery_not_validated"
        },
        "stage": {"codex_project_carrier_validated_live_delivery_pending"},
    }
    for key, expected in exact_prd_metadata.items():
        if metadata_values(prd_text, key) != expected:
            errors.append(f"PRD productization truth mismatch: {key}")

    for required_text in (
        "默认产品化方法是 `rename-first`、`preserve-first`",
        "仓库 Codex Skill 的 7 目录分层",
        "项目级 `$skill-name` 显式调用已有真实 Codex 证据",
        "用户原创且由已验证 release 以 Apache-2.0 发布的 dual-ai 内容，可以",
        "ready_for_repository_source_implementation: yes",
        "ready_for_live_delivery: no",
    ):
        if required_text not in prd_text:
            errors.append(f"PRD is missing rename-first boundary: {required_text}")
    for stale_text in (
        "clean-room 独立实现的公开产品",
        "P2 界面基线已由用户确认",
        "I6 的规范入口显示名",
        "当前没有第三方归属声明",
    ):
        if stale_text in prd_text:
            errors.append(f"PRD retains superseded productization text: {stale_text}")

    exact_clean_metadata = {
        "productization_default": {"rename_first_preserve_first"},
        "clean_room_scope": {"restricted_unknown_or_private_material"},
    }
    for key, expected in exact_clean_metadata.items():
        if metadata_values(clean_room_text, key) != expected:
            errors.append(f"source-aware policy metadata mismatch: {key}")
    for required_text in (
        "user_owned_upstream_release",
        "adopted",
        "adapted",
        "未列入 adoption 记录",
        "framework lock",
    ):
        if required_text not in clean_room_text:
            errors.append(f"source-aware policy is missing: {required_text}")
    for stale_text in (
        "私有上游只提供抽象理念",
        "公开版的实现、命名、文案、模板和测试必须从本产品需求重新设计并独立编写",
        "禁止边看上游文件边逐段改名",
    ):
        if stale_text in clean_room_text:
            errors.append(f"source-aware policy retains superseded rule: {stale_text}")

    if metadata_values(coverage_text, "source_method") != {
        "user_owned_upstream_release_trace_plus_user_scenarios"
    }:
        errors.append("capability coverage source method is not upstream-trace based")
    if metadata_values(coverage_text, "productization_default") != {
        "preserve_existing_behavior_before_redesign"
    }:
        errors.append("capability coverage does not preserve upstream behavior by default")
    if "Rename-first productization disposition" not in coverage_text:
        errors.append("capability coverage lacks rename-first dispositions")

    exact_roadmap_metadata = {
        "route_type": {"source_aware_rename_first_productization"},
        "current_phase": {"P4-codex-project-delivery-and-recovery"},
    }
    for key, expected in exact_roadmap_metadata.items():
        if metadata_values(roadmap_text, key) != expected:
            errors.append(f"productization roadmap mismatch: {key}")
    if "直接改名和最小适配是默认起点" not in roadmap_text:
        errors.append("productization roadmap lacks the confirmed rename-first default")

    expected_mode_line = (
        "implementation_mode: direct_adoption | rename_only | platform_adaptation | "
        "external_dependency | independent | mixed | pending"
    )
    expected_handoff_line = (
        "Direct adoption, rename-only adaptation, and platform adaptation may read "
        "only files named by the adoption record."
    )
    for required_text in (expected_mode_line, expected_handoff_line):
        if required_text not in behavior_standard_text:
            errors.append(
                f"behavior standard lacks a rename-first implementation mode: {required_text}"
            )
    stale_mode_line = "implementation_mode: direct_adaptation | independent | mixed | pending"
    if stale_mode_line in behavior_standard_text:
        errors.append("behavior standard retains the coarse direct-adaptation mode set")

    if (
        "relationship: primary_user_owned_productization_source_plus_secondary_public_references"
        not in registry_text
    ):
        errors.append("upstream registry does not separate primary and secondary sources")
    for required_text in (
        "## UP01 dual-ai 分享包",
        "role: primary_productization_source",
        "reviewed_release: 2026.07.11.3",
        "adoption_status: repository_source_adopted_verified",
        "candidate_record: upstream/FRAMEWORK-CANDIDATE.json",
        "codex_role_map: upstream/CODEX-SKILL-ROLE-MAP.json",
        "adoption_proposal: upstream/FRAMEWORK-ADOPTION-PROPOSAL.md",
        "adoption_plan: upstream/FRAMEWORK-ADOPTION-PLAN.md",
        "capability_map: upstream/CAPABILITY-IMPLEMENTATION-MAP.json",
        "adoption_record: upstream/FRAMEWORK-ADOPTION-LOG.md#release-2026-07-11-3-initial-adoption",
        "final_framework_lock: upstream/framework.lock.json",
    ):
        if required_text not in registry_text:
            errors.append(f"upstream registry is missing primary source evidence: {required_text}")

    try:
        capability_map = json.loads(capability_map_text)
    except json.JSONDecodeError as exc:
        capability_map = {}
        errors.append(f"capability implementation map JSON is invalid: {exc}")
    capability_entries = capability_map.get("capabilities")
    modes_by_id: dict[str, str] = {}
    if capability_map.get("status") != "adopted_verified":
        errors.append("capability implementation map is not finalized")
    if not isinstance(capability_entries, list):
        errors.append("capability implementation map entries are invalid")
    else:
        for entry in capability_entries:
            if not isinstance(entry, dict):
                continue
            capability_id = entry.get("capability_id")
            mode = entry.get("implementation_mode")
            if isinstance(capability_id, str) and isinstance(mode, str):
                modes_by_id[capability_id] = mode
        if set(modes_by_id) != EXPECTED_CAPABILITIES:
            errors.append("capability implementation map must contain C01-C19")

    if len(specs) != len(EXPECTED_CAPABILITIES):
        errors.append("productization trace check requires all 19 behavior specs")
    for spec_path, spec_text in specs.items():
        spec_ids = metadata_values(spec_text, "spec_id")
        spec_id = next(iter(spec_ids), "") if len(spec_ids) == 1 else ""
        if metadata_values(spec_text, "upstream_productization_trace") != {"mapped"}:
            errors.append(f"{spec_path}: upstream productization trace must be mapped")
        expected_mode = modes_by_id.get(spec_id)
        if expected_mode is None or metadata_values(spec_text, "implementation_mode") != {
            expected_mode
        }:
            errors.append(f"{spec_path}: implementation mode does not match capability map")
        for required_text in (
            "user_owned_upstream_release",
            "files named by an explicitly adopted and integrity-verified upstream release record",
            "unreleased or private upstream working files",
        ):
            if required_text not in spec_text:
                errors.append(f"{spec_path}: source-aware implementation boundary is missing")
                break

    exact_journey_metadata = {
        "status": {"reviewed_pending_user_confirmation"},
        "interface_design_status": {"unconfirmed"},
        "revalidation_reason": {"rename_first_upstream_surface_not_mapped"},
    }
    for key, expected in exact_journey_metadata.items():
        if metadata_values(journey_text, key) != expected:
            errors.append(f"novice journey revalidation metadata mismatch: {key}")

    exact_interface_metadata = {
        "status": {"reviewed_pending_user_confirmation"},
        "recommendation_status": {"pending_user_confirmation"},
        "interface_design_status": {"unconfirmed"},
        "revalidation_reason": {"existing_dual_ai_surface_was_not_mapped_first"},
    }
    for key, expected in exact_interface_metadata.items():
        if metadata_values(interface_text, key) != expected:
            errors.append(f"interface reopening metadata mismatch: {key}")
    for required_text in (
        "historical candidate evidence",
        "current default is to map and rename the existing surface first",
    ):
        if required_text not in interface_text:
            errors.append(f"interface reopening explanation is missing: {required_text}")
    if interface_evidence_text is None:
        errors.append("historical interface evidence is missing")
    else:
        if metadata_values(interface_evidence_text, "authority") != {
            "historical_candidate_evidence_only"
        }:
            errors.append("interface evidence still appears to grant current authority")
        if metadata_values(interface_evidence_text, "current_interface_authority") != {"none"}:
            errors.append("interface evidence current authority must be none")

    return errors


def upstream_adoption_errors(
    candidate_text: str,
    role_map_text: str,
    proposal_text: str,
    adoption_plan_text: str,
    capability_map_text: str,
    adoption_log_text: str,
    lock_text: str,
    public_candidates: set[str],
) -> list[str]:
    errors: list[str] = []
    try:
        candidate = json.loads(candidate_text)
    except (TypeError, json.JSONDecodeError) as exc:
        return [f"upstream framework candidate JSON is invalid: {exc}"]
    try:
        role_map = json.loads(role_map_text)
    except (TypeError, json.JSONDecodeError) as exc:
        return [f"upstream Codex role-map JSON is invalid: {exc}"]
    try:
        capability_map = json.loads(capability_map_text)
        framework_lock = json.loads(lock_text)
    except (TypeError, json.JSONDecodeError) as exc:
        return [f"upstream adoption JSON is invalid: {exc}"]

    def value(data: dict[str, object], *keys: str) -> object:
        current: object = data
        for key in keys:
            if not isinstance(current, dict) or key not in current:
                return None
            current = current[key]
        return current

    expected_candidate_values = {
        ("schema",): "cotend.framework-candidate",
        ("schema_version",): 1,
        ("status",): "adopted_verified",
        ("candidate_only",): False,
        ("release_id",): "2026.07.11.3",
        ("framework_protocol_version",): "1.52",
        ("dual_model_upgrade_version",): "1.7",
        ("package_schema_version",): 2,
        ("source_framework_commit",): "5496073e19e239ef19eb055f2b470185fab25d3a",
        ("release_anchor", "type"): "annotated_git_tag",
        ("release_anchor", "tag"): "dual-ai-share-2026.07.11.3",
        ("release_anchor", "tag_object"): "cef8add414a6d9704d3f58785a128bc56f44b263",
        ("release_anchor", "release_commit"): "71e45d9ebeff4d9d61c180711c25267b9fe31549",
        ("release_anchor", "package_tree"): "a70231e0445d9795a00212e8e6c53c149bfbc431",
        ("release_anchor", "publisher_identity_authenticated"): False,
        ("integrity", "manifest_sha256"): (
            "919fe34254b51619ddca1d010445281d4f7ceec958ee8cfd1958eaccb02bd006"
        ),
        ("integrity", "manifest_entries"): 65,
        ("integrity", "provenance_covered_files"): 66,
        ("integrity", "verification"): "passed",
        ("carriers", "codex", "skill_count"): 7,
        ("carriers", "claude", "skill_count"): 3,
        ("adoption", "state"): "adopted",
        ("adoption", "source_carrier"): "skills/",
        ("adoption", "capability_map"): "upstream/CAPABILITY-IMPLEMENTATION-MAP.json",
        ("adoption", "adoption_record"): (
            "upstream/FRAMEWORK-ADOPTION-LOG.md#release-2026-07-11-3-initial-adoption"
        ),
        ("adoption", "final_framework_lock_exists"): True,
    }
    for keys, expected in expected_candidate_values.items():
        if value(candidate, *keys) != expected:
            errors.append(f"upstream candidate mismatch: {'.'.join(keys)}")
    expected_skill_trees = {
        "diagnose-only": "88dc2e47dba438720a336c38103308aeae3d635e",
        "dual-ai-collaboration": "b75114a7e0fd2027943ed98217a0f9d581cbdae9",
        "dual-ai-init": "cb233ade310c37e0cd038ff5752eeced92a303f0",
        "dual-ai-project-init": "1f2fdd44e90f31fec310eaf78b02e48de4fed53c",
        "dual-model-upgrade": "dfb25bd4464e0266b665af138a5f3902b44ce281",
        "grill-me": "70df660726ef12349a40dc0353a681c82414fe95",
        "karpathy-guidelines": "e119339197d600aa39a24fd7a95c946800c9c949",
    }
    if value(candidate, "carriers", "codex", "skill_trees") != expected_skill_trees:
        errors.append("upstream candidate Codex Skill tree inventory drift")

    expected_skill_ids = {
        "cotend-init",
        "cotend-project-init",
        "cotend-collaboration",
        "cotend-diagnose-only",
        "cotend-model-upgrade",
        "grill-me",
        "karpathy-guidelines",
    }
    skill_files = {
        path for path in public_candidates if path.startswith("skills/")
    }
    actual_skill_ids = {
        path.split("/", 2)[1] for path in skill_files if path.count("/") >= 2
    }
    if actual_skill_ids != expected_skill_ids:
        errors.append("adopted Codex Skill directory set must contain exactly seven Skills")
    if len(skill_files) != 30:
        errors.append(f"adopted Codex Skill source set must contain 30 files: {len(skill_files)}")
    adopted_files = value(candidate, "adoption", "imported_files")
    adapted_files = value(candidate, "adoption", "adapted_files")
    if not isinstance(adopted_files, list) or not isinstance(adapted_files, list):
        errors.append("framework candidate file-level adoption inventory is invalid")
    else:
        adopted_set = set(adopted_files)
        adapted_set = set(adapted_files)
        expected_direct_adoption = {
            "skills/grill-me/SKILL.md",
            "skills/karpathy-guidelines/SKILL.md",
        }
        if adopted_set != expected_direct_adoption:
            errors.append("directly adopted Skill file inventory drift")
        if adopted_set & adapted_set or adopted_set | adapted_set != skill_files:
            errors.append("candidate adopted/adapted inventory does not equal the 30 Skill files")
    if value(candidate, "adoption", "required_before_lock") != []:
        errors.append("framework candidate retains unresolved pre-lock requirements")

    if role_map.get("schema") != "cotend.codex-skill-role-map":
        errors.append("Codex role map schema mismatch")
    if role_map.get("status") != "adopted_verified":
        errors.append("Codex role map is not finalized as adopted")
    if role_map.get("candidate_release") != "2026.07.11.3":
        errors.append("Codex role map release mismatch")
    if role_map.get("public_interface_authority") != (
        "codex_skill_source_set_adopted_live_delivery_pending"
    ):
        errors.append("Codex role map role-layer/name authority boundary drift")
    if role_map.get("role_layer_decision") != "product_owner_confirmed":
        errors.append("Codex role map role-layer decision mismatch")
    if role_map.get("user_owned_naming_decision") != "product_owner_confirmed":
        errors.append("Codex role map user-owned naming decision mismatch")
    if role_map.get("third_party_bundling_decision") != "product_owner_confirmed":
        errors.append("Codex role map third-party bundling decision mismatch")
    if role_map.get("skill_count") != 7:
        errors.append("Codex role map skill_count must be 7")

    role_entries = role_map.get("skills")
    if not isinstance(role_entries, list):
        errors.append("Codex role map skills must be a list")
        role_entries = []
    roles_by_id: dict[str, dict[str, object]] = {}
    for entry in role_entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("source_skill_id"), str):
            errors.append("Codex role map contains an invalid Skill entry")
            continue
        skill_id = entry["source_skill_id"]
        if skill_id in roles_by_id:
            errors.append(f"Codex role map duplicates Skill: {skill_id}")
            continue
        roles_by_id[skill_id] = entry
    if set(roles_by_id) != set(expected_skill_trees):
        errors.append("Codex role map must contain exactly the seven candidate Skills")

    expected_roles = {
        "dual-ai-init": (
            "user_owned_original",
            "unified_visible_entry",
            "adapted",
            "rename_only",
            "cotend-init",
        ),
        "dual-ai-project-init": (
            "user_owned_original",
            "internal_auto_mode_engine",
            "adapted",
            "platform_adaptation",
            "cotend-project-init",
        ),
        "dual-ai-collaboration": (
            "user_owned_original",
            "shared_governance_core",
            "adapted",
            "platform_adaptation",
            "cotend-collaboration",
        ),
        "diagnose-only": (
            "user_owned_original",
            "contextual_read_only_diagnosis",
            "adapted",
            "platform_adaptation",
            "cotend-diagnose-only",
        ),
        "dual-model-upgrade": (
            "user_owned_original",
            "advanced_model_role_lifecycle",
            "adapted",
            "platform_adaptation",
            "cotend-model-upgrade",
        ),
        "grill-me": (
            "adapted_third_party",
            "internal_clarification_companion",
            "adopted",
            "direct_adoption",
            "grill-me",
        ),
        "karpathy-guidelines": (
            "bundled_third_party",
            "internal_ai_implementation_discipline",
            "adopted",
            "direct_adoption",
            "karpathy-guidelines",
        ),
    }
    for skill_id, expected in expected_roles.items():
        entry = roles_by_id.get(skill_id)
        if entry is None:
            continue
        actual = (
            entry.get("source_relationship"),
            entry.get("current_role"),
            entry.get("adoption_status"),
            entry.get("implementation_mode"),
            entry.get("target_skill_id"),
        )
        if actual != expected:
            errors.append(f"Codex role mapping drift: {skill_id}")
        if entry.get("source_tree") != expected_skill_trees[skill_id]:
            errors.append(f"Codex role map tree mismatch: {skill_id}")

    expected_naming_status = {
        "dual-ai-init": "user_confirmed",
        "dual-ai-project-init": "user_confirmed",
        "dual-ai-collaboration": "user_confirmed",
        "diagnose-only": "user_confirmed",
        "dual-model-upgrade": "user_confirmed",
        "grill-me": "preserve_third_party_identity_if_bundled",
        "karpathy-guidelines": "preserve_third_party_identity_if_bundled",
    }
    for skill_id, expected in expected_naming_status.items():
        if roles_by_id.get(skill_id, {}).get("naming_status") != expected:
            errors.append(f"Codex role-map naming status drift: {skill_id}")

    init_entry = roles_by_id.get("dual-ai-init", {})
    if init_entry.get("delegates_to") != ["dual-ai-project-init"]:
        errors.append("dual-ai-init must remain the thin entry delegating to project init")
    for third_party_id in ("grill-me", "karpathy-guidelines"):
        if roles_by_id.get(third_party_id, {}).get("bundling_status") != "user_confirmed":
            errors.append(f"{third_party_id} bundling decision drift")

    adoption = role_map.get("adoption")
    if not isinstance(adoption, dict):
        errors.append("Codex role map adoption boundary is missing")
    else:
        expected_adoption_boundary = {
            "state": "adopted",
            "role_layers_confirmed": True,
            "user_owned_skill_names_confirmed": True,
            "final_names_confirmed": True,
            "final_names_scope": (
                "five_user_owned_ids_plus_preserved_third_party_identity"
            ),
            "physical_skill_count_confirmed": True,
            "physical_skill_count_scope": "repository_codex_skill_source_set",
            "confirmed_codex_skill_count": 7,
            "third_party_bundling_confirmed": True,
            "codex_skill_set_decisions_complete": True,
            "actual_adoption_authorized": True,
            "repository_source_carrier": "skills/",
            "repository_source_implemented": True,
            "capability_map": "upstream/CAPABILITY-IMPLEMENTATION-MAP.json",
            "adoption_record": (
                "upstream/FRAMEWORK-ADOPTION-LOG.md#release-2026-07-11-3-initial-adoption"
            ),
            "live_install_authorized": False,
            "live_install_performed": False,
            "plugin_or_marketplace_carrier": "github_root_candidate_local_verified",
            "final_framework_lock_exists": True,
        }
        for key, expected in expected_adoption_boundary.items():
            if adoption.get(key) != expected:
                errors.append(f"Codex role-map adoption boundary mismatch: {key}")

    if metadata_values(proposal_text, "status") != {"adopted_verified"}:
        errors.append("framework adoption proposal is not finalized as adopted")
    exact_proposal_metadata = {
        "candidate_release": {"2026.07.11.3"},
        "role_layer_status": {"user_confirmed"},
        "role_layer_decision": {"product_owner_confirmed"},
        "user_owned_skill_name_status": {"user_confirmed"},
        "MIT_companion_bundling_status": {"user_confirmed"},
        "codex_skill_set_decisions_status": {"complete"},
        "adoption_state": {"adopted"},
        "final_framework_lock_exists": {"true"},
        "analysis_language": {"zh-CN"},
    }
    for key, expected in exact_proposal_metadata.items():
        if metadata_values(proposal_text, key) != expected:
            errors.append(f"framework adoption proposal metadata mismatch: {key}")
    for required_text in (
        "7 个 Codex Skill 直接理解成 7 个同级公开命令",
        "dual-ai-init` 是普通用户的统一入口",
        "dual-ai-project-init` 是入口内部的 Auto Mode 引擎",
        "用户已确认保留这套分层",
        "五个用户原创 Skill 分别命名为",
        "确认 Codex 首发源树直接内置 `grill-me` 与 `karpathy-guidelines`",
        "仓库内 Codex 技能源集合已采用为 7 个目录、30 个文件",
        "`upstream/framework.lock.json` 已在以下条件同时满足后创建",
        "adoption_state: adopted",
    ):
        if required_text not in proposal_text:
            errors.append(f"framework adoption proposal is missing: {required_text}")

    if metadata_values(adoption_plan_text, "status") != {"implemented_verified"}:
        errors.append("framework adoption plan is not finalized as implemented")
    exact_plan_metadata = {
        "candidate_release": {"2026.07.11.3"},
        "target_platform": {"Codex"},
        "target_source_carrier": {"skills/"},
        "live_install_target": {"not_authorized"},
        "plugin_or_marketplace_carrier": {"github_root_candidate_local_verified"},
        "implementation_authority": {"product_owner_confirmed"},
        "adoption_state": {"adopted"},
        "final_framework_lock_exists": {"true"},
        "analysis_language": {"zh-CN"},
    }
    for key, expected in exact_plan_metadata.items():
        if metadata_values(adoption_plan_text, key) != expected:
            errors.append(f"framework adoption plan metadata mismatch: {key}")
    for required_text in (
        "7 个技能目录，共 30 个文件",
        "skills/cotend-init/",
        "skills/cotend-project-init/",
        "skills/cotend-collaboration/",
        "skills/cotend-diagnose-only/",
        "skills/cotend-model-upgrade/",
        "skills/grill-me/",
        "skills/karpathy-guidelines/",
        "cotend-collaboration-v1.52",
        "cotend-model-upgrade-v1.7",
        "mechanism_budget: three_repository_integrity_mechanisms_no_new_user_workflow",
        "不新增命令层、路由层、状态目录或重复内核",
        '"type": "containing_commit"',
        "锁文件只能在采用或升级提交中修改",
        "不安装到用户全局 Codex 目录",
        "仓库实现叶已经完成",
    ):
        if required_text not in adoption_plan_text:
            errors.append(f"framework adoption plan is missing: {required_text}")

    required_artifacts = {
        ".gitattributes",
        "NOTICE",
        "THIRD-PARTY-NOTICES.md",
        "THIRD-PARTY-SOURCES.json",
        "THIRD-PARTY-LICENSES/grill-me-MIT.txt",
        "THIRD-PARTY-LICENSES/karpathy-guidelines-MIT.txt",
        "scripts/verify_adopted_skill_set.py",
        "FRAMEWORK-CHANGE-EVAL.md",
        "upstream/CAPABILITY-IMPLEMENTATION-MAP.json",
        "upstream/FRAMEWORK-ADOPTION-LOG.md",
        "upstream/framework.lock.json",
    }
    missing_artifacts = required_artifacts - public_candidates
    if missing_artifacts:
        errors.append(f"adoption artifacts are missing or ignored: {sorted(missing_artifacts)}")

    if capability_map.get("schema") != "cotend.capability-implementation-map":
        errors.append("capability implementation map schema mismatch")
    if capability_map.get("status") != "adopted_verified":
        errors.append("capability implementation map status mismatch")
    if capability_map.get("capability_count") != 19:
        errors.append("capability implementation map count mismatch")

    expected_lock_values = {
        ("schema",): "cotend.framework-lock",
        ("schema_version",): 1,
        ("status",): "adopted_verified",
        ("release_id",): "2026.07.11.3",
        ("framework_protocol",): "cotend-collaboration-v1.52",
        ("model_upgrade_packet_family",): "cotend-model-upgrade-v1.7",
        ("source_release", "tag"): "dual-ai-share-2026.07.11.3",
        ("source_release", "tag_object"): "cef8add414a6d9704d3f58785a128bc56f44b263",
        ("source_release", "release_commit"): "71e45d9ebeff4d9d61c180711c25267b9fe31549",
        ("source_release", "package_tree"): "a70231e0445d9795a00212e8e6c53c149bfbc431",
        ("source_release", "manifest_sha256"): (
            "919fe34254b51619ddca1d010445281d4f7ceec958ee8cfd1958eaccb02bd006"
        ),
        ("target_platform",): "Codex",
        ("source_carrier",): "skills/",
        ("skill_count",): 7,
        ("skill_file_count",): 30,
        ("capability_map",): "upstream/CAPABILITY-IMPLEMENTATION-MAP.json",
        ("adoption_record",): (
            "upstream/FRAMEWORK-ADOPTION-LOG.md#release-2026-07-11-3-initial-adoption"
        ),
        ("delivery_boundaries", "repository_source_adopted"): True,
        ("delivery_boundaries", "live_install_performed"): False,
        ("delivery_boundaries", "plugin_or_marketplace_carrier"): (
            "github_root_candidate_local_verified"
        ),
        ("delivery_boundaries", "claude_carrier"): "deferred",
        ("delivery_boundaries", "push_release_or_publish"): "not_performed",
    }
    for keys, expected in expected_lock_values.items():
        if value(framework_lock, *keys) != expected:
            errors.append(f"framework lock mismatch: {'.'.join(keys)}")
    if framework_lock.get("source_skill_trees") != expected_skill_trees:
        errors.append("framework lock source Skill tree inventory drift")
    if framework_lock.get("adoption_anchor") != {
        "type": "containing_commit",
        "path": "upstream/framework.lock.json",
    }:
        errors.append("framework lock containing-commit anchor mismatch")
    for forbidden_key in ("adoption_commit", "resulting_commit", "containing_commit_hash"):
        if forbidden_key in framework_lock:
            errors.append(f"framework lock must not embed its own commit hash: {forbidden_key}")

    lock_mappings = framework_lock.get("skill_mapping")
    if not isinstance(lock_mappings, list):
        errors.append("framework lock Skill mapping is invalid")
    else:
        lock_by_source = {
            item.get("source"): item for item in lock_mappings if isinstance(item, dict)
        }
        for source_id, expected in expected_roles.items():
            item = lock_by_source.get(source_id)
            if item is None:
                errors.append(f"framework lock Skill mapping is missing: {source_id}")
                continue
            expected_disposition = expected[2]
            expected_mode = expected[3]
            expected_target = expected[4]
            if (
                item.get("target"),
                item.get("disposition"),
                item.get("implementation_mode"),
            ) != (expected_target, expected_disposition, expected_mode):
                errors.append(f"framework lock Skill mapping drift: {source_id}")
        if (
            len(lock_mappings) != 7
            or len(lock_by_source) != 7
            or set(lock_by_source) != set(expected_roles)
        ):
            errors.append("framework lock must map exactly seven source Skills")

    for marker in (
        "## release-2026-07-11-3-initial-adoption",
        "status: adopted_verified",
        "resulting_CoTend_commit: containing_commit",
        "live_install_performed: false",
        "7 个 Skill、30 个文件",
    ):
        if marker not in adoption_log_text:
            errors.append(f"framework adoption log is missing: {marker}")

    return errors


def local_recovery_truth_errors(status_text: str, plan_text: str) -> list[str]:
    errors: list[str] = []

    exact_status = {
        "productization_default": {"rename_first_preserve_first"},
        "framework_release_candidate": {"dual_ai_share_2026_07_11_3"},
        "framework_release_adoption": {"adopted_verified_repository_source"},
        "interface_authority": {
            "codex_project_carrier_validated_live_delivery_pending"
        },
    }
    for key, expected in exact_status.items():
        if metadata_values(status_text, key) != expected:
            errors.append(f"local STATUS productization truth mismatch: {key}")

    exact_plan = {
        "productization_default": {"rename_first_preserve_first"},
    }
    for key, expected in exact_plan.items():
        if metadata_values(plan_text, key) != expected:
            errors.append(f"local plan productization truth mismatch: {key}")

    status_leaves = metadata_values(status_text, "current_next_leaf")
    plan_leaves = metadata_values(plan_text, "current_next_leaf")
    active_nodes = metadata_values(plan_text, "active_node")
    if len(status_leaves) != 1 or status_leaves != plan_leaves:
        errors.append(
            f"local active leaf drift: STATUS={sorted(status_leaves)} "
            f"PLAN={sorted(plan_leaves)}"
        )
        return errors
    if active_nodes != plan_leaves:
        errors.append(
            f"local active node drift: NODE={sorted(active_nodes)} "
            f"LEAF={sorted(plan_leaves)}"
        )
        return errors

    current_leaf = next(iter(plan_leaves))
    active_leaf_path = ROOT / "PROJECT-PLAN-NODES" / f"{current_leaf}.md"
    if not active_leaf_path.exists():
        errors.append(f"local active leaf document is missing: {current_leaf}")
        return errors
    active_leaf_text = active_leaf_path.read_text(encoding="utf-8")
    if metadata_values(active_leaf_text, "route_state") != {"active"}:
        errors.append(f"local active leaf route state is not active: {current_leaf}")

    governing_decisions = metadata_values(plan_text, "governing_decision")
    activation_decisions = metadata_values(active_leaf_text, "activation_decision")
    if len(governing_decisions) != 1 or governing_decisions != activation_decisions:
        errors.append("local plan governing decision does not match active leaf activation")

    current_stages = metadata_values(plan_text, "current_stage")
    if len(current_stages) != 1:
        errors.append(f"local plan must identify one current stage: {sorted(current_stages)}")
        return errors
    current_stage = next(iter(current_stages))
    stage_path = ROOT / "PROJECT-PLAN-NODES" / f"{current_stage}.md"
    if not stage_path.exists():
        errors.append(f"local current stage document is missing: {current_stage}")
        return errors
    stage_text = stage_path.read_text(encoding="utf-8")
    if metadata_values(stage_text, "active_leaf") != plan_leaves:
        errors.append("local current stage does not point to the plan's active leaf")

    understanding_match = re.search(
        r"^\s*expanded:\s*(\S+)\s*$", stage_text, re.MULTILINE
    )
    if understanding_match is None:
        errors.append("local current stage lacks an expanded understanding link")
        return errors
    understanding_path = ROOT / understanding_match.group(1)
    if not understanding_path.exists():
        errors.append("local current-stage understanding document is missing")
        return errors
    understanding_text = understanding_path.read_text(encoding="utf-8")
    understanding_leaves = metadata_values(understanding_text, "current_leaf")
    if understanding_leaves and understanding_leaves != plan_leaves:
        errors.append("local current-stage understanding points to a different active leaf")

    return errors


def isolated_codex_carrier_errors(
    evidence_text: str,
    adoption_log_text: str,
    framework_eval_text: str,
    candidates: set[str],
) -> list[str]:
    errors: list[str] = []
    fixture_root = "tests/fixtures/codex-carrier"
    expected_paths = {
        f"{fixture_root}/{path}" for path in EXPECTED_CODEX_CARRIER_FIXTURE_FILES
    }
    if "scripts/verify_isolated_codex_carrier.py" not in candidates:
        errors.append("isolated Codex carrier verifier is missing or ignored")
    else:
        verifier_text = read("scripts/verify_isolated_codex_carrier.py")
        for marker in (
            'EXTERNAL_RUNTIME_PREFIX = "cotend-L21-runtime-"',
            "create_external_runtime_copy",
            "guarded_external_runtime_root",
            "parent_repository_context_inherited",
            "process.stdin.close()",
        ):
            if marker not in verifier_text:
                errors.append(f"isolated Codex carrier isolation is missing: {marker}")
    missing_paths = expected_paths - candidates
    if missing_paths:
        errors.append(
            f"isolated Codex carrier fixture files are missing: {sorted(missing_paths)}"
        )
    actual_paths = {
        path for path in candidates if path.startswith(f"{fixture_root}/")
    }
    if actual_paths != expected_paths:
        errors.append("isolated Codex carrier fixture inventory drift")

    combined_evidence = evidence_text + adoption_log_text
    for marker in (
        "status: passed_with_scope_limitations",
        "codex_cli: 0.142.0",
        "project_skill_carrier: .agents/skills",
        "fixture_skill_count: 7",
        "fixture_skill_file_count: 30",
        "live_scenario_count: 3",
        "negative_mutation_count: 4",
        "cli_boundary_negative_count: 3",
        "desktop_skill_selector_verified: false",
        "implicit_natural_language_trigger_verified: false",
        "passed_3_of_3",
        "passed_4_of_4",
        "passed_7_of_7_with_PYTHONUTF8",
        "父仓库根 Marketplace 上下文不继承",
        "CODEX_SKILL_DISCOVERY_OK version=codex-cli_0.144.1 repo_skills=7",
        "1024",
    ):
        if marker not in combined_evidence:
            errors.append(f"isolated Codex carrier evidence is missing: {marker}")

    scenario_path = ROOT / fixture_root / "live-scenarios.json"
    if scenario_path.is_file():
        try:
            scenarios = json.loads(scenario_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"isolated Codex live scenarios are invalid JSON: {exc}")
            scenarios = []
        scenario_ids = {
            item.get("id") for item in scenarios if isinstance(item, dict)
        }
        if scenario_ids != {"init-delegation", "pending-decision", "diagnose-only"}:
            errors.append("isolated Codex live scenario set drift")
        if len(scenarios) != 3:
            errors.append("isolated Codex carrier must define exactly three live scenarios")

    for skill in (
        "cotend-init",
        "cotend-project-init",
        "cotend-collaboration",
        "cotend-diagnose-only",
        "cotend-model-upgrade",
    ):
        agent_path = ROOT / "skills" / skill / "agents" / "openai.yaml"
        if not agent_path.is_file():
            errors.append(f"Codex agent metadata is missing: {skill}")
            continue
        prompt = re.search(
            r'^\s*default_prompt:\s*"(.+)"\s*$',
            agent_path.read_text(encoding="utf-8"),
            re.MULTILINE,
        )
        if prompt is None or len(prompt.group(1)) > 1024:
            errors.append(f"Codex default prompt limit mismatch: {skill}")

    if (
        "skills_list_7_of_7_and_three_read_only_explicit_scenarios_passed"
        not in framework_eval_text
    ):
        errors.append("framework evaluation lacks isolated Codex carrier result")
    if "framework_lock_changed: false" not in adoption_log_text:
        errors.append("adoption log lacks carrier lock boundary")
    return errors


def isolated_codex_plugin_fixture_errors(
    evidence_text: str,
    candidates: set[str],
) -> list[str]:
    errors: list[str] = []
    missing = EXPECTED_PLUGIN_FIXTURE_FILES - candidates
    if missing:
        errors.append(f"isolated Codex Plugin artifacts are missing: {sorted(missing)}")
        return errors

    verifier_text = read("scripts/verify_isolated_codex_plugin.py")
    for marker in (
        'PLUGIN_VERSION = "0.0.0-dev.1+codex.fixture"',
        "EXPECTED_FILE_COUNT = 30",
        '"--phase-a"',
        '"--negative-mutations"',
        '"remote_plugin"',
        "protected_user_snapshot",
        "validate_isolated_env",
        "validate_plugin_list_payload",
        "run_negative_mutations",
    ):
        if marker not in verifier_text:
            errors.append(f"isolated Codex Plugin verifier is missing: {marker}")

    test_text = read("tests/test_isolated_codex_plugin.py")
    actual_tests = set(re.findall(r"^\s+def (test_[a-z0-9_]+)\(", test_text, re.MULTILINE))
    missing_tests = EXPECTED_PLUGIN_FIXTURE_TESTS - actual_tests
    if missing_tests:
        errors.append(
            f"isolated Codex Plugin tests are missing: {sorted(missing_tests)}"
        )

    for key, expected in {
        "status": {"passed_isolated_fixture_phase_a"},
        "evidence_type": {"executed"},
        "codex_version": {"codex-cli_0.144.1"},
        "fixture_version": {"0.0.0-dev.1+codex.fixture"},
        "plugin_identity_authority": {"fixture_only_not_release"},
        "phase_a_steps": {"17"},
        "negative_cases": {"12"},
        "adopted_skills": {"7"},
        "adopted_skill_files": {"30"},
        "package_files": {"36"},
        "protected_user_metadata": {"unchanged_stat_only"},
        "tracked_production_plugin": {"none"},
    }.items():
        if metadata_values(evidence_text, key) != expected:
            errors.append(f"isolated Codex Plugin evidence mismatch: {key}")

    for marker in (
        "15 个写入根全部解析到 ignored fixture",
        "官方 Plugin validator：`passed`",
        "Plugin package：36 个文件",
        "实际执行并通过以下 17 步",
        "cotend:cotend-init",
        "Plugin 入口的实际 scope 为 `user`",
        "7 个原名 `repo` scope 入口同时可见",
        "以下 12 类变异全部",
        "local cachebuster update",
        "Public Plugins Directory submission",
        "ISOLATED_CODEX_PLUGIN_PHASE_A_OK steps=17",
    ):
        if marker not in evidence_text:
            errors.append(f"isolated Codex Plugin evidence is missing: {marker}")

    tracked_plugin_manifests = sorted(
        path
        for path in candidates
        if path.endswith("/.codex-plugin/plugin.json")
        or path == ".codex-plugin/plugin.json"
    )
    allowed_later_candidate = {
        ".codex-plugin/plugin.json",
        "packaging/codex-plugin/cotend/.codex-plugin/plugin.json"
    }
    unexpected_manifests = sorted(
        set(tracked_plugin_manifests) - allowed_later_candidate
    )
    if unexpected_manifests:
        errors.append(
            "fixture history found an unexpected tracked Plugin manifest: "
            f"{unexpected_manifests}"
        )
    return errors


def plugin_namespace_candidate_errors(
    evidence_text: str,
    evaluation_text: str,
    desktop_text: str,
    candidates: set[str],
) -> list[str]:
    errors: list[str] = []
    missing = EXPECTED_PLUGIN_NAMESPACE_FILES - candidates
    if missing:
        errors.append(
            f"Plugin namespace evaluation artifacts are missing: {sorted(missing)}"
        )
        return errors

    verifier_text = read("scripts/evaluate_plugin_namespace_candidates.py")
    for marker in (
        'version="0.0.0-dev.2+codex.namespace-preserve"',
        'version="0.0.0-dev.2+codex.namespace-short"',
        "SHORT_NAME_MAP",
        "VOLATILE_CONTAINER_LABELS",
        "assert_protected_product_state_unchanged",
        "verify_candidate_isolation",
        "validate_plugin_remove",
        "validate_marketplace_remove",
        "display_led_overlay",
        "--prepare and --execute are both required",
        "residual_migration_review_required",
    ):
        if marker not in verifier_text:
            errors.append(f"Plugin namespace verifier is missing: {marker}")

    test_text = read("tests/test_plugin_namespace_candidates.py")
    actual_tests = set(
        re.findall(r"^\s+def (test_[a-z0-9_]+)\(", test_text, re.MULTILINE)
    )
    missing_tests = EXPECTED_PLUGIN_NAMESPACE_TESTS - actual_tests
    if missing_tests:
        errors.append(
            f"Plugin namespace tests are missing: {sorted(missing_tests)}"
        )

    for key, expected in {
        "status": {"passed_two_physical_candidates"},
        "evidence_type": {"executed_with_bounded_inspection"},
        "codex_version": {"codex-cli_0.144.1"},
        "physical_candidates": {"2"},
        "metadata_overlays": {"1"},
        "source_identifier_occurrences": {"77"},
        "source_identifier_files": {"15"},
        "isolated_write_roots_per_candidate": {"15"},
        "lifecycle_steps_per_candidate": {"10"},
        "adopted_skills": {"7"},
        "adopted_skill_files": {"30"},
        "package_files_per_candidate": {"36"},
        "tracked_production_plugin": {"none"},
        "final_namespace_authority": {
            "candidate_baseline_confirmed_final_namespace_pending"
        },
        "subsequent_desktop_picker_evidence": {"passed_partial"},
        "desktop_picker_query": {"/cotend"},
        "desktop_hot_update_verified": {"false"},
        "desktop_new_task_refresh_verified": {"true"},
        "desktop_visible_entry_count": {"7"},
        "desktop_non_sending_chip_verified": {"true"},
        "desktop_interaction_verified": {"partial"},
        "model_behavior_verified": {"false"},
    }.items():
        if metadata_values(evidence_text, key) != expected:
            errors.append(f"Plugin namespace evidence mismatch: {key}")

    for marker in (
        "15 个源文件中共出现 77 次",
        "N1-preserve",
        "cotend:cotend-init",
        "移动路径：0；改写字节文件：0",
        "N2-short",
        "cotend:init",
        "28 个文件路径移动、10 个文件字节变化",
        "逐字节差异只包含这 10 次预期字符串替换",
        "仍有 67 处原 ID",
        "仍有 60 处需要语义复核",
        "N3-display-led",
        "增加的 package bytes 为 0",
        "当时 Desktop 和自然语言行为为 `not_run`",
        "后续 Desktop picker 实证",
        "混用造成的无效假阴性",
        "同一已打开任务不可见",
        "fresh app-server 发现 7 项",
        "b83b2bccccb3894cd6d5bd09ff6521b9358b0ac4c7b0c9169dad3be88c2af76a",
        "最终两个隔离环境中均没有已安装 Plugin",
        "PLUGIN_NAMESPACE_EVALUATION_OK physical_candidates=2",
    ):
        if marker not in evidence_text:
            errors.append(f"Plugin namespace evidence is missing: {marker}")

    for key, expected in {
        "status": {
            "user_confirmed_candidate_baseline_with_new_task_picker_and_chip_evidence"
        },
        "recommendation": {"N3_display_led_preserve_first"},
        "candidate_baseline_confirmed": {"true"},
        "production_namespace_confirmed": {"false"},
        "production_package_authorized": {"candidate_contract_only"},
        "desktop_surface_verified": {"partial_picker_and_non_sending_chip"},
        "desktop_hot_update_verified": {"false"},
        "desktop_new_task_refresh_verified": {"true"},
        "desktop_visible_entry_count": {"7"},
        "desktop_non_sending_chip_verified": {"true"},
        "desktop_interaction_verified": {"partial"},
        "model_behavior_verified": {"false"},
        "shared_behavior_change_authorized": {"false"},
    }.items():
        if metadata_values(evaluation_text, key) != expected:
            errors.append(f"Plugin namespace evaluation mismatch: {key}")

    for marker in (
        "N3 display-led preserve-first",
        "不是最终 namespace 定案",
        "错误语法造成的假阴性",
        "当前任务热更新未通过",
        "打开新任务或执行等价 Skill 快照刷新",
        "截图内没有出现 canonical 双前缀",
        "上游变更提案",
        "N2 的 validator 与 discovery 通过不能升级为",
        "用户确认后的状态",
    ):
        if marker not in evaluation_text:
            errors.append(f"Plugin namespace evaluation is missing: {marker}")

    for key, expected in {
        "status": {
            "passed_new_task_picker_and_non_sending_chip_with_refresh_boundary"
        },
        "evidence_type": {
            "controlled_live_lifecycle_plus_fresh_discovery_and_user_screenshot_inspection"
        },
        "candidate_id": {"N3-display-led"},
        "desktop_picker_query": {"/cotend"},
        "desktop_hot_update_verified": {"false"},
        "desktop_new_task_refresh_verified": {"true"},
        "desktop_refresh_contract_candidate": {
            "new_task_or_equivalent_skill_snapshot_refresh"
        },
        "fresh_app_server_entry_count": {"7"},
        "visible_entry_count": {"7"},
        "user_owned_friendly_display_names": {"5"},
        "companion_platform_prefixed_display_names": {"2"},
        "non_sending_chip_insertion_verified": {"true"},
        "chip_display_name": {"CoTend_Init"},
        "canonical_chip_visible": {"false"},
        "desktop_interaction_verified": {
            "partial_picker_and_non_sending_chip"
        },
        "model_behavior_verified": {"false"},
        "candidate_cleanup_verified": {"true"},
        "production_namespace_confirmed": {"false"},
        "production_package_authorized": {"false"},
        "screenshot_tracked": {"false"},
    }.items():
        if metadata_values(desktop_text, key) != expected:
            errors.append(f"Desktop Plugin surface evidence mismatch: {key}")

    for marker in (
        "Desktop Skill 选择器的正确查询是 `/cotend`",
        "`$skill-name` 是提示词中的显式 Skill 调用语法",
        "当前证据**不支持**“已打开任务可靠热更新”",
        "同一已打开任务查询 `/cotend`",
        "fresh `skills/list(forceReload=true)`",
        "打开新任务或执行等价 Skill 快照刷新",
        "d1d86970344e892d40b60a21a22a9df11f9f6ba4c5004ecd44d63594a4680314",
        "b83b2bccccb3894cd6d5bd09ff6521b9358b0ac4c7b0c9169dad3be88c2af76a",
        "`Cotend: Grill Me`",
        "`CoTend Init`",
        "`Cotend: Karpathy Guidelines`",
        "`CoTend Project Init`",
        "`CoTend Collaboration`",
        "`CoTend Diagnose Only`",
        "`CoTend Model Upgrade`",
        "`CoTend Init` 友好 chip",
        "9 个 Plugin、3 个 Marketplace",
        "消息发送与模型调用",
        "原始截图只保留在本地证据环境",
        "详情页字段和 canonical name",
        "N3 display-led preserve-first 继续作为 production-package 候选基线",
    ):
        if marker not in desktop_text:
            errors.append(f"Desktop Plugin surface evidence is missing: {marker}")
    return errors


def production_plugin_package_errors(
    evidence_text: str,
    candidates: set[str],
) -> list[str]:
    errors: list[str] = []
    missing = EXPECTED_PLUGIN_PACKAGE_FILES - candidates
    if missing:
        errors.append(f"production Plugin package artifacts are missing: {sorted(missing)}")
        return errors

    expected_manifest_path = (
        "packaging/codex-plugin/cotend/.codex-plugin/plugin.json"
    )
    tracked_plugin_manifests = sorted(
        path
        for path in candidates
        if path.endswith("/.codex-plugin/plugin.json")
        or path == ".codex-plugin/plugin.json"
    )
    if tracked_plugin_manifests != [
        ".codex-plugin/plugin.json",
        expected_manifest_path,
    ]:
        errors.append(
            "production Plugin manifest inventory mismatch: "
            f"{tracked_plugin_manifests}"
        )

    try:
        manifest = json.loads(read(expected_manifest_path))
        package_lock = json.loads(read("packaging/codex-plugin/package.lock.json"))
    except (json.JSONDecodeError, OSError):
        errors.append("production Plugin manifest or package lock is invalid JSON")
        return errors
    if not isinstance(manifest, dict) or not isinstance(package_lock, dict):
        errors.append("production Plugin manifest and package lock must be objects")
        return errors

    for key, expected in {
        "name": "cotend",
        "version": "0.1.0-rc.1",
        "skills": "./skills/",
        "license": "Apache-2.0",
    }.items():
        if manifest.get(key) != expected:
            errors.append(f"production Plugin manifest mismatch: {key}")
    for forbidden in ("apps", "mcpServers", "hooks"):
        if forbidden in manifest:
            errors.append(f"production Plugin manifest declares forbidden {forbidden}")
    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        errors.append("production Plugin manifest interface is missing")
    else:
        if interface.get("displayName") != "CoTend":
            errors.append("production Plugin display name mismatch")
        if interface.get("brandColor") != "#139C98":
            errors.append("production Plugin brand color mismatch")
        if interface.get("composerIcon") != "./assets/cotend-logo.png":
            errors.append("production Plugin composer icon mismatch")
        if interface.get("logo") != "./assets/cotend-logo.png":
            errors.append("production Plugin logo mismatch")
        if interface.get("logoDark") != "./assets/cotend-logo-dark.png":
            errors.append("production Plugin dark logo mismatch")
        prompts = interface.get("defaultPrompt")
        if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3:
            errors.append("production Plugin starter prompt count mismatch")
        elif any(not isinstance(prompt, str) or len(prompt) > 128 for prompt in prompts):
            errors.append("production Plugin starter prompt length mismatch")

    manifest_hash = hashlib.sha256(
        (ROOT / expected_manifest_path).read_bytes()
    ).hexdigest()
    plugin_lock = package_lock.get("plugin")
    source_lock = package_lock.get("source")
    output_lock = package_lock.get("package")
    authority = package_lock.get("authority")
    if package_lock.get("status") != "production_candidate_not_published":
        errors.append("production Plugin package status must remain candidate-only")
    if package_lock.get("schema_version") != 2:
        errors.append("production Plugin package lock schema mismatch")
    if not isinstance(plugin_lock, dict) or plugin_lock.get("manifest_sha256") != manifest_hash:
        errors.append("production Plugin manifest hash lock mismatch")
    if not isinstance(source_lock, dict) or source_lock.get(
        "path_hash_manifest_sha256"
    ) != "acbd6d6668d0e8fc34ea7585db5c758cc09a9ea08756f7a52b84f4a5b841ba1b":
        errors.append("production Plugin source manifest lock mismatch")
    if not isinstance(output_lock, dict) or output_lock.get(
        "path_hash_manifest_sha256"
    ) != "18f0b62852ebe1f7afbd43bcbff50706aacd1d66ae6edeb4c5b133d53fdd858f":
        errors.append("production Plugin package digest lock mismatch")
    if not isinstance(output_lock, dict) or output_lock.get("file_count") != 41:
        errors.append("production Plugin package file count mismatch")
    expected_brand_assets = [
        {
            "path": "assets/cotend-mark.svg",
            "role": "canonical_light_source",
            "sha256": "27c5a8566bb4d7800f9250715aef649adf5806b35784955a093cc37cf477238a",
        },
        {
            "path": "assets/cotend-mark-dark.svg",
            "role": "canonical_dark_source",
            "sha256": "63e1f28fee998a7d3a7d39a381d2990132ed5f9c63a70a10fd533ef2dbb1afac",
        },
        {
            "path": "assets/cotend-logo.png",
            "role": "composer_icon_and_light_logo",
            "sha256": "3a39de1b6c956b37a5e6efc0fb616a06104ce9d9417d3157ab5c5a002af72d49",
        },
        {
            "path": "assets/cotend-logo-dark.png",
            "role": "dark_logo",
            "sha256": "dc495bcbdba3c35f32e60a7f4d250593007de3e5620431f3b780d98a5e4c46fe",
        },
    ]
    if not isinstance(output_lock, dict) or output_lock.get(
        "brand_assets"
    ) != expected_brand_assets:
        errors.append("production Plugin brand asset lock mismatch")
    if authority != {
        "candidate_identity_only": False,
        "final_plugin_identity_confirmed": True,
        "release_or_publish_authorized": False,
    }:
        errors.append("production Plugin package authority boundary drifted")

    builder_text = read("scripts/build_codex_plugin.py")
    for marker in (
        'PLUGIN_VERSION = "0.1.0-rc.1"',
        'ALLOWED_OUTPUT_ROOTS = {".private-provenance", "dist"}',
        "expected_package_manifest",
        "PACKAGE_BRAND_ASSETS",
        "validate_brand_assets",
        "source_bytes_identical",
        "existing output is not an owned valid CoTend package",
        "run_official_validator",
    ):
        if marker not in builder_text:
            errors.append(f"production Plugin builder is missing: {marker}")
    attributes_text = read(".gitattributes")
    for marker in (
        "/skills/** text eol=lf",
        "/LICENSE text eol=lf",
        "/NOTICE text eol=lf",
        "/THIRD-PARTY-NOTICES.md text eol=lf",
        "/THIRD-PARTY-SOURCES.json text eol=lf",
        "/packaging/codex-plugin/cotend/.codex-plugin/plugin.json text eol=lf",
        "/packaging/codex-plugin/cotend/assets/*.svg text eol=lf",
        "/packaging/codex-plugin/cotend/assets/*.png binary",
        "/packaging/codex-plugin/package.lock.json text eol=lf",
    ):
        if marker not in attributes_text:
            errors.append(f"production Plugin LF contract is missing: {marker}")
    if "/dist/" not in read(".gitignore"):
        errors.append("generated production Plugin dist/ output must remain gitignored")
    verifier_text = read("scripts/verify_codex_plugin_package.py")
    for marker in (
        "NEGATIVE_CASES = 17",
        "protected_boundaries",
        "CODEX_PLUGIN_PRODUCTION_PACKAGE_OK",
        "plugin_installation\": \"not_run",
        "marketplace_write\": \"not_run",
    ):
        if marker not in verifier_text:
            errors.append(f"production Plugin verifier is missing: {marker}")

    test_text = read("tests/test_codex_plugin_package.py")
    actual_tests = set(
        re.findall(r"^\s+def (test_[a-z0-9_]+)\(", test_text, re.MULTILINE)
    )
    missing_tests = EXPECTED_PLUGIN_PACKAGE_TESTS - actual_tests
    if missing_tests:
        errors.append(f"production Plugin package tests are missing: {sorted(missing_tests)}")

    for key, expected in {
        "status": {"passed_isolated_production_candidate_contract"},
        "evidence_type": {"executed"},
        "codex_version": {"codex-cli_0.144.1"},
        "candidate_plugin_id": {"cotend"},
        "candidate_version": {"0.1.0-rc.1"},
        "identity_authority": {"initial_submission_identity_confirmed_not_release"},
        "semantic_sources": {"1"},
        "isolated_builds_compared": {"2"},
        "package_files": {"41"},
        "brand_assets": {"4"},
        "adopted_skills": {"7"},
        "adopted_skill_files": {"30"},
        "friendly_display_names": {"5"},
        "negative_cases": {"17"},
        "protected_user_boundaries": {"6"},
        "official_validator": {"passed"},
        "marketplace_write": {"false"},
        "plugin_installation": {"false"},
        "release_or_publish": {"false"},
        "final_plugin_identity_confirmed": {"true"},
    }.items():
        if metadata_values(evidence_text, key) != expected:
            errors.append(f"production Plugin package evidence mismatch: {key}")
    for marker in (
        "`skills/` 仍是唯一语义源",
        "41 个文件",
        "逐字节一致",
        "17 类负向边界",
        "当前 Plugin Creator validator：`passed`",
        "没有生成 Marketplace",
        "不代表已经满足公开 submission",
        "CODEX_PLUGIN_PRODUCTION_PACKAGE_OK builds=2 files=41",
    ):
        if marker not in evidence_text:
            errors.append(f"production Plugin package evidence is missing: {marker}")

    tracked_marketplaces = sorted(
        path for path in candidates if path.endswith("/.agents/plugins/marketplace.json")
    )
    if tracked_marketplaces:
        errors.append(f"production package must not track Marketplace files: {tracked_marketplaces}")
    duplicate_packaged_skills = sorted(
        path
        for path in candidates
        if path.startswith("packaging/codex-plugin/") and "/skills/" in path
    )
    if duplicate_packaged_skills:
        errors.append("production package must not track a second Skill source tree")
    return errors


def production_plugin_lifecycle_errors(
    evidence_text: str,
    candidates: set[str],
) -> list[str]:
    errors: list[str] = []
    missing = EXPECTED_PLUGIN_LIFECYCLE_FILES - candidates
    if missing:
        errors.append(
            f"production Plugin lifecycle artifacts are missing: {sorted(missing)}"
        )
        return errors

    verifier_text = read("scripts/verify_production_plugin_lifecycle.py")
    for marker in (
        'MARKETPLACE_NAME = "cotend-production-candidate-local"',
        "PRODUCTION_IDENTITY = lifecycle.PluginLifecycleIdentity",
        "package.build_package(plugin_root)",
        "package.verify_package(plugin_root)",
        'fail_after_step="plugin_add"',
        "recover_after_injected_failure",
        "purge_isolated_write_roots",
        'EXTERNAL_PROJECT_PREFIX = "cotend-L46-projects-"',
        "owned_external_system_temp_root",
        "projects_root=projects_root",
        "protected_user_snapshot",
        "PRODUCTION_PLUGIN_LIFECYCLE_OK",
        "real_user_plugin_or_marketplace_write",
    ):
        if marker not in verifier_text:
            errors.append(f"production Plugin lifecycle verifier is missing: {marker}")

    fixture_text = read("scripts/verify_isolated_codex_plugin.py")
    for marker in (
        "class PluginLifecycleIdentity",
        "FIXTURE_LIFECYCLE_IDENTITY = PluginLifecycleIdentity",
        "identity: PluginLifecycleIdentity = FIXTURE_LIFECYCLE_IDENTITY",
        "process.stdin.close()",
        "injected lifecycle failure after",
    ):
        if marker not in fixture_text:
            errors.append(f"shared Plugin lifecycle harness is missing: {marker}")

    test_text = read("tests/test_production_plugin_lifecycle.py")
    actual_tests = set(
        re.findall(r"^\s+def (test_[a-z0-9_]+)\(", test_text, re.MULTILINE)
    )
    missing_tests = EXPECTED_PLUGIN_LIFECYCLE_TESTS - actual_tests
    if missing_tests:
        errors.append(
            f"production Plugin lifecycle tests are missing: {sorted(missing_tests)}"
        )

    for key, expected in {
        "status": {"passed_isolated_production_plugin_lifecycle"},
        "evidence_type": {"executed"},
        "codex_version": {"codex-cli_0.144.1"},
        "candidate_plugin_id": {"cotend"},
        "candidate_version": {"0.1.0-rc.1"},
        "identity_authority": {"initial_submission_identity_confirmed_not_release"},
        "package_files": {"41"},
        "adopted_skills": {"7"},
        "adopted_skill_files": {"30"},
        "normal_lifecycle_steps": {"17"},
        "failure_recovery_steps": {"5"},
        "installed_plugin_skills": {"7"},
        "coexistence_standalone_skills": {"7"},
        "write_roots_redirected": {"15"},
        "protected_user_boundaries": {"8"},
        "runtime_write_roots_purged": {"true"},
        "final_plugin_installed": {"false"},
        "final_marketplace_configured": {"false"},
        "real_user_plugin_or_marketplace_write": {"false"},
        "official_validator": {"passed"},
        "release_or_publish": {"false"},
    }.items():
        if metadata_values(evidence_text, key) != expected:
            errors.append(f"production Plugin lifecycle evidence mismatch: {key}")

    for marker in (
        "精确 `cotend@0.1.0-rc.1` 41 文件生产候选",
        "正常场景完成 17 步",
        "完成 5 步恢复",
        "15 个隔离运行时写入根均被清除",
        "带 `cotend-L46-projects-` 固定前缀的独立根",
        "真实用户边界只做 stat-only 元数据快照",
        "该次运行没有被接受为证据",
        "不把隔离 lifecycle 表述成已经上架",
        "PRODUCTION_PLUGIN_LIFECYCLE_OK version=0.1.0-rc.1 files=41",
    ):
        if marker not in evidence_text:
            errors.append(f"production Plugin lifecycle evidence is missing: {marker}")

    tracked_marketplaces = sorted(
        path for path in candidates if path.endswith("/.agents/plugins/marketplace.json")
    )
    if tracked_marketplaces:
        errors.append(
            "production Plugin lifecycle must not track Marketplace files: "
            f"{tracked_marketplaces}"
        )
    return errors


def github_marketplace_root_carrier_errors(
    evidence_text: str,
    candidates: set[str],
) -> list[str]:
    errors: list[str] = []
    missing = EXPECTED_GITHUB_MARKETPLACE_CARRIER_FILES - candidates
    if missing:
        errors.append(
            "GitHub Marketplace root-carrier artifacts are missing: "
            f"{sorted(missing)}"
        )
        return errors

    try:
        root_manifest = json.loads(read(".codex-plugin/plugin.json"))
        production_manifest = json.loads(
            read("packaging/codex-plugin/cotend/.codex-plugin/plugin.json")
        )
        marketplace = json.loads(read(".agents/plugins/marketplace.json"))
    except (json.JSONDecodeError, OSError) as exc:
        return [f"GitHub Marketplace root-carrier JSON is invalid: {exc}"]
    if not isinstance(root_manifest, dict) or not isinstance(
        production_manifest, dict
    ):
        return ["GitHub Marketplace Plugin manifests must be objects"]

    expected_root = json.loads(json.dumps(production_manifest))
    expected_interface = expected_root.get("interface")
    if not isinstance(expected_interface, dict):
        errors.append("production Plugin interface is invalid for root derivation")
    else:
        expected_interface.update(
            {
                "composerIcon": (
                    "./packaging/codex-plugin/cotend/assets/cotend-logo.png"
                ),
                "logo": "./packaging/codex-plugin/cotend/assets/cotend-logo.png",
                "logoDark": (
                    "./packaging/codex-plugin/cotend/assets/cotend-logo-dark.png"
                ),
            }
        )
        if root_manifest != expected_root:
            errors.append(
                "root Plugin manifest must be the exact three-path production transform"
            )

    expected_marketplace = {
        "name": "cotend",
        "interface": {"displayName": "CoTend"},
        "plugins": [
            {
                "name": "cotend",
                "source": {"source": "url", "url": "./"},
                "policy": {
                    "installation": "AVAILABLE",
                    "authentication": "ON_INSTALL",
                },
                "category": "Developer Tools",
            }
        ],
    }
    if marketplace != expected_marketplace:
        errors.append("root Marketplace manifest drifted from the repository-root contract")

    tracked_marketplaces = sorted(
        path
        for path in candidates
        if path == ".agents/plugins/marketplace.json"
        or path.endswith("/.agents/plugins/marketplace.json")
    )
    if tracked_marketplaces != [".agents/plugins/marketplace.json"]:
        errors.append(
            "tracked Marketplace inventory mismatch: " f"{tracked_marketplaces}"
        )
    source_files = sorted(path for path in candidates if path.startswith("skills/"))
    if len(source_files) != 30:
        errors.append(f"root Marketplace Skill source count drifted: {len(source_files)}")
    if any(path.startswith("codex-skills/") for path in candidates):
        errors.append("legacy codex-skills source must not coexist with root skills")
    if any((ROOT / path).is_symlink() for path in source_files):
        errors.append("root Marketplace Skill source must not contain symlinks")

    verifier_text = read("scripts/verify_github_marketplace_carrier.py")
    for marker in (
        'EXTERNAL_PROJECT_PREFIX = "cotend-L54-projects-"',
        "POST_PUSH_NOT_RUN",
        "run_official_validator",
        "initialize_fixture_git_repository",
        "wait_for_protected_quiet_window",
        "lifecycle.protected_user_snapshot()",
        "lifecycle.WRITE_ROOT_ENV_KEYS",
        "local_marketplace_not_git_upgradeable",
        "remove_tree_with_readonly_retry",
        "remove_external_project_root",
        "external_project_handle_release_retries",
        "GITHUB_MARKETPLACE_CARRIER_OK",
    ):
        if marker not in verifier_text:
            errors.append(f"GitHub Marketplace verifier is missing: {marker}")

    test_text = read("tests/test_github_marketplace_carrier.py")
    actual_tests = set(
        re.findall(r"^\s+def (test_[a-z0-9_]+)\(", test_text, re.MULTILINE)
    )
    missing_tests = EXPECTED_GITHUB_MARKETPLACE_CARRIER_TESTS - actual_tests
    if missing_tests:
        errors.append(
            "GitHub Marketplace root-carrier tests are missing: "
            f"{sorted(missing_tests)}"
        )

    for key, expected in {
        "status": {"passed_isolated_github_marketplace_root_carrier"},
        "evidence_type": {"executed"},
        "codex_version": {"codex-cli_0.144.1"},
        "repository_carrier": {"present_and_valid"},
        "root_plugin_manifest": {".codex-plugin/plugin.json"},
        "root_marketplace_manifest": {".agents/plugins/marketplace.json"},
        "marketplace_name": {"cotend"},
        "marketplace_source": {"url_relative_root"},
        "candidate_version": {"0.1.0-rc.1"},
        "semantic_source": {"skills/"},
        "semantic_sources": {"1"},
        "source_skill_manifest_sha256": {
            "acbd6d6668d0e8fc34ea7585db5c758cc09a9ea08756f7a52b84f4a5b841ba1b"
        },
        "package_manifest_sha256": {
            "18f0b62852ebe1f7afbd43bcbff50706aacd1d66ae6edeb4c5b133d53fdd858f"
        },
        "allowed_manifest_path_rewrites": {"3"},
        "adopted_skills": {"7"},
        "adopted_skill_files": {"30"},
        "normal_lifecycle_steps": {"15"},
        "failure_recovery_steps": {"5"},
        "write_roots_redirected": {"15"},
        "protected_user_boundaries": {"8"},
        "focused_tests": {"12"},
        "full_unit_tests": {"157"},
        "repository_check": {
            "passed_166_public_candidates_19_capabilities_19_specs"
        },
        "official_validator": {"passed"},
        "local_marketplace_repeat_add": {"idempotent_success"},
        "local_marketplace_upgrade": {
            "local_path_not_configured_as_git_marketplace"
        },
        "external_project_root_removed": {"true"},
        "remote_owner_repo_fetch": {"not_run"},
        "git_backed_marketplace_upgrade": {"not_run"},
        "clean_novice_install": {"not_run"},
        "desktop_restart_visibility": {"not_run"},
        "release_publish_push": {"false"},
    }.items():
        if metadata_values(evidence_text, key) != expected:
            errors.append(f"GitHub Marketplace evidence mismatch: {key}")
    for marker in (
        "一次性本地 Git Marketplace",
        "正常场景观察到 1 次、恢复场景观察到 7 次",
        "真实用户 Codex/Agents 的 8 个边界只做 stat-only 元数据快照",
        "remote_git=not_run",
        "没有从真实 GitHub `owner/repo` 添加 Marketplace",
        "不表示 CoTend 已经公开可安装或完成上架",
    ):
        if marker not in evidence_text:
            errors.append(f"GitHub Marketplace evidence is missing: {marker}")

    attributes = read(".gitattributes")
    for marker in (
        "/\\.codex-plugin/plugin.json text eol=lf",
        "/.agents/plugins/marketplace.json text eol=lf",
        "/skills/** text eol=lf",
    ):
        if marker not in attributes:
            errors.append(f"GitHub Marketplace LF contract is missing: {marker}")
    return errors


def plugin_submission_material_errors(
    evidence_text: str,
    candidates: set[str],
) -> list[str]:
    errors: list[str] = []
    missing = EXPECTED_PLUGIN_SUBMISSION_FILES - candidates
    if missing:
        errors.append(
            f"Plugin submission material artifacts are missing: {sorted(missing)}"
        )
        return errors

    try:
        submission = json.loads(
            read("packaging/codex-plugin/submission-materials/submission.json")
        )
        reviewer_tests = json.loads(
            read("packaging/codex-plugin/submission-materials/reviewer-tests.json")
        )
    except (json.JSONDecodeError, OSError) as exc:
        return [f"Plugin submission material JSON is invalid: {exc}"]

    package_binding = submission.get("package", {})
    if submission.get("status") != "draft_not_submitted":
        errors.append("Plugin submission contract must remain draft_not_submitted")
    if package_binding.get("plugin_id") != "cotend" or package_binding.get(
        "version"
    ) != "0.1.0-rc.1":
        errors.append("Plugin submission package identity drifted")
    if package_binding.get("file_count") != 41 or package_binding.get(
        "path_hash_manifest_sha256"
    ) != "18f0b62852ebe1f7afbd43bcbff50706aacd1d66ae6edeb4c5b133d53fdd858f":
        errors.append("Plugin submission package digest drifted")
    if (
        package_binding.get("identity_authority")
        != "initial_submission_identity_confirmed_not_release"
        or package_binding.get("final_identity_confirmed") is not True
    ):
        errors.append("Plugin submission final identity state drifted")

    prompts = submission.get("starter_prompts")
    manifest = json.loads(
        read("packaging/codex-plugin/cotend/.codex-plugin/plugin.json")
    )
    if prompts != manifest.get("interface", {}).get("defaultPrompt"):
        errors.append("Plugin submission starter prompts differ from manifest")
    listing_logo = submission.get("listing", {}).get("logo")
    if listing_logo != {
        "status": "repository_asset_ready_portal_format_not_verified",
        "asset_path": "assets/cotend-logo.png",
    }:
        errors.append("Plugin submission listing logo drifted")
    positive = reviewer_tests.get("positive_cases")
    negative = reviewer_tests.get("negative_cases")
    if not isinstance(positive, list) or len(positive) != 5:
        errors.append("Plugin submission must contain exactly five positive cases")
    if not isinstance(negative, list) or len(negative) != 3:
        errors.append("Plugin submission must contain exactly three negative cases")
    if reviewer_tests.get("status") != "contract_only_not_run":
        errors.append("Plugin reviewer cases must remain contract_only_not_run")

    blockers = submission.get("blockers")
    if not isinstance(blockers, list) or len(blockers) != 10:
        errors.append("Plugin submission external blocker inventory drifted")
    else:
        expected_identity_value = {
            "plugin_id": "cotend",
            "version": "0.1.0-rc.1",
            "package_digest": (
                "18f0b62852ebe1f7afbd43bcbff50706aacd1d66ae6edeb4c5b133d53fdd858f"
            ),
            "confirmed_on": "2026-07-14",
            "confirmation_scope": (
                "initial_submission_identity_not_release_or_platform_acceptance"
            ),
            "platform_prerelease_acceptance": "not_verified_reopen_q02_if_rejected",
        }
        identity = blockers[0]
        if (
            not isinstance(identity, dict)
            or identity.get("id") != "final_plugin_identity_and_version"
            or identity.get("status") != "resolved"
            or identity.get("value") != expected_identity_value
        ):
            errors.append("Plugin submission confirmed identity evidence drifted")
        logo = blockers[3]
        logo_value = logo.get("value") if isinstance(logo, dict) else None
        if (
            not isinstance(logo, dict)
            or logo.get("id") != "production_logo"
            or logo.get("status") != "resolved"
            or not isinstance(logo_value, dict)
            or logo_value.get("source_sha256")
            != "27c5a8566bb4d7800f9250715aef649adf5806b35784955a093cc37cf477238a"
            or logo_value.get("primary_sha256")
            != "3a39de1b6c956b37a5e6efc0fb616a06104ce9d9417d3157ab5c5a002af72d49"
            or logo_value.get("portal_exact_format") != "not_verified"
        ):
            errors.append("Plugin submission production logo evidence drifted")
        if any(
            not isinstance(item, dict)
            or item.get("status") != "unresolved"
            or item.get("value") is not None
            for index, item in enumerate(blockers)
            if index not in {0, 3}
        ):
            errors.append("Plugin submission blocker was resolved without evidence")
    if submission.get("readiness") != {
        "status": "blocked_not_ready_for_portal_submission",
        "unresolved_blocker_ids": [
            "verified_publisher_identity",
            "apps_management_write_access",
            "website_url",
            "support_url",
            "privacy_policy_url",
            "terms_url",
            "country_or_region_availability",
            "policy_attestations",
        ],
        "portal_submission_ready": False,
    }:
        errors.append("Plugin submission readiness boundary drifted")
    if submission.get("authority") != {
        "repository_contract_only": True,
        "portal_opened": False,
        "portal_draft_created": False,
        "submitted_for_review": False,
        "approved": False,
        "published": False,
        "release_authorized": False,
        "push_authorized": False,
    }:
        errors.append("Plugin submission authority boundary drifted")

    verifier_text = read("scripts/verify_plugin_submission_materials.py")
    for marker in (
        "EXPECTED_POSITIVE_IDS",
        "EXPECTED_NEGATIVE_IDS",
        "EXPECTED_BLOCKER_IDS",
        "EXPECTED_PRODUCTION_LOGO_VALUE",
        "contract_only_not_run",
        "submission blocker was resolved without evidence",
        "PLUGIN_SUBMISSION_MATERIALS_OK",
    ):
        if marker not in verifier_text:
            errors.append(f"Plugin submission verifier is missing: {marker}")
    test_text = read("tests/test_plugin_submission_materials.py")
    actual_tests = set(
        re.findall(r"^\s+def (test_[a-z0-9_]+)\(", test_text, re.MULTILINE)
    )
    missing_tests = EXPECTED_PLUGIN_SUBMISSION_TESTS - actual_tests
    if missing_tests:
        errors.append(
            f"Plugin submission material tests are missing: {sorted(missing_tests)}"
        )
    if "NEGATIVE_MUTATION_COUNT = 17" not in test_text:
        errors.append("Plugin submission negative mutation count drifted")

    for key, expected in {
        "status": {"passed_repo_only_submission_material_contract"},
        "evidence_type": {"executed"},
        "submission_type": {"skills_only"},
        "candidate_plugin_id": {"cotend"},
        "candidate_version": {"0.1.0-rc.1"},
        "identity_authority": {"initial_submission_identity_confirmed_not_release"},
        "final_plugin_identity_confirmed": {"true"},
        "package_files": {"41"},
        "submission_contract_status": {"draft_not_submitted"},
        "starter_prompts": {"3"},
        "positive_reviewer_cases": {"5"},
        "negative_reviewer_cases": {"3"},
        "reviewer_case_execution": {"contract_only_not_run"},
        "unresolved_external_blockers": {"8"},
        "focused_unit_tests": {"7"},
        "negative_mutations": {"17"},
        "full_unit_tests": {"157"},
        "production_package_regression": {
            "passed_8_tests_17_negative_6_boundaries"
        },
        "production_lifecycle_regression": {
            "passed_17_normal_5_recovery_15_roots_purged"
        },
        "repository_check": {
            "passed_166_public_candidates_19_capabilities_19_specs"
        },
        "ruff_and_compileall": {"passed"},
        "portal_opened": {"false"},
        "submitted_for_review": {"false"},
        "release_or_publish": {"false"},
        "push": {"false"},
    }.items():
        if metadata_values(evidence_text, key) != expected:
            errors.append(f"Plugin submission material evidence mismatch: {key}")
    for marker in (
        "恰好 5 个正向和 3 个负向 reviewer case",
        "contract_only_not_run",
        "8 个未解决 blocker",
        "没有打开 OpenAI Platform 或 submission Portal",
        "PLUGIN_SUBMISSION_MATERIALS_OK status=draft_not_submitted",
        "Ran 157 tests - OK",
        "PRODUCTION_PLUGIN_LIFECYCLE_OK version=0.1.0-rc.1 files=41",
        "不表示已经 ready for Portal submission",
    ):
        if marker not in evidence_text:
            errors.append(f"Plugin submission material evidence is missing: {marker}")
    attributes = read(".gitattributes")
    for path in (
        "/packaging/codex-plugin/submission-materials/submission.json text eol=lf",
        "/packaging/codex-plugin/submission-materials/reviewer-tests.json text eol=lf",
    ):
        if path not in attributes:
            errors.append(f"Plugin submission LF contract is missing: {path}")
    return errors


def public_repository_onboarding_errors(
    evidence_text: str,
    candidates: set[str],
) -> list[str]:
    errors: list[str] = []
    missing = EXPECTED_PUBLIC_README_FILES - candidates
    if missing:
        errors.append(f"public repository onboarding artifacts are missing: {sorted(missing)}")
        return errors

    readme = read("README.md")
    for marker in (
        "# CoTend",
        "Pre-release AI development governance framework",
        "CoTend is not yet available in the Public Plugin Directory.",
        "No supported end-user installation is available yet.",
        "The current pre-release adapter targets Codex",
        "`CoTend Init` is the normal start or resume entry",
        "The plugin has not been submitted for review and has not been published.",
        "Do not treat them as a supported end-user installation.",
        "Codex or ChatGPT platform login, network access, permissions",
        "python scripts/build_codex_plugin.py --output dist/cotend --json",
        "python scripts/verify_plugin_submission_materials.py",
        "python scripts/verify_production_plugin_lifecycle.py",
        "python scripts/verify_github_marketplace_carrier.py",
    ):
        if marker not in readme:
            errors.append(f"public README is missing: {marker}")
    if re.search(r"[\u3400-\u9fff]", readme):
        errors.append("public README must remain English")
    skill_section = readme.split("<!-- skill-catalog-start -->", 1)
    if len(skill_section) != 2 or "<!-- skill-catalog-end -->" not in skill_section[1]:
        errors.append("public README Skill catalog markers are missing")
    else:
        ids = re.findall(
            r"^\| [^|]+ \| `([^`]+)` \|",
            skill_section[1].split("<!-- skill-catalog-end -->", 1)[0],
            re.MULTILINE,
        )
        expected_ids = {
            "cotend-init",
            "cotend-project-init",
            "cotend-collaboration",
            "cotend-diagnose-only",
            "cotend-model-upgrade",
            "grill-me",
            "karpathy-guidelines",
        }
        if len(ids) != 7 or set(ids) != expected_ids:
            errors.append("public README seven-Skill catalog drifted")

    submission = json.loads(
        read("packaging/codex-plugin/submission-materials/submission.json")
    )
    prompts = submission.get("starter_prompts")
    if not isinstance(prompts, list) or any(
        f"`{prompt}`" not in readme for prompt in prompts
    ):
        errors.append("public README starter prompts drifted")

    test_text = read("tests/test_public_readme.py")
    actual_tests = set(
        re.findall(r"^\s+def (test_[a-z0-9_]+)\(", test_text, re.MULTILINE)
    )
    missing_tests = EXPECTED_PUBLIC_README_TESTS - actual_tests
    if missing_tests:
        errors.append(f"public README tests are missing: {sorted(missing_tests)}")
    for key, expected in {
        "status": {"passed_public_repository_onboarding_contract"},
        "evidence_type": {"executed"},
        "public_surface_language": {"en"},
        "readme_status": {"pre_release_not_publicly_installable"},
        "visible_skill_catalog_rows": {"7"},
        "starter_prompts": {"3"},
        "relative_links_valid": {"true"},
        "maintainer_commands": {"7_safe_repo_only"},
        "focused_tests": {"6"},
        "full_unit_tests": {"157"},
        "production_package_regression": {
            "passed_8_tests_17_negative_6_boundaries"
        },
        "submission_material_regression": {
            "passed_3_prompts_5_positive_3_negative_8_blockers"
        },
        "production_lifecycle_regression": {
            "passed_17_normal_5_recovery_15_roots_purged"
        },
        "repository_check": {
            "passed_166_public_candidates_19_capabilities_19_specs"
        },
        "real_user_installation": {"false"},
        "portal_or_submission": {"false"},
        "release_publish_push": {"false"},
    }.items():
        if metadata_values(evidence_text, key) != expected:
            errors.append(f"public onboarding evidence mismatch: {key}")
    for marker in (
        "README 没有把 7 个物理 Skill 平铺成 7 个日常命令",
        "Public Plugin Directory 尚不可用",
        "没有真实用户 Plugin 安装、`codex plugin marketplace` 写入、Portal、submission、publish 或 push 命令",
        "不表示产品已经公开可安装或完成上架",
        "Ran 157 tests - OK",
    ):
        if marker not in evidence_text:
            errors.append(f"public onboarding evidence is missing: {marker}")
    if "/README.md text eol=lf" not in read(".gitattributes"):
        errors.append("public README LF contract is missing")
    return errors


def submission_prerequisite_packet_errors(
    evidence_text: str,
    candidates: set[str],
) -> list[str]:
    errors: list[str] = []
    missing = EXPECTED_SUBMISSION_PREREQUISITE_FILES - candidates
    if missing:
        errors.append(
            f"submission prerequisite artifacts are missing: {sorted(missing)}"
        )
        return errors

    result = subprocess.run(
        [sys.executable, "scripts/verify_submission_prerequisites.py"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "unknown failure"
        errors.append(f"submission prerequisite verifier failed: {detail}")
    else:
        for marker in (
            "SUBMISSION_PREREQUISITES_OK",
            "status=prerequisite_resolution_required",
            "prerequisites=10",
            "decisions=7",
            "active=none",
            "blocked=Q07-policy-attestations",
            "digest=18f0b62852ebe1f7afbd43bcbff50706aacd1d66ae6edeb4c5b133d53fdd858f",
        ):
            if marker not in result.stdout:
                errors.append(
                    f"submission prerequisite verifier output is missing: {marker}"
                )

    test_text = read("tests/test_submission_prerequisites.py")
    actual_tests = set(
        re.findall(r"^\s+def (test_[a-z0-9_]+)\(", test_text, re.MULTILINE)
    )
    missing_tests = EXPECTED_SUBMISSION_PREREQUISITE_TESTS - actual_tests
    if missing_tests:
        errors.append(
            f"submission prerequisite tests are missing: {sorted(missing_tests)}"
        )
    if "NEGATIVE_MUTATION_COUNT = 18" not in test_text:
        errors.append("submission prerequisite negative mutation count drifted")

    for marker in (
        "10 个先决条件、其中 8 个仍未解决",
        "7 个决策无环",
        "Q06 已记录全球首发意图",
        "Q07 在 7 项前置证据解决前保持 blocked",
        "policy attestations 位于最后",
        "没有打开 OpenAI Platform 或 submission Portal",
        "普通“继续”不解决这些前置证据",
        "python scripts/verify_submission_prerequisites.py",
        "不证明任何外部 blocker 已完成",
        "Ran 157 tests - OK",
        "REPOSITORY_CHECK_OK public_candidates=166 capabilities=19 behavior_specs=19",
        "没有真实用户安装、Platform 写入、Portal、submission、publish 或 push",
    ):
        if marker not in evidence_text:
            errors.append(f"submission prerequisite evidence is missing: {marker}")
    if (
        "/packaging/codex-plugin/submission-materials/prerequisites.json text eol=lf"
        not in read(".gitattributes")
    ):
        errors.append("submission prerequisite LF contract is missing")
    return errors


def contract_relationship_errors(index_text: str, specs: dict[str, str]) -> list[str]:
    errors: list[str] = []
    dependencies = index_dependencies(index_text)
    if set(dependencies) != EXPECTED_CAPABILITIES:
        errors.append("behavior dependency index must contain C01-C19")

    for capability, required in dependencies.items():
        unknown = set(required) - set(dependencies)
        if unknown:
            errors.append(f"{capability}: unknown dependencies {sorted(unknown)}")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(capability: str) -> None:
        if capability in visiting:
            errors.append(f"behavior dependency cycle includes {capability}")
            return
        if capability in visited:
            return
        visiting.add(capability)
        for dependency in dependencies.get(capability, []):
            visit(dependency)
        visiting.remove(capability)
        visited.add(capability)

    for capability in dependencies:
        visit(capability)

    owner_to_spec: dict[str, str] = {}
    for spec_path, spec_text in specs.items():
        spec_ids = metadata_values(spec_text, "spec_id")
        if len(spec_ids) != 1:
            errors.append(f"{spec_path}: expected one spec_id")
            continue
        spec_id = next(iter(spec_ids))
        declared_dependencies = metadata_list(spec_text, "depends_on")
        declared_consumers = metadata_list(spec_text, "required_by")
        owners = metadata_list(spec_text, "shared_rule_owners")
        if declared_dependencies is None or declared_consumers is None or owners is None:
            errors.append(f"{spec_path}: missing relationship metadata")
            continue
        if declared_dependencies != dependencies.get(spec_id):
            errors.append(f"{spec_id}: depends_on does not match behavior index")
        expected_consumers = sorted(
            capability for capability, required in dependencies.items() if spec_id in required
        )
        if sorted(declared_consumers) != expected_consumers:
            errors.append(f"{spec_id}: required_by is not the inverse dependency index")
        for owner in owners:
            previous = owner_to_spec.get(owner)
            if previous is not None:
                errors.append(f"shared rule owner {owner} is duplicated by {previous} and {spec_id}")
            owner_to_spec[owner] = spec_id

    return errors


def delivery_product_errors(candidates: set[str]) -> list[str]:
    errors: list[str] = []
    missing = EXPECTED_DELIVERY_PRODUCT_FILES - candidates
    if missing:
        errors.append(f"delivery product files are missing or ignored: {sorted(missing)}")

    package_files = {
        path
        for path in candidates
        if path.startswith("src/cotend_delivery/") and path.endswith(".py")
    }
    expected_package_files = {
        path
        for path in EXPECTED_DELIVERY_PRODUCT_FILES
        if path.startswith("src/cotend_delivery/")
    }
    if package_files != expected_package_files:
        errors.append("delivery package inventory drift")

    core_path = "src/cotend_delivery/core.py"
    if core_path in candidates:
        core_text = read(core_path)
        operations = re.search(
            r"^OPERATIONS = \{(?P<body>.*?)^\}",
            core_text,
            re.MULTILINE | re.DOTALL,
        )
        actual_operations = (
            set(re.findall(r'^\s+"([a-z_]+)",\s*$', operations.group("body"), re.MULTILINE))
            if operations
            else set()
        )
        if actual_operations != EXPECTED_DELIVERY_OPERATIONS:
            errors.append(f"delivery operation inventory drift: {sorted(actual_operations)}")
        for marker in (
            "EXPECTED_FILE_COUNT = 30",
            "class DeliveryLayout:",
            "USER_RECEIPT_SCHEMA_VERSION = 3",
            "PRODUCTION_USER_RECEIPT_SCHEMA_VERSION = 4",
            "FIRST_PARTY_SKILLS = EXPECTED_SKILLS[:5]",
            "SHAREABLE_COMPANION_SKILLS = EXPECTED_SKILLS[5:]",
            '"external_shared"',
            "_receipt_owned_skills",
            "include_previous_rollback=False",
            "transition_failed_rolled_back",
            "receipt_invalid",
            "unowned_collision",
            "symlink_boundary",
            "identity_migration_available",
            "downgrade_candidate",
            "preserve_existing",
            "isolated_production_user",
            "production_receipt_binding",
            "layout_context_rebind",
            "receipt_installation_identity_mismatch",
            "MUTATION_LOCK_SCHEMA",
            'self.mutation_lock_path = self.state_root / "mutation.lock"',
            "mutation_locked",
            "mutation_transition_interrupted",
            "owner_token=lease.owner_token",
            "RECOVERY_LOCK_SCHEMA",
            'self.recovery_lock_path = self.state_root / "recovery.lock"',
            "recovery_plan_id",
            "release_abandoned_lock",
            "rollback_interrupted_transition",
            "forward_finalize",
        ):
            if marker not in core_text:
                errors.append(f"delivery core contract marker is missing: {marker}")

    cli_path = "src/cotend_delivery/cli.py"
    if cli_path in candidates:
        cli_text = read(cli_path)
        for marker in (
            '"--project"',
            '"--apply"',
            '"--source-release-id"',
            '"--revision"',
            '"--confirm-recovery-plan-id"',
            "Mutation commands are dry-run unless --apply is provided.",
        ):
            if marker not in cli_text:
                errors.append(f"delivery CLI contract marker is missing: {marker}")

    harness_path = "scripts/verify_delivery_lifecycle.py"
    if harness_path in candidates:
        harness_text = read(harness_path)
        for marker in (
            "guarded_fixture",
            "DELIVERY_LIFECYCLE_OK",
            "DELIVERY_LIFECYCLE_NEGATIVE_OK",
            "DELIVERY_IDENTITY_MIGRATION_OK",
            "transition_failure_atomicity",
            "downgrade_not_update",
            "preserved_checkpoint_payload_drift",
            "DELIVERY_CONCURRENCY_OK",
            "same_project_contender_zero_write",
            "terminated_midmutation_detected",
            "DELIVERY_RECOVERY_OK",
            "confirmation_gate_zero_write",
            "stale_plan_toctou_zero_write",
            "terminated_recovery_retains_dual_evidence",
        ):
            if marker not in harness_text:
                errors.append(f"delivery lifecycle harness marker is missing: {marker}")

    user_harness_path = "scripts/verify_user_skill_delivery.py"
    if user_harness_path in candidates:
        user_harness_text = read(user_harness_path)
        for marker in (
            "stat_only_snapshot",
            "canonical_user_skills",
            "compatibility_user_skills",
            "USER_SKILL_DELIVERY_OK",
            "unchanged=true",
        ):
            if marker not in user_harness_text:
                errors.append(f"user delivery harness marker is missing: {marker}")

    tests_path = "tests/test_cotend_delivery.py"
    if tests_path in candidates:
        actual_tests = set(
            re.findall(r"^    def (test_[a-z0-9_]+)\(", read(tests_path), re.MULTILINE)
        )
        missing_tests = EXPECTED_DELIVERY_TESTS - actual_tests
        if missing_tests:
            errors.append(f"required delivery unit tests are missing: {sorted(missing_tests)}")

    user_tests_path = "tests/test_user_skill_delivery.py"
    if user_tests_path in candidates:
        actual_user_tests = set(
            re.findall(
                r"^    def (test_[a-z0-9_]+)\(",
                read(user_tests_path),
                re.MULTILINE,
            )
        )
        missing_user_tests = EXPECTED_USER_DELIVERY_TESTS - actual_user_tests
        if missing_user_tests:
            errors.append(
                f"required user delivery tests are missing: {sorted(missing_user_tests)}"
            )

    user_scope_path = "src/cotend_delivery/user_scope.py"
    if user_scope_path in candidates:
        user_scope_text = read(user_scope_path)
        for marker in (
            "class IsolatedUserSkillDeliveryManager",
            "DeliveryLayout.isolated_user",
            "_default_candidate=artifact",
        ):
            if marker not in user_scope_text:
                errors.append(f"user delivery adapter marker is missing: {marker}")

    user_evidence_path = "docs/evidence/ISOLATED-USER-SKILL-DELIVERY.md"
    if user_evidence_path in candidates:
        user_evidence = read(user_evidence_path)
        for marker in (
            "status: passed_isolated_only",
            "user_receipt_schema: 3_component_ownership",
            "USER_SKILL_DELIVERY_OK tests=19 skipped=0 protected_boundaries=6 unchanged=true",
            "real_user_scope_write: false",
            "production_state_root: resolved_in_later_non_live_contract",
        ):
            if marker not in user_evidence:
                errors.append(f"user delivery evidence is missing: {marker}")

    production_resolver_path = "src/cotend_delivery/production_resolver.py"
    if production_resolver_path in candidates:
        production_resolver = read(production_resolver_path)
        for marker in (
            "class ProductionUserLayout",
            'STATE_DIRECTORY_NAME = ".cotend-delivery"',
            '"cotend.production-installation.v1"',
            '"cotend.production-layout.v1"',
            '"explicit_receipt_migration_required"',
            '"first_party_compatibility_residue"',
            '"layout_context_changed"',
            '"installation_identity_mismatch"',
            '"current_envelope"',
            '"production_apply_forbidden"',
        ):
            if marker not in production_resolver:
                errors.append(f"production resolver marker is missing: {marker}")

    production_cli_path = "src/cotend_delivery/production_cli.py"
    if production_cli_path in candidates:
        production_cli = read(production_cli_path)
        for marker in (
            'prog="cotend-user-delivery"',
            "if args.apply:",
            '"production_apply_forbidden"',
            "ProductionUserDeliveryBridge",
            "bridge.execute",
            '"--expected-layout-fingerprint"',
        ):
            if marker not in production_cli:
                errors.append(f"production user CLI marker is missing: {marker}")

    production_scope_path = "src/cotend_delivery/production_scope.py"
    if production_scope_path in candidates:
        production_scope = read(production_scope_path)
        for marker in (
            "class ProductionUserDeliveryBridge",
            '"state": "hard_disabled"',
            '"manager_available": False',
            '"production_apply_forbidden"',
            "class IsolatedProductionUserSkillDeliveryManager",
            "DeliveryLayout.isolated_production_user",
            "_default_candidate=artifact",
        ):
            if marker not in production_scope:
                errors.append(f"production scope marker is missing: {marker}")

    production_harness_path = "scripts/verify_production_user_resolver.py"
    if production_harness_path in candidates:
        production_harness = read(production_harness_path)
        for marker in (
            "protected_boundaries",
            "stat_only_snapshot",
            "PRODUCTION_USER_RESOLVER_OK",
            "unchanged=true",
            "production_apply=false",
        ):
            if marker not in production_harness:
                errors.append(f"production resolver harness marker is missing: {marker}")

    production_tests_path = "tests/test_production_user_resolver.py"
    if production_tests_path in candidates:
        actual_production_tests = set(
            re.findall(
                r"^    def (test_[a-z0-9_]+)\(",
                read(production_tests_path),
                re.MULTILINE,
            )
        )
        missing_production_tests = (
            EXPECTED_PRODUCTION_RESOLVER_TESTS - actual_production_tests
        )
        if missing_production_tests:
            errors.append(
                "required production resolver tests are missing: "
                f"{sorted(missing_production_tests)}"
            )

    production_receipt_harness_path = "scripts/verify_production_user_receipt.py"
    if production_receipt_harness_path in candidates:
        production_receipt_harness = read(production_receipt_harness_path)
        for marker in (
            "protected_boundaries",
            "stat_only_snapshot",
            "PRODUCTION_USER_RECEIPT_OK",
            "unchanged=true",
            "production_apply=false",
        ):
            if marker not in production_receipt_harness:
                errors.append(
                    f"production receipt harness marker is missing: {marker}"
                )

    production_receipt_tests_path = "tests/test_production_user_receipt.py"
    if production_receipt_tests_path in candidates:
        actual_production_receipt_tests = set(
            re.findall(
                r"^    def (test_[a-z0-9_]+)\(",
                read(production_receipt_tests_path),
                re.MULTILINE,
            )
        )
        missing_production_receipt_tests = (
            EXPECTED_PRODUCTION_RECEIPT_TESTS - actual_production_receipt_tests
        )
        if missing_production_receipt_tests:
            errors.append(
                "required production receipt tests are missing: "
                f"{sorted(missing_production_receipt_tests)}"
            )

    production_evidence_path = "docs/evidence/PRODUCTION-USER-LAYOUT-RESOLVER.md"
    if production_evidence_path in candidates:
        production_evidence = read(production_evidence_path)
        for marker in (
            "status: passed_non_live_only",
            "canonical_payload: $HOME/.agents/skills",
            "state_root: $HOME/.agents/.cotend-delivery",
            "PRODUCTION_USER_RESOLVER_OK tests=13 skipped=0 protected_boundaries=6 unchanged=true production_apply=false",
            "real_user_scope_write: false",
            "production_apply: forbidden",
        ):
            if marker not in production_evidence:
                errors.append(f"production resolver evidence is missing: {marker}")

    production_receipt_evidence_path = (
        "docs/evidence/ISOLATED-PRODUCTION-USER-RECEIPT.md"
    )
    if production_receipt_evidence_path in candidates:
        production_receipt_evidence = read(production_receipt_evidence_path)
        for marker in (
            "status: passed_isolated_only",
            "production_user_receipt_schema: 4_identity_bound",
            "legacy_user_receipt_schema: 3_explicit_receipt_only_migration",
            "PRODUCTION_USER_RECEIPT_OK tests=13 skipped=0 protected_boundaries=6 unchanged=true production_apply=false",
            "transaction_bridge: hard_disabled",
            "real_user_scope_write: false",
            "production_apply: forbidden",
        ):
            if marker not in production_receipt_evidence:
                errors.append(f"production receipt evidence is missing: {marker}")

    target_lock_path = ROOT / "delivery" / "codex-artifact.lock.json"
    framework_lock_path = ROOT / "upstream" / "framework.lock.json"
    try:
        target_lock = json.loads(target_lock_path.read_text(encoding="utf-8"))
        framework_lock = json.loads(framework_lock_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"delivery target lock is invalid: {exc}")
        return errors
    source = target_lock.get("source")
    target = target_lock.get("target")
    product = target_lock.get("product")
    if (
        target_lock.get("schema") != "cotend.target-artifact-lock"
        or target_lock.get("schema_version") != 1
        or target_lock.get("status") != "verified"
        or source
        != {
            "framework_lock": "upstream/framework.lock.json",
            "release_id": framework_lock.get("release_id"),
            "carrier": framework_lock.get("source_carrier"),
            "framework_protocol": framework_lock.get("framework_protocol"),
        }
        or product != {"version": None}
        or target_lock.get("skill_count") != 7
        or target_lock.get("skill_file_count") != 30
    ):
        errors.append("delivery target lock source or envelope mismatch")
    expected_target = {
        "platform": "Codex",
        "lineage": "cotend-codex",
        "artifact_id": "cotend-codex-r000001",
        "revision": 1,
    }
    if not isinstance(target, dict) or any(
        target.get(key) != expected for key, expected in expected_target.items()
    ):
        errors.append("delivery target lock identity mismatch")
    carrier_files = {
        path.relative_to(ROOT / "skills").as_posix(): hashlib.sha256(
            path.read_bytes()
        ).hexdigest()
        for path in sorted((ROOT / "skills").rglob("*"))
        if path.is_file()
    }
    carrier_manifest = hashlib.sha256(
        json.dumps(
            carrier_files,
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()
    if not isinstance(target, dict) or target.get("manifest_sha256") != carrier_manifest:
        errors.append("delivery target lock manifest mismatch")
    expected_legacy_mapping = {
        "receipt_schema_version": 1,
        "artifact_id": framework_lock.get("release_id"),
        "protocol": framework_lock.get("framework_protocol"),
        "manifest_sha256": carrier_manifest,
        "target_artifact_id": "cotend-codex-r000001",
        "target_revision": 1,
    }
    if target_lock.get("legacy_receipt_mappings") != [expected_legacy_mapping]:
        errors.append("delivery target lock legacy mapping mismatch")
    identity_evidence_path = "docs/evidence/TARGET-ARTIFACT-IDENTITY-SCHEMA-V2.md"
    if identity_evidence_path not in candidates:
        errors.append("target artifact identity evidence is missing or ignored")
    else:
        evidence = read(identity_evidence_path)
        for marker in (
            "target_artifact_id: cotend-codex-r000001",
            "target_revision: 1",
            "source_framework_lock_changed: false",
            "receipt_schema: 2_with_schema_1_read_and_migration",
            "checkpoint_schema: 2_with_schema_1_snapshot_read",
            "identity_migration_available",
            "downgrade_candidate",
            "preserve_existing",
        ):
            if marker not in evidence:
                errors.append(f"target artifact identity evidence is missing: {marker}")
    concurrency_evidence_path = "docs/evidence/DELIVERY-CONCURRENCY-AND-INTERRUPTION.md"
    if concurrency_evidence_path not in candidates:
        errors.append("delivery concurrency evidence is missing or ignored")
    else:
        evidence = read(concurrency_evidence_path)
        for marker in (
            "status: passed_disposable_process_level",
            "mutation_lock_schema: 1",
            "same_project_contention: blocked_before_checkpoint_or_payload",
            "different_projects: independent",
            "stale_lock_cleanup: never_automatic",
            "process_liveness_role: diagnostic_only",
            "automatic_recovery: not_implemented",
            "DELIVERY_CONCURRENCY_OK cases=6",
        ):
            if marker not in evidence:
                errors.append(f"delivery concurrency evidence is missing: {marker}")
    recovery_evidence_path = "docs/evidence/DELIVERY-INTERRUPTED-RECOVERY.md"
    if recovery_evidence_path not in candidates:
        errors.append("delivery interrupted-recovery evidence is missing or ignored")
    else:
        evidence = read(recovery_evidence_path)
        for marker in (
            "status: passed_disposable_process_level",
            "recovery_lock_schema: 1",
            "confirmation: one_exact_snapshot_bound_recovery_plan_id",
            "release_abandoned_lock",
            "rollback_interrupted_transition",
            "forward_finalize: blocked_without_intended_target_evidence",
            "DELIVERY_RECOVERY_OK cases=8",
            "real_or_shared_project_apply: not_run",
        ):
            if marker not in evidence:
                errors.append(
                    f"delivery interrupted-recovery evidence is missing: {marker}"
                )
    return errors


def main() -> int:
    errors: list[str] = []
    candidates = git_candidates()

    for local_path in LOCAL_ONLY_PATHS:
        if local_path in candidates or any(path.startswith(f"{local_path}/") for path in candidates):
            errors.append(f"local-only path is publishable: {local_path}")

    text_candidates = {
        path
        for path in candidates
        if (ROOT / path).is_file() and (ROOT / path).suffix.lower() in {".md", ".txt", ".yaml", ".yml", ".json", ".toml", ".py"}
    }
    for relative_path in sorted(text_candidates - {".gitignore", "scripts/check_repository.py"}):
        text = read(relative_path)
        for label, pattern in FORBIDDEN_PUBLIC_PATTERNS.items():
            if (
                relative_path.startswith("skills/")
                and label in FRAMEWORK_SOURCE_ALLOWED_PATTERN_LABELS
            ):
                continue
            if pattern.search(text):
                errors.append(f"{relative_path}: {label}")
        if relative_path.startswith("skills/"):
            for label, pattern in FORBIDDEN_SKILL_MAINTAINER_PATTERNS.items():
                if pattern.search(text):
                    errors.append(f"{relative_path}: {label}")
    errors.extend(checker_self_scan_errors(read("scripts/check_repository.py")))

    reference_study_path = "docs/REFERENCE-FRAMEWORK-IMPLEMENTATION-STUDY.md"
    upstream_registry_path = "UPSTREAM-SOURCES.md"
    framework_candidate_path = "upstream/FRAMEWORK-CANDIDATE.json"
    codex_role_map_path = "upstream/CODEX-SKILL-ROLE-MAP.json"
    adoption_proposal_path = "upstream/FRAMEWORK-ADOPTION-PROPOSAL.md"
    adoption_plan_path = "upstream/FRAMEWORK-ADOPTION-PLAN.md"
    capability_map_path = "upstream/CAPABILITY-IMPLEMENTATION-MAP.json"
    adoption_log_path = "upstream/FRAMEWORK-ADOPTION-LOG.md"
    framework_lock_path = "upstream/framework.lock.json"
    if reference_study_path not in candidates:
        errors.append("reference framework implementation study is missing or ignored")
    if upstream_registry_path not in candidates:
        errors.append("upstream source registry is missing or ignored")
    for path in (
        framework_candidate_path,
        codex_role_map_path,
        adoption_proposal_path,
        adoption_plan_path,
        capability_map_path,
        adoption_log_path,
        framework_lock_path,
    ):
        if path not in candidates:
            errors.append(f"upstream adoption artifact is missing or ignored: {path}")
    if reference_study_path in candidates and upstream_registry_path in candidates:
        errors.extend(
            reference_study_errors(
                read(reference_study_path),
                read(upstream_registry_path),
            )
        )

    coverage_ids = table_capabilities("docs/CAPABILITY-COVERAGE.md")
    index_ids = table_capabilities("docs/BEHAVIOR-SPEC-INDEX.md")
    if coverage_ids != EXPECTED_CAPABILITIES:
        errors.append(f"capability coverage mismatch: {sorted(coverage_ids)}")
    if index_ids != EXPECTED_CAPABILITIES:
        errors.append(f"behavior index mismatch: {sorted(index_ids)}")

    index_text = read("docs/BEHAVIOR-SPEC-INDEX.md")
    if metadata_values(index_text, "capability_count") != {"19"}:
        errors.append("behavior index capability_count must be 19")

    prd_text = read("docs/PRODUCT-PRD.md")
    analysis_paths = (
        "docs/MARKET-LANDSCAPE.md",
        reference_study_path,
        upstream_registry_path,
        adoption_proposal_path,
        adoption_plan_path,
        "FRAMEWORK-CHANGE-EVAL.md",
    )
    errors.extend(
        owner_document_language_errors(
            prd_text,
            {path: read(path) for path in analysis_paths if path in candidates},
        )
    )

    framework_eval_text = read("FRAMEWORK-CHANGE-EVAL.md")
    for key, expected in {
        "change_type": {"workflow_behavior"},
        "decision": {"watch"},
    }.items():
        if metadata_values(framework_eval_text, key) != expected:
            errors.append(f"framework change evaluation mismatch: {key}")
    for required_text in (
        "11_of_11_negative_mutations_rejected",
        "maintainer_residue_mutation_rejected",
        "later_head_passed_and_lock_only_update_rejected",
        "four_protected_blobs_match_and_text_eol_lf_enforced",
        "first_live_codex_validation",
    ):
        if required_text not in framework_eval_text:
            errors.append(f"framework change evaluation is missing: {required_text}")

    carrier_evidence_path = "docs/evidence/ISOLATED-CODEX-CARRIER-VALIDATION.md"
    if carrier_evidence_path not in candidates:
        errors.append("isolated Codex carrier evidence is missing or ignored")
    else:
        errors.extend(
            isolated_codex_carrier_errors(
                read(carrier_evidence_path),
                read(adoption_log_path),
                framework_eval_text,
                candidates,
            )
        )

    plugin_fixture_evidence_path = (
        "docs/evidence/ISOLATED-CODEX-PLUGIN-FIXTURE.md"
    )
    if plugin_fixture_evidence_path not in candidates:
        errors.append("isolated Codex Plugin fixture evidence is missing or ignored")
    else:
        errors.extend(
            isolated_codex_plugin_fixture_errors(
                read(plugin_fixture_evidence_path),
                candidates,
            )
        )

    plugin_namespace_evidence_path = (
        "docs/evidence/CODEX-PLUGIN-NAMESPACE-CANDIDATES.md"
    )
    plugin_namespace_evaluation_path = (
        "docs/CODEX-PLUGIN-NAMESPACE-EVALUATION.md"
    )
    desktop_plugin_surface_path = (
        "docs/evidence/CODEX-DESKTOP-PLUGIN-SURFACE.md"
    )
    if (
        plugin_namespace_evidence_path not in candidates
        or plugin_namespace_evaluation_path not in candidates
        or desktop_plugin_surface_path not in candidates
    ):
        errors.append("Plugin namespace candidate evidence is missing or ignored")
    else:
        errors.extend(
            plugin_namespace_candidate_errors(
                read(plugin_namespace_evidence_path),
                read(plugin_namespace_evaluation_path),
                read(desktop_plugin_surface_path),
                candidates,
            )
        )

    production_plugin_package_evidence_path = (
        "docs/evidence/ISOLATED-CODEX-PLUGIN-PRODUCTION-PACKAGE.md"
    )
    if production_plugin_package_evidence_path not in candidates:
        errors.append("isolated production Plugin package evidence is missing or ignored")
    else:
        errors.extend(
            production_plugin_package_errors(
                read(production_plugin_package_evidence_path),
                candidates,
            )
        )

    production_plugin_lifecycle_evidence_path = (
        "docs/evidence/ISOLATED-CODEX-PLUGIN-PRODUCTION-LIFECYCLE.md"
    )
    if production_plugin_lifecycle_evidence_path not in candidates:
        errors.append("isolated production Plugin lifecycle evidence is missing or ignored")
    else:
        errors.extend(
            production_plugin_lifecycle_errors(
                read(production_plugin_lifecycle_evidence_path),
                candidates,
            )
        )

    github_marketplace_carrier_evidence_path = (
        "docs/evidence/GITHUB-MARKETPLACE-ROOT-CARRIER.md"
    )
    if github_marketplace_carrier_evidence_path not in candidates:
        errors.append("GitHub Marketplace root-carrier evidence is missing or ignored")
    else:
        errors.extend(
            github_marketplace_root_carrier_errors(
                read(github_marketplace_carrier_evidence_path),
                candidates,
            )
        )

    plugin_submission_evidence_path = (
        "docs/evidence/CODEX-PLUGIN-SUBMISSION-MATERIAL-CONTRACT.md"
    )
    if plugin_submission_evidence_path not in candidates:
        errors.append("Plugin submission material evidence is missing or ignored")
    else:
        errors.extend(
            plugin_submission_material_errors(
                read(plugin_submission_evidence_path),
                candidates,
            )
        )

    submission_prerequisite_evidence_path = (
        "docs/evidence/SUBMISSION-PREREQUISITE-DECISION-PACKET.md"
    )
    if submission_prerequisite_evidence_path not in candidates:
        errors.append("submission prerequisite evidence is missing or ignored")
    else:
        errors.extend(
            submission_prerequisite_packet_errors(
                read(submission_prerequisite_evidence_path),
                candidates,
            )
        )

    public_onboarding_evidence_path = (
        "docs/evidence/PUBLIC-REPOSITORY-ONBOARDING.md"
    )
    if public_onboarding_evidence_path not in candidates:
        errors.append("public repository onboarding evidence is missing or ignored")
    else:
        errors.extend(
            public_repository_onboarding_errors(
                read(public_onboarding_evidence_path),
                candidates,
            )
        )

    for key in (
        "architecture_design_status",
        "project_state_layout_status",
        "distribution_design_status",
    ):
        if metadata_values(prd_text, key) != {"unconfirmed"}:
            errors.append(f"PRD {key} must remain unconfirmed")
    for label, pattern in FORBIDDEN_UNCONFIRMED_PRD_PATTERNS.items():
        if pattern.search(prd_text):
            errors.append(f"docs/PRODUCT-PRD.md: {label}")

    spec_paths = sorted(
        path
        for path in candidates
        if path.startswith("docs/behavior-specs/") and path.endswith(".md")
    )
    spec_texts = {spec_path: read(spec_path) for spec_path in spec_paths}
    for spec_path in spec_paths:
        spec_text = spec_texts[spec_path]
        inputs = public_inputs(spec_text)
        if not inputs:
            errors.append(f"{spec_path}: missing public_inputs")
        for input_path in inputs:
            if input_path not in candidates:
                errors.append(f"{spec_path}: public input is missing or ignored: {input_path}")
        if metadata_values(spec_text, "product_baseline_version") != {"0.1.0"}:
            errors.append(f"{spec_path}: product baseline mismatch")
    errors.extend(contract_relationship_errors(index_text, spec_texts))
    errors.extend(delivery_product_errors(candidates))

    journey_path = "docs/NOVICE-JOURNEYS.md"
    journey_text = ""
    if journey_path not in candidates:
        errors.append("novice journey specification is missing or ignored")
    else:
        journey_text = read(journey_path)
        errors.extend(novice_journey_errors(journey_text))

    interface_path = "docs/INTERFACE-CANDIDATE-EVALUATION.md"
    interface_text = ""
    evidence_text: str | None = None
    if interface_path not in candidates:
        errors.append("interface candidate evaluation is missing or ignored")
    else:
        interface_text = read(interface_path)
        evidence_paths = metadata_values(interface_text, "blind_evidence")
        evidence_path = next(iter(evidence_paths), "") if len(evidence_paths) == 1 else ""
        evidence_text = read(evidence_path) if evidence_path in candidates else None
        errors.extend(interface_candidate_errors(interface_text, journey_text, evidence_text))

    if interface_text:
        errors.extend(
            interface_authority_errors(
                interface_text,
                journey_text,
                prd_text,
                interface_path,
            )
        )

    errors.extend(
        productization_truth_errors(
            prd_text,
            read("docs/CLEAN-ROOM-POLICY.md"),
            read("docs/CAPABILITY-COVERAGE.md"),
            read("docs/PRODUCTIZATION-ROADMAP.md"),
            read("docs/BEHAVIOR-SPECIFICATION-STANDARD.md"),
            read(upstream_registry_path),
            read(capability_map_path),
            spec_texts,
            journey_text,
            interface_text,
            evidence_text,
        )
    )

    upstream_adoption_paths = {
        framework_candidate_path,
        codex_role_map_path,
        adoption_proposal_path,
        adoption_plan_path,
        capability_map_path,
        adoption_log_path,
        framework_lock_path,
    }
    if upstream_adoption_paths <= candidates:
        errors.extend(
            upstream_adoption_errors(
                read(framework_candidate_path),
                read(codex_role_map_path),
                read(adoption_proposal_path),
                read(adoption_plan_path),
                read(capability_map_path),
                read(adoption_log_path),
                read(framework_lock_path),
                candidates,
            )
        )

    status_path = ROOT / "STATUS.md"
    plan_path = ROOT / "PROJECT-PLAN-TREE.md"
    if status_path.exists() and plan_path.exists():
        errors.extend(
            local_recovery_truth_errors(read("STATUS.md"), read("PROJECT-PLAN-TREE.md"))
        )
    elif status_path.exists() or plan_path.exists():
        errors.append("local recovery truth requires both STATUS and PROJECT-PLAN-TREE")

    understanding_index = ROOT / "PROJECT-UNDERSTANDING" / "README.md"
    if understanding_index.exists() and "active_route:" in understanding_index.read_text(encoding="utf-8"):
        errors.append("understanding index must not duplicate the active route")

    root_understanding = ROOT / "PROJECT-UNDERSTANDING" / "G0-full-project-understanding.md"
    if root_understanding.exists():
        root_text = root_understanding.read_text(encoding="utf-8")
        if re.search(r"\b16\s*个能力", root_text) or "C01-C19" not in root_text:
            errors.append("root understanding capability baseline drift")

    if errors:
        print("REPOSITORY_CHECK_FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "REPOSITORY_CHECK_OK "
        f"public_candidates={len(candidates)} capabilities={len(EXPECTED_CAPABILITIES)} "
        f"behavior_specs={len(spec_paths)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
