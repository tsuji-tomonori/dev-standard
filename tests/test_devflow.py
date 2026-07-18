from __future__ import annotations

import argparse
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools import devflow


class DevflowTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.policy_path = self.root / "governance" / "policy.json"
        self.catalog_path = self.root / "governance" / "checklist" / "catalog.json"
        self.work_root = self.root / "work"
        self.template_root = self.root / "docs" / "templates"
        self.improvements_path = self.root / "governance" / "improvements" / "proposals.json"
        self.report_root = self.root / "reports"
        self.template_root.mkdir(parents=True)
        self.policy = {
            "schema_version": 2,
            "standard": {"checklist": "checklist.xlsx", "catalog": "governance/checklist/catalog.json"},
            "profiles": {"CORE": {"description": "test", "sheets": ["01_要件定義"]}},
            "phase_order": ["intake", "requirements", "closed"],
            "authorization": {"phase": "requirements", "role": "requester", "title": "initial"},
            "phases": {
                "intake": {"title": "intake", "required_docs": ["docs/00-request.md"], "required_approvals": []},
                "requirements": {
                    "title": "requirements",
                    "required_docs": [
                        "docs/01-requirements.md",
                        "docs/01-traceability.md",
                        "docs/01-execution-plan.md",
                    ],
                    "required_approvals": ["requester"],
                },
                "closed": {"title": "closed", "required_docs": [], "required_approvals": []},
            },
            "document_placeholders": ["TBD", "{{", "}}"],
            "review_values": {
                "applicability": ["undecided", "applicable", "not-applicable"],
                "verdict": ["unreviewed", "pass", "fail"],
                "severity": ["Critical", "High", "Medium", "Low"],
            },
        }
        self.catalog = {
            "schema_version": 1,
            "generated_at": "2026-01-01T00:00:00Z",
            "source": "checklist.xlsx",
            "source_sha256": "source",
            "item_count": 1,
            "items": [
                {
                    "id": "REQ-001",
                    "sheet": "01_要件定義",
                    "phase": "requirements",
                    "base_severity": "High",
                    "profile": "CORE",
                    "always_on": True,
                    "artifact_tags": ["requirements"],
                    "risk_tags": [],
                    "scope_levels": [1, 2, 3],
                }
            ],
        }
        devflow.atomic_write_json(self.policy_path, self.policy)
        devflow.atomic_write_json(self.catalog_path, self.catalog)
        (self.template_root / "00-request.md").write_text(
            "# Request\n\nWork: {{WORK_ITEM}}\nTitle: {{TITLE}}\nCreated: {{CREATED_AT}}\nProfiles: {{PROFILES}}\n\n{{REQUEST}}\n" + "accepted\n" * 20,
            encoding="utf-8",
        )
        (self.template_root / "01-requirements.md").write_text("# Requirements\n\n" + "complete requirement\n" * 20, encoding="utf-8")
        (self.template_root / "01-traceability.md").write_text("# Traceability\n\n" + "complete trace\n" * 20, encoding="utf-8")
        (self.template_root / "01-execution-plan.md").write_text("# Plan\n\n" + "complete plan\n" * 20, encoding="utf-8")
        self.patchers = [
            patch.object(devflow, "ROOT", self.root),
            patch.object(devflow, "POLICY_PATH", self.policy_path),
            patch.object(devflow, "CATALOG_PATH", self.catalog_path),
            patch.object(devflow, "WORK_ROOT", self.work_root),
            patch.object(devflow, "TEMPLATE_ROOT", self.template_root),
            patch.object(devflow, "IMPROVEMENTS_PATH", self.improvements_path),
            patch.object(devflow, "REPORT_ROOT", self.report_root),
        ]
        for patcher in self.patchers:
            patcher.start()

    def tearDown(self) -> None:
        for patcher in reversed(self.patchers):
            patcher.stop()
        self.temp.cleanup()

    def init_item(self, work_id: str = "WI-test") -> Path:
        args = argparse.Namespace(id=work_id, title="Test", request="Build safely", profile=["CORE"], actor="tester")
        self.assertEqual(devflow.cmd_init(args), 0)
        return self.work_root / work_id

    def test_init_uses_scope_selector_and_preserves_audit_input(self) -> None:
        scopeflow = devflow.load_scopeflow()
        state = scopeflow.estimate_scope(
            "要件を更新する", expected_files=1, domains=["requirements"],
            artifact_tags=["requirements"], risk_tags=[],
        )
        scope_path = self.root / "estimate.json"
        devflow.atomic_write_json(scope_path, state)
        args = argparse.Namespace(
            id="WI-scoped", title="Scoped", request="要件を更新する",
            profile=["CORE"], actor="tester", scope_file=str(scope_path),
        )
        self.assertEqual(devflow.cmd_init(args), 0)
        work = self.work_root / "WI-scoped"
        saved = devflow.read_json(work / "execution-scope.json")
        self.assertEqual(saved["selection"]["selector_version"], "scope-selector-v1")
        self.assertEqual(saved["selection"]["selected_item_ids"], ["REQ-001"])
        self.assertTrue(devflow.read_json(work / "state.json")["execution_scope_sha256"])

    def test_invalid_scope_does_not_leave_partial_work_item(self) -> None:
        scope_path = self.root / "invalid-scope.json"
        scope_path.write_text("{}", encoding="utf-8")
        args = argparse.Namespace(
            id="WI-invalid", title="Invalid", request="要件を更新する",
            profile=["CORE"], actor="tester", scope_file=str(scope_path),
        )
        with self.assertRaises(devflow.GovernanceError):
            devflow.cmd_init(args)
        self.assertFalse((self.work_root / "WI-invalid").exists())

    def approve_requirements(self, work_id: str = "WI-test") -> None:
        work = self.work_root / work_id
        state = devflow.read_json(work / "state.json")
        state["current_phase"] = "requirements"
        devflow.atomic_write_json(work / "state.json", state)
        results = devflow.read_json(work / "review" / "checklist-results.json")
        item = results["items"][0]
        item.update({
            "applicability": "applicable",
            "verdict": "pass",
            "reviewer": "reviewer",
            "reviewed_at": "2026-01-01T00:00:00Z",
            "evidence": ["docs/01-requirements.md"],
            "severity_rationale": "テスト用の案件重要度",
        })
        devflow.atomic_write_json(work / "review" / "checklist-results.json", results)
        approve = argparse.Namespace(
            work_item=work_id,
            phase=None,
            decision="approved",
            approver="user@example.com",
            role=None,
            comment="要件と自律実行計画を確認",
        )
        self.assertEqual(devflow.cmd_approve(approve), 0)

    def test_initial_authorization_is_bound_to_requirements_and_plan_digest(self) -> None:
        work = self.init_item()
        state = devflow.read_json(work / "state.json")
        state["current_phase"] = "requirements"
        devflow.atomic_write_json(work / "state.json", state)
        results = devflow.read_json(work / "review" / "checklist-results.json")
        item = results["items"][0]
        item.update({
            "applicability": "applicable",
            "verdict": "pass",
            "reviewer": "reviewer",
            "reviewed_at": "2026-01-01T00:00:00Z",
            "evidence": ["docs/01-requirements.md"],
            "severity_rationale": "テスト用の案件重要度",
        })
        devflow.atomic_write_json(work / "review" / "checklist-results.json", results)
        before = devflow.gate_snapshot(work, state, results, "requirements", include_approvals=True)
        self.assertIn("APPROVAL_MISSING", {item["code"] for item in before["blockers"]})

        approve = argparse.Namespace(
            work_item="WI-test",
            phase=None,
            decision="approved",
            approver="user@example.com",
            role=None,
            comment="要件と自律実行計画を確認",
        )
        self.assertEqual(devflow.cmd_approve(approve), 0)
        approved = devflow.gate_snapshot(work, state, results, "requirements", include_approvals=True)
        self.assertTrue(approved["passed"])

        with (work / "docs" / "01-execution-plan.md").open("a", encoding="utf-8") as stream:
            stream.write("\nmaterial change\n")
        changed = devflow.gate_snapshot(work, state, results, "requirements", include_approvals=True)
        self.assertFalse(changed["passed"])
        self.assertNotEqual(approved["gate_digest"], changed["gate_digest"])
        self.assertIn("APPROVAL_MISSING", {item["code"] for item in changed["blockers"]})

    def test_initial_authorization_cannot_be_recorded_in_another_phase(self) -> None:
        self.init_item()
        approve = argparse.Namespace(
            work_item="WI-test",
            phase=None,
            decision="rejected",
            approver="user@example.com",
            role=None,
            comment="not ready",
        )
        with self.assertRaises(devflow.GovernanceError):
            devflow.cmd_approve(approve)

    def test_later_phase_needs_no_new_human_approval(self) -> None:
        work = self.init_item()
        self.approve_requirements()
        state = devflow.read_json(work / "state.json")
        state["current_phase"] = "requirements"
        devflow.atomic_write_json(work / "state.json", state)
        self.assertEqual(devflow.cmd_advance(argparse.Namespace(work_item="WI-test", actor="agent")), 0)
        self.assertEqual(devflow.read_json(work / "state.json")["current_phase"], "closed")

    def test_advance_rechecks_authorized_requirements(self) -> None:
        work = self.init_item()
        self.approve_requirements()
        state = devflow.read_json(work / "state.json")
        state["current_phase"] = "requirements"
        devflow.atomic_write_json(work / "state.json", state)
        self.assertEqual(devflow.cmd_advance(argparse.Namespace(work_item="WI-test", actor="agent")), 0)
        with (work / "docs" / "01-requirements.md").open("a", encoding="utf-8") as stream:
            stream.write("\nunauthorized scope change\n")
        with self.assertRaises(devflow.GovernanceError):
            devflow.cmd_advance(argparse.Namespace(work_item="WI-test", actor="agent"))

    def test_legacy_work_item_requires_explicit_migration(self) -> None:
        work = self.init_item()
        state = devflow.read_json(work / "state.json")
        state.pop("workflow_schema_version")
        devflow.atomic_write_json(work / "state.json", state)
        with self.assertRaises(devflow.GovernanceError):
            devflow.cmd_status(argparse.Namespace(work_item="WI-test", json=False))
        self.assertEqual(
            devflow.cmd_migrate(argparse.Namespace(work_item="WI-test", actor="owner")),
            0,
        )
        migrated = devflow.read_json(work / "state.json")
        self.assertEqual(migrated["workflow_schema_version"], 2)

    def test_applicable_check_requires_reachable_evidence(self) -> None:
        work = self.init_item()
        state = devflow.read_json(work / "state.json")
        state["current_phase"] = "requirements"
        devflow.atomic_write_json(work / "state.json", state)
        results = devflow.read_json(work / "review" / "checklist-results.json")
        item = results["items"][0]
        item.update({
            "applicability": "applicable",
            "verdict": "pass",
            "reviewer": "reviewer",
            "reviewed_at": "2026-01-01T00:00:00Z",
            "evidence": ["evidence/missing.txt"],
            "severity_rationale": "テスト用の案件重要度",
        })
        devflow.atomic_write_json(work / "review" / "checklist-results.json", results)
        blocked = devflow.gate_snapshot(work, state, results, "requirements", include_approvals=False)
        self.assertIn("CHECK_EVIDENCE", {failure["code"] for failure in blocked["blockers"]})

        (work / "evidence" / "proof.txt").write_text("proof", encoding="utf-8")
        item["evidence"] = ["evidence/proof.txt"]
        passed = devflow.gate_snapshot(work, state, results, "requirements", include_approvals=False)
        self.assertTrue(passed["passed"])

    def test_not_applicable_requires_rationale(self) -> None:
        work = self.init_item()
        state = devflow.read_json(work / "state.json")
        results = devflow.read_json(work / "review" / "checklist-results.json")
        item = results["items"][0]
        item.update({
            "applicability": "not-applicable",
            "na_rationale": "",
            "reviewer": "reviewer",
            "reviewed_at": "2026-01-01T00:00:00Z",
            "severity_rationale": "非該当でも基準重要度を維持",
        })
        blocked = devflow.gate_snapshot(work, state, results, "requirements", include_approvals=False)
        self.assertIn("CHECK_NA_RATIONALE", {failure["code"] for failure in blocked["blockers"]})
        item["na_rationale"] = "外部APIを持たないため非該当"
        passed = devflow.gate_snapshot(work, state, results, "requirements", include_approvals=False)
        self.assertTrue(passed["passed"])

    def test_fail_remains_blocking_without_later_risk_approval(self) -> None:
        work = self.init_item()
        state = devflow.read_json(work / "state.json")
        state["current_phase"] = "requirements"
        devflow.atomic_write_json(work / "state.json", state)
        results = devflow.read_json(work / "review" / "checklist-results.json")
        item = results["items"][0]
        item.update({
            "applicability": "applicable",
            "verdict": "fail",
            "issue_id": "ISSUE-1",
            "remediation_plan": "欠陥を修正して再試験する",
            "due_at": "2099-01-01",
            "reviewer": "reviewer",
            "reviewed_at": "2026-01-01T00:00:00Z",
            "severity_rationale": "未解決なら要求品質を損なう",
            "exception": {
                "status": "approved",
                "approver": "owner",
                "role": "governance-owner",
                "rationale": "accept",
                "expires_at": "2099-01-01T00:00:00Z",
            },
        })
        report = devflow.gate_snapshot(work, state, results, "requirements", include_approvals=False)
        self.assertIn("CHECK_FAIL_BLOCKING", {failure["code"] for failure in report["blockers"]})

    def test_batch_check_update_is_atomic_and_auditable(self) -> None:
        work = self.init_item()
        (work / "evidence" / "proof.txt").write_text("proof", encoding="utf-8")
        batch = self.root / "batch.json"
        batch.write_text(json.dumps([{
            "item": "REQ-001",
            "applicability": "applicable",
            "verdict": "pass",
            "severity": "High",
            "reviewer": "batch-reviewer",
            "evidence": ["evidence/proof.txt"],
            "severity_rationale": "要求工程の主要統制",
        }]), encoding="utf-8")
        args = argparse.Namespace(work_item="WI-test", input=str(batch), actor="batch-reviewer")
        self.assertEqual(devflow.cmd_set_checks(args), 0)
        result = devflow.read_json(work / "review" / "checklist-results.json")["items"][0]
        self.assertEqual((result["applicability"], result["verdict"]), ("applicable", "pass"))
        events = devflow.verify_chain(work / "events.jsonl")
        self.assertEqual(events[-1]["event"], "checklist-batch-updated")
        self.assertEqual(events[-1]["details"]["count"], 1)

        batch.write_text(json.dumps([{
            "item": "REQ-001",
            "applicability": "not-applicable",
            "verdict": "unreviewed",
            "severity": "High",
            "reviewer": "batch-reviewer",
            "severity_rationale": "非該当でも基準重要度を維持",
        }]), encoding="utf-8")
        with self.assertRaises(devflow.GovernanceError):
            devflow.cmd_set_checks(args)
        unchanged = devflow.read_json(work / "review" / "checklist-results.json")["items"][0]
        self.assertEqual(unchanged["applicability"], "applicable")

    def test_fail_requires_remediation_due_date_and_recheck_history(self) -> None:
        work = self.init_item()
        (work / "evidence" / "proof.txt").write_text("proof", encoding="utf-8")
        batch = self.root / "batch.json"
        common = {
            "item": "REQ-001",
            "applicability": "applicable",
            "severity": "Critical",
            "severity_rationale": "未解決なら要件追跡が成立しない",
            "reviewer": "critical-reviewer",
        }
        batch.write_text(json.dumps([{**common, "verdict": "fail", "issue": "ISSUE-1"}]), encoding="utf-8")
        args = argparse.Namespace(work_item="WI-test", input=str(batch), actor="critical-reviewer")
        with self.assertRaises(devflow.GovernanceError):
            devflow.cmd_set_checks(args)

        batch.write_text(json.dumps([{
            **common,
            "verdict": "fail",
            "issue": "ISSUE-1",
            "remediation_plan": "一意IDを付与して再検査する",
            "due_at": "2099-01-01",
        }]), encoding="utf-8")
        self.assertEqual(devflow.cmd_set_checks(args), 0)

        batch.write_text(json.dumps([{
            **common,
            "verdict": "pass",
            "evidence": ["evidence/proof.txt"],
        }]), encoding="utf-8")
        with self.assertRaises(devflow.GovernanceError):
            devflow.cmd_set_checks(args)

        batch.write_text(json.dumps([{
            **common,
            "verdict": "pass",
            "evidence": ["evidence/proof.txt"],
            "recheck": {
                "verdict": "pass",
                "evidence": ["evidence/proof.txt"],
                "reviewer": "recheck-reviewer",
                "reviewed_at": "2026-01-02T00:00:00Z",
            },
        }]), encoding="utf-8")
        self.assertEqual(devflow.cmd_set_checks(args), 0)
        result = devflow.read_json(work / "review" / "checklist-results.json")["items"][0]
        self.assertEqual(result["history"][-1]["verdict"], "fail")
        self.assertEqual(result["recheck"]["verdict"], "pass")

    def test_not_applicable_still_requires_reviewer_and_severity_rationale(self) -> None:
        work = self.init_item()
        results = devflow.read_json(work / "review" / "checklist-results.json")
        item = results["items"][0]
        item.update({"applicability": "not-applicable", "na_rationale": "外部APIなし"})
        report = devflow.gate_snapshot(
            work,
            devflow.read_json(work / "state.json"),
            results,
            "requirements",
            include_approvals=False,
        )
        codes = {failure["code"] for failure in report["blockers"]}
        self.assertIn("CHECK_REVIEWER", codes)
        self.assertIn("CHECK_SEVERITY_RATIONALE", codes)

    def test_tampered_approval_chain_is_rejected(self) -> None:
        path = self.root / "approvals.jsonl"
        devflow.append_chained(path, {"event": "one"})
        record = json.loads(path.read_text(encoding="utf-8"))
        record["event"] = "tampered"
        path.write_text(json.dumps(record) + "\n", encoding="utf-8")
        with self.assertRaises(devflow.GovernanceError):
            devflow.verify_chain(path)

    def test_improvement_proposal_remains_pending_for_a_new_work_item(self) -> None:
        proposal = devflow.propose_improvement(
            "inspect-quality-gates",
            "証跡不足が再発",
            "作業開始時に証跡パスを作成する",
            ["WI-1:verification:REQ-1"],
            "session-1",
        )
        proposals = devflow.load_improvements()
        self.assertEqual(proposals[0]["status"], "pending")
        self.assertEqual(proposals[0]["id"], proposal["id"])
        self.assertFalse(hasattr(devflow, "apply_approved_improvements"))


if __name__ == "__main__":
    unittest.main()
