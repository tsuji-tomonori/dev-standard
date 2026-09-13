#!/usr/bin/env python3
"""API構成profileの共通renderer・章検査・実装由来CRUD。"""
from __future__ import annotations

import ast
import csv
import hashlib
import html
import io
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

PROFILE = Path(__file__).resolve().parent.parent / 'assets/api-structure-lazunex-v1.json'


def profile():
    """固定参照の構造だけを読み、サービス固有の内容は取り込まない。"""
    if PROFILE.is_symlink():
        raise ValueError('symlink profile')
    return json.loads(PROFILE.read_text(encoding='utf-8'))


def cell(value):
    return html.escape(str(value), quote=True).replace('|', '&#124;').replace('\n', '<br>')


def table(rows, fields):
    if not rows:
        return '該当なし（対象モデルに項目なし）。\n'
    return '| ' + ' | '.join(fields.values()) + ' |\n|' + '---|' * len(fields) + '\n' + ''.join(
        '| ' + ' | '.join(cell(row.get(key, '')) for key in fields) + ' |\n' for row in rows)


def block(value):
    # code fenceをモデル文字列で終了させない。
    content = json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2)
    return '<pre>' + html.escape(content) + '</pre>\n'


def segment(value):
    if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', value) or value in {'.', '..'}:
        raise ValueError(f'group/API/filename requires safe path segment: {value}')
    return value


def names(model, operation):
    chosen = model.get('document_names', {})
    p = profile()
    if set(chosen) - set(p['documents']):
        raise ValueError('unknown document kind in placement policy')
    prefix = f'{segment(operation.get("group"))}/{segment(operation.get("slug"))}'
    result = {kind: f'{prefix}/{segment(chosen.get(kind, spec["filename"]))}' for kind, spec in p['documents'].items()}
    if len(set(result.values())) != 6 or any(not n.endswith('.md') for n in result.values()):
        raise ValueError('six distinct Markdown names required')
    return result


def sections(markdown):
    """fence内の見出し例は構成として数えない。"""
    result, fence = [], None
    for line in markdown.splitlines():
        marker = re.match(r'^\s*(`{3,}|~{3,})', line)
        if marker:
            char, length = marker[1][0], len(marker[1])
            if fence is None:
                fence = (char, length)
            elif char == fence[0] and length >= fence[1]:
                fence = None
            continue
        if fence:
            continue
        match = re.match(r'^(#{1,6})\s+(.+?)\s*$', line)
        if match:
            result.append([len(match[1]), match[2], []])
        elif result:
            result[-1][2].append(line)
    return result


