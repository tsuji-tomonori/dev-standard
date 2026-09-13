"""例外応答・型付きcatalog・テスト説明を実sourceの境界へ接続する。"""
from __future__ import annotations

import ast
import re

JAPANESE = re.compile('[ぁ-んァ-ヶ一-龯]')


def gwt(root, test_id, confined):
    """実テストdocstringから一意な日本語の検証単位を取得する。"""
    path, *names = test_id.split('::')
    if not names or not names[-1].startswith('test_'):
        raise ValueError('GWT requires an executable test identifier')
    tree = ast.parse(confined(root, path).read_text(encoding='utf-8'))
    for name in names:
        matches = [node for node in tree.body if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name]
        if len(matches) != 1:
            raise ValueError('missing or duplicate GWT test source')
        tree = matches[0]
    if not isinstance(tree, (ast.FunctionDef, ast.AsyncFunctionDef)) or not any(isinstance(n, (ast.Assert, ast.Call)) for n in ast.walk(tree)):
        raise ValueError('GWT source has no executable verification')
    text = ast.get_docstring(tree) or ''
    result = {}
    for phase in ['Given', 'When', 'Then']:
        lines = re.findall(r'^\s*' + phase + r'\s*[:：]\s*(.+)$', text, re.M)
        if len(lines) != 1 or not JAPANESE.search(lines[0]):
            raise ValueError(f'missing, duplicate or non-Japanese {phase} description: {test_id}')
        result[phase.lower()] = lines[0].strip()
    if len(set(result.values())) != 3:
        raise ValueError('duplicate GWT descriptions')
    return {**result, 'test': test_id, 'source': {'path': path, 'line': tree.lineno}}


def response(node, module, index):
    """literalなHTTP tuple、Problem/HTTPException keywordだけを確定する。"""
    value = node.value if isinstance(node, ast.Return) else node.exc if isinstance(node, ast.Raise) else node
    if isinstance(value, ast.Tuple) and len(value.elts) == 2:
        status = index.literal(module, value.elts[0])
        body = index.literal(module, value.elts[1])
    elif isinstance(value, ast.Call):
        constructor = index.resolve(module, ast.unparse(value.func))
        if not isinstance(node, ast.Raise) or constructor not in {'fastapi.HTTPException', 'fastapi.exceptions.HTTPException', 'starlette.exceptions.HTTPException'}:
            raise ValueError('unresolved response constructor requires exception adapter')
        fields = {kw.arg: kw.value for kw in value.keywords}
        if None in fields or value.args:
            raise ValueError('dynamic response requires exception adapter')
        status = index.literal(module, fields.get('status_code', fields.get('status')))
        if 'detail' in fields:
            body = index.literal(module, fields['detail'])
        else:
            body = {key: index.literal(module, fields[key]) for key in ['code', 'message']}
    else:
        raise ValueError('unresolved exception response; no generic fallback')
    if type(status) is not int or not 100 <= status <= 599 or not isinstance(body, dict):
        raise ValueError('invalid exception HTTP response')
    if not all(isinstance(body.get(key), str) and body[key].strip() for key in ['code', 'message']):
        raise ValueError('exception response requires safe code and message')
    return {'status': status, 'code': body['code'], 'message': body['message']}


