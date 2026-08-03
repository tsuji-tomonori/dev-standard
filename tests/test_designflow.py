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
        (self.root / ".git").mkdir()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def fastapi_fixture(self) -> tuple[Path, Path, Path, Path]:
        source = self.root / "src"
        sql = self.root / "sql"
        output = self.root / "docs" / "design" / "generated" / "api"
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
        args = [
            "fastapi",
            "--source-root",
            str(source),
            "--openapi",
            str(openapi),
            "--sql-root",
            str(sql),
            "--out",
            str(output),
            "--repo-root",
            str(self.root),
        ]
        self.assertEqual(designflow.main(args), 0)
        sequence = (output / "SEQUENCES.gen.md").read_text(encoding="utf-8")
        self.assertTrue(sequence.startswith("<!-- AUTO-GENERATED. DO NOT EDIT DIRECTLY."))
        self.assertIn("Generate: `python .agents/skills/generate-implementation-design/scripts/designflow.py fastapi", sequence)
        self.assertIn("Check: `python .agents/skills/generate-implementation-design/scripts/designflow.py fastapi", sequence)
        self.assertIn("functions.load_item", sequence)
        self.assertIn("functions.present_item", sequence)
        self.assertNotIn("router.get", sequence)
        self.assertIn("getItem", (output / "API_CATALOG.gen.md").read_text(encoding="utf-8"))
        self.assertIn("Item", (output / "INTERFACES.gen.md").read_text(encoding="utf-8"))
        crud = (output / "CRUD.gen.md").read_text(encoding="utf-8")
        self.assertRegex(crud, r"\| items \| C \| R \| U \| D \|")
        self.assertIn("create-1", (output / "QUERY_OBJECTS.gen.md").read_text(encoding="utf-8"))
        manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
        self.assertTrue(all(len(value["sha256"]) == 64 for value in manifest["sources"]))
        self.assertTrue(all(not value["path"].startswith("/") for value in manifest["sources"]))
        self.assertNotIn(str(self.root), (output / "QUERY_OBJECTS.gen.md").read_text(encoding="utf-8"))
        self.assertEqual(manifest["notice"], "AUTO-GENERATED. DO NOT EDIT DIRECTLY.")
        self.assertTrue(all(name.endswith((".gen.md", ".gen.json")) for name in manifest["generated"]))
        self.assertTrue((output / "API_DETAILS.gen.md").is_file())
        self.assertEqual(json.loads((output / "ERROR_CASES.gen.json").read_text(encoding="utf-8"))["cases"], [])
        first = {path.name: path.read_bytes() for path in output.iterdir() if path.is_file()}
        self.assertEqual(designflow.main(args), 0)
        second = {path.name: path.read_bytes() for path in output.iterdir() if path.is_file()}
        self.assertEqual(first, second)
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
        output = self.root / "docs" / "design" / "generated" / "cdk"
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
        args = ["cdk", "--template", str(template), "--out", str(output), "--repo-root", str(self.root)]
        self.assertEqual(designflow.main(args), 0)
        self.assertIn("AWS::S3::Bucket", (output / "RESOURCES.gen.md").read_text(encoding="utf-8"))
        self.assertIn("Stage", (output / "PARAMETERS.gen.md").read_text(encoding="utf-8"))
        self.assertEqual(designflow.main(args + ["--check"]), 0)

    def test_fastapi_optional_authorities_generate_complete_as_built_views(self) -> None:
        source, openapi, sql, output = self.fastapi_fixture()
        ddl = self.root / "ddl"
        e2e = self.root / "e2e"
        tool = self.root / "tool"
        ddl.mkdir()
        e2e.mkdir()
        tool.mkdir()
        (ddl / "schema.sql").write_text(
            "CREATE TABLE items (id TEXT PRIMARY KEY, parent_id TEXT, "
            "FOREIGN KEY (parent_id) REFERENCES items(id));\n",
            encoding="utf-8",
        )
        (e2e / "test_items.py").write_text(
            "def test_get_item():\n"
            "    \"\"\"既存itemを取得できる。\"\"\"\n"
            "    # Given: item exists\n"
            "    item_id = '1'\n"
            "    # When: API is called\n"
            "    response = item_id\n"
            "    # Then: item is returned\n"
            "    assert response == item_id\n",
            encoding="utf-8",
        )
        (tool / "tools.py").write_text(
            "import argparse\n\n"
            "def run():\n"
            "    \"\"\"Generate the declared artifact.\"\"\"\n"
            "    parser = argparse.ArgumentParser()\n"
            "    parser.add_argument('--out')\n"
            "    return parser.parse_args([])\n",
            encoding="utf-8",
        )
        evidence = self.root / "evidence.json"
        evidence.write_text(
            json.dumps({"runs": [{"id": "run-1", "status": "passed", "api_response": "https://ci.example/api", "db_result": "https://ci.example/db", "mock_result": "https://ci.example/mock"}]}),
            encoding="utf-8",
        )
        args = [
            "fastapi",
            "--source-root",
            str(source),
            "--openapi",
            str(openapi),
            "--sql-root",
            str(sql),
            "--ddl-root",
            str(ddl),
            "--e2e-root",
            str(e2e),
            "--tool-root",
            str(tool),
            "--evidence",
            str(evidence),
            "--out",
            str(output),
            "--repo-root",
            str(self.root),
        ]
        self.assertEqual(designflow.main(args), 0)
        for name in ["DB_DESIGN.gen.md", "E2E_SCENARIOS.gen.md", "TOOLS.gen.md", "TEST_EVIDENCE.gen.md"]:
            self.assertTrue((output / name).is_file(), name)
        self.assertIn("items", (output / "DB_DESIGN.gen.md").read_text(encoding="utf-8"))
        self.assertIn("Given", (output / "E2E_SCENARIOS.gen.md").read_text(encoding="utf-8"))
        self.assertIn("--out", (output / "TOOLS.gen.md").read_text(encoding="utf-8"))
        self.assertNotIn("response body", (output / "TEST_EVIDENCE.gen.md").read_text(encoding="utf-8"))

        evidence.write_text(
            json.dumps({"runs": [{"id": "run-2", "status": "passed", "api_response": "response body", "db_result": "-", "mock_result": "-"}]}),
            encoding="utf-8",
        )
        self.assertEqual(designflow.main(args), 2)

    def test_output_rejects_escape_symlink_and_unmanaged_replacement(self) -> None:
        source, openapi, sql, _ = self.fastapi_fixture()
        base = [
            "fastapi",
            "--source-root",
            str(source),
            "--openapi",
            str(openapi),
            "--sql-root",
            str(sql),
            "--repo-root",
            str(self.root),
        ]
        self.assertEqual(designflow.main(base + ["--out", str(self.root / "outside")]), 2)
        unmanaged = self.root / "docs" / "design" / "generated" / "unmanaged"
        unmanaged.mkdir(parents=True)
        (unmanaged / "human.txt").write_text("preserve", encoding="utf-8")
        self.assertEqual(designflow.main(base + ["--out", str(unmanaged)]), 2)
        self.assertEqual((unmanaged / "human.txt").read_text(encoding="utf-8"), "preserve")
        link = self.root / "docs" / "design" / "generated" / "linked"
        link.symlink_to(self.root / "outside", target_is_directory=True)
        self.assertEqual(designflow.main(base + ["--out", str(link / "bundle")]), 2)


if __name__ == "__main__":
    unittest.main()
