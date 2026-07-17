---
name: adversarial-validation
description: Try to falsify requirements, designs, implementations, tests, mitigations, or AI-agent behavior with a threat-model-driven and research-grounded validation campaign. Use before releasing security-sensitive, safety-critical, AI-enabled, authorization-changing, or externally exposed changes; after a mitigation or escaped defect; or whenever the user asks for adversarial review, red teaming, abuse cases, robustness testing, counterexamples, mutation testing, fuzzing, prompt-injection testing, or an independent challenge of a proposed solution.
---

# Adversarial Validation

Seek evidence that the change is wrong, unsafe, incomplete, or brittle. Do not re-perform the author's confirmation review.

## Required preparation

1. Read `references/research-basis.md` for the evidence-to-rule map.
2. Read `references/attack-playbook.md` and select only techniques relevant to the target and authorized environment.
3. Define the validation target as falsifiable claims: requirements, invariants, forbidden outcomes, trust boundaries, mitigations, and expected utility.
4. Write a threat model with assets, lifecycle stage, attacker goal, capability, knowledge, access, and test budget. State excluded surfaces.
5. Choose an oracle independent of the implementation where possible: specification property, reference implementation, differential comparison, metamorphic relation, deterministic checker, or qualified human review.

## Campaign

1. Establish benign baseline behavior and existing test results.
2. Build a risk-weighted attack portfolio. Include boundary and malformed inputs, state/order/concurrency variation, fault injection, abuse and privilege paths, and test mutation where relevant. For AI or agents, include direct and indirect prompt injection, untrusted tool data, multi-turn adaptation, data exfiltration attempts with synthetic secrets, multilingual/paraphrased variants, and over-refusal controls.
3. Separate case generation from judging. Blind or randomize presentation when practical. For an LLM judge, repeat judgments, swap pairwise order, use an explicit rubric, and confirm high-severity findings with a deterministic oracle or human reviewer.
4. Execute only in an authorized local, test, or isolated environment. Preserve the exact input, environment/version, seed or generation method, query/time budget, expected and actual behavior, minimal counterexample, and logs.
5. Classify each finding by violated claim, exploitability, impact, confidence, and reachability. A crash, policy violation, silent semantic divergence, surviving mutant, or mitigation bypass is evidence; stylistic disagreement is not.
6. Repair within the authorized scope, then rerun the unchanged reproducer, ordinary regression tests, benign utility controls, and holdout/adaptive variants. Do not tune only to disclosed examples.
7. Report tested and untested surfaces, attack budget, findings, fixes, residual risk, and evidence using `references/report-template.md`.

## Decision rules

- One reproducible high-impact counterexample is sufficient to fail the relevant claim.
- No finding within a finite budget is not proof of safety. Say “no counterexample found under this campaign,” never “secure” or “verified.”
- A defense fails if it blocks the attack by destroying required benign utility.
- A test suite is inadequate when realistic non-equivalent mutants survive, even if coverage is high.
- An AI-only judgment cannot be the sole basis for accepting a high-severity safety claim.
- Keep the attack set extensible and add variants after each mitigation; static benchmark success is not closure.

## Hard boundaries

- Do not attack third-party or production systems, use real secrets or personal data, create persistence, evade authorization, publish actionable exploit material, or perform destructive actions.
- Use synthetic canaries and minimum necessary artifacts. Redact sensitive details from Git and PRs.
- Stop when safe reproduction requires new authority, real victim data, production access, or an irreversible operation. Record the exact blocker and a safe test substitute.

