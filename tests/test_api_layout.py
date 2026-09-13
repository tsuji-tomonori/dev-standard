"""選択profileで空ファイル・未接続・所有境界違反を検出する。"""
from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from test_api_documents import designflow

layout = designflow.api_helper('api_layout')


class ApiLayoutTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.package = 'src/ops/items/read'
        self.folder = self.root / self.package
        self.write('router.py', "from fastapi import APIRouter\nfrom . import functions, schemas, response_builders, contract, samples\nrouter = APIRouter()\n"
                   "@router.get('/items', operation_id=contract.CONTRACT['operation_id'], response_model=schemas.Item, responses=samples.SAMPLES)\n"
                   "def get_item():\n    return response_builders.build(functions.load())\n")
        self.write('functions.py', 'from .generated import queries\ndef load():\n    return queries.read()\n')
        self.write('response_builders.py', 'from .schemas import Item\ndef build(row):\n    return Item(id=row["id"])\n')
        self.write('schemas.py', 'class Item:\n    id: str\n')
        self.write('contract.py', "CONTRACT = {'operation_id': 'getItem', 'method': 'GET', 'path': '/items'}\n")
        self.write('samples.py', "SAMPLES = {'200': {'description': '商品を取得'}}\n")
        self.write('sql/read.sql', '-- 商品を取得する。\nSELECT id FROM items;\n')
        self.write('generated/queries.py', "import db\ndef read():\n    return db.execute('src/ops/items/read/sql/read.sql')\n")
        self.document = {'paths': {'/items': {'get': {'operationId': 'getItem', 'responses': {'200': {'description': 'ok'}}}}}}
        self.config = {'profile': 'lazunex-v1', 'python_root': 'src', 'operations': {'getItem': {
            'package': self.package, 'handler': 'get_item', 'queries': {f'{self.package}/sql/read.sql': {'function': 'read'}}}}, 'shared': {}}

    def write(self, name, content):
        path = self.folder / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path

    def check(self):
        return layout.inspect(self.root, self.config, self.document)

    def test_connected_operation_and_local_reexport(self):
        result = self.check()
        self.assertEqual(result['operations'][0]['operation'], 'getItem')
        self.write('builders.py', 'from .response_builders import build\n')
        router = self.folder / 'router.py'
        router.write_text(router.read_text().replace('response_builders,', 'builders,').replace('response_builders.build', 'builders.build'))
        self.check()

    def test_empty_required_file(self):
        for role in layout.ROLES:
            path = self.folder / role
            before = path.read_text()
            for content in ['# 役割だけの空file\n', 'pass\n', '"""説明のみ"""\n']:
                self.write(role, content)
                with self.subTest(role=role), self.assertRaisesRegex(ValueError, 'empty responsibility'):
                    self.check()
            path.write_text(before)

    def test_unused_contract_samples_builder_and_comment_decoys(self):
        path = self.folder / 'router.py'
        original = path.read_text()
        changes = [("contract.CONTRACT['operation_id']", "'getItem'"), ('responses=samples.SAMPLES', 'responses={}'),
                   ('return response_builders.build(functions.load())', 'return functions.load()\n    # response_builders.build()')]
        for old, new in changes:
            path.write_text(original.replace(old, new))
            with self.subTest(old=old), self.assertRaisesRegex(ValueError, 'unconnected'):
                self.check()
        path.write_text(original)

    def test_nested_uncalled_builder_is_not_connected(self):
        path = self.folder / 'router.py'
        path.write_text(path.read_text().replace('    return response_builders.build(functions.load())',
                       '    def unused():\n        return response_builders.build(functions.load())\n    return functions.load()'))
        with self.assertRaisesRegex(ValueError, 'unconnected callable'):
            self.check()

    def test_aggregated_operations_global_queries_and_orphan_sql(self):
        self.config['operations']['another'] = copy.deepcopy(self.config['operations']['getItem'])
        self.document['paths']['/another'] = {'get': {'operationId': 'another'}}
        with self.assertRaisesRegex(ValueError, 'multiple operations'):
            self.check()
        del self.config['operations']['another']
        del self.document['paths']['/another']
        extra = self.root / 'src/generated/queries.py'
        extra.parent.mkdir()
        extra.write_text('def query(): return 1\n')
        with self.assertRaisesRegex(ValueError, 'global generated'):
            self.check()
        extra.unlink()
        self.write('sql/orphan.sql', 'SELECT 1;')
        with self.assertRaisesRegex(ValueError, 'SQL inventory'):
            self.check()

    def test_contract_mismatch_and_query_reference_or_symbol_collision(self):
        self.write('contract.py', "CONTRACT = {'operation_id':'getItem','method':'POST','path':'/items'}\n")
        with self.assertRaisesRegex(ValueError, 'contract mismatch'):
            self.check()
        self.write('contract.py', "CONTRACT = {'operation_id':'getItem','method':'GET','path':'/items'}\n")
        self.write('generated/queries.py', "import db\ndef read(): return db.execute('foreign/sql/read.sql')\n")
        with self.assertRaisesRegex(ValueError, 'owned SQL reference'):
            self.check()

    def test_shared_module_must_have_explicit_owner(self):
        self.write('functions.py', 'from common import load\n')
        (self.root / 'src/common.py').write_text('def load(): return 1\n')
        with self.assertRaisesRegex(ValueError, 'undeclared shared ownership'):
            self.check()

    def test_source_symlink_and_dynamic_route_are_rejected(self):
        path = self.folder / 'router.py'
        path.write_text(path.read_text().replace("'/items'", "compute_path()"))
        with self.assertRaisesRegex(ValueError, 'unsupported static metadata'):
            self.check()
        path.unlink()
        path.symlink_to(self.folder / 'functions.py')
        with self.assertRaisesRegex(ValueError, 'symlink'):
            self.check()

    def test_cli_reads_config_without_importing_target(self):
        (self.root / 'config.json').write_text(json.dumps(self.config))
        self.assertEqual(self.check()['profile'], 'lazunex-v1')

    def test_parameter_and_module_rebindings_are_not_real_connections(self):
        path = self.folder / 'router.py'
        original = path.read_text()
        for altered in [original.replace('def get_item():', 'def get_item(functions, response_builders):'),
                        original.replace('router = APIRouter()', 'router = APIRouter()\nfunctions = object()')]:
            path.write_text(altered)
            with self.assertRaisesRegex(ValueError, 'reassignment'):
                self.check()
        path.write_text(original)

    def test_empty_business_function_is_not_implementation(self):
        self.write('functions.py', 'from .generated import queries\ndef load():\n    pass\n')
        with self.assertRaisesRegex(ValueError, 'empty callable|not reachable'):
            self.check()

    def test_cross_operation_import_and_shared_back_dependency(self):
        other = self.root / 'src/ops/items/write'
        other.mkdir()
        (other / 'functions.py').write_text('def write(): return 1\n')
        # owner集合へ追加し、直接依存を実際に解決する。
        self.config['operations']['writeItem'] = {'package': 'src/ops/items/write', 'handler': 'write_item'}
        self.document['paths']['/write'] = {'post': {'operationId': 'writeItem'}}
        self.write('functions.py', 'from ..write.functions import write\ndef load(): return write()\n')
        with self.assertRaisesRegex(ValueError, 'API-to-API'):
            self.check()
        self.write('functions.py', 'from shared.auth import authorize\ndef load(): return authorize()\n')
        shared = self.root / 'src/shared'
        shared.mkdir()
        (shared / 'auth.py').write_text('from ops.items.write.functions import write\ndef authorize(): return write()\n')
        self.config['shared'] = {'src/shared': '認可判定'}
        with self.assertRaisesRegex(ValueError, 'API-to-API|back dependency'):
            self.check()

    def test_query_symbol_collision_and_literal_decoy(self):
        self.write('sql/other.sql', 'SELECT id FROM other;')
        self.config['operations']['getItem']['queries'][f'{self.package}/sql/other.sql'] = {'function': 'read'}
        self.write('generated/queries.py', "import db\ndef read():\n    return db.execute('src/ops/items/read/sql/read.sql', 'src/ops/items/read/sql/other.sql')\n")
        with self.assertRaisesRegex(ValueError, 'overwrite one generated symbol'):
            self.check()

    def test_tuple_nested_definition_and_local_import_shadowing(self):
        path = self.folder / 'router.py'
        original = path.read_text()
        for changed in [original.replace('router = APIRouter()', 'router = APIRouter()\nfunctions, response_builders = object(), object()'),
                        original.replace('def get_item():', 'def get_item():\n    def functions(): pass'),
                        original.replace('def get_item():', 'def get_item():\n    import foreign as functions')]:
            path.write_text(changed)
            with self.assertRaisesRegex(ValueError, 'reassignment'):
                self.check()
        path.write_text(original)

    def test_sql_path_print_decoy_does_not_bind_actual_query(self):
        self.write('generated/queries.py', "import db\ndef read():\n    print('src/ops/items/read/sql/read.sql')\n    return db.execute('foreign/sql/read.sql')\n")
        with self.assertRaisesRegex(ValueError, 'owned SQL reference'):
            self.check()

    def test_identical_sql_basenames_in_distinct_owners_are_preserved(self):
        import shutil
        other = 'src/ops/items/read_other'
        shutil.copytree(self.folder, self.root / other)
        for path in (self.root / other).rglob('*.py'):
            path.write_text(path.read_text().replace(self.package, other).replace("'/items'", "'/other'").replace("'getItem'", "'getOther'"))
        self.config['operations']['getOther'] = {'package': other, 'handler': 'get_item', 'queries': {other + '/sql/read.sql': {'function': 'read'}}}
        self.document['paths']['/other'] = {'get': {'operationId': 'getOther'}}
        result = self.check()
        self.assertEqual(len({op['queries'][0] for op in result['operations']}), 2)

    def test_empty_sample_container_and_schema_class_are_placeholders(self):
        self.write('samples.py', 'SAMPLES = {}\n')
        with self.assertRaisesRegex(ValueError, 'empty or unsupported samples'):
            self.check()
        self.write('samples.py', "SAMPLES = {'200': {'description': '商品を取得'}}\n")
        self.write('schemas.py', 'class Item:\n    pass\n')
        with self.assertRaisesRegex(ValueError, 'empty or unsupported schemas'):
            self.check()
