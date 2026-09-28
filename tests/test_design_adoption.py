"""言語非依存manifestの正例と、実commandを伴う契約違反の回帰検証。"""
from __future__ import annotations

import copy
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / '.agents/skills/generate-implementation-design/scripts/check_design.py'
ASSETS = SCRIPT.parent.parent / 'assets'
FIXTURE = ROOT / 'tests/fixtures/design-adapter/adapter.py'


def serialized(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n'


class DesignAdoptionTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.write('src/model.txt', 'current structure\n')
        self.write('mode.txt', 'normal')
        shutil.copyfile(FIXTURE, self.root / 'adapter.py')
        self.write('requirements.json', serialized({'requirements': [
            {'id': 'R1', 'status': 'active'}, {'id': 'R2', 'status': 'active'},
            {'id': 'RETIRED', 'status': 'retired'},
        ]}))
        files = [{
            'path': 'src/tools/adapter.txt', 'blob_sha': '1' * 40,
            'purpose': 'fixture generation', 'classification': 'as-built-generator',
            'requirement_ids': ['R1'], 'adoption': 'adapt',
            'reason': 'use the target command', 'language_assumptions': [],
            'connections': ['adapter.py'],
        }]
        self.inventory = {
            'schema_version': 1, 'repository': 'fixture:offline-reference',
            'revision': '2' * 40, 'source_root': 'src/tools', 'scope': 'target-adoption',
            'file_count': 1, 'tree_sha256': hashlib.sha256(
                ('src/tools/adapter.txt\t' + '1' * 40 + '\n').encode()).hexdigest(),
            'requirement_ids': ['R1'], 'files': files, 'gaps': [],
        }
        self.write('inventory.json', serialized(self.inventory))
        self.templates = {
            'docs/generated/index.md': '# 現在の設計\n\n{{SOURCE}}\n',
            'docs/generated/report.json': serialized({
                'configuration': 'pass', 'design_drift': 'pass',
                'execution_tests': 'not-run', 'unsupported_surfaces': [],
            }),
        }
        self.cap = {
            'status': 'required', 'requirement_ids': ['R1'], 'sources': ['src'],
            'generate': [sys.executable, 'adapter.py'],
            'check': [sys.executable, 'adapter.py', '--check'],
            'output_root': 'docs/generated', 'outputs': list(self.templates),
            'report': 'docs/generated/report.json',
        }
        self.contract = {
            'schema_version': 2, 'requirements': 'requirements.json',
            'applicable_requirement_ids': ['R1'], 'reference_inventories': ['inventory.json'],
            'surfaces': {name: {'status': 'not-applicable', 'reason': 'fixture has no such implementation'}
                         for name in ('api', 'data', 'infra', 'frontend')},
            'capabilities': {'design': self.cap},
        }
        self.contract['surfaces']['frontend'] = {'status': 'required', 'capabilities': ['design']}
        self.generate_baseline()

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')

    def generate_baseline(self):
        self.write('templates.json', serialized(self.templates))
        source = (self.root / 'src/model.txt').read_text().strip()
        for path, text in self.templates.items():
            self.write(path, text.replace('{{SOURCE}}', source))
        self.cap['outputs'] = list(self.templates)

    def invoke(self):
        self.write('contract.json', serialized(self.contract))
        return subprocess.run([sys.executable, str(SCRIPT), '--root', str(self.root),
                               '--contract', 'contract.json', '--legacy-layout-only'], text=True, capture_output=True)

    def reject(self, expected):
        result = self.invoke()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(expected, result.stderr, result.stderr)
        return result

    def api_fixture(self, no_access=False):
        self.contract['surfaces']['frontend'] = {'status': 'not-applicable', 'reason': 'API only'}
        self.contract['surfaces']['api'] = {'status': 'required', 'capabilities': ['design']}
        shutil.copyfile(ASSETS / 'api-document-profile-v1.json', self.root / 'profile.json')
        base = 'docs/generated/group/items'
        self.templates['docs/generated/index.md'] = '# 設計索引\n\n[group](group/index.md)\n{{SOURCE}}\n'
        self.templates['docs/generated/group/index.md'] = '# group\n\n[items](items/index.md)\n'
        documents = {kind: f'{base}/{kind}.md' for kind in (
            'detail-design', 'interface', 'messages', 'query', 'sequence', 'unit-test')}
        self.templates[f'{base}/index.md'] = '# API索引\n\n' + ''.join(
            f'[{kind}]({kind}.md)\n' for kind in documents)
        # 独立した手書きfixtureによりprofileの章順・階層を検証する。
        self.templates[documents['detail-design']] = '''# 詳細設計
## 1. 正常系入力
入力値。
## 2. 正常系前提
認証済み。
## 3. 正常系リソース変更
更新しない。
## 4. 正常系レスポンス
項目一覧。
'''
        self.templates[documents['interface']] = '''# Interface
## Headers
## Path Parameters
## Query Parameters
## Data
## Responses
##### 200 項目一覧
##### 400 入力不正
## Samples
### 200
#### Request
#### Response
### 400
#### Request
#### Response
'''
        self.templates[documents['messages']] = '''# ログ
## API
## 生成・検証方針
## メッセージ一覧
## ログ詳細
### 取得完了
#### 出力項目
## strict検証で要求する項目
'''
        self.templates[documents['query']] = '''# Query
## 項目取得
### SQL種別
SELECT
### SQLの概要
項目一覧を取得する。
### 利用するテーブル
items
### 引数
なし。
### 戻り値
項目一覧。
### 条件
なし。
'''
        self.templates[documents['sequence']] = '# Sequence\n\n```mermaid\nsequenceDiagram\nClient->>API: list\nAPI-->>Client: items\n```\n'
        self.templates[documents['unit-test']] = '''# 単体テスト
## 0. endpoint層の暗黙処理
## 1. 要因ごとの要素
### 入力
## 2. 組合せたテストケース一覧
## 3. テスト詳細
### 正常一覧
Given 項目が存在する。When 一覧を取得する。Then 項目が返る。
'''
        self.operation = {'id': 'listItems', 'group': 'group', 'api': 'items',
                          'documents': documents, 'sections': {
                              'queries': ['項目取得'], 'messages': ['取得完了'],
                              'responses': ['200 項目一覧', '400 入力不正'],
                              'samples': ['200', '400'],
                              'factors': ['入力'], 'cases': ['正常一覧']}}
        self.write('operations.json', serialized(['listItems']))
        self.contract['api'] = {
            'profile': 'profile.json', 'operation_inventory': 'operations.json',
            'root': 'docs/generated', 'index': 'docs/generated/index.md',
            'group_indexes': {'group': 'docs/generated/group/index.md'},
            'api_indexes': {'listItems': f'{base}/index.md'}, 'operations': [self.operation],
        }
        model = {'schema_version': 1, 'operations': ['listItems'], 'rows': [{
            'operation': 'listItems', 'resource': 'items', 'access': ['R'],
            'evidence': [{'path': 'src/model.txt', 'line': 1, 'role': 'read'}],
        }], 'no_access': {}, 'unresolved': []}
        if no_access:
            model.update(rows=[], no_access={'listItems': '固定応答で保存先へアクセスしない'})
            self.operation['sections']['queries'] = []
            self.operation['non_applicable'] = {'queries': '保存先へのアクセスなし'}
            self.templates[documents['query']] = '# Query\n\n該当なし（理由: 保存先へのアクセスなし）\n'
        resource, access = ('-', 'NONE') if no_access else ('items', 'R')
        crud = {'model': 'docs/generated/crud.json', 'csv': 'docs/generated/crud.csv',
                'table': 'docs/generated/crud.md', 'diagram': 'docs/generated/crud.mmd',
                'evidence': 'docs/generated/crud-evidence.json'}
        self.contract['crud'] = crud
        self.templates[crud['model']] = serialized(model)
        self.templates[crud['evidence']] = serialized(model)
        self.templates[crud['csv']] = f'operation,resource,access\nlistItems,{resource},{access}\n'
        self.templates[crud['table']] = '# API×保存先 CRUD\n\n| operation | resource | access |\n|---|---|---|\n' + f'| listItems | {resource} | {access} |\n'
        self.templates[crud['diagram']] = f'flowchart LR\n  a0["listItems"] -->|{access}| r0["{resource}"]\n'
        self.generate_baseline()

    def test_connected_design_runs_check_and_two_generations_without_writing_original(self):
        before = {p: (self.root / p).read_bytes() for p in self.cap['outputs']}
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.count('fixture adapter: check'), 1)
        self.assertEqual(result.stdout.count('fixture adapter: generate'), 2)
        report = json.loads(result.stdout.splitlines()[-1])
        self.assertEqual(report['execution_tests'], {'design': 'not-run'})
        self.assertEqual(before, {p: (self.root / p).read_bytes() for p in self.cap['outputs']})

    def test_api_six_documents_hierarchy_and_common_crud_model_pass(self):
        self.api_fixture()
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.count('fixture adapter: generate'), 2)

    def test_no_access_keeps_query_document_and_explicit_reason(self):
        self.api_fixture(no_access=True)
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)
        del self.operation['non_applicable']
        self.reject('explicit not-applicable reason')

    def test_chapter_missing_reordered_duplicate_and_query_section_missing(self):
        self.api_fixture()
        documents = self.operation['documents']
        mutations = [
            ('interface', lambda t: t.replace('## Headers\n', '')),
            ('interface', lambda t: t.replace('## Headers\n## Path Parameters', '## Path Parameters\n## Headers')),
            ('interface', lambda t: t + '## Samples\n'),
            ('query', lambda t: t.replace('### 引数\n', '')),
        ]
        original = copy.deepcopy(self.templates)
        for kind, mutation in mutations:
            with self.subTest(kind=kind, mutation=mutation):
                self.templates = copy.deepcopy(original)
                self.templates[documents[kind]] = mutation(self.templates[documents[kind]])
                self.generate_baseline()
                self.reject('chapter missing/order/duplicate')

    def test_interface_repeated_response_and_sample_chapters_are_required(self):
        self.api_fixture()
        path = self.operation['documents']['interface']
        original = self.templates[path]
        for removed in ('##### 400 入力不正\n', '### 400\n', '#### Request\n', '#### Response\n'):
            with self.subTest(removed=removed):
                self.templates[path] = original.replace(removed, '', 1)
                self.generate_baseline()
                self.reject('chapter missing/order/duplicate')

    def test_profile_grammar_types_and_section_constraints_are_validated(self):
        self.api_fixture()
        profile = json.loads((self.root / 'profile.json').read_text())
        mutations = [
            lambda p: p.update(schema_version=True),
            lambda p: p.update(headings={key: '' for key in p['headings']}),
            lambda p: p['headings'].update(interface=[]),
            lambda p: p['headings'].update(sequence=''),
            lambda p: p['headings']['interface'][0].update(level=True),
            lambda p: p['headings']['interface'][0].update(level=7),
            lambda p: p['headings']['interface'][0].update(title=' '),
            lambda p: p['headings']['interface'][0].update(repeat='mixed'),
            lambda p: p['headings']['query'][0].update(min=-1),
            lambda p: p['headings']['query'][0].update(min=True),
            lambda p: p['headings']['query'][0].update(children=''),
            lambda p: p['headings']['query'][0]['children'][0].update(level=2),
            lambda p: p['headings']['query'][0].pop('empty'),
            lambda p: p['headings']['query'][0].update(empty='該当なし'),
            lambda p: p.update(non_applicable='{unknown}'),
            lambda p: p.update(non_applicable='{reason!r}'),
            lambda p: p.update(layout='{group}/{api}/{unknown}.md'),
        ]
        for index, mutate in enumerate(mutations):
            with self.subTest(index=index):
                changed = copy.deepcopy(profile)
                mutate(changed)
                self.write('profile.json', serialized(changed))
                self.reject('profile')

    def test_published_profile_cannot_remove_or_change_chapters_under_same_version(self):
        self.api_fixture()
        profile = json.loads((self.root / 'profile.json').read_text())
        for kind in ('detail-design', 'interface', 'messages', 'query', 'unit-test'):
            for change in ('remove', 'rename'):
                with self.subTest(kind=kind, change=change):
                    changed = copy.deepcopy(profile)
                    section = changed['headings'][kind][0]
                    if change == 'remove':
                        changed['headings'][kind].pop(0)
                    elif 'title' in section:
                        section['title'] = '改変した章'
                    else:
                        section['children'].pop()
                    self.write('profile.json', serialized(changed))
                    self.reject('profile')

    def test_explicit_custom_profile_version_is_allowed(self):
        self.api_fixture()
        profile = json.loads((self.root / 'profile.json').read_text())
        profile.update(id='target-profile', version='2.0.0')
        self.write('profile.json', serialized(profile))
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_interface_response_and_sample_declarations_cannot_be_empty(self):
        self.api_fixture()
        for key in ('responses', 'samples'):
            with self.subTest(key=key):
                original = self.operation['sections'][key]
                self.operation['sections'][key] = []
                self.reject('missing repeated section')
                self.operation['sections'][key] = original

    def test_required_repeated_factors_cannot_be_empty(self):
        self.api_fixture()
        self.operation['sections']['factors'] = []
        self.reject('missing repeated section')

    def test_six_document_schema_and_operation_set_are_exact(self):
        self.api_fixture()
        value = self.operation['documents'].pop('query')
        self.reject('missing fields')
        self.operation['documents']['query'] = value
        self.write('operations.json', serialized(['listItems', 'unmappedOperation']))
        self.reject('operation inventory mismatch')

    def test_missing_hierarchy_link_is_rejected(self):
        self.api_fixture()
        self.templates['docs/generated/group/index.md'] = '# group\n\nAPI link is missing.\n'
        self.generate_baseline()
        self.reject('index missing API/document link')

    def test_stale_and_deleted_outputs_are_rejected(self):
        self.write('docs/generated/old.md', '# old layout')
        self.reject('stale or missing outputs')
        (self.root / 'docs/generated/old.md').unlink()
        (self.root / 'docs/generated/index.md').unlink()
        self.reject('stale or missing outputs')

    def test_retired_generator_target_is_rejected_even_when_manifest_keeps_it(self):
        self.templates['docs/generated/retired.md'] = '# 旧生成物\n'
        self.generate_baseline()
        del self.templates['docs/generated/retired.md']
        self.write('templates.json', serialized(self.templates))
        before = {p: (self.root / p).read_bytes() for p in self.cap['outputs']}
        result = self.reject('stale or missing outputs')
        self.assertIn('fixture adapter: check', result.stdout)
        self.assertIn('retired.md', result.stderr)
        self.assertEqual(before, {p: (self.root / p).read_bytes() for p in self.cap['outputs']})

    def test_both_generations_start_with_empty_owned_outputs(self):
        self.write('mode.txt', 'requires-clean-output')
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.count('fixture adapter: generate'), 2)

    def test_broken_file_and_fragment_links_are_rejected(self):
        for target in ('absent.md', 'index.md#absent-section'):
            with self.subTest(target=target):
                self.templates['docs/generated/index.md'] = f'# 現在の設計\n\n[broken]({target})\n'
                self.generate_baseline()
                self.reject('broken')

    def test_markdown_destination_and_title_variants_detect_missing_files(self):
        links = [
            "[x](missing.md 'Title')", '[x](<missing file.md>)',
            '[x](missing.md "Title")', '[x](missing.md (Title))',
            '[x](<missing file.md> \'Title\')', '[x](missing(part).md)',
            r'[x](missing\(part\).md)', '[x](missing&amp;file.md)',
            '[x](missing%20file.md)', "![x](missing.png 'Title')",
            '[x](\n<missing file.md>\n"Title"\n)',
            "[x][ref]\n\n[ref]: <missing file.md> 'Title'",
            '[REF][]\n\n[ref]: missing.md (Title)',
            '[Some   Label]\n\n[some label]: missing.md',
            '[![image](missing.png)](index.md)',
            '[a `]` b](missing.md)', '[a `[` b](missing.md)',
        ]
        for link in links:
            with self.subTest(link=link):
                self.templates['docs/generated/index.md'] = '# 現在の設計\n\n' + link + '\n'
                self.generate_baseline()
                self.reject('broken link')

    def test_supported_markdown_links_resolve_real_destinations(self):
        for name in ('file name.md', 'file(part).md', 'file&name.md'):
            self.templates['docs/generated/' + name] = '# リンク先\n'
        self.templates['docs/generated/index.md'] = '''# 現在の設計
[single](<file name.md> 'Title')
[double](file%20name.md "Title")
[parentheses](file(part).md (Title))
[entity](file&amp;name.md)
[explicit][My Label]
[my label][]
[MY LABEL]

[my label]: <file name.md>
  'Title'
'''
        self.generate_baseline()
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_unsupported_or_malformed_links_fail_with_source_location(self):
        links = ['[x](<missing.md)', '[x](missing.md "unterminated)',
                 '[x](missing file.md)', '<a href="missing.md">x</a>',
                 '> [ref]: missing.md\n\n[x][ref]']
        for link in links:
            with self.subTest(link=link):
                self.templates['docs/generated/index.md'] = '# 現在の設計\n\n' + link + '\n'
                self.generate_baseline()
                result = self.reject('unsupported or malformed Markdown link')
                self.assertIn('docs/generated/index.md:3', result.stderr)

    def test_link_examples_in_code_and_escaped_brackets_are_not_links(self):
        self.templates['docs/generated/index.md'] = r'''# 現在の設計
`[x](missing.md)`
`` [x](missing.md 'Title') ``
\[x](missing.md)
````markdown
[x](missing.md)
```
[x](<missing file.md>)
````
~~~markdown
[x](missing.md)
~~~~
'''
        self.generate_baseline()
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_crud_csv_table_diagram_and_evidence_must_match_model(self):
        self.api_fixture()
        for kind in ('csv', 'table', 'diagram', 'evidence'):
            with self.subTest(kind=kind):
                path = self.contract['crud'][kind]
                before = self.templates[path]
                self.templates[path] += '\nwrong projection\n'
                self.generate_baseline()
                self.reject(f'CRUD {kind} differs from common model')
                self.templates[path] = before

    def test_unresolved_dynamic_access_cannot_be_no_access(self):
        self.api_fixture(no_access=True)
        path = self.contract['crud']['model']
        model = json.loads(self.templates[path])
        model['unresolved'] = [{'operation': 'listItems', 'reason': 'dynamic call'}]
        self.templates[path] = serialized(model)
        self.generate_baseline()
        self.reject('unresolved CRUD is not no-access')

    def test_unknown_inactive_unmapped_and_excess_requirement_ids_are_rejected(self):
        for applicable, mapped in [(['UNKNOWN'], ['UNKNOWN']), (['RETIRED'], ['RETIRED']),
                                   (['R1', 'R2'], ['R1']), (['R1'], ['R1', 'R2'])]:
            with self.subTest(applicable=applicable, mapped=mapped):
                self.contract['applicable_requirement_ids'] = applicable
                self.cap['requirement_ids'] = mapped
                self.reject('unknown/inactive/unmapped/excess requirement IDs')

    def test_missing_duplicate_and_bad_sha_inventory_are_rejected(self):
        mutations = [lambda v: v.update(file_count=2),
                     lambda v: v['files'].append(copy.deepcopy(v['files'][0])),
                     lambda v: v['files'][0].update(blob_sha='3' * 40)]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                inventory = copy.deepcopy(self.inventory)
                mutation(inventory)
                self.write('inventory.json', serialized(inventory))
                self.reject('inventory' if len(inventory['files']) == 1 else 'duplicate')

    def test_missing_inventory_connection_is_rejected(self):
        self.inventory['files'][0]['connections'] = ['missing-adapter.py']
        self.write('inventory.json', serialized(self.inventory))
        self.reject('missing inventory connection')

    def test_second_generation_byte_difference_is_rejected(self):
        self.write('mode.txt', 'second-nondeterministic')
        before = (self.root / 'docs/generated/index.md').read_bytes()
        result = self.reject('nondeterministic generation')
        self.assertEqual(result.stdout.count('fixture adapter: generate'), 2)
        self.assertEqual((self.root / 'docs/generated/index.md').read_bytes(), before)

    def test_unsupported_surface_cannot_be_reported_as_success(self):
        path = self.cap['report']
        report = json.loads(self.templates[path])
        report['unsupported_surfaces'] = [{'path': 'src/model.txt', 'reason': 'dynamic call',
                                           'support_status': 'unsupported'}]
        self.templates[path] = serialized(report)
        self.generate_baseline()
        self.reject('unsupported surface remains incomplete')

    def test_combined_success_report_cannot_replace_separate_evidence(self):
        self.templates[self.cap['report']] = serialized({'status': 'success'})
        self.generate_baseline()
        self.reject('report must separate')

    def test_failed_execution_tests_are_not_hidden_by_configuration_pass(self):
        report = json.loads(self.templates[self.cap['report']])
        report['execution_tests'] = 'fail'
        self.templates[self.cap['report']] = serialized(report)
        self.generate_baseline()
        self.reject('failed adapter report')

    def test_output_symlink_and_unmanaged_declared_path_are_rejected(self):
        path = self.root / 'docs/generated/index.md'
        path.unlink()
        path.symlink_to(self.root / 'src/model.txt')
        self.reject('symlink')
        path.unlink()
        self.generate_baseline()
        self.write('elsewhere.md', '# unmanaged')
        self.cap['outputs'].append('elsewhere.md')
        self.reject('unmanaged output path')

    def test_source_symlink_is_rejected(self):
        (self.root / 'src/link.txt').symlink_to(self.root / 'mode.txt')
        self.reject('symlink')

    def test_parent_traversal_and_absolute_output_paths_are_rejected(self):
        for path in ('../outside.md', '/tmp/outside.md'):
            with self.subTest(path=path):
                self.cap['outputs'] = [path]
                self.reject('invalid relative path')

    def test_check_that_rewrites_outputs_is_rejected_without_changing_original(self):
        self.write('mode.txt', 'rewrite-check')
        before = (self.root / 'docs/generated/index.md').read_bytes()
        self.reject('check: drift')
        self.assertEqual((self.root / 'docs/generated/index.md').read_bytes(), before)

    def test_source_change_detects_drift_without_regenerating_original(self):
        before = (self.root / 'docs/generated/index.md').read_bytes()
        self.write('src/model.txt', 'changed structure')
        self.reject('check command failed')
        self.assertEqual((self.root / 'docs/generated/index.md').read_bytes(), before)

    def test_generator_cannot_write_unowned_file_or_delete_outputs(self):
        for mode, message in [('unowned-write', 'changed unowned files'),
                              ('delete-output', 'stale or missing outputs'),
                              ('directory-replacement', 'stale')]:
            with self.subTest(mode=mode):
                self.write('mode.txt', mode)
                self.reject(message)
                self.assertFalse((self.root / 'unowned.txt').exists())
                self.assertTrue((self.root / 'docs/generated/index.md').is_file())

    def test_unowned_directory_and_symlink_replacement_are_rejected(self):
        for mode in ('unowned-directory', 'unowned-symlink-replacement'):
            with self.subTest(mode=mode):
                target = self.root / 'unowned-empty'
                if mode == 'unowned-symlink-replacement':
                    target.mkdir()
                self.write('mode.txt', mode)
                self.reject('unowned')
                self.assertFalse(target.is_symlink())
                if target.exists():
                    self.assertEqual(list(target.iterdir()), [])

    def test_undeclared_empty_output_directory_is_stale(self):
        (self.root / 'docs/generated/unused').mkdir()
        self.reject('stale undeclared output directory')

    def test_generator_cannot_add_undeclared_output_directory(self):
        self.write('mode.txt', 'undeclared-output-directory')
        self.reject('stale undeclared output directory')

    def test_reference_blueprint_cannot_claim_connected_target_adoption(self):
        self.inventory['scope'] = 'reference-blueprint'
        self.write('inventory.json', serialized(self.inventory))
        self.reject('target-adoption')

    def test_reference_style_links_are_checked(self):
        for text in ('[ghost][]\n\n[ghost]: absent.md', '[ghost]\n\n[ghost]: absent.md', '[label][absent]'):
            with self.subTest(text=text):
                self.templates['docs/generated/index.md'] = '# Design\n\n' + text + '\n'
                self.generate_baseline()
                self.reject('broken')

    def test_valid_collapsed_and_shortcut_reference_links(self):
        self.templates['docs/generated/index.md'] = '# Design\n\n[current][] and [current]\n\n[current]: index.md\n'
        self.generate_baseline()
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_overlapping_output_roots_are_rejected(self):
        self.contract['capabilities']['alias'] = copy.deepcopy(self.cap)
        self.reject('overlapping output ownership')

    def test_manifest_missing_unknown_field_and_wrong_version_are_rejected(self):
        missing = subprocess.run([sys.executable, str(SCRIPT), '--root', str(self.root)],
                                 text=True, capture_output=True)
        self.assertNotEqual(missing.returncode, 0)
        self.assertIn('as-built incomplete', missing.stderr)
        self.contract['surprise'] = True
        self.reject('unknown fields')
        del self.contract['surprise']
        self.contract['schema_version'] = 1
        self.reject('schema_version: invalid value')

    def test_unclassified_or_unconnected_surface_is_rejected(self):
        surface = self.contract['surfaces'].pop('data')
        self.reject('classify')
        self.contract['surfaces']['data'] = surface
        self.contract['surfaces']['frontend']['capabilities'] = ['missing']
        self.reject('missing/unsupported capability')

    def test_missing_commands_and_check_flag_are_rejected(self):
        value = self.cap.pop('generate')
        self.reject('capability requires generation')
        self.cap['generate'] = value
        self.cap['check'].remove('--check')
        self.reject('capability requires generation')

    def test_non_applicable_requires_reason(self):
        self.contract['surfaces']['data']['reason'] = ' '
        self.reject('invalid string')

    def test_empty_markdown_is_not_complete(self):
        self.templates['docs/generated/index.md'] = ' \n'
        self.generate_baseline()
        self.reject('nonempty Markdown design required')


if __name__ == '__main__':
    unittest.main()
