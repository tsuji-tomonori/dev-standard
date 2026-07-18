---
name: govern-development-request
description: Govern a development request by defining requirements and a complete autonomous execution plan, obtaining one initial requester authorization, then continuing through every quality gate, implementation, verification, publication, and closure without routine approval pauses. Use for any feature, fix, architecture, security, release, checklist, or durable AI-instruction change in this repository.
---

# Govern Development Request

Turn the user's request into one bounded authorization followed by uninterrupted, traceable execution.

This skill is an internal lifecycle component. The user speaks naturally; the agent owns all work-item, setup, checklist, test, and publication commands. Never instruct the user to run them.

## Workflow

1. Read `references/work-item-contract.md` and current state. Invoke `$right-size-execution` before work-item initialization; record independent scope, assurance, compute, and mode evidence, policy revision, soft budgets, required verification, evidence-backed Expand conditions, stopping conditions, and authority boundary in `execution-profile.json`. Do not impose a global Expand count cap.
2. Select only scope-relevant profiles: `CORE`, a cloud delta when used, and `AI-CONDITIONAL` for model or agent work. Use the scope selector instead of registering every profile row as automatic N/A.
3. Create or resume the work item. Preserve the request verbatim. Use `$calibrated-collaborative-listening` only when one missing fact materially changes outcome, risk, or authority.
4. Define requirements, traceability, and an outcome-first execution plan containing success criteria, external effects, defaults, validation, rollback, authority boundary, and stop rules. Generate its execution summary from the structured scope; leave reversible implementation choices open.
5. Inspect the requirements gate. Load only selected checklist rows and use a read-only reviewer only when its independent judgment materially improves the result.
6. Present one compact authorization package, then record the requester's explicit decision with `$authorize-autonomous-execution`.
7. After authorization, Execute within the soft budget. Expand only one axis after a recorded trigger; context and dependency expansion precede capability escalation. Fix in-scope findings without another approval and recheck preceding gates before advancement.
8. Stop after decisive success and mandatory final gates. Finalize execution-efficiency evidence. Stop early only when completion needs unavailable capability or materially new authority; record the exact blocker and exhausted alternatives.

## Hard boundaries

- Do not implement before authorization, authorize for the requester, weaken selected checks, or mark N/A without a concrete rationale.
- A changed authorized artifact invalidates authorization. Derived artifacts and repairable findings stay inside the autonomous loop.
- Keep raw production evidence outside Git; store only a redacted reference or immutable link.

Read `references/learned-rules.md` when it exists and apply only rules carrying a recorded governance approval.
