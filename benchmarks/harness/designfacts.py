from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .io import BenchmarkError, digest_value, load_json

HTTP_METHODS = {"get", "put", "post", "delete", "options", "head", "patch", "trace"}
TOKEN = re.compile(r"[A-Za-z_][A-Za-z0-9_.$]*|'(?:''|[^'])*'|\"(?:\"\"|[^\"])*\"|[(),;*=<>.+/-]")
IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_.$]*$")


class CallOrder(ast.NodeVisitor):
    def __init__(self) -> None:
        self.calls: list[str] = []

    def visit_Call(self, node: ast.Call) -> None:
        self.visit(node.func)
        for argument in node.args:
            self.visit(argument)
        for keyword in node.keywords:
            self.visit(keyword.value)
        self.calls.append(display_call(node.func))


def display_call(node: ast.AST) -> str:
    parts: list[str] = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
    return ".".join(reversed(parts)) or "call"


def python_route_facts(path: Path) -> list[dict[str, Any]]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (OSError, SyntaxError) as exc:
        raise BenchmarkError(f"cannot parse Python fixture {path}: {exc}") from exc
    facts: list[dict[str, Any]] = []
    for node in tree.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        method = route = None
        for decorator in node.decorator_list:
            if not isinstance(decorator, ast.Call) or not isinstance(decorator.func, ast.Attribute):
                continue
            candidate = decorator.func.attr.lower()
            if candidate not in HTTP_METHODS or not decorator.args or not isinstance(decorator.args[0], ast.Constant):
                continue
            method, route = candidate.upper(), str(decorator.args[0].value)
        if method is None or route is None:
            continue
        collector = CallOrder()
        for statement in node.body:
            collector.visit(statement)
        facts.append({"kind": "route", "method": method, "path": route, "function": node.name, "calls": collector.calls})
    return sorted(facts, key=lambda item: (item["path"], item["method"], item["function"]))


def openapi_facts(path: Path) -> list[dict[str, Any]]:
    document = load_json(path)
    if not isinstance(document, dict):
        raise BenchmarkError(f"{path}: OpenAPI root must be an object")
    facts: list[dict[str, Any]] = []
    seen: set[str] = set()
    for route, item in sorted(document.get("paths", {}).items()):
        if not isinstance(item, dict):
            continue
        for method, operation in sorted(item.items()):
            if method.lower() not in HTTP_METHODS or not isinstance(operation, dict):
                continue
            operation_id = str(operation.get("operationId") or f"{method}-{route}")
            if operation_id in seen:
                raise BenchmarkError(f"duplicate OpenAPI operationId: {operation_id}")
            seen.add(operation_id)
            facts.append(
                {
                    "kind": "openapi-operation",
                    "method": method.upper(),
                    "path": route,
                    "operation_id": operation_id,
                    "requirements": sorted(map(str, operation.get("x-requirement-ids", []))),
                    "responses": sorted(map(str, operation.get("responses", {}).keys())),
                }
            )
    return facts


@dataclass(frozen=True)
class SqlStatement:
    operation: str
    target: str | None
    tables: tuple[str, ...]

    def fact(self, source: str, index: int) -> dict[str, Any]:
        return {
            "kind": "sql-statement",
            "source": source,
            "index": index,
            "operation": self.operation,
            "target": self.target or "-",
            "tables": list(self.tables),
        }


def _unquoted_identifier(token: str) -> str | None:
    return token if IDENTIFIER.fullmatch(token) else None


def _split_sql(text: str) -> list[list[str]]:
    tokens = TOKEN.findall(text)
    if not tokens:
        return []
    statements: list[list[str]] = []
    current: list[str] = []
    depth = 0
    for token in tokens:
        if token == "(":
            depth += 1
        elif token == ")":
            depth -= 1
            if depth < 0:
                raise BenchmarkError("malformed SQL: unmatched closing parenthesis")
        if token == ";" and depth == 0:
            if current:
                statements.append(current)
                current = []
            continue
        current.append(token)
    if depth:
        raise BenchmarkError("malformed SQL: unmatched opening parenthesis")
    if current:
        statements.append(current)
    return statements


def _next_identifier(tokens: list[str], index: int) -> str:
    if index >= len(tokens):
        raise BenchmarkError("malformed SQL: expected table identifier")
    value = _unquoted_identifier(tokens[index])
    if value is None:
        raise BenchmarkError(f"malformed SQL table identifier: {tokens[index]}")
    return value.split(".")[-1]


