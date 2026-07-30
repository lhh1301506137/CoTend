from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "skills"
    / "cotend-project-init"
    / "scripts"
    / "maintain_project_agents_router.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location("cotend_project_router", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("router module could not be loaded")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class CoTendProjectAgentsRouterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.router = load_module()

    def test_create_check_and_idempotent_apply(self) -> None:
        with tempfile.TemporaryDirectory(prefix="cotend-router-") as temporary:
            root = Path(temporary)
            created = self.router.update_agents(root, "zh-CN", apply=True)
            self.assertEqual(created["contract"], "cotend.project-router.v1")
            self.assertEqual(created["result"], "created")
            text = (root / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("<!-- COTEND:PROJECT-ROUTER:START -->", text)
            self.assertIn("$cotend-collaboration", text)
            self.assertIn("$cotend-session-handoff", text)
            self.assertNotIn("Trellis", text)

            checked = self.router.update_agents(root, "zh-CN", apply=False)
            self.assertEqual(checked["result"], "unchanged")
            second = self.router.update_agents(root, "zh-CN", apply=True)
            self.assertEqual(second["result"], "unchanged")
            self.assertEqual(text, (root / "AGENTS.md").read_text(encoding="utf-8"))

    def test_preserves_bom_newline_and_bytes_outside_managed_block(self) -> None:
        with tempfile.TemporaryDirectory(prefix="cotend-router-bom-") as temporary:
            root = Path(temporary)
            agents = root / "AGENTS.md"
            original = b"\xef\xbb\xbf# User Rules\r\n\r\nKeep this exact.\r\n"
            agents.write_bytes(original)
            self.router.update_agents(root, "en", apply=True)
            first = agents.read_bytes()
            self.assertTrue(first.startswith(original))
            self.assertIn(b"\r\n<!-- COTEND:PROJECT-ROUTER:START -->\r\n", first)

            self.router.update_agents(root, "zh-CN", apply=True)
            second = agents.read_bytes()
            self.assertTrue(second.startswith(original))
            self.assertIn("CoTend 项目路由".encode("utf-8"), second)

    def test_malformed_or_duplicate_markers_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory(prefix="cotend-router-invalid-") as temporary:
            root = Path(temporary)
            agents = root / "AGENTS.md"
            agents.write_text(
                "<!-- COTEND:PROJECT-ROUTER:START -->\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                self.router.RouterError, "managed_marker_pair_incomplete"
            ):
                self.router.update_agents(root, "en", apply=False)

            agents.write_text(
                (
                    "<!-- COTEND:PROJECT-ROUTER:START -->\n"
                    "<!-- COTEND:PROJECT-ROUTER:END -->\n"
                    "<!-- COTEND:PROJECT-ROUTER:START -->\n"
                    "<!-- COTEND:PROJECT-ROUTER:END -->\n"
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                self.router.RouterError, "managed_marker_pair_duplicate"
            ):
                self.router.update_agents(root, "en", apply=False)

    def test_invalid_utf8_and_noncanonical_tag_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory(prefix="cotend-router-invalid-") as temporary:
            root = Path(temporary)
            (root / "AGENTS.md").write_bytes(b"\xff")
            with self.assertRaisesRegex(
                self.router.RouterError, "agents_invalid_utf8"
            ):
                self.router.update_agents(root, "en", apply=False)
            with self.assertRaisesRegex(
                self.router.RouterError, "normalized_tag_not_canonical"
            ):
                self.router.normalize_tag("ZH-cn")


if __name__ == "__main__":
    unittest.main()
