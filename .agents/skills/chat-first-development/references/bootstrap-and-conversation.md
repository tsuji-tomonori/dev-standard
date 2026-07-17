# Bootstrap and conversation contract

## Preflight owned by the AI

Perform these checks silently at the start of a development request:

1. Locate the repository root, read applicable instructions, inspect Git state, and preserve unrelated changes.
2. Detect the full runtime by checking for `tools/devflow.py`, `governance/policy.json`, `docs/templates`, and the checklist catalog.
3. If the full runtime exists, create a repository-local environment only when required, install pinned dependencies locally, validate the catalog, and create or resume the work item. Repair safe setup drift without involving the user.
4. If the runtime is absent, create a lightweight work record. Do not stop to ask the user to copy more files or run an installer.
5. Detect available tests, build commands, GitHub integration, and publication boundary. Record missing external capability as a blocker only when it becomes necessary.

Never present these as setup instructions to the user.

## Lightweight record

Create `work/<id>/` with concise Markdown files for:

- original request;
- requirements, acceptance criteria, and traceability;
- autonomous execution plan and authority boundary;
- design decisions and risks;
- implementation changes;
- test and security evidence;
- PR/release result and retrospective.

The record is evidence, not a substitute for repository tests or review.

## Conversation sequence

1. Reflect the likely core goal in one or two sentences.
2. Ask only about a fact whose alternatives would produce materially different results. Prefer one grouped question; otherwise proceed with stated reversible assumptions.
3. Produce one compact authorization package after the requirements are coherent.
4. Accept an unambiguous natural-language approval such as “進めて”, “承認”, or “その内容で実装して”. Do not require a command phrase.
5. After approval, communicate milestones without transferring commands or routine decisions to the user.

## Completion sequence

Complete relevant design, implementation, tests, static checks, security review, documentation, Git commits, remote branch, PR, and CI. Do not merge unless explicitly authorized. Close the work record only after evidence is current.

