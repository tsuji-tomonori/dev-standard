"""選択参照のrouterフローを実ASTから抽出する。未解決呼出しは補完しない。"""
from __future__ import annotations

import ast
import json
import re


def inspect(index, config):
    """明示した個別処理とportの境界を検査し、順序付きフローを返す。"""
    handler = config['handler']
    steps = set(config.get('steps', []))
    ports = set(config.get('ports', []))
    pure = set(config.get('pure_calls', []))
    transactions = set(config.get('transactions', []))
    queries = config.get('sql_calls', {})
    if not steps or any(s not in index.defs for s in {handler, *steps}):
        raise ValueError('flow requires a real handler and named implementation steps')
    if (steps & (ports | pure | transactions)) or (ports & pure) or (transactions & (ports | pure)):
        raise ValueError('overlapping flow call classifications')
    if any(s in index.defs for s in ports | pure | transactions):
        raise ValueError('internal implementation cannot be classified as an opaque external call')
    # 個別処理から他の個別処理・routerへの委譲とtransactionを拒否する。
    for step in sorted(steps):
        calls = index.reachable(step)
        if (calls - {step}) & (steps | {handler}):
            raise ValueError(f'whole flow delegated to step: {step}')
        effects = []
        for symbol in calls:
            for node in index.nodes(symbol):
                if not isinstance(node, ast.Call):
                    continue
                name = target(symbol, node, index)
                if name in transactions or name.rsplit('.', 1)[-1] in {'commit', 'rollback', 'transaction'}:
                    raise ValueError(f'transaction belongs to router: {symbol}:{node.lineno}')
                if name in ports or (name in queries and name not in index.defs):
                    effects.append((symbol, node.lineno))
        if len(effects) > 1:
            raise ValueError(f'multiple effects in one step; split workflow: {step}')
    events, active = [], set()
    def emit(kind, symbol, node, **values):
        events.append({'kind': kind, 'source': {'path': index.paths[index.owner_module(symbol)], 'line': node.lineno}, **values})
    def expression(node, symbol, in_router):
        if node is None:
            return
        if isinstance(node, (ast.Lambda, ast.ListComp, ast.DictComp, ast.SetComp, ast.GeneratorExp, ast.IfExp, ast.BoolOp)):
            raise ValueError(f'unsupported conditional expression flow: {symbol}:{node.lineno}')
        if isinstance(node, ast.Call):
            # Pythonは引数を評価した後で外側の関数を呼ぶ。
            for argument in [*node.args, *(kw.value for kw in node.keywords)]:
                expression(argument, symbol, in_router)
            name = target(symbol, node, index)
            if in_router and name in ports | set(queries):
                raise ValueError(f'direct DB/provider call in router: {name}')
            if name in transactions and not in_router:
                raise ValueError('transaction belongs to router')
            if name not in steps | ports | pure | transactions | set(queries) and name not in index.defs:
                raise ValueError(f'unresolved flow call: {name}; supply a bounded adapter or call classification')
            label = name
            if name in queries:
                text = read_sql(index, queries[name])
                label = text.splitlines()[0].removeprefix('--').strip()
                if not text.startswith('--') or not re.search('[ぁ-んァ-ヶ一-龯]', label):
                    raise ValueError('SQL arrow requires a Japanese purpose comment')
            emit('transaction' if name in transactions else 'call', symbol, node, target=name, label=label)
            if name in index.defs:
                if name in active:
                    raise ValueError(f'unsupported recursive flow: {name}')
                if in_router and name not in steps:
                    raise ValueError(f'unclassified router helper: {name}')
                walk_function(name, False)
            return
        for child in ast.iter_child_nodes(node):
            expression(child, symbol, in_router)
    def terminal(nodes):
        for node in nodes:
            if isinstance(node, (ast.Return, ast.Raise, ast.Break, ast.Continue)):
                return True
            if isinstance(node, ast.If) and node.orelse and terminal(node.body) and terminal(node.orelse):
                return True
            if isinstance(node, (ast.With, ast.AsyncWith)) and terminal(node.body):
                return True
            if isinstance(node, ast.Try) and (terminal(node.finalbody) or
                    terminal(node.body) and all(terminal(h.body) for h in node.handlers) or
                    node.orelse and terminal(node.orelse) and all(terminal(h.body) for h in node.handlers)):
                return True
        return False

    def statements(nodes, symbol, in_router):
        for node in nodes:
            if isinstance(node, ast.If):
                expression(node.test, symbol, in_router)
                emit('alt', symbol, node, label=ast.unparse(node.test))
                statements(node.body, symbol, in_router)
                if node.orelse:
                    emit('else', symbol, node, label='条件不成立')
                    statements(node.orelse, symbol, in_router)
                emit('end', symbol, node)
            elif isinstance(node, (ast.For, ast.AsyncFor, ast.While)):
                expression(node.test if isinstance(node, ast.While) else node.iter, symbol, in_router)
                emit('loop', symbol, node, label=ast.unparse(node.test if isinstance(node, ast.While) else node.target))
                statements(node.body, symbol, in_router)
                emit('end', symbol, node)
                if node.orelse:
                    raise ValueError('loop else requires adapter')
            elif isinstance(node, ast.Try):
                emit('alt', symbol, node, label='正常処理')
                statements(node.body, symbol, in_router)
                for catch in node.handlers:
                    emit('else', symbol, catch, label='catch ' + (ast.unparse(catch.type) if catch.type else 'BaseException'))
                    statements(catch.body, symbol, in_router)
                emit('end', symbol, node)
                if node.orelse:
                    emit('opt', symbol, node, label='例外なし')
                    statements(node.orelse, symbol, in_router)
                    emit('end', symbol, node)
                if node.finalbody:
                    emit('opt', symbol, node, label='finally（常時）')
                    statements(node.finalbody, symbol, in_router)
                    emit('end', symbol, node)
            elif isinstance(node, (ast.With, ast.AsyncWith)):
                for item in node.items:
                    expression(item.context_expr, symbol, in_router)
                emit('opt', symbol, node, label='context enter / exit')
                statements(node.body, symbol, in_router)
                emit('end', symbol, node)
            elif isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign, ast.Expr, ast.Return, ast.Raise)):
                expression(getattr(node, 'value', None) if not isinstance(node, ast.Raise) else node.exc, symbol, in_router)
                if isinstance(node, (ast.Return, ast.Raise)):
                    emit('return' if isinstance(node, ast.Return) else 'raise', symbol, node, label=ast.unparse(node))
                    return
            elif isinstance(node, (ast.Pass, ast.Break, ast.Continue)):
                emit('note', symbol, node, label=ast.unparse(node))
                if isinstance(node, (ast.Break, ast.Continue)):
                    return
            else:
                raise ValueError(f'unsupported flow statement: {type(node).__name__}:{node.lineno}')
            if terminal([node]):
                return
    def walk_function(symbol, in_router):
        index.refs(symbol)  # alias shadowingを同じ境界で拒否する。
        active.add(symbol)
        start = len(events)
        statements(index.defs[symbol].body, symbol, in_router)
        emitted = events[start:]
        effects = [e for e in emitted if e.get('target') in ports or (e.get('target') in queries and e.get('target') not in index.defs)]
        if symbol in steps and (len(effects) > 1 or effects and any(e['kind'] == 'loop' for e in emitted)):
            raise ValueError(f'multiple effects in one expanded step: {symbol}')
        active.remove(symbol)
    walk_function(handler, True)
    used = {event.get('target') for event in events}
    if not steps <= used or not set(queries) <= used:
        raise ValueError('unused flow step or SQL mapping')
    return {'precision': 'static ordered AST; declared external boundaries', 'handler': handler, 'events': events}


