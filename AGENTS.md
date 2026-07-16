# Repository instructions

## Mandatory governed flow

- Treat every feature, fix, architecture change, security change, release, checklist change, and durable AI instruction change as a governed work item.
- Start with `$govern-development-request`. Do not implement before the intake and requirements gates have current approvals.
- Create and maintain phase documents with `$author-lifecycle-docs`; preserve the user's original request verbatim in `docs/00-request.md`.
- Inspect every gate with `$inspect-quality-gates`. Do not weaken a gate, mark items N/A without rationale, or claim Pass without reachable evidence.
- Record decisions with `$record-governance-approval`. An AI agent must never impersonate a requester, product owner, architect, security owner, QA owner, operations owner, release owner, or governance owner.
- At session end use `$retrospect-and-improve`; the Stop hook generates the baseline retrospective automatically.

## Review delegation

- Delegate independent reviews to the matching project custom agent after the relevant documents exist: `requirements-reviewer`, `architecture-reviewer`, `security-reviewer`, `test-reviewer`, `operations-reviewer`, and `gate-auditor`.
- Keep reviewers read-only. The implementing agent resolves findings; the reviewer rechecks evidence.
- Use the `improvement-coach` only for retrospective proposals. It cannot approve or apply its own proposal.

## Commands

- Setup: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`
- Export catalog: `.venv/bin/python tools/devflow.py catalog`
- Check catalog: `.venv/bin/python tools/devflow.py catalog --check`
- Test: `.venv/bin/python -m unittest discover -s tests -v`
- Full verification: `make verify`
- Inspect work item: `.venv/bin/python tools/devflow.py inspect --work-item <ID>`
- Audit records: `.venv/bin/python tools/devflow.py audit`

## Definition of done

- The active phase and every preceding phase have passing inspections bound to the approved artifact digests.
- Every applicable checklist item has a verdict, reviewer, timestamp, and reachable evidence.
- Every N/A has a concrete scope/risk rationale. Every accepted Fail has an Issue ID, unexpired exception, rationale, and authorized approver.
- Requirements are traceable to design, code, tests, and evidence.
- Relevant tests, catalog validation, skill validation, repository validation, and audit pass.
- The release and retrospective gates are approved and the work item reaches `closed`.

## Commits and publication

- Use `$japanese-git-commit-gitmoji` for every commit message.
- Split commits by purpose; do not join unrelated work with `と`, `および`, or `/` in the subject.
- Inspect staged files and any included work/retrospective report before committing.
- Never publish `.workspace/`, credentials, transcripts, personal data, or unredacted production evidence.

## Durable improvement

- Record repeated friction as a proposal under `governance/improvements/proposals.json`.
- Only a named governance-owner may approve a proposal.
- Approved proposals may update only the target skill's `references/learned-rules.md`; core SKILL.md or this file requires a normal governed work item and review.
