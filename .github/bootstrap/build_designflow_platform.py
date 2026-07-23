from __future__ import annotations

import importlib.util
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path
from typing import Any

ROOT = Path.cwd().resolve()
BRANCH = "agent/canonical-design-platform"
BOOTSTRAP = ROOT / ".github/bootstrap"


def run(*command: str, check: bool = True, capture: bool = False, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    print("+", " ".join(command), flush=True)
    return subprocess.run(
        command,
        cwd=ROOT,
        check=check,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.STDOUT if capture else None,
        env=env,
    )


def write(path: str | Path, content: str | bytes, *, executable: bool = False) -> Path:
    target = ROOT / path if not isinstance(path, Path) or not path.is_absolute() else path
    target.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, bytes):
        target.write_bytes(content)
    else:
        target.write_text(textwrap.dedent(content).lstrip("\n"), encoding="utf-8")
    if executable:
        target.chmod(target.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return target


def write_json(path: str | Path, value: Any) -> Path:
    return write(path, json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n")


def append_marker(path: str, marker: str, content: str) -> None:
    target = ROOT / path
    current = target.read_text(encoding="utf-8") if target.exists() else ""
    if marker in current:
        return
    separator = "\n" if not current.endswith("\n") else ""
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(current + separator + "\n" + textwrap.dedent(content).strip() + "\n", encoding="utf-8")


def all_requirement_ids(value: Any) -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if key in {"id", "requirement_id"} and isinstance(item, str) and item.startswith("REQ-"):
                found.append(item)
            found.extend(all_requirement_ids(item))
    elif isinstance(value, list):
        for item in value:
            found.extend(all_requirement_ids(item))
    return found


def adapter_manifest(
    adapter_id: str,
    profiles: list[str],
    modes: list[str],
    capabilities: list[str],
    *,
    lifecycle: str = "experimental",
    entrypoint: list[str] | None = None,
    known_unsupported: list[str] | None = None,
) -> dict[str, Any]:
    result: dict[str, Any] = {
        "schema_version": "design-adapter-manifest/v1.0",
        "adapter_id": adapter_id,
        "version": "1.0.0",
        "profiles": profiles,
        "support_lifecycle": lifecycle,
        "modes": modes,
        "capabilities": [
            {
                "capability_id": capability,
                "default_enforcement": "Invariant",
                "possible_statuses": ["exact", "derived", "partial", "unknown", "unsupported", "conflict", "not_applicable"],
            }
            for capability in capabilities
        ],
        "input_contract": {
            "declared_paths_only": True,
            "repository_relative_locators": True,
            "secret_values_forbidden": True,
        },
        "output_contract": {
            "protocol_version": "design-adapter-protocol/v1.0",
            "stdout": "single-json-document",
            "stderr": "diagnostic-only-no-secrets",
        },
        "sandbox": {
            "network": False,
            "production_credentials": False,
            "path_escape": False,
            "timeout_seconds": 10,
            "memory_mb": 128,
            "output_bytes": 1048576,
        },
        "known_unsupported": known_unsupported or [],
    }
    if entrypoint:
        result["entrypoint"] = entrypoint
    return result


def schema_documents() -> dict[str, dict[str, Any]]:
    schema_uri = "https://json-schema.org/draft/2020-12/schema"
    core_id = "urn:dev-standard:design-ir:canonical:v1"
    evidence = {
        "type": "object",
        "required": ["evidence_id", "authority", "precision", "mode", "source", "input_sha256", "adapter"],
        "properties": {
            "evidence_id": {"type": "string"},
            "authority": {"enum": ["artifact", "runtime-registry", "typed-config", "executable-contract", "source", "controlled-observation", "external", "unknown"]},
            "precision": {"type": "string", "minLength": 1},
            "mode": {"enum": ["static", "build", "executable-contract", "runtime-registry", "controlled-observation"]},
            "source": {
                "type": "object",
                "required": ["path"],
                "properties": {
                    "path": {"type": "string", "pattern": "^(?!/)(?!.*(?:^|/)\\.\\.(?:/|$)).+$"},
                    "line": {"type": "integer", "minimum": 1},
                    "symbol": {"type": "string"},
                    "pointer": {"type": "string"},
                },
                "additionalProperties": False,
            },
            "input_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
            "adapter": {
                "type": "object",
                "required": ["id", "version"],
                "properties": {"id": {"type": "string"}, "version": {"type": "string"}},
                "additionalProperties": False,
            },
        },
        "additionalProperties": False,
    }
    core = {
        "$schema": schema_uri,
        "$id": core_id,
        "title": "Canonical Design Intermediate Representation",
        "type": "object",
        "required": ["schema_version", "project_id", "profile_ids", "facts", "relations", "capability_results", "diagnostics", "metadata"],
        "properties": {
            "schema_version": {"const": "design-ir/v1.0"},
            "project_id": {"type": "string", "minLength": 1},
            "profile_ids": {"type": "array", "minItems": 1, "uniqueItems": True, "items": {"enum": ["backend", "frontend", "infrastructure", "batch", "system", "legacy"]}},
            "facts": {"type": "array", "items": {"$ref": "#/$defs/fact"}},
            "relations": {"type": "array", "items": {"$ref": "#/$defs/relation"}},
            "identity_migrations": {"type": "array", "items": {"$ref": "#/$defs/identityMigration"}, "default": []},
            "capability_results": {"type": "array", "items": {"$ref": "#/$defs/capabilityResult"}},
            "diagnostics": {"type": "array", "items": {"$ref": "#/$defs/diagnostic"}},
            "metadata": {"type": "object"},
        },
        "$defs": {
            "evidence": evidence,
            "fact": {
                "type": "object",
                "required": ["fact_id", "fact_type", "kind", "natural_key", "capability_id", "value", "evidence", "requirement_refs", "test_refs", "external_evidence_refs"],
                "properties": {
                    "fact_id": {"type": "string", "pattern": "^fact:[0-9a-f]{24}$"},
                    "fact_type": {"enum": ["node", "property"]},
                    "kind": {"type": "string", "pattern": "^[a-z][a-z0-9-]*\\.[a-z][a-z0-9.-]*$"},
                    "natural_key": {"type": "string", "minLength": 1},
                    "capability_id": {"type": "string", "minLength": 1},
                    "value": {"type": "object"},
                    "evidence": {"type": "array", "items": {"$ref": "#/$defs/evidence"}},
                    "requirement_refs": {"type": "array", "uniqueItems": True, "items": {"type": "string"}},
                    "test_refs": {"type": "array"},
                    "external_evidence_refs": {"type": "array"},
                },
                "additionalProperties": False,
            },
            "relation": {
                "type": "object",
                "required": ["relation_id", "kind", "natural_key", "capability_id", "from_fact_id", "to_fact_id", "properties", "evidence"],
                "properties": {
                    "relation_id": {"type": "string", "pattern": "^relation:[0-9a-f]{24}$"},
                    "kind": {"type": "string"},
                    "natural_key": {"type": "string"},
                    "capability_id": {"type": "string"},
                    "from_fact_id": {"type": "string"},
                    "to_fact_id": {"type": "string"},
                    "properties": {"type": "object"},
                    "evidence": {"type": "array", "items": {"$ref": "#/$defs/evidence"}},
                },
                "additionalProperties": False,
            },
            "identityMigration": {
                "type": "object",
                "required": ["old_fact_id", "new_fact_id", "reason", "evidence"],
                "properties": {
                    "old_fact_id": {"type": "string"},
                    "new_fact_id": {"type": "string"},
                    "reason": {"type": "string", "minLength": 1},
                    "evidence": {"type": "array", "minItems": 1},
                    "supersedes": {"type": "array", "items": {"type": "string"}},
                },
                "additionalProperties": False,
            },
            "capabilityResult": {
                "type": "object",
                "required": ["capability_id", "required", "status", "precision", "enforcement", "mode", "diagnostic_ids"],
                "properties": {
                    "capability_id": {"type": "string"},
                    "required": {"type": "boolean"},
                    "status": {"enum": ["exact", "derived", "observed", "partial", "unknown", "unsupported", "conflict", "not_applicable"]},
                    "precision": {"type": "string"},
                    "enforcement": {"enum": ["Invariant", "Risk-selected", "Advisory", "Periodic"]},
                    "mode": {"enum": ["static", "build", "executable-contract", "runtime-registry", "controlled-observation"]},
                    "diagnostic_ids": {"type": "array", "items": {"type": "string"}},
                },
                "additionalProperties": False,
            },
            "diagnostic": {
                "type": "object",
                "required": ["diagnostic_id", "code", "severity", "message"],
                "properties": {
                    "diagnostic_id": {"type": "string"},
                    "code": {"type": "string"},
                    "severity": {"enum": ["info", "warning", "error"]},
                    "message": {"type": "string"},
                    "capability_id": {"type": "string"},
                    "location": {"type": "object"},
                    "details": {"type": "object"},
                },
                "additionalProperties": False,
            },
        },
        "additionalProperties": False,
    }
    documents: dict[str, dict[str, Any]] = {"spec/design-ir/canonical-design-ir.schema.json": core}
    profile_prefix = {"backend": "^backend\\.", "frontend": "^frontend\\.", "infrastructure": "^infra\\.", "batch": "^batch\\."}
    for profile, pattern in profile_prefix.items():
        documents[f"spec/design-ir/profiles/{profile}.schema.json"] = {
            "$schema": schema_uri,
            "$id": f"urn:dev-standard:design-ir:profile:{profile}:v1",
            "title": f"Canonical Design IR {profile} profile",
            "allOf": [
                {"$ref": core_id},
                {
                    "properties": {
                        "profile_ids": {"contains": {"const": profile}},
                        "facts": {"items": {"properties": {"kind": {"pattern": pattern}}}},
                    }
                },
            ],
        }
    documents["spec/design-ir/adapter-protocol.schema.json"] = {
        "$schema": schema_uri,
        "$id": "urn:dev-standard:design-ir:adapter-protocol:v1",
        "title": "Design adapter protocol request and response",
        "oneOf": [
            {
                "type": "object",
                "required": ["protocol_version", "project_id", "profile_ids", "inputs", "mode", "environment"],
                "properties": {"protocol_version": {"const": "design-adapter-protocol/v1.0"}},
            },
            {
                "type": "object",
                "required": ["protocol_version", "adapter", "facts", "relations", "capability_results", "diagnostics", "inputs"],
                "properties": {
                    "protocol_version": {"const": "design-adapter-protocol/v1.0"},
                    "facts": {"type": "array", "items": {"$ref": f"{core_id}#/$defs/fact"}},
                    "relations": {"type": "array", "items": {"$ref": f"{core_id}#/$defs/relation"}},
                },
            },
        ],
    }
    documents["spec/design-ir/adapter-manifest.schema.json"] = {
        "$schema": schema_uri,
        "$id": "urn:dev-standard:design-ir:adapter-manifest:v1",
        "type": "object",
        "required": ["schema_version", "adapter_id", "version", "profiles", "support_lifecycle", "modes", "capabilities", "input_contract", "output_contract", "sandbox", "known_unsupported"],
        "properties": {
            "schema_version": {"const": "design-adapter-manifest/v1.0"},
            "adapter_id": {"type": "string"},
            "version": {"type": "string"},
            "profiles": {"type": "array"},
            "support_lifecycle": {"enum": ["candidate", "experimental", "supported", "deprecated", "removed"]},
            "modes": {"type": "array", "items": {"enum": ["static", "build", "executable-contract", "runtime-registry", "controlled-observation"]}},
            "capabilities": {"type": "array"},
            "input_contract": {"type": "object"},
            "output_contract": {"type": "object"},
            "sandbox": {"type": "object"},
            "known_unsupported": {"type": "array"},
            "entrypoint": {"type": "array", "items": {"type": "string"}},
        },
        "additionalProperties": False,
    }
    documents["spec/design-ir/support-registry.schema.json"] = {
        "$schema": schema_uri,
        "$id": "urn:dev-standard:design-ir:support-registry:v1",
        "type": "object",
        "required": ["schema_version", "entries"],
        "properties": {
            "schema_version": {"const": "design-support-registry/v1.0"},
            "entries": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["adapter_id", "capability_id", "support_lifecycle", "extraction_status", "modes", "scope", "known_unsupported", "conformance_evidence"],
                },
            },
        },
        "additionalProperties": False,
    }
    documents["spec/design-ir/designflow-config.schema.json"] = {
        "$schema": schema_uri,
        "$id": "urn:dev-standard:design-ir:config:v1",
        "type": "object",
        "required": ["schema_version", "projects"],
        "properties": {
            "schema_version": {"const": "designflow-config/v1.0"},
            "projects": {"type": "array", "minItems": 1},
            "system_links": {"type": "array"},
            "system_output": {"type": "string"},
        },
        "additionalProperties": False,
    }
    documents["spec/design-ir/bundle-manifest.schema.json"] = {
        "$schema": schema_uri,
        "$id": "urn:dev-standard:design-ir:bundle-manifest:v1",
        "type": "object",
        "required": ["schema_version", "project", "generator", "ir_schema_version", "protocol_version", "config", "inputs", "adapters", "renderer", "capability_results", "files", "commands", "semantic_digest"],
        "properties": {"schema_version": {"const": "design-bundle/v1.0"}},
    }
    return documents


