"""契約テスト用の小さな実検査。実アプリの意味検査成功を主張するfixtureではない。"""
import json
import os
import sys
from pathlib import Path


def validate_source(value):
    if not value.strip():
        raise ValueError('source is empty')


def validate_sample(request, response):
    if not isinstance(request, dict) or not request.get('name') or not isinstance(response, dict) or not response.get('id'):
        raise ValueError('concrete request/response pair is missing')


def source_positive():
    validate_source(Path('src/model.txt').read_text())


def source_negative():
    try:
        validate_source('')
    except ValueError:
        return
    raise AssertionError('empty source mutation was accepted')


def sample_positive():
    validate_sample({'name': 'example'}, {'id': 'example-id'})


def sample_negative():
    try:
        validate_sample('OpenAPIを参照', 'schemaに従う')
    except ValueError:
        return
    raise AssertionError('placeholder mutation was accepted')


cases = [source_positive, source_negative, sample_positive, sample_negative]
tests = []
for case in cases:
    try:
        case()
        status = 'pass'
    except (AssertionError, ValueError):
        status = 'fail'
    tests.append({'id': case.__name__, 'kind': case.__name__.rsplit('_', 1)[1],
                  'status': status, 'path': 'conformance.py', 'line': case.__code__.co_firstlineno})
report = {'schema_version': 1, 'source_digest': os.environ['DEV_STANDARD_SOURCE_DIGEST'],
          'tests': tests, 'rules': [
              {'id': 'RULE-SOURCE', 'status': 'pass', 'test_ids': ['source_positive', 'source_negative'], 'reason': ''},
              {'id': 'RULE-SAMPLE', 'status': 'pass', 'test_ids': ['sample_positive', 'sample_negative'], 'reason': ''}]}
mode = Path('conformance-mode.txt').read_text().strip()
if mode == 'no-report':
    sys.exit(0)
if mode == 'write-source':
    Path('src/model.txt').write_text('changed by checker')
if mode == 'stale':
    report['source_digest'] = '0' * 64
if mode == 'missing-negative':
    report['rules'][0]['test_ids'] = ['source_positive']
if mode == 'not-run':
    report['tests'][0]['status'] = 'not-run'
if mode == 'uncollected':
    report['rules'][0]['test_ids'] = ['not-collected']
if mode == 'missing-rule':
    report['rules'].pop()
if mode == 'fail':
    sys.exit(2)
Path(sys.argv[1]).write_text(json.dumps(report), encoding='utf-8')
print('fixture conformance: executed 4 real cases', flush=True)
