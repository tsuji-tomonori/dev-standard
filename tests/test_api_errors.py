"""例外HTTP・運用catalog・安全な型付きcontextと日本語GWTの実接続を検証する。"""
import copy
import tempfile
import unittest
from pathlib import Path

from test_api_documents import designflow

layout = designflow.api_helper('api_layout')


class ErrorsTest(unittest.TestCase):
    def setUp(self):
        self.errors = designflow.api_helper('api_errors')
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.src = self.root / 'src'
        self.src.mkdir()
        (self.src / 'types_.py').write_text('class Failure(Exception): pass\nclass Context:\n    stage: str\n')
        self.catalog = self.src / 'catalog.py'
        self.entry = {'id': 'MODEL_FAILURE', 'exception': 'types_.Failure', 'status': 200, 'code': 'model_failed',
                      'message': 'モデル処理に失敗しました。', 'level': 'ERROR', 'operator_action': '依存先の状態を確認し再試行する。', 'context_type': 'types_.Context'}
        self.catalog.write_text('MODEL_FAILURE = '+repr(self.entry)+'\n')
        self.router = self.src / 'router.py'
        self.router.write_text('import provider\nimport ops_logger\nimport catalog\nfrom types_ import Failure, Context\ndef handle():\n    try:\n        return provider.run()\n    except Failure:\n        ops_logger.error(catalog.MODEL_FAILURE, context_model=Context(stage="model"))\n        return 200, {"code":"model_failed", "message":"モデル処理に失敗しました。"}\n')
        self.config = {'handler': 'router.handle', 'logger': 'ops_logger.error', 'rules': [{
            'source': {'path': 'src/router.py', 'line': 8}, 'log': {'path': 'src/router.py', 'line': 9},
            'response': {'path': 'src/router.py', 'line': 10}}]}
    def check(self):
        return self.errors.inspect(layout.Index(self.root, 'src'), self.config)
    def test_internal_failure_keeps_real_success_status(self):
        result = self.check()[0]
        self.assertEqual((result['status'], result['code'], result['outcome']), (200, 'model_failed', 'handled'))
        self.assertEqual(result['operator_action'], self.entry['operator_action'])
        self.router.write_text(self.router.read_text().replace('return 200,', 'return 201,'))
        self.entry['status'] = 201
        self.catalog.write_text('MODEL_FAILURE = '+repr(self.entry)+'\n')
        self.assertEqual(self.check()[0]['status'], 201)
    def test_missing_catalog_exception_response_and_log_mappings_fail(self):
        original = copy.deepcopy(self.entry)
        for change in [{'status': 500}, {'exception': 'ValueError'}, {'operator_action': ''}, {'context_type': 'unknown.Context'}]:
            self.entry = {**original, **change}
            self.catalog.write_text('MODEL_FAILURE = '+repr(self.entry)+'\n')
            with self.assertRaises(ValueError):
                self.check()
        self.entry = original
        self.catalog.write_text('MODEL_FAILURE = '+repr(original)+'\n')
        self.config['rules'] = []
        with self.assertRaisesRegex(ValueError, 'mapping'):
            self.check()
    def test_dynamic_http_and_secret_log_context_are_rejected(self):
        original = self.router.read_text()
        for changed in [original.replace('return 200,', 'return status,'),
                        original.replace('stage="model"', 'stage=str(secret_exception)'),
                        original.replace('stage="model"', 'stage=42'),
                        original.replace('context_model=Context(stage="model")', 'context_model=Context(stage="model"), exc_info=True')]:
            self.router.write_text(changed)
            with self.assertRaises(ValueError) as caught:
                self.check()
            self.assertNotIn('secret_exception', str(caught.exception))
        self.router.write_text(original)
    def test_conditional_catch_cannot_hide_an_unmapped_outcome(self):
        self.router.write_text(self.router.read_text().replace('        return 200,', '        if uncertain:\n            return 200,'))
        self.config['rules'][0]['response']['line'] = 11
        with self.assertRaisesRegex(ValueError, 'conditional'):
            self.check()
    def test_hidden_catch_branch_unknown_response_and_raw_exception_sink_fail(self):
        original = self.router.read_text()
        self.router.write_text(original.replace('        ops_logger.error', '        if uncertain:\n            return 500, {"code":"other", "message":"unsafe"}\n        ops_logger.error'))
        self.config['rules'][0]['log']['line'] = 11
        self.config['rules'][0]['response']['line'] = 12
        with self.assertRaisesRegex(ValueError, 'conditional'):
            self.check()
        self.config['rules'][0]['log']['line'] = 9
        self.config['rules'][0]['response']['line'] = 10
        self.router.write_text(original.replace('return 200, {"code":"model_failed", "message":"モデル処理に失敗しました。"}',
                                               'return unrelated(status=200, code="model_failed", message="モデル処理に失敗しました。")'))
        with self.assertRaisesRegex(ValueError, 'constructor'):
            self.check()
        self.router.write_text(original.replace('except Failure:', 'except Failure as exc:').replace('        ops_logger.error', '        print(str(exc))\n        ops_logger.error'))
        self.config['rules'][0]['log']['line'] = 10
        self.config['rules'][0]['response']['line'] = 11
        with self.assertRaisesRegex(ValueError, 'raw caught exception'):
            self.check()

    def test_continued_worker_does_not_invent_http_500(self):
        self.router.write_text('import provider\nimport ops_logger\nimport catalog\nfrom types_ import Failure, Context\ndef handle():\n    for job in [1]:\n        try:\n            provider.run()\n        except Failure:\n            ops_logger.error(catalog.MODEL_FAILURE, context_model=Context(stage="model"))\n            continue\n')
        self.entry['status'] = None
        self.catalog.write_text('MODEL_FAILURE = '+repr(self.entry)+'\n')
        self.config['rules'][0] = {'source': {'path': 'src/router.py', 'line': 9}, 'log': {'path': 'src/router.py', 'line': 10}, 'response': {'path': 'src/router.py', 'line': 11}}
        self.assertEqual(self.check()[0]['outcome'], 'continue')
    def test_real_catch_returns_safe_result_and_typed_logger_rejects_wrong_context(self):
        import sys
        import types
        from dataclasses import make_dataclass
        from unittest.mock import patch
        type_module = types.ModuleType('types_')
        type_module.Failure = type('Failure', (Exception,), {})
        type_module.Context = make_dataclass('Context', [('stage', str)])
        catalog_module = types.ModuleType('catalog')
        catalog_module.MODEL_FAILURE = self.entry
        records = []
        def log(catalog, *, context_model):
            if type(context_model) is not type_module.Context or type(context_model.stage) is not str:
                raise TypeError('invalid context')
            records.append((catalog['id'], catalog['level'], catalog['message'], context_model.stage))
        def fail():
            raise type_module.Failure('secret-body jwt-sensitive-value')
        modules = {'types_': type_module, 'catalog': catalog_module,
                   'ops_logger': types.SimpleNamespace(error=log), 'provider': types.SimpleNamespace(run=fail)}
        with patch.dict(sys.modules, modules):
            namespace = {}
            exec(self.router.read_text(), namespace)
            status, body = namespace['handle']()
        self.assertEqual(status, 200)
        self.assertEqual(body['code'], self.entry['code'])
        self.assertEqual(records[0][:3], (self.entry['id'], self.entry['level'], body['message']))
        self.assertNotIn('jwt-sensitive-value', repr(records) + repr(body))
        with self.assertRaises(TypeError):
            log(self.entry, context_model=object())
        with self.assertRaises(TypeError):
            log(self.entry, context_model=type_module.Context(stage=42))

    def test_raise_and_reraise_bind_to_actual_registered_http_handler(self):
        boundary = self.src / 'http.py'
        boundary.write_text('import ops_logger\nimport catalog\nfrom types_ import Failure, Context\n@app.exception_handler(Failure)\ndef failure_handler():\n    ops_logger.error(catalog.MODEL_FAILURE, context_model=Context(stage="model"))\n    return 200, {"code":"model_failed", "message":"モデル処理に失敗しました。"}\n')
        self.config['http_handlers'] = ['http.failure_handler']
        self.router.write_text('from types_ import Failure\ndef handle():\n    raise Failure()\n')
        self.config['rules'] = [{'source': {'path': 'src/router.py', 'line': 3},
                                'log': {'path': 'src/http.py', 'line': 6},
                                'response': {'path': 'src/http.py', 'line': 7}}]
        self.assertEqual(self.check()[0]['outcome'], 'reraised-to-http')
        self.router.write_text('import provider\nfrom types_ import Failure\ndef handle():\n    try:\n        provider.run()\n    except Failure:\n        raise\n')
        self.config['rules'][0]['source']['line'] = 6
        self.assertEqual(self.check()[0]['outcome'], 'reraised-to-http')
        boundary.write_text(boundary.read_text().replace('exception_handler(Failure)', 'exception_handler(ValueError)'))
        with self.assertRaisesRegex(ValueError, 'type mismatch'):
            self.check()

    def test_japanese_gwt_comes_from_actual_test_and_rejects_missing_duplicate(self):
        test = self.root / 'test_app.py'
        text = 'def test_failure():\n    """Given: モデルが失敗する。\n    When: 回答を要求する。\n    Then: 安全な失敗結果を返す。\n    """\n    assert 1 == 1\n'
        test.write_text(text)
        self.assertEqual(self.errors.gwt(self.root, 'test_app.py::test_failure', layout.confined)['given'], 'モデルが失敗する。')
        for changed in [text.replace('Given:', 'Setup:'), text.replace('When:', 'Given:'), text.replace('モデルが失敗する。', 'fixture_name')]:
            test.write_text(changed)
            with self.assertRaises(ValueError):
                self.errors.gwt(self.root, 'test_app.py::test_failure', layout.confined)


