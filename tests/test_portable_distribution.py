from __future__ import annotations

import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools import install_reference


class PortableDistributionMatrixTest(unittest.TestCase):
    def test_portable_and_source_runners_share_mapping_and_render_modules(self) -> None:
        source_runner = (
            install_reference.ROOT / "tools/quintflow.py"
        ).read_text(encoding="utf-8")
        portable_runner = (
            install_reference.ROOT / "tools/portable_quintflow.py"
        ).read_text(encoding="utf-8")
        for module in ["spec_mapping", "render_requirements", "render_skills"]:
            self.assertIn(module, source_runner)
            self.assertIn(f'_load_pinned_tool("{module}")', portable_runner)
        self.assertNotIn("_CATALOG_FIELDS", portable_runner)
        self.assertNotIn("def _render_requirements", portable_runner)
        self.assertEqual(
            install_reference._runner_local_modules(
                install_reference.ROOT / "tools/portable_quintflow.py"
            ),
            ["render_requirements", "render_skills", "safe_io", "spec_mapping"],
        )

    def test_every_profile_on_every_host_has_exact_skill_and_runtime_closure(self) -> None:
        manifest = install_reference.load_manifest()
        activation = manifest["portable_runtime"]["activation_skill"]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for profile in sorted(manifest["profiles"]):
                selected = install_reference._selected_skills(manifest, [profile])
                has_python_runtime = (
                    install_reference._dependency_runtime(manifest, selected) is not None
                )
                for host in ["codex", "claude-code"]:
                    target = root / f"{profile}-{host}"
                    target.mkdir()
                    with contextlib.redirect_stdout(io.StringIO()):
                        install_reference.install(
                            target,
                            [profile],
                            apply=True,
                            force=False,
                            host=host,
                        )
                    receipt = json.loads(
                        (target / ".dev-standard/install/receipt.json").read_text(
                            encoding="utf-8"
                        )
                    )
                    self.assertEqual(receipt["skills"], selected, (profile, host))
                    skill_root = target / (
                        ".agents/skills" if host == "codex" else ".claude/skills"
                    )
                    actual = sorted(
                        path.parent.name for path in skill_root.glob("*/SKILL.md")
                    )
                    self.assertEqual(actual, selected, (profile, host))
                    has_skills = bool(selected)
                    self.assertEqual(
                        (target / "spec/skills/skills.qnt").exists(), has_skills
                    )
                    self.assertEqual(
                        (target / "spec/skills/skills.json").exists(), has_skills
                    )
                    has_runtime = activation in selected
                    self.assertEqual((target / "tools/quintflow.py").exists(), has_runtime)
                    self.assertEqual(
                        (target / ".dev-standard/quint/source/package-lock.json").exists(),
                        has_runtime,
                    )
                    self.assertEqual(receipt["quint_version"] is not None, has_runtime)
                    self.assertEqual(
                        (target / "tools/portable_python.py").exists(),
                        has_python_runtime,
                    )
                    for protected in [
                        ".github/workflows",
                        ".github/PULL_REQUEST_TEMPLATE",
                        ".github/rulesets",
                    ]:
                        self.assertFalse((target / protected).exists(), (profile, host))
                    for name in selected:
                        interface = skill_root / name / "agents/openai.yaml"
                        self.assertEqual(interface.exists(), host == "codex")
                    environment = dict(os.environ)
                    environment.pop("PYTHONPATH", None)
                    for script in sorted(skill_root.glob("*/scripts/*.py")):
                        result = subprocess.run(
                            [sys.executable, "-I", str(script), "--help"],
                            cwd=target,
                            env=environment,
                            text=True,
                            capture_output=True,
                            check=False,
                        )
                        self.assertEqual(
                            result.returncode,
                            0,
                            (profile, host, script.relative_to(target), result.stdout, result.stderr),
                        )


if __name__ == "__main__":
    unittest.main()
