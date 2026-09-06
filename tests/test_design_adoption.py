from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / (
    ".agents/skills/generate-implementation-design/scripts/check_design.py"
)
spec = importlib.util.spec_from_file_location("check_design", SCRIPT)
assert spec and spec.loader
design = importlib.util.module_from_spec(spec)
spec.loader.exec_module(design)


class DesignAdoptionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "src").mkdir()
        (self.root / "src/model.txt").write_text("current structure")
        (self.root / "design.md").write_text("current structure")
        (self.root / "drift.py").write_text(
            "from pathlib import Path\n"
            "import sys\n"
            "sys.exit(Path('src/model.txt').read_bytes() != Path('design.md').read_bytes())\n"
        )
        self.surface = {
            "status": "required", "sources": ["src"], "markdown": ["design.md"],
            "generate": [sys.executable, "generate.py"],
            "check": [sys.executable, "drift.py"],
        }
        self.contract = {"schema_version": 1, "surfaces": {
            key: {"status": "not-applicable", "reason": "fixture has no such surface"}
            for key in design.SURFACES
        }}
        self.contract["surfaces"]["frontend"] = self.surface

    def check(self) -> None:
        (self.root / "contract.json").write_text(json.dumps(self.contract))
        design.check(self.root, "contract.json")

    def test_connected_current_design_passes_without_writing(self) -> None:
        before = (self.root / "design.md").read_bytes()
        self.check()
        self.assertEqual((self.root / "design.md").read_bytes(), before)

    def test_missing_contract_fails_cli(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.root)], capture_output=True
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn(b"as-built incomplete", result.stderr)

    def test_unclassified_surface_is_not_silently_skipped(self) -> None:
        del self.contract["surfaces"]["data"]
        with self.assertRaisesRegex(ValueError, "classify"):
            self.check()

    def test_unsupported_is_incomplete(self) -> None:
        self.surface["status"] = "blocked"
        with self.assertRaisesRegex(ValueError, "incomplete"):
            self.check()

    def test_missing_and_empty_markdown_fail(self) -> None:
        for content in [None, "  \n"]:
            with self.subTest(content=content):
                path = self.root / "design.md"
                if content is None:
                    path.unlink()
                else:
                    path.write_text(content)
                with self.assertRaisesRegex(ValueError, "Markdown design"):
                    self.check()

    def test_implementation_change_fails_without_repairing_design(self) -> None:
        (self.root / "src/model.txt").write_text("changed structure")
        with self.assertRaisesRegex(ValueError, "drift command failed"):
            self.check()
        self.assertEqual((self.root / "design.md").read_text(), "current structure")

    def test_json_only_is_not_human_design(self) -> None:
        (self.root / "design.json").write_text("{}")
        self.surface["markdown"] = ["design.json"]
        with self.assertRaisesRegex(ValueError, "Markdown design"):
            self.check()

    def test_check_that_regenerates_is_rejected(self) -> None:
        (self.root / "drift.py").write_text(
            "from pathlib import Path\nPath('design.md').write_text('rewritten')\n"
        )
        with self.assertRaisesRegex(ValueError, "rewrote"):
            self.check()

    def test_not_applicable_requires_reason(self) -> None:
        self.contract["surfaces"]["data"]["reason"] = ""
        with self.assertRaisesRegex(ValueError, "reason"):
            self.check()

    def test_output_escape_and_symlink_are_rejected(self) -> None:
        (self.root / "alias.md").symlink_to(self.root / "design.md")
        for output in ["../design.md", "/design.md", "alias.md"]:
            with self.subTest(output=output):
                self.surface["markdown"] = [output]
                with self.assertRaises(ValueError):
                    self.check()

    def test_missing_generator_command_is_incomplete(self) -> None:
        del self.surface["generate"]
        with self.assertRaisesRegex(ValueError, "generate"):
            self.check()


if __name__ == "__main__":
    unittest.main()
