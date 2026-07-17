---
name: verify-against-engineering-standards
description: Verify canonical requirements, generated design, implementation, tests, and operations against versioned SWEBOK and official cloud-vendor best practices using evidence-backed checklists. Use for quality gates, architecture reviews, standards compliance, Well-Architected reviews, or before release. Select only applicable profiles, verify source freshness, and require direct evidence for Pass, a concrete rationale for N/A, and an issue for Fail.
---

# Verify Against Engineering Standards

Apply standards as an independent quality lens without silently overriding the user's canonical requirements.

## Source control

1. Read `governance/standards/registry.json`, or bootstrap it from `assets/standards.registry.json`.
2. Run `scripts/standardsflow.py check`. If a source is stale, inspect its current official page, assess changes, and update the registry/checklist in a separately traceable delta before claiming current best-practice coverage.
3. Use the pinned checklist version for reproducibility. “Latest” without a checked date and official URL is not evidence.

## Review order

1. Validate the durable requirements catalog and generated requirements docs.
2. Check requirement quality and lifecycle practices against SWEBOK.
3. Check generated detailed design against canonical requirement IDs and source manifests.
4. Check implementation and tests against both requirements and generated design; identify missing, wrong, and extra behavior.
5. Select `CORE`, cloud-common, the actual vendor delta, and conditional AI profiles. Do not run every vendor profile mechanically.
6. Evaluate each applicable checklist item with reachable evidence. Use `$adversarial-review` to seek counterexamples for consequential claims.

## Verdict contract

- `Pass`: requirement/check ID plus a repository path, test result, generated manifest, or other directly reachable evidence.
- `N/A`: scope fact explaining why the check cannot apply; not “not needed”.
- `Fail`: violated rule, impact, issue ID, and retest method. Do not convert failure into an exception approval.
- Record the standard source ID and version used. Separate “meets the pinned edition” from “registry freshness confirmed”.

## Completion

Release only when canonical requirements, derived docs, source manifests, tests, selected checklist results, source freshness, and repository audit all pass. Standards can propose improvements, but an unapproved standard-driven scope expansion remains a future requirement delta.
