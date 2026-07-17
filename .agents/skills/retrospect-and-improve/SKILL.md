---
name: retrospect-and-improve
description: Generate and review session retrospectives, detect repeated gate failures, and propose testable durable improvements without auto-applying them. Use at session end, after rework or escaped defects, and when recurring agent mistakes should become a separately planned and initially authorized work item.
---

# Retrospect and Improve

Turn observed friction into evidence-backed candidates for a future governed work item.

## Workflow

1. Let the Stop hook create the session report, or run `scripts/retrospect.py --session-id <ID>`.
2. Read the newest report, affected work item events, inspection reports, user corrections, and test outcomes.
3. Separate one-off noise from recurring process failures. Read `references/improvement-policy.md`.
4. Use the automatically generated proposal when the same blocker recurs across sessions. Add a manual proposal only with concrete evidence.
5. Ask `improvement-coach` to challenge the root cause when subagents are available and permitted.
6. Do not auto-apply the proposal. If it is outside the current authorized execution plan, leave it pending.
7. When selected, create a new governed work item that names the exact skill, change, evidence, evaluation, and rollback in its requirements and execution plan.
8. Obtain that work item's one initial requester authorization, implement it autonomously, validate the skill and repository, and confirm in a later task that the failure no longer recurs.

## Update boundary

No retrospective proposal is automatically applied. Any durable change to `references/learned-rules.md`, core `SKILL.md`, `AGENTS.md`, hooks, agents, policy, or gate code requires inclusion in an initially authorized execution plan.

Never ingest secrets or raw transcripts into proposals or learned rules. Store concise behavior and evidence identifiers.
