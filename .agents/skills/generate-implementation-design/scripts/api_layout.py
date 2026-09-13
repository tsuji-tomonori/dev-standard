#!/usr/bin/env python3
"""選択したAPI所有境界と、静的に解決できる実接続を検査する。対象コードは実行しない。"""
from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path

METHODS = {'get', 'post', 'put', 'patch', 'delete', 'options', 'head', 'trace'}
ROLES = ('router.py', 'functions.py', 'schemas.py', 'response_builders.py', 'contract.py', 'samples.py')


def confined(root: Path, name: str) -> Path:
    """repository外、リンク、非通常fileを入力にしない。"""
    if not isinstance(name, str) or not name or '\\' in name or any(p in {'', '.', '..'} for p in name.split('/')):
        raise ValueError(f'invalid source path: {name}')
    path = root / name
    if Path(name).is_absolute():
        raise ValueError(f'absolute source path: {name}')
    for parent in (path, *path.parents):
        if parent == root:
            break
        if parent.is_symlink():
            raise ValueError(f'symlink source: {name}')
    if not path.is_file():
        raise ValueError(f'missing source: {name}')
    return path


def dotted(node):
    """名前と属性の連鎖だけを名前解決の対象にする。"""
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = dotted(node.value)
        return f'{base}.{node.attr}' if base else ''
    return ''


def scoped(node):
    """未呼出しの入れ子関数を実接続として数えない。"""
    result = []

    def walk(current):
        result.append(current)
        for child in ast.iter_child_nodes(current):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
                continue
            walk(child)
    walk(node)
    return result


def bindings(scope):
    """呼出し走査とは別にscope内の名前束縛を収集する。"""
    result = set()
    def walk(node):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            result.add(node.name)
            return
        if isinstance(node, ast.Lambda):
            return
        if isinstance(node, ast.Name) and isinstance(node.ctx, (ast.Store, ast.Del)):
            result.add(node.id)
        if isinstance(node, ast.ExceptHandler) and node.name:
            result.add(node.name)
        if isinstance(node, (ast.MatchAs, ast.MatchStar)) and node.name:
            result.add(node.name)
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            result.update(entry.asname or entry.name.split('.')[0] for entry in node.names)
        for child in ast.iter_child_nodes(node):
            walk(child)
    for node in scope.body:
        walk(node)
    if hasattr(scope, 'args'):
        result.update(node.arg for node in ast.walk(scope.args) if isinstance(node, ast.arg))
    return result