def enrich_documents(test):
    """既存の実SQL fixtureへ型付き例外経路と実テストの説明を接続する。"""
    import ast
    router = test.fixture.source / 'items/router.py'
    original = router.read_text()
    header = ('import ops_logger\nfrom builtins import RuntimeError\n'
              'class Context:\n    stage: str\n'
              'MODEL_FAILURE = '+repr({'id': 'MODEL_FAILURE', 'exception': 'builtins.RuntimeError', 'status': 200,
              'code': 'model_failed', 'message': 'モデル処理に失敗しました。', 'level': 'ERROR',
              'operator_action': '依存先の状態を確認し再試行する。', 'context_type': 'items.router.Context'})+'\n')
    original = original.replace("    row = connection.execute('SELECT id FROM items WHERE id = :item_id', {'item_id': item_id}).fetchone()",
        "    try:\n        row = connection.execute('SELECT id FROM items WHERE id = :item_id', {'item_id': item_id}).fetchone()\n"
        "    except RuntimeError:\n        ops_logger.error(MODEL_FAILURE, context_model=Context(stage='model'))\n"
        "        return 200, {'code':'model_failed', 'message':'モデル処理に失敗しました。'}")
    router.write_text(header + original)
    tree = ast.parse(router.read_text())
    handler = next(n for n in tree.body if isinstance(n, ast.FunctionDef))
    catch = next(n for n in ast.walk(handler) if isinstance(n, ast.ExceptHandler))
    execute = next(n for n in ast.walk(handler) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == 'execute')
    test.op['source'] = {'path': 'src/items/router.py', 'line': handler.lineno}
    test.op['accesses'][0]['source']['line'] = execute.lineno
    test.op['non_access_calls'] = [{'symbol': 'ops_logger.error', 'adapter': 'fixture-log-contract',
                                  'reason': '型付きcatalogのログ出力のみ。業務データの永続化なし。',
                                  'source': {'path': 'src/items/router.py', 'line': catch.body[0].lineno}}]
    test.model['error_contract'] = {'operations': {'getItem': {'handler': 'items.router.get_item', 'logger': 'ops_logger.error',
        'rules': [{'source': {'path': 'src/items/router.py', 'line': catch.lineno},
                   'log': {'path': 'src/items/router.py', 'line': catch.body[0].lineno},
                   'response': {'path': 'src/items/router.py', 'line': catch.body[-1].lineno}}]}}}
    path = test.fixture.test_root / 'test_items.py'
    text = path.read_text()
    for name, given, then in [('test_get_item', '商品Aが登録されている。', '商品Aを取得できる。'),
                              ('test_missing_item', '商品Aが存在しない。', '商品なしの応答を返す。')]:
        text = text.replace(f'def {name}():\n', f'def {name}():\n    """Given: {given}\n    When: 商品Aを要求する。\n    Then: {then}\n    """\n')
    path.write_text(text)
    test.save()