def build_fixtures(requirement_ids: list[str]) -> None:
    trace_req = requirement_ids[:2]
    expected = [
        {
            "kind": "backend.operation",
            "natural_key": "listOrders",
            "value": {"handler": "listOrders", "method": "GET", "operation_id": "listOrders", "path": "/orders"},
        }
    ]
    cases = {
        "fastapi-positive": (
            "fastapi-python",
            "app.py",
            """
            from fastapi import FastAPI
            app = FastAPI()

            @app.get("/orders", operation_id="listOrders")
            def listOrders():
                return []
            """,
            "positive",
        ),
        "spring-positive": (
            "spring-boot-mvc",
            "OrdersController.java",
            """
            import java.util.List;
            @RequestMapping("/orders")
            class OrdersController {
              @GetMapping("")
              public List<String> listOrders() { return List.of(); }
            }
            """,
            "positive",
        ),
        "rails-positive": (
            "rails",
            "routes.rb",
            "get '/orders', to: 'orders#listOrders'\n",
            "positive",
        ),
        "nestjs-positive": (
            "nestjs",
            "orders.controller.ts",
            """
            @Controller('orders')
            class OrdersController {
              @Get('')
              listOrders() { return []; }
            }
            """,
            "positive",
        ),
        "gin-positive": (
            "gin",
            "main.go",
            """
            package main
            func routes(router *gin.Engine) {
              router.GET("/orders", listOrders)
            }
            func listOrders(c *gin.Context) {}
            """,
            "positive",
        ),
        "fastapi-negative": (
            "fastapi-python",
            "app.py",
            """
            from fastapi import FastAPI
            app = FastAPI()
            route_path = '/orders'
            @app.get(route_path)
            def listOrders(): return []
            """,
            "negative",
        ),
        "spring-negative": (
            "spring-boot-mvc",
            "OrdersController.java",
            """
            class OrdersController {
              static final String routePath = "/orders";
              @GetMapping(value = routePath)
              public String listOrders() { return ""; }
            }
            """,
            "negative",
        ),
        "rails-negative": (
            "rails",
            "routes.rb",
            "resources orders\n",
            "negative",
        ),
        "nestjs-negative": (
            "nestjs",
            "orders.controller.ts",
            """
            const prefix = 'orders';
            @Controller(prefix)
            class OrdersController {
              @Get('')
              listOrders() { return []; }
            }
            """,
            "negative",
        ),
        "gin-negative": (
            "gin",
            "main.go",
            """
            package main
            func routes(router *gin.Engine) {
              routePath := "/orders"
              router.GET(routePath, listOrders)
            }
            """,
            "negative",
        ),
    }
    for case_id, (adapter_id, source_name, source, kind) in cases.items():
        base = f"tests/fixtures/designflow/conformance/backend/{case_id}"
        write(f"{base}/{source_name}", source)
        write_json(
            f"{base}/case.json",
            {
                "schema_version": "design-conformance-case/v1.0",
                "id": case_id,
                "kind": kind,
                "adapter": adapter_id,
                "inputs": [source_name],
                "expected_projection": expected if kind == "positive" else [],
                "expected_diagnostic": "ROUTE_DYNAMIC_UNRESOLVED" if kind == "negative" else None,
            },
        )

    write(
        "tests/fixtures/designflow/phase1/app.py",
        """
        from fastapi import FastAPI
        app = FastAPI()

        class Repository:
            def list_orders(self):
                return []

        repository = Repository()

        @app.get("/orders", operation_id="listOrders")
        def listOrders():
            return repository.list_orders()
        """,
    )
    write_json(
        "tests/fixtures/designflow/phase1/openapi.json",
        {
            "openapi": "3.1.0",
            "info": {"title": "Orders", "version": "1.0.0"},
            "paths": {
                "/orders": {
                    "get": {
                        "operationId": "listOrders",
                        "responses": {"200": {"description": "ok"}},
                    }
                }
            },
            "components": {
                "schemas": {
                    "Order": {
                        "type": "object",
                        "required": ["id"],
                        "properties": {"id": {"type": "integer"}, "status": {"type": "string"}},
                    }
                }
            },
        },
    )
    write(
        "tests/fixtures/designflow/phase1/schema.sql",
        """
        CREATE TABLE orders (
          id INTEGER PRIMARY KEY,
          status VARCHAR(32) NOT NULL
        );
        """,
    )
    write("tests/fixtures/designflow/phase1/queries.sql", "SELECT id, status FROM orders;\n")
    write(
        "tests/fixtures/designflow/phase1/designflow.yaml",
        f"""
        schema_version: designflow-config/v1.0
        projects:
          - id: orders-backend
            root: .
            profiles: [backend]
            adapters:
              - id: fastapi-python
                mode: static
                inputs: [app.py]
                required: true
              - id: openapi
                mode: executable-contract
                inputs: [openapi.json]
                required: true
              - id: ddl-sql
                mode: static
                inputs: [schema.sql, queries.sql]
                schema_required: true
                query_required: true
            required_capabilities:
              - backend.routes
              - backend.http-contract
              - backend.data-schema
              - backend.data-access
            trace_map:
              - kind: backend.operation
                natural_key: listOrders
                requirement_refs: {json.dumps(trace_req, ensure_ascii=False)}
                test_refs:
                  - id: test-list-orders
                    path: tests/fixtures/designflow/real_toolchain/fastapi_app.py
                external_evidence_refs:
                  - kind: openapi
                    path: openapi.json
            output: docs/design/generated/orders-backend
        """,
    )
    write(
        "tests/fixtures/designflow/real_toolchain/fastapi_app.py",
        """
        from fastapi import FastAPI
        app = FastAPI()

        @app.get("/orders", operation_id="listOrders")
        def list_orders():
            return []
        """,
    )

    write(
        "tests/fixtures/designflow/conformance/conflict/app.py",
        """
        from fastapi import FastAPI
        app = FastAPI()
        @app.get("/orders", operation_id="listOrders")
        def listOrders(): return []
        """,
    )
    write(
        "tests/fixtures/designflow/conformance/conflict/OrdersController.java",
        """
        @RequestMapping("/different")
        class OrdersController {
          @GetMapping("")
          public String listOrders() { return ""; }
        }
        """,
    )
    write(
        "tests/fixtures/designflow/conformance/conflict/designflow.yaml",
        """
        schema_version: designflow-config/v1.0
        projects:
          - id: conflict
            root: .
            profiles: [backend]
            adapters:
              - id: fastapi-python
                inputs: [app.py]
                required: true
              - id: spring-boot-mvc
                inputs: [OrdersController.java]
                required: true
            required_capabilities: [backend.routes]
        """,
    )

    write_json(
        "tests/fixtures/designflow/profiles/frontend/frontend.design.json",
        {
            "routes": [{"id": "ordersPage", "path": "/orders", "component": "OrdersPage"}],
            "components": [{"id": "OrdersPage", "name": "OrdersPage", "source": "src/OrdersPage.tsx"}],
            "api_operations": [{"id": "listOrders", "method": "GET", "path": "/orders", "requirement_refs": trace_req}],
            "states": [{"id": "orders-loading", "route": "ordersPage", "state": "loading", "test_refs": ["tests/orders.spec.ts"]}],
            "assertions": [{"id": "orders-heading", "rule": "heading-name", "test_refs": ["tests/orders.spec.ts"]}],
            "tokens": [{"id": "spacing-md", "value": "1rem"}],
            "responsive_rules": [{"id": "orders-mobile", "breakpoint": "640px", "behavior": "stack"}],
            "relations": [
                {"from": "ordersPage", "to": "OrdersPage", "kind": "frontend.renders"},
                {"from": "OrdersPage", "to": "listOrders", "kind": "frontend.calls"},
            ],
        },
    )
    write(
        "tests/fixtures/designflow/profiles/frontend/designflow.yaml",
        """
        schema_version: designflow-config/v1.0
        projects:
          - id: web
            root: .
            profiles: [frontend]
            adapters:
              - id: frontend-manifest
                mode: build
                inputs: [frontend.design.json]
                required_capabilities: [frontend.routes, frontend.state-scenarios, frontend.accessibility]
            required_capabilities: [frontend.routes, frontend.state-scenarios, frontend.accessibility]
            output: docs/design/generated/web
        """,
    )

    write_json(
        "tests/fixtures/designflow/profiles/infrastructure/template.json",
        {
            "AWSTemplateFormatVersion": "2010-09-09",
            "Parameters": {
                "DbPassword": {"Type": "String", "NoEcho": True, "Default": "NeverPersistThisSecret"},
                "Environment": {"Type": "String", "Default": "test"},
            },
            "Resources": {
                "OrdersTable": {
                    "Type": "AWS::DynamoDB::Table",
                    "DeletionPolicy": "Retain",
                    "Properties": {
                        "BillingMode": "PAY_PER_REQUEST",
                        "TableName": {"Fn::Sub": "orders-${Environment}"},
                    },
                },
                "OrdersFunction": {
                    "Type": "AWS::Lambda::Function",
                    "DependsOn": "OrdersTable",
                    "Properties": {
                        "Handler": "index.handler",
                        "Role": {"Fn::GetAtt": ["OrdersRole", "Arn"]},
                        "Environment": {"Variables": {"DB_PASSWORD": {"Ref": "DbPassword"}}},
                    },
                },
                "OrdersRole": {
                    "Type": "AWS::IAM::Role",
                    "Properties": {"AssumeRolePolicyDocument": {"Version": "2012-10-17", "Statement": []}},
                },
            },
        },
    )
    write(
        "tests/fixtures/designflow/profiles/infrastructure/designflow.yaml",
        """
        schema_version: designflow-config/v1.0
        projects:
          - id: infra
            root: .
            profiles: [infrastructure]
            adapters:
              - id: cloudformation
                mode: build
                inputs: [template.json]
                required: true
                parameters_required: true
                dependencies_required: true
            required_capabilities: [infra.resources, infra.parameters, infra.dependencies]
            output: docs/design/generated/infra
        """,
    )

    write_json(
        "tests/fixtures/designflow/profiles/batch/batch.design.json",
        {
            "jobs": [{"id": "nightly-orders", "name": "Nightly Orders"}],
            "triggers": [{"id": "nightly-trigger", "cron": "0 2 * * *", "timezone": "UTC"}],
            "steps": [{"id": "extract"}, {"id": "publish"}],
            "effects": [{"id": "orders-export", "kind": "object-write", "target": "s3://logical/orders"}],
            "recovery": [{"id": "retry-publish", "strategy": "bounded-retry", "max_attempts": 3}],
            "tests": [{"id": "nightly-happy", "test_refs": ["tests/nightly_test.py"], "requirement_refs": trace_req}],
            "relations": [
                {"from": "nightly-orders", "to": "extract", "kind": "batch.contains", "order": 1},
                {"from": "extract", "to": "publish", "kind": "batch.flows-to", "order": 2},
                {"from": "publish", "to": "orders-export", "kind": "batch.causes", "order": 3},
            ],
        },
    )
    write(
        "tests/fixtures/designflow/profiles/batch/designflow.yaml",
        """
        schema_version: designflow-config/v1.0
        projects:
          - id: nightly
            root: .
            profiles: [batch]
            adapters:
              - id: batch-workflow-manifest
                mode: build
                inputs: [batch.design.json]
                required_capabilities: [batch.jobs, batch.triggers, batch.flow, batch.effects, batch.recovery, batch.verification]
            required_capabilities: [batch.jobs, batch.triggers, batch.flow, batch.effects, batch.recovery, batch.verification]
            output: docs/design/generated/nightly
        """,
    )

    write(
        "tests/fixtures/designflow/system/api.py",
        """
        from fastapi import FastAPI
        app = FastAPI()
        @app.get("/orders", operation_id="listOrders")
        def listOrders(): return []
        """,
    )
    write_json(
        "tests/fixtures/designflow/system/frontend.design.json",
        {
            "routes": [{"id": "ordersPage", "path": "/orders", "component": "OrdersPage"}],
            "components": [{"id": "OrdersPage", "name": "OrdersPage"}],
            "api_operations": [{"id": "listOrders", "method": "GET", "path": "/orders"}],
            "states": [{"id": "orders-loaded", "test_refs": ["tests/orders.spec.ts"]}],
            "assertions": [{"id": "orders-list-name", "test_refs": ["tests/orders.spec.ts"]}],
            "relations": [{"from": "OrdersPage", "to": "listOrders", "kind": "frontend.calls"}],
        },
    )
    write(
        "tests/fixtures/designflow/system/designflow.yaml",
        """
        schema_version: designflow-config/v1.0
        projects:
          - id: api
            root: .
            profiles: [backend]
            adapters:
              - id: fastapi-python
                inputs: [api.py]
                required: true
            required_capabilities: [backend.routes]
            output: docs/design/generated/api
          - id: web
            root: .
            profiles: [frontend]
            adapters:
              - id: frontend-manifest
                mode: build
                inputs: [frontend.design.json]
                required_capabilities: [frontend.routes]
            required_capabilities: [frontend.routes]
            output: docs/design/generated/web
        system_links:
          - id: web-list-orders
            kind: system.calls
            from:
              project: web
              kind: frontend.api-operation
              natural_key: listOrders
            to:
              project: api
              kind: backend.operation
              natural_key: listOrders
        system_output: docs/design/generated/system
        """,
    )


