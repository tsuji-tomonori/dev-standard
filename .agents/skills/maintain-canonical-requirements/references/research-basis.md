# Evidence-to-rule map

Source classes and the cross-skill verification record are defined in [`docs/reference/skill-evidence-audit.md`](../../../../docs/reference/skill-evidence-audit.md).

| Class | Source | Finding or authority used | Operational rule |
|---|---|---|---|
| G | Design Council, [Framework for Innovation](https://www.designcouncil.org.uk/our-resources/framework-for-innovation/) | The Double Diamond separates divergent exploration from convergent definition, development, and delivery; discovery should understand rather than assume the problem. | Separate discover/define and develop/deliver. Do not converge on the first formulation. Treat the framework as process guidance, not a mandatory lifecycle standard. |
| N | IEEE Computer Society, [SWEBOK Guide Version 4.0a](https://www.computer.org/education/bodies-of-knowledge/software-engineering) | Requirements work includes elicitation, analysis, specification, validation, and ongoing management. | Treat conversation, atomization, validation, change control, and traceability as one lifecycle. Use the version and scope registered in `governance/standards/registry.json`; do not claim complete SWEBOK conformance. |
| N | NASA, [Software Requirements](https://swehb.nasa.gov/display/SWEHBVD/4.1+-+Software+Requirements) | Requirements should be traceable, verifiable, unambiguous, and maintained under change control. | Require stable IDs, acceptance evidence, source links, revisions, and explicit delta operations. Do not imply NASA certification. |
| R | Basili et al., [The Empirical Investigation of Perspective-Based Reading](https://doi.org/10.1007/BF00368702) | Requirements reviewers use operational scenarios from distinct perspectives such as user, designer, and tester. | Review each proposed requirement from stakeholder, implementer, and tester perspectives before persistence. Do not assume every perspective has equal yield for every artifact. |
| L | [`calibrated-collaborative-listening` evidence map](../../calibrated-collaborative-listening/references/evidence-map.md) | Meaning-preserving formulation requires tentative inference, selective clarification, factual boundaries, and concise semantic checks. | Formulate likely intent, ask only path-changing questions, preserve conditions and negations, and allow easy correction. |

The sources guide conversation, review, and lifecycle design. They do not create a durable requirement by themselves. Requirement authority still comes from the user, consumer contract, law, adopted standard, or repository policy.

The JSON shape, revision protocol, generated-document contract, classification defaults, and atomic replacement behavior are local deterministic controls (`L`), not direct empirical findings.
