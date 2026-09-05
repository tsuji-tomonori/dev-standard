from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".agents/skills/govern-development-request/scripts/regulatedflow.py"
START = ROOT / ".agents/skills/govern-development-request/scripts/start.py"


class RegulatedFlowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / "tools").mkdir()
        shutil.copy2(ROOT / "tools/safe_io.py", self.root / "tools/safe_io.py")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def run_flow(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--root", str(self.root), *arguments],
            text=True,
            capture_output=True,
            check=False,
        )

    def init(self, work_id: str = "RG-1", *extra: str) -> subprocess.CompletedProcess[str]:
        return self.run_flow(
            "init",
            "--id",
            work_id,
            "--duty-kind",
            "contract",
            "--duty-reference",
            "MSA:RETENTION-7Y",
            "--obligation",
            "retain signed release evidence for seven years",
            "--authority",
            "named release owner approval",
            "--retention",
            "retain for seven years",
            *extra,
        )

    def authorize(self, work_id: str = "RG-1", *extra: str) -> subprocess.CompletedProcess[str]:
        evidence = self.write_authority_evidence(work_id)
        return self.run_flow(
            "authorize",
            "--id",
            work_id,
            "--authority-evidence",
            evidence.relative_to(self.root).as_posix(),
            *extra,
        )

    def write_authority_evidence(
        self,
        work_id: str = "RG-1",
        **overrides: object,
    ) -> Path:
        value: dict[str, object] = {
            "schema_version": 1,
            "evidence_kind": "target-owned-authorization",
            "work_id": work_id,
            "authority_boundary": "named release owner approval",
            "authority_identity": "release-owner:alice@example.invalid",
            "approval_reference": "target-owned-approval:APR-42",
            "authorized_scope": "src/auth and focused tests",
            "result_boundary": "repair named authorization rejection",
            "effects": ["repository source and focused tests"],
            "rollback": "revert the bounded source change",
            "stop_conditions": ["new external or irreversible effect appears"],
            "expires_at": "2099-08-30T00:00:00Z",
            "nonce": "APR-42-once",
        }
        value.update(overrides)
        path = self.root / "target-authority" / f"{work_id}.json"
        path.parent.mkdir(exist_ok=True)
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def assert_evidence_race_rolls_back(
        self,
        arguments: list[str],
        *,
        expected_status: str,
        expected_events: int,
    ) -> None:
        evidence_path = self.root / "target-authority/RG-1.json"
        spec = importlib.util.spec_from_file_location(f"regulatedflow_cas_{arguments[0]}", SCRIPT)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        flow = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(flow)
        args = flow.build_parser().parse_args(["--root", str(self.root), *arguments])
        safe_io = flow._safe_io(self.root)
        real_exchange = safe_io._exchange_existing
        injected = False

        def exchange_then_change(parent_fd: int, temporary: str, destination: str) -> None:
            nonlocal injected
            real_exchange(parent_fd, temporary, destination)
            if not injected:
                injected = True
                value = json.loads(evidence_path.read_text())
                value["authorized_scope"] = "production tenant"
                evidence_path.write_text(json.dumps(value), encoding="utf-8")

        handler = getattr(flow, f"command_{arguments[0]}")
        with safe_io.trusted_root(self.root) as root_fd:
            with mock.patch.object(safe_io, "_exchange_existing", side_effect=exchange_then_change):
                with self.assertRaises(safe_io.ConcurrentModificationError):
                    handler(args, self.root, safe_io, root_fd)
        events = (self.root / "work/RG-1/regulated/events.jsonl").read_text().splitlines()
        state = json.loads((self.root / "work/RG-1/regulated/state.json").read_text())
        self.assertTrue(injected)
        self.assertEqual(len(events), expected_events)
        self.assertEqual(state["status"], expected_status)

    def verify(self, work_id: str = "RG-1", *extra: str) -> subprocess.CompletedProcess[str]:
        return self.run_flow(
            "verify",
            "--id",
            work_id,
            "--result",
            "pass",
            "--summary",
            "selected regulated checks passed",
            "--evidence-ref",
            "local:test-regulated",
            "--observed-scope",
            "src/auth and focused tests",
            "--observed-result",
            "repair named authorization rejection",
            "--observed-effect",
            "repository source and focused tests",
            *extra,
        )

    def test_lifecycle_closes_with_internal_authorization_binding(self) -> None:
        self.assertEqual(self.init("RG-1", "--external-anchor-required").returncode, 0)
        authorized = self.authorize()
        self.assertEqual(authorized.returncode, 0, authorized.stderr)
        authorization_digest = json.loads(authorized.stdout)["authorization_digest"]
        events = [json.loads(line) for line in (self.root / "work/RG-1/regulated/events.jsonl").read_text().splitlines()]
        evidence = json.loads((self.root / "target-authority/RG-1.json").read_text())
        canonical = (json.dumps(evidence, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()
        self.assertEqual(events[1]["payload"]["authority_evidence_digest"], hashlib.sha256(canonical).hexdigest())
        self.assertEqual(events[1]["payload"]["authority_evidence_path"], "target-authority/RG-1.json")
        verified = self.verify()
        self.assertEqual(verified.returncode, 0, verified.stderr)
        closed = self.run_flow("close", "--id", "RG-1")
        self.assertEqual(closed.returncode, 0, closed.stderr)
        payload = json.loads(closed.stdout)
        self.assertEqual(payload["local_anchor"]["authorization_digest"], authorization_digest)
        self.assertEqual(payload["external_anchor_handoff"]["digest"], payload["local_anchor"]["anchor_digest"])
        checked = self.run_flow("check", "--id", "RG-1")
        self.assertEqual(checked.returncode, 0, checked.stderr)
        self.assertEqual(json.loads(checked.stdout)["events"], 4)

    def test_verify_and_close_refuse_skipped_transitions(self) -> None:
        self.assertEqual(self.init().returncode, 0)
        self.assertEqual(self.verify().returncode, 2)
        result = self.run_flow("close", "--id", "RG-1")
        self.assertEqual(result.returncode, 2)
        self.assertIn("cannot close from status active", result.stderr)

    def test_expired_authority_evidence_is_rejected(self) -> None:
        self.assertEqual(self.init().returncode, 0)
        evidence = self.write_authority_evidence(expires_at="2026-08-28T00:00:00Z")
        result = self.run_flow(
            "authorize",
            "--id",
            "RG-1",
            "--authority-evidence",
            evidence.relative_to(self.root).as_posix(),
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("already expired", result.stderr)

    def test_authorize_requires_preexisting_target_owned_evidence_not_cli_claims(self) -> None:
        self.assertEqual(self.init().returncode, 0)
        missing = self.run_flow(
            "authorize",
            "--id",
            "RG-1",
            "--authority-evidence",
            "target-authority/missing.json",
        )
        self.assertEqual(missing.returncode, 2)
        self.assertIn("does not exist", missing.stderr)
        scalar_claim = self.run_flow(
            "authorize",
            "--id",
            "RG-1",
            "--authority-identity",
            "self",
            "--authority-evidence-digest",
            "a" * 64,
        )
        self.assertEqual(scalar_claim.returncode, 2)
        checked = self.run_flow("check", "--id", "RG-1")
        self.assertEqual(json.loads(checked.stdout)["status"], "active")

    def test_authority_evidence_binding_scope_and_location_are_strict(self) -> None:
        self.assertEqual(self.init().returncode, 0)
        mismatched = self.write_authority_evidence(work_id="OTHER")
        result = self.run_flow(
            "authorize",
            "--id",
            "RG-1",
            "--authority-evidence",
            mismatched.relative_to(self.root).as_posix(),
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("another work item", result.stderr)
        runner_owned = self.root / ".devflow/run/authority.json"
        runner_owned.parent.mkdir(parents=True, exist_ok=True)
        runner_owned.write_text(json.dumps({}), encoding="utf-8")
        result = self.run_flow(
            "authorize",
            "--id",
            "RG-1",
            "--authority-evidence",
            ".devflow/run/authority.json",
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("runner-owned", result.stderr)

    def test_pass_verification_requires_target_owned_evidence(self) -> None:
        self.assertEqual(self.init().returncode, 0)
        self.assertEqual(self.authorize().returncode, 0)
        command = [
            "verify",
            "--id",
            "RG-1",
            "--result",
            "pass",
            "--summary",
            "claimed pass",
            "--observed-scope",
            "src/auth and focused tests",
            "--observed-result",
            "repair named authorization rejection",
            "--observed-effect",
            "repository source and focused tests",
        ]
        result = self.run_flow(*command)
        self.assertEqual(result.returncode, 2)
        self.assertIn("evidence references", result.stderr)

    def test_risk_signal_without_concrete_duty_is_rejected(self) -> None:
        result = self.run_flow(
            "init",
            "--id",
            "RG-1",
            "--duty-kind",
            "safety",
            "--duty-reference",
            "SEC:1",
            "--obligation",
            "authorization",
            "--authority",
            "owner",
            "--retention",
            "one year",
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("risk signal alone", result.stderr)

    def test_scope_and_effect_outside_authorization_are_rejected(self) -> None:
        self.assertEqual(self.init().returncode, 0)
        self.assertEqual(self.authorize().returncode, 0)
        scope = self.verify("RG-1", "--observed-scope", "production tenant")
        self.assertEqual(scope.returncode, 2)
        self.assertIn("outside authorization", scope.stderr)
        effect = self.verify("RG-1", "--observed-effect", "production deploy")
        self.assertEqual(effect.returncode, 2)
        self.assertIn("outside authorization", effect.stderr)

    def test_authorization_evidence_and_event_tampering_are_rejected(self) -> None:
        self.assertEqual(self.init().returncode, 0)
        self.assertEqual(self.authorize().returncode, 0)
        events = self.root / "work/RG-1/regulated/events.jsonl"
        events.write_text(events.read_text().replace("repository source", "production deploy"), encoding="utf-8")
        result = self.run_flow("check", "--id", "RG-1")
        self.assertEqual(result.returncode, 2)
        self.assertIn("digest mismatch", result.stderr)

    def test_authority_evidence_substitution_is_rejected(self) -> None:
        self.assertEqual(self.init().returncode, 0)
        self.assertEqual(self.authorize().returncode, 0)
        evidence = self.root / "target-authority/RG-1.json"
        value = json.loads(evidence.read_text())
        value["authorized_scope"] = "production tenant"
        evidence.write_text(json.dumps(value), encoding="utf-8")
        result = self.run_flow("check", "--id", "RG-1")
        self.assertEqual(result.returncode, 2)
        self.assertIn("differs from the bound authorization", result.stderr)

    def test_authority_evidence_change_during_publication_rolls_back_transition(self) -> None:
        self.assertEqual(self.init().returncode, 0)
        self.write_authority_evidence()
        self.assert_evidence_race_rolls_back(
            [
                "authorize",
                "--id",
                "RG-1",
                "--authority-evidence",
                "target-authority/RG-1.json",
            ],
            expected_status="active",
            expected_events=1,
        )

    def test_verify_and_close_bind_evidence_as_publication_precondition(self) -> None:
        self.assertEqual(self.init().returncode, 0)
        self.assertEqual(self.authorize().returncode, 0)
        self.assert_evidence_race_rolls_back(
            [
                "verify",
                "--id",
                "RG-1",
                "--result",
                "pass",
                "--summary",
                "selected checks passed",
                "--evidence-ref",
                "local:test-regulated",
                "--observed-scope",
                "src/auth and focused tests",
                "--observed-result",
                "repair named authorization rejection",
                "--observed-effect",
                "repository source and focused tests",
            ],
            expected_status="authorized",
            expected_events=2,
        )

        value = json.loads((self.root / "target-authority/RG-1.json").read_text())
        value["authorized_scope"] = "src/auth and focused tests"
        (self.root / "target-authority/RG-1.json").write_text(json.dumps(value), encoding="utf-8")
        self.assertEqual(self.verify().returncode, 0)
        self.assert_evidence_race_rolls_back(
            ["close", "--id", "RG-1"],
            expected_status="verified",
            expected_events=3,
        )
        self.assertFalse((self.root / "work/RG-1/regulated/anchor.json").exists())

    def test_symlinked_authority_evidence_is_rejected(self) -> None:
        self.assertEqual(self.init().returncode, 0)
        outside = self.root / "outside-evidence.json"
        outside.write_text(json.dumps({}), encoding="utf-8")
        authority = self.root / "target-authority"
        authority.mkdir()
        (authority / "RG-1.json").symlink_to(outside)
        result = self.run_flow(
            "authorize",
            "--id",
            "RG-1",
            "--authority-evidence",
            "target-authority/RG-1.json",
        )
        self.assertEqual(result.returncode, 2)

    def test_state_tampering_is_rejected_by_replay(self) -> None:
        self.assertEqual(self.init().returncode, 0)
        self.assertEqual(self.authorize().returncode, 0)
        state = self.root / "work/RG-1/regulated/state.json"
        state.write_text(state.read_text().replace('"authorized"', '"verified"'), encoding="utf-8")
        result = self.run_flow("check", "--id", "RG-1")
        self.assertEqual(result.returncode, 2)
        self.assertIn("differs from strict event replay", result.stderr)

    def test_symlinked_work_directory_is_rejected(self) -> None:
        outside = self.root / "outside"
        outside.mkdir()
        (self.root / "work").mkdir()
        (self.root / "work/RG-1").symlink_to(outside, target_is_directory=True)
        result = self.init()
        self.assertEqual(result.returncode, 2)
        self.assertFalse((outside / "regulated/state.json").exists())

    def test_concurrent_initialization_has_one_winner(self) -> None:
        command = [
            sys.executable,
            str(SCRIPT),
            "--root",
            str(self.root),
            "init",
            "--id",
            "RG-1",
            "--duty-kind",
            "contract",
            "--duty-reference",
            "MSA:1",
            "--obligation",
            "retain approval evidence",
            "--authority",
            "bounded approval",
            "--retention",
            "one year",
        ]
        first = subprocess.Popen(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        second = subprocess.Popen(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        first.communicate(timeout=10)
        second.communicate(timeout=10)
        self.assertEqual(sorted([first.returncode, second.returncode]), [0, 2])

    def test_start_refuses_symlinked_regulatedflow_sibling(self) -> None:
        scripts = self.root / ".agents/skills/govern-development-request/scripts"
        scripts.mkdir(parents=True)
        shutil.copy2(START, scripts / "start.py")
        outside = self.root / "outside.py"
        outside.write_text("raise RuntimeError('must not load')\n", encoding="utf-8")
        (scripts / "regulatedflow.py").symlink_to(outside)
        result = subprocess.run(
            [sys.executable, str(scripts / "start.py"), "--id", "RG-1"],
            cwd=self.root,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("must not load", result.stderr)

    def test_start_uses_host_native_sibling_in_codex_and_claude_packages(self) -> None:
        for host_root in [".agents/skills", ".claude/skills"]:
            with self.subTest(host_root=host_root), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                scripts = root / host_root / "govern-development-request/scripts"
                scripts.mkdir(parents=True)
                (root / "tools").mkdir()
                shutil.copy2(ROOT / "tools/safe_io.py", root / "tools/safe_io.py")
                shutil.copy2(START, scripts / "start.py")
                shutil.copy2(SCRIPT, scripts / "regulatedflow.py")
                result = subprocess.run(
                    [sys.executable, "-I", str(scripts / "start.py"), "--help"],
                    cwd=root,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, (host_root, result.stdout, result.stderr))
                self.assertIn("--duty-kind", result.stdout)


if __name__ == "__main__":
    unittest.main()
