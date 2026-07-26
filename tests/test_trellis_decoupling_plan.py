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

    def validate(
        self,
        contract: dict | None = None,
        inventory: dict[str, int] | None = None,
    ) -> dict:
        return decoupling.validate_contract(
            self.contract if contract is None else contract,
            self.document_text,
            self.inventory if inventory is None else inventory,
            self.tracked_paths,
        )

    def test_current_migration_preserves_baseline_and_advances_all_capabilities(
        self,
    ) -> None:
        result = self.validate()
        self.assertEqual(result["capabilities"], 8)
        self.assertEqual(result["gates"], 6)
        self.assertEqual(result["runtime_mentions"], 0)
        self.assertEqual(result["runtime_files"], 0)
        self.assertTrue(result["skill_behavior_changed"])
        self.assertEqual(result["native_capabilities_verified"], 8)
        self.assertEqual(result["cumulative_gates_verified"], 3)

    def test_immutable_baseline_change_is_rejected(self) -> None:
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

    def test_verified_capability_cannot_regress_to_baseline(self) -> None:
        changed = copy.deepcopy(self.contract)
        changed["capabilities"][6]["status"] = "baseline_frozen"
        with self.assertRaises(decoupling.TrellisDecouplingPlanError):
            self.validate(changed)

    def test_current_inventory_drift_is_rejected(self) -> None:
        changed = copy.deepcopy(self.contract)
        changed["current_runtime"]["file_mentions"][
            "skills/cotend-collaboration/references/plan-tree.md"
        ] = 1
        changed["current_runtime"]["mention_count"] = 1
        changed["current_runtime"]["file_count"] = 1
        with self.assertRaises(decoupling.TrellisDecouplingPlanError):
            self.validate(changed)

    def test_code_and_contract_cannot_drift_together_inside_allowed_path(self) -> None:
        path = "skills/cotend-collaboration/references/plan-tree.md"
        changed_contract = copy.deepcopy(self.contract)
        changed_inventory = copy.deepcopy(self.inventory)
        changed_contract["current_runtime"]["file_mentions"][path] = 1
        changed_contract["current_runtime"]["mention_count"] = 1
        changed_contract["current_runtime"]["file_count"] = 1
        changed_inventory[path] = 1
        with self.assertRaises(decoupling.TrellisDecouplingPlanError):
            self.validate(changed_contract, changed_inventory)

    def test_td08_evidence_cannot_be_removed(self) -> None:
        changed = copy.deepcopy(self.contract)
        changed["capabilities"][-1]["evidence"].pop()
        with self.assertRaises(decoupling.TrellisDecouplingPlanError):
            self.validate(changed)

    def test_td01_evidence_cannot_be_removed(self) -> None:
        changed = copy.deepcopy(self.contract)
        changed["capabilities"][0]["evidence"].pop()
        with self.assertRaises(decoupling.TrellisDecouplingPlanError):
            self.validate(changed)

    def test_td02_evidence_cannot_be_removed(self) -> None:
        changed = copy.deepcopy(self.contract)
        changed["capabilities"][1]["evidence"].pop()
        with self.assertRaises(decoupling.TrellisDecouplingPlanError):
            self.validate(changed)

    def test_td03_evidence_cannot_be_removed(self) -> None:
        changed = copy.deepcopy(self.contract)
        changed["capabilities"][2]["evidence"].pop()
        with self.assertRaises(decoupling.TrellisDecouplingPlanError):
            self.validate(changed)

    def test_td04_evidence_cannot_be_removed(self) -> None:
        changed = copy.deepcopy(self.contract)
        changed["capabilities"][3]["evidence"].pop()
        with self.assertRaises(decoupling.TrellisDecouplingPlanError):
            self.validate(changed)

    def test_td05_evidence_cannot_be_removed(self) -> None:
        changed = copy.deepcopy(self.contract)
        changed["capabilities"][4]["evidence"] = []
        with self.assertRaises(decoupling.TrellisDecouplingPlanError):
            self.validate(changed)

    def test_td06_evidence_cannot_be_removed(self) -> None:
        changed = copy.deepcopy(self.contract)
        changed["capabilities"][5]["evidence"].pop()
        with self.assertRaises(decoupling.TrellisDecouplingPlanError):
            self.validate(changed)

    def test_td07_evidence_cannot_be_removed(self) -> None:
        changed = copy.deepcopy(self.contract)
        changed["capabilities"][6]["evidence"].pop()
        with self.assertRaises(decoupling.TrellisDecouplingPlanError):
            self.validate(changed)

    def test_g03_evidence_and_completion_cannot_be_removed(self) -> None:
        changed = copy.deepcopy(self.contract)
        changed["gates"][2]["evidence"].pop()
        with self.assertRaises(decoupling.TrellisDecouplingPlanError):
            self.validate(changed)

        changed = copy.deepcopy(self.contract)
        changed["gates"][2]["status"] = "not_started"
        with self.assertRaises(decoupling.TrellisDecouplingPlanError):
            self.validate(changed)

    def test_g04_evidence_and_completion_cannot_be_removed(self) -> None:
        changed = copy.deepcopy(self.contract)
        changed["gates"][3]["evidence"].pop()
        with self.assertRaises(decoupling.TrellisDecouplingPlanError):
            self.validate(changed)

        changed = copy.deepcopy(self.contract)
        changed["gates"][3]["status"] = "not_started"
        with self.assertRaises(decoupling.TrellisDecouplingPlanError):
            self.validate(changed)

    def test_g05_completion_cannot_regress(self) -> None:
        changed = copy.deepcopy(self.contract)
        changed["gates"][4]["status"] = "not_started"
        with self.assertRaises(decoupling.TrellisDecouplingPlanError):
            self.validate(changed)

    def test_g06_cannot_advance_during_g05(self) -> None:
        changed = copy.deepcopy(self.contract)
        changed["gates"][5]["status"] = "complete"
        with self.assertRaises(decoupling.TrellisDecouplingPlanError):
            self.validate(changed)

    def test_g05_slice_must_record_runtime_and_target_change(self) -> None:
        changed = copy.deepcopy(self.contract)
        changed["this_slice"]["skill_behavior_changed"] = False
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
