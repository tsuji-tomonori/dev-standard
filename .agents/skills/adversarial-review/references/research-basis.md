# Research basis and operational rules

This map records the evidence used to design the skill. It distinguishes peer-reviewed techniques, official assurance guidance, versioned preprints, and local workflow choices. The cross-skill verification record is [`docs/reference/skill-evidence-audit.md`](../../../../docs/reference/skill-evidence-audit.md).

| Class | Source | Finding or authority used | Operational rule |
|---|---|---|---|
| R | Claessen & Hughes, [QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs](https://doi.org/10.1145/357766.351266) (ICFP 2000) | Executable properties, generated inputs, custom generators, and counterexample reduction make random testing useful beyond example tests. | Express invariants as properties, generate boundary/adversarial inputs, and minimize failures. |
| R | Chen et al., [Metamorphic Testing: A Review of Challenges and Opportunities](https://doi.org/10.1145/3143561) (ACM CSUR 2018) | Metamorphic relations provide both test generation and an oracle where exact expected outputs are unavailable. | Define justified relations across transformed inputs and flag unexplained output changes. Validate the relation itself. |
| R | Jia & Harman, [An Analysis and Survey of the Development of Mutation Testing](https://doi.org/10.1109/TSE.2010.62) (IEEE TSE 2011) | Artificial faults can assess test-suite adequacy; equivalent mutants are an important limitation. | Use realistic scoped mutants, investigate survivors, and do not count equivalent mutants as failures. |
| R | Parnas & Weiss, [Active Design Reviews: Principles and Practices](https://doi.org/10.1016/0164-1212(87)90025-2) (1987) | Reviewers are more effective when selected for explicit expertise, focused on suitable aspects, asked to make positive assertions, and given questions that require careful study. | Assign concrete perspectives and questions; require derived answers and evidence instead of general comments. |
| R | Basili et al., [The Empirical Investigation of Perspective-Based Reading](https://doi.org/10.1007/BF00368702) (1996) | Requirements reviewers use operational scenarios from distinct perspectives such as user, designer, and tester; combined perspectives aim for broader defect coverage. | Split the review into artifact-relevant perspectives and consolidate unique findings. |
| R | Laitenberger et al., [An Internally Replicated Quasi-Experimental Comparison of Checklist and Perspective-Based Reading of Code Documents](https://doi.org/10.1109/32.922713) (IEEE TSE 2001) | Three industrial studies found perspective-based reading detected more unique code defects at lower defect-detection cost than checklist reading in the studied setting. | Prefer concrete role/scenario passes over one undifferentiated checklist pass, without claiming universal superiority for every artifact. |
| N | NASA, [Assuring NASA's Safety and Mission Critical Software](https://ntrs.nasa.gov/citations/20160000215) (2015) | IV&V is an objective examination asking whether software does what it should, avoids what it should not do, and behaves under adverse conditions; technical independence matters. | Derive expected behavior independently and challenge required and forbidden outcomes. Do not imply NASA assurance or certification. |
| P | Shi et al., [Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge](https://arxiv.org/abs/2406.07791) (versioned preprint) | Position bias is non-random in the studied judges and varies by judge, task, candidate, and answer-quality gap. | Swap answer order, repeat judgments, use explicit rubrics, and escalate unstable or high-severity cases. Treat reported rates and model rankings as version- and benchmark-bound. |

## Synthesis

The sources converge on six controls:

1. Translate the artifact into falsifiable claims before reviewing it.
2. Reconstruct expectations from authoritative sources independently of the implementation rationale.
3. Use focused reviewer perspectives and concrete questions rather than an undirected pass.
4. Seek contradictions and counterexamples with multiple techniques because no one technique covers all defect classes.
5. Preserve reproducible evidence, scope, budget, uncertainty, and unexamined surfaces.
6. Repair confirmed findings and retest with the unchanged counterexample plus a new holdout variant.

The selection of perspectives, severity thresholds, repair budget, and escalation path is local policy (`L`). An LLM judge is bounded evidence, never the sole oracle for a high-severity conclusion.
