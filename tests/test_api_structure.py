"""固定profileの章、階層、CRUDと移行driftを実sourceで検証する。"""
from __future__ import annotations

import copy
import csv
import hashlib
import io
import json
import unittest

from test_api_documents import ApiDocumentsTest, designflow

structure = designflow.api_helper('api_structure')


class ApiStructureTest(unittest.TestCase):
    def setUp(self):
        self.fixture = ApiDocumentsTest()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        f = self.fixture
        self.root, self.op, self.model = f.root, f.operation, f.model
        self.model.update(structure_profile='lazunex-v1', python_root='src')
        self.op.update(group='items', slug='get-item', router_implicit='入力はitem_idを受け取る。',
                       no_samples_reason='このfixtureは直接呼出しのためHTTP sampleを持たない。')
        sql = f.source / 'items/sql/read.sql'
        sql.parent.mkdir()
        sql.write_text('SELECT id FROM items WHERE id = :item_id')
        self.op['accesses'] = [{'store': 'inventory', 'phase': 'runtime', 'sql': 'src/items/sql/read.sql',
                                'source': {'path': 'src/items/router.py', 'line': 4}}]
        self.save()

    def save(self):
        self.fixture.save_model()
        for path in self.fixture.source.rglob('*.sql'):
            self.model['source_sha256'][path.relative_to(self.root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
        self.fixture.model_path.write_text(json.dumps(self.model, ensure_ascii=False))

    def render(self):
        return self.fixture.render()

    def test_reference_chapters_hierarchy_and_custom_names(self):
        files = self.render()
        structure.validate_structure(files, self.model, json.loads(self.fixture.openapi.read_text()))
        self.assertIn('items/get-item/detail-design_gen.md', files)
        self.assertIn('items/index.gen.md', files)
        self.assertIn('crud/access.gen.csv', files)
        self.assertIn('Headers', files['items/get-item/if_gen.html'])
        self.model['document_names'] = {'interface': 'interface.gen.md'}
        self.assertIn('items/get-item/interface.gen.md', self.render())
        self.assertNotIn('items/get-item/if_gen.md', self.render())

    def test_chapter_deletion_reorder_duplicate_and_fence_spoof_rejected(self):
        files = self.render()
        name = 'items/get-item/detail-design_gen.md'
        original = files[name]
        for mutated in [original.replace('## 2. 正常系前提', '前提'),
                        original.replace('## 2. 正常系前提', '## 1. 正常系入力'),
                        original.replace('## 1. 正常系入力', '## 2. 正常系前提').replace('## 4. 正常系レスポンス', '## 1. 正常系入力'),
                        original.replace('## 2. 正常系前提', '```\n## 2. 正常系前提\n```')]:
            with self.subTest(mutated=mutated[:40]), self.assertRaisesRegex(ValueError, 'chapter'):
                structure.validate_document('detail-design', mutated, self.op)
        with self.assertRaisesRegex(ValueError, 'SQL subsections'):
            structure.validate_document('query', files['items/get-item/query_gen.md'].replace('### 条件', '条件'), self.op)
        with self.assertRaisesRegex(ValueError, 'chapter'):
            structure.validate_document('query', '# query\n', self.op)

    def test_missing_case_and_log_details_detected(self):
        files = self.render()
        for kind, replacement in [('unit-test', '### TC2'), ('messages', '### item.read')]:
            name = structure.names(self.model, self.op)[kind]
            with self.assertRaisesRegex(ValueError, 'repeated|chapter'):
                structure.validate_document(kind, files[name].replace(replacement, replacement[1:]), self.op)

    def test_crud_model_csv_table_diagram_share_access_and_no_access(self):
        files = self.render()
        data = json.loads(files['crud/model.gen.json'])
        self.assertEqual([(r['resource'], r['action']) for r in data['accesses']], [('items', 'R')])
        rows = list(csv.reader(io.StringIO(files['crud/access.gen.csv'])))
        self.assertEqual(rows, [['API', 'inventory:items'], ['getItem', 'R']])
        self.assertIn('A0 -->|R| R0', files['crud/index.gen.md'])
        self.assertIn('inventory: items', files['crud/diagram.gen.svg'])
        self.assertIn('diagram.gen.svg', files['crud/index.gen.html'])
        self.op['accesses'] = []
        self.op['no_access_reason'] = 'health check'
        with self.assertRaisesRegex(designflow.DesignError, 'unmapped persistence'):
            self.render()

    def test_sql_ast_write_targets_join_cte_and_insert_select(self):
        cases = [
            ('SELECT i.id FROM items i JOIN users u ON i.id=u.id', [('items', 'R'), ('users', 'R')]),
            ('INSERT INTO items SELECT id FROM source', [('items', 'C'), ('source', 'R')]),
            ('UPDATE items SET id=s.id FROM source s WHERE items.id=s.id', [('items', 'U'), ('source', 'R')]),
            ('DELETE FROM items USING source WHERE items.id=source.id', [('items', 'D'), ('source', 'R')]),
            ('WITH x AS (SELECT id FROM items) SELECT * FROM x', [('items', 'R')]),
        ]
        for sql, expected in cases:
            with self.subTest(sql=sql):
                self.assertEqual(structure.sql_accesses(sql), expected)
        for sql in ['MERGE INTO items USING source ON 1=1 WHEN MATCHED THEN DELETE', 'SELECT 1; SELECT 2']:
            with self.assertRaises(ValueError):
                structure.sql_accesses(sql)

    def test_access_must_be_runtime_and_reachable_and_sql_bound(self):
        original = copy.deepcopy(self.op['accesses'][0])
        for changes in [{'phase': 'synth'}, {'source': {'path': 'src/items/router.py', 'line': 1}}, {'sql': '../outside.sql'}]:
            self.op['accesses'][0] = {**original, **changes}
            with self.assertRaises((designflow.DesignError, FileNotFoundError)):
                self.render()
        self.op['accesses'][0] = original
        self.op['unresolved_accesses'] = ['dynamic dispatch']
        with self.assertRaisesRegex(designflow.DesignError, 'unresolved'):
            self.render()

    def test_duplicate_hierarchy_old_outputs_broken_links_and_path_escape(self):
        files = self.render()
        document = json.loads(self.fixture.openapi.read_text())
        for name, content in [('old.detail-design.md', '# old'), ('items/index.gen.md', '# items\n[missing](missing.md)')]:
            modified = {**files, name: content}
            with self.assertRaises(ValueError):
                structure.validate_structure(modified, self.model, document)
        self.op['slug'] = '../escape'
        with self.assertRaisesRegex(designflow.DesignError, 'safe path segment'):
            self.render()

    def test_nested_generate_check_and_old_file_detection(self):
        self.save()
        self.assertEqual(designflow.main(self.fixture.argv), 0)
        before = {p.relative_to(self.fixture.out): p.read_bytes() for p in self.fixture.out.rglob('*') if p.is_file()}
        self.assertEqual(designflow.main([*self.fixture.argv, '--check']), 0)
        self.assertEqual(before, {p.relative_to(self.fixture.out): p.read_bytes() for p in self.fixture.out.rglob('*') if p.is_file()})
        (self.fixture.out / 'old.gen.md').write_text('# old')
        self.assertNotEqual(designflow.main([*self.fixture.argv, '--check']), 0)

    def test_nested_symlink_is_not_followed(self):
        self.save()
        designflow.main(self.fixture.argv)
        document = self.fixture.out / 'items/get-item/query_gen.md'
        document.unlink()
        document.symlink_to(self.fixture.model_path)
        self.assertNotEqual(designflow.main([*self.fixture.argv, '--check']), 0)

    def test_non_sql_and_health_and_api_deletion_share_one_model(self):
        path = self.root / 'src/storage_api.py'
        path.write_text("import storage\ndef upload():\n    return storage.put_object('bucket', 'key')\ndef health():\n    return {'ok': True}\n")
        index = designflow.api_helper('api_layout').Index(self.root, 'src')
        model = {'operations': [
            {'id': 'upload', 'source': {'path': 'src/storage_api.py', 'line': 2}, 'accesses': [
                {'store': 'object', 'phase': 'runtime', 'source': {'path': 'src/storage_api.py', 'line': 3},
                 'symbol': 'storage.put_object', 'action': 'C', 'resource': 'bucket/key', 'adapter': 'fixture-storage-v1'}]},
            {'id': 'health', 'source': {'path': 'src/storage_api.py', 'line': 4}, 'accesses': [], 'no_access_reason': '定数応答のみ'}]}
        data = structure.crud(model, self.root, index)
        self.assertEqual(data['accesses'][0]['action'], 'C')
        self.assertEqual(data['no_access'], [{'operation': 'health', 'reason': '定数応答のみ'}])
        self.assertIn('health,-', structure.render_crud(data)['crud/access.gen.csv'])
        model['operations'].pop(0)
        reduced = structure.render_crud(structure.crud(model, self.root, index))
        self.assertNotIn('upload', reduced['crud/access.gen.csv'])

    def test_sql_change_updates_crud_and_drift(self):
        self.save()
        self.assertEqual(designflow.main(self.fixture.argv), 0)
        sql = self.root / 'src/items/sql/read.sql'
        sql.write_text('SELECT id FROM items JOIN users USING (id)')
        router = self.root / 'src/items/router.py'
        router.write_text(router.read_text().replace('SELECT id FROM items WHERE id = :item_id', sql.read_text()))
        self.save()
        self.assertNotEqual(designflow.main([*self.fixture.argv, '--check']), 0)
        self.assertEqual(designflow.main(self.fixture.argv), 0)
        self.assertIn('inventory:users', (self.fixture.out / 'crud/access.gen.csv').read_text())

    def test_csv_formula_prefixes_are_neutralized(self):
        data = {'operations': ['=1+1'], 'accesses': [{'operation': '=1+1', 'store': '@SUM(1)', 'resource': 'r', 'action': 'R', 'source': {}}], 'no_access': []}
        rows = list(csv.reader(io.StringIO(structure.render_crud(data)['crud/access.gen.csv'])))
        self.assertEqual(rows[1][0], "'=1+1")
        self.assertTrue(rows[0][1].startswith("'@"))

    def test_dynamic_access_without_adapter_diagnostic_cannot_be_no_access(self):
        path = self.root / 'src/dynamic.py'
        path.write_text("import storage\ndef handler(action):\n    return getattr(storage, action)('bucket', 'key')\n")
        index = designflow.api_helper('api_layout').Index(self.root, 'src')
        model = {'operations': [{'id': 'dynamic', 'source': {'path': 'src/dynamic.py', 'line': 2},
                                'accesses': [], 'no_access_reason': 'no persistence'}]}
        with self.assertRaisesRegex(ValueError, 'dynamic access'):
            structure.crud(model, self.root, index)

    def test_message_child_and_factor_deletion_are_rejected(self):
        files = self.render()
        with self.assertRaisesRegex(ValueError, 'detail children'):
            structure.validate_document('messages', files['items/get-item/messages_gen.md'].replace('#### 出力項目', '出力項目'), self.op)
        with self.assertRaisesRegex(ValueError, 'factors'):
            structure.validate_document('unit-test', files['items/get-item/unit-test_gen.md'].replace('### F1 商品有無', '商品有無'), self.op)

    def test_multiple_stores_and_combined_actions(self):
        data = {'operations': ['update'], 'accesses': [
            {'operation': 'update', 'store': store, 'resource': 'items', 'action': action, 'source': {}}
            for store, action in [('db', 'R'), ('db', 'U'), ('object', 'C')]], 'no_access': []}
        files = structure.render_crud(data)
        self.assertIn('update,RU,C', files['crud/access.gen.csv'])
        self.assertIn('A0 -->|RU| R0', files['crud/index.gen.md'])
        self.assertIn('A0 -->|C| R1', files['crud/index.gen.md'])

    def test_independent_adapter_uses_common_structure_and_crud_checks(self):
        self.save()
        self.assertEqual(designflow.main(self.fixture.argv), 0)
        checker = designflow.api_helper('check_design')
        prefix = self.fixture.out.relative_to(self.root).as_posix()
        paths = {kind: prefix + '/' + name for kind, name in structure.names(self.model, self.op).items()}
        surface = {'openapi': self.fixture.openapi.relative_to(self.root).as_posix(), 'operation_documents': {'getItem': paths},
                   'markdown': list(paths.values()), 'structure_root': prefix, 'structure_model': self.fixture.model_path.name}
        checker.api_outputs(self.root, surface)
        csv_path = self.fixture.out / 'crud/access.gen.csv'
        csv_path.write_text(csv_path.read_text().replace(',R', ',U'))
        with self.assertRaisesRegex(ValueError, 'CRUD model/output drift'):
            checker.api_outputs(self.root, surface)

    def test_fresh_cli_process_loads_profile_helpers_for_external_repository(self):
        import subprocess
        import sys
        self.save()
        result = subprocess.run([sys.executable, designflow.__file__, *self.fixture.argv], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_assigned_dynamic_callable_cannot_be_no_access(self):
        path = self.root / 'src/dynamic_assigned.py'
        path.write_text("import storage\ndef handler(action):\n    call = getattr(storage, action)\n    return call('bucket', 'key')\n")
        index = designflow.api_helper('api_layout').Index(self.root, 'src')
        model = {'operations': [{'id': 'dynamic', 'source': {'path': 'src/dynamic_assigned.py', 'line': 2},
                                'accesses': [], 'no_access_reason': 'no persistence'}]}
        with self.assertRaisesRegex(ValueError, 'dynamic callable'):
            structure.crud(model, self.root, index)

    def test_unknown_service_call_requires_explicit_adapter_disposition(self):
        path = self.root / 'src/unknown_service.py'
        path.write_text("import service\ndef handler():\n    return service.perform()\n")
        index = designflow.api_helper('api_layout').Index(self.root, 'src')
        op = {'id': 'unknown', 'source': {'path': 'src/unknown_service.py', 'line': 2},
              'accesses': [], 'no_access_reason': 'adapter confirms pure computation'}
        with self.assertRaisesRegex(ValueError, 'adapter disposition'):
            structure.crud({'operations': [op]}, self.root, index)
        op['non_access_calls'] = [{'source': {'path': 'src/unknown_service.py', 'line': 3}, 'symbol': 'service.perform',
                                  'reason': '計算だけを行うサービス関数', 'adapter': 'fixture-service-v1'}]
        self.assertEqual(structure.crud({'operations': [op]}, self.root, index)['no_access'][0]['operation'], 'unknown')
