from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "tools" / "generate_host_assets.py"
SPEC = importlib.util.spec_from_file_location("generate_host_assets", PATH)
assert SPEC and SPEC.loader
host_assets = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(host_assets)


class GenerateHostAssetsTest(unittest.TestCase):
    def test_claude_package_is_generated_from_canonical_assets(self) -> None:
        config = host_assets.adapters()
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            host_assets.populate("claude-code", output, config)
            self.assertTrue((output / ".claude/skills/chat-first-development/SKILL.md").is_file())
            self.assertFalse((output / ".claude/skills/chat-first-development/agents/openai.yaml").exists())
            reviewer = (output / ".claude/agents/gate-auditor.md").read_text(encoding="utf-8")
            self.assertIn("tools: Read, Grep, Glob", reviewer)
            self.assertNotIn("gpt-", reviewer.lower())
            self.assertTrue((output / "CLAUDE.snippet.md").is_file())
            snippet = (output / "CLAUDE.snippet.md").read_text(encoding="utf-8")
            self.assertIn("3本だけ", snippet)
            self.assertIn("CI/CD workflow", snippet)
            self.assertNotIn("required checkを必須", snippet)
            self.assertTrue((output / "manifest.json").is_file())

    def test_all_host_outputs_are_byte_deterministic(self) -> None:
        config = host_assets.adapters()
        for host in sorted(config["hosts"]):
            with tempfile.TemporaryDirectory() as first_dir, tempfile.TemporaryDirectory() as second_dir:
                first = Path(first_dir)
                second = Path(second_dir)
                host_assets.populate(host, first, config)
                host_assets.populate(host, second, config)
                self.assertEqual(host_assets.file_snapshot(first), host_assets.file_snapshot(second))

    def test_generated_host_paths_are_not_tracked(self) -> None:
        host_assets.validate_no_tracked_generated(host_assets.adapters())

    def test_multi_file_host_package_uses_an_archive_artifact(self) -> None:
        workflow = (ROOT / ".github/workflows/host-assets.yml").read_text(encoding="utf-8")
        self.assertIn("path: .devflow/generated/hosts", workflow)
        self.assertNotIn("archive: false", workflow)


if __name__ == "__main__":
    unittest.main()
