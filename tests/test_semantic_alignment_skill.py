from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
import unittest
import unicodedata
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
HELPER = (
    ROOT
    / "skills"
    / "cotend-semantic-alignment"
    / "scripts"
    / "semantic-contract.mjs"
)


def normalize(value: Any) -> Any:
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value.replace("\r\n", "\n").replace("\r", "\n"))
    if isinstance(value, list):
        return [normalize(item) for item in value]
    if isinstance(value, dict):
        return {
            unicodedata.normalize("NFC", key): normalize(child)
            for key, child in value.items()
        }
    return value


class SemanticAlignmentSkillTests(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        if shutil.which("node") is None:
            raise unittest.SkipTest("Node.js is required by the shipped semantic helper")

    def payload(self) -> dict[str, Any]:
        return {
            "schema": "cotend.semantic-contract.v1",
            "contract_id": "SC-calculator-L2-v1",
            "node_id": "calculator-split",
            "semantic_level": "L2",
            "parent_node_id": "calculator-mvp",
            "scope": "target_feature",
            "meaning": {
                "complete_goal": "Split a bill exactly by cents.\r\nNever lose value.",
                "user_visible_result": "Every share and the total are shown.",
            },
            "protected_product_rules": [
                "Remainder cents are assigned in participant order."
            ],
        }

    def run_helper(
        self,
        command: str,
        *,
        input_path: Path,
        expected: str | None = None,
        contract_id: str | None = None,
        decision_ref: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        arguments = ["node", str(HELPER), command, "--input", str(input_path)]
        if expected is not None:
            arguments.extend(["--expected", expected])
        if contract_id is not None:
            arguments.extend(["--contract-id", contract_id])
        if decision_ref is not None:
            arguments.extend(["--decision-ref", decision_ref])
        return subprocess.run(
            arguments,
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )

    def test_semantic_alignment_is_direct_writable_and_init_is_report_only(self) -> None:
        semantic = (HELPER.parent.parent / "SKILL.md").read_text(encoding="utf-8")
        init = (ROOT / "skills" / "cotend-init" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        authority = (
            ROOT
            / "skills"
            / "cotend-collaboration"
            / "references"
            / "authority-and-triggers.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Invoke this Skill directly.", semantic)
        self.assertIn(
            "Do not run or require `cotend-init` or full `cotend-project-init`",
            semantic,
        )
        self.assertIn("This pointer is a report-only handback", init)
        self.assertIn("classified_by_init: no", init)
        self.assertIn("executed: no", init)
        self.assertIn(
            "Route explicit writable project/feature meaning work directly",
            authority,
        )

    def test_semantic_contract_digest_is_canonical_and_verifiable(self) -> None:
        payload = self.payload()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            compact = root / "compact.json"
            formatted = root / "formatted.json"
            compact.write_text(
                json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
                encoding="utf-8",
            )
            formatted.write_text(
                json.dumps(
                    dict(reversed(list(payload.items()))),
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            first = self.run_helper("digest", input_path=compact)
            second = self.run_helper("digest", input_path=formatted)
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            first_result = json.loads(first.stdout)
            second_result = json.loads(second.stdout)
            self.assertEqual(first_result["digest"], second_result["digest"])

            canonical = json.dumps(
                normalize(payload),
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            )
            expected = "sha256:" + hashlib.sha256(
                canonical.encode("utf-8")
            ).hexdigest()
            self.assertEqual(first_result["canonical_json"], canonical)
            self.assertEqual(first_result["digest"], expected)

            verified = self.run_helper(
                "verify",
                input_path=formatted,
                expected=expected,
            )
            self.assertEqual(verified.returncode, 0, verified.stderr)
            self.assertTrue(json.loads(verified.stdout)["verified"])

    def test_semantic_contract_rejects_mismatch_and_normalized_duplicate_keys(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            payload_path = root / "payload.json"
            payload_path.write_text(
                json.dumps(self.payload(), ensure_ascii=False),
                encoding="utf-8",
            )
            mismatch = self.run_helper(
                "verify",
                input_path=payload_path,
                expected="sha256:" + ("0" * 64),
            )
            self.assertEqual(mismatch.returncode, 2)
            self.assertIn("digest mismatch", mismatch.stderr)

            ambiguous = self.payload()
            ambiguous["meaning"] = {"é": "one", "e\u0301": "two"}
            ambiguous_path = root / "ambiguous.json"
            ambiguous_path.write_text(
                json.dumps(ambiguous, ensure_ascii=False),
                encoding="utf-8",
            )
            rejected = self.run_helper("digest", input_path=ambiguous_path)
            self.assertEqual(rejected.returncode, 2)
            self.assertIn("normalization-ambiguous", rejected.stderr)

    def test_semantic_contract_verify_log_binds_one_decision(self) -> None:
        payload = self.payload()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            payload_path = root / "payload.json"
            payload_path.write_text(
                json.dumps(payload, ensure_ascii=False),
                encoding="utf-8",
            )
            digest_result = self.run_helper("digest", input_path=payload_path)
            self.assertEqual(digest_result.returncode, 0, digest_result.stderr)
            digest = json.loads(digest_result.stdout)["digest"]
            decision_ref = "DEC-" + "20260723-001"
            log_path = root / "DECISIONS.md"
            log_path.write_text(
                "# Decision Log\n\n"
                f"## {decision_ref}: Confirm calculator semantics\n\n"
                "```cotend.semantic-contract.v1\n"
                + json.dumps(payload, ensure_ascii=False, indent=2)
                + "\n```\n",
                encoding="utf-8",
            )

            verified = self.run_helper(
                "verify-log",
                input_path=log_path,
                expected=digest,
                contract_id=payload["contract_id"],
                decision_ref=decision_ref,
            )
            self.assertEqual(verified.returncode, 0, verified.stderr)
            result = json.loads(verified.stdout)
            self.assertTrue(result["verified"])
            self.assertEqual(result["payload_count"], 1)
            self.assertEqual(result["decision_ref"], decision_ref)


if __name__ == "__main__":
    unittest.main()