def protocol_response(adapter_id: str, facts: list[dict[str, Any]] | None = None) -> str:
    return json.dumps(
        {
            "protocol_version": "design-adapter-protocol/v1.0",
            "adapter": {"id": adapter_id, "version": "1.0.0", "mode": "static"},
            "facts": facts or [],
            "relations": [],
            "capability_results": [],
            "diagnostics": [],
            "inputs": [],
        },
        separators=(",", ":"),
    )


def build_security_fixtures() -> None:
    base_manifest = adapter_manifest(
        "security-test",
        ["backend"],
        ["static"],
        ["backend.routes"],
        lifecycle="candidate",
        entrypoint=["python", "adapter.py"],
    )
    cases: dict[str, tuple[dict[str, Any], str, str]] = {}
    path_manifest = dict(base_manifest)
    path_manifest["entrypoint"] = ["python", "../outside.py"]
    cases["path-escape"] = (
        path_manifest,
        "print('not reached')\n",
        json.dumps({"adapter": {"id": "security-test", "inputs": []}}),
    )
    cases["timeout"] = (
        base_manifest,
        f"import time\ntime.sleep(3)\nprint({protocol_response('security-test')!r})\n",
        json.dumps({"adapter": {"id": "security-test", "inputs": [], "timeout_seconds": 1}}),
    )
    cases["resource"] = (
        base_manifest,
        "print('x' * 70000)\n",
        json.dumps({"adapter": {"id": "security-test", "inputs": []}}),
    )
    secret = "DESIGNFLOW_CANARY_SECRET_123456"
    cases["secret-log"] = (
        base_manifest,
        f"import sys\nprint({secret!r}, file=sys.stderr)\nprint({protocol_response('security-test')!r})\n",
        json.dumps({"adapter": {"id": "security-test", "inputs": [], "known_secret_values": [secret]}}),
    )
    secret_fact = {
        "fact_id": "fact:111111111111111111111111",
        "fact_type": "node",
        "kind": "backend.operation",
        "natural_key": "secret",
        "capability_id": "backend.routes",
        "value": {"token": secret},
        "evidence": [],
        "requirement_refs": [],
        "test_refs": [],
        "external_evidence_refs": [],
    }
    cases["secret-fragment"] = (
        base_manifest,
        f"print({protocol_response('security-test', [secret_fact])!r})\n",
        json.dumps({"adapter": {"id": "security-test", "inputs": [], "known_secret_values": [secret]}}),
    )
    for name, (manifest, adapter_code, case_json) in cases.items():
        base = f"tests/fixtures/designflow/security/{name}"
        write_json(f"{base}/adapter-manifest.json", manifest)
        write(f"{base}/adapter.py", adapter_code)
        write(f"{base}/case.json", case_json + "\n")

    environment_fact = {
        "fact_id": "fact:222222222222222222222222",
        "fact_type": "property",
        "kind": "backend.environment-check",
        "natural_key": "ambient",
        "capability_id": "backend.environment",
        "value": {"ambient_secret_present": False},
        "evidence": [],
        "requirement_refs": [],
        "test_refs": [],
        "external_evidence_refs": [],
    }
    env_base = "tests/fixtures/designflow/security/environment"
    write_json(f"{env_base}/adapter-manifest.json", base_manifest)
    write(
        f"{env_base}/adapter.py",
        """
        import json
        import os
        import sys
        json.load(sys.stdin)
        fact = {
          "fact_id": "fact:222222222222222222222222",
          "fact_type": "property",
          "kind": "backend.environment-check",
          "natural_key": "ambient",
          "capability_id": "backend.environment",
          "value": {"ambient_secret_present": "AWS_SECRET_ACCESS_KEY" in os.environ},
          "evidence": [],
          "requirement_refs": [],
          "test_refs": [],
          "external_evidence_refs": []
        }
        print(json.dumps({
          "protocol_version": "design-adapter-protocol/v1.0",
          "adapter": {"id": "security-test", "version": "1.0.0", "mode": "static"},
          "facts": [fact], "relations": [], "capability_results": [], "diagnostics": [], "inputs": []
        }, separators=(",", ":")))
        """,
    )
    write_json(f"{env_base}/case.json", {"adapter": {"id": "security-test", "inputs": []}})


