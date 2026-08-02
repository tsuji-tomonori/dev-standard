from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from benchmarks.harness.designfacts import cloudformation_facts, derive_cloudformation_facts, derive_fastapi_sql_facts, sql_facts
from benchmarks.harness.io import BenchmarkError

ROOT = Path(__file__).resolve().parents[2]


class DesignFactsTest(unittest.TestCase):
    def test_fastapi_openapi_sql_ast_digest_determinism_and_drift(self) -> None:
        source = ROOT / "benchmarks/fixtures/B06/gold"
        first = derive_fastapi_sql_facts(source)
        second = derive_fastapi_sql_facts(source)
        self.assertEqual(first, second)
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / "fixture"
            shutil.copytree(source, candidate)
            (candidate / "sql/read.sql").write_text("SELECT items.id FROM items JOIN owners ON owners.id = items.id;\n", encoding="utf-8")
            self.assertNotEqual(first["source_digest"], derive_fastapi_sql_facts(candidate)["source_digest"])

    def test_cloudformation_structured_facts_digest_determinism_and_drift(self) -> None:
        source = ROOT / "benchmarks/fixtures/B07/gold"
        first = derive_cloudformation_facts(source)
        self.assertEqual(first, derive_cloudformation_facts(source))
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / "fixture"
            shutil.copytree(source, candidate)
            template = candidate / "cdk.out/stack.template.yaml"
            template.write_text(template.read_text(encoding="utf-8") + "  Table:\n    Type: AWS::DynamoDB::Table\n", encoding="utf-8")
            self.assertNotEqual(first["source_digest"], derive_cloudformation_facts(candidate)["source_digest"])

    def test_sql_ast_handles_join_dml_multi_statement_and_rejects_malformed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "all.sql").write_text(
                "SELECT a.id FROM alpha a JOIN beta b ON b.id = a.id;"
                "INSERT INTO gamma (id) VALUES (1);"
                "UPDATE delta SET id = 2;"
                "DELETE FROM epsilon WHERE id = 1;\n",
                encoding="utf-8",
            )
            facts = sql_facts(root)
            self.assertEqual([item["operation"] for item in facts], ["SELECT", "INSERT", "UPDATE", "DELETE"])
            self.assertEqual(facts[0]["tables"], ["alpha", "beta"])
            (root / "bad.sql").write_text("SELECT * FROM (alpha;\n", encoding="utf-8")
            with self.assertRaises(BenchmarkError):
                sql_facts(root)

    def test_cloudformation_intrinsic_tags_are_parsed_without_execution(self) -> None:
        template = ROOT / "benchmarks/fixtures/B07/gold/cdk.out/stack.template.yaml"
        facts = cloudformation_facts(template)
        self.assertIn("AWS::S3::Bucket", {item.get("type") for item in facts})
        self.assertIn("Stage", {item.get("name") for item in facts})
