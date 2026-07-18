---
name: chat-first-development
description: Start and complete repository development from an ordinary natural-language conversation. Use whenever a user casually describes a feature, fix, refactor, design concern, failing behavior, or incomplete idea and wants the repository changed, even when they do not mention skills, requirements, planning, tests, GitHub, or a workflow. Automatically prepare the local workflow, articulate requirements, obtain one compact initial authorization, then design, implement, test, publish a PR, verify CI, and close the work without asking the user to run commands.
---

# Chat-first Development

Make the chat the only user interface. Own setup and lifecycle mechanics internally.

## Workflow

1. Read `references/bootstrap-and-conversation.md`. Inspect the repository and determine whether the full governance runtime is present.
2. Treat the user's ordinary development request as intake. Preserve their words, infer reversible details, and use `$calibrated-collaborative-listening` only for ambiguity that materially changes outcome, risk, or authority.
3. Bootstrap automatically:
   - ensure `$maintain-canonical-requirements` has a canonical `spec/requirements/requirements.json` and generated human view;
   - ensure `$verify-against-engineering-standards` has a versioned source registry and generated source view;
   - with `tools/devflow.py`, prepare a repository-local environment and use the full governed flow;
   - without it, create a lightweight `work/<id>/` record containing only request-local fragments, the proposed canonical delta, plan, design, test evidence, release result, and retrospective.
4. Before governance initialization, use `$right-size-execution` to estimate scope, assurance, compute, and mode independently from deterministic features and at most one reusable metadata probe. Do not add an Estimate-only LLM call. Persist the execution profile for repository changes and let it select and omission-audit task-specific checklist rows.
5. Detect frontend experience scope when the request concerns a screen, flow, navigation, content hierarchy, interaction, component, design system, responsive behavior, accessibility, frontend visual quality, or phrases such as “使いやすくしたい” or “デザインを良くしたい”. For that scope, route the lifecycle through:
   - `$elicit-frontend-requirements` during requirements, reusing `$calibrated-collaborative-listening` and `$maintain-canonical-requirements`;
   - `$design-frontend-experience` during detailed design and test design;
   - `$implement-frontend-experience` during implementation;
   - `$test-frontend-experience` during verification.
   Do not force these skills onto backend-only work, and do not skip requirements merely because a screenshot or Figma frame was supplied.
6. Summarize the intended outcome, atomic requirement add/update/retire delta, acceptance criteria, scope, external effects, defaults, stop conditions, and completion definition in one compact natural-language authorization package. Ask for one explicit approve/reject decision.
7. After approval, apply the canonical delta and follow `$right-size-execution` Execute/Expand. Expand one axis only on verification failure, new evidence, or measured overrun; stop after decisive success. Continue through design, implementation, review, tests, PR creation, CI verification, and closure. For FastAPI/CDK, use `$generate-implementation-design`; for frontend experience work, use the four phase-specific frontend skills above; use `$adversarial-review` when correctness needs an independent, defect-seeking challenge. Repair in-scope failures without routine questions or approvals.
8. Finalize the efficiency report, then report only useful progress, results, or a genuine blocker. Never expose lifecycle commands as work for the user.

## Interaction contract

- Never ask the user to run Python, shell, installer, test, Git, or governance commands.
- Never require the user to name a skill, work item, profile, phase, model, or checklist.
- Ask at most the smallest conversational question needed to avoid a materially wrong result. Group closely related choices.
- Do not turn ordinary implementation choices into questions. State reasonable reversible assumptions in the authorization package.
- For frontend work, ask about users, tasks, context, consequences, and priorities rather than asking a design novice to choose tokens, component APIs, typography scales, or accessibility techniques.
- Keep the initial authorization as the only human execution gate. Do not infer it or authorize on the user's behalf.
- After authorization, continue until the requested result and relevant PR/CI evidence exist, unless new authority or unavailable capability is genuinely required.

## Safety boundaries

- Keep setup repository-local. Do not write to global or home configuration, install a personal skill, overwrite active target instructions/configuration, merge a PR, deploy production, or expose secrets unless the authorization explicitly includes it.
- Preserve target-specific `AGENTS.md` and `.codex/config.toml`. Add only a clearly delimited compatible section when needed, and include it in the reviewed change.
- Prefer the full deterministic harness when present. Never weaken a gate to make progress; fall back to the lightweight record only when the runtime was not copied.
- Never treat `work/` as durable requirements authority or directly edit generated requirements and detailed-design documents.
