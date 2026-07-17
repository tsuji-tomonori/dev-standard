# Risk-based attack playbook

Select techniques from the relevant rows; do not execute every row mechanically.

| Target | Falsification techniques | Useful oracle/evidence |
|---|---|---|
| Requirements | counterexample, conflicting stakeholder goal, missing pre/postcondition, misuse/abuse case, extreme scale/time/order | acceptance criteria, domain rule, traceability |
| Architecture | trust-boundary crossing, confused deputy, single point of failure, dependency outage, replay/reordering, degraded mode | invariant, threat model, failure-mode test |
| API/data | malformed and oversized values, encoding/canonicalization, duplicate/replay, schema drift, authorization matrix, state transition | schema/property, reference parser, audit log |
| Implementation | property-based generation and shrinking, mutation testing, fuzzing, differential implementation, metamorphic relation, race/fault injection | deterministic assertion, mutation score with equivalent review, sanitizer/log |
| Tests | seed a plausible defect, invert predicate, delete validation, perturb boundary, swap ordering, force dependency failure | test must fail for a non-equivalent mutant |
| AI/model | paraphrase/language variation, multi-turn escalation, instruction conflict, jailbreak, output-format pressure, hallucination/grounding challenge | policy rubric plus independent confirmation |
| Tool-using agent | indirect prompt injection in tool data, synthetic-secret exfiltration, unauthorized tool call, excessive permissions, cross-task data leak | tool trace, capability policy, synthetic canary |
| Mitigation | adaptive variant, transfer attack, alternate modality/path, repeated trials, benign near-neighbor | attack success, utility, over-refusal, variance |

## Minimum portfolio by risk

- Low: one independent oracle, boundary/negative cases, ordinary regression.
- Medium: Low plus property/metamorphic or mutation test, failure path, holdout variant.
- High/Critical: Medium plus explicit threat model, independent evaluator, adaptive attack, benign utility control, reproducible artifact review, residual-risk decision.

## Evaluator checks

- Is the judge independent from the generator and implementation rationale?
- Would swapping order, names, formatting, or verbosity change the verdict?
- Is the rubric tied to a falsifiable requirement rather than preference?
- Can a deterministic checker or qualified human confirm a high-severity result?
- Are false positives, over-refusal, and ordinary-task failure measured?

