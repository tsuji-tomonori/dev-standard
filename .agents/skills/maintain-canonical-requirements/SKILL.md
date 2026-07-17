---
name: maintain-canonical-requirements
description: Discover, articulate, atomize, and persist product requirements through natural conversation. Use when requirements are being created, clarified, added, changed, retired, or reconciled; when ideas must diverge and converge; or when work-item notes need promotion into the durable specification. Maintain `spec/requirements/requirements.json` as the authoritative source and generate human-readable docs from it. Treat `work/` as transient conversation and execution evidence, never as the durable requirements authority.
---

# Maintain Canonical Requirements

Turn conversation into a durable, reviewable specification without making the user operate tooling.

## Boundaries

- `work/<id>` records the request fragment, decisions, delta, plan, and execution evidence.
- `spec/requirements/requirements.json` is the only durable requirements authority.
- `docs/requirements/REQUIREMENTS.md` is generated for people and must not be edited directly.
- Preserve IDs and history. “Delete” means `retire` with a reason; do not erase a previously authoritative requirement.

If the canonical file does not exist, copy `assets/requirements.template.json` to the canonical path, replace the product name/date, and include this bootstrap in the initial authorization. The agent performs this setup; never ask the user to run the script.

## Conversation workflow

1. Use `$calibrated-collaborative-listening` to formulate the likely need, constraint, tension, and decision point without over-agreeing.
2. Discover before defining: explore users, problems, outcomes, exceptions, and alternatives. Read `references/research-basis.md` when choosing elicitation or divergence/convergence techniques.
3. Converge when additional ideas stop changing the problem boundary. Summarize the smallest coherent scope, excluded scope, assumptions, and unresolved decisions.
4. Split each durable requirement into one observable obligation. Give it one subject, one action, one object, one lifecycle status, and independently testable acceptance criteria. Move conjunctions that introduce separate obligations into separate requirement IDs.
5. Compare the proposed requirements with the current canonical catalog. Produce explicit `add`, `update`, and `retire` operations; never replace the catalog from scratch.
6. Put the proposed delta and its effects in the current work item. Include changed IDs, reason, compatibility impact, trace impact, and validation plan.
7. Include the delta in the single initial requester authorization boundary. After authorization, apply it with `scripts/specflow.py apply`; do not ask for another routine approval.
8. Run `validate`, regenerate docs, then run `check`. Repair failures autonomously within the authorized delta.

## Atomicity rules

- One requirement ID expresses one normative action. The machine schema rejects multi-action fields, multiline obligations, missing acceptance criteria, duplicate IDs, stale revisions, and partial updates.
- An update names the expected item revision. A change set names the expected catalog revision. Any mismatch fails before writing.
- Validate the complete candidate in memory before replacing the canonical file. Generated docs are reproducible derivatives and CI rejects drift.
- Never silently infer a consequential product choice. Record it as unresolved or ask one low-pressure question when different answers change the requirement.

## Completion

Report the changed requirement IDs and their generated document sections. A work item can close only when the canonical catalog validates, generated docs are current, traces are updated, and no unauthorized requirement was added.
