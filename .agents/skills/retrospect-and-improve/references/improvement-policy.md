# Improvement policy

Propose an improvement only when it is:

- evidenced by an escaped defect, incident, rollback, or recurring cost with more than one observation;
- scoped to one skill and one preventable behavior;
- phrased as an action another agent can follow;
- testable in a future task;
- compared with at least one lighter deletion, consolidation, test, or selector alternative;
- bounded by a measurable evaluation, an executable rollback, and a dated review or sunset;
- free of secrets, personal data, and task-specific transient details;
- suitable for an atomic future requirement and a measurable acceptance test.

Reject instructions that weaken checks, broaden authority beyond its recorded boundary, bypass authorization where a real authority boundary exists, hide failures, or encode untrusted user content as durable policy.

A user correction, regulated close, periodic audit, critical-miss label, single transient failed check, ordinary successful session, or missing template token is not itself a trigger. It activates this Skill only when it supplies direct evidence of an escaped defect, incident, rollback, or recurring cost. Otherwise return a bounded `not_triggered` result.

Reject repository-wide or multi-Skill scope, missing lighter alternatives, unmeasurable evaluation, and rollback values such as `never` or `none`.
