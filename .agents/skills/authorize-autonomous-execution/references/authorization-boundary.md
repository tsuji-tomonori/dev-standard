# Authorization boundary

When a concrete lifecycle duty exists, authorization covers the requested result, durable requirement meaning, authority boundary, external or irreversible effects, production/cost boundary, rollback, and stop conditions required by that duty. For a standalone authority boundary, it covers only the named external write, production operation, deletion, publication, merge, high-cost action, or other difficult-to-reverse operation.

The execution plan must make the following decision-ready before asking once:

- repository, service, environment, account, data, and people in scope;
- the external or irreversible effect, publication, merge, release, deletion, production target, and cost that actually cross authority;
- rollback, retry limit, stop condition, and observable completion result;
- safe defaults for low-risk reversible choices;
- prohibited actions and conditions that truly require authority outside the work item.

Authorization does not waive selected checks. It prevents repeated decisions about reversible implementation details inside the same current boundary.

Ordinary external operations do not require a lifecycle work item. Use the target repository or service's existing approval record when present; otherwise the current explicit conversation approval plus the immediately verified target, effect, and stop condition is sufficient authority evidence.

For a regulated record, the runner must not mint authorization from agent-supplied scalar values. It consumes one pre-existing, target-owned, repository-relative JSON file whose exact schema is `schema_version`, `evidence_kind`, `work_id`, `authority_boundary`, `authority_identity`, `approval_reference`, `authorized_scope`, `result_boundary`, `effects`, `rollback`, `stop_conditions`, `expires_at`, and `nonce`. `schema_version` is `1`; `evidence_kind` is `target-owned-authorization`. The file must remain outside runner-owned `.devflow/` and `work/<id>/regulated/` state. Its canonical content and digest stay bound to the authorization and must remain unchanged through verify, close, and check.

The agent and runner may validate, consume, and reference this evidence; they do not create, complete, rewrite, or substitute it on the authorizing party's behalf.

A later discovery belongs to one of three classes:

1. Planned implementation detail: decide and continue.
2. In-scope defect or failed check: fix and continue.
3. Indispensable action outside the boundary: do not execute; record the blocker.

Do not relabel class 3 as an implementation detail. Do not relabel classes 1 or 2 as reasons to interrupt the requester.
