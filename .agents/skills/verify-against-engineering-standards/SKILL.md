---
name: verify-against-engineering-standards
description: Verify canonical requirements, generated design, implementation, tests, and operations against versioned SWEBOK and official cloud-vendor guidance using auditable evidence-backed checklists. Use for quality gates, architecture reviews, standards alignment, Well-Architected reviews, or before release. Select only applicable profiles, verify source freshness, and record applicability, project severity rationale, direct Pass evidence, concrete N/A rationale, Fail remediation, and recheck history. Do not claim compliance merely because guidance was reviewed.
---

# Verify Against Engineering Standards

Apply standards as an independent quality lens without silently overriding the user's canonical requirements. Treat SWEBOK and Well-Architected material as knowledge and decision guidance, not universal normative requirements or proof of compliance.

## Source control

1. Read `governance/standards/registry.json`, or bootstrap it from `assets/standards.registry.json`. Require title, version/publication date, official URL, checked date, scope, change-check date, prior-version change summary, profiles, and a pinned artifact SHA-256 when a local source is used.
2. Run `scripts/standardsflow.py check`. If a source is stale, inspect its current official page, assess changes, and update the registry/checklist in a separately traceable delta before claiming current best-practice coverage.
3. Use the pinned checklist version for reproducibility. “Latest” without a checked date and official URL is not evidence.

## Review order

1. Validate the durable requirements catalog and generated requirements docs.
2. Check requirement quality and lifecycle practices against SWEBOK.
3. Check generated detailed design against canonical requirement IDs and source manifests.
4. Check implementation and tests against both requirements and generated design; identify missing, wrong, and extra behavior.
5. Select `CORE`, then cloud-common, the actual vendor delta, and conditional AI profiles. Within those profiles, use `$right-size-execution` attributes `always_on`, `assurance_levels`, `artifact_tags`, `risk_tags`, changed paths, and `phase`; preserve selector version, input features, selected IDs, excluded count, selected digest, deterministic exclusion sample, and mandatory misses. Treat unselected controls as `not-selected`, not automatic N/A. Reuse prior evidence for duplicate control groups and add only vendor-specific differences.
6. Evaluate each applicable checklist item with reachable evidence. Use `$adversarial-review` to seek counterexamples for consequential claims.
7. Enforce one check, one control, and one evidence decision. Split independent acceptance conditions before reviewing; do not mark a composite item Pass when only part is satisfied.

## Verdict contract

- For every decided item, record base severity, context-derived project severity, severity rationale, reviewer, and review date. Base severity is advisory; project severity is the gate input.
- `Pass`: requirement/check ID plus a repository path, test result, generated manifest, or other directly reachable evidence.
- `N/A`: scope fact explaining why the check cannot apply; not “not needed”. Record reviewer and date even when it is N/A.
- `Fail`: violated rule, impact, issue ID, remediation plan, due date, and retest method. Do not convert failure into an exception approval.
- After remediation, preserve the former Fail in history and record a Pass recheck with reachable evidence, reviewer, and date.
- Record the standard source ID and version used. Separate “aligned with the pinned edition” from “registry freshness confirmed”; neither is a certification or complete compliance claim.

## Completion

Release only when canonical requirements, derived docs, source manifests, tests, selected checklist results, source freshness, selector audit, and repository audit all pass. Unselected rows are not bulk N/A results. Standards can propose improvements, but an unapproved standard-driven scope expansion remains a future requirement delta.
