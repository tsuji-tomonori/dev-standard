---
name: adversarial-review
description: Critically review requirements, designs, implementations, tests, or documents by assuming they may contain mistakes and trying to falsify their claims with contradictions, omissions, counterexamples, independent derivation, and evidence. Use when the user asks whether something is really correct, requests an adversarial or skeptical review, wants assumptions challenged, or needs a rigorous second pass. This is defect-seeking review, not security red teaming or attack simulation.
---

# Adversarial Review

Treat “the artifact contains a mistake” as a search hypothesis. Seek decisive evidence, but let the evidence determine the conclusion. Critique claims and artifacts, never people.

## Prepare the review

1. Read `references/research-basis.md` for the evidence-to-rule map.
2. Read `references/challenge-playbook.md` and choose only the perspectives and techniques relevant to the artifact.
3. Convert the artifact into falsifiable claims: required outcomes, forbidden outcomes, invariants, preconditions, postconditions, assumptions, and trace links.
4. Establish the authoritative source for each claim. Derive expected behavior from that source, not from the artifact's rationale or implementation.
5. State review scope, time/case budget, excluded surfaces, and the standard of evidence.

## Review workflow

1. Reconstruct the intended result independently before reading implementation justifications where practical.
2. Review from distinct perspectives such as requester/domain expert, implementer, tester, operator, and maintainer. Give each perspective concrete questions or tasks instead of asking for general impressions.
3. For every important claim, ask: “What is the smallest observation that would prove this wrong?” Search for contradictions, omissions, ambiguity, unjustified assumptions, unreachable acceptance criteria, over/under-constraint, trace gaps, and unintended behavior.
4. Construct counterexamples using boundaries, invalid and missing values, state/order changes, concurrency, failure paths, alternate interpretations, and scale. Use property-based, metamorphic, differential, or mutation testing when they provide stronger evidence.
5. Make positive assertions: answer the review question and show the derivation or executable evidence. “This seems risky” is not a finding.
6. Separate hypothesis generation from verdicts. For an LLM judge, use an explicit rubric, repeat unstable judgments, swap pairwise order, and independently confirm consequential findings.
7. Classify each finding by violated claim, minimal evidence, impact, confidence, and affected scope. Distinguish confirmed defects, unresolved questions, and preferences.
8. Repair within scope, then rerun the unchanged counterexample, ordinary regression tests, and a new holdout variant. Report with `references/report-template.md`.

## Decision rules

- One valid counterexample is sufficient to disprove the relevant universal claim.
- Absence of a counterexample within a finite review is not proof of correctness. Say what was examined and what remains unexamined.
- Reject a finding that cannot name a violated claim or provide reproducible evidence; record it as a question if uncertainty remains.
- A test suite is inadequate when realistic non-equivalent mutants survive, even if coverage is high.
- Do not use the author's explanation as the sole oracle for the author's result.
- Do not manufacture defects to satisfy the adversarial stance. Confirm correctness when the evidence survives the stated challenge.

## Boundaries

- Do not turn review into security testing unless the request independently requires it.
- Do not invent requirements, silently change the authoritative source, or treat stylistic preference as correctness.
- Be direct about defects without sarcasm, hostility, score-settling, or criticism of the author.
- Stop when a conclusion requires unavailable domain authority or evidence. Record the uncertainty and the smallest fact needed to resolve it.
