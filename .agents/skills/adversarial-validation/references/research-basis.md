# Research basis and operational rules

This map records the evidence used to design the skill. It distinguishes techniques supported by research from local workflow choices.

| Source | Research finding used | Operational rule in this skill |
|---|---|---|
| Claessen & Hughes, [QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs](https://research.chalmers.se/en/publication/237427) (ICFP 2000) | Executable properties, generated inputs, custom generators, and counterexample reduction make random testing useful beyond example tests. | Express invariants as properties, generate boundary/adversarial inputs, and minimize failures. |
| Chen et al., [Metamorphic Testing: A Review of Challenges and Opportunities](https://doi.org/10.1145/3143561) (ACM CSUR 2018) | Metamorphic relations provide both test generation and an oracle where exact expected outputs are unavailable. | Define relations across transformed inputs and flag unjustified output changes. |
| Jia & Harman, [An Analysis and Survey of the Development of Mutation Testing](https://doi.org/10.1109/TSE.2010.62) (IEEE TSE 2011) | Artificial faults can assess test-suite adequacy; equivalent mutants are an important limitation. | Use realistic scoped mutants, investigate survivors, and do not count equivalent mutants as failures. |
| Perez et al., [Red Teaming Language Models with Language Models](https://arxiv.org/abs/2202.03286) (2022) | Automated generation scales the diversity and difficulty of harmful test cases and can expose multi-turn harms, but is one tool among several. | Use model-generated variants for breadth, include multi-turn cases, and retain independent judging/human escalation. |
| Ganguli et al., [Red Teaming Language Models to Reduce Harms](https://arxiv.org/abs/2209.07858) (2022) | Transparent instructions, processes, datasets, statistical methods, and uncertainty are central to interpretable red-team results. | Record method, budget, artifacts, uncertainty, tested population, and residual risk. |
| Perez et al., [Discovering Language Model Behaviors with Model-Written Evaluations](https://arxiv.org/abs/2212.09251) (2022) | Model-written evaluations can scale discovery of behavioral tendencies, including concerning behavior. | Use generated evaluations for discovery, not as a sole high-severity acceptance oracle. |
| Shi et al., [Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge](https://arxiv.org/abs/2406.07791) (2024) | Pairwise LLM judges exhibit non-random position bias with judge/task variation. | Swap answer order, repeat judgments, use rubrics, and escalate unstable/high-severity cases. |
| Chao et al., [JailbreakBench](https://arxiv.org/abs/2404.01318) (NeurIPS 2024) | Reproducible adversarial evaluation needs an explicit threat model, prompts/artifacts, scoring, query cost, benign behaviors, and standardized comparisons. | Preserve artifacts and budgets; report attack success together with benign utility/over-refusal. |
| Debenedetti et al., [AgentDojo](https://arxiv.org/abs/2406.13352) (NeurIPS 2024) | Tool-using agents face indirect prompt injection through untrusted data; dynamic, extensible tasks are needed because attacks and defenses evolve. | Test untrusted tool outputs, task utility, adaptive attacks, and post-mitigation variants. |
| NIST, [Adversarial Machine Learning: Taxonomy and Terminology](https://doi.org/10.6028/NIST.AI.100-2e2025) (AI 100-2, 2025) | Attack assessment should identify lifecycle stage, attacker goals/objectives, capabilities, knowledge, and applicable mitigations; no universal defense exists. | Require a scoped threat model and state residual/untested risk rather than claiming complete security. |
| OpenAI, [GPT-4o System Card](https://openai.com/index/gpt-4o-system-card/) (2024) | External experts, multiple phases/checkpoints, multi-turn testing, automated graders plus human labels, and targeted evals were combined for risk discovery and mitigation testing. | Combine exploratory and structured phases, automation and independent review, then convert findings into regression evaluations. |

## Synthesis

The sources converge on five controls:

1. Define falsifiable properties and an attacker model before generating cases.
2. Use a portfolio because no single generator, benchmark, judge, or defense is sufficient.
3. Separate attack generation from evaluation and test evaluator stability.
4. Preserve reproducible artifacts, budget, uncertainty, and benign utility.
5. Repair findings and retest with unchanged reproducers plus new holdout/adaptive variants.

