"""実フローの順序とquery専用型の意味を負例で検証する。"""
import tempfile
import unittest
from pathlib import Path

from test_api_documents import designflow

flow = designflow.api_helper('api_flow')
layout = designflow.api_helper('api_layout')
sql_models = designflow.api_helper('sql_models')


class FlowTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.src = self.root / 'src'
        self.src.mkdir()
        (self.src / 'steps.py').write_text('import db\ndef load():\n    return db.read()\ndef build(row):\n    return row\n')
        self.router = self.src / 'router.py'
        self.router.write_text('import steps\nimport tx\ndef handle():\n    row = steps.load()\n    if row:\n        tx.commit()\n    else:\n        tx.rollback()\n    return steps.build(row)\n')
        self.config = {'handler': 'router.handle', 'steps': ['steps.load', 'steps.build'],
                       'ports': ['db.read'], 'transactions': ['tx.commit', 'tx.rollback']}
    def inspect(self):
        return flow.inspect(layout.Index(self.root, 'src'), self.config)
    def test_order_branch_and_transaction_change_diagram(self):
        original = flow.mermaid(self.inspect())
        self.assertLess(original.index('steps.load'), original.index('tx.commit'))
        self.assertIn('alt row', original)
        self.router.write_text(self.router.read_text().replace('if row:', 'if row is None:').replace('tx.commit()', 'tx.rollback()'))
        updated = flow.mermaid(self.inspect())
        self.assertNotEqual(original, updated)
        self.assertNotIn('tx.commit', updated)
    def test_flow_reversal_direct_port_and_unknown_fail(self):
        original = self.router.read_text()
        for text, message in [(original.replace('steps.load()', 'db.read()'), 'unresolved|direct'),
                              (original.replace('steps.load()', 'mystery()'), 'unresolved'),
                              (original.replace('steps.load()', 'getattr(steps, "load")()'), 'dynamic')]:
            self.router.write_text(text)
            with self.assertRaisesRegex(ValueError, message):
                self.inspect()
        self.router.write_text(original)
        step = self.src / 'steps.py'
        step.write_text('import db\ndef load():\n    row=db.read()\n    return build(row)\ndef build(row):\n    return row\n')
        with self.assertRaisesRegex(ValueError, 'whole flow'):
            self.inspect()
    def test_loop_catch_finally_and_argument_evaluation(self):
        self.router.write_text('import steps\nimport tx\ndef handle():\n    try:\n        for item in [1,2]:\n            steps.build(steps.load())\n    except RuntimeError:\n        tx.rollback()\n    finally:\n        tx.commit()\n')
        result = flow.mermaid(self.inspect())
        self.assertIn('loop item', result)
        self.assertIn('catch RuntimeError', result)
        self.assertIn('finally', result)
        self.assertLess(result.index('steps.load'), result.index('steps.build'))
    def test_step_transaction_and_multiple_effects_fail(self):
        step = self.src / 'steps.py'
        for body in ['import tx\ndef load():\n    tx.commit()\n', 'import db\ndef load():\n    db.read()\n    return db.read()\n']:
            step.write_text(body+'def build(row):\n    return row\n')
            with self.assertRaisesRegex(ValueError, 'transaction|multiple effects'):
                self.inspect()
    def test_sql_comment_and_unreachable_mapping(self):
        self.config['sql_calls'] = {'db.read': 'src/read.sql'}
        (self.src / 'read.sql').write_text('-- 商品を取得する。\nSELECT id FROM items')
        self.assertIn('商品を取得する。', flow.mermaid(self.inspect()))
        (self.src / 'read.sql').write_text('SELECT id FROM items')
        with self.assertRaisesRegex(ValueError, 'Japanese'):
            self.inspect()
    def test_unreachable_steps_and_repeated_helper_effects_fail(self):
        original = self.router.read_text()
        self.router.write_text('import steps\ndef handle():\n    return None\n    steps.load()\n    steps.build(None)\n')
        with self.assertRaisesRegex(ValueError, 'unused'):
            self.inspect()
        for body in ['if flag:\n        return None\n    else:\n        return None',
                     'with tx.commit():\n        return None',
                     'try:\n        pass\n    finally:\n        return None']:
            self.router.write_text('import steps\nimport tx\ndef handle():\n    '+body+'\n    steps.load()\n    steps.build(None)\n')
            with self.assertRaisesRegex(ValueError, 'unused'):
                self.inspect()
        self.router.write_text(original)
        (self.src / 'steps.py').write_text('import db\ndef helper(): return db.read()\ndef load():\n    helper()\n    return helper()\ndef build(row): return row\n')
        with self.assertRaisesRegex(ValueError, 'multiple effects'):
            self.inspect()

    def test_internal_code_cannot_be_hidden_as_pure(self):
        self.config['pure_calls'] = ['steps.load']
        with self.assertRaisesRegex(ValueError, 'overlapping|opaque'):
            self.inspect()


