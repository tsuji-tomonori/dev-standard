"""実generatorのprofile出力を品質portalのブラウザfixtureへ接続する。"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from test_api_errors import enrich_documents
from test_api_structure import ApiStructureTest, structure
from test_evidence_portal import evidence, fixture


def build(destination: Path):
    test = ApiStructureTest()
    test.setUp()
    try:
        enrich_documents(test)
        files = test.render()
        inputs = destination / 'input'
        inputs.mkdir(parents=True, exist_ok=True)
        for name, content in files.items():
            path = inputs / 'design' / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8')
        (inputs / 'design/other.html').write_text('<!doctype html><html lang="ja"><h1>運用設計</h1></html>')
        data = fixture()
        names = structure.names(test.model, test.op)
        data['design'] = {'applicable': True, 'items': [
            {'id': kind, 'name': kind, 'status': 'passed', 'hierarchy': ['items', 'getItem'], 'path': 'design/' + path[:-3] + '.html'}
            for kind, path in names.items()], 'files': ['design/' + name for name in files] + ['design/other.html']}
        data['design']['items'].extend([
            {'id': 'crud', 'name': 'CRUD対応', 'status': 'passed', 'hierarchy': ['保存先', 'CRUD'],
             'path': 'design/crud/index.gen.html', 'diagram': 'design/crud/diagram.gen.svg', 'download': 'design/crud/access.gen.csv'},
            {'id': 'operations', 'name': '運用設計', 'status': 'passed', 'hierarchy': ['運用'], 'path': 'design/other.html'},
        ])
        evidence.validate(data, 'abc')
        (inputs / 'report.json').write_text(json.dumps(data, ensure_ascii=False, indent=2))
        evidence.render(data, inputs, destination / 'site')
    finally:
        test.doCleanups()
        test.fixture.doCleanups()


if __name__ == '__main__':
    build(Path(sys.argv[1]))