class Index:
    """通常のPython import、alias、ローカル再exportを解決する小さなindex。"""

    def __init__(self, root: Path, python_root: str):
        self.root = root
        self.python_root = python_root
        base = root / python_root
        if not base.is_dir() or base.is_symlink() or not base.resolve().is_relative_to(root.resolve()):
            raise ValueError('invalid python_root')
        self.modules, self.paths, self.aliases, self.defs, self.values = {}, {}, {}, {}, {}
        for path in sorted(base.rglob('*.py')):
            confined(root, path.relative_to(root).as_posix())
            relative = path.relative_to(base).with_suffix('')
            parts = list(relative.parts)
            if parts[-1] == '__init__':
                parts.pop()
            module = '.'.join(parts)
            tree = ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
            self.modules[module], self.paths[module] = tree, path.relative_to(root).as_posix()
            aliases = self.aliases[module] = {}
            package = parts if path.name == '__init__.py' else parts[:-1]
            for node in tree.body:
                if isinstance(node, ast.Import):
                    for entry in node.names:
                        aliases[entry.asname or entry.name.split('.')[0]] = entry.name if entry.asname else entry.name.split('.')[0]
                elif isinstance(node, ast.ImportFrom):
                    prefix = package[:len(package) - node.level + 1] if node.level else []
                    target = '.'.join([*prefix, *node.module.split('.')]) if node.module else '.'.join(prefix)
                    for entry in node.names:
                        if entry.name == '*':
                            raise ValueError(f'unsupported wildcard import: {path}:{node.lineno}')
                        aliases[entry.asname or entry.name] = f'{target}.{entry.name}'.strip('.')
                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    self.defs[f'{module}.{node.name}'] = node
                elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                    targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                    for target in targets:
                        if isinstance(target, ast.Name):
                            self.values[f'{module}.{target.id}'] = node.value

        for module, aliases in self.aliases.items():
            without_imports = ast.Module(body=[n for n in self.modules[module].body if not isinstance(n, (ast.Import, ast.ImportFrom))], type_ignores=[])
            if bindings(without_imports) & set(aliases):
                raise ValueError(f'unsupported module alias reassignment: {module}')

    def module_for(self, path):
        found = [module for module, name in self.paths.items() if name == path]
        if len(found) != 1:
            raise ValueError(f'Python source outside index: {path}')
        return found[0]

    def resolve(self, module, name, seen=None):
        seen = set() if seen is None else seen
        marker = (module, name)
        if marker in seen:
            raise ValueError(f'cyclic re-export: {module}.{name}')
        seen.add(marker)
        head, *tail = name.split('.')
        target = self.aliases[module].get(head, f'{module}.{head}')
        full = '.'.join([target, *tail])
        if full in self.defs or full in self.values or full in self.modules:
            return full
        for candidate in sorted(self.modules, key=len, reverse=True):
            prefix = candidate + '.'
            if full.startswith(prefix):
                remainder = full[len(prefix):]
                if remainder.split('.')[0] in self.aliases[candidate]:
                    return self.resolve(candidate, remainder, seen)
        return full

    def owner_module(self, symbol):
        return next((m for m in sorted(self.modules, key=len, reverse=True) if symbol == m or symbol.startswith(m + '.')), None)

    def refs(self, symbol, calls_only=False):
        module = self.owner_module(symbol)
        node = self.defs.get(symbol)
        if node is None:
            return set()
        nodes = scoped(node)
        known = set(self.aliases[module]) | {key[len(module)+1:] for key in self.defs if key.startswith(module + '.') and '.' not in key[len(module)+1:]}
        shadow = bindings(node) & known
        if shadow:
            raise ValueError(f'unsupported alias reassignment: {symbol}: {sorted(shadow)}')
        result = set()
        arguments = {arg.arg for arg in ast.walk(node.args) if isinstance(arg, ast.arg)} if hasattr(node, 'args') else set()
        for child in nodes:
            if isinstance(child, ast.Call) and isinstance(child.func, ast.Name) and child.func.id in (arguments | bindings(node)):
                raise ValueError(f'unsupported dynamic callable binding: {symbol}:{child.lineno}')
            target = child.func if isinstance(child, ast.Call) else child
            if calls_only and not isinstance(child, ast.Call):
                continue
            name = dotted(target)
            if name:
                result.add(self.resolve(module, name))
        return result

    def nodes(self, symbol):
        return scoped(self.defs[symbol])

    def reachable(self, symbol):
        visited, pending = set(), [symbol]
        while pending:
            current = pending.pop()
            if current in visited:
                continue
            visited.add(current)
            pending.extend(self.refs(current, calls_only=True) & set(self.defs) - visited)
        return visited

    def literal(self, module, node, seen=None):
        """定数・辞書・keyword構築からHTTP契約値を限定解決する。"""
        seen = set() if seen is None else seen
        try:
            return ast.literal_eval(node)
        except (ValueError, TypeError):
            pass
        name = dotted(node)
        if name:
            symbol = self.resolve(module, name)
            if symbol in seen:
                raise ValueError('cyclic metadata')
            seen.add(symbol)
            if symbol in self.values:
                return self.literal(self.owner_module(symbol), self.values[symbol], seen)
            if isinstance(node, ast.Attribute):
                value = self.literal(module, node.value, seen)
                if isinstance(value, dict) and node.attr in value:
                    return value[node.attr]
        if isinstance(node, ast.Subscript):
            value = self.literal(module, node.value, seen.copy())
            key = self.literal(module, node.slice, seen.copy())
            return value[key]
        if isinstance(node, ast.Call) and node.keywords and not node.args:
            return {kw.arg: self.literal(module, kw.value, seen.copy()) for kw in node.keywords if kw.arg}
        if isinstance(node, ast.Dict):
            return {self.literal(module, key, seen.copy()): self.literal(module, value, seen.copy()) for key, value in zip(node.keys, node.values)}
        raise ValueError(f'unsupported static metadata: {self.paths[module]}:{getattr(node, "lineno", 0)}')

    def call_at(self, source, roots):
        path, line = source.get('path'), source.get('line')
        if not isinstance(line, int):
            raise ValueError('call evidence requires source line')
        module = self.module_for(path)
        for symbol in roots:
            if self.owner_module(symbol) != module:
                continue
            for node in scoped(self.defs[symbol]):
                if isinstance(node, ast.Call) and node.lineno == line:
                    return module, node
        raise ValueError(f'access evidence is not a reachable call: {path}:{line}')


def operation_ids(document):
    """OpenAPIの操作集合を重複なしで取得する。"""
    result = {}
    for path, item in document.get('paths', {}).items():
        for method, op in item.items():
            if method not in METHODS:
                continue
            identity = op.get('operationId')
            if not identity or identity in result:
                raise ValueError('empty or duplicate OpenAPI operation ID')
            result[identity] = (method, path, op)
    if not result:
        raise ValueError('empty OpenAPI operation inventory')
    return result


