---
name: inspect-quality-gates
description: Strictly inspect lifecycle documents, checklist applicability, verdicts, evidence, exceptions, reviewers, approvals, and record integrity for a governed work item. Use before requesting approval, advancing a phase, claiming completion, committing a release, or reviewing a pull request.
---

# Inspect Quality Gates

Use the deterministic harness as the source of gate truth and explain every blocker.

## Workflow

1. Read `references/gate-rules.md` and any approved `references/learned-rules.md`.
2. Run `scripts/inspect.py --work-item <ID>` for the current phase. Use `--ignore-approvals` only while preparing content, never for advancing or completion.
3. Group blockers by documents, applicability, verdict/evidence, exception, reviewer, and approval.
4. Delegate a read-only independent review to the custom agent matching the phase. Use `gate-auditor` for the final cross-phase check.
5. Resolve the cause. Never edit policy, remove profiles, delete items, or create empty evidence merely to obtain PASS.
6. Re-run inspection after every material change because the gate digest and approvals may change.
7. Before release, run `make verify` and `python tools/devflow.py audit`.

## Evidence rules

- Pass needs a reachable file or URL that directly proves the acceptance criterion.
- N/A needs a scope, architecture, law, or risk rationale specific to the item.
- Fail needs an Issue ID; accepted Fail also needs a named, authorized, unexpired exception.
- Reviewer identity and timestamp are mandatory for applicable checks.
- Duplicate controls may share evidence and Issue IDs, but each selected row still needs an explicit disposition.

Report uncertainty as a blocker. Absence of a detected failure is not proof of completion.
