from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / ".agents/skills/generate-implementation-design/scripts/qualityflow.py"
SPEC = importlib.util.spec_from_file_location("qualityflow", PATH)
assert SPEC and SPEC.loader
qualityflow = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(qualityflow)


class QualityflowTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / "src/items"
        self.sql = self.root / "sql"
        self.tests = self.root / "tests"
        self.e2e = self.root / "e2e"
        for path in [self.source, self.sql, self.tests, self.e2e]:
            path.mkdir(parents=True)
        (self.source / "router.py").write_text(
            "from fastapi import APIRouter\nfrom . import functions\n\n"
            "router = APIRouter()\n\n"
            "@router.post('/items', operation_id='createItem', openapi_extra={"
            "'x-api-number': 'API-001', 'x-permission': 'items:create', "
            "'x-business-summary': 'Create an item'})\n"
            "async def create_item():\n"
            "    \"\"\"Create one item.\"\"\"\n"
            "    if functions.invalid():\n"
            "        functions.error_response(code='invalid', status_code=400, message_id='items.invalid')\n"
            "    return functions.create_item('create.sql')\n",
            encoding="utf-8",
        )
        (self.source / "functions.py").write_text(
            "def invalid(): return False\n"
            "def error_response(**values): return values\n"
            "def create_item(path): return path\n",
            encoding="utf-8",
        )
        (self.source / "samples.py").write_text(
            "API_SAMPLES = {\n"
            "    'createItem:success': {'id': '1'},\n"
            "    'createItem:ERR-CREATE-ITEM-INVALID': {'code': 'invalid'},\n"
            "}\n",
            encoding="utf-8",
        )
        self.openapi = self.root / "openapi.json"
        self.openapi.write_text(
            json.dumps(
                {
                    "openapi": "3.1.0",
                    "paths": {
                        "/items": {
                            "post": {
                                "operationId": "createItem",
                                "responses": {"200": {"description": "OK"}},
                            }
                        }
                    },
                }
            ),
            encoding="utf-8",
        )
        (self.sql / "create.sql").write_text("-- create an item\nINSERT INTO items (id) VALUES ('1');\n", encoding="utf-8")
        (self.tests / "test_items.py").write_text(
            "from src.items.samples import API_SAMPLES\n\n"
            "def test_success_sample():\n"
            "    \"\"\"正常responseがsampleと一致する。\"\"\"\n"
            "    # 1. 初期化\n"
            "    response = {'id': '1'}\n"
            "    # 2. テストの実行\n"
            "    actual = response\n"
            "    # 3. アサーション\n"
            "    assert actual == API_SAMPLES['createItem:success']\n\n"
            "def test_error_sample():\n"
            "    \"\"\"異常responseがsampleと一致する。\"\"\"\n"
            "    # 1. 初期化\n"
            "    response = {'code': 'invalid'}\n"
            "    # 2. テストの実行\n"
            "    actual = response\n"
            "    # 3. アサーション\n"
            "    assert actual == API_SAMPLES['createItem:ERR-CREATE-ITEM-INVALID']\n",
            encoding="utf-8",
        )
        (self.e2e / "test_items.py").write_text(
            "@operation('createItem')\n"
            "def test_create_item():\n"
            "    \"\"\"item作成後のDB状態を確認する。\"\"\"\n"
            "    # Given: no item\n"
            "    before = None\n"
            "    # When: create API\n"
            "    response = before\n"
            "    # Then: item exists\n"
            "    assert_db_state(response)\n\n"
            "@covers('ERR-CREATE-ITEM-INVALID')\n"
            "def test_create_item_invalid():\n"
            "    \"\"\"入力不正時に状態が変わらない。\"\"\"\n"
            "    # Given: invalid input\n"
            "    before = None\n"
            "    # When: create API\n"
            "    response = before\n"
            "    # Then: state is unchanged\n"
            "    assert_state_unchanged(response)\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_api_sample_and_crud_contracts_pass_and_detect_failures(self) -> None:
        self.assertEqual(qualityflow.api_consistency(self.root / "src", self.openapi), [])
        self.assertEqual(qualityflow.sample_consistency(self.root / "src", self.tests), [])
        self.assertEqual(qualityflow.crud_e2e_consistency(self.root / "src", self.sql, self.e2e), [])
        self.assertEqual(
            qualityflow.main(
                [
                    "crud-e2e",
                    "--source-root",
                    str(self.root / "src"),
                    "--sql-root",
                    str(self.sql),
                    "--e2e-root",
                    str(self.e2e),
                ]
            ),
            0,
        )
        (self.source / "samples.py").write_text("API_SAMPLES = {'createItem:success': {'id': '1'}}\n", encoding="utf-8")
        self.assertIn("error sample missing", "\n".join(qualityflow.api_consistency(self.root / "src", self.openapi)))
        (self.e2e / "test_items.py").write_text("", encoding="utf-8")
        self.assertIn("write API lacks", "\n".join(qualityflow.crud_e2e_consistency(self.root / "src", self.sql, self.e2e)))

    def test_coverage_is_advisory_until_explicitly_enforced(self) -> None:
        coverage = self.root / "coverage.json"
        coverage.write_text(
            json.dumps({"totals": {"num_statements": 100, "covered_lines": 94, "num_branches": 20, "covered_branches": 17}}),
            encoding="utf-8",
        )
        result = qualityflow.coverage_result(coverage, qualityflow.DEFAULT_THRESHOLDS)
        self.assertEqual(result["status"], "advisory")
        self.assertEqual(qualityflow.main(["coverage", "--input", str(coverage)]), 0)
        self.assertEqual(qualityflow.main(["coverage", "--input", str(coverage), "--enforce"]), 1)

    def test_test_structure_threshold_and_suppression_contracts(self) -> None:
        self.assertEqual(qualityflow.test_structure(self.tests, "unit"), [])
        self.assertEqual(qualityflow.test_structure(self.e2e, "e2e"), [])
        self.assertEqual(qualityflow.threshold_consistency(qualityflow.DEFAULT_THRESHOLDS), [])
        config = self.root / "thresholds.json"
        value = json.loads(qualityflow.DEFAULT_THRESHOLDS.read_text(encoding="utf-8"))
        value["coverage"]["statement_percent"] = 80
        config.write_text(json.dumps(value), encoding="utf-8")
        self.assertIn("coverage", "\n".join(qualityflow.threshold_consistency(config)))

        standard = self.root / "standard.md"
        standard.write_text("| `RULE-ONE` | MUST | x | X |\n", encoding="utf-8")
        source = self.root / "suppressed.py"
        source.write_text("value = 1  # ignore[RULE-ONE] generated compatibility\n", encoding="utf-8")
        inventory, failures = qualityflow.suppression_inventory(self.root, standard)
        self.assertEqual(len(inventory), 1)
        self.assertEqual(failures, [])
        source.write_text("value = 1  # ignore[RULE-UNKNOWN]\n", encoding="utf-8")
        _, failures = qualityflow.suppression_inventory(self.root, standard)
        self.assertTrue(any("reason missing" in failure for failure in failures))
        self.assertTrue(any("orphan Rule ID" in failure for failure in failures))

    def test_external_report_aggregates_quality_checks_without_repository_results(self) -> None:
        coverage = self.root / "coverage.json"
        coverage.write_text(
            json.dumps({"totals": {"num_statements": 100, "covered_lines": 100, "num_branches": 20, "covered_branches": 20}}),
            encoding="utf-8",
        )
        report = self.root / "external" / "report.json"
        self.assertEqual(
            qualityflow.main(
                [
                    "report",
                    "--root",
                    str(self.root),
                    "--coverage",
                    str(coverage),
                    "--standard",
                    str(ROOT / "docs/standards/AS-BUILT-DESIGN.md"),
                    "--json-out",
                    str(report),
                ]
            ),
            0,
        )
        checks = {item["check_id"] for item in json.loads(report.read_text(encoding="utf-8"))["checks"]}
        self.assertEqual(checks, {"FAST-019", "FAST-020", "FAST-021", "AUD-008"})


if __name__ == "__main__":
    unittest.main()