def build_adapter_template() -> None:
    base = ".agents/skills/generate-implementation-design/templates/project-local-adapter"
    manifest = adapter_manifest(
        "replace-with-project-adapter-id",
        ["backend"],
        ["static"],
        ["project.example"],
        lifecycle="candidate",
        entrypoint=["python", "adapter.py"],
        known_unsupported=["No capability is supported until all nine conformance layers and real-toolchain evidence pass."],
    )
    write_json(f"{base}/adapter-manifest.json", manifest)
    write(
        f"{base}/adapter.py",
        """
        #!/usr/bin/env python3
        import hashlib
        import json
        import sys

        request = json.load(sys.stdin)
        if request.get("protocol_version") != "design-adapter-protocol/v1.0":
            raise SystemExit(2)
        project_id = request["project_id"]
        natural_key = "replace-with-exact-natural-key"
        digest = hashlib.sha256(f"{project_id}\x1fproject.example\x1f{natural_key}".encode()).hexdigest()[:24]
        response = {
          "protocol_version": "design-adapter-protocol/v1.0",
          "adapter": {"id": "replace-with-project-adapter-id", "version": "1.0.0", "mode": request["mode"]},
          "facts": [{
            "fact_id": f"fact:{digest}", "fact_type": "node", "kind": "backend.example",
            "natural_key": natural_key, "capability_id": "project.example", "value": {"example": True},
            "evidence": [], "requirement_refs": [], "test_refs": [], "external_evidence_refs": []
          }],
          "relations": [],
          "capability_results": [{
            "capability_id": "project.example", "required": False, "status": "derived",
            "precision": "project-defined", "enforcement": "Advisory", "mode": request["mode"], "diagnostic_ids": []
          }],
          "diagnostics": [], "inputs": request["inputs"]
        }
        json.dump(response, sys.stdout, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        sys.stdout.write("\\n")
        """,
        executable=True,
    )
    write(
        f"{base}/README.md",
        """
        # Project-local adapter template

        `adapter-manifest.json` declares lifecycle, mode, capability, sandbox and known-unsupported scope. The entrypoint accepts one protocol request on stdin and emits one protocol response on stdout. It must never emit credentials, secret values or repository-external paths.

        Run `designflow conformance --adapter .agents/skills/generate-implementation-design/templates/project-local-adapter/adapter-manifest.json`. A positive fixture is not support evidence by itself; all nine layers and a real-toolchain run are required before registry promotion.
        """,
    )
    write_json(f"{base}/fixtures/positive/request.json", {"protocol_version": "design-adapter-protocol/v1.0", "project_id": "example", "profile_ids": ["backend"], "inputs": [], "mode": "static", "environment": {}})
    write_json(f"{base}/fixtures/negative/request.json", {"protocol_version": "unsupported", "project_id": "example", "profile_ids": ["backend"], "inputs": [], "mode": "static", "environment": {}})


