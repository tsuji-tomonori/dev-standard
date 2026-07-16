# Document rules

## Required qualities

- Atomic: each requirement or decision can be evaluated independently.
- Testable: state a method, threshold, expected result, or explicit review criterion.
- Traceable: connect request → requirement → decision/design → implementation → test → evidence.
- Owned: name the responsible role and approver.
- Version-aware: identify the system/model/configuration version under review.
- Risk-aware: record alternatives, tradeoffs, residual risk, and N/A rationale.

## AI-specific content

For AI work, document the use-case boundary, stakeholders, model/data provenance, lawful basis, release criteria, evaluation dataset, quality/safety thresholds, human oversight, agent authority, tool permissions, monitoring, decommissioning, and cost limits. Do not assume every AI workload needs training, RAG, fine-tuning, multi-region deployment, or an autonomous agent.

## Evidence

Prefer reproducible commands, test reports, signed artifacts, CI URLs, immutable logs, or redacted screenshots. A prose claim by the implementing agent is not independent evidence.
