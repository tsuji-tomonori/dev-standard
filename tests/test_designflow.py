from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module():
    path = ROOT / ".agents/skills/generate-implementation-design/scripts/designflow.py"
    spec = importlib.util.spec_from_file_location("designflow", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


designflow = load_module()


class DesignflowTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def fastapi_fixture(self) -> tuple[Path, Path, Path, Path]:
        source = self.root / "src"
        sql = self.root / "sql"
        output = self.root / "docs"
        (source / "items").mkdir(parents=True)
        sql.mkdir()
        (source / "items/router.py").write_text(
            "from fastapi import APIRouter\nfrom . import functions\n\n"
            "router = APIRouter()\n\n"
            "@router.get('/items/{item_id}')\n"
            "async def get_item(item_id: str):\n"
            "    item = functions.load_item(item_id)\n"
            "    return functions.present_item(item)\n",
            encoding="utf-8",
        )
        (source / "items/functions.py").write_text(
            "def load_item(item_id): return {'id': item_id}\n"
            "def present_item(item): return item\n",
            encoding="utf-8",
        )
        openapi = self.root / "openapi.json"
        openapi.write_text(json.dumps({
            "openapi": "3.1.0",
            "paths": {"/items/{item_id}": {"get": {
                "operationId": "getItem",
                "summary": "Get item",
                "x-requirement-ids": ["REQ-ITEM-001"],
                "responses": {"200": {"description": "OK", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Item"}}}}},
            }}},
            "components": {"schemas": {"Item": {"type": "object", "required": ["id"], "properties": {"id": {"type": "string"}}}}},
        }), encoding="utf-8")
        (sql / "read.sql").write_text("SELECT id FROM items;\n", encoding="utf-8")
        (sql / "create.sql").write_text("INSERT INTO items (id) VALUES ('1');\n", encoding="utf-8")
        (sql / "update.sql").write_text("UPDATE items SET id = '2' WHERE id = '1';\n", encoding="utf-8")
        (sql / "delete.sql").write_text("DELETE FROM items WHERE id = '2';\n", encoding="utf-8")
        return source, openapi, sql, output

    def test_fastapi_openapi_and_sql_docs_are_generated_and_drift_checked(self) -> None:
        source, openapi, sql, output = self.fastapi_fixture()
        args = ["fastapi", "--source-root", str(source), "--openapi", str(openapi), "--sql-root", str(sql), "--out", str(output)]
        self.assertEqual(designflow.main(args), 0)
        sequence = (output / "SEQUENCES.md").read_text(encoding="utf-8")
        self.assertIn("functions.load_item", sequence)
        self.assertIn("functions.present_item", sequence)
        self.assertNotIn("router.get", sequence)
        self.assertIn("getItem", (output / "API_CATALOG.md").read_text(encoding="utf-8"))
        self.assertIn("Item", (output / "INTERFACES.md").read_text(encoding="utf-8"))
        crud = (output / "CRUD.md").read_text(encoding="utf-8")
        self.assertRegex(crud, r"\| items \| C \| R \| U \| D \|")
        self.assertIn("create-1", (output / "QUERY_OBJECTS.md").read_text(encoding="utf-8"))
        manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
        self.assertTrue(all(len(value["sha256"]) == 64 for value in manifest["sources"]))
        self.assertEqual(designflow.main(args + ["--check"]), 0)
        functions = source / "items/functions.py"
        functions.write_text(functions.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        self.assertEqual(designflow.main(args + ["--check"]), 2)

    def test_nested_calls_follow_runtime_evaluation_order(self) -> None:
        path = self.root / "router.py"
        path.write_text(
            "@router.get('/nested')\n"
            "def nested():\n"
            "    return outer(inner())\n",
            encoding="utf-8",
        )
        calls = designflow.router_operations(path)[0]["calls"]
        self.assertEqual(calls, ["inner", "outer"])

    def test_response_variable_is_rejected(self) -> None:
        path = self.root / "router.py"
        path.write_text(
            "@router.get('/bad')\n"
            "def bad():\n"
            "    response = build()\n"
            "    return response\n",
            encoding="utf-8",
        )
        with self.assertRaises(designflow.DesignError):
            designflow.router_operations(path)

    def test_cloudformation_resources_and_parameters_are_generated(self) -> None:
        template = self.root / "stack.yaml"
        output = self.root / "cdk"
        template.write_text(
            "Parameters:\n"
            "  Stage:\n"
            "    Type: String\n"
            "    Default: dev\n"
            "    AllowedValues: [dev, prod]\n"
            "Resources:\n"
            "  Bucket:\n"
            "    Type: AWS::S3::Bucket\n"
            "    Properties:\n"
            "      BucketName: !Ref Stage\n",
            encoding="utf-8",
        )
        args = ["cdk", "--template", str(template), "--out", str(output)]
        self.assertEqual(designflow.main(args), 0)
        self.assertIn("AWS::S3::Bucket", (output / "RESOURCES.md").read_text(encoding="utf-8"))
        self.assertIn("Stage", (output / "PARAMETERS.md").read_text(encoding="utf-8"))
        self.assertEqual(designflow.main(args + ["--check"]), 0)


if __name__ == "__main__":
    unittest.main()
