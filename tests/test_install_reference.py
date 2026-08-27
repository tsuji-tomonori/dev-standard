from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools import install_reference


class InstallReferenceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.target = Path(self.temp.name) / "target"
        self.target.mkdir()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_dry_run_does_not_write(self) -> None:
        copied, unchanged, conflicts = install_reference.install(
            self.target, ["default"], apply=False, force=False
        )
        self.assertGreater(copied, 0)
        self.assertEqual((unchanged, conflicts), (0, 0))
        self.assertFalse((self.target / ".agents").exists())

    def test_default_installs_only_entry_and_three_pillars(self) -> None:
        install_reference.install(self.target, ["default"], apply=True, force=False)
        installed = {
            path.parent.name
            for path in (self.target / ".agents" / "skills").glob("*/SKILL.md")
        }
        self.assertEqual(
            installed,
            {
                "chat-first-development",
                "maintain-canonical-requirements",
                "generate-implementation-design",
                "inspect-quality-gates",
            },
        )
        self.assertFalse((self.target / "governance").exists())
        self.assertFalse((self.target / ".github").exists())

    def test_default_preserves_existing_repository_policy_byte_for_byte(self) -> None:
        workflow = self.target / ".github" / "workflows" / "target.yml"
        rules = self.target / ".github" / "target-rules.json"
        workflow.parent.mkdir(parents=True)
        workflow.write_bytes(b"name: target-owned\n")
        rules.write_bytes(b'{"merge":"rebase"}\n')
        before = {workflow: workflow.read_bytes(), rules: rules.read_bytes()}

        install_reference.install(self.target, ["default"], apply=True, force=False)

        self.assertEqual({path: path.read_bytes() for path in before}, before)
        self.assertEqual(
            sorted(path.relative_to(self.target).as_posix() for path in workflow.parent.iterdir()),
            [".github/workflows/target.yml"],
        )

    def test_existing_instructions_are_merged_only_inside_managed_block(self) -> None:
        agents = self.target / "AGENTS.md"
        agents.write_text("target-owned instruction\n", encoding="utf-8")
        install_reference.install(self.target, ["default"], apply=True, force=False)
        text = agents.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("target-owned instruction\n"))
        self.assertEqual(text.count(install_reference.INSTRUCTION_START), 1)
        self.assertIn("3本だけ", text)

    def test_conflict_fails_before_other_writes_and_force_is_explicit(self) -> None:
        conflict = self.target / ".agents" / "skills" / "chat-first-development" / "SKILL.md"
        conflict.parent.mkdir(parents=True)
        conflict.write_text("target-owned", encoding="utf-8")
        with self.assertRaises(install_reference.InstallError):
            install_reference.install(self.target, ["default"], apply=True, force=False)
        self.assertEqual(conflict.read_text(encoding="utf-8"), "target-owned")
        install_reference.install(self.target, ["default"], apply=True, force=True)
        self.assertNotEqual(conflict.read_text(encoding="utf-8"), "target-owned")

    def test_claude_host_uses_generated_layout(self) -> None:
        install_reference.install(
            self.target, ["default"], apply=True, force=False, host="claude-code"
        )
        self.assertTrue((self.target / ".claude/skills/chat-first-development/SKILL.md").is_file())
        self.assertFalse((self.target / ".claude/skills/chat-first-development/agents/openai.yaml").exists())


if __name__ == "__main__":
    unittest.main()