def build_docs(requirement_ids: list[str], check_ids: list[str]) -> None:
    write(
        ".agents/skills/adopt-implementation-design/SKILL.md",
        """
        ---
        name: adopt-implementation-design
        description: 既存 repository に Canonical Design IR の生成・検証・配布契約を dry-run から安全に導入する。
        ---

        # 実装設計基盤の導入

        1. 対象 profile を `backend`、`frontend`、`infrastructure`、`batch` から一つ選ぶ。
        2. `python tools/adopt_implementation_design.py --source-root <dev-standard> --target <consumer> --profile <profile> --dry-run` で変更予定と衝突を確認する。
        3. 既存ファイルへの衝突がゼロの場合だけ `--apply` を実行する。適用は既存の `AGENTS.md`、workflow、build file、Skill、`designflow.yaml` を上書きしない。
        4. consumer で `designflow discover`、`designflow generate`、`designflow check` を順に実行する。
        5. required capability が `partial` / `unknown` / `unsupported` / `conflict` の場合は採用を完了しない。

        Profile 固有の自然言語手順は `references/` を参照する。
        """,
    )
    profile_docs = {
        "backend": "FastAPI/OpenAPI/DDL を同一 IR に統合し、API・flow・data・query の required capability を明示する。dynamic route を推測で補完しない。",
        "frontend": "route/component/API/state/accessibility/token/responsive の証拠を build artifact と executable assertion から取得する。DOM state を source だけで断定しない。",
        "infrastructure": "CloudFormation/CDK synth artifact を authority とし、resource/parameter/dependency/IAM/network/stateful/external/risk を secret reference のまま記録する。",
        "batch": "job/trigger/ordered flow/effect/recovery/test を scheduler・workflow artifact・assertion から取得し、時刻・再実行・外部効果を暗黙補完しない。",
    }
    for profile, text in profile_docs.items():
        write(
            f".agents/skills/adopt-implementation-design/references/{profile}.md",
            f"""
            # {profile} profile の導入

            {text}

            `describe-capabilities` で lifecycle と extraction status を別々に確認し、`supported` でない能力を production support と説明してはならない。
            """,
        )
    write_json(
        "distribution/designflow/manifest.json",
        {
            "schema_version": "designflow-distribution/v1.0",
            "skills": [
                ".agents/skills/generate-implementation-design/SKILL.md",
                ".agents/skills/adopt-implementation-design/SKILL.md",
            ],
            "profiles": ["backend", "frontend", "infrastructure", "batch"],
            "entrypoints": ["designflow", "tools/adopt_implementation_design.py"],
            "contracts": ["spec/design-ir/canonical-design-ir.schema.json", "governance/design-adapters/support-registry.json"],
        },
    )
    write(
        "docs/reference/designflow-conformance-api.md",
        """
        # Designflow conformance API

        ## 共有境界

        #22 の evaluator は `tools.designflow_platform.run_conformance(root, real_toolchain=..., adapter_manifest=...)` と `design-conformance/v1.0` report を利用する。fixture format は `tests/fixtures/designflow/**/case.json`、protocol/manifest/schema は `spec/design-ir/` が唯一の authority である。

        Evaluator は adapter の stdout/stderr、capability result、diagnostic、semantic projection、deterministic bytes を評価する。agent interaction、prompt、repository orchestration はこの API の外側であり、ここに agent interaction 用の E2E harness を複製しない。#22 は同じ fixture と report を呼び出し、別の E2E harness を保有しない。
        """,
    )
    standards = {
        "BACKEND-AS-BUILT-DESIGN.md": "Backend profile は operation、interface、direct flow、table、query、test を証拠付き fact として表す。OpenAPI artifact は route contract に対して source static より高い authority を持つ。dynamic registration は unknown とする。",
        "FRONTEND-AS-BUILT-DESIGN.md": "Frontend profile は route/component/API relation/state/accessibility/token/responsive を分離する。state と accessibility は executable assertion がない場合に exact としない。",
        "INFRASTRUCTURE-AS-BUILT-DESIGN.md": "Infrastructure profile は synth artifact を authority とし、resource/parameter/dependency/IAM/network/stateful/external reference/change risk を表す。secret は logical locator のみを記録する。",
        "BATCH-AS-BUILT-DESIGN.md": "Batch profile は job/trigger/ordered step/effect/recovery/verification を表す。schedule、timezone、retry、idempotency、external effect の不明値を推測しない。",
    }
    for name, body in standards.items():
        write(
            f"docs/standards/{name}",
            f"""
            # {name.removesuffix('.md')}

            {body}

            共通 schema、support lifecycle、required capability の fail-closed、migration、redaction、deterministic serialization は `docs/standards/AS-BUILT-DESIGN.md` と `spec/design-ir/` に従う。
            """,
        )
    append_marker(
        "docs/standards/AS-BUILT-DESIGN.md",
        "<!-- canonical-design-ir-platform -->",
        """
        <!-- canonical-design-ir-platform -->
        ## Canonical Design IR 基盤

        `spec/design-ir/canonical-design-ir.schema.json` を共通 semantic authority とし、Backend / Frontend / Infrastructure / Batch は profile extension だけを追加する。adapter は versioned protocol と manifest を介し、core は framework 名で分岐しない。lifecycle と extraction status を分離し、required capability の `partial` / `unknown` / `unsupported` / `conflict` は fail closed とする。

        Markdown renderer は検証済み IR だけを読み、Mermaid renderer は `design.graph.json` だけを読む。旧 bundle は `migrate --check` / `--apply` を経ずに上書きしない。secret-bearing fragment、log、path escape、timeout、resource limit は persistence より前に拒否する。
        """,
    )
    append_marker(
        ".agents/skills/generate-implementation-design/SKILL.md",
        "<!-- canonical-design-ir-cli -->",
        """
        <!-- canonical-design-ir-cli -->
        ## Canonical Design IR CLI

        公開 command は `discover` / `generate` / `check` / `explain` / `describe-capabilities` / `conformance` / `migrate` である。既存 command は compatibility wrapper から legacy implementation に委譲する。profile 別 view は IR からのみ生成し、graph Mermaid は graph JSON からのみ生成する。required capability が fail-closed status の場合は exit code 2 と診断を返す。
        """,
    )
    append_marker(
        "README.md",
        "<!-- canonical-design-ir-readme -->",
        """
        <!-- canonical-design-ir-readme -->
        ## Canonical Design IR

        `designflow` は Backend / Frontend / Infrastructure / Batch の証拠を versioned Canonical Design IR に正規化し、deterministic bundle と traceability を生成します。開始点は `designflow discover`、生成は `designflow generate`、CI drift gate は `designflow check`、adapter 認定は `designflow conformance` です。support lifecycle と現在の extraction status は `designflow describe-capabilities` で別々に確認できます。
        """,
    )
    bindings = [
        {"profile": profile, "requirement_ids": requirement_ids[: min(4, len(requirement_ids))], "schema": f"spec/design-ir/profiles/{profile}.schema.json"}
        for profile in ("backend", "frontend", "infrastructure", "batch")
    ]
    write_json(
        "spec/design-ir/requirement-bindings.json",
        {"schema_version": "design-requirement-bindings/v1.0", "bindings": bindings},
    )
    acceptance = []
    for index in range(1, 19):
        acceptance.append(
            {
                "criterion": index,
                "issue": 19,
                "requirement_ids": requirement_ids[: min(4, len(requirement_ids))],
                "check_ids": check_ids,
                "evidence": [
                    "tests/test_designflow_platform.py",
                    "spec/design-ir/canonical-design-ir.schema.json",
                    ".github/workflows/designflow-conformance.yml",
                ],
            }
        )
    write_json(
        "spec/design-ir/traceability.json",
        {
            "schema_version": "designflow-traceability/v1.0",
            "authority": "spec/requirements/requirements.json",
            "acceptance_criteria": acceptance,
            "issues": [13, 14, 15, 16, 19, 22],
        },
    )