def validate_document(kind, text, operation):
    spec = profile()['documents'][kind]
    parsed = sections(text)
    if len([row for row in parsed if row[0] == 1]) != 1:
        raise ValueError(f'{kind}: exactly one title required')
    expected = spec['chapters'][:]
    if kind == 'query':
        expected = [cell(q['id']) for q in operation['queries']] or [spec['empty_heading']]
    actual = [row[1] for row in parsed if row[0] == 2]
    if actual != expected:
        raise ValueError(f'{kind}: chapter order/missing/duplicate: {actual} != {expected}')
    for level, heading, body in parsed:
        if level == 2 and not any(line.strip() for line in body) and kind not in {'query', 'messages', 'unit-test'}:
            raise ValueError(f'{kind}: empty required section: {heading}')
    if kind == 'query':
        for query in operation['queries']:
            start = next(i for i, row in enumerate(parsed) if row[:2] == [2, cell(query['id'])])
            children = []
            for level, heading, body in parsed[start + 1:]:
                if level <= 2:
                    break
                if level == 3:
                    if not any(line.strip() for line in body):
                        raise ValueError(f'query: empty SQL section: {heading}')
                    children.append(heading)
            if children != spec['repeat']['children']:
                raise ValueError('query: missing/duplicate/reordered SQL subsections')
        if not operation['queries'] and operation['no_queries_reason'] not in text:
            raise ValueError('query: concrete not-applicable reason missing')
    if kind in {'messages', 'unit-test'}:
        repeat = spec['repeat']
        start = next(i for i, row in enumerate(parsed) if row[:2] == [2, repeat['under']])
        repeats = []
        for level, heading, body in parsed[start + 1:]:
            if level <= 2:
                break
            if level == 3:
                repeats.append(heading)
                if not any(line.strip() for line in body):
                    raise ValueError(f'{kind}: empty repeated section')
        if repeats != [cell(item['id']) for item in operation[repeat['source']]]:
            raise ValueError(f'{kind}: missing/reordered repeated sections')
        if kind == 'messages':
            for message in operation['messages']:
                position = next(i for i, row in enumerate(parsed) if row[:2] == [3, cell(message['id'])])
                children = []
                for level, title, body in parsed[position+1:]:
                    if level <= 3:
                        break
                    if level == 4:
                        if not any(line.strip() for line in body):
                            raise ValueError('messages: empty required detail child')
                        children.append(title)
                if children != repeat['children']:
                    raise ValueError('messages: missing/duplicate/reordered detail children')
        if kind == 'unit-test':
            position = next(i for i, row in enumerate(parsed) if row[:2] == [2, '1. 要因ごとの要素'])
            factors = []
            for level, title, body in parsed[position+1:]:
                if level <= 2:
                    break
                if level == 3:
                    factors.append(title)
                    if not any(line.strip() for line in body):
                        raise ValueError('unit-test: empty factor')
            if factors != [cell(f['id']) + ' ' + cell(f['name']) for f in operation['factors']]:
                raise ValueError('unit-test: missing/reordered factors')
        if repeats != [cell(item['id']) for item in operation[repeat['source']]]:
            raise ValueError(f'{kind}: missing/reordered repeated sections')
    if kind == 'sequence' and '```mermaid\nsequenceDiagram\n' not in text:
        raise ValueError('sequence: missing Mermaid sequence')


def check_links(files):
    """生成範囲内のMarkdown相対linkを解決し、索引移動時の断絶を拒否する。"""
    import posixpath
    for name, content in files.items():
        if not name.endswith('.md'):
            continue
        for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)', content):
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target = posixpath.normpath(posixpath.join(posixpath.dirname(name), unquote(parsed.path)))
            if target not in files:
                raise ValueError(f'broken document link: {name} -> {link}')


def validate_structure(files, model, document):
    if model.get('structure_profile') != 'lazunex-v1':
        raise ValueError('unsupported structure_profile')
    exported = {op['operationId'] for item in document['paths'].values() for method, op in item.items()
                if method in {'get', 'post', 'put', 'patch', 'delete', 'options', 'head', 'trace'}}
    ops = model['operations']
    if len(ops) != len(exported) or {op['id'] for op in ops} != exported:
        raise ValueError('structure operation inventory differs from OpenAPI')
    expected, prefixes = set(), set()
    for operation in ops:
        paths = names(model, operation)
        prefix = str(Path(next(iter(paths.values()))).parent)
        if prefix in prefixes:
            raise ValueError('multiple operations share a document directory')
        prefixes.add(prefix)
        expected.update(paths.values())
        expected.update([f'{operation["group"]}/index.gen.md', f'{prefix}/index.gen.md'])
        for kind, name in paths.items():
            if name not in files:
                raise ValueError(f'missing document: {name}')
            validate_document(kind, files[name], operation)
    expected.add('API_DOCUMENTS.gen.md')
    actual = {name for name in files if name.endswith('.md') and not name.startswith('crud/')}
    if actual != expected:
        raise ValueError(f'old or missing document outputs: {sorted(actual ^ expected)}')
    check_links(files)


