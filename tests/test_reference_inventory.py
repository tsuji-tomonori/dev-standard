"""固定した参照treeの全件性と、言語非依存の採用記録契約をネットなしで検証する。"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / '.agents/skills/generate-implementation-design'
SCRIPT = SKILL / 'scripts/reference_inventory.py'
SPEC = importlib.util.spec_from_file_location('reference_inventory_test_subject', SCRIPT)
inventory = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(inventory)
CATALOG = SKILL / 'assets/reference-tools/lazunex-096e1e5.json'
PINNED_REVISION = '096e1e580ab1c0670c57e4febad2bd9fdd4698ee'
PINNED_TREE = '8cac4a032500cf2e846f5dbbec08aa275cc9593d74a7168e8604f75fcebdfa5e'


def fixture():
    files = [{
        'path': 'src/tools/checker.js', 'blob_sha': 'a' * 40,
        'purpose': 'endpoint所有の検査', 'classification': 'static-checker',
        'requirement_ids': ['REQ-TEST-001'], 'adoption': 'adapt',
        'reason': '対象言語へ解析を移す', 'language_assumptions': ['JavaScript'],
        'connections': ['tools/checker.js'],
    }]
    return {
        'schema_version': 1, 'repository': 'local-reference', 'revision': 'b' * 40,
        'source_root': 'src/tools', 'scope': 'reference-blueprint', 'file_count': 1,
        'tree_sha256': inventory.tree_digest(files), 'requirement_ids': ['REQ-TEST-001', 'REQ-TEST-002'],
        'files': files, 'gaps': [{'requirement_id': 'REQ-TEST-002', 'reason': '導入先で動的呼出しを補う'}],
    }


ACTIVE = {'REQ-TEST-001', 'REQ-TEST-002'}


class ReferenceInventoryTest(unittest.TestCase):
    def test_pinned_catalog_is_complete_and_matches_canonical_ids(self):
        data = inventory.read_json(CATALOG)
        requirements = inventory.read_json(ROOT / 'spec/requirements/requirements.json')
        active = {item['id'] for item in requirements['requirements'] if item['status'] == 'active'}
        self.assertEqual(data['revision'], PINNED_REVISION)
        self.assertEqual(data['file_count'], 52)
        self.assertEqual(len(data['files']), 52)
        self.assertEqual(len({item['path'] for item in data['files']}), 52)
        self.assertEqual(data['tree_sha256'], PINNED_TREE)
        # checker自身のdigest関数とは別に固定treeを照合する。
        records = ''.join(item['path'] + '\t' + item['blob_sha'] + '\n'
                          for item in sorted(data['files'], key=lambda item: item['path']))
        self.assertEqual(hashlib.sha256(records.encode()).hexdigest(), PINNED_TREE)
        inventory.validate_inventory(data, active)
        covered = {identity for item in data['files'] for identity in item['requirement_ids']}
        covered.update(gap['requirement_id'] for gap in data['gaps'])
        self.assertEqual(covered, set(data['requirement_ids']))
        self.assertLessEqual(covered, active)
        adapter_scope = {identity for identity in active if identity.startswith((
            "REQ-ASBUILT-", "REQ-DESIGN-", "REQ-DOCS-", "REQ-EVIDENCE-"))}
        self.assertEqual(covered, adapter_scope)

    def test_catalog_markdown_is_deterministic_and_current(self):
        data = inventory.read_json(CATALOG)
        expected = inventory.render(data)
        reordered = copy.deepcopy(data)
        reordered['files'].reverse()
        self.assertEqual(inventory.render(reordered), expected)
        self.assertEqual(CATALOG.with_suffix('.md').read_text(), expected)

    def test_semantic_checks_map_to_their_own_obligations_and_explicit_gaps(self):
        data = inventory.read_json(CATALOG)
        files = {item['path']: set(item['requirement_ids']) for item in data['files']}
        expected = {
            'check_api_router_ignored_returns.py': {'REQ-DESIGN-018'},
            'check_constant_bool_returns.py': {'REQ-DESIGN-019'},
            'check_bool_router_conditions.py': {'REQ-DESIGN-018'},
            'check_api_function_exception_policy.py': {'REQ-DESIGN-021'},
        }
        for name, identities in expected.items():
            with self.subTest(name=name):
                self.assertEqual(files['src/tools/' + name], identities)
        self.assertLessEqual({'REQ-DESIGN-020', 'REQ-DESIGN-021', 'REQ-DESIGN-022'},
                             files['src/tools/rulecheck/builtin_checks.py'])
        gaps = {item['requirement_id'] for item in data['gaps']}
        self.assertLessEqual({'REQ-DESIGN-009', 'REQ-DESIGN-015', 'REQ-DESIGN-018',
                              'REQ-DESIGN-020', 'REQ-DESIGN-022', 'REQ-DESIGN-023',
                              'REQ-DESIGN-024', 'REQ-DESIGN-025', 'REQ-ASBUILT-035'}, gaps)

    def test_language_independent_fixture_and_explicit_gap(self):
        inventory.validate_inventory(fixture(), ACTIVE)

    def test_missing_excess_duplicate_and_sha_mismatch_are_rejected(self):
        mutations = (
            lambda data: data['files'].clear(),
            lambda data: data['files'].append({**data['files'][0], 'path': 'src/tools/extra.rs'}),
            lambda data: data['files'].append({**data['files'][0], 'purpose': 'duplicate path'}),
            lambda data: data['files'][0].update(blob_sha='c' * 40),
            lambda data: data['files'][0].update(path='src/tools/renamed.js'),
        )
        for index, mutate in enumerate(mutations):
            with self.subTest(index=index):
                data = fixture()
                mutate(data)
                with self.assertRaises(ValueError):
                    inventory.validate_inventory(data, ACTIVE)

    def test_duplicate_path_is_rejected_even_with_updated_count_and_digest(self):
        data = fixture()
        data['files'].append({**data['files'][0], 'purpose': '同じpathの異なる説明'})
        data['file_count'] = 2
        data['tree_sha256'] = inventory.tree_digest(data['files'])
        with self.assertRaisesRegex(ValueError, 'duplicate paths'):
            inventory.validate_inventory(data, ACTIVE)

    def test_unknown_inactive_unmapped_and_extra_requirement_ids_are_rejected(self):
        mutations = (
            lambda data: data['files'][0]['requirement_ids'].append('REQ-UNKNOWN-001'),
            lambda data: data['requirement_ids'].append('REQ-UNKNOWN-001'),
            lambda data: data['gaps'].clear(),
            lambda data: data['requirement_ids'].remove('REQ-TEST-002'),
        )
        for index, mutate in enumerate(mutations):
            with self.subTest(index=index):
                data = fixture()
                mutate(data)
                with self.assertRaisesRegex(ValueError, 'coverage|unknown|inactive'):
                    inventory.validate_inventory(data, ACTIVE)
        with self.assertRaisesRegex(ValueError, 'unknown|inactive'):
            inventory.validate_inventory(fixture(), {'REQ-TEST-001'})

    def test_invalid_schema_fields_and_missing_decision_are_rejected(self):
        mutations = (
            lambda data: data.update(extra='unknown field'),
            lambda data: data.update(file_count=True),
            lambda data: data.update(schema_version=True),
            lambda data: data.update(revision='main'),
            lambda data: data['files'][0].update(adoption='maybe'),
            lambda data: data['files'][0].update(classification='python-only'),
            lambda data: data['files'][0].update(reason=' '),
            lambda data: data['files'][0].pop('purpose'),
            lambda data: data['gaps'][0].update(reason=''),
        )
        for index, mutate in enumerate(mutations):
            with self.subTest(index=index):
                data = fixture()
                mutate(data)
                with self.assertRaises(ValueError):
                    inventory.validate_inventory(data, ACTIVE)

    def test_adopted_tool_requires_connection_and_nonadoption_requires_reason(self):
        data = fixture()
        data['files'][0]['connections'] = []
        with self.assertRaisesRegex(ValueError, 'connection'):
            inventory.validate_inventory(data, ACTIVE)
        data['files'][0]['adoption'] = 'not-adopted'
        inventory.validate_inventory(data, ACTIVE)
        data['files'][0]['reason'] = ''
        with self.assertRaises(ValueError):
            inventory.validate_inventory(data, ACTIVE)

    def test_target_adoption_requires_actual_confined_connection(self):
        data = fixture()
        data['scope'] = 'target-adoption'
        with self.assertRaisesRegex(ValueError, 'target_root'):
            inventory.validate_inventory(data, ACTIVE)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaisesRegex(ValueError, 'missing inventory connection'):
                inventory.validate_inventory(data, ACTIVE, target_root=root)
            (root / 'tools').mkdir()
            (root / 'tools/checker.js').write_text('export const connected = true;\n')
            inventory.validate_inventory(data, ACTIVE, target_root=root)
            (root / 'tools/link.js').symlink_to(root / 'tools/checker.js')
            for connection in ('../checker.js', '/etc/passwd', 'tools/link.js', 'tools'):
                with self.subTest(connection=connection):
                    data['files'][0]['connections'] = [connection]
                    with self.assertRaises(ValueError):
                        inventory.validate_inventory(data, ACTIVE, target_root=root)

    def test_inventory_paths_must_stay_inside_source_root(self):
        for path in ('elsewhere/checker.js', '../tools/checker.js', '/src/tools/checker.js', 'src/tools/../checker.js'):
            with self.subTest(path=path):
                data = fixture()
                data['files'][0]['path'] = path
                data['tree_sha256'] = inventory.tree_digest(data['files'])
                with self.assertRaises(ValueError):
                    inventory.validate_inventory(data, ACTIVE)

    def test_duplicate_json_keys_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'bad.json'
            path.write_text('{"files": [], "files": []}')
            with self.assertRaisesRegex(ValueError, 'duplicate JSON key'):
                inventory.read_json(path)

    def test_cli_markdown_check_reports_drift_without_repair(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, requirements, output = root / 'inventory.json', root / 'requirements.json', root / 'inventory.md'
            source.write_text(json.dumps(fixture()))
            requirements.write_text(json.dumps({'requirements': [{'id': name, 'status': 'active'} for name in sorted(ACTIVE)]}))
            command = [sys.executable, str(SCRIPT), str(source), '--requirements', str(requirements), '--out', str(output)]
            subprocess.run(command, check=True, capture_output=True)
            original = output.read_bytes()
            subprocess.run([*command, '--check'], check=True, capture_output=True)
            self.assertEqual(output.read_bytes(), original)
            output.write_text('drift')
            result = subprocess.run([*command, '--check'], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('Markdown drift', result.stderr)
            self.assertEqual(output.read_text(), 'drift')

    def test_local_git_reference_root_checks_fixed_commit_and_entire_tree(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            def git(*args):
                return subprocess.check_output(['git', '-C', str(root), *args], text=True).strip()
            git('init', '-q')
            (root / 'src/tools').mkdir(parents=True)
            (root / 'src/tools/checker.js').write_text('export const valid = true;\n')
            git('add', '.')
            git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                '-c', 'commit.gpgsign=false', 'commit', '-qm', 'reference fixture')
            data = fixture()
            data['revision'] = git('rev-parse', 'HEAD')
            data['files'][0]['blob_sha'] = git('rev-parse', 'HEAD:src/tools/checker.js')
            data['tree_sha256'] = inventory.tree_digest(data['files'])
            inventory.validate_inventory(data, ACTIVE, reference_root=root)
            source, requirements = root / 'inventory.json', root / 'requirements.json'
            source.write_text(json.dumps(data))
            requirements.write_text(json.dumps({'requirements': [
                {'id': name, 'status': 'active'} for name in sorted(ACTIVE)]}))
            subprocess.run([sys.executable, str(SCRIPT), str(source), '--requirements',
                            str(requirements), '--reference-root', str(root)],
                           check=True, capture_output=True)
            # 作業treeの変更は固定commitの照合結果を変えない。
            (root / 'src/tools/checker.js').write_text('working tree drift\n')
            inventory.validate_inventory(data, ACTIVE, reference_root=root)
            changed = copy.deepcopy(data)
            changed['files'][0]['blob_sha'] = 'd' * 40
            changed['tree_sha256'] = inventory.tree_digest(changed['files'])
            with self.assertRaisesRegex(ValueError, 'mismatching blob'):
                inventory.validate_inventory(changed, ACTIVE, reference_root=root)
            (root / 'src/tools/extra.rs').write_text('fn main() {}\n')
            git('add', '.')
            git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                '-c', 'commit.gpgsign=false', 'commit', '-qm', 'second reference fixture')
            data['revision'] = git('rev-parse', 'HEAD')
            with self.assertRaisesRegex(ValueError, 'missing/excess'):
                inventory.validate_inventory(data, ACTIVE, reference_root=root)


if __name__ == '__main__':
    unittest.main()
