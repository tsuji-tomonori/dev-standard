# Evidence map

This map supports the operational rules in `elicit-frontend-requirements`; it does not claim that a short agent interview replaces direct user research or professional ergonomics work. Source classes and the full audit are defined in [`docs/reference/skill-evidence-audit.md`](../../../../docs/reference/skill-evidence-audit.md).

| Class | Source | Finding or authority used | Operational rule |
|---|---|---|---|
| N | ISO, [ISO 9241-210:2019](https://www.iso.org/standard/77520.html) | Human-centred design activities and principles apply throughout the life cycle of interactive systems. | Establish context of use, involve affected people when possible, iterate, and carry human-centred evidence beyond intake. |
| N | ISO, [ISO 9241-11:2018](https://www.iso.org/standard/63500.html) | Usability is an outcome of use in a specified context rather than an intrinsic adjective of an interface. | Replace “intuitive” or “easy” with contextual effectiveness, efficiency, satisfaction, risk, or review criteria. |
| G | Design Council, [Framework for Innovation](https://www.designcouncil.org.uk/our-resources/framework-for-innovation/) | Discover and define should precede development and delivery; divergence and convergence are distinct. | Do not converge on the first UI solution or on the requester's first visual example. Treat the framework as process guidance, not a mandatory standard. |
| L | Existing [`calibrated-collaborative-listening`](../../calibrated-collaborative-listening/SKILL.md) evidence map | Common ground, perspective-getting, selective follow-up questions, autonomy, and meaning-preserving compression improve formulation quality within documented limits. | Reuse the existing listening skill; ask only path-changing questions and present inference as correctable. |
| L | Existing [`maintain-canonical-requirements`](../../maintain-canonical-requirements/SKILL.md) research basis | Requirements require elicitation, analysis, specification, validation, change control, and traceability. | Promote durable frontend obligations into the one canonical catalog as atomic deltas. |
| N | W3C WAI, [WCAG 2 Overview](https://www.w3.org/WAI/standards-guidelines/wcag/) | Accessibility requirements concern content, structure, presentation, and interaction, including mobile use. | Elicit accessibility, input modality, content, and reflow needs during requirements rather than deferring them to testing. Use the applicable versioned Recommendation for conformance. |
| G | W3C WAI, [Involving Users in Web Accessibility](https://www.w3.org/WAI/test-evaluate/involving-users/) | Evaluation with people with disabilities complements standards-based inspection and reveals real use barriers. | Record when direct participation is needed and do not infer all access needs from automated rules. |
| G | GOV.UK Service Manual, [User research](https://www.gov.uk/service-manual/user-research) | Research should understand users, tasks, constraints, and whether a service solves the right problem. | Start with work and context, separate evidence from assumptions, and avoid preference-only interviews. |

## Evidence boundary

A source in this map does not by itself create a project requirement. Durable obligations still require an identified authority and must be persisted through `maintain-canonical-requirements`.

## Limits

- A requester may not represent every user group.
- Interview statements are reported or elicited evidence, not automatically verified behavior.
- Prototype and usability evaluation are required when actual interaction quality is consequential.
- Standards and design-system guidance must be versioned through `$verify-against-engineering-standards` when used as a gate.
