from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "cotend-collaboration" / "scripts" / "failure_memory.py"


def load_module():
    spec = importlib.util.spec_from_file_location("cotend_failure_memory", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("failure memory module could not be loaded")
    module = importlib.util.module_from_spec(spec)
    previous = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = previous
    return module


class CoTendFailureMemoryTests(unittest.TestCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-X", "utf8", str(SCRIPT), *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )

    def test_catalog_matches_canonical_markdown_records(self) -> None:
        result = self.run_cli("validate")
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["schema"], "cotend.failure-catalog.v1")
        self.assertEqual(payload["record_count"], 2)
        self.assertEqual(
            [record["id"] for record in payload["records"]],
            ["AFP-001", "AFP-002"],
        )

    def test_generic_root_skill_alone_admits_no_pattern(self) -> None:
        result = self.run_cli(
            "select", "--skill", "cotend-collaboration"
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["selected_count"], 0)
        self.assertEqual(payload["cards"], [])

    def test_specific_skill_or_task_tag_returns_compact_guards(self) -> None:
        by_skill = json.loads(
            self.run_cli(
                "select", "--skill", "cotend-session-handoff"
            ).stdout
        )
        self.assertEqual(by_skill["selected_count"], 1)
        self.assertEqual(by_skill["cards"][0]["id"], "AFP-002")
        self.assertFalse(by_skill["full_records_loaded_into_output"])

        by_tag = json.loads(
            self.run_cli("select", "--tag", "main-chain").stdout
        )
        self.assertEqual(by_tag["cards"][0]["id"], "AFP-001")
        self.assertLessEqual(by_tag["selected_count"], 3)

    def test_limit_above_hard_cap_fails_closed(self) -> None:
        result = self.run_cli("select", "--tag", "evidence", "--limit", "4")
        self.assertEqual(result.returncode, 2)
        self.assertIn("ordinary result limit must be 1..3", result.stderr)

    def test_selected_record_hash_mismatch_fails_closed(self) -> None:
        module = load_module()
        catalog = module.validate_catalog()
        catalog["records"][0]["record_sha256"] = "0" * 64
        with self.assertRaisesRegex(
            module.FailureMemoryError, "selected record hash differs"
        ):
            module.select_cards(
                catalog=catalog,
                tags=["main-chain"],
                skills=[],
                limit=3,
            )


if __name__ == "__main__":
    unittest.main()
