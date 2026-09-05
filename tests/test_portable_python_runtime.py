from __future__ import annotations

import contextlib
import io
import os
import shutil
import tempfile
import unittest
from collections.abc import Callable
from pathlib import Path
from unittest import mock

from tools import install_reference, portable_python


class PortablePythonRuntimeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.target = Path(self.temporary.name) / "target"
        self.target.mkdir()
        with contextlib.redirect_stdout(io.StringIO()):
            install_reference.install(
                self.target,
                ["implementation-design"],
                apply=True,
                force=False,
            )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _target_constants(self) -> mock._patch:
        return mock.patch.multiple(
            portable_python,
            ROOT=self.target,
            COMMITMENT=self.target / ".dev-standard/install/commitment.json",
            RECEIPT=self.target / ".dev-standard/install/receipt.json",
            RUNTIME_PARENT=self.target / ".dev-standard/python/runtime",
        )

    @staticmethod
    def _write_file(directory_fd: int, name: str, content: bytes) -> None:
        descriptor = os.open(
            name,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL,
            0o600,
            dir_fd=directory_fd,
        )
        try:
            os.write(descriptor, content)
        finally:
            os.close(descriptor)

    def _fake_pip_install(
        self, candidate_fd: int, _root_fd: int, requirements: dict[str, str]
    ) -> None:
        os.mkdir("site-packages", mode=0o700, dir_fd=candidate_fd)
        site_fd = os.open(
            "site-packages",
            os.O_RDONLY | getattr(os, "O_DIRECTORY", 0),
            dir_fd=candidate_fd,
        )
        try:
            modules = {
                "pyyaml": ("yaml", b"__version__ = '6.0.2'\n"),
                "sqlglot": ("sqlglot", b"__version__ = '27.28.1'\nexp = object()\n"),
            }
            for name, version in requirements.items():
                module, source = modules[name]
                os.mkdir(module, mode=0o700, dir_fd=site_fd)
                module_fd = os.open(
                    module,
                    os.O_RDONLY | getattr(os, "O_DIRECTORY", 0),
                    dir_fd=site_fd,
                )
                try:
                    self._write_file(module_fd, "__init__.py", source)
                finally:
                    os.close(module_fd)
                metadata_name = f"{name.replace('-', '_')}-{version}.dist-info"
                os.mkdir(metadata_name, mode=0o700, dir_fd=site_fd)
                metadata_fd = os.open(
                    metadata_name,
                    os.O_RDONLY | getattr(os, "O_DIRECTORY", 0),
                    dir_fd=site_fd,
                )
                try:
                    self._write_file(
                        metadata_fd,
                        "METADATA",
                        f"Metadata-Version: 2.1\nName: {name}\nVersion: {version}\n".encode(),
                    )
                finally:
                    os.close(metadata_fd)
        finally:
            os.close(site_fd)

    def _run_after_snapshots(
        self,
        script: str,
        arguments: list[str],
        mutation: Callable[[], None],
    ) -> int:
        """Mutate the installed tree after snapshots but before child execution."""

        with self._target_constants(), mock.patch.object(
            portable_python, "_pip_install", side_effect=self._fake_pip_install
        ):
            self.assertTrue(portable_python.setup())
            real_run = portable_python.subprocess.run
            started = False

            def mutate_then_run(command: list[str], **kwargs: object) -> object:
                nonlocal started
                self.assertFalse(started)
                started = True
                mutation()
                return real_run(command, **kwargs)

            with mock.patch.object(
                portable_python.subprocess,
                "run",
                side_effect=mutate_then_run,
            ):
                result = portable_python.run(script, arguments)
            self.assertTrue(started)
            return result

    def test_setup_and_run_are_isolated_and_receipt_bound(self) -> None:
        target_venv = self.target / ".venv"
        target_venv.mkdir()
        sentinel = target_venv / "target-owned.txt"
        sentinel.write_bytes(b"unchanged")
        script = ".agents/skills/generate-implementation-design/scripts/designflow.py"

        with self._target_constants(), mock.patch.object(
            portable_python, "_pip_install", side_effect=self._fake_pip_install
        ):
            self.assertTrue(portable_python.setup())
            self.assertFalse(portable_python.setup())
            self.assertEqual(portable_python.run(script, ["--help"]), 0)
            self.assertFalse(portable_python.setup())

        self.assertEqual(sentinel.read_bytes(), b"unchanged")
        self.assertEqual(
            [path for path in (self.target / ".dev-standard/python/runtime").iterdir() if path.is_dir()],
            [
                path
                for path in (self.target / ".dev-standard/python/runtime").iterdir()
                if len(path.name) == 64
            ],
        )

    def test_unrecorded_adjacent_module_cannot_shadow_pinned_dependency(self) -> None:
        script = ".agents/skills/generate-implementation-design/scripts/designflow.py"
        shadow = self.target / Path(script).parent / "yaml.py"
        marker = self.target / "unmanaged-shadow-was-imported"

        with self._target_constants(), mock.patch.object(
            portable_python, "_pip_install", side_effect=self._fake_pip_install
        ):
            self.assertTrue(portable_python.setup())
            shadow.write_text(
                "from pathlib import Path\n"
                "Path('unmanaged-shadow-was-imported').write_text('executed')\n",
                encoding="utf-8",
            )
            self.assertEqual(portable_python.run(script, ["--help"]), 0)

        self.assertFalse(marker.exists())

    def test_recorded_sibling_swap_before_child_start_cannot_execute(self) -> None:
        script = ".agents/skills/generate-implementation-design/scripts/qualityflow.py"
        sibling = self.target / Path(script).with_name("designflow.py")
        marker = self.target / "malicious-recorded-sibling-executed"

        def replace_sibling() -> None:
            sibling.write_text(
                "from pathlib import Path\n"
                "Path('malicious-recorded-sibling-executed').write_text('executed')\n",
                encoding="utf-8",
            )

        result = self._run_after_snapshots(
            script,
            ["api", "--source-root", "missing", "--openapi", "missing.json"],
            replace_sibling,
        )

        self.assertEqual(result, 2)
        self.assertFalse(marker.exists())

    def test_recorded_safe_io_swap_before_child_start_cannot_execute(self) -> None:
        script = ".agents/skills/generate-implementation-design/scripts/designflow.py"
        runtime = self.target / "tools/safe_io.py"
        marker = self.target / "malicious-safe-io-executed"

        def replace_runtime() -> None:
            runtime.write_text(
                "from pathlib import Path\n"
                "Path('malicious-safe-io-executed').write_text('executed')\n",
                encoding="utf-8",
            )

        result = self._run_after_snapshots(
            script,
            [
                "cdk",
                "--template",
                "missing.json",
                "--requirements",
                "missing-requirements.json",
                "--trace",
                "missing-trace.json",
                "--test-root",
                "missing-tests",
                "--out",
                "docs/design/generated/cdk/stack",
                "--repo-root",
                ".",
            ],
            replace_runtime,
        )

        self.assertEqual(result, 2)
        self.assertFalse(marker.exists())

    def test_default_thresholds_are_snapshot_bound_at_child_start(self) -> None:
        script = ".agents/skills/generate-implementation-design/scripts/qualityflow.py"
        thresholds = (
            self.target
            / ".agents/skills/generate-implementation-design/assets/as-built-thresholds.json"
        )

        result = self._run_after_snapshots(
            script,
            ["thresholds"],
            lambda: thresholds.write_text("{}\n", encoding="utf-8"),
        )

        self.assertEqual(result, 0)

    def test_default_standard_is_snapshot_bound_at_child_start(self) -> None:
        script = ".agents/skills/generate-implementation-design/scripts/qualityflow.py"
        standard = self.target / "docs/standards/AS-BUILT-DESIGN.md"
        (self.target / ".git").mkdir()
        source_root = self.target / "checks"
        source_root.mkdir()
        (source_root / "suppressed.py").write_text(
            "value = 1  # ignore[GEN-DO-001] documented compatibility\n",
            encoding="utf-8",
        )

        result = self._run_after_snapshots(
            script,
            ["suppressions", "--root", str(source_root)],
            lambda: standard.write_text("# replaced standard\n", encoding="utf-8"),
        )

        self.assertEqual(result, 0)

    def test_repository_name_replacement_is_refused_before_output(self) -> None:
        script = ".agents/skills/generate-implementation-design/scripts/designflow.py"
        fixture = Path(__file__).parent / "fixtures/portable_cdk"
        smoke = self.target / "smoke"
        shutil.copytree(fixture, smoke)
        displaced = Path(self.temporary.name) / "target.displaced"

        def replace_repository_name() -> None:
            self.target.rename(displaced)
            shutil.copytree(displaced, self.target)

        result = self._run_after_snapshots(
            script,
            [
                "cdk",
                "--template",
                str(self.target / "smoke/stack.yaml"),
                "--requirements",
                str(self.target / "smoke/requirements.json"),
                "--trace",
                str(self.target / "smoke/trace.json"),
                "--test-root",
                str(self.target / "smoke/tests"),
                "--out",
                "docs/design/generated/cdk/stack",
                "--repo-root",
                str(self.target),
            ],
            replace_repository_name,
        )

        self.assertEqual(result, 2)
        self.assertTrue(self.target.is_dir())
        self.assertTrue(displaced.is_dir())
        output = Path("docs/design/generated/cdk/stack")
        self.assertFalse((self.target / output).exists())
        self.assertFalse((displaced / output).exists())

    def test_requirements_are_rechecked_against_receipt_after_metadata_validation(self) -> None:
        requirements = (
            self.target
            / ".agents/skills/generate-implementation-design/requirements.txt"
        )
        with self._target_constants(), portable_python.safe_io.trusted_root(
            self.target
        ) as root_fd:
            receipt, records = portable_python._receipt(root_fd)
            requirements.write_text("PyYAML==6.0.1\n", encoding="utf-8")
            with self.assertRaisesRegex(
                portable_python.PortablePythonError,
                "changed after receipt validation",
            ):
                portable_python._requirements(receipt, records, root_fd)

    def test_unmanaged_or_wrong_host_script_is_refused(self) -> None:
        with self._target_constants(), portable_python.safe_io.trusted_root(
            self.target
        ) as root_fd:
            receipt, records = portable_python._receipt(root_fd)
            for value in [
                "../outside.py",
                "tools/portable_python.py",
                ".claude/skills/generate-implementation-design/scripts/designflow.py",
            ]:
                with self.assertRaises(portable_python.PortablePythonError):
                    portable_python._script_relative(value, receipt, records)


if __name__ == "__main__":
    unittest.main()
