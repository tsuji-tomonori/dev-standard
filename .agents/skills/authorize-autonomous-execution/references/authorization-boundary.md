# Authorization boundary

The initial authorization covers the exact requirements digest produced from the requirements, traceability, autonomous execution plan, and requirements checklist results.

The execution plan must make the following decision-ready before asking once:

- repository, service, environment, account, data, and people in scope;
- every expected file or component category;
- local commands, network tools, external writes, publication, merge, release, deletion, and cost;
- test, review, evidence, CI, retry, rollback, and completion behavior;
- safe defaults for low-risk reversible choices;
- prohibited actions and conditions that truly require authority outside the work item.

Authorization does not waive quality gates. It replaces repeated human phase decisions with a stable boundary and continuous deterministic verification.

A later discovery belongs to one of three classes:

1. Planned implementation detail: decide and continue.
2. In-scope defect or failed check: fix and continue.
3. Indispensable action outside the boundary: do not execute; record the blocker.

Do not relabel class 3 as an implementation detail. Do not relabel classes 1 or 2 as reasons to interrupt the requester.
