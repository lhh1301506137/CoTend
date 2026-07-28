from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import verify_native_real_project_acceptance as g06  # noqa: E402


class NativeRealProjectAcceptanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.allowed = self.root / "uat"
        self.allowed.mkdir()
        self.project = self.allowed / "retained-project"
        self.private = ROOT / ".private-provenance" / "g06-test-sources" / self.root.name
        self.r10_source = self.private / "r10-skills"
        self.source = self.private / "r11-repository"
        self.user_boundaries = self.root / "user-boundaries"
        self.boundary_patcher = mock.patch.object(
            g06.plugin_boundary,
            "protected_user_paths",
            return_value={
                "user_codex_root": self.user_boundaries / ".codex",
                "user_codex_config": self.user_boundaries / ".codex" / "config.toml",
                "user_codex_auth": self.user_boundaries / ".codex" / "auth.json",
                "user_codex_plugins": self.user_boundaries / ".codex" / "plugins",
                "user_codex_skills": self.user_boundaries / ".codex" / "skills",
                "user_agents_root": self.user_boundaries / ".agents",
                "user_agents_plugins": self.user_boundaries / ".agents" / "plugins",
                "user_agents_skills": self.user_boundaries / ".agents" / "skills",
            },
        )
        self.boundary_patcher.start()

    def tearDown(self) -> None:
        self.boundary_patcher.stop()
        self.temp.cleanup()
        if self.private.exists():
            shutil.rmtree(self.private)

    def prepare_and_deliver(self) -> None:
        g06.extract_r11_source(self.source)
        g06.prepare_project(self.project, self.allowed)
        g06.deliver_r11_to_r12(self.project, self.allowed, self.source)

    def init_payload(
        self,
        *,
        created: list[str] | None = None,
        updated: list[str] | None = None,
    ) -> dict[str, object]:
        return {
            "scenario_id": "g06-real-fresh-init",
            "invoked_skill": "cotend-init",
            "skill_source_path": g06.INIT_SKILL,
            "skill_source_sha256": g06.sha256(self.project / g06.INIT_SKILL),
            "auto_mode": "fresh_init",
            "readiness": "continue_ready",
            "adoption_profile": "standard",
            "runtime_profile": "full",
            "durable_files_created": created or [],
            "durable_files_updated": updated or [],
            "product_implementation_started": False,
            "protected_product_files_modified": False,
            "git_commit_created": False,
            "handback_required": True,
            "summary": "ready",
        }

    def write_chinese_governance(
        self,
        paths: tuple[str, ...] = ("STATUS.md",),
        *,
        declared_language: str = "zh-CN",
    ) -> None:
        payloads = {
            "STATUS.md": (
                "# 项目状态\n\n"
                "user_facing_language_resolution:\n"
                "  contract: dual-ai.user-facing-language-resolution.v1\n"
                "  status: resolved\n"
                f"  normalized_tag: {declared_language}\n"
                "  source: project_local_explicit\n"
                "  adapter: cotend\n"
                "  canonical_carrier: STATUS.md\n"
                "  persisted: yes\n"
                "  conflict: none\n\n"
                "初始化已经完成，当前项目可以继续，但必须等待用户下一条明确指令。\n"
            ),
            "REVIEW-LOG.md": (
                "# 审查记录\n\n"
                "初始化边界检查已经通过，没有开始产品实现，也没有创建任何提交。\n"
            ),
            "QUALITY-SIGNALS.md": (
                "# 质量信号\n\n"
                "当前没有产品实现、提交、发布或任何全局状态变更。\n"
            ),
        }
        for relative in paths:
            self.project.joinpath(relative).write_text(
                payloads[relative],
                encoding="utf-8",
            )

    def test_extracts_exact_r10_from_trusted_commit(self) -> None:
        artifact = g06.extract_r10_source(self.r10_source)
        self.assertEqual(artifact.artifact_id, g06.R10_ID)
        self.assertEqual(artifact.manifest_sha256, g06.R10_MANIFEST)
        self.assertEqual(len(artifact.skills), 8)
        self.assertEqual(len(artifact.files), 40)

    def test_extracts_exact_r11_repository_from_trusted_commit(self) -> None:
        artifact = g06.extract_r11_source(self.source)
        self.assertEqual(artifact.artifact_id, g06.R11_ID)
        self.assertEqual(artifact.manifest_sha256, g06.R11_MANIFEST)
        self.assertEqual(len(artifact.skills), 8)
        self.assertEqual(len(artifact.files), 40)
        self.assertTrue((self.source / "upstream" / "framework.lock.json").is_file())
        self.assertTrue(
            (self.source / "delivery" / "codex-artifact.lock.json").is_file()
        )

    def test_project_guard_rejects_escape_and_nested_child(self) -> None:
        with self.assertRaises(g06.RealProjectAcceptanceError):
            g06.guarded_project(self.root / "outside", self.allowed)
        with self.assertRaises(g06.RealProjectAcceptanceError):
            g06.guarded_project(self.allowed / "nested" / "project", self.allowed)

    def test_prepare_project_creates_clean_git_baseline(self) -> None:
        result = g06.prepare_project(self.project, self.allowed)
        self.assertEqual(result["baseline_files"], 4)
        self.assertTrue((self.project / "PROJECT-BRIEF.md").is_file())
        self.assertEqual(g06.git_status(self.project), "")
        recovered = g06.recover_prepared_project(self.project, self.allowed)
        self.assertEqual(recovered["git_head"], result["git_head"])
        self.assertEqual(recovered["recovery"], "validated_existing_prepare_after_failed_boundary_check")
        with self.assertRaises(g06.RealProjectAcceptanceError):
            g06.prepare_project(self.project, self.allowed)

    def test_project_delivery_updates_r11_to_exact_r12(self) -> None:
        self.prepare_and_deliver()
        state = g06.DeliveryManager(self.project).inspect(g06.r12_artifact())
        self.assertEqual(state["artifact_id"], g06.R12_ID)
        self.assertEqual(state["installation"], "complete")
        self.assertEqual(g06.git_status(self.project), "")

    def test_codex_command_is_ephemeral_and_project_bounded(self) -> None:
        output = ROOT / ".private-provenance" / "g06-test-output" / "init.json"
        command = g06.build_codex_command(self.project, output)
        g06.validate_codex_command(command, self.project)
        self.assertIn("--ignore-user-config", command)
        self.assertNotIn("--add-dir", command)
        self.assertNotIn("--sandbox", command)
        self.assertIn(g06.WORKSPACE_PERMISSION_CONFIG, command)
        self.assertIn("plugins", command)
        self.assertIn("remote_plugin", command)

    def test_codex_command_accepts_explicit_low_cost_model_configuration(self) -> None:
        output = ROOT / ".private-provenance" / "g06-test-output" / "init.json"
        model = "gpt-5.4-mini"
        reasoning_effort = "medium"
        command = g06.build_codex_command(
            self.project,
            output,
            model=model,
            reasoning_effort=reasoning_effort,
        )

        g06.validate_codex_command(
            command,
            self.project,
            expected_model=model,
            expected_reasoning_effort=reasoning_effort,
        )
        self.assertEqual(command[command.index("--model") + 1], model)
        self.assertIn(
            f'model_reasoning_effort="{reasoning_effort}"',
            command,
        )

        drifted = command.copy()
        effort_index = drifted.index(
            f'model_reasoning_effort="{reasoning_effort}"'
        )
        drifted[effort_index] = 'model_reasoning_effort="high"'
        with self.assertRaises(g06.RealProjectAcceptanceError):
            g06.validate_codex_command(
                drifted,
                self.project,
                expected_model=model,
                expected_reasoning_effort=reasoning_effort,
            )

    def test_codex_command_rejects_legacy_or_missing_permission_profile(self) -> None:
        output = ROOT / ".private-provenance" / "g06-test-output" / "init.json"
        command = g06.build_codex_command(self.project, output)

        legacy = command.copy()
        legacy[1:1] = ["--sandbox", "workspace-write"]
        with self.assertRaises(g06.RealProjectAcceptanceError):
            g06.validate_codex_command(legacy, self.project)

        missing = command.copy()
        permission_index = missing.index(g06.WORKSPACE_PERMISSION_CONFIG)
        del missing[permission_index - 1 : permission_index + 1]
        with self.assertRaises(g06.RealProjectAcceptanceError):
            g06.validate_codex_command(missing, self.project)

    def test_windows_path_mapping_is_drive_bounded(self) -> None:
        drive = "H:"
        self.assertEqual(
            g06.pure_windows_path_to_wsl(
                drive + r"\CoTend-UAT\expense-splitter-g06-r12"
            ),
            "/mnt/h/CoTend-UAT/expense-splitter-g06-r12",
        )
        for unsafe in (
            r"relative\project",
            r"\\server\share\project",
            drive + r"\project\..\outside",
        ):
            with self.subTest(unsafe=unsafe):
                with self.assertRaises(g06.RealProjectAcceptanceError):
                    g06.pure_windows_path_to_wsl(unsafe)

    @unittest.skipUnless(os.name == "nt", "Windows extended path normalization")
    def test_extended_windows_path_normalizes_for_boundary_comparison(self) -> None:
        drive = "C:"
        extended = Path(
            "\\\\?\\"
            + drive
            + r"\Users\example\.codex\plugins\cache"
        )
        expected = Path(
            drive + r"\Users\example\.codex\plugins\cache"
        ).resolve(strict=False)
        self.assertEqual(g06.normalize_boundary_path(extended), expected)

    def test_wsl_runtime_root_is_one_guarded_child(self) -> None:
        self.assertEqual(
            str(g06.guarded_wsl_runtime_root("/home/cotend/g06-runtime-test")),
            "/home/cotend/g06-runtime-test",
        )
        for unsafe in (
            "/home/cotend",
            "/home/cotend/nested/g06-runtime-test",
            "/home/other/g06-runtime-test",
            "/home/cotend/not-a-runtime",
            "g06-runtime-relative",
        ):
            with self.subTest(unsafe=unsafe):
                with self.assertRaises(g06.RealProjectAcceptanceError):
                    g06.guarded_wsl_runtime_root(unsafe)

    def test_wsl_inventory_parser_handles_utf16_and_default_marker(self) -> None:
        inventory = (
            "  NAME            STATE           VERSION\r\n"
            "* Ubuntu         Stopped         1\r\n"
            "  CoTend-G06     Stopped         2\r\n"
        ).encode("utf-16-le")
        parsed = g06.parse_wsl_verbose_output(inventory)
        self.assertEqual(
            parsed,
            [
                {
                    "name": "CoTend-G06",
                    "state": "Stopped",
                    "version": 2,
                    "default_marker": False,
                },
                {
                    "name": "Ubuntu",
                    "state": "Stopped",
                    "version": 1,
                    "default_marker": True,
                },
            ],
        )
        snapshot = {
            "default_distribution_id": "{test}",
            "default_distribution_name": "Ubuntu",
            "default_version": 1,
            "distributions": parsed,
        }
        g06.require_wsl_host_baseline(snapshot, "CoTend-G06")
        with self.assertRaises(g06.RealProjectAcceptanceError):
            g06.require_wsl_host_baseline(snapshot, "missing")

    def test_wsl_codex_command_is_explicit_and_project_bounded(self) -> None:
        runtime = "/home/cotend/g06-runtime-test"
        command = g06.build_wsl_codex_command(
            "/mnt/h/uat/retained-project",
            "/mnt/h/private/init.json",
            "CoTend-G06",
            runtime,
            wsl_executable="wsl.exe",
        )
        g06.validate_codex_command(
            command,
            self.project,
            carrier="wsl2",
            expected_project="/mnt/h/uat/retained-project",
            expected_output="/mnt/h/private/init.json",
            wsl_distribution="CoTend-G06",
            wsl_runtime_root=runtime,
        )
        self.assertEqual(
            command[:7],
            [
                "wsl.exe",
                "-d",
                "CoTend-G06",
                "-u",
                "cotend",
                "--",
                "/usr/bin/env",
            ],
        )
        self.assertIn(g06.WSL_CODEX, command)
        for name in g06.WSL_SECRET_ENV_KEYS:
            self.assertNotIn(
                True,
                [value.startswith(f"{name}=") for value in command],
            )

        widened = command.copy()
        widened[widened.index(g06.WSL_CODEX)] = "codex"
        with self.assertRaises(g06.RealProjectAcceptanceError):
            g06.validate_codex_command(
                widened,
                self.project,
                carrier="wsl2",
                expected_project="/mnt/h/uat/retained-project",
                expected_output="/mnt/h/private/init.json",
                wsl_distribution="CoTend-G06",
                wsl_runtime_root=runtime,
            )

    def test_wsl_runtime_auth_copy_and_cleanup_are_bounded(self) -> None:
        class LifecycleRunner:
            def __init__(self, expected_size: int) -> None:
                self.expected_size = expected_size
                self.runtime_present = False
                self.terminated = False
                self.termination_count = 0
                self.operations: list[str] = []

            def __call__(
                self,
                command: list[str],
                **_: object,
            ) -> subprocess.CompletedProcess[str]:
                if command[1:2] == ["--terminate"]:
                    self.terminated = True
                    self.termination_count += 1
                    self.operations.append("terminate")
                    return subprocess.CompletedProcess(command, 0, "", "")
                linux = command[command.index("--") + 1 :]
                executable = linux[0]
                self.operations.append(executable)
                if executable == "/usr/bin/install":
                    self.runtime_present = True
                elif executable == "/usr/bin/stat":
                    return subprocess.CompletedProcess(
                        command,
                        0,
                        f"{self.expected_size}\n",
                        "",
                    )
                elif executable == "/usr/bin/realpath":
                    return subprocess.CompletedProcess(
                        command,
                        0,
                        "/home/cotend/g06-runtime-test\n",
                        "",
                    )
                elif executable == "/usr/bin/rm":
                    self.runtime_present = False
                elif executable == "/usr/bin/test":
                    target = linux[-1]
                    if target == "/home/cotend/g06-runtime-test":
                        return subprocess.CompletedProcess(
                            command,
                            0 if not self.runtime_present else 1,
                            "",
                            "",
                        )
                return subprocess.CompletedProcess(command, 0, "", "")

        auth = self.private / "opaque-auth.json"
        auth.parent.mkdir(parents=True, exist_ok=True)
        auth.write_bytes(b"opaque-test-auth")
        lifecycle = LifecycleRunner(auth.stat().st_size)
        prepared = g06.prepare_wsl_runtime(
            "CoTend-G06",
            "/home/cotend/g06-runtime-test",
            auth,
            wsl_executable="wsl.exe",
            runner=lifecycle,
            path_mapper=lambda _: "/mnt/h/private/opaque-auth.json",
        )
        self.assertEqual(prepared["auth_source_size"], auth.stat().st_size)
        self.assertFalse(prepared["auth_contents_read_by_verifier"])
        self.assertTrue(lifecycle.runtime_present)
        lifecycle.operations.clear()
        cleaned = g06.cleanup_wsl_runtime(
            "CoTend-G06",
            "/home/cotend/g06-runtime-test",
            wsl_executable="wsl.exe",
            runner=lifecycle,
        )
        self.assertTrue(cleaned["runtime_root_removed"])
        self.assertFalse(lifecycle.runtime_present)
        self.assertTrue(lifecycle.terminated)
        self.assertEqual(lifecycle.termination_count, 2)
        self.assertEqual(
            lifecycle.operations,
            [
                "terminate",
                "/usr/bin/realpath",
                "/usr/bin/rm",
                "/usr/bin/test",
                "terminate",
            ],
        )

    def test_wsl_wrapper_wires_event_and_content_checkpoints(self) -> None:
        self.project.mkdir()
        model = "gpt-5.4-mini"
        reasoning_effort = "medium"
        auth = self.private / "opaque-auth.json"
        auth.parent.mkdir(parents=True, exist_ok=True)
        auth.write_bytes(b"opaque-test-auth")
        output = self.private / "init-result.json"
        evidence = self.private / "evidence.json"
        host = {
            "default_distribution_id": "{test}",
            "default_distribution_name": "Ubuntu",
            "default_version": 1,
            "distributions": [
                {
                    "name": "CoTend-G06",
                    "state": "Stopped",
                    "version": 2,
                    "default_marker": False,
                }
            ],
        }
        plugin = {
            "global:user_codex_plugins": {
                "file_count": 1,
                "manifest_sha256": "test",
            }
        }

        def fake_init(
            *_: object,
            event_checkpoint: object,
            **kwargs: object,
        ) -> dict[str, object]:
            self.assertTrue(callable(event_checkpoint))
            self.assertEqual(kwargs["model"], model)
            self.assertEqual(kwargs["reasoning_effort"], reasoning_effort)
            event_checkpoint(  # type: ignore[operator]
                {
                    "status": "running",
                    "json_events_seen": 1,
                    "last_event_type": "thread.started",
                }
            )
            return {"status": "pass", "handback_required": True}

        with (
            mock.patch.object(
                g06,
                "protected_boundary_snapshot",
                return_value={},
            ),
            mock.patch.object(
                g06,
                "assert_protected_boundaries_unchanged",
            ),
            mock.patch.object(
                g06,
                "protected_plugin_content_snapshot",
                side_effect=[plugin, plugin],
            ),
            mock.patch.object(
                g06,
                "snapshot_wsl_host",
                side_effect=[host, host],
            ),
            mock.patch.object(
                g06,
                "probe_wsl_carrier",
                return_value={"distribution": "CoTend-G06"},
            ),
            mock.patch.object(
                g06,
                "prepare_wsl_runtime",
                return_value={"runtime_root": "/home/cotend/g06-runtime-test"},
            ),
            mock.patch.object(
                g06,
                "cleanup_wsl_runtime",
                return_value={
                    "runtime_root_removed": True,
                    "distribution_terminated": True,
                },
            ),
            mock.patch.object(g06, "run_real_init", side_effect=fake_init),
        ):
            result = g06.run_real_init_wsl(
                self.project,
                self.allowed,
                output,
                distribution="CoTend-G06",
                runtime_root="/home/cotend/g06-runtime-test",
                auth_source=auth,
                evidence=evidence,
                model=model,
                reasoning_effort=reasoning_effort,
            )
        persisted = json.loads(evidence.read_text(encoding="utf-8"))
        self.assertEqual(
            persisted["run-init-wsl-events"]["last_event_type"],
            "thread.started",
        )
        self.assertEqual(persisted["run-init-wsl-call"]["model"], model)
        self.assertEqual(
            persisted["run-init-wsl-call"]["reasoning_effort"],
            reasoning_effort,
        )
        self.assertEqual(
            persisted["run-init-wsl-content-boundary"]["status"],
            "pass",
        )
        self.assertTrue(result["plugin_content_boundary_unchanged"])

    def test_init_response_schema_is_strict_and_explicitly_typed(self) -> None:
        schema_path = g06.TEMPLATE_ROOT / g06.INIT_SCHEMA
        schema = g06.validate_response_schema(schema_path)
        self.assertEqual(set(schema["required"]), set(schema["properties"]))
        for value in schema["properties"].values():
            self.assertIn("type", value)

        invalid_path = self.private / "invalid-schema.json"
        invalid = json.loads(schema_path.read_text(encoding="utf-8"))
        del invalid["properties"]["scenario_id"]["type"]
        invalid_path.parent.mkdir(parents=True, exist_ok=True)
        invalid_path.write_text(json.dumps(invalid), encoding="utf-8")
        with self.assertRaises(g06.RealProjectAcceptanceError):
            g06.validate_response_schema(invalid_path)

    def test_language_acceptance_contract_is_strict_and_external_to_template(
        self,
    ) -> None:
        contract = g06.load_language_acceptance_contract()
        self.assertEqual(contract["expected_language"], "zh-CN")
        self.assertEqual(
            contract["status_field"],
            "user_facing_language_resolution.normalized_tag",
        )
        self.assertNotEqual(
            g06.LANGUAGE_ACCEPTANCE_CONTRACT.parent,
            g06.TEMPLATE_ROOT,
        )

        invalid_path = self.private / "invalid-language-contract.json"
        invalid_path.parent.mkdir(parents=True, exist_ok=True)
        invalid = dict(contract)
        invalid["minimum_cjk_characters_per_changed_document"] = 1
        invalid_path.write_text(json.dumps(invalid), encoding="utf-8")
        with self.assertRaises(g06.RealProjectAcceptanceError):
            g06.load_language_acceptance_contract(invalid_path)

    def test_isolated_runtime_redirects_write_roots_and_requires_only_auth(self) -> None:
        runtime = self.private / "isolated-runtime"
        with self.assertRaises(g06.RealProjectAcceptanceError):
            g06.build_isolated_runtime_env(runtime)
        auth = runtime / "codex-home" / "auth.json"
        auth.write_bytes(b"opaque-test-auth")
        env = g06.build_isolated_runtime_env(runtime)
        self.assertEqual(env["CODEX_HOME"], str(runtime / "codex-home"))
        self.assertEqual(env["HOME"], str(runtime / "process-home"))
        self.assertEqual(env["USERPROFILE"], str(runtime / "process-home"))
        self.assertNotIn("OPENAI_API_KEY", env)
        self.assertFalse((runtime / "codex-home" / "skills").exists())
        self.assertFalse((runtime / "process-home" / ".agents").exists())

    def test_codex_failure_summary_extracts_errors_and_redacts_secrets(self) -> None:
        stdout = "\n".join(
            (
                json.dumps({"type": "thread.started", "thread_id": "not-an-error"}),
                json.dumps(
                    {
                        "type": "turn.failed",
                        "error": {
                            "message": "synthetic failure Bearer private-token",
                            "detail": "api_key=sk-private123456",
                        },
                    }
                ),
            )
        )
        summary = g06.codex_failure_summary(stdout, "refresh_token=private-value")
        encoded = json.dumps(summary)
        self.assertIn("synthetic failure", encoded)
        self.assertIn("<redacted>", encoded)
        self.assertNotIn("private-token", encoded)
        self.assertNotIn("private123456", encoded)
        self.assertNotIn("private-value", encoded)

    def test_runtime_redaction_handles_quoted_tokens_and_jwts(self) -> None:
        jwt = "eyJ" + "a" * 24 + "." + "b" * 16 + "." + "c" * 16
        opaque = "x" * 39 + "1"
        masked_api_key = "sk-projectprefix***keysuffix"
        value = json.dumps(
            {
                "access_token": "quoted-private-token",
                "client_secret": "private-secret",
                "nested": jwt,
                "opaque": opaque,
                "provider_message": f"Rejected key {masked_api_key}",
            }
        )
        redacted = g06.redact_runtime_text(value)
        self.assertNotIn("quoted-private-token", redacted)
        self.assertNotIn("private-secret", redacted)
        self.assertNotIn(jwt, redacted)
        self.assertNotIn(opaque, redacted)
        self.assertNotIn(masked_api_key, redacted)
        self.assertNotIn("sk-", redacted)
        self.assertIn("<redacted>", redacted)
        self.assertIn("<redacted-api-key>", redacted)
        self.assertIn("<redacted-jwt>", redacted)
        self.assertIn("<redacted-opaque>", redacted)

    def test_safe_event_checkpoint_excludes_agent_content(self) -> None:
        event = g06.safe_codex_event(
            json.dumps(
                {
                    "type": "item.completed",
                    "item": {
                        "type": "agent_message",
                        "text": "private prompt and response",
                    },
                }
            ),
            1,
            25,
        )
        self.assertEqual(
            event,
            {
                "sequence": 1,
                "elapsed_ms": 25,
                "type": "item.completed",
                "item_type": "agent_message",
            },
        )
        self.assertNotIn("private", json.dumps(event))

    def test_event_journal_is_bounded_and_drops_raw_invalid_lines(self) -> None:
        journal = g06.CodexEventJournal(limit=3)
        journal.record_stdout("not-json private prompt", 1)
        for index in range(5):
            journal.record_stdout(
                json.dumps({"type": f"event.{index}"}),
                index + 2,
            )
        snapshot = journal.snapshot("running", 10)
        self.assertEqual(snapshot["stdout_lines_seen"], 6)
        self.assertEqual(snapshot["invalid_json_lines_seen"], 1)
        self.assertEqual(snapshot["json_events_seen"], 5)
        self.assertEqual(snapshot["events_dropped"], 2)
        self.assertEqual(len(snapshot["events_retained"]), 3)
        self.assertNotIn("private prompt", json.dumps(snapshot))

    def test_streaming_runner_completes_and_checkpoints_safe_events(self) -> None:
        checkpoints: list[dict[str, object]] = []
        evidence = self.private / "stream-events.json"

        def checkpoint(payload: dict[str, object]) -> None:
            checkpoints.append(payload)
            g06.write_evidence(evidence, "events", payload)

        code = (
            "import json,sys;"
            "sys.stdin.read();"
            "print(json.dumps({'type':'thread.started'}),flush=True);"
            "print(json.dumps({'type':'turn.completed'}),flush=True)"
        )
        completed = g06.run_codex_streaming(
            [sys.executable, "-u", "-c", code],
            cwd=self.root,
            input_text="synthetic input",
            event_checkpoint=checkpoint,
            total_timeout_seconds=3,
            inactivity_timeout_seconds=2,
        )
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(checkpoints[-1]["status"], "completed")
        self.assertEqual(checkpoints[-1]["json_events_seen"], 2)
        self.assertEqual(
            checkpoints[-1]["last_event_type"],
            "turn.completed",
        )
        persisted = json.loads(evidence.read_text(encoding="utf-8"))
        self.assertEqual(persisted["events"], checkpoints[-1])
        self.assertEqual(
            list(evidence.parent.glob(evidence.name + ".tmp-*")),
            [],
        )

    def test_streaming_runner_distinguishes_inactivity_timeout(self) -> None:
        checkpoints: list[dict[str, object]] = []
        code = (
            "import json,time;"
            "print(json.dumps({'type':'thread.started'}),flush=True);"
            "time.sleep(10)"
        )
        with self.assertRaises(g06.CodexProcessTimeout) as raised:
            g06.run_codex_streaming(
                [sys.executable, "-u", "-c", code],
                cwd=self.root,
                input_text="",
                event_checkpoint=checkpoints.append,
                total_timeout_seconds=3,
                inactivity_timeout_seconds=0.25,
            )
        self.assertEqual(raised.exception.timeout_kind, "inactivity")
        self.assertEqual(checkpoints[-1]["status"], "timed_out")
        self.assertTrue(
            checkpoints[-1]["process_tree"]["tree_termination_confirmed"]  # type: ignore[index]
        )

    def test_streaming_runner_distinguishes_total_timeout(self) -> None:
        checkpoints: list[dict[str, object]] = []
        code = (
            "import json,time;"
            "end=time.monotonic()+10;"
            "\nwhile time.monotonic()<end:"
            "\n print(json.dumps({'type':'heartbeat'}),flush=True);"
            "\n time.sleep(0.03)"
        )
        with self.assertRaises(g06.CodexProcessTimeout) as raised:
            g06.run_codex_streaming(
                [sys.executable, "-u", "-c", code],
                cwd=self.root,
                input_text="",
                event_checkpoint=checkpoints.append,
                total_timeout_seconds=0.5,
                inactivity_timeout_seconds=0.4,
            )
        self.assertEqual(raised.exception.timeout_kind, "total")
        self.assertEqual(checkpoints[-1]["status"], "timed_out")
        self.assertGreater(checkpoints[-1]["json_events_seen"], 1)

    def test_streaming_timeout_terminates_descendant_process(self) -> None:
        sentinel = self.root / "descendant-survived.txt"
        child = (
            "import pathlib,time;"
            "time.sleep(1);"
            f"pathlib.Path({str(sentinel)!r}).write_text('survived',encoding='utf-8')"
        )
        parent = (
            "import json,subprocess,sys,time;"
            f"subprocess.Popen([sys.executable,'-c',{child!r}]);"
            "print(json.dumps({'type':'thread.started'}),flush=True);"
            "time.sleep(10)"
        )
        with self.assertRaises(g06.CodexProcessTimeout):
            g06.run_codex_streaming(
                [sys.executable, "-u", "-c", parent],
                cwd=self.root,
                input_text="",
                total_timeout_seconds=3,
                inactivity_timeout_seconds=0.25,
            )
        time.sleep(1)
        self.assertFalse(sentinel.exists())

    def test_streaming_checkpoint_failure_terminates_process(self) -> None:
        terminations: list[int] = []

        def checkpoint(payload: dict[str, object]) -> None:
            if int(payload["json_events_seen"]) >= 1:
                raise RuntimeError("synthetic checkpoint failure")

        def terminate(
            process: subprocess.Popen[str],
        ) -> dict[str, object]:
            process.kill()
            process.wait(timeout=5)
            terminations.append(process.pid)
            return {
                "method": "test",
                "terminated": True,
                "tree_termination_confirmed": True,
                "returncode": process.returncode,
            }

        code = (
            "import json,time;"
            "print(json.dumps({'type':'thread.started'}),flush=True);"
            "time.sleep(10)"
        )
        with self.assertRaisesRegex(
            RuntimeError,
            "synthetic checkpoint failure",
        ):
            g06.run_codex_streaming(
                [sys.executable, "-u", "-c", code],
                cwd=self.root,
                input_text="",
                event_checkpoint=checkpoint,
                total_timeout_seconds=3,
                inactivity_timeout_seconds=2,
                tree_terminator=terminate,
            )
        self.assertEqual(len(terminations), 1)

    def test_content_digest_detects_same_size_same_mtime_change(self) -> None:
        plugin = self.root / "plugin"
        plugin.mkdir()
        payload = plugin / "payload.bin"
        payload.write_bytes(b"before")
        file_stat = payload.stat()
        root_stat = plugin.stat()
        metadata_before = g06.stat_only_tree(plugin)
        content_before = g06.content_tree_digest(plugin)

        payload.write_bytes(b"change")
        payload.touch()
        os.utime(
            payload,
            ns=(file_stat.st_atime_ns, file_stat.st_mtime_ns),
        )
        os.utime(
            plugin,
            ns=(root_stat.st_atime_ns, root_stat.st_mtime_ns),
        )
        self.assertEqual(g06.stat_only_tree(plugin), metadata_before)
        self.assertNotEqual(
            g06.content_tree_digest(plugin)["manifest_sha256"],
            content_before["manifest_sha256"],
        )

    def test_stat_only_tree_normalizes_non_file_sizes(self) -> None:
        boundary = self.root / "boundary"
        child = boundary / "child"
        child.mkdir(parents=True)
        child.joinpath("payload.txt").write_text("payload\n", encoding="utf-8")

        records = {
            path: (kind, mode, size, mtime_ns)
            for path, kind, mode, size, mtime_ns in g06.stat_only_tree(boundary)
        }

        self.assertEqual(records["."][0], "directory")
        self.assertEqual(records["."][2], 0)
        self.assertEqual(records["child"][0], "directory")
        self.assertEqual(records["child"][2], 0)
        self.assertEqual(records["child/payload.txt"][0], "file")
        self.assertEqual(
            records["child/payload.txt"][2],
            child.joinpath("payload.txt").stat().st_size,
        )

    def test_boundary_differences_report_exact_path_and_fields(self) -> None:
        before = {
            "global:user_codex_plugins": (
                (".", "directory", 16895, 0, 100),
                ("payload.txt", "file", 33188, 7, 200),
            ),
        }
        after = {
            "global:user_codex_plugins": (
                (".", "directory", 16895, 0, 100),
                ("payload.txt", "file", 33189, 8, 201),
            ),
        }

        details = g06.boundary_snapshot_differences(before, after)

        self.assertEqual(
            details,
            {
                "changed_labels": ["global:user_codex_plugins"],
                "difference_count": 1,
                "truncated": False,
                "differences": [
                    {
                        "label": "global:user_codex_plugins",
                        "path": "payload.txt",
                        "changed_fields": ["mode", "size", "mtime_ns"],
                        "before": {
                            "kind": "file",
                            "mode": 33188,
                            "size": 7,
                            "mtime_ns": 200,
                        },
                        "after": {
                            "kind": "file",
                            "mode": 33189,
                            "size": 8,
                            "mtime_ns": 201,
                        },
                    },
                ],
            },
        )

    def test_protected_boundary_error_includes_exact_bounded_difference(
        self,
    ) -> None:
        before = {
            "extra:1": (
                ("sentinel.txt", "file", 33188, 7, 200),
            ),
        }
        after = {
            "extra:1": (
                ("sentinel.txt", "file", 33188, 8, 200),
            ),
        }
        with (
            mock.patch.object(
                g06,
                "protected_boundary_snapshot",
                return_value=after,
            ),
            self.assertRaises(g06.RealProjectAcceptanceError) as raised,
        ):
            g06.assert_protected_boundaries_unchanged(
                before,
                self.project,
                self.allowed,
            )

        message = str(raised.exception)
        self.assertIn('"path": "sentinel.txt"', message)
        self.assertIn('"changed_fields": ["size"]', message)
        self.assertNotIn("payload", message)

    def test_plugin_content_snapshot_never_reads_auth_path(self) -> None:
        plugin = self.root / "plugins"
        plugin.mkdir()
        plugin.joinpath("payload.txt").write_text("plugin\n", encoding="utf-8")
        auth = self.root / "auth.json"
        auth.write_text("must-not-be-read\n", encoding="utf-8")
        scanned: list[Path] = []

        def digest(path: Path) -> dict[str, object]:
            scanned.append(path)
            return {"manifest_sha256": "test"}

        with (
            mock.patch.object(
                g06.plugin_boundary,
                "protected_user_paths",
                return_value={
                    "user_codex_plugins": plugin,
                    "user_codex_auth": auth,
                },
            ),
            mock.patch.object(g06, "content_tree_digest", side_effect=digest),
        ):
            snapshot = g06.protected_plugin_content_snapshot()
        self.assertEqual(scanned, [plugin])
        self.assertEqual(
            snapshot,
            {"global:user_codex_plugins": {"manifest_sha256": "test"}},
        )

    def test_init_result_requires_exact_project_skill_hash_and_handback(self) -> None:
        self.prepare_and_deliver()
        result = self.init_payload(created=["STATUS.md", "REVIEW-LOG.md"])
        g06.validate_init_result(self.project, result)
        result["skill_source_sha256"] = "0" * 64
        with self.assertRaises(g06.RealProjectAcceptanceError):
            g06.validate_init_result(self.project, result)

    def test_run_init_rejects_non_governance_mutation_from_runner(self) -> None:
        self.prepare_and_deliver()
        output = ROOT / ".private-provenance" / "g06-test-output" / f"{self.root.name}.json"

        def bad_runner(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
            self.project.joinpath("expense_splitter.py").write_text("bad\n", encoding="utf-8")
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(json.dumps(self.init_payload()), encoding="utf-8")
            return subprocess.CompletedProcess(command, 0, "", "")

        try:
            with self.assertRaises(g06.RealProjectAcceptanceError):
                g06.run_real_init(self.project, self.allowed, output, runner=bad_runner)
        finally:
            if output.exists():
                output.unlink()

    def test_run_init_accepts_exact_governance_change_report(self) -> None:
        self.prepare_and_deliver()
        output = ROOT / ".private-provenance" / "g06-test-output" / f"{self.root.name}-good.json"
        runtime = self.private / "isolated-runtime"
        auth = runtime / "codex-home" / "auth.json"
        auth.parent.mkdir(parents=True)
        auth.write_bytes(b"opaque-test-auth")
        observed_env: dict[str, str] = {}

        def good_runner(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
            observed_env.update(kwargs["env"])  # type: ignore[arg-type]
            self.write_chinese_governance()
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(
                json.dumps(self.init_payload(created=["STATUS.md"])),
                encoding="utf-8",
            )
            return subprocess.CompletedProcess(command, 0, "", "")

        try:
            result = g06.run_real_init(
                self.project,
                self.allowed,
                output,
                isolated_runtime_root=runtime,
                runner=good_runner,
            )
            self.assertEqual(result["created_governance_paths"], ["STATUS.md"])
            self.assertEqual(result["updated_governance_paths"], [])
            self.assertTrue(result["isolated_runtime"])
            self.assertEqual(observed_env["CODEX_HOME"], str(runtime / "codex-home"))
            self.assertEqual(
                result["governance_language_acceptance"]["expected_language"],
                "zh-CN",
            )
        finally:
            if output.exists():
                output.unlink()

    def test_run_init_accepts_wsl_carrier_command(self) -> None:
        self.prepare_and_deliver()
        output = (
            ROOT
            / ".private-provenance"
            / "g06-test-output"
            / f"{self.root.name}-wsl-good.json"
        )
        observed_command: list[str] = []

        def path_mapper(path: Path) -> str:
            if path == self.project.resolve():
                return "/mnt/h/uat/retained-project"
            return "/mnt/h/private/init.json"

        def good_runner(
            command: list[str],
            **kwargs: object,
        ) -> subprocess.CompletedProcess[str]:
            observed_command.extend(command)
            self.assertNotIn("env", kwargs)
            self.write_chinese_governance()
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(
                json.dumps(self.init_payload(created=["STATUS.md"])),
                encoding="utf-8",
            )
            return subprocess.CompletedProcess(command, 0, "", "")

        try:
            result = g06.run_real_init(
                self.project,
                self.allowed,
                output,
                carrier="wsl2",
                wsl_distribution="CoTend-G06",
                wsl_runtime_root="/home/cotend/g06-runtime-test",
                wsl_executable="wsl.exe",
                path_mapper=path_mapper,
                runner=good_runner,
            )
            self.assertEqual(result["carrier"], "wsl2")
            self.assertTrue(result["isolated_runtime"])
            self.assertEqual(
                observed_command[:7],
                [
                    "wsl.exe",
                    "-d",
                    "CoTend-G06",
                    "-u",
                    "cotend",
                    "--",
                    "/usr/bin/env",
                ],
            )
        finally:
            if output.exists():
                output.unlink()

    def test_run_init_rejects_english_governance_despite_zh_status_claim(
        self,
    ) -> None:
        self.prepare_and_deliver()
        output = (
            ROOT
            / ".private-provenance"
            / "g06-test-output"
            / f"{self.root.name}-language-negative.json"
        )
        negative = ROOT / "tests" / "fixtures" / "g06-language-negative"
        created = ["STATUS.md", "REVIEW-LOG.md", "QUALITY-SIGNALS.md"]

        def false_pass_runner(
            command: list[str],
            **_: object,
        ) -> subprocess.CompletedProcess[str]:
            for relative in created:
                shutil.copy2(negative / relative, self.project / relative)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(
                json.dumps(self.init_payload(created=created)),
                encoding="utf-8",
            )
            return subprocess.CompletedProcess(command, 0, "", "")

        try:
            with self.assertRaisesRegex(
                g06.RealProjectAcceptanceError,
                "Chinese content oracle",
            ):
                g06.run_real_init(
                    self.project,
                    self.allowed,
                    output,
                    runner=false_pass_runner,
                )
        finally:
            if output.exists():
                output.unlink()

    def test_run_init_rejects_status_language_declaration_mismatch(self) -> None:
        self.prepare_and_deliver()
        output = (
            ROOT
            / ".private-provenance"
            / "g06-test-output"
            / f"{self.root.name}-language-declaration.json"
        )

        def mismatch_runner(
            command: list[str],
            **_: object,
        ) -> subprocess.CompletedProcess[str]:
            self.write_chinese_governance(declared_language="en")
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(
                json.dumps(self.init_payload(created=["STATUS.md"])),
                encoding="utf-8",
            )
            return subprocess.CompletedProcess(command, 0, "", "")

        try:
            with self.assertRaisesRegex(
                g06.RealProjectAcceptanceError,
                "governance language differs",
            ):
                g06.run_real_init(
                    self.project,
                    self.allowed,
                    output,
                    runner=mismatch_runner,
                )
        finally:
            if output.exists():
                output.unlink()

    def test_run_init_rejects_managed_skill_mutation(self) -> None:
        self.prepare_and_deliver()
        output = ROOT / ".private-provenance" / "g06-test-output" / f"{self.root.name}-skill.json"

        def bad_runner(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
            skill = self.project / g06.INIT_SKILL
            skill.write_text(skill.read_text(encoding="utf-8") + "\n", encoding="utf-8")
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(json.dumps(self.init_payload()), encoding="utf-8")
            return subprocess.CompletedProcess(command, 0, "", "")

        try:
            with self.assertRaises(g06.RealProjectAcceptanceError):
                g06.run_real_init(self.project, self.allowed, output, runner=bad_runner)
        finally:
            if output.exists():
                output.unlink()

    def test_run_init_rejects_protected_project_mutation(self) -> None:
        self.prepare_and_deliver()
        protected = self.root / "other-project"
        protected.mkdir()
        sentinel = protected / "sentinel.txt"
        sentinel.write_text("before\n", encoding="utf-8")
        output = ROOT / ".private-provenance" / "g06-test-output" / f"{self.root.name}-boundary.json"

        def bad_runner(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
            sentinel.write_text("after\n", encoding="utf-8")
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(json.dumps(self.init_payload()), encoding="utf-8")
            return subprocess.CompletedProcess(command, 7, "", "synthetic runner failure")

        try:
            with self.assertRaises(g06.RealProjectAcceptanceError) as raised:
                g06.run_real_init(
                    self.project,
                    self.allowed,
                    output,
                    protected_paths=(protected,),
                    runner=bad_runner,
                )
            self.assertIn('"returncode": 7', str(raised.exception))
            self.assertIn("synthetic runner failure", str(raised.exception))
        finally:
            if output.exists():
                output.unlink()

    def test_live_sibling_drift_does_not_mask_json_failure(self) -> None:
        self.prepare_and_deliver()
        sibling = self.allowed / "active-sibling"
        sibling.mkdir()
        sentinel = sibling / "build-output.txt"
        sentinel.write_text("before\n", encoding="utf-8")
        output = ROOT / ".private-provenance" / "g06-test-output" / f"{self.root.name}-live.json"

        def failing_runner(
            command: list[str],
            **kwargs: object,
        ) -> subprocess.CompletedProcess[str]:
            sentinel.write_text("after\n", encoding="utf-8")
            stdout = json.dumps(
                {
                    "type": "turn.failed",
                    "error": {"message": "observable synthetic failure"},
                }
            )
            return subprocess.CompletedProcess(command, 9, stdout, "")

        try:
            with self.assertRaises(g06.RealProjectAcceptanceError) as raised:
                g06.run_real_init(
                    self.project,
                    self.allowed,
                    output,
                    runner=failing_runner,
                )
            message = str(raised.exception)
            self.assertIn("observable synthetic failure", message)
            self.assertIn("uat_sibling:active-sibling", message)
        finally:
            if output.exists():
                output.unlink()

    def test_delivery_rollback_restores_r11_then_current_r12(self) -> None:
        self.prepare_and_deliver()
        result = g06.rollback_restore(
            self.project,
            self.allowed,
            self.source,
            require_product=False,
        )
        self.assertEqual(result["rollback_target"], g06.R11_ID)
        self.assertEqual(result["restored_target"], g06.R12_ID)
        self.assertTrue(result["non_delivery_files_unchanged"])


if __name__ == "__main__":
    unittest.main()