class ErrorDocumentsTest(unittest.TestCase):
    def test_generated_documents_use_catch_response_catalog_and_source_gwt(self):
        from test_api_structure import ApiStructureTest
        fixture = ApiStructureTest()
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        self.addCleanup(fixture.fixture.doCleanups)
        enrich_documents(fixture)
        files = fixture.render()
        self.assertIn('モデル処理に失敗しました。', files['items/get-item/messages_gen.html'])
        self.assertIn('依存先の状態を確認し再試行する。', files['items/get-item/sequence_gen.html'])
        self.assertIn('商品Aが登録されている。', files['items/get-item/unit-test_gen.html'])
        import json
        checker = designflow.api_helper('check_design')
        structure = designflow.api_helper('api_structure')
        output = fixture.root / 'rendered'
        for name, content in files.items():
            path = output / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        surface = {'structure_model': 'api-model.json', 'structure_root': 'rendered', 'operation_documents': {'getItem': {
            kind: 'rendered/' + name for kind, name in structure.names(fixture.model, fixture.op).items()}}}
        document = json.loads(fixture.fixture.openapi.read_text())
        checker.check_structure(fixture.root, surface, document)
        path = output / 'items/get-item/messages_gen.md'
        path.write_text(path.read_text().replace('依存先の状態を確認し再試行する。', '確認不要'))
        with self.assertRaisesRegex(ValueError, 'semantic document/output drift'):
            checker.check_structure(fixture.root, surface, document)
