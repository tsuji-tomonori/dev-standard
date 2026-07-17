---
name: authorize-autonomous-execution
description: Record the single explicit requester decision that authorizes a governed work item’s frozen requirements, traceability, autonomous execution plan, external effects, and completion conditions. Use once after the requirements content gate passes and before any implementation; never use for later lifecycle phases, routine design choices, review fixes, tests, CI, or release.
---

# Authorize Autonomous Execution

Bind one real human decision to the complete boundary within which the agent must finish without further approval pauses.

## Workflow

1. Read `references/authorization-boundary.md` and any approved `references/learned-rules.md`.
2. Confirm the work item uses the current workflow schema. Migrate a legacy item explicitly; never reuse an old approval as the new authorization.
3. Confirm these files are complete:
   - `docs/00-request.md`;
   - `docs/01-requirements.md`;
   - `docs/01-traceability.md`;
   - `docs/01-execution-plan.md`.
4. Run `python tools/devflow.py inspect --work-item <ID> --phase requirements --ignore-approvals`. Resolve every content and checklist blocker.
5. Show the requester one decision package containing:
   - requirements and acceptance criteria;
   - all planned tasks and affected systems;
   - allowed and prohibited actions;
   - external writes, publication, merge, deletion, cost, and rollback;
   - defaults for reversible ambiguity;
   - residual risks, stop conditions, and definition of done;
   - the effect that authorization starts uninterrupted execution.
6. Wait for one explicit approve or reject decision. Silence, continued conversation, previous approval, or inferred intent is not authorization.
7. Run `scripts/authorize.py` with the exact approver identity, decision, and comment.
8. Re-run normal inspection and advance. Continue with `$govern-development-request`; do not request phase approvals.

## Hard Boundaries

- Never choose the decision or impersonate the requester.
- Never authorize unresolved requirements content or checklist blockers.
- Never alter `approvals.jsonl` or `events.jsonl` directly.
- Never widen the execution plan after authorization.
- Treat a changed requirement, execution plan, traceability document, or requirements checklist result as stale authorization.
- Do not request another approval for implementation detail, reviewer feedback, test repair, CI repair, documentation alignment, or planned publication.
- If completion requires an action outside the authorized boundary, do not perform it. Exhaust in-scope alternatives and record a blocker.

Read `references/learned-rules.md` when present.
