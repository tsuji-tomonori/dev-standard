"""参照適合を要件別に照合し、導入先の意味検査を新規実行する共通契約。

意味解析器ではない。trusted adapterの実test collector・正負例の結果を検査する。
一時reportは生成帳票と分離し、保存済みpassを再利用しない。
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path


def exact(value, keys: set[str], label: str) -> None:
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError(f'conformance {label}: fields mismatch')


def unique(values, label: str, empty: bool = False) -> set[str]:
    if (not isinstance(values, list) or (not values and not empty)
            or any(not isinstance(v, str) or not v.strip() for v in values)
            or len(set(values)) != len(values)):
        raise ValueError(f'conformance {label}: unique nonblank IDs required')
    return set(values)


def declared_sources(root: Path, data: dict, confined) -> set[str]:
    paths = set()
    for cap in data['capabilities'].values():
        if cap['status'] == 'required':
            for value in cap['sources']:
                path = confined(root, value)
                if path.is_dir():
                    paths.update(p.relative_to(root).as_posix() for p in path.rglob('*') if p.is_file())
                else:
                    paths.add(value)
    return paths


def source_digest(root: Path, data: dict, confined) -> str:
    """宣言sourceと適合判断の入力を共通側でハッシュ化する。未宣言sourceの検出はadapter責務。"""
    paths = {data['requirements'], data['conformance']['profile'], data['conformance']['mapping'], *data['reference_inventories']}
    for cap in data['capabilities'].values():
        if cap['status'] != 'required':
            continue
        for value in cap['sources']:
            path = confined(root, value)
            if path.is_dir():
                paths.update(p.relative_to(root).as_posix() for p in path.rglob('*') if p.is_file())
            else:
                paths.add(value)
    if 'api' in data:
        paths.add(data['api']['profile'])
    digest = hashlib.sha256()
    for value in sorted(paths):
        path = confined(root, value)
        digest.update(value.encode() + b'\0' + hashlib.sha256(path.read_bytes()).digest())
    digest.update(json.dumps(data, sort_keys=True, ensure_ascii=False).encode())
    return digest.hexdigest()


def prepare(root: Path, data: dict, assets: Path, confined, read_json) -> dict:
    """参照元の置換、要件の潰し込み、棚卸し集合の欠落を拒否する。"""
    config = data.get('conformance')
    exact(config, {'profile', 'mapping', 'check'}, 'configuration')
    command = config['check']
    if (not isinstance(command, list) or not command
            or any(not isinstance(v, str) or not v.strip() for v in command)
            or command.count('{report}') != 1):
        raise ValueError('conformance check argv requires exactly one {report} argument')
    profile = read_json(confined(root, config['profile']))
    exact(profile, {'schema_version', 'id', 'version', 'reference', 'rule_ids', 'advisory_rule_ids'}, 'profile')
    if type(profile['schema_version']) is not int or profile['schema_version'] != 1:
        raise ValueError('conformance profile version unsupported')
    unique([profile['id']], 'profile ID')
    unique([profile['version']], 'profile version')
    rules = unique(profile['rule_ids'], 'profile rules')
    advisory = unique(profile['advisory_rule_ids'], 'advisory rules', empty=True)
    if not advisory <= rules:
        raise ValueError('conformance advisory IDs outside profile')
    exact(profile['reference'], {'repository', 'revision'}, 'reference')
    if (not isinstance(profile['reference']['repository'], str) or not profile['reference']['repository'].strip()
            or not isinstance(profile['reference']['revision'], str)
            or len(profile['reference']['revision']) != 40
            or any(c not in '0123456789abcdef' for c in profile['reference']['revision'])):
        raise ValueError('conformance requires a fixed reference commit')
    canonical = read_json(assets / 'lazunex-conformance-v1.json')
    same_id = (profile['id'], profile['version']) == (canonical['id'], canonical['version'])
    if (same_id or profile['reference'] == canonical['reference']) and profile != canonical:
        raise ValueError('conformance cannot shrink or replace the pinned lazunex baseline')
    if 'api' in data and read_json(confined(root, data['api']['profile']))['reference'] != profile['reference']:
        raise ValueError('conformance/API profile reference mismatch')
    inventories = [read_json(confined(root, p)) for p in data['reference_inventories']]
    selected = [v for v in inventories if all(v.get(k) == val for k, val in profile['reference'].items())]
    if not selected:
        raise ValueError('conformance authoritative reference inventory missing (secondary references cannot replace it)')
    if profile['reference'] == canonical['reference']:
        blueprint = read_json(assets / 'reference-tools/lazunex-096e1e5.json')
        expected = {x['path']: x['blob_sha'] for x in blueprint['files']}
        if not any(v['source_root'] == blueprint['source_root'] and {x['path']: x['blob_sha'] for x in v['files']} == expected for v in selected):
            raise ValueError('conformance pinned reference tool set mismatch')
    mapping = read_json(confined(root, config['mapping']))
    exact(mapping, {'schema_version', 'reference', 'rules'}, 'mapping')
    if type(mapping['schema_version']) is not int or mapping['schema_version'] != 1 or mapping['reference'] != profile['reference']:
        raise ValueError('conformance mapping reference/version mismatch')
    if not isinstance(mapping['rules'], list):
        raise ValueError('conformance rules must be an array')
    local = {r['id']: r for r in read_json(confined(root, data['requirements']))['requirements'] if r['status'] == 'active'}
    mapped = {}
    criteria = set()
    for item in mapping['rules']:
        exact(item, {'id', 'status', 'requirement_id', 'acceptance_id', 'reason'}, 'rule mapping')
        if item['id'] in mapped or item['id'] not in rules:
            raise ValueError('conformance duplicate/unknown rule mapping')
        if item['status'] not in {'required', 'advisory', 'not-applicable'}:
            raise ValueError('conformance unsupported rule is incomplete')
        requirement = local.get(item['requirement_id'])
        if (requirement is None or item['requirement_id'] not in data['applicable_requirement_ids']
                or item['acceptance_id'] not in {c['id'] for c in requirement.get('acceptance_criteria', [])}):
            raise ValueError('conformance active target acceptance criterion missing')
        if not isinstance(item['reason'], str) or not item['reason'].strip():
            raise ValueError('conformance disposition requires a specific reason')
        key = item['requirement_id'], item['acceptance_id']
        if key in criteria:
            raise ValueError('conformance collapsed requirements: each reference rule needs a distinct acceptance criterion')
        criteria.add(key)
        if item['status'] != 'not-applicable':
            expected_status = 'advisory' if item['id'] in advisory else 'required'
            if item['status'] != expected_status:
                raise ValueError('conformance required/advisory disposition changed')
        mapped[item['id']] = item
    if set(mapped) != rules:
        raise ValueError('conformance missing reference rules')
    return {'rules': mapped, 'source_digest': source_digest(root, data, confined),
            'declared_sources': declared_sources(root, data, confined)}


def validate_result(root: Path, report: dict, prepared: dict, confined) -> dict:
    """意味検査を実行したtest単位と要件の対応を確認し、生成driftから推論しない。"""
    exact(report, {'schema_version', 'source_digest', 'tests', 'rules'}, 'execution report')
    if type(report['schema_version']) is not int or report['schema_version'] != 1 or report['source_digest'] != prepared['source_digest']:
        raise ValueError('conformance stale/wrong-source execution report')
    if not isinstance(report['tests'], list) or not isinstance(report['rules'], list):
        raise ValueError('conformance report tests/rules must be arrays')
    tests = {}
    for test in report['tests']:
        exact(test, {'id', 'kind', 'status', 'path', 'line'}, 'test result')
        unique([test['id']], 'test ID')
        if test['id'] in tests or test['kind'] not in {'positive', 'negative'}:
            raise ValueError('conformance duplicate test ID or unknown test kind')
        if test['status'] not in {'pass', 'fail', 'error', 'skipped', 'not-run'}:
            raise ValueError('conformance unknown test status')
        path = confined(root, test['path'])
        if test['path'] not in prepared['declared_sources']:
            raise ValueError('conformance test source is outside the hashed declared sources')
        if (type(test['line']) is not int or test['line'] < 1 or not path.is_file()
                or test['line'] > len(path.read_text(encoding='utf-8').splitlines())):
            raise ValueError('conformance test source location missing')
        tests[test['id']] = test
    observed = set()
    used_tests = set()
    counts = {'required': 0, 'advisory': 0, 'not_applicable': 0}
    advisory_results = []
    for item in report['rules']:
        exact(item, {'id', 'status', 'test_ids', 'reason'}, 'rule result')
        rule = prepared['rules'].get(item['id'])
        if rule is None or item['id'] in observed:
            raise ValueError('conformance duplicate/unknown rule result')
        observed.add(item['id'])
        if not isinstance(item['reason'], str):
            raise ValueError('conformance result reason must be text')
        ids = unique(item['test_ids'], 'test references', empty=True)
        if not ids <= tests.keys():
            raise ValueError('conformance references an uncollected test ID')
        used_tests.update(ids)
        if rule['status'] == 'not-applicable':
            if item['status'] != 'not-applicable' or item['reason'] != rule['reason']:
                raise ValueError('conformance not-applicable must match the reviewed requirement disposition')
            if {tests[i]['kind'] for i in ids} != {'positive', 'negative'} or any(tests[i]['status'] != 'pass' for i in ids):
                raise ValueError('conformance not-applicable requires executed applicability positive and negative tests')
            counts['not_applicable'] += 1
        elif rule['status'] == 'advisory':
            if item['status'] not in {'pass', 'fail', 'not-run'} or not item['reason'].strip():
                raise ValueError('conformance advisory result must be explicit')
            if item['status'] == 'pass' and (not ids or any(tests[i]['status'] != 'pass' for i in ids)):
                raise ValueError('conformance advisory pass contradicts test execution')
            counts['advisory'] += 1
            advisory_results.append({'id': item['id'], 'status': item['status'], 'reason': item['reason']})
        else:
            if item['status'] != 'pass' or {tests[i]['kind'] for i in ids} != {'positive', 'negative'}:
                raise ValueError('conformance required rule needs executed positive and negative tests')
            if any(tests[i]['status'] != 'pass' for i in ids):
                raise ValueError('conformance required test failed/skipped/not-run')
            counts['required'] += 1
    if observed != prepared['rules'].keys() or used_tests != tests.keys():
        raise ValueError('conformance incomplete rule/test correspondence')
    return {'status': 'pass', **counts, 'advisory_results': advisory_results,
            'source_digest': prepared['source_digest'], 'executed_test_count': sum(t['status'] in {'pass', 'fail', 'error'} for t in tests.values()),
            'not_run_test_count': sum(t['status'] in {'skipped', 'not-run'} for t in tests.values())}


def execute(root: Path, data: dict, prepared: dict, confined, read_json) -> dict:
    """新規一時fileへ一度だけ意味検査を実行する。shell/保存済みpass/欠落reportを使用しない。"""
    with tempfile.TemporaryDirectory(prefix='dev-standard-conformance-') as directory:
        report = Path(directory) / 'result.json'
        command = [str(report) if arg == '{report}' else arg for arg in data['conformance']['check']]
        env = {**os.environ, 'DEV_STANDARD_SOURCE_DIGEST': prepared['source_digest'], 'PYTHONDONTWRITEBYTECODE': '1'}
        result = subprocess.run(command, cwd=root, env=env, check=False, timeout=300)
        if result.returncode or not report.is_file() or report.is_symlink():
            raise ValueError('conformance command failed or did not produce a fresh report')
        return validate_result(root, read_json(report), prepared, confined)
