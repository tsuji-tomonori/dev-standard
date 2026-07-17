# Repository instructions

## Outcome

Deliver each requested repository change end to end with one bounded requester authorization and deterministic quality evidence. Choose the implementation path; do not ask for routine design, review, test, CI, or release decisions after authorization.

## Invariants

- Govern substantive changes with `$govern-development-request`. Freeze the request, requirements, traceability, execution plan, authority boundary, success criteria, and stopping conditions before implementation.
- Record one real requester decision with `$authorize-autonomous-execution`; never infer it. A changed authorized artifact requires a new authorization boundary.
- Preserve the original request in `docs/00-request.md`. Use `$calibrated-collaborative-listening` only when consequential ambiguity changes that boundary, and ask only for the smallest blocking fact.
- Use `$inspect-quality-gates` as gate truth. Pass requires direct evidence; N/A requires a scope or risk rationale; Fail remains blocking.
- After authorization, act autonomously within scope until `closed`. Stop only for unavailable capability or authority outside the plan, and record the exact blocker.
- Keep secrets, raw transcripts, personal data, `.workspace/`, and production evidence out of Git.

## Efficient execution

- Optimize for the outcome, not a prescribed procedure. Prefer reversible assumptions and the fewest useful tool loops.
- Keep the root agent focused on decisions and implementation. Delegate only bounded, independent, read-heavy review that materially improves quality or latency; reviewers remain read-only.
- Use the lightest model and reasoning level that passes representative checks. Follow [docs/AI-OPERATING-POLICY.md](docs/AI-OPERATING-POLICY.md).
- Treat the lifecycle checklist as a validation contract, not prompt content. Load only the current phase and relevant item details.

## Commands

- Setup: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`
- Full verification: `make verify`
- Inspect: `.venv/bin/python tools/devflow.py inspect --work-item <ID>`
- Audit: `.venv/bin/python tools/devflow.py audit`

## Definition of done

- Authorization is current; requirements trace to design, code, tests, and evidence.
- Every selected check has a defensible disposition, and all applicable checks pass.
- Relevant tests, skill/catalog/repository validation, audit, release, and retrospective pass; the work item is `closed`.

## Publication

- Use `$japanese-git-commit-gitmoji`; split commits by purpose and inspect staged files.
- Never publish `.workspace/`, credentials, transcripts, personal data, or unredacted production evidence.
- Durable improvements outside the authorized plan remain pending proposals for a future governed work item.
