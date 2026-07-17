---
name: author-lifecycle-docs
description: Create and maintain the mandatory request, requirements, autonomous execution plan, architecture, design, test, implementation, operations, release, traceability, and retrospective documents for a governed work item. Use whenever a phase document is missing, incomplete, stale, or affected by implementation evidence.
---

# Author Lifecycle Documents

Create decision-ready artifacts for the current phase without hiding uncertainty.

## Workflow

1. Read the work item's `state.json`, current phase definition in `governance/policy.json`, and `references/document-rules.md`.
2. Read the user's original words in `docs/00-request.md` before editing derived documents.
3. Open the relevant templates under `docs/templates/` and the phase's catalog items. Use the item acceptance criteria to shape measurable content.
4. Before initial authorization, use `$calibrated-collaborative-listening` and ask the smallest blocking clarification when a decision materially changes scope, authority, risk, privacy, cost, external effects, or acceptance. Otherwise document the default and proceed.
5. Complete `docs/01-execution-plan.md` before authorization. Include every planned change area, tool, external write, publication action, test, rollback, default decision, stopping condition, and completion proof needed to finish without later approvals.
6. Replace every `TBD`, `TODO`, `未記入`, `未確定`, and template token. Do not delete a required section to silence validation.
7. Complete the planned mappings in `docs/01-traceability.md` before authorization, then freeze it with the requirements and plan. Record actual implementation and evidence mappings in the phase logs without changing the authorization digest.
8. Link decisions, risks, evidence, Issue IDs, and owners. Use measurable thresholds for nonfunctional requirements.
9. Run `python tools/devflow.py inspect --work-item <ID> --phase requirements --ignore-approvals` before requesting the single authorization. Afterward, update derived phase documents without requesting more approvals.

## Document integrity

- Preserve the user request verbatim; put interpretation in separate sections.
- Distinguish fact, user decision, assumption, proposal, and unresolved question.
- Freeze requirements, initial traceability, and execution plan after authorization. Put actual implementation choices and evidence mappings in phase logs without expanding authority.
- Keep superseded decisions traceable in the decision log; do not silently rewrite history.
- Never edit `approvals.jsonl` or `events.jsonl` directly.
- Do not include credentials, personal data, production dumps, or unredacted exploit details in public artifacts.

Read `references/learned-rules.md` when present.
