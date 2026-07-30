from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class CoTendV176AdaptationTests(unittest.TestCase):
    def test_source_is_cotend_native_and_trellis_free(self) -> None:
        offenders = []
        for path in SKILLS.rglob("*"):
            if path.is_file() and path.suffix in {".md", ".yaml", ".json", ".py"}:
                if "trellis" in path.read_text(
                    encoding="utf-8", errors="ignore"
                ).casefold():
                    offenders.append(path.relative_to(ROOT).as_posix())
        self.assertEqual(offenders, [])

    def test_karpathy_adaptation_is_disclosed_under_mit(self) -> None:
        registry = json.loads(
            (ROOT / "THIRD-PARTY-SOURCES.json").read_text(encoding="utf-8")
        )
        component = next(
            item
            for item in registry["components"]
            if item["component"] == "karpathy-guidelines"
        )
        self.assertEqual(component["relationship"], "adapted_third_party")
        self.assertEqual(component["license"], "MIT")
        self.assertEqual(
            component["content_policy"], "cotend_adapted_from_reviewed_source"
        )
        self.assertIn("CoTend adaptation", component["required_attribution"])
        notice = (ROOT / "THIRD-PARTY-NOTICES.md").read_text(encoding="utf-8")
        self.assertIn("## karpathy-guidelines", notice)
        self.assertIn("Relationship: adapted third party", notice)
        self.assertIn("execution-authorization precedence rule", notice)

    def test_collaboration_owns_bounded_repair_and_impact_authority(self) -> None:
        authority = text(
            "skills/cotend-collaboration/references/authority-and-triggers.md"
        )
        self.assertIn("## Bounded Failure Repair Before Handback", authority)
        self.assertIn("one bounded repair and recheck", authority)
        self.assertIn("Architecture authority is classified by impact", authority)
        self.assertIn("same impact classification", authority)
        self.assertIn("cotend-collaboration-v1.76", text(
            "skills/cotend-collaboration/SKILL.md"
        ))

    def test_project_understanding_reconstruction_has_one_native_owner(self) -> None:
        plan = text("skills/cotend-collaboration/references/plan-tree.md")
        templates = text("skills/cotend-collaboration/references/templates.md")
        project_init = text("skills/cotend-project-init/SKILL.md")
        self.assertIn("## Project Understanding Reconstruction", plan)
        for trigger in (
            "first_project_entry",
            "same_primary_new_session",
            "confirmed_primary_takeover",
            "cross_domain_architecture_or_cumulative_main_chain",
            "drift_rework_route_break_or_stale_assumption",
        ):
            self.assertIn(trigger, plan)
        self.assertIn("full_current_mvp", plan)
        self.assertIn("affected_l1_domain", plan)
        self.assertIn("active_path_delta", plan)
        self.assertIn("project_understanding_reconstruction:", templates)
        self.assertIn("Do not define a second project-understanding", project_init)

    def test_codegraph_read_equivalence_and_no_automatic_init(self) -> None:
        context = text(
            "skills/cotend-collaboration/references/code-context-harness.md"
        )
        maintenance = text(
            "skills/cotend-project-init/references/maintenance-and-coordination.md"
        )
        closeout = text(
            "skills/cotend-project-init/references/verification-and-closeout-workflow.md"
        )
        self.assertIn("fresh verbatim source is Read-equivalent", context)
        self.assertIn("Never run `codegraph init .` without the user's approval", context)
        self.assertIn("wait for explicit user approval", maintenance)
        self.assertIn("ask the user before running `codegraph init .`", closeout)

    def test_session_handoff_is_thin_literal_gate(self) -> None:
        entry = text("skills/cotend-session-handoff/SKILL.md")
        workflow = text(
            "skills/cotend-session-handoff/references/session-handoff-workflow.md"
        )
        self.assertLessEqual(len(entry.splitlines()), 45)
        self.assertIn("If the literal is absent:", entry)
        self.assertIn("do not call tools", entry)
        self.assertIn("references/session-handoff-workflow.md", entry)
        self.assertIn("full_current_mvp", workflow)
        self.assertIn("Project Understanding Reconstruction", workflow)

    def test_project_init_router_and_model_upgrade_contracts_are_current(self) -> None:
        project_init = text("skills/cotend-project-init/SKILL.md")
        router = text(
            "skills/cotend-project-init/scripts/maintain_project_agents_router.py"
        )
        model_upgrade = text("skills/cotend-model-upgrade/SKILL.md")
        self.assertIn("cotend-collaboration-v1.76", project_init)
        self.assertIn("cotend.project-router.v1", router)
        self.assertIn("COTEND:PROJECT-ROUTER:START", router)
        self.assertIn("Version: 1.14", model_upgrade)
        self.assertIn("full_current_mvp", model_upgrade)
        self.assertIn("impact-neutral L3/L4", model_upgrade)


if __name__ == "__main__":
    unittest.main()