def render(model, document):
    """検証済み意味モデルから固定profileの章を組み立てる。"""
    files, groups = {}, {}
    exported = {op['operationId']: (method, path, item, op) for path, item in document['paths'].items()
                for method, op in item.items() if method in {'get', 'post', 'put', 'patch', 'delete', 'options', 'head', 'trace'}}
    for op in model['operations']:
        paths = names(model, op)
        method, path, path_item, interface = exported[op['id']]
        heading = f'# {cell(op["id"])} — {method.upper()} {cell(path)}\n\n'
        heading += f'実装根拠: `{cell(op["source"]["path"])}:{op["source"]["line"]}`\n\n'
        navigation = '[API一覧](../../API_DOCUMENTS.gen.md) / [グループ](../index.gen.md) / [API](index.gen.md)\n\n'
        navigation += ' | '.join(f'[{kind}]({Path(name).name})' for kind, name in paths.items()) + '\n\n'
        def chapter(title, content):
            return f'## {title}\n\n{content}\n'
        def rows(key, columns):
            return table(op[key], columns) if op[key] else op[f'no_{key}_reason'] + '\n'
        detail = chapter('1. 正常系入力', rows('inputs', {'origin': 'Location', 'name': 'Name', 'type': 'Type', 'description': '説明'}))
        detail += chapter('2. 正常系前提', cell(op['preconditions']))
        changed = [r for r in op['resources'] if r['action'].upper() not in {'R', 'READ', 'SELECT', '参照', '読取', '読み取り'}]
        detail += chapter('3. 正常系リソース変更', table(changed, {'database': '保存先', 'table': 'リソース', 'action': '操作', 'condition': '条件', 'source': '根拠'})
                          if changed else '実装モデルに正常系で作成・更新・削除するリソースはありません。')
        detail += chapter('4. 正常系レスポンス', rows('outputs', {'name': '項目', 'type': '型', 'description': '説明', 'origin': '値の取得元'}))
        files[paths['detail-design']] = heading + navigation + detail
        parameters = {}
        for parameter in [*path_item.get('parameters', []), *interface.get('parameters', [])]:
            if '$ref' in parameter:
                ref = parameter['$ref']
                if not ref.startswith('#/'):
                    raise ValueError('resolve external OpenAPI parameter references in adapter')
                parameter = document
                for key in ref[2:].split('/'):
                    parameter = parameter[key.replace('~1', '/').replace('~0', '~')]
            parameters[(parameter['in'], parameter['name'])] = parameter
        view = ''
        for label, location in [('Headers', 'header'), ('Path Parameters', 'path'), ('Query Parameters', 'query')]:
            selected = [p for (loc, _), p in parameters.items() if loc == location]
            view += chapter(label, block(selected) if selected else f'該当なし（OpenAPIに{location}入力なし）。')
        view += chapter('Data', block(interface['requestBody']) if 'requestBody' in interface else '該当なし（OpenAPIにrequestBodyなし）。')
        view += chapter('Responses', block({'responses': interface['responses'], 'components': document.get('components', {})}))
        samples = op.get('samples', [])
        view += chapter('Samples', block(samples) if samples else cell(op['no_samples_reason']))
        files[paths['interface']] = heading + navigation + view
        messages = chapter('API', cell(op['summary'])) + chapter('生成・検証方針', '対象実装モデルのログを表示します。参照サービスのログや検証結果は転記しません。')
        messages += chapter('メッセージ一覧', rows('messages', {'id': 'ID', 'level': 'レベル', 'template': '本文'}))
        logs = ''
        for message in op['messages']:
            logs += f'### {cell(message["id"])}\n\n' + block({key: value for key, value in message.items() if key != 'fields'})
            logs += '\n#### 出力項目\n\n' + (table(message['fields'], {'name': '項目', 'type': '型', 'description': '説明', 'masking': 'マスク'})
                                                       if message['fields'] else cell(message['no_fields_reason'])) + '\n'
        messages += chapter('ログ詳細', logs or cell(op['no_messages_reason']))
        messages += chapter('strict検証で要求する項目', 'ログID・出力条件・項目・マスク・実装根拠を意味モデルで検査します。実行結果は別途検証します。')
        files[paths['messages']] = heading + navigation + messages
        query_text = ''
        for query in op['queries']:
            query_text += f'## {cell(query["id"])}\n\n'
            values = [query['kind'], query['summary'], {'database': query['database'], 'table': query['table'], 'source': query['source']},
                      query['arguments'] or query['no_arguments_reason'], query['returns'], query['conditions']]
            for title, value in zip(profile()['documents']['query']['repeat']['children'], values):
                query_text += f'### {title}\n\n{block(value)}\n'
        files[paths['query']] = heading + navigation + (query_text or chapter('該当なし', cell(op['no_queries_reason'])))
        files[paths['sequence']] = heading + navigation + '```mermaid\n' + op['sequence'].rstrip() + '\n```\n'
        if 'exception_paths' in op:
            exceptions = table(op['exception_paths'], {'exception': '例外型', 'outcome': '捕捉・継続', 'status': 'HTTP status',
                               'code': 'code', 'message': '安全な応答', 'log_id': 'ログID', 'level': 'レベル',
                               'operator_action': '確認・復旧', 'source': '例外根拠', 'response_source': '応答根拠'})
            files[paths['sequence']] += '\n例外応答と運用ログの対応\n\n' + exceptions
            files[paths['messages']] += '\n例外応答との対応\n\n' + exceptions
        tests = chapter('0. Router層の暗黙処理', cell(op['router_implicit']))
        factors = ''.join(f'### {cell(f["id"])} {cell(f["name"])}\n\n' + table(f['elements'], {'id': '要素', 'description': '説明', 'expected': '期待結果'}) + '\n' for f in op['factors'])
        tests += chapter('1. 要因ごとの要素', factors)
        tests += chapter('2. 直積したテストケース一覧', '以下は対象実装で対応付けたケースです。未実装の直積全組合せを網羅したとは扱いません。\n\n' +
                         table(op['cases'], {'id': 'ケース', 'covers': '要因・要素', 'tests': '実在テスト'}))
        details = ''
        for case in op['cases']:
            details += f'### {cell(case["id"])}\n\n'
            if 'verification_units' in case:
                details += table(case['verification_units'],
                    {'given': '前提（Given）', 'when': '操作（When）', 'then': '期待結果（Then）', 'test': 'テスト根拠'})
                details += '\n期待ログ: ' + cell(case['expected_logs']) + '\n\n期待データ: ' + cell(case['expected_data']) + '\n\n'
            else:
                details += block(case) + '\n'
        tests += chapter('3. テスト詳細', details)
        files[paths['unit-test']] = heading + navigation + tests
        prefix = f'{op["group"]}/{op["slug"]}'
        files[f'{prefix}/index.gen.md'] = heading + navigation
        groups.setdefault(op['group'], []).append((op['slug'], op['id']))
    for group, ops in sorted(groups.items()):
        files[f'{group}/index.gen.md'] = f'# {cell(group)}\n\n[API一覧](../API_DOCUMENTS.gen.md)\n\n' + ''.join(
            f'- [{cell(identity)}]({slug}/index.gen.md)\n' for slug, identity in sorted(ops))
    files['API_DOCUMENTS.gen.md'] = '# API生成帳票一覧\n\n' + ''.join(f'- [{cell(group)}]({group}/index.gen.md)\n' for group in sorted(groups))
    files['OPENAPI.gen.json'] = json.dumps({**document, 'x-generated-notice': 'AUTO-GENERATED. DO NOT EDIT DIRECTLY.'}, ensure_ascii=False, indent=2) + '\n'
    validate_structure(files, model, document)
    return files


