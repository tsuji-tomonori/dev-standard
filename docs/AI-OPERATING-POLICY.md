# AI operating policy

## Goal

Give the agent the outcome, hard constraints, evidence requirements, authority boundary, and stopping conditions. Leave reversible implementation choices to the agent. Human intervention is reserved for the initial authorization and genuinely new authority.

## Prompt contract

State each instruction once. Keep the user-visible outcome, success criteria, hard constraints, evidence requirements, authority boundary, required output, and stop rules. Remove repeated process narration, generic examples, broad absolute rules, and instructions already enforced by code. Prefer decision rules over step-by-step prescriptions.

## Autonomy boundary

- Answer, review, diagnose, or plan: inspect and report; do not silently implement.
- Change, build, or fix: make all in-scope reversible changes and validate without another approval.
- Stop for an external write, destructive or costly action, or scope expansion only when it was not included in the initial execution plan.
- Stop tool loops when the outcome has sufficient evidence. Retry only when a missing required fact has a meaningful fallback.

## Model routing

The root agent is not pinned so Codex can match capability to the task. Custom read-only reviewers use `gpt-5.6-terra`, the documented lower-cost Codex option.

| Work shape | Model | Reasoning | Escalate when |
|---|---|---|---|
| Inventory, document scan, routine operations review | `gpt-5.6-terra` | `low` | evidence conflicts or consequential ambiguity appears |
| Requirements, architecture, test, process review | `gpt-5.6-terra` | `medium` | representative checks expose a quality gap |
| Security and cross-phase audit | `gpt-5.6-terra` | `high` | measured quality remains insufficient; then use unpinned root judgment |

Do not select `max`, `xhigh`, pro mode, or extra agents by default. Increase capability or reasoning one level at a time only when a named check fails. For API workloads outside Codex, `gpt-5.6-luna` is the efficient high-volume family member; it is not pinned here because the current Codex manual documents `gpt-5.6-terra` for lighter subagents.

## Checklist use

The 1,740-item catalog remains the deterministic validation contract and control source; do not copy it into the system prompt.

1. Select profiles from actual scope.
2. Load only the current phase's selected items.
3. Record applicability, verdict, severity, reviewer, timestamp, and direct evidence.
4. Require a concrete rationale for N/A and an issue for Fail.
5. Recheck preceding gates and run the full audit before release.

## Minimal-prompt regression checklist

- [ ] Outcome, success criteria, authority boundary, evidence, and stop rules remain explicit.
- [ ] No active instruction is repeated without a distinct purpose.
- [ ] Examples remain only for a product requirement or measured failure.
- [ ] Only relevant tools and checklist details enter context.
- [ ] Root reasoning and creative implementation choices are not prescribed.
- [ ] Reviewer model and effort are the least expensive settings that pass tests.
- [ ] Validation covers behavior, prompt contracts, model routing, repository rules, and audit integrity.

## Sources

- [Using GPT-5.6](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.6)
- [Prompting guidance for GPT-5.6](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6)
- [Codex subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
