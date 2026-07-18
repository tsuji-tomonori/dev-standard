---
name: inspect-quality-gates
description: Strictly inspect lifecycle documents, checklist applicability, verdicts, evidence, exceptions, reviewers, the single initial authorization, every preceding gate, and record integrity. Use before initial authorization, phase advancement, completion claims, publication, or pull-request review.
---

# Inspect Quality Gates

All inspection and verification commands are agent-owned implementation details. Never transfer them to the user.

Use the deterministic harness as the source of gate truth and explain every blocker.

## Workflow

1. Read `references/gate-rules.md` and any approved `references/learned-rules.md`.
2. Before initial authorization, run `scripts/inspect.py --work-item <ID> --phase requirements --ignore-approvals`. Never use `--ignore-approvals` for advancement, publication, or completion.
3. After authorization, run normal inspection and verify that requirements, execution plan, and requirements checklist still match the authorized digest.
4. When `execution-profile.json` exists, validate its schema and policy revision; enforce the assurance floor; and audit unexplained budget overrun, evidence-free or stagnant single-axis Expand, post-success activity, compute escalation without demonstrated insufficiency, selector manifest, and mandatory-control misses. In shadow mode keep efficiency and selector findings advisory; malformed ledgers and assurance-floor violations remain blocking.
5. Group blockers by documents, applicability, verdict/evidence, reviewer, authorization, execution scope, and preceding phase.
6. Delegate only bounded independent judgment when it materially improves quality; use `gate-auditor` for the final cross-phase check.
7. Resolve the cause without asking for another phase approval. Never edit policy, remove profiles, delete items, or create empty evidence merely to obtain PASS.
8. Re-run inspection after every material change. A requirements or plan digest change invalidates authorization; a derived-document change only requires its quality gate to pass again.
9. Before release, run `make verify`, soft scope audit, and `python tools/devflow.py audit`.

## Evidence rules

- Pass needs a reachable file or URL that directly proves the acceptance criterion.
- N/A needs a scope, architecture, law, or risk rationale specific to the item.
- Fail needs an Issue ID and remains blocking in the single-authorization workflow; fix the cause instead of seeking a later human exception.
- Reviewer identity and timestamp are mandatory for applicable checks.
- Duplicate controls may share evidence and Issue IDs, but each selected row still needs an explicit disposition.

Report consequential uncertainty as a blocker. Absence of a detected failure is not proof of completion.
