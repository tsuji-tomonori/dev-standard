from __future__ import annotations

import copy
import hashlib
import json
import runpy
import unittest

import test_designflow as legacy

designflow = legacy.designflow


class ApiDocumentsTest(unittest.TestCase):
    """6帳票の内容・欠落・テスト対応と非破壊drift検査を検証する。"""

    def setUp(self) -> None:
        legacy.DesignflowTest.setUp(self)
        self.addCleanup(self.temp.cleanup)
        self.source, self.openapi, self.sql, self.out = legacy.DesignflowTest.fastapi_fixture(self)
        self.model_path = self.root / 'api-model.json'
        source = {"path": "src/items/router.py", "line": 6}
        self.operation = {
            "id": "getItem", "summary": "商品IDで在庫DBの商品を取得する。",
            "source": source, "preconditions": "item_idを指定する。",
            "inputs": [{"name": "item_id", "type": "string", "description": "商品ID", "origin": "path"}],
            "outputs": [{"name": "id", "type": "string", "description": "商品ID", "origin": "inventory.items.id"}],
            "errors": "商品がない場合は404とし、DBを書き換えない。",
            "resources": [{"id": "R1", "database": "inventory", "table": "items", "action": "参照",
                           "input": "item_id", "output": "商品1件または0件", "condition": "id一致",
                           "query_id": "Q1", "source": source}],
            "queries": [{"id": "Q1", "database": "inventory", "table": "items", "kind": "SELECT",
                         "summary": "商品IDに一致する商品を取得する。", "conditions": "id = :item_id",
                         "arguments": [{"name": "item_id", "type": "str", "description": "対象ID"}],
                         "returns": "Item | None", "transaction": "読み取りのみ", "source": source}],
            "messages": [{"id": "item.read", "level": "INFO", "template": "商品参照を完了した。",
                          "condition": "取得完了時", "operator_action": "通常は対応不要",
                          "fields": [{"name": "request_id", "type": "str", "description": "追跡ID", "masking": "不要"}],
                          "source": source}],
            "factors": [{"id": "F1", "name": "商品有無", "source": source, "elements": [
                {"id": "exists", "description": "商品あり", "expected": "200と商品"},
                {"id": "missing", "description": "商品なし", "expected": "404"},
            ]}],
            "cases": [
                {"id": "TC1", "given": "商品Aを登録済み", "when": "Aを取得", "then": "200、id=A",
                 "expected_logs": "item.readが1件", "expected_data": "変更なし",
                 "covers": [["F1", "exists"]], "tests": ["tests/test_items.py::test_get_item"]},
                {"id": "TC2", "given": "商品なし", "when": "Aを取得", "then": "404",
                 "expected_logs": "item.readは出力しない", "expected_data": "変更なし",
                 "covers": [["F1", "missing"]], "tests": ["tests/test_items.py::test_missing_item"]},
            ],
            "sequence": "sequenceDiagram\n    participant C as 呼び出し元\n    participant A as API\n    participant D as データベース\n    C->>A: 商品取得\n    A->>D: 商品参照\n    D-->>A: 検索結果\n    alt 商品あり\n        A-->>C: 200 商品\n    else 商品なし\n        A-->>C: 404\n    end\n",
        }
        (self.source / 'items/functions.py').unlink()
        (self.source / 'items/router.py').write_text(
            "import logging\n\n"
            "def get_item(connection, item_id, request_id):\n"
            "    row = connection.execute('SELECT id FROM items WHERE id = :item_id', {'item_id': item_id}).fetchone()\n"
            "    if row is None:\n"
            "        return 404, {'error': 'not_found'}\n"
            "    logging.getLogger('api-fixture').info('商品参照を完了した。', extra={'request_id': request_id, 'message_id': 'item.read'})\n"
            "    return 200, {'id': row[0]}\n", encoding='utf-8',
        )
        (self.test_root / 'test_items.py').write_text(
            "import logging\nimport runpy\nimport sqlite3\nfrom pathlib import Path\n\n"
            "get_item = runpy.run_path(str(Path(__file__).parents[1] / 'src/items/router.py'))['get_item']\n\n"
            "def check_case(present):\n"
            "    connection = sqlite3.connect(':memory:')\n"
            "    connection.execute('CREATE TABLE items (id TEXT)')\n"
            "    if present:\n        connection.execute(\"INSERT INTO items VALUES ('A')\")\n"
            "    before = connection.execute('SELECT * FROM items').fetchall()\n"
            "    records = []\n"
            "    handler = logging.Handler()\n"
            "    handler.emit = records.append\n"
            "    logger = logging.getLogger('api-fixture')\n"
            "    previous = logger.level\n"
            "    logger.setLevel(logging.INFO)\n"
            "    logger.addHandler(handler)\n"
            "    try:\n"
            "        result = get_item(connection, 'A', 'req-1')\n"
            "        assert result == ((200, {'id': 'A'}) if present else (404, {'error': 'not_found'}))\n"
            "        assert connection.execute('SELECT * FROM items').fetchall() == before\n"
            "        assert len(records) == int(present)\n"
            "        if present:\n"
            "            assert records[0].request_id == 'req-1'\n"
            "            assert records[0].getMessage() == '商品参照を完了した。'\n"
            "    finally:\n"
            "        logger.removeHandler(handler)\n"
            "        logger.setLevel(previous)\n"
            "        connection.close()\n\n"
            "def test_get_item():\n    check_case(True)\n\n"
            "def test_missing_item():\n    check_case(False)\n", encoding='utf-8',
        )
        self.model = {"schema_version": 1, "operations": [self.operation]}
        self.save_model()
        self.argv = ['api-documents', '--repo-root', str(self.root), '--source-root', str(self.source),
                     '--openapi', str(self.openapi), '--test-root', str(self.test_root),
                     '--model', str(self.model_path), '--out', str(self.out)]

    def save_model(self) -> None:
        paths = [*self.source.rglob('*.py'), *self.test_root.rglob('test*.py'), self.openapi]
        self.model['source_sha256'] = {p.relative_to(self.root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
        self.model_path.write_text(json.dumps(self.model, ensure_ascii=False), encoding='utf-8')

    def render(self) -> dict[str, str]:
        return designflow.render_api_documents(
            self.model, json.loads(self.openapi.read_text()),
            designflow.pytest_collection_manifest(self.test_root, self.root),
            root=self.root, implementation_sources=set(self.source.rglob('*.py')),
        )

    def test_mapped_fixture_cases_execute_response_log_and_database_assertions(self) -> None:
        namespace = runpy.run_path(str(self.test_root / 'test_items.py'))
        for case in self.operation['cases']:
            for node in case['tests']:
                namespace[node.split('::')[1]]()

    def test_six_documents_have_semantic_fields_and_swagger(self) -> None:
        files = self.render()
        token = hashlib.sha256(b'getItem').hexdigest()[:16]
        self.assertTrue(all(f'{token}.{kind}.gen.md' in files for kind in designflow.API_DOCUMENT_KINDS))
        detail = files[f'{token}.detail-design.gen.md']
        self.assertIn('inventory', detail)
        self.assertIn('inventory.items.id', detail)
        query = files[f'{token}.query.gen.md']
        self.assertIn('id = :item_id', query)
        self.assertIn('Item &#124; None', query)
        self.assertIn('request_id', files[f'{token}.messages.gen.md'])
        self.assertIn('tests/test_items.py::test_missing_item', files[f'{token}.unit-test.gen.md'])
        self.assertIn('alt 商品あり', files[f'{token}.sequence.gen.md'])
        exported = json.loads(files['OPENAPI.gen.json'])
        self.assertEqual(exported['paths'], json.loads(self.openapi.read_text())['paths'])
        self.assertIn('"get"', files[f'{token}.interface.gen.md'])

    def test_generate_repeat_check_and_missing_each_document(self) -> None:
        self.assertEqual(designflow.main(self.argv), 0)
        original = {p.name: p.read_bytes() for p in self.out.iterdir()}
        self.assertEqual(designflow.main(self.argv), 0)
        self.assertEqual(original, {p.name: p.read_bytes() for p in self.out.iterdir()})
        self.assertEqual(designflow.main(self.argv + ['--check']), 0)
        for kind in designflow.API_DOCUMENT_KINDS:
            file = next(self.out.glob(f'*.{kind}.gen.md'))
            payload = file.read_bytes()
            file.unlink()
            self.assertNotEqual(designflow.main(self.argv + ['--check']), 0)
            self.assertFalse(file.exists())
            file.write_bytes(payload)

    def test_stale_implementation_is_not_repaired_by_check(self) -> None:
        self.assertEqual(designflow.main(self.argv), 0)
        file = self.source / 'items/router.py'
        file.write_text(file.read_text() + '\n# 変更\n')
        self.assertNotEqual(designflow.main(self.argv + ['--check']), 0)

    def test_missing_required_semantics_fail(self) -> None:
        for group, key in [('queries', 'conditions'), ('messages', 'template'), ('resources', 'database'), ('cases', 'given')]:
            with self.subTest(group=group, key=key):
                backup = self.operation[group][0].pop(key)
                with self.assertRaises(designflow.DesignError):
                    self.render()
                self.operation[group][0][key] = backup

    def test_uncovered_unknown_and_nonexistent_test_fail(self) -> None:
        original = copy.deepcopy(self.operation['cases'])
        self.operation['cases'].pop()
        with self.assertRaisesRegex(designflow.DesignError, 'uncovered'):
            self.render()
        self.operation['cases'] = copy.deepcopy(original)
        self.operation['cases'][0]['covers'] = [['F1', 'unknown']]
        with self.assertRaisesRegex(designflow.DesignError, 'unknown'):
            self.render()
        self.operation['cases'] = copy.deepcopy(original)
        self.operation['cases'][0]['tests'] = ['tests/test_items.py::test_deleted']
        with self.assertRaisesRegex(designflow.DesignError, 'collection manifest'):
            self.render()

    def test_api_addition_and_wrong_database_fail(self) -> None:
        document = json.loads(self.openapi.read_text())
        document['paths']['/extra'] = {'get': {'operationId': 'extra', 'responses': {}}}
        self.openapi.write_text(json.dumps(document))
        with self.assertRaisesRegex(designflow.DesignError, 'inventory'):
            self.render()
        document['paths'].pop('/extra')
        self.openapi.write_text(json.dumps(document))
        self.operation['resources'][0]['database'] = 'wrong'
        with self.assertRaisesRegex(designflow.DesignError, 'destination'):
            self.render()

    def test_no_database_or_logs_still_produces_six_with_reasons(self) -> None:
        for group in ['resources', 'queries', 'messages']:
            self.operation[group] = []
            with self.assertRaises(designflow.DesignError):
                self.render()
            self.operation[f'no_{group}_reason'] = 'このAPIは当該操作を行わない。'
        self.assertEqual(len([name for name in self.render() if name.endswith('.gen.md')]), 7)
