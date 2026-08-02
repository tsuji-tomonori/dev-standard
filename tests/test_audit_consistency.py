from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "tools/audit_consistency.py"
SPEC = importlib.util.spec_from_file_location("audit_consistency", PATH)
assert SPEC and SPEC.loader
audit_consistency = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit_consistency)


class AuditConsistencyTest(unittest.TestCase):
    def test_current_skills_docs_traces_and_generators_pass(self) -> None:
        result = audit_consistency.run_audit()
        self.assertEqual(result["overall"], "合格", result["findings"])
        self.assertEqual(result["blocking_findings"], 0)
        self.assertEqual(result["metrics"]["skill_count"], 18)
        self.assertEqual(result["metrics"]["requirement_count"], 52)
        self.assertEqual(result["metrics"]["auto_generation_requirement_count"], 29)
        self.assertEqual(result["metrics"]["missing_trace_count"], 0)
        self.assertLessEqual(result["metrics"]["skill_description_characters"], 5000)


if __name__ == "__main__":
    unittest.main()
