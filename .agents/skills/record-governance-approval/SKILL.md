---
name: record-governance-approval
description: Record an explicit human gate approval or rejection in the tamper-evident approval chain, bound to the current document and checklist digest. Use only after the named decision-maker has reviewed a passing gate and clearly stated the decision, role, identity, and comment.
---

# Record Governance Approval

Create an auditable decision without impersonating the decision-maker.

## Workflow

1. Read `references/approval-roles.md` and approved `references/learned-rules.md`.
2. Run `python tools/devflow.py inspect --work-item <ID> --ignore-approvals` and confirm content/checklist blockers are zero.
3. Show the human decision-maker:
   - work item and phase;
   - gate digest;
   - required approval role;
   - material decisions and residual risk;
   - effect of approval or rejection.
4. Wait for an explicit decision. Silence, continued conversation, prior approval, or an agent's judgment is not approval.
5. Run `scripts/approve.py` with the exact identity, role, decision, and comment supplied by the human.
6. Re-run normal inspection. Record every required role separately.
7. If any bound document or checklist result changes, request fresh approval for the new digest.

## Hard boundaries

- Do not choose the approver identity or decision.
- Do not approve unresolved content blockers.
- Do not edit, squash, reorder, or regenerate `approvals.jsonl`.
- Rejection is a valid auditable outcome; preserve it and resolve the stated reason.
- Risk exceptions are checklist-level decisions and do not replace phase approval.
