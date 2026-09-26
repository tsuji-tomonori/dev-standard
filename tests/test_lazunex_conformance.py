"""参照元保持・個別受入条件・新規意味検査・CRUD行列の回帰契約。"""
from __future__ import annotations

import copy
import importlib.util
import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

import test_design_adoption as legacy

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / '.agents/skills/generate-implementation-design/scripts'
ASSETS = SCRIPTS.parent / 'assets'


def load(name):
    spec = importlib.util.spec_from_file_location('test_' + name, SCRIPTS / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MATRIX = load('crud_matrix')
CONFORMANCE = load('conformance')
INVENTORY = load('reference_inventory')


def crud_model():
    return {'schema_version': 2, 'operations': ['write', 'health', 'read'],
            'resources': [{'id': 'db.items', 'group': 'DB', 'kind': 'database'},
                          {'id': 'db.unused', 'group': 'DB', 'kind': 'database'},
                          {'id': 'identity.client', 'group': 'Identity', 'kind': 'external'}],
            'rows': [
                {'operation': 'read', 'resource': 'db.items', 'access': ['R'],
                 'evidence': [{'path': 'source.txt', 'line': 1, 'role': 'read'}]},
                {'operation': 'write', 'resource': 'db.items', 'access': ['U', 'C', 'R', 'D'],
                 'evidence': [{'path': 'source.txt', 'line': 2, 'role': 'write'},
                              {'path': 'source.txt', 'line': 1, 'role': 'read'}]},
                {'operation': 'write', 'resource': 'identity.client', 'access': ['C'],
                 'evidence': [{'path': 'source.txt', 'line': 3, 'role': 'write'}]}],
            'no_access': {'health': '依存先へアクセスしない。'}, 'unresolved': []}


class CrudMatrixTest(unittest.TestCase):
    def test_pivot_keeps_unused_columns_all_operations_and_crud_order(self):
        rendered = MATRIX.renderings(crud_model())
        self.assertEqual(rendered['csv'].decode(), 'api,db.items,db.unused,identity.client\nhealth,,,\nread,R,,\nwrite,CRUD,,C\n')
        self.assertIn('| health |  |  |  |', rendered['table'].decode())

    def test_each_store_has_its_own_matrix_including_no_access(self):
        groups = MATRIX.groups(crud_model())
        self.assertEqual(set(groups), {'DB', 'Identity'})
        self.assertEqual(groups['Identity']['csv'].decode(), 'api,identity.client\nhealth,\nread,\nwrite,C\n')

    def test_diagram_has_shared_nodes_read_direction_and_no_fake_none_resource(self):
        diagram = MATRIX.renderings(crud_model())['diagram'].decode()
        self.assertTrue(diagram.startswith('```mermaid\nflowchart LR'))
        self.assertEqual(diagram.count('a2["write"]'), 1)
        self.assertEqual(diagram.count('r0["db.items"]'), 1)
        self.assertIn('r0 -->|R| a1', diagram)
        self.assertIn('a2 -->|CUD| r0', diagram)
        self.assertNotIn('NONE', diagram)
        self.assertNotIn('a0 -->', diagram)
        self.assertIn('ER関係を表す図ではない', diagram)

    def test_input_set_order_does_not_change_any_rendering(self):
        model = crud_model()
        original = MATRIX.renderings(model)
        for key in ('operations', 'resources', 'rows'):
            model[key].reverse()
        for row in model['rows']:
            row['access'].reverse()
            row['evidence'].reverse()
        self.assertEqual(original, MATRIX.renderings(model))

    def test_unknown_duplicate_missing_and_unresolved_are_rejected(self):
        mutations = [
            lambda m: m['resources'].append(copy.deepcopy(m['resources'][0])),
            lambda m: m['rows'].append(copy.deepcopy(m['rows'][0])),
            lambda m: m['rows'][0].update(resource='missing'),
            lambda m: m['rows'][0].update(operation='missing'),
            lambda m: m['rows'][0].update(access=['NONE']),
            lambda m: m['rows'][0].update(evidence=[]),
            lambda m: m['rows'][0]['evidence'][0].update(role='write'),
            lambda m: m['rows'][0]['evidence'][0].update(line=0),
            lambda m: m['rows'][0]['evidence'][0].update(line=True),
            lambda m: m['no_access'].update(read='未解析をno-accessへ偽装'),
            lambda m: m['no_access'].clear(),
            lambda m: m['unresolved'].append({'path': 'dynamic', 'reason': 'unknown call'}),
            lambda m: m['resources'][0].update(kind='queue-unknown'),
            lambda m: m['resources'][2].update(group='DB'),
        ]
        for index, mutation in enumerate(mutations):
            with self.subTest(index=index):
                model = crud_model()
                mutation(model)
                with self.assertRaises(ValueError):
                    MATRIX.renderings(model)

    def test_csv_markdown_and_mermaid_escape_labels(self):
        model = {'schema_version': 2, 'operations': ['op,"<x>|\n'], 'resources': [], 'rows': [],
                 'no_access': {'op,"<x>|\n': '理由'}, 'unresolved': []}
        rendered = MATRIX.renderings(model)
        self.assertIn('&lt;x&gt;&#124;', rendered['table'].decode())
        self.assertIn('&quot;', rendered['diagram'].decode())
        self.assertIn('"op,""<x>|\n"', rendered['csv'].decode())


class ReferenceConformanceTest(unittest.TestCase):
    def setUp(self):
        # 旧章構成fixtureを再利用するが、このsuiteは常にv3/default入口で検証する。
        self.f = legacy.DesignAdoptionTest()
        self.f.setUp()
        self.addCleanup(self.f.doCleanups)
        self.f.api_fixture()
        f = self.f
        f.contract['schema_version'] = 3
        f.contract['applicable_requirement_ids'] = ['R1', 'R2']
        f.cap['requirement_ids'] = ['R1', 'R2']
        f.cap['sources'].append('conformance.py')
        f.write('requirements.json', legacy.serialized({'requirements': [
            {'id': 'R1', 'status': 'active', 'acceptance_criteria': [{'id': 'A1'}]},
            {'id': 'R2', 'status': 'active', 'acceptance_criteria': [{'id': 'A2'}]}]}))
        f.inventory['requirement_ids'] = ['R1', 'R2']
        f.inventory['files'][0]['requirement_ids'] = ['R1', 'R2']
        f.write('inventory.json', legacy.serialized(f.inventory))
        reference = {k: f.inventory[k] for k in ('repository', 'revision')}
        api_profile = json.loads((f.root / 'profile.json').read_text())
        api_profile.update(id='fixture-six-documents', reference=reference)
        f.write('profile.json', legacy.serialized(api_profile))
        self.profile = {'schema_version': 1, 'id': 'fixture-conformance', 'version': '1.0.0',
                        'reference': reference, 'rule_ids': ['RULE-SOURCE', 'RULE-SAMPLE'],
                        'advisory_rule_ids': []}
        self.mapping = {'schema_version': 1, 'reference': reference, 'rules': [
            {'id': 'RULE-SOURCE', 'status': 'required', 'requirement_id': 'R1', 'acceptance_id': 'A1', 'reason': 'source validator'},
            {'id': 'RULE-SAMPLE', 'status': 'required', 'requirement_id': 'R2', 'acceptance_id': 'A2', 'reason': 'sample validator'}]}
        f.contract['conformance'] = {'profile': 'conformance-profile.json', 'mapping': 'mapping.json',
                                     'check': [sys.executable, 'conformance.py', '{report}']}
        shutil.copyfile(ROOT / 'tests/fixtures/design-adapter/conformance.py', f.root / 'conformance.py')
        f.write('conformance-mode.txt', 'normal')
        self.model = json.loads(f.templates[f.contract['crud']['model']])
        self.model.update(schema_version=2, resources=[{'id': 'items', 'group': 'db', 'kind': 'database'}])
        self.save()

    def save(self):
        f = self.f
        f.write('conformance-profile.json', legacy.serialized(self.profile))
        f.write('mapping.json', legacy.serialized(self.mapping))
        config = f.contract['crud']
        f.templates[config['model']] = legacy.serialized(self.model)
        for kind, body in MATRIX.renderings(self.model).items():
            f.templates[config[kind]] = body.decode()
        config['groups'] = {}
        for group, outputs in MATRIX.groups(self.model).items():
            config['groups'][group] = {}
            for kind, body in outputs.items():
                path = f'docs/generated/crud-{group}.{kind}'
                config['groups'][group][kind] = path
                f.templates[path] = body.decode()
        f.generate_baseline()
        f.write('contract.json', legacy.serialized(f.contract))

    def invoke(self, *args):
        self.f.write('contract.json', legacy.serialized(self.f.contract))
        return subprocess.run([sys.executable, str(legacy.SCRIPT), '--root', str(self.f.root),
                               '--contract', 'contract.json', *args], text=True, capture_output=True)

    def reject(self, message):
        result = self.invoke()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(message, result.stderr)

    def prepare(self):
        return CONFORMANCE.prepare(self.f.root, self.f.contract, ASSETS, INVENTORY.confined, INVENTORY.read_json)

    def test_default_entry_runs_fresh_semantic_tests_and_preserves_business_test_status(self):
        before = {p.relative_to(self.f.root): p.read_bytes() for p in self.f.root.rglob('*') if p.is_file()}
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.count('fixture conformance: executed 4 real cases'), 1)
        report = json.loads(result.stdout.splitlines()[-1])
        self.assertEqual(report['reference_conformance']['executed_test_count'], 4)
        self.assertEqual(report['reference_conformance']['required'], 2)
        self.assertEqual(report['execution_tests'], {'design': 'not-run'})
        after = {p.relative_to(self.f.root): p.read_bytes() for p in self.f.root.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_v2_cannot_claim_default_completion_and_v3_cannot_use_legacy_bypass(self):
        result = self.invoke('--legacy-layout-only')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('cannot bypass', result.stderr)
        self.f.contract['schema_version'] = 2
        self.reject('schema v3')

    def test_fresh_report_and_real_positive_negative_results_are_mandatory(self):
        for mode, message in [
            ('no-report', 'fresh report'), ('stale', 'wrong-source'),
            ('missing-negative', 'positive and negative'), ('not-run', 'failed/skipped/not-run'),
            ('uncollected', 'uncollected'), ('missing-rule', 'incomplete rule/test'),
            ('fail', 'command failed'), ('write-source', 'changed repository files')]:
            with self.subTest(mode=mode):
                self.f.write('conformance-mode.txt', mode)
                self.reject(message)

    def test_reference_cannot_be_replaced_by_a_secondary_inventory(self):
        self.f.inventory['repository'] = 'fixture:secondary'
        self.f.write('inventory.json', legacy.serialized(self.f.inventory))
        self.reject('authoritative reference inventory missing')

    def test_missing_collapsed_unknown_and_inactive_criteria_are_rejected(self):
        original = copy.deepcopy(self.mapping)
        mutations = [
            (lambda m: m['rules'].pop(), 'missing reference rules'),
            (lambda m: m['rules'][1].update(requirement_id='R1', acceptance_id='A1'), 'collapsed'),
            (lambda m: m['rules'][1].update(acceptance_id='invented'), 'acceptance criterion missing'),
            (lambda m: m['rules'][1].update(status='advisory'), 'disposition changed'),
            (lambda m: m['rules'][1].update(status='unsupported'), 'incomplete'),
        ]
        for mutate, message in mutations:
            with self.subTest(message=message):
                self.mapping = copy.deepcopy(original)
                mutate(self.mapping)
                self.save()
                with self.assertRaisesRegex(ValueError, message):
                    self.prepare()

    def test_changed_source_changes_digest(self):
        old = self.prepare()['source_digest']
        self.f.write('src/model.txt', 'new structure')
        self.assertNotEqual(old, self.prepare()['source_digest'])

    def test_reference_profile_mismatch_and_pinned_profile_shrink_are_rejected(self):
        self.profile['reference'] = {'repository': 'fixture:other', 'revision': '3' * 40}
        self.save()
        with self.assertRaisesRegex(ValueError, 'profile reference mismatch'):
            self.prepare()
        self.profile = json.loads((ASSETS / 'lazunex-conformance-v1.json').read_text())
        self.profile['rule_ids'].pop()
        self.save()
        with self.assertRaisesRegex(ValueError, 'shrink or replace'):
            self.prepare()

    def test_wrong_group_csv_and_edge_list_replacement_fail_before_execution(self):
        self.f.templates[self.f.contract['crud']['groups']['db']['csv']] = 'api,items\nlistItems,U\n'
        self.f.generate_baseline()
        self.reject('group export differs')
        self.save()
        self.f.templates[self.f.contract['crud']['csv']] = 'operation,resource,access\nlistItems,items,R\n'
        self.f.generate_baseline()
        self.reject('CRUD csv differs')

    def test_advisory_does_not_silently_become_a_blocking_threshold(self):
        self.profile['advisory_rule_ids'] = ['RULE-SAMPLE']
        self.mapping['rules'][1]['status'] = 'advisory'
        self.save()
        prepared = self.prepare()
        tests = [{'id': kind, 'kind': kind, 'status': 'pass', 'path': 'conformance.py', 'line': 1}
                 for kind in ('positive', 'negative')]
        report = {'schema_version': 1, 'source_digest': prepared['source_digest'], 'tests': tests,
                  'rules': [{'id': 'RULE-SOURCE', 'status': 'pass', 'test_ids': ['positive', 'negative'], 'reason': ''},
                            {'id': 'RULE-SAMPLE', 'status': 'not-run', 'test_ids': [], 'reason': '測定未実施。昇格しない。'}]}
        observed = CONFORMANCE.validate_result(self.f.root, report, prepared, INVENTORY.confined)
        self.assertEqual(observed['advisory_results'][0]['status'], 'not-run')

    def test_not_applicable_requires_both_executed_applicability_examples(self):
        self.mapping['rules'][1].update(status='not-applicable', reason='保存先へアクセスする機能がない')
        self.save()
        prepared = self.prepare()
        tests = [{'id': kind, 'kind': kind, 'status': 'pass', 'path': 'conformance.py', 'line': 1}
                 for kind in ('positive', 'negative')]
        report = {'schema_version': 1, 'source_digest': prepared['source_digest'], 'tests': tests,
                  'rules': [{'id': 'RULE-SOURCE', 'status': 'pass', 'test_ids': ['positive', 'negative'], 'reason': ''},
                            {'id': 'RULE-SAMPLE', 'status': 'not-applicable', 'test_ids': ['positive', 'negative'],
                             'reason': self.mapping['rules'][1]['reason']}]}
        observed = CONFORMANCE.validate_result(self.f.root, report, prepared, INVENTORY.confined)
        self.assertEqual(observed['not_applicable'], 1)
        report['rules'][1]['test_ids'] = []
        with self.assertRaisesRegex(ValueError, 'applicability positive and negative'):
            CONFORMANCE.validate_result(self.f.root, report, prepared, INVENTORY.confined)

    def test_test_location_must_belong_to_hashed_declared_sources(self):
        self.f.write('untracked-tests.py', 'def something(): pass\n')
        prepared = self.prepare()
        report = {'schema_version': 1, 'source_digest': prepared['source_digest'],
                  'tests': [{'id': 'unit', 'kind': 'positive', 'status': 'pass', 'path': 'untracked-tests.py', 'line': 1}], 'rules': []}
        with self.assertRaisesRegex(ValueError, 'outside the hashed declared sources'):
            CONFORMANCE.validate_result(self.f.root, report, prepared, INVENTORY.confined)

    def test_invalid_or_uncollected_locations_are_not_accepted_as_test_evidence(self):
        prepared = self.prepare()
        for line in (0, True, 100000):
            with self.subTest(line=line):
                report = {'schema_version': 1, 'source_digest': prepared['source_digest'],
                          'tests': [{'id': 'unit', 'kind': 'positive', 'status': 'pass', 'path': 'conformance.py', 'line': line}], 'rules': []}
                with self.assertRaisesRegex(ValueError, 'source location missing'):
                    CONFORMANCE.validate_result(self.f.root, report, prepared, INVENTORY.confined)


if __name__ == '__main__':
    unittest.main()
