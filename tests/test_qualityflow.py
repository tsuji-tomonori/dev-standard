from __future__ import annotations

import importlib.util
import json
import shutil
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
        (self.root / ".git").mkdir()
        (self.root / "tools").mkdir()
        shutil.copyfile(ROOT / "tools/safe_io.py", self.root / "tools/safe_io.py")
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
            "    'createItem:ERR-INVALID': {'code': 'invalid'},\n"
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
            "    response = client.post('/items')\n"
            "    # 2. テストの実行\n"
            "    actual = response.json()\n"
            "    # 3. アサーション\n"
            "    assert actual == API_SAMPLES['createItem:success']\n\n"
            "def test_error_sample():\n"
            "    \"\"\"異常responseがsampleと一致する。\"\"\"\n"
            "    # 1. 初期化\n"
            "    response = client.post('/items', json={})\n"
            "    # 2. テストの実行\n"
            "    actual = response.json()\n"
            "    # 3. アサーション\n"
            "    assert actual == API_SAMPLES['createItem:ERR-INVALID']\n",
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
            "@covers('ERR-INVALID')\n"
            "def test_create_item_invalid():\n"
            "    \"\"\"入力不正時に状態が変わらない。\"\"\"\n"
            "    # Given: invalid input\n"
            "    before = None\n"
            "    # When: create API\n"
            "    response = before\n"
            "    # Then: state is unchanged\n"
            "    assert_db_state_unchanged(response)\n",
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
        self.assertIn("DB write lacks", "\n".join(qualityflow.crud_e2e_consistency(self.root / "src", self.sql, self.e2e)))

    def test_samples_require_runtime_response_provenance(self) -> None:
        self.assertEqual(qualityflow.sample_consistency(self.root / "src", self.tests), [])
        (self.tests / "test_items.py").write_text(
            "from src.items.samples import API_SAMPLES\n\n"
            "def test_fabricated_response():\n"
            "    fabricated = {'id': '1'}\n"
            "    assert fabricated == API_SAMPLES['createItem:success']\n",
            encoding="utf-8",
        )
        failures = qualityflow.sample_consistency(self.root / "src", self.tests)
        self.assertTrue(any("runtime response" in failure for failure in failures))

        (self.tests / "test_items.py").write_text(
            "from src.items.samples import API_SAMPLES\n\n"
            "class UncollectableHelper:\n"
            "    def test_fake_sample(self):\n"
            "        actual = client.post('/items').json()\n"
            "        assert actual == API_SAMPLES['createItem:success']\n",
            encoding="utf-8",
        )
        failures = qualityflow.sample_consistency(self.root / "src", self.tests)
        self.assertTrue(any("createItem:success" in failure for failure in failures))

    def test_sample_provenance_is_branch_aware_and_reassignment_kills_trust(self) -> None:
        (self.tests / "test_items.py").write_text(
            "from src.items.samples import API_SAMPLES\n\n"
            "def test_branch(flag):\n"
            "    if flag:\n"
            "        actual = client.post('/items').json()\n"
            "    else:\n"
            "        actual = {'id': 'fabricated'}\n"
            "    assert actual == API_SAMPLES['createItem:success']\n\n"
            "def test_reassigned():\n"
            "    actual = client.post('/items').json()\n"
            "    actual = {'id': 'fabricated'}\n"
            "    assert actual == API_SAMPLES['createItem:ERR-INVALID']\n",
            encoding="utf-8",
        )
        failures = qualityflow.sample_consistency(self.root / "src", self.tests)
        self.assertTrue(any("every reaching branch" in failure for failure in failures))
        self.assertTrue(any("createItem:ERR-INVALID" in failure for failure in failures))

        (self.tests / "test_items.py").write_text(
            "from src.items.samples import API_SAMPLES\n\n"
            "def test_mixed_tuple():\n"
            "    actual, fabricated = (client.post('/items').json(), {'id': 'fabricated'})\n"
            "    assert fabricated == API_SAMPLES['createItem:success']\n\n"
            "def test_conditional(flag):\n"
            "    actual = client.post('/items').json() if flag else {'id': 'fabricated'}\n"
            "    assert actual == API_SAMPLES['createItem:ERR-INVALID']\n",
            encoding="utf-8",
        )
        failures = qualityflow.sample_consistency(self.root / "src", self.tests)
        self.assertTrue(any("createItem:success" in failure for failure in failures))
        self.assertTrue(any("createItem:ERR-INVALID" in failure for failure in failures))

        (self.tests / "test_items.py").write_text(
            "from src.items.samples import API_SAMPLES\n\n"
            "def test_unreachable_sample():\n"
            "    actual = client.post('/items').json()\n"
            "    assert actual == (API_SAMPLES['createItem:success'] "
            "if False else {'id': 'fabricated'})\n"
            "    assert (actual == API_SAMPLES['createItem:ERR-INVALID']) "
            "if False else True\n",
            encoding="utf-8",
        )
        failures = qualityflow.sample_consistency(self.root / "src", self.tests)
        self.assertTrue(any("createItem:success" in failure for failure in failures))
        self.assertTrue(any("createItem:ERR-INVALID" in failure for failure in failures))

    def test_runtime_adapter_requires_explicit_authority_and_real_client(self) -> None:
        (self.tests / "test_items.py").write_text(
            "from src.items.samples import API_SAMPLES\n\n"
            "def invoke_api():\n"
            "    return {'id': 'fabricated'}\n\n"
            "def test_untrusted():\n"
            "    actual = invoke_api()\n"
            "    assert actual == API_SAMPLES['createItem:success']\n",
            encoding="utf-8",
        )
        failures = qualityflow.sample_consistency(self.root / "src", self.tests)
        self.assertTrue(any("runtime response" in failure for failure in failures))

        (self.tests / "test_items.py").write_text(
            "from src.items.samples import API_SAMPLES\n\n"
            "@trusted_runtime_response_adapter('local-test-client')\n"
            "def invoke_api():\n"
            "    return client.post('/items').json()\n\n"
            "def test_success():\n"
            "    actual = invoke_api()\n"
            "    assert actual == API_SAMPLES['createItem:success']\n\n"
            "def test_error():\n"
            "    actual = client.post('/items', json={}).json()\n"
            "    assert actual == API_SAMPLES['createItem:ERR-INVALID']\n",
            encoding="utf-8",
        )
        self.assertEqual(qualityflow.sample_consistency(self.root / "src", self.tests), [])

        (self.tests / "test_items.py").write_text(
            "from src.items.samples import API_SAMPLES\n\n"
            "@trusted_runtime_response_adapter('local-test-client')\n"
            "def invoke_api():\n"
            "    def never_called():\n"
            "        return client.post('/items')\n"
            "    return {'id': 'fabricated'}\n\n"
            "def test_success():\n"
            "    actual = invoke_api()\n"
            "    assert actual == API_SAMPLES['createItem:success']\n\n"
            "def test_error():\n"
            "    actual = client.post('/items', json={}).json()\n"
            "    self.assertEqual(actual, API_SAMPLES['createItem:ERR-INVALID'])\n",
            encoding="utf-8",
        )
        failures = qualityflow.sample_consistency(self.root / "src", self.tests)
        self.assertTrue(any("trusted adapter return lacks" in failure for failure in failures))
        self.assertTrue(any("createItem:success" in failure for failure in failures))
        self.assertFalse(any("createItem:ERR-INVALID" in failure for failure in failures))

    def test_crud_e2e_requires_db_and_external_effect_specific_assertions(self) -> None:
        functions = self.source / "functions.py"
        functions.write_text(
            "def invalid(): return False\n"
            "def error_response(**values): return values\n"
            "def publish(): return inventory_client.publish()\n"
            "def create_item(path):\n"
            "    publish()\n"
            "    return path\n",
            encoding="utf-8",
        )
        failures = qualityflow.crud_e2e_consistency(self.root / "src", self.sql, self.e2e)
        self.assertTrue(any("external write lacks assert_external_state" in item for item in failures))
        self.assertTrue(any("external error effect lacks" in item for item in failures))

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
        coverage.write_text(
            json.dumps(
                {
                    "totals": {
                        "num_statements": 10,
                        "covered_lines": 11,
                        "num_branches": 2,
                        "covered_branches": -1,
                    }
                }
            ),
            encoding="utf-8",
        )
        with self.assertRaises(qualityflow.QualityError):
            qualityflow.coverage_result(coverage, qualityflow.DEFAULT_THRESHOLDS)

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

    def test_suppression_output_is_confined_and_qualityflow_has_no_duplicate_report(self) -> None:
        report = self.root / "suppressions.json"
        self.assertEqual(
            qualityflow.main(
                [
                    "suppressions",
                    "--root",
                    str(self.root),
                    "--standard",
                    str(ROOT / "docs/standards/AS-BUILT-DESIGN.md"),
                    "--json-out",
                    str(report),
                ]
            ),
            0,
        )
        self.assertEqual(json.loads(report.read_text(encoding="utf-8"))["schema_version"], 1)
        self.assertEqual(
            qualityflow.main(
                [
                    "suppressions",
                    "--root",
                    str(self.root),
                    "--standard",
                    str(ROOT / "docs/standards/AS-BUILT-DESIGN.md"),
                    "--json-out",
                    str(self.root.parent / "escape.json"),
                ]
            ),
            2,
        )

    def test_invalid_and_unsupported_sql_are_bounded_findings(self) -> None:
        invalid = self.root / "invalid"
        invalid.mkdir()
        (invalid / "bad.sql").write_text("SELECT 'unterminated;\n", encoding="utf-8")
        findings = qualityflow.implementation_structure(invalid)
        self.assertTrue(any("invalid SQL" in finding for finding in findings))
        (invalid / "bad.sql").write_text(
            "MERGE INTO a USING b ON a.id = b.id WHEN MATCHED THEN DELETE;\n",
            encoding="utf-8",
        )
        findings = qualityflow.implementation_structure(invalid)
        self.assertTrue(any("unsupported SQL statement" in finding for finding in findings))

    def test_quality_inputs_reject_lexical_symlinks(self) -> None:
        coverage = self.root / "coverage.json"
        coverage.write_text(
            json.dumps(
                {
                    "totals": {
                        "num_statements": 1,
                        "covered_lines": 1,
                        "num_branches": 1,
                        "covered_branches": 1,
                    }
                }
            ),
            encoding="utf-8",
        )
        linked = self.root / "linked-coverage.json"
        linked.symlink_to(coverage)
        with self.assertRaises(qualityflow.QualityError):
            qualityflow.coverage_result(linked, qualityflow.DEFAULT_THRESHOLDS)


if __name__ == "__main__":
    unittest.main()