def inspect(index, config):
    """全catch/raiseの対応と、catalog・応答・context型の実接続を検査する。"""
    handler = config['handler']
    boundaries = config.get('http_handlers', [])
    roots = index.reachable(handler)
    for symbol in boundaries:
        if symbol not in index.defs:
            raise ValueError('missing HTTP exception handler')
        decorators = index.defs[symbol].decorator_list
        if not any(isinstance(d, ast.Call) and isinstance(d.func, ast.Attribute) and d.func.attr == 'exception_handler' and len(d.args) == 1 for d in decorators):
            raise ValueError('HTTP boundary lacks exception_handler binding')
        roots |= index.reachable(symbol)
    nodes = {}
    for symbol in roots:
        module = index.owner_module(symbol)
        for node in index.nodes(symbol):
            if isinstance(node, ast.Raise) and any(isinstance(c, ast.ExceptHandler) and c.lineno < node.lineno <= c.end_lineno for c in index.nodes(symbol)):
                continue  # catchの終端raiseはcatch->応答の一経路として検査する。
            if isinstance(node, (ast.ExceptHandler, ast.Raise)):
                key = (index.paths[module], node.lineno)
                if key in nodes:
                    raise ValueError('ambiguous exception source')
                nodes[key] = (symbol, node)
    rules = config.get('rules', [])
    if len(rules) != len(nodes) or {(r['source']['path'], r['source']['line']) for r in rules} != set(nodes):
        raise ValueError('missing or duplicate exception path mapping')
    results, log_locations = [], set()
    logger = config['logger']
    for rule in rules:
        key = (rule['source']['path'], rule['source']['line'])
        symbol, node = nodes[key]
        module = index.owner_module(symbol)
        exception_node = node.type if isinstance(node, ast.ExceptHandler) else node.exc.func if isinstance(node.exc, ast.Call) else None
        if exception_node is None:
            if not isinstance(node, ast.Raise) or node.exc is not None:
                raise ValueError('dynamic or bare catch requires exception adapter')
            # bare re-raiseの型は最小のenclosing catchから導出する。
            enclosing = [n for n in index.nodes(symbol) if isinstance(n, ast.ExceptHandler) and n.lineno < node.lineno <= n.end_lineno]
            if not enclosing:
                raise ValueError('unresolved re-raise type')
            exception_node = min(enclosing, key=lambda n: n.end_lineno-n.lineno).type
        if not isinstance(exception_node, (ast.Name, ast.Attribute)):
            raise ValueError('dynamic exception type requires adapter')
        if isinstance(node, ast.ExceptHandler):
            if any(isinstance(n, (ast.If, ast.Try, ast.For, ast.While, ast.With, ast.Match)) for statement in node.body for n in ast.walk(statement)):
                raise ValueError('conditional catch outcome requires exception adapter')
            outcomes = [n for statement in node.body for n in ast.walk(statement) if isinstance(n, (ast.Return, ast.Raise, ast.Continue))]
            if len(outcomes) != 1 or node.body[-1] is not outcomes[0]:
                raise ValueError('catch requires one terminal outcome; adapter required')
            if node.name and any(isinstance(n, ast.Name) and n.id == node.name and isinstance(n.ctx, ast.Load)
                                 for statement in node.body for n in ast.walk(statement)):
                raise ValueError('raw caught exception use requires privacy adapter')
        exception = index.resolve(module, ast.unparse(exception_node))
        log_module, log = index.call_at(rule['log'], roots)
        if index.resolve(log_module, ast.unparse(log.func)) != logger or len(log.args) != 1 or not isinstance(log.args[0], (ast.Name, ast.Attribute)):
            raise ValueError('exception log must use the configured typed catalog logger')
        if rule['log']['path'] == key[0] and not node.lineno <= log.lineno <= node.end_lineno:
            # raiseの直前logは同じ関数の直前statementのみ許可する。
            if not isinstance(node, ast.Raise) or log.lineno != node.lineno-1:
                raise ValueError('log is outside the actual exception boundary')
        if rule['log']['path'] != key[0] and not any(index.owner_module(b) == log_module for b in boundaries):
            raise ValueError('log is not connected to an HTTP exception handler')
        catalog = index.literal(log_module, log.args[0])
        required = ['id', 'exception', 'status', 'code', 'message', 'level', 'operator_action', 'context_type']
        if not isinstance(catalog, dict) or any(k not in catalog for k in required) or any(not isinstance(catalog[k], str) or not catalog[k].strip() for k in required if k != 'status'):
            raise ValueError('incomplete typed operational catalog')
        if catalog['exception'] != exception or catalog['level'] not in {'WARNING', 'ERROR', 'CRITICAL'}:
            raise ValueError('catalog exception type or level mismatch')
        keywords = {kw.arg: kw.value for kw in log.keywords}
        if set(keywords) != {'context_model'}:
            raise ValueError('log privacy requires only a typed context; no raw message, exc_info or extra')
        context = keywords['context_model']
        if not isinstance(context, ast.Call) or context.args or any(kw.arg is None for kw in context.keywords):
            raise ValueError('unsupported dynamic log context')
        context_type = index.resolve(log_module, ast.unparse(context.func))
        if context_type != catalog['context_type'] or not isinstance(index.defs.get(context_type), ast.ClassDef):
            raise ValueError('log context type mismatch')
        klass = index.defs[context_type]
        fields = {n.target.id: ast.unparse(n.annotation) for n in klass.body if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name)}
        if set(fields) != {kw.arg for kw in context.keywords} or not fields:
            raise ValueError('log context field mismatch')
        safe_types = {'str': str, 'int': int, 'bool': bool}
        for kw in context.keywords:
            # runtime値のprivacy/taintは独自adapterで証明する。静的literal以外を推測しない。
            if not isinstance(kw.value, ast.Constant) or fields[kw.arg] not in safe_types or type(kw.value.value) is not safe_types[fields[kw.arg]]:
                raise ValueError('unsafe or incorrectly typed log context; runtime privacy adapter required')
            if re.search('token|jwt|secret|password|body|exception|message', kw.arg, re.I):
                raise ValueError('sensitive log context field')
        response_ref = rule['response']
        response_module = index.module_for(response_ref['path'])
        candidates = [(s, n) for s in roots if index.owner_module(s) == response_module for n in index.nodes(s)
                      if isinstance(n, (ast.Return, ast.Raise, ast.Continue)) and n.lineno == response_ref['line']]
        if len(candidates) != 1:
            raise ValueError('response is not a unique reachable exception outcome')
        response_symbol, actual_node = candidates[0]
        if isinstance(node, ast.ExceptHandler) and response_symbol == symbol:
            if actual_node not in node.body or not any(isinstance(n, ast.Expr) and n.value is log for n in node.body):
                raise ValueError('conditional catch outcome requires exception adapter')
        if response_symbol == symbol:
            if isinstance(node, ast.ExceptHandler) and not node.lineno <= actual_node.lineno <= node.end_lineno:
                raise ValueError('response is outside catch')
            if isinstance(node, ast.Raise) and actual_node is not node:
                raise ValueError('raise must map its actual HTTP boundary')
        elif response_symbol not in boundaries:
            raise ValueError('response is not an HTTP exception boundary')
        else:
            decorators = index.defs[response_symbol].decorator_list
            accepted = [index.resolve(response_module, ast.unparse(d.args[0])) for d in decorators if isinstance(d, ast.Call) and isinstance(d.func, ast.Attribute) and d.func.attr == 'exception_handler']
            if exception not in accepted:
                raise ValueError('HTTP handler exception type mismatch')
            boundary = index.defs[response_symbol]
            if log_module != response_module or not boundary.lineno <= log.lineno <= boundary.end_lineno:
                raise ValueError('log and response belong to different HTTP boundaries')
            if any(isinstance(n, (ast.If, ast.Try, ast.Match)) for statement in boundary.body for n in ast.walk(statement)):
                raise ValueError('conditional HTTP handler requires exception adapter')
        if isinstance(actual_node, ast.Continue):
            actual = {'status': None, 'code': catalog['code'], 'message': catalog['message']}
            outcome = 'continue'
        else:
            actual = response(actual_node, response_module, index)
            outcome = 'reraised-to-http' if response_symbol != symbol else 'handled'
        if any(catalog[k] != actual[k] for k in ['status', 'code', 'message']):
            raise ValueError('HTTP and log catalog disagree')
        if outcome == 'continue' and catalog['status'] is not None:
            raise ValueError('continued job must not invent an HTTP status')
        log_locations.add((rule['log']['path'], rule['log']['line']))
        results.append({'exception': exception, 'outcome': outcome, **actual, 'log_id': catalog['id'], 'level': catalog['level'],
                        'operator_action': catalog['operator_action'], 'source': rule['source'], 'log_source': rule['log'],
                        'response_source': response_ref, 'context_type': context_type})
    actual_logs = {(index.paths[index.owner_module(s)], n.lineno) for s in roots for n in index.nodes(s) if isinstance(n, ast.Call) and index.resolve(index.owner_module(s), ast.unparse(n.func)) == logger}
    if actual_logs != log_locations:
        raise ValueError('unmapped operational log call')
    return results
