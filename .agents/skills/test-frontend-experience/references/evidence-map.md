# Evidence map

This map supports `test-frontend-experience`. Each method has bounded coverage; combine methods according to risk rather than treating one tool as complete proof.

| Source | Finding used | Operational rule |
|---|---|---|
| ISO, [ISO 9241-11:2018](https://www.iso.org/standard/63500.html) | Usability is an outcome of use in context. | Evaluate specified users, goals, tasks, resources, and environment rather than an interface in isolation. |
| W3C WAI, [Evaluating Web Accessibility Overview](https://www.w3.org/WAI/test-evaluate/) | Accessibility evaluation combines standards, methods, tools, and human judgment. | Use automated checks as one layer and preserve manual and assistive-technology evaluation. |
| W3C WAI, [Easy Checks](https://www.w3.org/WAI/test-evaluate/preliminary/) | Preliminary checks reveal common barriers but are not a complete accessibility evaluation. | Never equate a quick scan or checklist with full conformance. |
| W3C, [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | Success criteria define testable accessibility outcomes across content and interaction. | Map applicable criteria to concrete pages, components, states, inputs, and evidence. |
| W3C WAI, [Involving Users in Web Accessibility](https://www.w3.org/WAI/test-evaluate/involving-users/) | Evaluation with disabled people identifies real-use issues but does not replace standards-based review. | Treat participant observation and conformance inspection as complementary evidence. |
| W3C WAI, [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/) | Composite widgets have expected semantic and keyboard interaction patterns. | Test rendered roles, names, states, focus, and keyboard commands for custom widgets. |
| Brooke, [System Usability Scale](https://www.usability.gov/how-to-and-tools/methods/system-usability-scale.html) | SUS is a compact subjective usability questionnaire, not a direct behavioral measure. | Use subjective scores only alongside task evidence and report their scope. |
| UEQ Team, [User Experience Questionnaire](https://www.ueq-online.org/) | UEQ instruments measure multiple subjective experience dimensions with defined analysis tools. | Use only when those dimensions answer an approved evaluation question; do not substitute them for task success. |
| Moshagen and Thielsch, [Visual Aesthetics of Websites Inventory](https://doi.org/10.1080/10447318.2010.535239) | Visual aesthetics can be measured as a construct distinct from usability. | Keep visual-quality judgments separate from task performance and accessibility verdicts. |
| Nielsen Norman Group, [Aesthetic-Usability Effect](https://www.nngroup.com/articles/aesthetic-usability-effect/) | Attractive interfaces may be perceived as easier to use and can mask usability problems. | Verify behavior independently from visual preference and satisfaction. |
| web.dev, [Core Web Vitals](https://web.dev/articles/vitals) | Loading, interaction responsiveness, and visual stability require runtime evidence. | Test applicable performance outcomes under representative conditions and record metric context. |

## Limits

- No single browser, viewport, automated tool, participant, or questionnaire proves universal quality.
- Small qualitative samples support problem discovery, not precise population estimates.
- Test reports must identify versions, environments, data, and unexecuted scope to remain auditable.
