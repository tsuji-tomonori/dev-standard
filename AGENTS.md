# Repository instructions

## Outcome

Deliver each requested repository change end to end with one bounded requester authorization and deterministic quality evidence. Choose the implementation path; do not ask for routine design, review, test, CI, or release decisions after authorization.

The user interface is ordinary conversation. For any feature, fix, refactor, design concern, or incomplete development idea, start with `$chat-first-development` even when the user does not name a skill or workflow. Never ask the user to run setup, Python, test, Git, or governance commands.

Durable product requirements live only in `spec/requirements/requirements.json`. Use `$maintain-canonical-requirements` to discover intent, atomize obligations, and record explicit add/update/retire deltas. `work/<id>/` is noncanonical request context, authorization scope, plan, and evidence. `docs/requirements/REQUIREMENTS.md` is generated; never edit it directly.

## Invariants

- Govern substantive changes with `$govern-development-request`. Freeze the request, requirements, traceability, execution plan, authority boundary, success criteria, and stopping conditions before implementation.
- Before work-item initialization, use `$right-size-execution` to record the L1/L2/L3 operating point, risk floor, confidence, soft budgets, minimum decisive verification, and task-specific checklist selection. Treat Estimate/Execute/Expand as one state machine.
- Record one real requester decision with `$authorize-autonomous-execution`; never infer it. A changed authorized artifact requires a new authorization boundary.
- Preserve the original request in `docs/00-request.md`. Use `$calibrated-collaborative-listening` only when consequential ambiguity changes that boundary, and ask only for the smallest blocking fact.
- Include the proposed canonical requirement delta and base revision in the one initial authorization. Apply that delta after authorization and reject stale catalog or item revisions.
- For FastAPI or CDK work, use `$generate-implementation-design`. Generate sequence, OpenAPI interface, SQL CRUD/query, and CloudFormation resource/parameter views from implementation artifacts; never maintain those views as competing prose.
- Use `$verify-against-engineering-standards` to confirm the selected SWEBOK/cloud source versions are current and apply their checklist contract to requirements, generated design, implementation, and tests.
- Use `$inspect-quality-gates` as gate truth. Pass requires direct evidence; N/A requires a scope or risk rationale; Fail remains blocking.
- Use `$adversarial-review` when requirements, design, implementation, or tests need an independent challenge, and after an escaped defect or consequential correction. Assume mistakes may exist, seek counterexamples with an independent oracle, and do not treat absence of findings as proof.
- After authorization, act autonomously within scope until `closed`. Stop only for unavailable capability or authority outside the plan, and record the exact blocker.
- Keep secrets, raw transcripts, personal data, `.workspace/`, and production evidence out of Git.

## Efficient execution

- Optimize for the outcome, not a prescribed procedure. Prefer reversible assumptions and the fewest useful tool loops.
- Expand one axis only after verification failure, new dependency/contract evidence, or measured overrun. Expand scope and dependencies before model capability; stop exploration after decisive success.
- Preserve selector version, input features, selected checklist IDs, and digest. Do not register every unselected row as N/A.
- Keep the root agent focused on decisions and implementation. Delegate only bounded, independent, read-heavy review that materially improves quality or latency; reviewers remain read-only.
- Use the lightest model and reasoning level that passes representative checks. Follow [docs/AI-OPERATING-POLICY.md](docs/AI-OPERATING-POLICY.md).
- Treat the lifecycle checklist as a validation contract, not prompt content. Load only the current phase and relevant item details.

## Automatic bootstrap

- On the first development request, inspect the repository and prepare the workflow automatically. Keep environments and dependencies repository-local.
- If `spec/requirements/requirements.json` or `governance/standards/registry.json` is absent, bootstrap it from the owning skill's asset and include the new files in the authorized change. Generate human-readable views immediately.
- If the full governance runtime is present, use it internally. If it is absent, use the chat-first skill's lightweight work record and continue; do not ask the user to install tooling.
- Preserve existing target instructions and active configuration. Merge only a delimited compatible section as part of the reviewed repository change.
- Translate natural language into requirements, acceptance criteria, traceability, and an execution plan. Ask only for the single initial authorization and any genuinely blocking fact.

## AI-owned commands

These are implementation details for the agent, not instructions for the user.

- Prepare a repository-local environment and dependencies when required.
- Run the full verification, current gate inspection, and audit before publication.
- Discover and run the target repository's own build, test, lint, and type-check commands.

## Definition of done

- Authorization is current; requirements trace to design, code, tests, and evidence.
- The canonical catalog validates; generated requirement/design/standard views are byte-current with their sources.
- Every selected check has a defensible disposition, and all applicable checks pass.
- Relevant tests, skill/catalog/repository validation, audit, release, and retrospective pass; the work item is `closed`.

## Publication

- Use `$japanese-git-commit-gitmoji`; split commits by purpose and inspect staged files.
- Never publish `.workspace/`, credentials, transcripts, personal data, or unredacted production evidence.
- Durable improvements outside the authorized plan remain pending proposals for a future governed work item.
