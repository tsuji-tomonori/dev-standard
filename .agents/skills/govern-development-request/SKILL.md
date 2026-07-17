---
name: govern-development-request
description: Govern a development request by defining requirements and a complete autonomous execution plan, obtaining one initial requester authorization, then continuing through every quality gate, implementation, verification, publication, and closure without routine approval pauses. Use for any feature, fix, architecture, security, release, checklist, or durable AI-instruction change in this repository.
---

# Govern Development Request

Turn the user's request into one bounded authorization followed by uninterrupted, traceable execution.

## Workflow

1. Read `references/work-item-contract.md` and current state. Select only scope-relevant profiles: `CORE`, a cloud delta when used, and `AI-CONDITIONAL` for model or agent work.
2. Create or resume the work item. Preserve the request verbatim. Use `$calibrated-collaborative-listening` only when one missing fact materially changes outcome, risk, or authority.
3. Define requirements, traceability, and an outcome-first execution plan containing success criteria, external effects, defaults, validation, rollback, authority boundary, and stop rules. Leave reversible implementation choices open.
4. Inspect the requirements gate. Load only relevant checklist rows and use a read-only reviewer only when its independent judgment materially improves the result.
5. Present one compact authorization package, then record the requester's explicit decision with `$authorize-autonomous-execution`.
6. After authorization, choose and execute the efficient path through design, implementation, verification, publication, and closure. Fix in-scope findings without another approval; recheck preceding gates before advancement.
7. Stop only when completion needs unavailable capability or materially new authority. Record the exact blocker and exhausted alternatives.

## Hard boundaries

- Do not implement before authorization, authorize for the requester, weaken selected checks, or mark N/A without a concrete rationale.
- A changed authorized artifact invalidates authorization. Derived artifacts and repairable findings stay inside the autonomous loop.
- Keep raw production evidence outside Git; store only a redacted reference or immutable link.

Read `references/learned-rules.md` when it exists and apply only rules carrying a recorded governance approval.
