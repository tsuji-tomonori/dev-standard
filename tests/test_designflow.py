from __future__ import annotations

import ast
import importlib.util
import io
import json
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

from tools import safe_io as portable_safe_io

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
        (self.root / "tools").mkdir()
        shutil.copyfile(ROOT / "tools/safe_io.py", self.root / "tools/safe_io.py")

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
            "    item = functions.load_item(\n"
            "        item_id, 'read.sql', 'create.sql', 'update.sql', 'delete.sql'\n"
            "    )\n"
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
                "parameters": [
                    {
                        "name": "item_id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "string"},
                    }
                ],
                "responses": {"200": {"description": "OK", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Item"}}}}},
            }}},
            "components": {"schemas": {"Item": {"type": "object", "required": ["id"], "properties": {"id": {"type": "string"}}}}},
        }), encoding="utf-8")
        (sql / "read.sql").write_text("SELECT id FROM items;\n", encoding="utf-8")
        (sql / "create.sql").write_text("INSERT INTO items (id) VALUES ('1');\n", encoding="utf-8")
        (sql / "update.sql").write_text("UPDATE items SET id = '2' WHERE id = '1';\n", encoding="utf-8")
        (sql / "delete.sql").write_text("DELETE FROM items WHERE id = '2';\n", encoding="utf-8")
        self.test_root = self.root / "tests"
        self.test_root.mkdir()
        (self.test_root / "test_items.py").write_text(
            "def test_get_item():\n"
            "    assert True\n",
            encoding="utf-8",
        )
        self.requirements = self.root / "requirements.json"
        self.requirements.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "requirements": [
                        {"id": "REQ-ITEM-001", "status": "active", "title": "Get an item"}
                    ],
                }
            ),
            encoding="utf-8",
        )
        self.trace = self.root / "trace.json"
        self.trace.write_text(
            json.dumps(
                {
                    "schema_version": 2,
                    "applicable_requirement_ids": ["REQ-ITEM-001"],
                    "links": [
                        {
                            "requirement_id": "REQ-ITEM-001",
                            "artifact": {"kind": "operation", "id": "getItem"},
                            "tests": ["tests/test_items.py::test_get_item"],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        return source, openapi, sql, output

    def trace_args(self) -> list[str]:
        return [
            "--requirements",
            str(self.requirements),
            "--trace",
            str(self.trace),
            "--test-root",
            str(self.test_root),
        ]

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
            *self.trace_args(),
            "--out",
            str(output),
            "--repo-root",
            str(self.root),
        ]
        self.assertEqual(designflow.main(args), 0)
        sequence = (output / "SEQUENCES.gen.md").read_text(encoding="utf-8")
        self.assertTrue(sequence.startswith("<!-- AUTO-GENERATED. DO NOT EDIT DIRECTLY."))
        self.assertIn(
            "Generate: `python tools/portable_python.py run "
            "<host-skill-path>/scripts/designflow.py -- fastapi",
            sequence,
        )
        self.assertIn(
            "Check: `python tools/portable_python.py run "
            "<host-skill-path>/scripts/designflow.py -- fastapi",
            sequence,
        )
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
        self.assertIn("item_id", (output / "INTERFACES.gen.md").read_text(encoding="utf-8"))
        self.assertIn(
            "tests/test_items.py::test_get_item",
            (output / "TEST_MANIFEST.gen.json").read_text(encoding="utf-8"),
        )
        self.assertIn("REQ-ITEM-001", (output / "TRACEABILITY.gen.md").read_text(encoding="utf-8"))
        self.assertEqual(json.loads((output / "ERROR_CASES.gen.json").read_text(encoding="utf-8"))["cases"], [])
        first = {path.name: path.read_bytes() for path in output.iterdir() if path.is_file()}
        self.assertEqual(designflow.main(args), 0)
        second = {path.name: path.read_bytes() for path in output.iterdir() if path.is_file()}
        self.assertEqual(first, second)
        self.assertEqual(designflow.main(args + ["--check"]), 0)
        after_check = {path.name: path.read_bytes() for path in output.iterdir() if path.is_file()}
        self.assertEqual(second, after_check)
        functions = source / "items/functions.py"
        functions.write_text(functions.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            self.assertEqual(designflow.main(args + ["--check"]), 2)
        self.assertIn(
            "docs/design/generated/api/manifest.json",
            stdout.getvalue(),
        )

    def test_nested_calls_follow_runtime_evaluation_order(self) -> None:
        path = self.root / "router.py"
        path.write_text(
            "from fastapi import APIRouter\n"
            "router = APIRouter()\n\n"
            "@router.get('/nested')\n"
            "def nested():\n"
            "    return outer(inner())\n",
            encoding="utf-8",
        )
        calls = designflow.router_operations(path)[0]["calls"]
        self.assertEqual(calls, ["inner", "outer"])

    def test_router_prefix_and_recursive_helper_effects_are_observed(self) -> None:
        domain = self.root / "src/items"
        domain.mkdir(parents=True)
        router = domain / "router.py"
        router.write_text(
            "from fastapi import APIRouter\n"
            "from . import functions\n\n"
            "router = APIRouter(prefix='/v1')\n\n"
            "@router.post('/items', operation_id='createItem')\n"
            "def create_item():\n"
            "    return functions.create_item()\n",
            encoding="utf-8",
        )
        (domain / "functions.py").write_text(
            "def persist():\n"
            "    return repository.execute('create.sql')\n\n"
            "def create_item():\n"
            "    persist()\n"
            "    inventory_client.publish()\n"
            "    return present()\n\n"
            "def present():\n"
            "    return {'ok': True}\n",
            encoding="utf-8",
        )
        operation = designflow.router_operations(router)[0]
        self.assertEqual(operation["path"], "/v1/items")
        self.assertIn("repository.execute", operation["calls"])
        self.assertIn("create.sql", operation["sql_files"])
        self.assertEqual(operation["external_effects"], ["inventory_client.publish"])

    def test_duplicate_routes_and_metadata_conflicts_are_rejected(self) -> None:
        first = {
            "method": "GET",
            "path": "/items",
            "operation_id": "getItems",
        }
        with self.assertRaises(designflow.DesignError):
            designflow.validate_operation_set([first, {**first, "operation_id": "other"}])
        handler = {
            **first,
            "operation_id_explicit": True,
            "metadata": {"x-permission": "items:read"},
        }
        document = {
            "paths": {
                "/items": {
                    "get": {
                        "operationId": "getItems",
                        "x-permission": "items:admin",
                        "responses": {"200": {"description": "OK"}},
                    }
                }
            }
        }
        with self.assertRaises(designflow.DesignError):
            designflow.openapi_docs(document, [handler])

    def test_trace_rejects_unknown_requirement_artifact_and_test_node(self) -> None:
        self.fastapi_fixture()
        artifact_requirements = {"getItem": ["REQ-ITEM-001"]}
        self.trace.write_text(
            json.dumps(
                {
                    "schema_version": 2,
                    "applicable_requirement_ids": ["REQ-ITEM-001"],
                    "links": [
                        {
                            "requirement_id": "REQ-ITEM-001",
                            "artifact": {"kind": "operation", "id": "getItem"},
                            "tests": ["tests/test_items.py::test_missing"],
                        }
                    ]
                }
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(designflow.DesignError, "pytest collection manifest"):
            designflow.traceability_view(
                self.requirements,
                self.trace,
                "operation",
                artifact_requirements,
                self.test_root,
                self.root,
            )
        self.trace.write_text(
            json.dumps(
                {
                    "schema_version": 2,
                    "applicable_requirement_ids": ["REQ-UNKNOWN"],
                    "links": [
                        {
                            "requirement_id": "REQ-UNKNOWN",
                            "artifact": {"kind": "operation", "id": "getItem"},
                            "tests": ["tests/test_items.py::test_get_item"],
                        }
                    ]
                }
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(designflow.DesignError, "unknown or inactive"):
            designflow.traceability_view(
                self.requirements,
                self.trace,
                "operation",
                artifact_requirements,
                self.test_root,
                self.root,
            )
        self.trace.write_text(
            json.dumps(
                {
                    "schema_version": 2,
                    "applicable_requirement_ids": ["REQ-ITEM-001"],
                    "links": [
                        {
                            "requirement_id": "REQ-ITEM-001",
                            "artifact": {"kind": "operation", "id": "getItem"},
                            "tests": [{"node": "tests/test_items.py::test_get_item"}],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(designflow.DesignError, "non-empty unique array"):
            designflow.traceability_view(
                self.requirements,
                self.trace,
                "operation",
                artifact_requirements,
                self.test_root,
                self.root,
            )

    def test_structured_inputs_reject_duplicate_mapping_keys(self) -> None:
        duplicate = self.root / "duplicate.json"
        duplicate.write_text('{"paths": {}, "paths": {}}', encoding="utf-8")
        with self.assertRaisesRegex(designflow.DesignError, "duplicate JSON mapping key"):
            designflow.load_structured(duplicate)

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
        output = self.root / "docs" / "design" / "generated" / "cdk" / "stack"
        template.write_text(
            "Parameters:\n"
            "  Stage:\n"
            "    Type: String\n"
            "    Default: dev\n"
            "    AllowedValues: [dev, prod]\n"
            "Resources:\n"
            "  Bucket:\n"
            "    Type: AWS::S3::Bucket\n"
            "    Metadata:\n"
            "      RequirementIds: [REQ-BUCKET-001]\n"
            "    Properties:\n"
            "      BucketName: !Ref Stage\n",
            encoding="utf-8",
        )
        self.test_root = self.root / "tests"
        self.test_root.mkdir()
        (self.test_root / "test_stack.py").write_text(
            "def test_bucket():\n"
            "    assert True\n",
            encoding="utf-8",
        )
        self.requirements = self.root / "requirements.json"
        self.requirements.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "requirements": [
                        {"id": "REQ-BUCKET-001", "status": "active", "title": "Store objects"}
                    ],
                }
            ),
            encoding="utf-8",
        )
        self.trace = self.root / "trace.json"
        self.trace.write_text(
            json.dumps(
                {
                    "schema_version": 2,
                    "applicable_requirement_ids": ["REQ-BUCKET-001"],
                    "links": [
                        {
                            "requirement_id": "REQ-BUCKET-001",
                            "artifact": {"kind": "resource", "id": "Bucket"},
                            "tests": ["tests/test_stack.py::test_bucket"],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        args = [
            "cdk",
            "--template", "stack.yaml",
            "--requirements", "requirements.json",
            "--trace", "trace.json",
            "--test-root", "tests",
            "--out",
            "docs/design/generated/cdk/stack",
            "--repo-root",
            str(self.root),
        ]
        (self.root / ".git").rmdir()
        self.assertEqual(designflow.main(args), 0)
        self.assertIn("AWS::S3::Bucket", (output / "RESOURCES.gen.md").read_text(encoding="utf-8"))
        self.assertIn("BucketName", (output / "RESOURCES.gen.md").read_text(encoding="utf-8"))
        self.assertIn("Stage", (output / "PARAMETERS.gen.md").read_text(encoding="utf-8"))
        self.assertIn("REQ-BUCKET-001", (output / "TRACEABILITY.gen.md").read_text(encoding="utf-8"))
        self.assertEqual(designflow.main(args + ["--check"]), 0)

    def test_portable_root_replacement_after_first_input_read_is_refused(self) -> None:
        template = self.root / "stack.json"
        template.write_text(
            json.dumps(
                {
                    "Resources": {
                        "Bucket": {
                            "Type": "AWS::S3::Bucket",
                            "Metadata": {"RequirementIds": ["REQ-BUCKET-001"]},
                        }
                    }
                }
            ),
            encoding="utf-8",
        )
        requirements = self.root / "requirements.json"
        requirements.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "requirements": [
                        {
                            "id": "REQ-BUCKET-001",
                            "status": "active",
                            "title": "Store objects",
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        tests = self.root / "tests"
        tests.mkdir()
        (tests / "test_stack.py").write_text(
            "def test_bucket() -> None:\n    assert True\n",
            encoding="utf-8",
        )
        trace = self.root / "trace.json"
        trace.write_text(
            json.dumps(
                {
                    "schema_version": 2,
                    "applicable_requirement_ids": ["REQ-BUCKET-001"],
                    "links": [
                        {
                            "requirement_id": "REQ-BUCKET-001",
                            "artifact": {"kind": "resource", "id": "Bucket"},
                            "tests": ["tests/test_stack.py::test_bucket"],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        output = self.root / "docs/design/generated/cdk/stack"
        displaced = self.root.with_name(f"{self.root.name}.displaced")
        self.addCleanup(shutil.rmtree, displaced, True)
        root_info = self.root.stat()
        runtime = mock.Mock()
        runtime.root_identity = (root_info.st_dev, root_info.st_ino)
        runtime.load_relative.return_value = portable_safe_io
        real_load = designflow.load_structured
        replaced = False

        def load_then_replace(path: Path):
            nonlocal replaced
            document = real_load(path)
            if path == template and not replaced:
                replaced = True
                self.root.rename(displaced)
                shutil.copytree(displaced, self.root)
            return document

        arguments = [
            "cdk",
            "--template",
            str(template),
            "--requirements",
            str(requirements),
            "--trace",
            str(trace),
            "--test-root",
            str(tests),
            "--out",
            "docs/design/generated/cdk/stack",
            "--repo-root",
            str(self.root),
        ]
        designflow._load_safe_io_module.cache_clear()
        try:
            with (
                mock.patch.dict(
                    sys.modules,
                    {"_dev_standard_portable_imports": runtime},
                ),
                mock.patch.object(
                    designflow,
                    "load_structured",
                    side_effect=load_then_replace,
                ),
            ):
                self.assertEqual(designflow.main(arguments), 2)
        finally:
            designflow._load_safe_io_module.cache_clear()

        self.assertTrue(replaced)
        self.assertFalse(output.exists())
        self.assertFalse((displaced / "docs/design/generated/cdk/stack").exists())

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
            *self.trace_args(),
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

    def test_structured_cfg_rejects_unprojectable_python_and_renders_branches(self) -> None:
        branch = self.root / "branch_router.py"
        branch.write_text(
            "from fastapi import APIRouter\n"
            "router = APIRouter()\n\n"
            "@router.get('/branch')\n"
            "def branch(flag: bool):\n"
            "    if flag:\n"
            "        notify_success()\n"
            "    else:\n"
            "        notify_failure()\n"
            "    return respond()\n",
            encoding="utf-8",
        )
        operation = designflow.router_operations(branch)[0]
        self.assertEqual(operation["flow"][0]["kind"], "branch")
        rendered = designflow.render_sequences([operation])
        self.assertIn("alt flag", rendered)
        self.assertIn("else otherwise", rendered)

        early_return = self.root / "early_return_router.py"
        early_return.write_text(
            "from fastapi import APIRouter\n"
            "router = APIRouter()\n\n"
            "@router.get('/early')\n"
            "def early(flag: bool):\n"
            "    if flag:\n"
            "        return reject()\n"
            "    return accept()\n",
            encoding="utf-8",
        )
        early_flow = designflow.router_operations(early_return)[0]["flow"]
        self.assertEqual([step["kind"] for step in early_flow], ["branch"])
        self.assertEqual(
            [step["name"] for step in early_flow[0]["then"] if step["kind"] == "call"],
            ["reject"],
        )
        self.assertEqual(
            [step["name"] for step in early_flow[0]["else"] if step["kind"] == "call"],
            ["accept"],
        )

        nested = self.root / "nested_router.py"
        nested.write_text(
            "from fastapi import APIRouter\n"
            "router = APIRouter()\n\n"
            "@router.get('/nested')\n"
            "def nested():\n"
            "    def never_called():\n"
            "        return hidden()\n"
            "    return respond()\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(designflow.DesignError, "nested definitions"):
            designflow.router_operations(nested)

        dynamic = self.root / "dynamic_router.py"
        dynamic.write_text(
            "from fastapi import APIRouter\n"
            "router = APIRouter()\n"
            "route_path = '/dynamic'\n\n"
            "@router.get(route_path)\n"
            "def dynamic():\n"
            "    return respond()\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(designflow.DesignError, "literal"):
            designflow.router_operations(dynamic)

        callback = self.root / "callback_router.py"
        callback.write_text(
            "from fastapi import APIRouter\n"
            "router = APIRouter()\n\n"
            "@router.get('/callback')\n"
            "def callback_route(callback):\n"
            "    return callback()\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(designflow.DesignError, "dynamic call target"):
            designflow.router_operations(callback)

        callback_attribute = self.root / "callback_attribute_router.py"
        callback_attribute.write_text(
            "from fastapi import APIRouter\n"
            "router = APIRouter()\n\n"
            "@router.get('/callback-attribute')\n"
            "def callback_attribute_route(callback):\n"
            "    return callback.respond()\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(designflow.DesignError, "dynamic call target"):
            designflow.router_operations(callback_attribute)

        (self.root / "functions.py").write_text(
            "def fail():\n"
            "    raise ValueError('boom')\n",
            encoding="utf-8",
        )
        helper_raise = self.root / "helper_raise_router.py"
        helper_raise.write_text(
            "from fastapi import APIRouter\n"
            "from . import functions\n"
            "router = APIRouter()\n\n"
            "@router.get('/helper-raise')\n"
            "def helper_raise():\n"
            "    functions.fail()\n"
            "    return respond()\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(designflow.DesignError, "helper raise is unsupported"):
            designflow.router_operations(helper_raise)

        unsupported = self.root / "loop_router.py"
        unsupported.write_text(
            "from fastapi import APIRouter\n"
            "router = APIRouter()\n\n"
            "@router.get('/loop')\n"
            "def loop():\n"
            "    for item in values():\n"
            "        consume(item)\n"
            "    return respond()\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(designflow.DesignError, "unsupported flow node For"):
            designflow.router_operations(unsupported)

        hidden_target = self.root / "target_router.py"
        hidden_target.write_text(
            "from fastapi import APIRouter\n"
            "router = APIRouter()\n\n"
            "@router.get('/target')\n"
            "def target():\n"
            "    container()[index()] = value()\n"
            "    return respond()\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(designflow.DesignError, "unsupported assignment target"):
            designflow.router_operations(hidden_target)

    def test_error_case_ids_are_global_and_collisions_fail_closed(self) -> None:
        first = {
            "method": "GET",
            "path": "/first",
            "operation_id": "first",
            "errors": [{"id": "ERR-NOT-FOUND"}],
        }
        second = {
            "method": "GET",
            "path": "/second",
            "operation_id": "second",
            "errors": [{"id": "ERR-NOT-FOUND"}],
        }
        with self.assertRaisesRegex(designflow.DesignError, "duplicate global error"):
            designflow.validate_operation_set([first, second])
        tree = ast.parse("def invalid():\n    return error_response(code='!!!')\n")
        with self.assertRaisesRegex(designflow.DesignError, "stable global ID"):
            designflow.error_cases(tree.body[0])

    def test_openapi_path_query_header_parameters_are_complete(self) -> None:
        operation = {
            "operationId": "getItem",
            "parameters": [
                {
                    "name": "item_id",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "string"},
                },
                {
                    "name": "expand",
                    "in": "query",
                    "schema": {"type": "boolean"},
                },
                {
                    "name": "X-Request-Id",
                    "in": "header",
                    "schema": {"type": "string"},
                },
            ],
            "responses": {"200": {"description": "OK"}},
        }
        document = {
            "paths": {"/items/{item_id}": {"get": operation}},
            "components": {"schemas": {}},
        }
        _, interfaces = designflow.openapi_docs(document)
        self.assertIn("`item_id` | path | yes", interfaces)
        self.assertIn("`expand` | query | no", interfaces)
        self.assertIn("`X-Request-Id` | header | no", interfaces)
        operation["parameters"] = []
        with self.assertRaisesRegex(designflow.DesignError, "path parameter mismatch"):
            designflow.openapi_docs(document)

        operation["parameters"] = [
            {
                "name": "item_id",
                "in": "path",
                "required": True,
                "schema": {"type": "string"},
            },
            {"name": "X-Request-Id", "in": "header", "schema": {"type": "string"}},
            {"name": "x-request-id", "in": "header", "schema": {"type": "string"}},
        ]
        with self.assertRaisesRegex(designflow.DesignError, "duplicate OpenAPI parameter"):
            designflow.openapi_docs(document)

    def test_sql_rejects_merge_unbound_and_ambiguous_basename_mapping(self) -> None:
        sql = self.root / "sql"
        sql.mkdir()
        (sql / "merge.sql").write_text(
            "MERGE INTO target USING source ON target.id = source.id "
            "WHEN MATCHED THEN UPDATE SET value = source.value;\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(designflow.DesignError, "unsupported SQL statement"):
            designflow.parse_sql(sql, self.root)

        (sql / "merge.sql").unlink()
        for directory in (sql / "a", sql / "b"):
            directory.mkdir()
            (directory / "read.sql").write_text("SELECT id FROM items;\n", encoding="utf-8")
        queries, _ = designflow.parse_sql(sql, self.root)
        operation = {"operation_id": "getItem", "sql_files": ["read.sql"]}
        with self.assertRaisesRegex(designflow.DesignError, "basename is ambiguous"):
            designflow.bind_operation_queries([operation], queries)
        operation["sql_files"] = ["a/read.sql"]
        with self.assertRaisesRegex(designflow.DesignError, "lack an explicit operation mapping"):
            designflow.bind_operation_queries([operation], queries)
        operation["sql_files"] = ["./a/read.sql", "b/read.sql"]
        with self.assertRaisesRegex(designflow.DesignError, "normalized relative path"):
            designflow.bind_operation_queries([operation], queries)

    def test_sql_mapping_uses_executed_literals_and_physical_tables(self) -> None:
        router = self.root / "dead_sql_router.py"
        router.write_text(
            "from fastapi import APIRouter\n"
            "router = APIRouter()\n\n"
            "@router.get('/items')\n"
            "def get_items():\n"
            "    unused = 'read.sql'\n"
            "    return respond()\n",
            encoding="utf-8",
        )
        operation = designflow.router_operations(router)[0]
        self.assertEqual(operation["sql_files"], [])

        sql = self.root / "sql"
        sql.mkdir()
        (sql / "read.sql").write_text(
            "WITH recent AS (SELECT id FROM users) SELECT * FROM recent;\n",
            encoding="utf-8",
        )
        (sql / "update.sql").write_text(
            "WITH recent AS (SELECT id FROM users) "
            "UPDATE items SET id = source.id FROM source "
            "JOIN recent ON source.id = recent.id;\n",
            encoding="utf-8",
        )
        queries, matrix = designflow.parse_sql(sql, self.root)
        query_by_file = {query["file"]: query for query in queries}
        self.assertEqual(query_by_file["read.sql"]["tables"], ["users"])
        self.assertEqual(
            query_by_file["update.sql"]["tables"],
            ["items", "source", "users"],
        )
        self.assertEqual(
            matrix,
            {"items": {"U"}, "source": {"R"}, "users": {"R"}},
        )
        with self.assertRaisesRegex(
            designflow.DesignError,
            "lack an explicit operation mapping",
        ):
            designflow.bind_operation_queries([operation], queries)

    def test_column_foreign_keys_and_explicit_query_mapping_are_rendered(self) -> None:
        ddl = self.root / "ddl"
        sql = self.root / "sql"
        ddl.mkdir()
        sql.mkdir()
        (ddl / "schema.sql").write_text(
            "CREATE TABLE parent (id INT PRIMARY KEY);\n"
            "CREATE TABLE child (id INT PRIMARY KEY, parent_id INT REFERENCES parent(id));\n",
            encoding="utf-8",
        )
        (sql / "write.sql").write_text(
            "INSERT INTO child (id, parent_id) VALUES (1, 2);\n",
            encoding="utf-8",
        )
        operations = [
            {
                "operation_id": "createChild",
                "sql_files": ["write.sql"],
            }
        ]
        rendered = designflow.ddl_docs(ddl, sql, operations)
        self.assertIn("`child` | `parent_id` | `parent` | `id`", rendered)
        self.assertIn("createChild", rendered)

    def test_applicable_requirements_are_exact_without_requiring_all_active(self) -> None:
        self.fastapi_fixture()
        document = json.loads(self.requirements.read_text(encoding="utf-8"))
        document["requirements"].append(
            {"id": "REQ-UNRELATED-001", "status": "active", "title": "Unrelated"}
        )
        self.requirements.write_text(json.dumps(document), encoding="utf-8")
        rendered = designflow.traceability_view(
            self.requirements,
            self.trace,
            "operation",
            {"getItem": ["REQ-ITEM-001"]},
            self.test_root,
            self.root,
        )
        self.assertIn("REQ-ITEM-001", rendered)
        self.assertNotIn("REQ-UNRELATED-001", rendered)
        trace = json.loads(self.trace.read_text(encoding="utf-8"))
        trace["applicable_requirement_ids"].append("REQ-UNRELATED-001")
        self.trace.write_text(json.dumps(trace), encoding="utf-8")
        with self.assertRaisesRegex(designflow.DesignError, "explicit applicable"):
            designflow.traceability_view(
                self.requirements,
                self.trace,
                "operation",
                {"getItem": ["REQ-ITEM-001"]},
                self.test_root,
                self.root,
            )

    def test_pytest_manifest_rejects_noncollectable_and_symlinked_nodes(self) -> None:
        tests = self.root / "tests"
        tests.mkdir()
        (tests / "test_nodes.py").write_text(
            "import pytest\n\n"
            "def test_real():\n"
            "    assert True\n\n"
            "@pytest.mark.parametrize('value', [1])\n"
            "def test_parameterized(value):\n"
            "    assert value\n\n"
            "@pytest.mark.parametrize('value', [1, 2])\n"
            "class TestParameterized:\n"
            "    def test_value(self, value):\n"
            "        assert value\n",
            encoding="utf-8",
        )
        manifest = designflow.pytest_collection_manifest(tests, self.root)
        self.assertIn("tests/test_nodes.py::test_real", manifest["nodes"])
        self.assertNotIn("tests/test_nodes.py::test_parameterized", manifest["nodes"])
        self.assertNotIn(
            "tests/test_nodes.py::TestParameterized::test_value",
            manifest["nodes"],
        )
        linked = self.root / "linked-tests"
        linked.symlink_to(tests, target_is_directory=True)
        with self.assertRaisesRegex(designflow.DesignError, "unsafe input tree"):
            designflow.pytest_collection_manifest(linked, self.root)

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
            *self.trace_args(),
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

    def test_output_swap_during_publication_preserves_competing_directory(self) -> None:
        generated = self.root / "docs" / "design" / "generated"
        out = generated / "api"
        source = self.root / "source.txt"
        source.write_text("source\n", encoding="utf-8")
        files = {
            "API.gen.json": json.dumps(
                {
                    "notice": "AUTO-GENERATED. DO NOT EDIT DIRECTLY.",
                    "value": 1,
                }
            )
        }
        designflow.write_bundle(
            out,
            files,
            [("source", source)],
            "fastapi",
            repository_root=self.root,
        )

        real_rename = designflow.os.rename
        real_noreplace = designflow.rename_directory_noreplace
        displaced = generated / ".api.racer-managed"
        swapped = False

        def swap_before_backup(
            safe_io: object,
            source_fd: int,
            source_name: str,
            destination_fd: int,
            destination_name: str,
            *,
            display: Path,
        ) -> None:
            nonlocal swapped
            if (
                not swapped
                and source_name == out.name
                and destination_name.startswith(".api.backup-")
            ):
                swapped = True
                real_rename(
                    source_name,
                    displaced.name,
                    src_dir_fd=source_fd,
                    dst_dir_fd=destination_fd,
                )
                designflow.os.mkdir(source_name, dir_fd=source_fd)
                (out / "human.txt").write_text("preserve", encoding="utf-8")
            real_noreplace(
                safe_io,
                source_fd,
                source_name,
                destination_fd,
                destination_name,
                display=display,
            )

        files["API.gen.json"] = json.dumps(
            {
                "notice": "AUTO-GENERATED. DO NOT EDIT DIRECTLY.",
                "value": 2,
            }
        )
        with mock.patch.object(
            designflow,
            "rename_directory_noreplace",
            side_effect=swap_before_backup,
        ):
            with self.assertRaisesRegex(designflow.DesignError, "changed after validation"):
                designflow.write_bundle(
                    out,
                    files,
                    [("source", source)],
                    "fastapi",
                    repository_root=self.root,
                )
        self.assertEqual((out / "human.txt").read_text(encoding="utf-8"), "preserve")
        self.assertTrue((displaced / "manifest.json").is_file())

    def test_check_rejects_byte_identical_actual_directory_replacement(self) -> None:
        source, openapi, sql, output = self.fastapi_fixture()
        args = [
            "fastapi",
            "--source-root",
            str(source),
            "--openapi",
            str(openapi),
            "--sql-root",
            str(sql),
            *self.trace_args(),
            "--out",
            str(output),
            "--repo-root",
            str(self.root),
        ]
        self.assertEqual(designflow.main(args), 0)
        displaced = output.with_name(".api.validated-before-check")
        real_generate = designflow.generate_fastapi
        swapped = False

        def generate_then_replace(*values: object, **keywords: object) -> None:
            nonlocal swapped
            real_generate(*values, **keywords)
            if keywords.get("candidate") and not swapped:
                swapped = True
                output.rename(displaced)
                shutil.copytree(displaced, output)

        stdout = io.StringIO()
        with (
            mock.patch.object(
                designflow, "generate_fastapi", side_effect=generate_then_replace
            ),
            redirect_stdout(stdout),
        ):
            self.assertEqual(designflow.main(args + ["--check"]), 2)

        self.assertTrue(swapped)
        self.assertIn("changed after validation", stdout.getvalue())
        self.assertTrue((output / "manifest.json").is_file())
        self.assertTrue((displaced / "manifest.json").is_file())

    def test_check_rebinds_actual_name_after_pinned_comparison(self) -> None:
        source, openapi, sql, output = self.fastapi_fixture()
        args = [
            "fastapi",
            "--source-root",
            str(source),
            "--openapi",
            str(openapi),
            "--sql-root",
            str(sql),
            *self.trace_args(),
            "--out",
            str(output),
            "--repo-root",
            str(self.root),
        ]
        self.assertEqual(designflow.main(args), 0)
        actual, identity = designflow.validate_existing_output_path(
            output, self.root
        )
        displaced = output.with_name(".api.pinned-during-check")
        real_identity = designflow.pinned_directory_identity
        actual_identity_calls = 0

        def swap_after_actual_comparison(
            descriptor: int,
            *,
            display: Path,
            safe_io: object,
        ) -> tuple[int, int, str]:
            nonlocal actual_identity_calls
            result = real_identity(
                descriptor,
                display=display,
                safe_io=safe_io,
            )
            if display == output:
                actual_identity_calls += 1
                if actual_identity_calls == 2:
                    output.rename(displaced)
                    shutil.copytree(displaced, output)
            return result

        with tempfile.TemporaryDirectory(prefix="designflow-check-") as directory:
            candidate = Path(directory) / "api"
            shutil.copytree(output, candidate)
            with mock.patch.object(
                designflow,
                "pinned_directory_identity",
                side_effect=swap_after_actual_comparison,
            ):
                with self.assertRaisesRegex(designflow.DesignError, "name changed"):
                    designflow.compare_bundle(
                        candidate,
                        actual,
                        repository_root=self.root,
                        actual_identity=identity,
                    )

        self.assertEqual(actual_identity_calls, 3)
        self.assertTrue((output / "manifest.json").is_file())
        self.assertTrue((displaced / "manifest.json").is_file())

    def test_output_parent_swap_is_refused_before_any_external_stage_write(self) -> None:
        design = self.root / "docs" / "design"
        design.mkdir(parents=True)
        out = design / "generated" / "api"
        source = self.root / "source.txt"
        source.write_text("source\n", encoding="utf-8")
        external = Path(tempfile.mkdtemp(prefix="designflow-external-"))
        self.addCleanup(shutil.rmtree, external)
        displaced = design / "generated-pinned"
        real_mkdir = designflow.os.mkdir
        swapped = False

        def swap_created_parent(
            name: str,
            mode: int = 0o777,
            *,
            dir_fd: int | None = None,
        ) -> None:
            nonlocal swapped
            real_mkdir(name, mode=mode, dir_fd=dir_fd)
            if name == "generated" and dir_fd is not None and not swapped:
                swapped = True
                designflow.os.rename(
                    name,
                    displaced.name,
                    src_dir_fd=dir_fd,
                    dst_dir_fd=dir_fd,
                )
                designflow.os.symlink(
                    external,
                    name,
                    target_is_directory=True,
                    dir_fd=dir_fd,
                )

        files = {
            "API.gen.json": json.dumps(
                {
                    "notice": "AUTO-GENERATED. DO NOT EDIT DIRECTLY.",
                    "value": 1,
                }
            )
        }
        with mock.patch.object(designflow.os, "mkdir", side_effect=swap_created_parent):
            with self.assertRaisesRegex(designflow.DesignError, "unsafe"):
                designflow.write_bundle(
                    out,
                    files,
                    [("source", source)],
                    "fastapi",
                    repository_root=self.root,
                )

        self.assertTrue(swapped)
        self.assertEqual(list(external.iterdir()), [])

    def test_base_exception_cleans_descriptor_staged_bundle(self) -> None:
        generated = self.root / "docs" / "design" / "generated"
        out = generated / "api"
        source = self.root / "source.txt"
        source.write_text("source\n", encoding="utf-8")
        files = {
            "API.gen.json": json.dumps(
                {
                    "notice": "AUTO-GENERATED. DO NOT EDIT DIRECTLY.",
                    "value": 1,
                }
            )
        }

        with mock.patch.object(designflow.os, "write", side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                designflow.write_bundle(
                    out,
                    files,
                    [("source", source)],
                    "fastapi",
                    repository_root=self.root,
                )

        self.assertFalse(out.exists())
        self.assertEqual(list(generated.glob(".api.candidate-*")), [])

    def test_base_exception_cleans_external_check_candidate_by_parent_fd(self) -> None:
        source = self.root / "source.txt"
        source.write_text("source\n", encoding="utf-8")
        files = {
            "API.gen.json": json.dumps(
                {
                    "notice": "AUTO-GENERATED. DO NOT EDIT DIRECTLY.",
                    "value": 1,
                }
            )
        }
        with tempfile.TemporaryDirectory(prefix="designflow-check-") as directory:
            parent = Path(directory)
            out = parent / "api"
            with mock.patch.object(
                designflow.os, "write", side_effect=KeyboardInterrupt
            ):
                with self.assertRaises(KeyboardInterrupt):
                    designflow.write_bundle(
                        out,
                        files,
                        [("source", source)],
                        "fastapi",
                        repository_root=self.root,
                        candidate=True,
                    )

            self.assertFalse(out.exists())
            self.assertEqual(list(parent.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
