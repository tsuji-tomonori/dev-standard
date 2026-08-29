---
name: adversarial-review
description: Falsify claims in requirements, designs, code, tests, or documents using contradictions, omissions, counterexamples, and independent evidence. Use for adversarial, skeptical, or rigorous second-pass review; not attack simulation.
---

# Adversarial Review

## Formal specification

`spec/skills/skills.qnt` の `skillContracts` にある `name: "adversarial-review"` を形式契約とする。

形式契約の`applicability`と`activationContexts`に該当しない場合は起動せず、artifactやblocking判定を作らないno-opとする。

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
8. Return a bounded repair handoff that names the violated claim, minimal change, unchanged counterexample, ordinary regression tests, and a new holdout variant. Report with `references/report-template.md`.

If no claim is falsified, return an explicit scoped `no finding` conclusion, the evidence examined, and residual uncertainty. A repair handoff is conditional on a confirmed defect; it is not manufactured for a no-finding result.

## Decision rules

- One valid counterexample is sufficient to disprove the relevant universal claim.
- Absence of a counterexample within a finite review is not proof of correctness. Say what was examined and what remains unexamined.
- Reject a finding that cannot name a violated claim or provide reproducible evidence; record it as a question if uncertainty remains.
- A test suite is inadequate when realistic non-equivalent mutants survive, even if coverage is high.
- Do not use the author's explanation as the sole oracle for the author's result.
- Do not manufacture defects to satisfy the adversarial stance. Confirm correctness when the evidence survives the stated challenge.

## Boundaries

- This is not security red teaming or attack simulation.
- This is a review-only Skill. Do not modify the reviewed artifact; an independently authorized implementation Skill owns any repair and returns the result for re-review.
- Do not turn review into security testing unless the request independently requires it.
- Do not invent requirements, silently change the authoritative source, or treat stylistic preference as correctness.
- Be direct about defects without sarcasm, hostility, score-settling, or criticism of the author.
- Stop when a conclusion requires unavailable domain authority or evidence. Record the uncertainty and the smallest fact needed to resolve it.

## Completion

- The result is either confirmed findings with conditional repair handoffs, or a scoped no-finding conclusion.
- Every verdict names the authority, examined evidence, excluded surface, and residual uncertainty.
- The reviewed artifact remains unchanged.

<!-- BEGIN GENERATED QUINT CONTRACT -->
## Quint contract（自動生成）

このblockは`spec/skills/skills.qnt`から生成するviewです。直接編集しません。

- Skill: `adversarial-review`
- 役割: independent-review
- 柱: auxiliary
- guardrail: no
- repository blocking: no
- 既定portable: no
- 適用条件: when-explicitly-requested
- 起動context: `explicit-review-request`
- 外部作用capability: no
- repository policy `ciWorkflow`: false
- repository policy `requiredCheck`: false
- repository policy `branchProtection`: false
- repository policy `ruleset`: false
- repository policy `mergeStrategy`: false
- repository policy `prTemplate`: false
- repository policy `commitFormat`: false
- 前提: falsifiable claims and an authority are available
- 事後条件: a bounded review report, including an explicit no-finding result when appropriate, is returned without mutating the artifact
- Authority: artifact-authority
- 副作用: none
- 失敗状態: report-bounded
- 入力: `artifact`, `authority`, `review-scope`
- 出力: `review-result`, `optional-findings`, `residual-uncertainty`, `conditional-repair-handoff`
- 義務: `reconstruct-independent-authority`, `seek-falsifying-evidence`, `allow-evidence-supported-no-finding-result`, `report-bounded-findings`
- 禁止事項: `do not mutate the reviewed artifact`, `do not claim proof from a finite review`, `do not invent requirements`
- 依存Skill: なし
- 必須asset: `references/challenge-playbook.md`, `references/report-template.md`, `references/research-basis.md`
- 要件trace: なし
- manual digest: `09678c3a766efe9f49c35f2fc930381e14e1465e651b3fe2135521fa847beb47`
- payload digest: `9ad70d5f3a5dda494f0249985dfdea45c00bb217418a8be95476324f243dff99`
- interface digest: `2a288a121591cb1bd3c950bc18615d267d1edf0f28331f2157aa7296ef9ef856`
<!-- END GENERATED QUINT CONTRACT -->
