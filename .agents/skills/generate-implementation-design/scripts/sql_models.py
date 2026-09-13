"""限定したDDL/SQL ASTからquery専用の厳格なParams/Rowを生成する。"""
from __future__ import annotations

import keyword
import re

import sqlglot
from sqlglot import exp

TYPES = {'INT': 'int', 'BIGINT': 'int', 'SMALLINT': 'int', 'TEXT': 'str', 'VARCHAR': 'str', 'CHAR': 'str',
         'BOOLEAN': 'bool', 'DOUBLE': 'float', 'FLOAT': 'float'}


def identifier(name):
    """生成コードへ安全な識別子だけを渡す。"""
    if not isinstance(name, str) or not name.isidentifier() or keyword.iskeyword(name) or name.startswith('_'):
        raise ValueError(f'unsupported model identifier: {name}')
    return name


def project(ddl, sql, dialect='postgres'):
    """単一tableの明示列SELECT/INSERT/UPDATE/DELETEに対応する。推測fallbackはしない。"""
    tables = {}
    for statement in sqlglot.parse(ddl, read=dialect):
        if not isinstance(statement, exp.Create) or not isinstance(statement.this, exp.Schema) or statement.args.get('kind') != 'TABLE':
            raise ValueError('unsupported DDL; supply a resolved schema adapter')
        if statement.this.this.db or statement.this.this.catalog:
            raise ValueError('qualified DDL requires explicit schema adapter')
        table = statement.this.this.name
        if table in tables:
            raise ValueError('duplicate DDL table')
        columns = tables[table] = {}
        for column in statement.this.expressions:
            if not isinstance(column, exp.ColumnDef):
                raise ValueError('unsupported table constraint; supply schema adapter')
            name = identifier(column.name)
            kind = column.args['kind'].this.value
            if kind not in TYPES:
                raise ValueError(f'unsupported SQL type: {kind}')
            nullable = not any(isinstance(c.kind, (exp.NotNullColumnConstraint, exp.PrimaryKeyColumnConstraint)) for c in column.constraints)
            if name in columns:
                raise ValueError('duplicate DDL column')
            columns[name] = (TYPES[kind], nullable)
    parsed = sqlglot.parse(sql, read=dialect)
    if len(parsed) != 1 or not isinstance(parsed[0], (exp.Select, exp.Insert, exp.Update, exp.Delete)):
        raise ValueError('one supported SQL statement is required')
    query = parsed[0]
    sources = list(query.find_all(exp.Table))
    if len(sources) != 1 or sources[0].name not in tables or sources[0].db:
        raise ValueError('joins, subqueries and unknown tables require a SQL model adapter')
    if query.args.get('with') or query.args.get('with_') or query.args.get('returning'):
        raise ValueError('CTE/RETURNING requires SQL model adapter')
    columns, params, rows = tables[sources[0].name], {}, {}
    def column_type(node):
        if not isinstance(node, exp.Column) or node.name not in columns:
            raise ValueError('unresolved SQL column type')
        if node.table and node.table not in {sources[0].name, sources[0].alias}:
            raise ValueError('unknown column qualifier')
        return columns[node.name]
    for node in query.find_all(exp.Column):
        column_type(node)
    def bind(node, value):
        if not isinstance(node, exp.Placeholder) or not node.name:
            raise ValueError('only named bound SQL parameters are supported')
        name = identifier(node.name)
        if name in params and params[name] != value:
            raise ValueError('conflicting bound parameter type or NULL constraint')
        params[name] = value
    for node in query.walk():
        if isinstance(node, (exp.EQ, exp.NEQ, exp.GT, exp.GTE, exp.LT, exp.LTE)):
            for left, right in [(node.this, node.expression), (node.expression, node.this)]:
                if isinstance(left, exp.Column) and isinstance(right, exp.Placeholder):
                    bind(right, column_type(left))
    if isinstance(query, exp.Insert):
        if not isinstance(query.this, exp.Schema) or not isinstance(query.expression, exp.Values) or len(query.expression.expressions) != 1:
            raise ValueError('INSERT requires explicit columns and one VALUES tuple')
        names, values = query.this.expressions, query.expression.expressions[0].expressions
        if len(names) != len(values) or len({n.name for n in names}) != len(names):
            raise ValueError('INSERT binding arity or duplicate column')
        for name, value in zip(names, values):
            if name.name not in columns:
                raise ValueError('unknown INSERT column')
            if isinstance(value, exp.Placeholder):
                bind(value, columns[name.name])
            else:
                raise ValueError('INSERT expression requires adapter')
    if isinstance(query, exp.Select):
        for node in query.expressions:
            original = node.this if isinstance(node, exp.Alias) else node
            value = column_type(original)
            name = identifier(node.alias_or_name)
            if name in rows:
                raise ValueError('duplicate projection field')
            rows[name] = value
    if {node.name for node in query.find_all(exp.Placeholder)} != set(params):
        raise ValueError('unresolved bound parameter type')
    return {'params': params, 'row': rows, 'kind': type(query).__name__}


def generate(ddl, queries, dialect='postgres'):
    """query単位のkeyword-only dataclassを生成し、余剰・型・NULLを実行時拒否する。"""
    lines = ['# 自動生成。DDL/SQL正本から再生成し、直接編集しない。',
             'from dataclasses import dataclass, fields', '',
             'def _validate(instance):',
             '    for field in fields(instance):',
             '        value = getattr(instance, field.name)',
             '        allowed = field.type.__args__ if hasattr(field.type, "__args__") else (field.type,)',
             '        if type(value) not in allowed:',
             '            raise TypeError(f"invalid type or NULL: {field.name}")', '']
    names = set()
    for query_name, sql in sorted(queries.items()):
        identifier(query_name)
        base = ''.join(part.capitalize() for part in re.split('_+', query_name))
        if base in names:
            raise ValueError('generated query model name collision')
        names.add(base)
        projection = project(ddl, sql, dialect)
        for suffix, key in [('Params', 'params'), ('Row', 'row')]:
            if key == 'row' and projection['kind'] != 'Select':
                continue
            lines.extend(['@dataclass(frozen=True, kw_only=True)', f'class {base}{suffix}:'])
            for name, (kind, nullable) in projection[key].items():
                lines.append(f'    {name}: {kind}' + (' | None' if nullable else ''))
            lines.extend(['    def __post_init__(self):', '        _validate(self)', ''])
    return '\n'.join(lines) + '\n'


def inspect(root, config, confined):
    """現在の正本から再生成して、欠落・手編集・SQL/DDL変更を検出する。"""
    ddl = confined(root, config['ddl']).read_text(encoding='utf-8')
    queries = {name: confined(root, path).read_text(encoding='utf-8') for name, path in config['queries'].items()}
    output = generate(ddl, queries, config.get('dialect', 'postgres'))
    if confined(root, config['output']).read_text(encoding='utf-8') != output:
        raise ValueError('query-specific SQL models drift; regenerate from DDL/SQL')
    return {name: project(ddl, sql, config.get('dialect', 'postgres')) for name, sql in queries.items()}
