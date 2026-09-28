"""言語非依存CRUD v2。行列を正規表示、Mermaidを補助表示として射影する。"""
from __future__ import annotations

import csv
import html
import io
import json

ORDER = 'CRUD'


def unique_strings(values, label: str, *, empty: bool = False) -> list[str]:
    """ID集合の型・重複・空白を検査する。"""
    if (not isinstance(values, list) or (not values and not empty)
            or any(not isinstance(v, str) or not v.strip() for v in values)
            or len(set(values)) != len(values)):
        raise ValueError(f'CRUD {label}: unique nonblank strings required')
    return values


def validate(model: dict) -> None:
    """未使用資源を含む母集合と、根拠付き関係を別々に保持する。"""
    if (set(model) != {'schema_version', 'operations', 'resources', 'rows', 'no_access', 'unresolved'}
            or type(model['schema_version']) is not int or model['schema_version'] != 2):
        raise ValueError('CRUD matrix requires model schema_version 2')
    ops = set(unique_strings(model['operations'], 'operations'))
    if not isinstance(model['resources'], list) or not isinstance(model['rows'], list):
        raise ValueError('CRUD resources/rows must be arrays')
    resources = set()
    group_kinds = {}
    for item in model['resources']:
        if not isinstance(item, dict) or set(item) != {'id', 'group', 'kind'}:
            raise ValueError('CRUD resource requires id/group/kind')
        unique_strings([item['id']], 'resource ID')
        unique_strings([item['group']], 'resource group')
        if item['kind'] not in {'database', 'external'}:
            raise ValueError('CRUD resource kind must be database or external')
        if item['id'] in resources:
            raise ValueError('CRUD duplicate resource ID; qualify cross-store names')
        if group_kinds.setdefault(item['group'], item['kind']) != item['kind']:
            raise ValueError('CRUD group cannot mix database and external resources')
        resources.add(item['id'])
    seen = set()
    accessed = set()
    for row in model['rows']:
        if not isinstance(row, dict) or set(row) != {'operation', 'resource', 'access', 'evidence'}:
            raise ValueError('CRUD row fields mismatch')
        pair = row['operation'], row['resource']
        if pair in seen or pair[0] not in ops or pair[1] not in resources:
            raise ValueError('CRUD duplicate or unknown operation/resource')
        seen.add(pair)
        accessed.add(pair[0])
        access = set(unique_strings(row['access'], 'access'))
        if not access <= set(ORDER):
            raise ValueError('CRUD access must be C/R/U/D')
        evidence = row['evidence']
        if not isinstance(evidence, list) or not evidence:
            raise ValueError('CRUD evidence is required')
        roles = set()
        for source in evidence:
            if (not isinstance(source, dict) or set(source) != {'path', 'line', 'role'}
                    or not isinstance(source['path'], str) or not source['path'].strip()
                    or type(source['line']) is not int or source['line'] < 1
                    or source['role'] not in {'read', 'write'}):
                raise ValueError('CRUD invalid evidence location/role')
            roles.add(source['role'])
        expected = ({'read'} if 'R' in access else set()) | ({'write'} if access & set('CUD') else set())
        if roles != expected:
            raise ValueError('CRUD evidence must distinguish read/write')
    if (not isinstance(model['no_access'], dict)
            or set(model['no_access']) != ops - accessed
            or any(not isinstance(v, str) or not v.strip() for v in model['no_access'].values())):
        raise ValueError('CRUD no_access must cover only actual no-access operations')
    if model['unresolved'] != []:
        raise ValueError('CRUD unresolved access is incomplete, not no-access')


def cell(value: str) -> str:
    return html.escape(value, quote=False).replace('|', '&#124;').replace('\r', '&#13;').replace('\n', '&#10;')


def matrix(model: dict, resources: list[str]) -> dict[str, bytes]:
    """C/R/U/Dをセル内で集約し、未使用列とアクセスなし行を落とさない。"""
    cells = {(r['operation'], r['resource']): set(r['access']) for r in model['rows']}
    rows = [['api', *resources]]
    for op in sorted(model['operations']):
        rows.append([op, *[''.join(c for c in ORDER if c in cells.get((op, resource), set())) for resource in resources]])
    stream = io.StringIO(newline='')
    csv.writer(stream, lineterminator='\n').writerows(rows)
    table = [rows[0], ['---'] * len(rows[0]), *rows[1:]]
    return {'csv': stream.getvalue().encode(),
            'table': ('\n'.join('| ' + ' | '.join(cell(c) for c in row) + ' |' for row in table) + '\n').encode()}


def groups(model: dict) -> dict[str, dict[str, bytes]]:
    validate(model)
    return {group: matrix(model, sorted(r['id'] for r in model['resources'] if r['group'] == group))
            for group in sorted({r['group'] for r in model['resources']})}


def renderings(model: dict) -> dict[str, bytes]:
    validate(model)
    resources = sorted(r['id'] for r in model['resources'])
    result = matrix(model, resources)
    ops = {op: f'a{i}' for i, op in enumerate(sorted(model['operations']))}
    nodes = {r: f'r{i}' for i, r in enumerate(resources)}

    def label(value: str) -> str:
        return json.dumps(cell(value).replace('"', '&quot;'), ensure_ascii=False)

    lines = ['```mermaid', 'flowchart LR']
    lines += [f'  {node}[{label(op)}]' for op, node in ops.items()]
    for index, group in enumerate(sorted({r['group'] for r in model['resources']})):
        lines += [f'  subgraph g{index}[{label(group)}]']
        lines += [f'    {nodes[r["id"]]}[{label(r["id"])}]' for r in sorted(model['resources'], key=lambda r: r['id']) if r['group'] == group]
        lines += ['  end']
    for row in sorted(model['rows'], key=lambda r: (r['operation'], r['resource'])):
        op, resource = ops[row['operation']], nodes[row['resource']]
        if 'R' in row['access']:
            lines += [f'  {resource} -->|R| {op}']
        writes = ''.join(c for c in 'CUD' if c in row['access'])
        if writes:
            lines += [f'  {op} -->|{writes}| {resource}']
    lines += ['```', '', 'R: 資源からAPIへの参照。C/U/D: APIから資源への変更。ER関係を表す図ではない。', '', '## アクセスなし', '']
    lines += [f'- {cell(op)}: {cell(reason)}' for op, reason in sorted(model['no_access'].items())] or ['該当なし。']
    result['diagram'] = ('\n'.join(lines) + '\n').encode()
    # 集合の順序は入力順に依存させない。根拠の内容自体は推測・補完しない。
    normalized = [{**row, 'access': [c for c in ORDER if c in row['access']],
                   'evidence': sorted(row['evidence'], key=lambda e: (e['path'], e['line'], e['role']))}
                  for row in sorted(model['rows'], key=lambda r: (r['operation'], r['resource']))]
    result['evidence'] = (json.dumps(normalized, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode()
    return result