def sql_accesses(sql):
    """SQL ASTの更新対象と実table参照を区別する。CTE名は保存先にしない。"""
    import sqlglot
    from sqlglot import exp
    from sqlglot.optimizer.scope import traverse_scope
    statements = sqlglot.parse(sql)
    if len(statements) != 1 or not isinstance(statements[0], (exp.Select, exp.Union, exp.Insert, exp.Update, exp.Delete)):
        raise ValueError('unsupported CRUD SQL statement')
    statement = statements[0]
    action = {exp.Insert: 'C', exp.Update: 'U', exp.Delete: 'D'}.get(type(statement))
    target = statement.this if action else None
    if isinstance(target, exp.Schema):
        target = target.this
    if action and not isinstance(target, exp.Table):
        raise ValueError('unsupported SQL write target')
    def identity(table):
        return '.'.join(part for part in [table.catalog, table.db, table.name] if part)
    cte_refs = {id(source) for scope in traverse_scope(statement) for _, (source, resolved) in scope.selected_sources.items() if not isinstance(resolved, exp.Table)}
    records = set()
    if target is not None:
        records.add((identity(target), action))
    for table_node in statement.find_all(exp.Table):
        if table_node is target or id(table_node) in cte_refs:
            continue
        records.add((identity(table_node), 'R'))
    return sorted(records)


