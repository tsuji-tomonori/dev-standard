# FastAPI implementation-to-design contract

## Operation layout

- `router.py`: path-operation declaration and ordered orchestration only. It may validate/construct narrow typed inputs and call named functions, but must not contain domain algorithms or persistence details.
- `functions.py`: concrete application/domain operations. Prefer three or fewer arguments; introduce a narrowly scoped Pydantic input model beyond that and explain the grouping in its docstring.
- Return the final response-producing call directly. A route ending with `response = ...; return response` is a contract violation.
- Put `/health` under a `system` domain router, not in `main.py`.
- Examples declared in schemas/OpenAPI are executable unit-test expectations, not decorative documentation.

## Generated artifacts

| Source | Generated design |
|---|---|
| `router.py` AST | operation flow and Mermaid sequence diagrams |
| application `openapi.json` | API catalog and request/response interface catalog |
| raw `.sql` parsed with SQLGlot | query-object catalog and table CRUD matrix |
| source bytes | manifest SHA-256 used by `--check` |

Static analysis must reject missing direct returns, unparseable Python/SQL, duplicate OpenAPI operation IDs, and generated drift. A route flow describes call order; it does not infer runtime behavior hidden inside a called function.

Primary references: [FastAPI OpenAPI generation](https://fastapi.tiangolo.com/how-to/extending-openapi/), [OpenAPI Specification](https://spec.openapis.org/oas/latest.html), and [SQLGlot AST documentation](https://sqlglot.com/sqlglot.html).