class SqlModelsTest(unittest.TestCase):
    ddl = 'CREATE TABLE items (id INTEGER PRIMARY KEY, title TEXT NOT NULL, note TEXT)'
    query = 'SELECT id, note AS comment FROM items WHERE id = :item_id'
    def test_exact_projection_bound_params_and_strict_runtime_types(self):
        generated = sql_models.generate(self.ddl, {'read': self.query})
        scope = {}
        exec(generated, scope)
        Params, Row = scope['ReadParams'], scope['ReadRow']
        self.assertEqual(Params(item_id=1).item_id, 1)
        self.assertEqual(Row(id=1, comment=None).comment, None)
        for kwargs in [{'item_id': '1'}, {'item_id': True}, {'item_id': None}, {'item_id': 1, 'title': 'extra'}]:
            with self.assertRaises(TypeError):
                Params(**kwargs)
        with self.assertRaises(TypeError):
            Row(id=None, comment='x')
        with self.assertRaises(TypeError):
            Row(id=1, title='not projected', comment='x')
        self.assertEqual(generated, sql_models.generate(self.ddl, {'read': self.query}))
    def test_insert_update_bind_only_actual_arguments(self):
        for query in ['INSERT INTO items (id,title) VALUES (:key,:name)', 'UPDATE items SET title=:name WHERE id=:key']:
            actual = sql_models.project(self.ddl, query)
            self.assertEqual(actual['params'], {'key': ('int', False), 'name': ('str', False)})
            self.assertEqual(actual['row'], {})
    def test_unknown_projection_join_types_and_conflicting_bind_fail(self):
        for query in ['SELECT * FROM items', 'SELECT id+1 FROM items', 'SELECT id FROM items JOIN other ON 1=1',
                      'SELECT id FROM items WHERE id=:x AND title=:x', 'SELECT id FROM items WHERE id=:x LIMIT :n']:
            with self.subTest(query=query), self.assertRaises(ValueError):
                sql_models.project(self.ddl, query)
        with self.assertRaises(ValueError):
            sql_models.project('CREATE TABLE items(id JSON)', 'SELECT id FROM items')
    def test_qualified_ddl_is_not_an_unqualified_table(self):
        with self.assertRaisesRegex(ValueError, 'qualified DDL'):
            sql_models.project('CREATE TABLE private.items(id TEXT NOT NULL)', 'SELECT id FROM items')

    def test_missing_hand_edited_sql_and_ddl_drift(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'ddl.sql').write_text(self.ddl)
            (root / 'read.sql').write_text(self.query)
            expected = sql_models.generate(self.ddl, {'read': self.query})
            (root / 'models.py').write_text(expected)
            config = {'ddl': 'ddl.sql', 'queries': {'read': 'read.sql'}, 'output': 'models.py'}
            sql_models.inspect(root, config, layout.confined)
            for file, text in [('models.py', expected+'# edited\n'), ('read.sql', 'SELECT id FROM items WHERE id=:item_id'),
                               ('ddl.sql', self.ddl.replace('note TEXT', 'note TEXT NOT NULL'))]:
                path = root / file
                original = path.read_text()
                path.write_text(text)
                with self.assertRaisesRegex(ValueError, 'drift'):
                    sql_models.inspect(root, config, layout.confined)
                path.write_text(original)
            (root / 'models.py').unlink()
            with self.assertRaisesRegex(ValueError, 'missing'):
                sql_models.inspect(root, config, layout.confined)
