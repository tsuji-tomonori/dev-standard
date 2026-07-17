# Governance integration reference

Copy the relevant rules below into the target repository's `AGENTS.md`. Keep any
target-specific build, test, ownership, and safety instructions already present.

- Treat ordinary natural-language feature, fix, refactor, and design requests as
  triggers for `chat-first-development`. Do not require skill names or commands.
- The AI owns repository-local setup, dependency preparation, lifecycle commands,
  tests, Git publication, and CI checks. Never ask the user to run them.
- For a new development request, use `govern-development-request` to create the
  work item, requirements, traceability, and autonomous execution plan before
  implementation.
- Use `maintain-canonical-requirements` for intent discovery and revision-checked
  add/update/retire operations. `spec/requirements/requirements.json` is the only
  durable requirement authority; `work/<id>` is request-local context and evidence.
- Ask the requester for one initial authorization covering the requirements,
  execution plan, authority boundary, and completion criteria.
- After that authorization, continue autonomously inside the approved boundary.
  Stop only for a material scope change, missing authority, destructive action,
  external coordination, unresolved safety risk, or failed completion gate.
- Use `author-lifecycle-docs`, `authorize-autonomous-execution`,
  `inspect-quality-gates`, and `retrospect-and-improve` at their corresponding
  lifecycle stages.
- Generate FastAPI/CDK detailed design from router/OpenAPI/SQL/CloudFormation
  artifacts with `generate-implementation-design`; reject generated drift.
- Verify requirements, design, implementation, and tests with
  `verify-against-engineering-standards`, the selected checklist profiles, and
  the fresh official sources in `governance/standards/registry.json`.
- Treat `governance/policy.json`, `governance/checklist/catalog.json`, the canonical
  requirements catalog, and each work item's authorized delta/plan hashes as authoritative.
- Use the smallest capable model for bounded checks. Escalate model capability
  only when the current model cannot satisfy a documented quality gate.
