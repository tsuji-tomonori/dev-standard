# Critical-review challenge playbook

Select techniques from the relevant rows; do not execute every row mechanically.

| Target | Defect hypotheses and challenge techniques | Useful oracle/evidence |
|---|---|---|
| Requirements | contradiction, omission, ambiguous quantifier, undefined term, unverifiable criterion, missing pre/postcondition, conflicting stakeholder outcome | source request, domain rule, acceptance example, traceability |
| Architecture | requirement not allocated, invalid dependency assumption, missing failure behavior, state/order/concurrency contradiction, unowned responsibility | architectural invariant, scenario walkthrough, dependency contract |
| API/data | missing/extra/invalid values, boundary and scale, encoding, duplicates, schema evolution, illegal state transition | schema/property, reference parser, state model |
| Implementation | property-based generation and shrinking, mutation testing, fuzzing, differential implementation, metamorphic relation, race/fault injection | deterministic assertion, mutation score with equivalent review, sanitizer/log |
| Tests | seed a plausible defect, invert predicate, delete validation, perturb boundary, swap ordering, force dependency failure | test must fail for a non-equivalent mutant |
| Tests | assertion repeats implementation, missing requirement, weak oracle, nondeterminism, happy-path bias, surviving plausible mutant | requirement-to-test trace, seeded fault, deterministic result |
| Document/change set | stale reference, internal contradiction, undocumented decision, partial rename, packaging omission, migration gap | repository inventory, link/reference check, clean install |

## Perspective prompts

- Requester/domain: Does every outcome match the actual need? What is missing, over-constrained, or impossible to accept objectively?
- Implementer: Can this be built without inventing behavior? Which assumption, interface, state, or dependency is underspecified?
- Tester: What observation would disprove each claim? Which boundary, transition, failure, or alternative interpretation is uncovered?
- Operator/user: What fails in real sequencing, recovery, scale, configuration, or ordinary usage?
- Maintainer: Which coupling, duplication, compatibility promise, or undocumented decision makes the next change wrong?

## Evaluator checks

- Is the oracle independent from the artifact and its implementation rationale?
- Would swapping order, names, formatting, or verbosity change the verdict?
- Is the rubric tied to a falsifiable requirement rather than preference?
- Can a deterministic checker or qualified human confirm a high-severity result?
- Could the same evidence reproduce the finding for another reviewer?