def crud(model, root, index):
    """到達する呼出しとSQL正本を照合し、全表示形式用のモデルを一度だけ作る。"""
    records, empty = [], []
    for operation in model['operations']:
        module = index.module_for(operation['source']['path'])
        candidates = [symbol for symbol, node in index.defs.items() if index.owner_module(symbol) == module
                      and node.lineno <= operation['source']['line'] <= node.end_lineno and hasattr(node, 'args')]
        if len(candidates) != 1:
            raise ValueError(f'CRUD requires an unambiguous handler source: {operation["id"]}')
        reachable = index.reachable(candidates[0])
        accesses = operation.get('accesses')
        if not isinstance(accesses, list):
            raise ValueError('profile requires explicit access inventory (including empty)')
        if operation.get('unresolved_accesses'):
            raise ValueError(f'unresolved dynamic accesses: {operation["id"]}')
        if not accesses:
            reason = operation.get('no_access_reason')
            if not isinstance(reason, str) or not reason.strip():
                raise ValueError('no access requires implementation reason')
            empty.append({'operation': operation['id'], 'reason': reason})
        seen = set()
        non_access = set()
        for disposition in operation.get('non_access_calls', []):
            mod, call = index.call_at(disposition['source'], reachable)
            if (index.resolve(mod, ast.unparse(call.func)) != disposition.get('symbol')
                    or not disposition.get('reason') or not disposition.get('adapter')):
                raise ValueError('non-access call requires adapter, reason and exact binding')
            non_access.add((disposition['source']['path'], disposition['source']['line']))
        for access in accesses:
            module, call = index.call_at(access['source'], reachable)
            destination = access['store']
            if not isinstance(destination, str) or not destination.strip() or access.get('phase') != 'runtime':
                raise ValueError('CRUD accepts named runtime stores only')
            source = access['source']
            marker = (source['path'], source['line'])
            seen.add(marker)
            if 'sql' in access:
                sql_path = access['sql']
                from_path = root / sql_path
                if (not isinstance(sql_path, str) or Path(sql_path).is_absolute() or any(part in {'', '.', '..'} for part in sql_path.split('/'))
                        or any(path.is_symlink() for path in (from_path, *from_path.parents)) or not from_path.resolve().is_relative_to(root.resolve())):
                    raise ValueError('unsafe CRUD SQL source')
                actual_sql = from_path.read_text(encoding='utf-8')
                strings = {n.value for n in ast.walk(call) if isinstance(n, ast.Constant) and isinstance(n.value, str)}
                # SQL本文または所有先を含むpathが実呼出しに渡る静的範囲。
                if sql_path not in strings and actual_sql.strip().rstrip(';') not in {s.strip().rstrip(';') for s in strings}:
                    raise ValueError(f'SQL source not bound to reachable call: {sql_path}')
                pairs = sql_accesses(actual_sql)
                provenance = {'path': sql_path, 'sha256': hashlib.sha256(actual_sql.encode()).hexdigest()}
            else:
                # サービスadapterは実call symbolとresource/actionを明示する。
                symbol = index.resolve(module, ast.unparse(call.func))
                if symbol != access.get('symbol') or access.get('action') not in {'C', 'R', 'U', 'D'}:
                    raise ValueError('non-SQL adapter binding/action mismatch')
                if not access.get('resource') or not access.get('adapter'):
                    raise ValueError('non-SQL access requires resource and adapter identity')
                pairs = [(access['resource'], access['action'])]
                provenance = {'symbol': symbol, 'adapter': access['adapter']}
            for resource, action in pairs:
                records.append({'operation': operation['id'], 'store': destination, 'resource': resource,
                                'action': action, 'source': source, 'extraction': provenance})
        # 明示された永続化callの欠落をアクセスなしと偽らない。
        for symbol in reachable:
            for node in index.nodes(symbol):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, (ast.Call, ast.Subscript, ast.Lambda)):
                        raise ValueError(f'unsupported dynamic access call: {operation["id"]}:{node.lineno}')
                    if isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Call):
                        receiver = ast.unparse(node.func.value.func).split('.')[-1]
                        supported = (receiver in {'execute', 'executemany'} and node.func.attr in {'fetchone', 'fetchall'}) or (
                            receiver == 'getLogger' and node.func.attr in {'info', 'debug', 'warning', 'error', 'exception', 'critical'})
                        if not supported:
                            raise ValueError(f'unsupported dynamic receiver: {operation["id"]}:{node.lineno}')
                    name = ast.unparse(node.func).split('.')[-1]
                    marker = (index.paths[index.owner_module(symbol)], node.lineno)
                    resolved = index.resolve(index.owner_module(symbol), ast.unparse(node.func))
                    pure = isinstance(node.func, ast.Name) and node.func.id in {
                        'dict', 'list', 'tuple', 'set', 'frozenset', 'str', 'int', 'float', 'bool', 'len', 'min', 'max', 'sum', 'sorted', 'range', 'enumerate', 'zip', 'isinstance'}
                    logging = resolved.startswith('logging.') or (isinstance(node.func, ast.Attribute)
                        and isinstance(node.func.value, ast.Call) and ast.unparse(node.func.value.func).endswith('logging.getLogger'))
                    fetched = isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Call) and node.func.attr in {'fetchone', 'fetchall'}
                    if resolved not in index.defs and not (pure or logging or fetched) and marker not in seen | non_access:
                        raise ValueError(f'unmapped persistence or unresolved external call requires adapter disposition: {marker}')
                    if name in {'execute', 'executemany', 'put_object', 'get_object', 'delete_object', 'upsert', 'query', 'scan'}:
                        marker = (index.paths[index.owner_module(symbol)], node.lineno)
                        if marker not in seen:
                            raise ValueError(f'unmapped persistence call: {marker}')
    return {'schema_version': 1, 'notice': 'AUTO-GENERATED. DO NOT EDIT DIRECTLY.',
            'scope': 'reachable static calls; other dynamic/service behavior requires target adapter',
            'operations': sorted(op['id'] for op in model['operations']),
            'accesses': sorted(records, key=lambda r: (r['operation'], r['store'], r['resource'], r['action'], r['source']['path'], r['source']['line'])),
            'no_access': sorted(empty, key=lambda row: row['operation'])}


