# Evidence map

This map supports `design-frontend-experience`. Project requirements and a versioned source registry remain authoritative over generic design guidance.

| Source | Finding used | Operational rule |
|---|---|---|
| ISO, [ISO 9241-210:2019](https://www.iso.org/standard/77520.html) | Human-centred design is iterative and considers the complete user experience across the system life cycle. | Design from context and tasks, preserve iteration, and carry decisions into implementation and evaluation. |
| Design Council, [Framework for Innovation](https://www.designcouncil.org.uk/resources/framework-for-innovation/) | Develop explores alternative answers before Deliver tests and improves a selected direction. | Compare materially different alternatives for consequential choices and record why one was selected. |
| W3C, [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | Accessibility includes perceivable information, operable interaction, understandable behavior, and robust implementation. | Specify content, keyboard, focus, input, error, reflow, motion, and semantic expectations during design. |
| W3C WAI, [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/) | Common widget patterns require defined keyboard interaction and semantic roles, but native HTML should be preferred where suitable. | Include semantic and keyboard contracts; do not design custom widgets as visual shapes only. |
| Figma, [MCP Server Guide](https://github.com/figma/mcp-server-guide) | Design context is improved by reusable components, variables, semantic layer names, auto layout, annotations, and Code Connect mappings. | Discover and reuse design-system primitives, express responsive intent, and map design components to code where available. |
| Figma, [figma-generate-design skill](https://github.com/figma/mcp-server-guide/blob/main/skills/figma-generate-design/SKILL.md) | Composed views should be assembled incrementally from published components, variables, and styles rather than hardcoded primitives. | Build the design contract from tokens and components and validate section by section. |
| OpenAI, [frontend-skill](https://github.com/openai/skills/blob/main/skills/.curated/frontend-skill/SKILL.md) | Strong frontend work benefits from a visual thesis, restrained hierarchy, cohesive content, imagery, and intentional motion. | Record a coherent visual direction, but subordinate it to user tasks, accessibility, and product consistency. |
| Anthropic, [frontend-design skill](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md) | Distinctive design requires a deliberate conceptual direction rather than generic generated styling. | Avoid unexamined AI defaults and state what makes the direction appropriate and memorable. |
| GOV.UK Design System, [Accessibility](https://design-system.service.gov.uk/accessibility/) | Using accessible components does not by itself make a service accessible; the service must be researched, designed, developed, and tested. | Treat component accessibility as necessary but not sufficient and preserve whole-flow evaluation in the test plan. |

## Limits

- Visual quality is context-dependent; no source provides a universal style prescription.
- Design-system reuse may require an explicit exception when it conflicts with an approved requirement.
- A design artifact does not prove usability or accessibility until implemented and evaluated in context.
