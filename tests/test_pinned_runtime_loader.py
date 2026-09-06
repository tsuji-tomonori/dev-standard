from __future__ import annotations

import importlib.util
import json
import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "tools" / "portable_quintflow.py"
SPEC = importlib.util.spec_from_file_location("portable_quintflow_test", PATH)
assert SPEC and SPEC.loader
portable = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(portable)


class PinnedRuntimeLoaderTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "target"
        self.root.mkdir()
        self.source = self.root / ".dev-standard/quint/source"
        self.source.mkdir(parents=True)
        (self.source / "package.json").write_bytes((ROOT / "package.json").read_bytes())
        (self.source / "package-lock.json").write_bytes((ROOT / "package-lock.json").read_bytes())
        self.parent = self.root / ".dev-standard/quint/runtime"
        self.runtime = self.parent / portable.QUINT_VERSION
        self.constants = mock.patch.multiple(
            portable,
            ROOT=self.root,
            RUNTIME_SOURCE=self.source,
            RUNTIME_PARENT=self.parent,
            RUNTIME=self.runtime,
            REQUIREMENTS_QNT=self.root / "spec/requirements/requirements.qnt",
            REQUIREMENTS_JSON=self.root / "spec/requirements/requirements.json",
            REQUIREMENTS_DOC=self.root / "docs/requirements/REQUIREMENTS.md",
            SKILLS_QNT=self.root / "spec/skills/skills.qnt",
            SKILLS_JSON=self.root / "spec/skills/skills.json",
            COMMITMENT=self.root / ".dev-standard/install/commitment.json",
            RECEIPT=self.root / ".dev-standard/install/receipt.json",
        )
        self.constants.start()
        self.receipt = mock.patch.object(
            portable,
            "_receipt",
            return_value={
                "host": "codex",
                "interface_policy": "required",
                "skills": [],
                "quint_version": portable.QUINT_VERSION,
                "assets": [],
            },
        )
        self.receipt.start()

    def tearDown(self) -> None:
        self.receipt.stop()
        self.constants.stop()
        self.temp.cleanup()

    def fake_npm(self, command: list[str], **kwargs: object) -> subprocess.CompletedProcess[str]:
        self.assertEqual(command[1:], ["ci", "--ignore-scripts", "--no-audit", "--no-fund"])
        cwd = str(kwargs["cwd"])
        stage = Path(os.readlink(cwd)) if cwd.startswith("/proc/self/fd/") else Path(cwd)
        self.assertNotEqual(stage, self.runtime)
        self.assertIn(".stage-", stage.name)
        package = stage / "node_modules/@informalsystems/quint"
        cli = package / "dist/src/cli.js"
        cli.parent.mkdir(parents=True)
        cli.write_text("#!/usr/bin/env node\n", encoding="utf-8")
        cli.chmod(0o755)
        (package / "package.json").write_text(
            json.dumps({"name": "@informalsystems/quint", "version": portable.QUINT_VERSION}),
            encoding="utf-8",
        )
        binaries = stage / "node_modules/.bin"
        binaries.mkdir()
        (binaries / "quint").symlink_to("../@informalsystems/quint/dist/src/cli.js")
        nested = stage / "node_modules/dependency/node_modules/.bin"
        nested.mkdir(parents=True)
        (nested / "tool").symlink_to("../../tool.js")
        return subprocess.CompletedProcess(command, 0, "", "")

    def test_setup_stages_then_publishes_and_safe_install_is_idempotent(self) -> None:
        with mock.patch.object(portable.subprocess, "run", side_effect=self.fake_npm) as npm:
            self.assertTrue(portable.setup())
        self.assertEqual(npm.call_count, 1)
        self.assertTrue(portable.validate_runtime().is_file())
        self.assertFalse((self.runtime / "node_modules/.bin").exists())
        self.assertFalse((self.runtime / "node_modules/dependency/node_modules/.bin").exists())

        with mock.patch.object(portable.subprocess, "run") as npm_again:
            self.assertFalse(portable.setup())
        npm_again.assert_not_called()

    def test_existing_runtime_node_modules_symlink_fails_without_touching_external(self) -> None:
        external = Path(self.temp.name) / "external"
        external.mkdir()
        sentinel = external / "sentinel.txt"
        sentinel.write_bytes(b"outside")
        self.runtime.mkdir(parents=True)
        (self.runtime / "node_modules").symlink_to(external, target_is_directory=True)

        with mock.patch.object(portable.subprocess, "run") as npm:
            with self.assertRaises((portable.PortableQuintError, portable.safe_io.SafeIOError)):
                portable.setup()
        npm.assert_not_called()
        self.assertEqual(sentinel.read_bytes(), b"outside")

    def test_repository_node_modules_symlink_is_never_used_or_modified(self) -> None:
        external = Path(self.temp.name) / "external-node-modules"
        external.mkdir()
        sentinel = external / "sentinel.txt"
        sentinel.write_bytes(b"outside")
        (self.root / "node_modules").symlink_to(external, target_is_directory=True)

        with mock.patch.object(portable.subprocess, "run", side_effect=self.fake_npm):
            self.assertTrue(portable.setup())
        self.assertEqual(sentinel.read_bytes(), b"outside")
        self.assertEqual(sorted(path.name for path in external.iterdir()), ["sentinel.txt"])

    def test_ambient_or_explicit_quint_override_is_not_supported(self) -> None:
        source = PATH.read_text(encoding="utf-8")
        self.assertNotIn("DEV_STANDARD_QUINT_BIN", source)
        self.assertNotIn("node_modules/.bin/quint", source)

    def test_skill_cli_invariants_are_zero_argument_boolean_values(self) -> None:
        source = (ROOT / "spec/skills/skills.qnt").read_text(encoding="utf-8")
        self.assertEqual(
            portable.SKILL_INVARIANTS,
            [
                "formalContractsHold",
                "workflowOrderIsConsistent",
                "portablePolicyIsUntouched",
            ],
        )
        for invariant in portable.SKILL_INVARIANTS:
            self.assertRegex(source, rf"(?m)^  val {invariant} = all \{{$")
        formal_contract = source[
            source.index("  val formalContractsHold =") :
            source.index("  val workflowOrderIsConsistent =")
        ]
        self.assertIn("runnerConformanceIsExplicit(contracts)", formal_contract)
        self.assertIn(
            '"runnerConformanceIsExplicit"',
            PATH.read_text(encoding="utf-8"),
        )

    def test_external_node_override_must_be_absolute_and_is_resolved_to_a_real_file(self) -> None:
        with mock.patch.dict(os.environ, {"DEV_STANDARD_NODE_BIN": "relative-node"}, clear=True):
            with self.assertRaises(portable.PortableQuintError):
                portable._command_path("node", "DEV_STANDARD_NODE_BIN")

        executable = self.root / "node-real"
        executable.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        executable.chmod(executable.stat().st_mode | stat.S_IXUSR)
        link = self.root / "node-link"
        link.symlink_to(executable)
        with mock.patch.dict(os.environ, {"DEV_STANDARD_NODE_BIN": str(link)}, clear=True):
            self.assertEqual(
                portable._command_path("node", "DEV_STANDARD_NODE_BIN"), executable
            )

    @unittest.skipUnless(__import__("sys").platform.startswith("linux"), "fd path test")
    def test_quint_spec_input_is_pinned_before_path_replacement(self) -> None:
        spec = self.root / "spec/model.qnt"
        spec.parent.mkdir(parents=True)
        spec.write_bytes(b"module safe {}\n")
        cli = self.root / "runtime/cli.js"
        cli.parent.mkdir(parents=True)
        cli.write_bytes(b"// cli\n")
        node = self.root / "node"
        node.write_text("#!/bin/sh\n", encoding="utf-8")
        node.chmod(node.stat().st_mode | stat.S_IXUSR)
        observed = b""

        def replace_then_read(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
            nonlocal observed
            pinned_spec = Path(command[3])
            spec.write_bytes(b"module malicious {}\n")
            observed = pinned_spec.read_bytes()
            return subprocess.CompletedProcess(command, 0, "", "")

        with (
            mock.patch.object(portable, "validate_runtime", return_value=cli),
            mock.patch.object(portable, "_command_path", return_value=node),
            mock.patch.object(portable.subprocess, "run", side_effect=replace_then_read),
        ):
            portable.run_quint(
                "typecheck",
                str(spec.relative_to(self.root)),
                pinned_inputs=(spec,),
            )
        self.assertEqual(observed, b"module safe {}\n")

    def test_generate_refuses_to_publish_when_a_read_input_changes(self) -> None:
        requirements = self.root / "spec/requirements/requirements.qnt"
        requirements.parent.mkdir(parents=True)
        requirements.write_bytes(b"module requirements {}\n")
        catalog = {
            "schemaVersion": 1,
            "catalogRevision": 0,
            "product": "portable",
            "updatedAt": "2026-08-29",
            "requirements": [],
        }

        def mutate_then_derive(*_: object, **__: object) -> dict[Path, bytes]:
            requirements.write_bytes(b"module changed {}\n")
            return {
                portable.REQUIREMENTS_JSON: b"{}\n",
                portable.REQUIREMENTS_DOC: b"# generated\n",
            }

        with (
            mock.patch.object(portable, "_preflight"),
            mock.patch.object(portable, "_extract_state", return_value=catalog),
            mock.patch.object(portable, "_derived", side_effect=mutate_then_derive),
        ):
            with self.assertRaises(portable.safe_io.ConcurrentModificationError):
                portable.generate()

        self.assertFalse(portable.REQUIREMENTS_JSON.exists())
        self.assertFalse(portable.REQUIREMENTS_DOC.exists())

    def test_installed_skill_catalog_must_be_complete_even_for_empty_subset(self) -> None:
        portable.SKILLS_JSON.parent.mkdir(parents=True)
        portable.SKILLS_JSON.write_text('{"contracts": []}\n', encoding="utf-8")

        with self.assertRaisesRegex(
            portable.PortableQuintError, "exactly the expected 17 Skills"
        ):
            portable._verify_installed_skills(
                {
                    "host": "codex",
                    "interface_policy": "required",
                    "skills": [],
                }
            )


if __name__ == "__main__":
    unittest.main()
