"""言語非依存のadapter出力fixtureを品質portalへ接続する。解析の正しさは検証しない。"""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

from test_evidence_portal import evidence, fixture


def build(destination: Path):
    inputs = destination / 'input'
    inputs.mkdir(parents=True, exist_ok=True)
    documents = {
        'detail': '<h2>正常系入力</h2><p>商品識別子を受け取る。</p>',
        'interface': '<h2>Headers</h2><h2>Path Parameters</h2>',
        'messages': '<h2>運用ログ</h2><p>モデル処理に失敗しました。</p><p>依存先の状態を確認し再試行する。</p>',
        'query': '<h2>SQL種別</h2><p>SELECT</p>',
        'sequence': '<h2>処理順序</h2><p>受付 → 商品取得 → 応答</p>',
        'unit-test': '<h2>前提（Given）</h2><p>商品Aが登録されている。</p><h2>操作（When）</h2><p>商品Aを取得する。</p><h2>期待結果（Then）</h2><p>商品Aの詳細を返す。</p>',
    }
    links = ''.join(f'<a href="{kind}.html">{kind}</a> ' for kind in documents)
    files = {}
    for kind, body in documents.items():
        files[f'design/items/getItem/{kind}.html'] = (
            '<!doctype html><html lang="ja"><meta charset="utf-8">'
            f'<title>{kind}</title><nav>{links}</nav><h1>{kind}</h1>{body}</html>')
    # 表・図・CSVは同じ言語非依存fixtureモデルから組み立てる。
    api, resource, access = 'getItem', 'inventory:items', 'R'
    files['design/crud/index.html'] = (
        '<!doctype html><html lang="ja"><meta charset="utf-8"><title>CRUD</title>'
        f'<h1>CRUD対応</h1><table><tr><th>API</th><th>{resource}</th></tr>'
        f'<tr><td>{api}</td><td>{access}</td></tr></table></html>')
    files['design/crud/access.csv'] = f'API,{resource}\n{api},{access}\n'
    label = html.escape(f'{api} → {access} → {resource}')
    files['design/crud/diagram.svg'] = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="640" height="90" viewBox="0 0 640 90">'
        '<rect x="1" y="1" width="638" height="88" fill="#eef5ff" stroke="#0757ae"/>'
        f'<text x="24" y="52" font-family="sans-serif" font-size="22">{label}</text></svg>')
    files['design/other.html'] = '<!doctype html><html lang="ja"><meta charset="utf-8"><h1>運用設計</h1></html>'
    for name, content in files.items():
        path = inputs / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
    data = fixture()
    data['design'] = {'applicable': True, 'items': [
        {'id': kind, 'name': kind, 'status': 'passed', 'hierarchy': ['items', 'getItem'],
         'path': f'design/items/getItem/{kind}.html'} for kind in documents], 'files': list(files)}
    data['design']['items'].extend([
        {'id': 'crud', 'name': 'CRUD対応', 'status': 'passed', 'hierarchy': ['保存先', 'CRUD'],
         'path': 'design/crud/index.html', 'diagram': 'design/crud/diagram.svg', 'download': 'design/crud/access.csv'},
        {'id': 'operations', 'name': '運用設計', 'status': 'passed', 'hierarchy': ['運用'], 'path': 'design/other.html'},
    ])
    evidence.validate(data, 'abc')
    (inputs / 'report.json').write_text(json.dumps(data, ensure_ascii=False, indent=2))
    evidence.render(data, inputs, destination / 'site')


if __name__ == '__main__':
    build(Path(sys.argv[1]))
