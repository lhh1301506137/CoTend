from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import verify_trellis_decoupling_plan as decoupling  # noqa: E402


class TrellisDecouplingPlanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(decoupling.CONTRACT_PATH.read_text(encoding="utf-8"))
        cls.document_text = decoupling.DOCUMENT_PATH.read_text(encoding="utf-8")
        cls.inventory = decoupling.runtime_inventory()
        cls.tracked_paths = decoupling.tracked_paths()

    def validate(self, contract: dict | None = None) -> dict:
        return decoupling.validate_contract(
            self.contract if contract is None else contract,
            self.document_text,
            self.inventory,
            self.tracked_paths,
        )

    def test_current_baseline_is_exact_and_behavior_unchanged(self) -> None:
        result = self.validate()
        self.assertEqual(result["capabilities"], 8)
        self.assertEqual(result["gates"], 6)
        self.assertEqual(result["runtime_mentions"], 241)
        self.assertEqual(result["runtime_files"], 22)
        self.assertFalse(result["skill_behavior_changed"])

    def test_early_runtime_text_deletion_is_rejected(self) -> None:
        changed = copy.deepcopy(self.contract)
        changed["baseline"]["file_mentions"][
            "skills/cotend-project-init/SKILL.md"
        ] -= 1
        with self.assertRaises(decoupling.TrellisDecouplingPlanError):
            self.validate(changed)

    def test_missing_capability_is_rejected(self) -> None:
        changed = copy.deepcopy(self.contract)
        changed["capabilities"].pop()
        with self.assertRaises(decoupling.TrellisDecouplingPlanError):
            self.validate(changed)

    def test_capability_cannot_advance_without_implementation(self) -> None:
        changed = copy.deepcopy(self.contract)
        changed["capabilities"][0]["status"] = "native_parity_verified"
        with self.assertRaises(decoupling.TrellisDecouplingPlanError):
            self.validate(changed)

    def test_mechanical_rename_cannot_be_enabled(self) -> None:
        changed = copy.deepcopy(self.contract)
        changed["target"]["mechanical_rename_allowed"] = True
        with self.assertRaises(decoupling.TrellisDecouplingPlanError):
            self.validate(changed)

    def test_tracked_trellis_path_is_rejected(self) -> None:
        with self.assertRaises(decoupling.TrellisDecouplingPlanError):
            decoupling.validate_contract(
                self.contract,
                self.document_text,
                self.inventory,
                self.tracked_paths + [".trellis/config.yaml"],
            )


if __name__ == "__main__":
    unittest.main()
