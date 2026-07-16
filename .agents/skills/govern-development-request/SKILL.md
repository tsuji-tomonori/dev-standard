---
name: govern-development-request
description: Govern a user development request from intake through lifecycle gates, documentation, review, approval, and closure. Use for any feature, fix, architecture change, security change, release, or AI-driven development task that must follow this repository's SWEBOK v4 and Well-Architected checklist workflow.
---

# Govern Development Request

Turn the user's request into a traceable work item and enforce every lifecycle gate.

## Workflow

1. Read `AGENTS.md`, `governance/policy.json`, and `references/work-item-contract.md`.
2. Run `python tools/devflow.py status --work-item <ID>` when an ID exists. Never infer the active phase from memory.
3. When no work item exists, select profiles from the request:
   - Always include `CORE`.
   - Add the selected cloud vendor delta; the harness adds `CLOUD-COMMON`.
   - Add `AI-CONDITIONAL` for ML, generative AI, RAG, models, or agents.
4. Create the work item with `scripts/start.py` or `tools/devflow.py init`. Preserve the user's words verbatim in `docs/00-request.md`.
5. Use `$author-lifecycle-docs` for the current phase. Record unresolved ambiguity instead of inventing requirements.
6. Use the matching read-only custom agent for an independent review. Resolve its findings and re-run the gate.
7. Use `$inspect-quality-gates` until content and checklist blockers are zero.
8. Present the artifact digest, material decisions, residual risks, and exact approval role to the user. Stop for an explicit decision.
9. Use `$record-governance-approval` only after that decision. Advance only when the current gate passes.
10. Repeat through `retrospective`, then reach `closed`.

## Hard boundaries

- Do not write implementation code before intake and requirements approvals.
- Do not skip phases, reduce selected profiles, or bulk-mark checks to make a gate pass.
- Do not approve on behalf of any human role.
- Treat a changed document or checklist result as requiring fresh approval.
- Keep raw production evidence outside Git; store a redacted reference or immutable external link.

Read `references/learned-rules.md` when it exists and apply only rules carrying a recorded governance approval.
