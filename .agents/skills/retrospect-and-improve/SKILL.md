---
name: retrospect-and-improve
description: Generate and review session retrospectives, detect repeated gate failures, propose durable workflow improvements, obtain governance approval, and apply approved lessons to repository skills. Use at session end, after rework or escaped defects, and when recurring agent mistakes should update future behavior.
---

# Retrospect and Improve

Turn observed friction into approved, testable skill improvements.

## Workflow

1. Let the Stop hook create the session report, or run `scripts/retrospect.py --session-id <ID>`.
2. Read the newest report, affected work item events, inspection reports, user corrections, and test outcomes.
3. Separate one-off noise from recurring process failures. Read `references/improvement-policy.md`.
4. Use the automatically generated proposal when the same blocker recurs across sessions. Add a manual proposal only with concrete evidence.
5. Ask `improvement-coach` to challenge the root cause and verify that the proposed rule is preventive and testable.
6. Present pending proposals to the governance-owner. Do not approve your own proposal.
7. After explicit approval, run `python tools/devflow.py improvement-approve --id <ID> --approver <identity>`.
8. The next Stop hook applies approved proposals automatically; `improvement-apply` can apply immediately.
9. Validate the changed skill and repository. Confirm in a later task that the failure no longer recurs.

## Update boundary

Automatic application may append only to the target skill's `references/learned-rules.md`. Changing core `SKILL.md`, `AGENTS.md`, hooks, agents, policy, or gate code requires a normal governed work item and review.

Never ingest secrets or raw transcripts into learned rules. Store concise behavior, evidence identifiers, approval identity, and approval time.