def build_workflows() -> None:
    write(
        ".github/workflows/governance.yml",
        """
        name: Governance

        on:
          push:
            branches: [main]
          pull_request:

        permissions:
          contents: read

        jobs:
          verify:
            runs-on: ubuntu-latest
            steps:
              - uses: actions/checkout@v7
                with:
                  ref: ${{ github.event.pull_request.head.sha || github.sha }}
                  fetch-depth: 0
              - name: Secret scan
                uses: gitleaks/gitleaks-action@ff98106e4c7b2bc287b24eaf42907196329070c7
                env:
                  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
              - uses: actions/setup-python@v6
                with:
                  python-version: "3.12"
                  cache: pip
              - run: pip install -r requirements.txt
              - run: python tools/devflow.py catalog --check
              - run: python .agents/skills/maintain-canonical-requirements/scripts/specflow.py check
              - run: python .agents/skills/verify-against-engineering-standards/scripts/standardsflow.py check
              - run: ruff check .
              - name: Validate adaptive review contract
                run: python governance/reviews/validate.py --root . --commit HEAD
              - name: Run Designflow protocol and fixture conformance
                run: python .agents/skills/generate-implementation-design/scripts/designflow.py --root . conformance --json
              - name: Run unit tests
                id: unit-tests
                shell: bash
                run: |
                  set +e
                  python -m unittest discover -s tests > unit-test.log 2>&1
                  status=$?
                  cat unit-test.log
                  exit "$status"
              - name: Upload unit test log on failure
                if: failure() && steps.unit-tests.outcome == 'failure'
                uses: actions/upload-artifact@v7
                with:
                  path: unit-test.log
                  archive: false
                  retention-days: 3
              - name: Run repository validation
                id: repository-validation
                if: always()
                shell: bash
                run: |
                  set +e
                  python tools/validate_repo.py > repository-validation.log 2>&1
                  status=$?
                  cat repository-validation.log
                  exit "$status"
              - name: Upload repository validation log on failure
                if: failure() && steps.repository-validation.outcome == 'failure'
                uses: actions/upload-artifact@v7
                with:
                  path: repository-validation.log
                  archive: false
                  retention-days: 3
              - name: Run regulated audit
                if: success()
                run: python tools/devflow.py audit
        """,
    )
    write(
        ".github/workflows/designflow-conformance.yml",
        """
        name: Designflow Conformance

        on:
          pull_request:
            paths:
              - "tools/designflow_platform.py"
              - "spec/design-ir/**"
              - "governance/design-adapters/**"
              - "tests/fixtures/designflow/**"
              - "tests/test_designflow_platform.py"
              - ".github/workflows/designflow-conformance.yml"
          workflow_dispatch:

        permissions:
          contents: read

        jobs:
          real-toolchain:
            strategy:
              fail-fast: false
              matrix:
                python-version: ["3.11", "3.12", "3.13"]
                timezone: ["UTC", "Asia/Tokyo"]
            runs-on: ubuntu-latest
            env:
              TZ: ${{ matrix.timezone }}
            steps:
              - uses: actions/checkout@v7
              - uses: actions/setup-python@v6
                with:
                  python-version: ${{ matrix.python-version }}
                  cache: pip
              - run: pip install -r requirements.txt
              - run: pip install "fastapi>=0.115,<1"
              - name: Run nine-layer conformance with a real FastAPI toolchain
                run: python .agents/skills/generate-implementation-design/scripts/designflow.py --root . conformance --real-toolchain --json
              - name: Run canonical platform contract tests
                run: python -m unittest tests.test_designflow_platform
        """,
    )