def parse_sql_statement(tokens: list[str]) -> SqlStatement:
    upper = [token.upper() for token in tokens]
    operation = upper[0] if upper else ""
    tables: set[str] = set()
    target: str | None = None
    if operation == "SELECT":
        if "FROM" not in upper:
            raise BenchmarkError("malformed SELECT: missing FROM")
        for keyword in ("FROM", "JOIN"):
            for index, value in enumerate(upper):
                if value == keyword:
                    tables.add(_next_identifier(tokens, index + 1))
    elif operation == "INSERT":
        if len(upper) < 3 or upper[1] != "INTO":
            raise BenchmarkError("malformed INSERT: expected INTO")
        target = _next_identifier(tokens, 2)
        tables.add(target)
    elif operation == "UPDATE":
        target = _next_identifier(tokens, 1)
        if "SET" not in upper:
            raise BenchmarkError("malformed UPDATE: missing SET")
        tables.add(target)
    elif operation == "DELETE":
        if len(upper) < 3 or upper[1] != "FROM":
            raise BenchmarkError("malformed DELETE: expected FROM")
        target = _next_identifier(tokens, 2)
        tables.add(target)
    else:
        raise BenchmarkError(f"unsupported SQL operation: {operation or '<empty>'}")
    return SqlStatement(operation=operation, target=target, tables=tuple(sorted(tables)))


def sql_facts(root: Path, *, source_base: Path | None = None) -> list[dict[str, Any]]:
    facts: list[dict[str, Any]] = []
    for path in sorted(root.rglob("*.sql")):
        relative = path.relative_to(source_base or root).as_posix()
        try:
            statements = _split_sql(path.read_text(encoding="utf-8"))
        except OSError as exc:
            raise BenchmarkError(f"cannot read SQL {path}: {exc}") from exc
        for index, tokens in enumerate(statements, 1):
            facts.append(parse_sql_statement(tokens).fact(relative, index))
    return facts


class CloudFormationLoader(yaml.SafeLoader):
    pass


def _unknown_tag(loader: CloudFormationLoader, suffix: str, node: yaml.Node) -> Any:
    if isinstance(node, yaml.ScalarNode):
        value = loader.construct_scalar(node)
    elif isinstance(node, yaml.SequenceNode):
        value = loader.construct_sequence(node)
    else:
        value = loader.construct_mapping(node)
    return {"tag": suffix, "value": value}


CloudFormationLoader.add_multi_constructor("!", _unknown_tag)


def cloudformation_facts(path: Path) -> list[dict[str, Any]]:
    try:
        document = yaml.load(path.read_text(encoding="utf-8"), Loader=CloudFormationLoader)
    except (OSError, yaml.YAMLError) as exc:
        raise BenchmarkError(f"cannot parse CloudFormation {path}: {exc}") from exc
    if not isinstance(document, dict):
        raise BenchmarkError("CloudFormation root must be a mapping")
    facts: list[dict[str, Any]] = []
    for name, parameter in sorted(document.get("Parameters", {}).items()):
        if not isinstance(parameter, dict):
            raise BenchmarkError(f"parameter {name} must be a mapping")
        facts.append({"kind": "cfn-parameter", "name": name, "type": parameter.get("Type", "-"), "default": parameter.get("Default", "-")})
    for logical_id, resource in sorted(document.get("Resources", {}).items()):
        if not isinstance(resource, dict):
            raise BenchmarkError(f"resource {logical_id} must be a mapping")
        depends = resource.get("DependsOn", [])
        if isinstance(depends, str):
            depends = [depends]
        facts.append(
            {
                "kind": "cfn-resource",
                "logical_id": logical_id,
                "type": resource.get("Type", "-"),
                "depends_on": sorted(map(str, depends)),
                "condition": resource.get("Condition", "-"),
            }
        )
    return facts


def derive_fastapi_sql_facts(root: Path) -> dict[str, Any]:
    python_paths = sorted(root.rglob("*.py"))
    openapi_paths = sorted(root.rglob("openapi.json"))
    sql_roots = sorted({path.parent for path in root.rglob("*.sql")})
    if not python_paths or not openapi_paths or not sql_roots:
        raise BenchmarkError(f"{root}: FastAPI fixture requires Python, openapi.json and SQL")
    facts: list[dict[str, Any]] = []
    for path in python_paths:
        facts.extend(python_route_facts(path))
    facts.extend(openapi_facts(openapi_paths[0]))
    for sql_root in sql_roots:
        facts.extend(sql_facts(sql_root, source_base=root))
    ordered = sorted(facts, key=lambda item: repr(sorted(item.items())))
    return {"adapter": "fastapi-sql", "facts": ordered, "source_digest": digest_value(ordered)}


def derive_cloudformation_facts(root: Path) -> dict[str, Any]:
    candidates = sorted(list(root.rglob("*.yaml")) + list(root.rglob("*.yml")) + list(root.rglob("*.json")))
    candidates = [path for path in candidates if path.name != "state.json"]
    if not candidates:
        raise BenchmarkError(f"{root}: no CloudFormation template")
    facts = cloudformation_facts(candidates[0])
    ordered = sorted(facts, key=lambda item: repr(sorted(item.items())))
    return {"adapter": "cloudformation", "facts": ordered, "source_digest": digest_value(ordered)}
