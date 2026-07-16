---
name: author-lifecycle-docs
description: Create and maintain the mandatory request, requirements, architecture, design, test, implementation, operations, release, traceability, and retrospective documents for a governed work item. Use whenever a phase document is missing, incomplete, stale, or changed by a user request.
---

# Author Lifecycle Documents

Create decision-ready artifacts for the current phase without hiding uncertainty.

## Workflow

1. Read the work item's `state.json`, current phase definition in `governance/policy.json`, and `references/document-rules.md`.
2. Read the user's original words in `docs/00-request.md` before editing derived documents.
3. Open the relevant templates under `docs/templates/` and the phase's catalog items. Use the item acceptance criteria to shape measurable content.
4. Ask the smallest blocking clarification when a decision materially changes scope, risk, privacy, cost, or acceptance. Otherwise document the assumption and its validation owner.
5. Replace every `TBD`, `TODO`, `未記入`, `未確定`, and template token. Do not delete a required section to silence validation.
6. Update `docs/01-traceability.md` whenever requirements, design, implementation, tests, or evidence change.
7. Link decisions, risks, evidence, Issue IDs, and owners. Use measurable thresholds for nonfunctional requirements.
8. Run `python tools/devflow.py inspect --work-item <ID> --ignore-approvals` before asking for approval.

## Document integrity

- Preserve the user request verbatim; put interpretation in separate sections.
- Distinguish fact, user decision, assumption, proposal, and unresolved question.
- Keep superseded decisions traceable in the decision log; do not silently rewrite history.
- Never edit `approvals.jsonl` or `events.jsonl` directly.
- Do not include credentials, personal data, production dumps, or unredacted exploit details in public artifacts.

Read `references/learned-rules.md` when present.