def render_crud(data):
    """CSV・表・Mermaid図・JSON証拠を同じ集合から生成する。"""
    output = {'crud/model.gen.json': json.dumps(data, ensure_ascii=False, indent=2) + '\n'}
    resources = sorted({(r['store'], r['resource']) for r in data['accesses']})
    records = {(op, store, resource): ''.join(a for a in 'CRUD' if any(
        r['operation'] == op and r['store'] == store and r['resource'] == resource and r['action'] == a for r in data['accesses']))
        for op in data['operations'] for store, resource in resources}
    buffer = io.StringIO(newline='')
    writer = csv.writer(buffer, lineterminator='\n')
    def csv_cell(value):
        return "'" + value if value.lstrip().startswith(('=', '+', '-', '@', '\t', '\r', '\n')) else value
    writer.writerow(['API', *[csv_cell(f'{store}:{resource}') for store, resource in resources]])
    for op in data['operations']:
        writer.writerow([csv_cell(op), *[records[(op, store, resource)] or '-' for store, resource in resources]])
    output['crud/access.gen.csv'] = buffer.getvalue()
    lines = ['flowchart LR']
    for number, op in enumerate(data['operations']):
        lines.append(f'  A{number}["{cell(op)}"]')
    for number, (store, resource) in enumerate(resources):
        lines.append(f'  R{number}["{cell(store)}: {cell(resource)}"]')
    for ai, op in enumerate(data['operations']):
        for ri, (store, resource) in enumerate(resources):
            if records[(op, store, resource)]:
                lines.append(f'  A{ai} -->|{records[(op, store, resource)]}| R{ri}')
    markdown = '# API × リソース CRUD\n\n[API一覧](../API_DOCUMENTS.gen.md) · [CSV取得](access.gen.csv) · [抽出根拠](model.gen.json)\n\n'
    markdown += table(data['accesses'], {'operation': 'API', 'store': '保存先', 'resource': 'リソース', 'action': 'CRUD', 'source': '根拠'})
    markdown += '\n## アクセスなし\n\n' + table(data['no_access'], {'operation': 'API', 'reason': '理由'})
    markdown += '\n## CRUD図\n\n```mermaid\n' + '\n'.join(lines) + '\n```\n'
    output['crud/index.gen.md'] = markdown
    height = max(160, 70 * max(len(data['operations']), len(resources)) + 40)
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{height}" viewBox="0 0 1000 {height}" role="img" aria-label="APIと保存先のCRUD対応図">',
           '<rect width="100%" height="100%" fill="white"/>']
    for ai, op in enumerate(data['operations']):
        for ri, (store, resource) in enumerate(resources):
            action = records[(op, store, resource)]
            if action:
                y1, y2 = 50 + ai * 70, 50 + ri * 70
                svg.append(f'<path d="M320 {y1} L640 {y2}" stroke="#326090" fill="none"/>')
                svg.append(f'<text x="450" y="{(y1+y2)//2-5}" font-family="sans-serif" font-size="15">{action}</text>')
    for x, labels in [(15, data['operations']), (645, [f'{store}: {resource}' for store, resource in resources])]:
        for number, label in enumerate(labels):
            y = 50 + number * 70
            svg.append(f'<rect x="{x}" y="{y-23}" width="300" height="46" rx="6" fill="#eef4fc" stroke="#326090"/>')
            svg.append(f'<text x="{x+10}" y="{y+5}" font-family="sans-serif" font-size="15">{html.escape(label)}</text>')
    svg.append('</svg>')
    output['crud/diagram.gen.svg'] = '\n'.join(svg) + '\n'
    return output