def target(symbol, call, index):
    """動的呼出しを名前として推測しない。"""
    def dotted(node):
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            base = dotted(node.value)
            return base + '.' + node.attr if base else ''
        return ''
    name = dotted(call.func)
    if not name:
        raise ValueError(f'dynamic flow call: {symbol}:{call.lineno}')
    return index.resolve(index.owner_module(symbol), name)


def read_sql(index, path):
    """indexと同じrepository境界でSQL正本を読む。"""
    from pathlib import Path
    p = index.root / path
    if Path(path).is_absolute() or '..' in Path(path).parts or not p.is_file() or any(x.is_symlink() for x in (p, *p.parents)):
        raise ValueError('unsafe flow SQL source')
    return p.read_text(encoding='utf-8')


def mermaid(flow):
    """実際の順序付きイベントだけを図へ投影する。"""
    def label(value):
        return str(value).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('\n', ' ').replace(';', ',')
    lines = ['sequenceDiagram', 'participant R as Router', 'participant S as Step / Port']
    for event in flow['events']:
        kind, text = event['kind'], label(event.get('label', ''))
        if kind in {'alt', 'else', 'loop', 'opt'}:
            lines.append(f'{kind} {text}')
        elif kind == 'end':
            lines.append('end')
        elif kind in {'call', 'transaction'}:
            lines.append(f'R->>S: {text}')
        else:
            lines.append(f'Note over R: {text}')
    return '\n'.join(lines) + '\n'


def serialize(flow):
    """adapterで利用できる決定的なmachine-readable表現。"""
    return json.dumps(flow, ensure_ascii=False, sort_keys=True, indent=2) + '\n'
