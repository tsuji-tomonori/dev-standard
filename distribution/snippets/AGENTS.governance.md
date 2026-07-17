# Governance integration reference

Copy the relevant rules below into the target repository's `AGENTS.md`. Keep any
target-specific build, test, ownership, and safety instructions already present.

- For a new development request, use `govern-development-request` to create the
  work item, requirements, traceability, and autonomous execution plan before
  implementation.
- Ask the requester for one initial authorization covering the requirements,
  execution plan, authority boundary, and completion criteria.
- After that authorization, continue autonomously inside the approved boundary.
  Stop only for a material scope change, missing authority, destructive action,
  external coordination, unresolved safety risk, or failed completion gate.
- Use `author-lifecycle-docs`, `authorize-autonomous-execution`,
  `inspect-quality-gates`, and `retrospect-and-improve` at their corresponding
  lifecycle stages.
- Treat `governance/controls.yaml`, `governance/checklist-catalog.json`, and each
  work item's authorized requirement and execution-plan hashes as authoritative.
- Use the smallest capable model for bounded checks. Escalate model capability
  only when the current model cannot satisfy a documented quality gate.