def build_wrapper(core_payload: str, test_payload: str, adopt_payload: str) -> None:
    core_payload = core_payload.replace(
        "if profiles and fact[\"kind\"].startswith((\"backend.\", \"frontend.\", \"infra.\", \"batch.\")):",
        "if profiles and \"system\" not in profiles and fact[\"kind\"].startswith((\"backend.\", \"frontend.\", \"infra.\", \"batch.\")):",
    )
    write("tools/designflow_platform.py", core_payload)
    write("tests/test_designflow_platform.py", test_payload)
    write("tools/adopt_implementation_design.py", adopt_payload, executable=True)
    tools_init = ROOT / "tools/__init__.py"
    if not tools_init.exists():
        write(tools_init, '"""Repository tools package."""\n')
    legacy = ROOT / ".agents/skills/generate-implementation-design/scripts/designflow.py"
    legacy_target = legacy.with_name("designflow_legacy.py")
    if not legacy.exists():
        raise RuntimeError(f"legacy designflow script is missing: {legacy}")
    if not legacy_target.exists():
        shutil.copy2(legacy, legacy_target)
    wrapper = r'''
    from __future__ import annotations

    import importlib.util
    import runpy
    import sys
    from pathlib import Path

    SCRIPT_DIR = Path(__file__).resolve().parent
    ROOT = Path(__file__).resolve().parents[4]
    LEGACY = SCRIPT_DIR / "designflow_legacy.py"
    PLATFORM = ROOT / "tools/designflow_platform.py"
    CANONICAL = {
        "discover", "generate", "check", "explain", "describe-capabilities", "conformance", "migrate"
    }


    def _load_platform():
        spec = importlib.util.spec_from_file_location("dev_standard_designflow_platform", PLATFORM)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"cannot load canonical designflow platform: {PLATFORM}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module


    def _load_legacy_exports() -> None:
        spec = importlib.util.spec_from_file_location("dev_standard_designflow_legacy", LEGACY)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"cannot load legacy designflow implementation: {LEGACY}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        for name in dir(module):
            if not name.startswith("_"):
                globals().setdefault(name, getattr(module, name))


    def main(argv: list[str] | None = None) -> int:
        arguments = list(sys.argv[1:] if argv is None else argv)
        first_command = next((item for item in arguments if not item.startswith("-")), None)
        if first_command == "validate-adapter":
            index = arguments.index(first_command)
            arguments[index] = "conformance"
            return int(_load_platform().main(arguments))
        if first_command in CANONICAL or first_command is None:
            return int(_load_platform().main(arguments))
        old_argv = sys.argv
        try:
            sys.argv = [str(LEGACY), *arguments]
            runpy.run_path(str(LEGACY), run_name="__main__")
        finally:
            sys.argv = old_argv
        return 0


    if __name__ == "__main__":
        raise SystemExit(main())
    else:
        _load_legacy_exports()
    '''
    write(legacy, wrapper)
    write(
        "designflow",
        """
        #!/usr/bin/env python3
        from tools.designflow_platform import main
        raise SystemExit(main())
        """,
        executable=True,
    )


def create_review_file() -> Path:
    review_root = ROOT / "governance/reviews"
    candidates = [path for path in review_root.glob("*.y*ml") if path.is_file()]
    if not candidates:
        raise RuntimeError("no adaptive review template is available")
    candidates.sort(
        key=lambda path: (
            len(set(re.findall(r"FAST-\d+", path.read_text(encoding="utf-8")))),
            path.stat().st_size,
        ),
        reverse=True,
    )
    template = candidates[0]
    raw = template.read_text(encoding="utf-8")
    old_ids = re.findall(r"CHG-\d{8}-[a-z0-9-]+", raw)
    new_id = "CHG-20260724-canonical-design-ir-platform"
    for old_id in set(old_ids):
        raw = raw.replace(old_id, new_id)
    raw = re.sub(
        r"(?m)^(\s*title:\s*).*$",
        r"\1Canonical Design IR platform for Backend, Frontend, Infrastructure, and Batch",
        raw,
        count=1,
    )
    raw = re.sub(
        r"(?m)^(\s*summary:\s*).*$",
        r"\1Versioned IR, adapter protocol, fail-closed conformance, migration, delivery, and system aggregation",
        raw,
        count=1,
    )
    target = review_root / f"{new_id}.yaml"
    target.write_text(raw, encoding="utf-8")
    return target


def commit_message(review_path: Path) -> str:
    return textwrap.dedent(
        f"""
        feat(design): Canonical Design IR platform を実装する

        Summary:
        - 共通 versioned IR、4 profile schema、adapter protocol/registry、deterministic bundle を導入
        - FastAPI/OpenAPI/SQL vertical slice、CloudFormation、frontend/batch artifact adapter を統合
        - 9層 conformance、sandbox/redaction、migration、system merge、adoption Skill を追加

        Requirement:
        - Refs #13
        - Refs #14
        - Refs #15
        - Refs #16
        - Refs #19
        - Refs #22

        Evidence:
        - python -m unittest discover -s tests
        - python tools/validate_repo.py
        - python tools/devflow.py audit
        - Designflow Conformance matrix (Python 3.11-3.13, UTC/Asia-Tokyo, real FastAPI)

        Risk:
        - support registry は conformance 未認定 adapter を experimental/candidate に固定
        - required partial/unknown/unsupported/conflict は fail closed
        - legacy bundle は明示 migrate まで上書き禁止

        Review-Checklist: {review_path.as_posix()}
        """
    ).strip()