def html_views(files):
    """本rendererのMarkdownを閲覧用HTMLへ変換する。任意HTMLは実行しない。"""
    outputs = {}
    for name, markdown in files.items():
        if not name.endswith('.md'):
            continue
        body, fence, pre, table_open = [], False, False, False
        for line in markdown.splitlines():
            if line.startswith('```'):
                fence = not fence
                body.append('<pre><code>' if fence else '</code></pre>')
                continue
            if fence:
                body.append(html.escape(line) + '\n')
                continue
            if line.startswith('<pre>'):
                pre = True
                line = line[5:]
                body.append('<pre>')
            if pre:
                closing = line.endswith('</pre>')
                body.append(html.escape(html.unescape(line[:-6] if closing else line)) + '\n')
                if closing:
                    body.append('</pre>')
                    pre = False
                continue
            def inline(value):
                # 生成済みの相対linkだけをHTMLへ移す。
                parts, cursor = [], 0
                for match in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', value):
                    parts.append(html.escape(html.unescape(value[cursor:match.start()])))
                    target = match[2]
                    if urlsplit(target).scheme not in {'', 'https', 'http'}:
                        raise ValueError('unsafe generated link')
                    if target.endswith('.md'):
                        target = target[:-3] + '.html'
                    parts.append(f'<a href="{html.escape(target, quote=True)}">{html.escape(html.unescape(match[1]))}</a>')
                    cursor = match.end()
                parts.append(html.escape(html.unescape(value[cursor:])))
                return ''.join(parts)
            if line.startswith('|'):
                if not table_open:
                    table_open = True
                    body.append('<table>')
                if not re.fullmatch(r'[| :\-]+', line):
                    body.append('<tr>' + ''.join(f'<td>{inline(value.strip())}</td>' for value in line.strip('|').split('|')) + '</tr>')
                continue
            if table_open:
                body.append('</table>')
                table_open = False
            match = re.match(r'^(#{1,6}) (.+)$', line)
            if match:
                level = len(match[1])
                body.append(f'<h{level}>{inline(match[2])}</h{level}>')
            elif line.strip():
                body.append('<p>' + inline(line) + '</p>')
        if table_open:
            body.append('</table>')
        if name == 'crud/index.gen.md':
            body.insert(1, '<img src="diagram.gen.svg" alt="APIと保存先のCRUD対応図">')
        outputs[name[:-3] + '.html'] = ('<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width">'
                                       '<title>API設計</title><style>body{font:16px system-ui;max-width:1100px;margin:auto;padding:24px} '
                                       'table{border-collapse:collapse;width:100%}td{border:1px solid #bbb;padding:8px}pre{overflow:auto;background:#f5f5f5;padding:12px}'
                                       'img{max-width:100%}a{color:#145da0}p{line-height:1.6}</style><main>' + '\n'.join(body) + '</main></html>\n')
    return outputs
