from __future__ import annotations

import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools import install_reference, portable_quintflow


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
        self.assertFalse((self.target / ".dev-standard").exists())
        install_reference.install(self.target, ["default"], apply=True, force=True)
        self.assertNotEqual(conflict.read_text(encoding="utf-8"), "target-owned")

    def test_claude_host_uses_generated_layout(self) -> None:
        install_reference.install(
            self.target, ["default"], apply=True, force=False, host="claude-code"
        )
        self.assertTrue((self.target / ".claude/skills/chat-first-development/SKILL.md").is_file())
        self.assertFalse((self.target / ".claude/skills/chat-first-development/agents/openai.yaml").exists())

    def test_runtime_closure_is_host_independent_and_only_follows_requirements_skill(self) -> None:
        formal_contracts = {
            "spec/skills/skills.qnt",
            "spec/skills/skills.json",
        }
        required = {
            "tools/quintflow.py",
            "tools/safe_io.py",
            "tools/spec_mapping.py",
            "tools/render_requirements.py",
            "tools/render_skills.py",
            ".dev-standard/quint/source/package.json",
            ".dev-standard/quint/source/package-lock.json",
            "spec/skills/skills.qnt",
            "spec/skills/skills.json",
        }
        manifest = install_reference.load_manifest()
        for profile in ["default", "full", "requirements", "frontend"]:
            selected = install_reference._selected_skills(manifest, [profile])
            expected = (
                required
                if manifest["portable_runtime"]["activation_skill"] in selected
                else formal_contracts
            )
            by_host: dict[str, dict[str, str]] = {}
            for host in ["codex", "claude-code"]:
                items = install_reference.plan(
                    self.target,
                    [profile],
                    manifest,
                    host=host,
                )
                runtime = {
                    item.destination.relative_to(self.target).as_posix(): hashlib.sha256(
                        item.source.read_bytes()
                    ).hexdigest()
                    for item in items
                    if item.destination.relative_to(self.target).as_posix() in required
                }
                self.assertEqual(set(runtime), expected, (profile, host))
                by_host[host] = runtime
            self.assertEqual(by_host["codex"], by_host["claude-code"], profile)
        for host in ["codex", "claude-code"]:
            items = install_reference.plan(self.target, ["regulated"], manifest, host=host)
            destinations = {
                item.destination.relative_to(self.target).as_posix() for item in items
            }
            self.assertTrue({"spec/skills/skills.qnt", "spec/skills/skills.json"}.issubset(destinations))
            self.assertNotIn("tools/quintflow.py", destinations)

    def test_dependency_closure_is_derived_from_formal_skill_contracts(self) -> None:
        manifest = copy.deepcopy(install_reference.load_manifest())
        manifest["profiles"]["dependency-probe"] = [
            {
                "source": ".agents/skills/chat-first-development",
                "destination": ".agents/skills/chat-first-development",
            }
        ]
        items = install_reference.plan(
            self.target,
            ["dependency-probe"],
            manifest,
        )
        installed = {
            item.destination.parts[item.destination.parts.index("skills") + 1]
            for item in items
            if "skills" in item.destination.parts and item.destination.name == "SKILL.md"
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

    def test_skill_python_dependencies_use_an_isolated_runtime_only_when_needed(self) -> None:
        manifest = install_reference.load_manifest()
        for profile, expected_python, expected_quint in [
            ("implementation-design", True, False),
            ("aws-cdk-implementation-design", True, False),
            ("default", True, True),
            ("regulated", False, False),
            ("right-size-execution", False, False),
        ]:
            destinations = {
                item.destination.relative_to(self.target).as_posix()
                for item in install_reference.plan(
                    self.target, [profile], manifest
                )
            }
            self.assertEqual(
                "tools/portable_python.py" in destinations,
                expected_python,
                profile,
            )
            self.assertEqual(
                "tools/quintflow.py" in destinations,
                expected_quint,
                profile,
            )
            if profile in {"regulated", "right-size-execution"}:
                self.assertIn("tools/safe_io.py", destinations, profile)

    def test_reinstall_is_idempotent_including_receipt_and_runtime(self) -> None:
        install_reference.install(self.target, ["default"], apply=True, force=False)
        first = {
            path.relative_to(self.target).as_posix(): path.read_bytes()
            for path in self.target.rglob("*")
            if path.is_file()
        }
        install_reference.install(self.target, ["default"], apply=True, force=False)
        second = {
            path.relative_to(self.target).as_posix(): path.read_bytes()
            for path in self.target.rglob("*")
            if path.is_file()
        }
        self.assertEqual(first, second)

    def test_portable_quint_receipt_requires_the_host_interface_pair(self) -> None:
        install_reference.install(self.target, ["default"], apply=True, force=False)
        receipt_path = self.target / ".dev-standard/install/receipt.json"
        commitment_path = self.target / ".dev-standard/install/commitment.json"
        original_receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        original_commitment = json.loads(commitment_path.read_text(encoding="utf-8"))

        for host, policy in [
            ("codex", "canonical-omitted"),
            (["codex"], "required"),
        ]:
            with self.subTest(host=host, policy=policy):
                receipt = copy.deepcopy(original_receipt)
                receipt["host"] = host
                receipt["interface_policy"] = policy
                receipt_bytes = (
                    json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True)
                    + "\n"
                ).encode()
                receipt_path.write_bytes(receipt_bytes)
                commitment = copy.deepcopy(original_commitment)
                commitment["receipt_sha256"] = hashlib.sha256(receipt_bytes).hexdigest()
                commitment_path.write_text(
                    json.dumps(
                        commitment,
                        ensure_ascii=False,
                        indent=2,
                        sort_keys=True,
                    )
                    + "\n",
                    encoding="utf-8",
                )
                with mock.patch.multiple(
                    portable_quintflow,
                    ROOT=self.target,
                    COMMITMENT=commitment_path,
                    RECEIPT=receipt_path,
                ):
                    with self.assertRaisesRegex(
                        portable_quintflow.PortableQuintError,
                        "receipt identity",
                    ):
                        portable_quintflow._receipt()

        receipt_path.write_text(
            json.dumps(
                original_receipt,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        commitment_path.write_text(
            json.dumps(
                original_commitment,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )

    def test_symlinked_runtime_destination_fails_without_external_write(self) -> None:
        external = Path(self.temp.name) / "external"
        external.mkdir()
        sentinel = external / "sentinel.txt"
        sentinel.write_bytes(b"outside")
        runtime_source = self.target / ".dev-standard/quint/source"
        runtime_source.parent.mkdir(parents=True)
        runtime_source.symlink_to(external, target_is_directory=True)

        with self.assertRaises(
            (install_reference.InstallError, install_reference.safe_io.UnsafePathError)
        ):
            install_reference.install(self.target, ["default"], apply=True, force=True)

        self.assertEqual(sentinel.read_bytes(), b"outside")
        self.assertEqual(sorted(path.name for path in external.iterdir()), ["sentinel.txt"])

    def test_root_alias_and_home_identity_are_refused(self) -> None:
        with self.assertRaises(install_reference.InstallError):
            install_reference.install(Path("/tmp/.."), ["default"], apply=False, force=False)
        with self.assertRaises(install_reference.InstallError):
            install_reference.install(Path.home(), ["default"], apply=False, force=False)

    def test_profile_shrink_and_tampered_metadata_are_refused(self) -> None:
        install_reference.install(
            self.target, ["default", "regulated"], apply=True, force=False
        )
        with self.assertRaises(install_reference.InstallError):
            install_reference.install(
                self.target, ["default"], apply=True, force=True
            )
        commitment = self.target / ".dev-standard/install/commitment.json"
        commitment.write_text("{}\n", encoding="utf-8")
        with self.assertRaises(install_reference.InstallError):
            install_reference.install(
                self.target, ["default", "regulated"], apply=False, force=True
            )

    def test_claude_dry_run_does_not_create_source_tree_host_package(self) -> None:
        generated = install_reference.ROOT / ".devflow/generated/hosts/claude-code"
        before = {
            path.relative_to(generated).as_posix(): path.read_bytes()
            for path in generated.rglob("*")
            if path.is_file()
        } if generated.exists() else None
        install_reference.install(
            self.target,
            ["default"],
            apply=False,
            force=False,
            host="claude-code",
        )
        after = {
            path.relative_to(generated).as_posix(): path.read_bytes()
            for path in generated.rglob("*")
            if path.is_file()
        } if generated.exists() else None
        self.assertEqual(after, before)

    def test_policy_paths_and_their_parent_are_denied_without_stripping_dot_prefix(self) -> None:
        manifest = install_reference.load_manifest()
        for destination in [
            ".github/workflows/check.yml",
            "./.github/workflows/check.yml",
            ".github",
            ".",
        ]:
            self.assertTrue(
                install_reference._protected(destination, manifest), destination
            )

        mutated = copy.deepcopy(manifest)
        mutated["profiles"]["default"][0]["destination"] = ".github/workflows/check.yml"
        with self.assertRaises(install_reference.InstallError):
            install_reference.plan(self.target, ["default"], mutated)

    def test_formal_contract_mapping_cannot_collide_with_a_skill_destination(self) -> None:
        manifest = copy.deepcopy(install_reference.load_manifest())
        manifest["formal_skill_contracts"]["mappings"][0]["destination"] = (
            ".agents/skills/chat-first-development/SKILL.md"
        )
        with self.assertRaises(install_reference.InstallError):
            install_reference.plan(self.target, ["default"], manifest)

    def test_cas_race_is_a_clean_cli_error_and_leaves_target_unmodified(self) -> None:
        with mock.patch.object(
            install_reference.safe_io,
            "atomic_batch_write_cas",
            side_effect=install_reference.safe_io.ConcurrentModificationError("race"),
        ):
            result = install_reference.main(
                ["--target", str(self.target), "--profile", "default", "--apply"]
            )
        self.assertEqual(result, 2)
        self.assertFalse((self.target / ".agents").exists())


if __name__ == "__main__":
    unittest.main()
