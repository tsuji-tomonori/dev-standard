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
            "schema_version": 1,
            "standard": {"checklist": "checklist.xlsx", "catalog": "governance/checklist/catalog.json"},
            "profiles": {"CORE": {"description": "test", "sheets": ["01_要件定義"]}},
            "phase_order": ["intake", "requirements", "closed"],
            "phases": {
                "intake": {"title": "intake", "required_docs": ["docs/00-request.md"], "required_approvals": ["requester"]},
                "requirements": {"title": "requirements", "required_docs": ["docs/01-requirements.md"], "required_approvals": []},
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

    def test_approval_is_bound_to_current_document_digest(self) -> None:
        work = self.init_item()
        state = devflow.read_json(work / "state.json")
        results = devflow.read_json(work / "review" / "checklist-results.json")
        before = devflow.gate_snapshot(work, state, results, "intake", include_approvals=True)
        self.assertIn("APPROVAL_MISSING", {item["code"] for item in before["blockers"]})

        approve = argparse.Namespace(
            work_item="WI-test",
            phase="intake",
            decision="approved",
            approver="user@example.com",
            role="requester",
            comment="要求原文と目的を確認",
        )
        self.assertEqual(devflow.cmd_approve(approve), 0)
        approved = devflow.gate_snapshot(work, state, results, "intake", include_approvals=True)
        self.assertTrue(approved["passed"])

        with (work / "docs" / "00-request.md").open("a", encoding="utf-8") as stream:
            stream.write("\nmaterial change\n")
        changed = devflow.gate_snapshot(work, state, results, "intake", include_approvals=True)
        self.assertFalse(changed["passed"])
        self.assertNotEqual(before["gate_digest"], changed["gate_digest"])
        self.assertIn("APPROVAL_MISSING", {item["code"] for item in changed["blockers"]})

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
        item.update({"applicability": "not-applicable", "na_rationale": ""})
        blocked = devflow.gate_snapshot(work, state, results, "requirements", include_approvals=False)
        self.assertIn("CHECK_NA_RATIONALE", {failure["code"] for failure in blocked["blockers"]})
        item["na_rationale"] = "外部APIを持たないため非該当"
        passed = devflow.gate_snapshot(work, state, results, "requirements", include_approvals=False)
        self.assertTrue(passed["passed"])

    def test_tampered_approval_chain_is_rejected(self) -> None:
        path = self.root / "approvals.jsonl"
        devflow.append_chained(path, {"event": "one"})
        record = json.loads(path.read_text(encoding="utf-8"))
        record["event"] = "tampered"
        path.write_text(json.dumps(record) + "\n", encoding="utf-8")
        with self.assertRaises(devflow.GovernanceError):
            devflow.verify_chain(path)

    def test_approved_improvement_updates_target_skill_once(self) -> None:
        skill = self.root / ".agents" / "skills" / "inspect-quality-gates"
        (skill / "references").mkdir(parents=True)
        (skill / "SKILL.md").write_text("---\nname: inspect-quality-gates\ndescription: test\n---\n", encoding="utf-8")
        proposal = devflow.propose_improvement(
            "inspect-quality-gates",
            "証跡不足が再発",
            "作業開始時に証跡パスを作成する",
            ["WI-1:verification:REQ-1"],
            "session-1",
        )
        proposals = devflow.load_improvements()
        proposals[0].update({"status": "approved", "approved_by": "owner", "approved_at": "2026-01-01T00:00:00Z"})
        devflow.save_improvements(proposals)
        self.assertEqual(devflow.apply_approved_improvements(), [proposal["id"]])
        self.assertEqual(devflow.apply_approved_improvements(), [])
        learned = (skill / "references" / "learned-rules.md").read_text(encoding="utf-8")
        self.assertEqual(learned.count(proposal["id"]), 1)


if __name__ == "__main__":
    unittest.main()
