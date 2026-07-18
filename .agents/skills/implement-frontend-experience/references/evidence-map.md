# Evidence map

This map supports `implement-frontend-experience`. Repository conventions and approved design decisions take precedence over generic framework advice.

| Source | Finding used | Operational rule |
|---|---|---|
| WHATWG, [HTML Living Standard](https://html.spec.whatwg.org/) | HTML elements carry defined semantics, interaction, form, and accessibility behavior. | Start from native elements and platform behavior before creating custom abstractions. |
| W3C WAI, [ARIA Authoring Practices: Read Me First](https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/) | ARIA does not change browser behavior and poorly implemented custom widgets can reduce accessibility; native HTML is preferred when suitable. | Use ARIA to supplement correct semantics, not to repair arbitrary clickable containers. |
| W3C, [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | Conformance depends on perceivable, operable, understandable, and robust behavior across content and interaction. | Implement keyboard, focus, labels, status, errors, reflow, target, authentication, and motion requirements as applicable. |
| Figma, [MCP Server Guide](https://github.com/figma/mcp-server-guide) | Generated code and design context must be translated into project conventions; components, variables, Code Connect, annotations, and visual references improve consistency. | Treat generated output as input, reuse repository primitives, and verify both structured context and rendered result. |
| Figma, [figma-implement-design skill](https://github.com/figma/mcp-server-guide/blob/main/skills/figma-implement-design/SKILL.md) | Figma-to-code work requires design context, screenshots, asset handling, project-convention translation, and visual validation. | Inspect before coding and compare the implementation with both the behavioral contract and visual reference. |
| OpenAI, [frontend-skill](https://github.com/openai/skills/blob/main/skills/.curated/frontend-skill/SKILL.md) | High-quality frontend implementation depends on hierarchy, restraint, cohesive content, and intentional motion rather than component volume. | Preserve the approved visual thesis and avoid clutter or arbitrary feature-like decoration during implementation. |
| Anthropic, [frontend-design skill](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md) | Production frontend work should be functional, cohesive, context-specific, and carefully refined. | Require working states and context-appropriate craft rather than a static mock or generic generated styling. |
| web.dev, [Responsive web design basics](https://web.dev/articles/responsive-web-design-basics) | Responsive layouts depend on flexible content, viewport behavior, and breakpoints driven by layout needs. | Implement reflow rules and test content pressure rather than targeting device labels alone. |
| web.dev, [Core Web Vitals](https://web.dev/articles/vitals) | User-perceived loading, responsiveness, and visual stability can be evaluated with field-oriented performance measures. | Preserve applicable performance budgets and record impact instead of treating visual polish as performance-neutral. |

## Limits

- Framework-specific implementation rules must come from the target repository and its pinned documentation.
- Pixel comparison cannot validate semantics, keyboard behavior, content correctness, or responsive adaptation.
- Automated accessibility rules are implementation feedback, not complete evidence of accessible use.
