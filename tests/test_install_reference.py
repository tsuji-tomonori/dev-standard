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
            self.target, ["communication"], apply=False, force=False
        )
        self.assertGreater(copied, 0)
        self.assertEqual((unchanged, conflicts), (0, 0))
        self.assertFalse((self.target / ".agents").exists())

    def test_apply_copies_standard_skill_layout(self) -> None:
        install_reference.install(self.target, ["communication"], apply=True, force=False)
        installed = self.target / ".agents" / "skills" / "calibrated-collaborative-listening" / "SKILL.md"
        source = install_reference.ROOT / ".agents" / "skills" / "calibrated-collaborative-listening" / "SKILL.md"
        self.assertEqual(installed.read_bytes(), source.read_bytes())

    def test_conflict_fails_before_other_writes_and_force_is_explicit(self) -> None:
        conflict = self.target / ".agents" / "skills" / "calibrated-collaborative-listening" / "SKILL.md"
        conflict.parent.mkdir(parents=True)
        conflict.write_text("target-owned", encoding="utf-8")
        with self.assertRaises(install_reference.InstallError):
            install_reference.install(self.target, ["communication"], apply=True, force=False)
        self.assertEqual(conflict.read_text(encoding="utf-8"), "target-owned")
        install_reference.install(self.target, ["communication"], apply=True, force=True)
        self.assertNotEqual(conflict.read_text(encoding="utf-8"), "target-owned")

    def test_agents_profile_uses_codex_standard_directory(self) -> None:
        install_reference.install(self.target, ["agents"], apply=True, force=False)
        installed = sorted(path.name for path in (self.target / ".codex" / "agents").glob("*.toml"))
        expected = sorted(path.name for path in (install_reference.ROOT / ".codex" / "agents").glob("*.toml"))
        self.assertEqual(installed, expected)

    def test_full_profile_preserves_target_configuration_and_installs_merge_references(self) -> None:
        agents_file = self.target / "AGENTS.md"
        config_file = self.target / ".codex" / "config.toml"
        agents_file.write_text("target agents\n", encoding="utf-8")
        config_file.parent.mkdir(parents=True)
        config_file.write_text("target config\n", encoding="utf-8")

        install_reference.install(self.target, ["full"], apply=True, force=False)

        self.assertEqual(agents_file.read_text(encoding="utf-8"), "target agents\n")
        self.assertEqual(config_file.read_text(encoding="utf-8"), "target config\n")
        self.assertTrue((self.target / "AGENTS.governance.reference.md").is_file())
        self.assertTrue((self.target / ".codex" / "config.reference.toml").is_file())
        self.assertTrue((self.target / "checklist.xlsx").is_file())
        self.assertTrue((self.target / "requirements.txt").is_file())


if __name__ == "__main__":
    unittest.main()
