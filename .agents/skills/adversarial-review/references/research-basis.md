# Research basis and operational rules

This map records the evidence used to design the skill. It distinguishes techniques supported by research from local workflow choices.

| Source | Research finding used | Operational rule in this skill |
|---|---|---|
| Claessen & Hughes, [QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs](https://research.chalmers.se/en/publication/237427) (ICFP 2000) | Executable properties, generated inputs, custom generators, and counterexample reduction make random testing useful beyond example tests. | Express invariants as properties, generate boundary/adversarial inputs, and minimize failures. |
| Chen et al., [Metamorphic Testing: A Review of Challenges and Opportunities](https://doi.org/10.1145/3143561) (ACM CSUR 2018) | Metamorphic relations provide both test generation and an oracle where exact expected outputs are unavailable. | Define relations across transformed inputs and flag unjustified output changes. |
| Jia & Harman, [An Analysis and Survey of the Development of Mutation Testing](https://doi.org/10.1109/TSE.2010.62) (IEEE TSE 2011) | Artificial faults can assess test-suite adequacy; equivalent mutants are an important limitation. | Use realistic scoped mutants, investigate survivors, and do not count equivalent mutants as failures. |
| Parnas & Weiss, [Active Design Reviews: Principles and Practices](https://doi.org/10.1016/0164-1212(87)90025-2) (1987) | Reviewers are more effective when selected for explicit expertise, focused on suitable aspects, asked to make positive assertions, and given questions that require careful study. | Assign concrete perspectives and questions; require derived answers and evidence instead of general comments. |
| Basili et al., [The Empirical Investigation of Perspective-Based Reading](https://ntrs.nasa.gov/citations/19990018557) (1996) | Requirements reviewers use operational scenarios from distinct perspectives such as user, designer, and tester; combined perspectives aim for broader defect coverage. | Split the review into artifact-relevant perspectives and consolidate unique findings. |
| Laitenberger et al., [An Internally Replicated Quasi-Experimental Comparison of Checklist and Perspective-Based Reading of Code Documents](https://publica.fraunhofer.de/entities/publication/ad72ecaa-e07f-4a34-9ed8-0042bc4ea9c0) (IEEE TSE 2001) | Three industrial studies found perspective-based reading detected more unique code defects at lower defect-detection cost than checklist reading. | Prefer concrete role/scenario passes over one undifferentiated checklist pass. |
| NASA, [Assuring NASA's Safety and Mission Critical Software](https://ntrs.nasa.gov/citations/20160000215) (2015) | IV&V is an objective examination asking whether software does what it should, avoids what it should not do, and behaves under adverse conditions; technical independence matters. | Derive expected behavior independently and challenge both required and forbidden outcomes across the lifecycle. |
| Shi et al., [Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge](https://arxiv.org/abs/2406.07791) (2024) | Pairwise LLM judges exhibit non-random position bias with judge/task variation. | Swap answer order, repeat judgments, use rubrics, and escalate unstable/high-severity cases. |

## Synthesis

The sources converge on six controls:

1. Translate the artifact into falsifiable claims before reviewing it.
2. Reconstruct expectations from authoritative sources independently of the implementation rationale.
3. Use focused reviewer perspectives and concrete questions rather than an undirected pass.
4. Seek contradictions and counterexamples with multiple techniques because no one technique covers all defect classes.
5. Preserve reproducible evidence, scope, budget, uncertainty, and unexamined surfaces.
6. Repair confirmed findings and retest with the unchanged counterexample plus a new holdout variant.
