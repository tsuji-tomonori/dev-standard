---
name: generate-implementation-design
description: Generate deterministic detailed-design documentation that stays one-to-one with FastAPI or AWS CDK implementation artifacts. Use for FastAPI router/functions structure, router-derived sequence diagrams, OpenAPI API and interface catalogs, raw-SQL CRUD and query-object documentation, CDK synthesis, or CloudFormation resource and parameter catalogs. Run the bundled generator and reject source/design drift instead of manually rewriting derived docs.
---

# Generate Implementation Design

Generate detailed design from implementation contracts while keeping canonical requirements above both.

## Authority order

1. `spec/requirements/requirements.json` defines intended behavior.
2. Implementation artifacts define implemented structure and interfaces.
3. Generated detailed design describes those artifacts and includes their digests.
4. A mismatch is a defect; never edit generated docs to hide it.
5. Markdown outputs use `.gen.md` under `docs/design/generated/` and begin with a direct-edit prohibition plus generate/check command templates.

## FastAPI contract

- Organize each operation so `router.py` shows orchestration and `functions.py` contains concrete processing.
- Keep route bodies as a readable sequence of calls. Return the final call directly; do not assign a response only to return the variable.
- Generate sequence diagrams from route AST call order.
- Generate API/IF catalogs from the application-produced OpenAPI document, not duplicated annotations or prose.
- Keep executable SQL in `.sql` files. Parse it with SQLGlot AST; generate query objects and a CRUD matrix from parsed statements. Reject unparseable SQL rather than guessing with regular expressions.
- Read `references/fastapi-contract.md` before creating or restructuring a FastAPI project.
- Prepare the repository-local dependencies from this skill's `requirements.txt` when YAML or SQL parsing support is absent. Do not ask the user to install them.

Run:

`scripts/designflow.py fastapi --source-root <src> --openapi <openapi.json> --sql-root <sql> --out docs/design/generated/fastapi`

Use `--check` in CI after generation.

## AWS CDK contract

- Synthesize CDK before documentation. The deployment-level input is each generated CloudFormation YAML/JSON template.
- Generate resource inventory and parameter details from `Resources` and `Parameters`.
- Record template path and SHA-256. A different synthesized template requires regenerated design.
- Read `references/cdk-contract.md` before creating or restructuring a CDK project.

Run:

`scripts/designflow.py cdk --template <template.yaml> --out docs/design/generated/cdk/<stack>`

## Gate

Generated design is complete only when generation succeeds, a second run is byte-identical, `--check` passes, requirement IDs trace to operations/resources/tests, and `$verify-against-engineering-standards` passes. Implementation-derived documentation does not prove that the implementation satisfies the requirement.