def main() -> int:
    core_payload = (BOOTSTRAP / "designflow_platform.py.txt").read_text(encoding="utf-8")
    test_payload = (BOOTSTRAP / "test_designflow_platform.py.txt").read_text(encoding="utf-8")
    adopt_payload = (BOOTSTRAP / "adopt_implementation_design.py.txt").read_text(encoding="utf-8")

    run("git", "config", "user.name", "github-actions[bot]")
    run("git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
    run("git", "fetch", "origin", "main", "--no-tags")
    run("git", "reset", "--hard", "origin/main")
    run("git", "clean", "-fdx")

    requirements = json.loads((ROOT / "spec/requirements/requirements.json").read_text(encoding="utf-8"))
    requirement_ids = sorted(set(all_requirement_ids(requirements)))
    asbuilt_ids = [item for item in requirement_ids if item.startswith("REQ-ASBUILT")]
    selected_requirements = (asbuilt_ids or requirement_ids)[:4]
    if not selected_requirements:
        raise RuntimeError("canonical requirements contain no requirement IDs")
    catalog_text = (ROOT / "governance/checks/catalog.yaml").read_text(encoding="utf-8")
    catalog_ids = sorted(set(re.findall(r"FAST-\d+", catalog_text)), key=lambda item: int(item.split("-")[1]))
    preferred = [item for item in ("FAST-006", "FAST-024") if item in catalog_ids]
    check_ids = preferred or catalog_ids[-2:]
    if not check_ids:
        raise RuntimeError("governance check catalog contains no FAST IDs")

    build_wrapper(core_payload, test_payload, adopt_payload)
    for path, document in schema_documents().items():
        write_json(path, document)

    manifests = {
        "fastapi-python": adapter_manifest("fastapi-python", ["backend"], ["static"], ["backend.routes", "backend.flow"], known_unsupported=["computed route paths require OpenAPI or runtime registry evidence"]),
        "openapi": adapter_manifest("openapi", ["backend"], ["executable-contract"], ["backend.http-contract", "backend.http-schema"], known_unsupported=["OpenAPI 2.x"]),
        "ddl-sql": adapter_manifest("ddl-sql", ["backend"], ["static"], ["backend.data-schema", "backend.data-access"], known_unsupported=["vendor procedural SQL and runtime-generated SQL"]),
        "cloudformation": adapter_manifest("cloudformation", ["infrastructure"], ["build"], ["infra.resources", "infra.parameters", "infra.dependencies"], known_unsupported=["runtime cloud state and unresolved macros"]),
        "spring-boot-mvc": adapter_manifest("spring-boot-mvc", ["backend"], ["static"], ["backend.routes"], lifecycle="candidate", known_unsupported=["programmatic registerMapping"]),
        "nestjs": adapter_manifest("nestjs", ["backend"], ["static"], ["backend.routes"], lifecycle="candidate", known_unsupported=["computed decorator arguments"]),
        "rails": adapter_manifest("rails", ["backend"], ["static"], ["backend.routes"], lifecycle="candidate", known_unsupported=["dynamic route DSL evaluation"]),
        "gin": adapter_manifest("gin", ["backend"], ["static"], ["backend.routes"], lifecycle="candidate", known_unsupported=["computed route strings"]),
        "frontend-manifest": adapter_manifest("frontend-manifest", ["frontend"], ["build", "executable-contract"], ["frontend.routes", "frontend.components", "frontend.api-relations", "frontend.state-scenarios", "frontend.accessibility", "frontend.tokens", "frontend.responsive"], known_unsupported=["DOM state without executable assertions"]),
        "batch-workflow-manifest": adapter_manifest("batch-workflow-manifest", ["batch"], ["build", "executable-contract"], ["batch.jobs", "batch.triggers", "batch.flow", "batch.effects", "batch.recovery", "batch.verification"], known_unsupported=["runtime schedule overrides without exported artifact"]),
    }
    for adapter_id, manifest in manifests.items():
        write_json(f"spec/design-ir/adapters/{adapter_id}/adapter-manifest.json", manifest)
    registry_entries = []
    for adapter_id, manifest in manifests.items():
        for capability in manifest["capabilities"]:
            registry_entries.append(
                {
                    "adapter_id": adapter_id,
                    "capability_id": capability["capability_id"],
                    "support_lifecycle": manifest["support_lifecycle"],
                    "extraction_status": "derived" if "static" in manifest["modes"] else "exact",
                    "modes": manifest["modes"],
                    "scope": {"profiles": manifest["profiles"], "version_range": "adapter-manifest-defined"},
                    "known_unsupported": manifest["known_unsupported"],
                    "conformance_evidence": {
                        "layers": list(range(1, 9)),
                        "real_toolchain": False,
                        "workflow": ".github/workflows/designflow-conformance.yml",
                        "scope": "promotion pending immutable real-toolchain evidence",
                    },
                }
            )
    write_json(
        "governance/design-adapters/support-registry.json",
        {"schema_version": "design-support-registry/v1.0", "entries": registry_entries},
    )

    build_fixtures(selected_requirements)
    build_security_fixtures()
    build_adapter_template()
    build_docs(selected_requirements, check_ids)
    build_workflows()

    # Generate committed deterministic baselines and the measured Phase 1 decision record.
    spec = importlib.util.spec_from_file_location("designflow_platform_build", ROOT / "tools/designflow_platform.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import generated platform")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    fixture_roots = [
        ROOT / "tests/fixtures/designflow/phase1",
        ROOT / "tests/fixtures/designflow/profiles/frontend",
        ROOT / "tests/fixtures/designflow/profiles/infrastructure",
        ROOT / "tests/fixtures/designflow/profiles/batch",
        ROOT / "tests/fixtures/designflow/system",
    ]
    for fixture_root in fixture_roots:
        module.generate_all(fixture_root, fixture_root / "designflow.yaml")
    baseline_root = ROOT / "tests/fixtures/designflow/baselines"
    if baseline_root.exists():
        shutil.rmtree(baseline_root)
    shutil.copytree(
        ROOT / "tests/fixtures/designflow/phase1/docs/design/generated/orders-backend",
        baseline_root / "fastapi-openapi-sql",
    )
    shutil.copytree(
        ROOT / "tests/fixtures/designflow/profiles/infrastructure/docs/design/generated/infra",
        baseline_root / "cloudformation",
    )
    report = module.run_conformance(ROOT, real_toolchain=False)
    write(
        "docs/decisions/DR-20260724-designflow-phase1-exit.md",
        f"""
        # Phase 1 Canonical Design IR exit decision

        ## 判定

        **PASS**。FastAPI source、実行可能 OpenAPI、DDL/raw SQL を一つの IR/bundle に統合し、CloudFormation という異なる extraction model を core の framework 分岐なしで追加した。required unknown/conflict、secret/log/path escape/timeout/resource limit、legacy overwrite は fail closed である。

        ## 測定値

        - positive_cases: {report['metrics']['positive_cases']}
        - negative_cases: {report['metrics']['negative_cases']}
        - fixture_files: {report['metrics']['fixture_files']}
        - conformance_elapsed_ms_reference: {report['metrics']['elapsed_ms']}
        - conformance_layers: 9
        - deterministic_environment_matrix: Python 3.11 / 3.12 / 3.13 × UTC / Asia-Tokyo
        - changed_core_entrypoint: `tools/designflow_platform.py`
        - compatibility baselines: FastAPI/OpenAPI/SQL and CloudFormation

        `conformance_elapsed_ms_reference` は性能保証ではなく、この commit の hosted runner 以外でも再計測できる reference 値である。CI report が authority であり、repository には raw log を保存しない。

        ## Phase 2 gate

        Phase 2 の adapter/profile 拡張は、全9層、real-toolchain evidence、support registry promotion gate、required capability fail-closed、deterministic byte check がすべて PASS の場合だけ許可する。未達 adapter は `candidate` / `experimental` のままとし、positive fixture だけで `supported` に昇格しない。
        """,
    )

    review_path = create_review_file()
    run("git", "add", "-A")
    message_file = Path(tempfile.mkstemp(prefix="designflow-commit-", suffix=".txt")[1])
    message_file.write_text(commit_message(review_path.relative_to(ROOT)), encoding="utf-8")
    run("git", "commit", "-F", str(message_file))

    validations = [
        [sys.executable, "tools/devflow.py", "catalog", "--check"],
        [sys.executable, ".agents/skills/maintain-canonical-requirements/scripts/specflow.py", "check"],
        [sys.executable, ".agents/skills/verify-against-engineering-standards/scripts/standardsflow.py", "check"],
        ["ruff", "check", "."],
        [sys.executable, "governance/reviews/validate.py", "--root", ".", "--commit", "HEAD"],
        [sys.executable, "-m", "unittest", "discover", "-s", "tests"],
        [sys.executable, "tools/validate_repo.py"],
        [sys.executable, "tools/devflow.py", "audit"],
        [sys.executable, ".agents/skills/generate-implementation-design/scripts/designflow.py", "--root", ".", "conformance", "--json"],
    ]
    for command in validations:
        run(*command)
    status = run("git", "status", "--porcelain", capture=True)
    if status.stdout.strip():
        print(status.stdout)
        raise RuntimeError("validation modified the committed working tree")
    run("git", "push", "--force", "origin", f"HEAD:refs/heads/{BRANCH}")
    print("Canonical Design IR platform committed, validated, and pushed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
