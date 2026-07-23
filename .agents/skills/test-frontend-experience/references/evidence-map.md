# Evidence map

This map supports `test-frontend-experience`. Each method has bounded coverage; combine methods according to risk rather than treating one tool as complete proof. Source classes and the full audit are defined in [`docs/reference/skill-evidence-audit.md`](../../../../docs/reference/skill-evidence-audit.md).

| Class | Source | Finding or authority used | Operational rule |
|---|---|---|---|
| N | ISO, [ISO 9241-11:2018](https://www.iso.org/standard/63500.html) | Usability is an outcome of use in context. | Evaluate specified users, goals, tasks, resources, and environment rather than an interface in isolation. |
| G | W3C WAI, [Evaluating Web Accessibility Overview](https://www.w3.org/WAI/test-evaluate/) | Accessibility evaluation combines standards, methods, tools, and human judgment. | Use automated checks as one layer and preserve manual and assistive-technology evaluation. |
| G | W3C WAI, [Easy Checks](https://www.w3.org/WAI/test-evaluate/preliminary/) | Preliminary checks reveal common barriers but are not a complete accessibility evaluation. | Never equate a quick scan or checklist with full conformance. |
| N | W3C, [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | Success criteria define testable accessibility outcomes across content and interaction. | Map applicable criteria to concrete pages, components, states, inputs, and evidence. |
| G | W3C WAI, [Involving Users in Web Accessibility](https://www.w3.org/WAI/test-evaluate/involving-users/) | Evaluation with disabled people identifies real-use issues but does not replace standards-based review. | Treat participant observation and conformance inspection as complementary evidence. |
| G | W3C WAI, [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/) | Composite widgets have expected semantic and keyboard interaction patterns. APG examples do not themselves provide conformance. | Test rendered roles, names, states, focus, and keyboard commands for custom widgets. |
| R | Brooke (1996), [SUS—A Quick and Dirty Usability Scale](https://www.researchgate.net/publication/319394819_SUS_--_a_quick_and_dirty_usability_scale) | SUS is a ten-item global subjective usability assessment developed for low-cost comparison. It is not a direct behavioral measure. | Use subjective scores only alongside task evidence and report participants, context, administration, and interpretation. |
| R | Laugwitz, Held, & Schrepp (2008), [Construction and Evaluation of a User Experience Questionnaire](https://doi.org/10.1007/978-3-540-89350-9_6) | UEQ measures defined subjective experience dimensions with a documented instrument and analysis method. | Use it only when those dimensions answer an approved evaluation question; do not substitute it for task success. |
| R | Moshagen & Thielsch (2010), [Facets of Visual Aesthetics](https://doi.org/10.1016/j.ijhcs.2010.05.006) | VisAWI operationalizes visual aesthetics as a multidimensional construct distinct from usability. | Keep visual-quality judgments separate from task performance and accessibility verdicts. |
| R | Tractinsky, Katz, & Ikar (2000), [What Is Beautiful Is Usable](https://doi.org/10.1016/S0953-5438(00)00031-X) | In the studied ATM-like interface, perceived aesthetics related strongly to perceived usability. The result is context-bound and does not show that attractiveness always masks defects. | Verify behavior independently from visual preference and satisfaction. |
| G | web.dev, [Core Web Vitals](https://web.dev/articles/vitals) | Loading, interaction responsiveness, and visual stability require runtime evidence and context. | Test applicable performance outcomes under representative conditions and record metric source, environment, percentile, and limitations. |

## Evidence boundary

Questionnaires, visual ratings, automated accessibility rules, performance metrics, screenshots, and LLM review are different evidence types. None may be silently promoted to a complete usability, accessibility, or quality verdict.

## Limits

- No single browser, viewport, automated tool, participant, or questionnaire proves universal quality.
- Small qualitative samples support problem discovery, not precise population estimates.
- Test reports must identify versions, environments, data, participants where applicable, and unexecuted scope to remain auditable.