def inspect(root: Path, config: dict, document: dict) -> dict:
    """明示選択profileでのみAPI構成適合を検査し、根拠を返す。"""
    if config.get('profile') != 'lazunex-v1':
        raise ValueError('select supported layout profile: lazunex-v1')
    index = Index(root, config['python_root'])
    operations = config.get('operations', {})
    exported = operation_ids(document)
    if set(operations) != set(exported):
        raise ValueError('layout operation inventory differs from OpenAPI')
    owners = [item['package'] for item in operations.values()]
    if len(owners) != len(set(owners)):
        raise ValueError('multiple operations in one package')
    shared = config.get('shared', {})
    if any(not isinstance(role, str) or not role.strip() for role in shared.values()):
        raise ValueError('shared ownership requires concrete responsibility')
    for path in [*owners, *shared]:
        if not path or Path(path).is_absolute() or any(p in {'', '.', '..'} for p in path.split('/')):
            raise ValueError('invalid ownership path')
    def owner(path):
        matches = [p for p in [*owners, *shared] if path.startswith(p + '/')]
        if len(matches) > 1:
            raise ValueError('overlapping ownership roots')
        return matches[0] if matches else None
    # importだけでも別API依存・共有からAPIへの逆依存を検出する。
    for module, path in index.paths.items():
        origin = owner(path)
        if not origin:
            continue
        for target in index.aliases[module].values():
            resolved = index.resolve(module, next(k for k, v in index.aliases[module].items() if v == target))
            other_module = index.owner_module(resolved)
            if other_module is None:
                continue
            other = owner(index.paths[other_module])
            if other in owners and other != origin:
                raise ValueError(f'API-to-API or shared back dependency: {path} -> {index.paths[other_module]}')
            if other is None:
                raise ValueError(f'undeclared shared ownership: {path} -> {index.paths[other_module]}')
    result, declared_routes = [], set()
    for identity, item in sorted(operations.items()):
        package = item['package']
        modules = {}
        for role in ROLES:
            path = f'{package}/{role}'
            module = index.module_for(path)
            tree = index.modules[module]
            substantive = [n for n in tree.body if not isinstance(n, (ast.Import, ast.ImportFrom, ast.Pass)) and not (
                isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant))]
            if not substantive:
                raise ValueError(f'empty responsibility file: {path}')
            modules[role] = module
        handler = f'{modules["router.py"]}.{item["handler"]}'
        function = index.defs.get(handler)
        if not isinstance(function, (ast.FunctionDef, ast.AsyncFunctionDef)):
            raise ValueError(f'missing handler: {handler}')
        routes = [node for node in function.decorator_list if isinstance(node, ast.Call) and dotted(node.func).split('.')[-1] in METHODS]
        if len(routes) != 1:
            raise ValueError(f'one HTTP operation per handler is required: {handler}')
        route = routes[0]
        declared_routes.add(handler)
        method, path, _ = exported[identity]
        if dotted(route.func).split('.')[-1] != method:
            raise ValueError(f'HTTP method mismatch: {identity}')
        route_path = index.literal(modules['router.py'], route.args[0]) if route.args else ''
        prefix = item.get('router_prefix', '')
        if prefix + route_path != path:
            raise ValueError(f'HTTP path mismatch: {identity}')
        keywords = {kw.arg: kw.value for kw in route.keywords}
        if 'operation_id' not in keywords or index.literal(modules['router.py'], keywords['operation_id']) != identity:
            raise ValueError(f'operation ID mismatch: {identity}')
        calls = index.reachable(handler)
        referenced = set().union(*(index.refs(symbol) for symbol in calls))
        for role in ('functions.py', 'response_builders.py'):
            if not any(index.owner_module(symbol) == modules[role] for symbol in calls):
                raise ValueError(f'unconnected callable responsibility: {package}/{role}')
        for role in ('schemas.py', 'contract.py', 'samples.py'):
            if not any(index.owner_module(symbol) == modules[role] for symbol in referenced):
                raise ValueError(f'unconnected reference responsibility: {package}/{role}')
        sample_values = [symbol for symbol in referenced if symbol in index.values and index.owner_module(symbol) == modules['samples.py']]
        if not sample_values or not any(index.literal(modules['samples.py'], index.values[symbol]) for symbol in sample_values):
            raise ValueError(f'empty or unsupported samples: {identity}')
        schema_symbols = [symbol for symbol in referenced if symbol in index.defs and index.owner_module(symbol) == modules['schemas.py']]
        if not schema_symbols or not any(any(not isinstance(n, ast.Pass) and not (isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant))
                                            for n in index.defs[symbol].body) for symbol in schema_symbols):
            raise ValueError(f'empty or unsupported schemas: {identity}')
        # 定数contractは実decoratorとの一致も確認する。
        contract_symbols = [s for s in referenced if s in index.values and index.owner_module(s) == modules['contract.py']]
        for symbol in contract_symbols:
            value = index.literal(modules['contract.py'], index.values[symbol])
            if isinstance(value, dict):
                for key, expected in [('operation_id', identity), ('operationId', identity), ('method', method.upper()), ('path', path)]:
                    if key in value and value[key] != expected:
                        raise ValueError(f'contract mismatch: {identity}.{key}')
        # HTTP層の直接永続化とSQL所有境界の迂回を許さない。
        for symbol in calls:
            module = index.owner_module(symbol)
            if module in {modules['functions.py'], modules['response_builders.py']}:
                meaningful = [n for n in index.defs[symbol].body if not isinstance(n, ast.Pass) and not (
                    isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant)) and not (
                    isinstance(n, ast.Return) and (n.value is None or isinstance(n.value, ast.Constant) and n.value.value in (None, Ellipsis)))]
                if not meaningful:
                    raise ValueError(f'empty callable responsibility: {symbol}')
            if module in {modules['router.py'], modules['functions.py'], modules['response_builders.py']}:
                for node in scoped(index.defs[symbol]):
                    if isinstance(node, ast.Call) and dotted(node.func).split('.')[-1] in ({'execute', 'executemany', 'cursor'} if module == modules['router.py'] else {'execute', 'executemany', 'commit', 'rollback', 'cursor'}):
                        raise ValueError(f'persistence outside owned query: {symbol}:{node.lineno}')
        sql_paths = sorted((root / package / 'sql').glob('*.sql'))
        bindings = item.get('queries', {})
        if {p.relative_to(root).as_posix() for p in sql_paths} != set(bindings):
            raise ValueError(f'owned SQL inventory mismatch: {identity}')
        symbols = []
        if len({binding['function'] for binding in bindings.values()}) != len(bindings):
            raise ValueError(f'multiple SQL files overwrite one generated symbol: {identity}')
        for sql_path, binding in bindings.items():
            confined(root, sql_path)
            wrapper = f'{package}/generated/queries.py'
            module = index.module_for(wrapper)
            symbol = f'{module}.{binding["function"]}'
            if symbol not in calls:
                raise ValueError(f'owned query is not reachable: {sql_path}')
            sql_calls = [call for call in scoped(index.defs[symbol]) if isinstance(call, ast.Call)
                         and dotted(call.func).split('.')[-1] in {'execute', 'executemany'}]
            if not sql_calls:
                raise ValueError(f'no SQL execution binding: {sql_path}')
            allowed = {sql_path, str(Path(sql_path).relative_to(package))}
            for call in sql_calls:
                argument = call.args[0] if call.args else next((kw.value for kw in call.keywords if kw.arg in {'query', 'statement', 'sql'}), None)
                try:
                    value = index.literal(module, argument)
                except ValueError as exc:
                    raise ValueError(f'unsupported SQL argument binding: {sql_path}') from exc
                if not isinstance(value, str) or value not in allowed:
                    raise ValueError(f'wrapper has no owned SQL reference: {sql_path}')
            symbols.append(symbol)
        if len(symbols) != len(set(symbols)):
            raise ValueError(f'multiple SQL files overwrite one generated symbol: {identity}')
        result.append({'operation': identity, 'package': package, 'handler': handler,
                       'reachable': sorted(calls), 'queries': sorted(bindings)})
    actual_routes = {symbol for symbol, node in index.defs.items() if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and any(
        isinstance(d, ast.Call) and dotted(d.func).split('.')[-1] in METHODS for d in node.decorator_list)}
    if actual_routes != declared_routes:
        raise ValueError('undeclared or aggregated HTTP operations')
    all_owned_sql = {p.relative_to(root).as_posix() for p in (root / config['python_root']).rglob('*.sql')}
    for sql_path in all_owned_sql:
        confined(root, sql_path)
    declared_sql = {p for item in operations.values() for p in item.get('queries', {})}
    # 共有queryも別ownerと明示し、各APIからの到達はadapterで補完する。
    shared_sql = {p for p in all_owned_sql if owner(p) in shared}
    if all_owned_sql != declared_sql | shared_sql:
        raise ValueError('SQL outside operation or declared shared ownership')
    for module, path in index.paths.items():
        if path.endswith('/generated/queries.py') and owner(path) is None:
            raise ValueError(f'global generated query module: {path}')
    return {'profile': config['profile'], 'scope': 'static Python bindings and supplied OpenAPI; runtime mounting requires adapter', 'operations': result}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--config', required=True)
    parser.add_argument('--openapi', required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        result = inspect(root, json.loads(confined(root, args.config).read_text()), json.loads(confined(root, args.openapi).read_text()))
    except (ValueError, KeyError, SyntaxError) as exc:
        parser.exit(1, f'API layout: {exc}\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
