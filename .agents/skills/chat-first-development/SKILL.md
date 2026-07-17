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
   - with `tools/devflow.py`, prepare a repository-local environment and use the full governed flow;
   - without it, create a lightweight `work/<id>/` record containing request, requirements, plan, design, test evidence, release result, and retrospective.
4. Summarize the intended outcome, acceptance criteria, scope, external effects, defaults, stop conditions, and completion definition in one compact natural-language authorization package. Ask for one explicit approve/reject decision.
5. After approval, choose implementation details and continue through design, implementation, review, tests, PR creation, CI verification, and closure. Use `$adversarial-validation` for high-risk surfaces or when a mitigation needs an independent challenge. Repair in-scope failures without routine questions or approvals.
6. Report only useful progress, results, or a genuine blocker. Never expose lifecycle commands as work for the user.

## Interaction contract

- Never ask the user to run Python, shell, installer, test, Git, or governance commands.
- Never require the user to name a skill, work item, profile, phase, model, or checklist.
- Ask at most the smallest conversational question needed to avoid a materially wrong result. Group closely related choices.
- Do not turn ordinary implementation choices into questions. State reasonable reversible assumptions in the authorization package.
- Keep the initial authorization as the only human execution gate. Do not infer it or authorize on the user's behalf.
- After authorization, continue until the requested result and relevant PR/CI evidence exist, unless new authority or unavailable capability is genuinely required.

## Safety boundaries

- Keep setup repository-local. Do not write to global or home configuration, install a personal skill, overwrite active target instructions/configuration, merge a PR, deploy production, or expose secrets unless the authorization explicitly includes it.
- Preserve target-specific `AGENTS.md` and `.codex/config.toml`. Add only a clearly delimited compatible section when needed, and include it in the reviewed change.
- Prefer the full deterministic harness when present. Never weaken a gate to make progress; fall back to the lightweight record only when the runtime was not copied.
