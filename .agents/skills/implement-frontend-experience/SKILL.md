---
name: implement-frontend-experience
description: Implement an approved frontend experience in production code from canonical requirements and detailed design. Use when building or changing frontend pages, flows, components, styling, responsive behavior, content states, interaction, accessibility, design tokens, or Figma-derived UI. Reuse the existing stack and design system, implement complete states and semantics, validate incrementally, and record any design divergence instead of improvising hidden requirements.
---

# Implement Frontend Experience

Translate the approved frontend design contract into maintainable, accessible, responsive production code without losing intent between design and implementation.

## Required inputs and composition

- Read the original request, canonical requirements, `docs/03-detailed-design.md`, `docs/03-test-plan.md`, architecture decisions, and the relevant existing frontend before editing code.
- Use `$design-frontend-experience` when the required behavior, state, content, token, component, responsive rule, or accessibility contract is missing or contradictory.
- Use `$author-lifecycle-docs` to maintain `docs/04-implementation-log.md` and actual trace mappings.
- Use `$verify-against-engineering-standards` for applicable accessibility, framework, platform, security, privacy, and performance guidance.
- Use `$adversarial-review` after implementation for high-risk interaction, design-system changes, destructive actions, authorization boundaries, or broad shared-component changes.

Read `references/evidence-map.md` when maintaining this skill, selecting implementation rules, or explaining the basis for design-system and accessibility decisions.

## Workflow

1. Inspect before editing:
   - framework, routing, state management, data fetching, forms, validation, internationalization, testing, and build conventions;
   - existing tokens, themes, primitives, shared components, feature components, icons, assets, and styling approach;
   - supported browsers, devices, rendering modes, performance budgets, and accessibility tooling;
   - nearby implementations that express the same product convention.
2. Build the implementation slice from the requirement-to-design matrix. Prefer a vertical slice that completes one user task and its states over creating disconnected visual components.
3. Reuse in this order:
   1. native platform or semantic HTML behavior;
   2. established design-system tokens and components;
   3. existing feature patterns;
   4. a justified extension to the design system;
   5. a local primitive only when the preceding options cannot satisfy the approved design.
4. Treat generated Figma or model output as design evidence, not final repository code. Translate it to project naming, architecture, components, tokens, state management, tests, localization, and accessibility conventions.
5. Implement semantic structure first. Choose elements and interaction models by meaning and behavior, then style them. Do not replace a native control with a generic element plus ARIA unless the approved interaction genuinely requires a custom widget.
6. Implement the complete applicable state contract:
   - default and populated;
   - hover, focus-visible, active or pressed, selected, and visited;
   - disabled and read-only;
   - loading, delayed, progressive, and cancellation;
   - empty, no-results, partial, stale, and offline;
   - field and form validation, system error, conflict, permission denied, success, undo, and retry.
7. Preserve all input paths and alternatives specified by design:
   - keyboard operation and logical focus order;
   - focus placement and restoration for dialogs, drawers, menus, route changes, errors, and removed content;
   - pointer and touch behavior;
   - non-drag and non-gesture alternatives;
   - visible labels, accessible names, descriptions, status messages, and error associations;
   - reduced-motion behavior and no information conveyed by color or motion alone.
8. Implement responsiveness as content and layout rules. Verify long content, localization expansion, zoom, reflow, small viewports, large viewports, virtual keyboards, and dense data according to the approved support matrix.
9. Use semantic design tokens rather than repeated literal style values when a token exists or the value expresses a reusable decision. Do not create a new token for every local number; add tokens when they encode a stable design role.
10. Keep component APIs narrow and meaningful. Model variants and states explicitly, prevent invalid combinations where practical, preserve composition, and avoid boolean-prop collections that hide mutually exclusive modes.
11. Keep content production-ready. Use approved terminology and representative data. Do not leave lorem ipsum, unexplained icon-only actions, generic error messages, or silent failures in completed flows.
12. Implement in small coherent steps and validate each slice:
   - type and build checks;
   - lint and static accessibility rules;
   - unit and component tests for behavior and states;
   - browser rendering and interaction checks;
   - screenshots or visual comparison when a visual reference exists.
13. Compare the result with the design contract, not only with a screenshot. Check behavior, content, states, responsive rules, semantics, focus, tokens, and component mapping.
14. Record actual changed paths, reused and added primitives, requirement and design IDs, test evidence, performance effects, and every divergence in `docs/04-implementation-log.md`.
15. When implementation exposes a design defect, update the derived design and test plan within the authorized scope before continuing. When it exposes a materially new product obligation, route a canonical delta through `$maintain-canonical-requirements` rather than hiding it in code.

## Implementation boundaries

- Do not redesign opportunistically while coding merely because another styling choice is easier.
- Do not duplicate an existing component to avoid understanding its API.
- Do not hardcode Figma coordinates, colors, typography, or breakpoints when project primitives express the same intent.
- Do not claim accessibility from semantic-looking markup or a passing automated scanner alone.
- Do not add animations that lack purpose, ignore reduced-motion preferences, delay task completion, or conceal state changes.
- Do not optimize for a single screenshot at the expense of real content, zoom, localization, or interactive states.
- Do not weaken types, lint rules, tests, or design-system constraints to make the implementation pass.

## Code review gates

The implementation is not ready for verification when:

- an applicable requirement or design decision has no changed code or explicit N/A rationale;
- state behavior exists only for the happy path;
- keyboard or focus behavior depends on browser accident rather than an intentional contract;
- new visual literals duplicate existing tokens or shared components;
- custom widgets lack complete semantics and interaction behavior;
- responsive behavior fails with representative content or supported zoom and reflow;
- implementation differs from the approved design without a recorded rationale and updated trace;
- tests assert CSS details while missing task behavior and user-visible outcomes;
- `docs/04-implementation-log.md` cannot identify what was implemented and how it was validated.

## Completion

Complete when the approved frontend task works through all applicable states and supported contexts, requirements and design decisions map to code and tests, reused and new design-system elements are explicit, incremental checks pass, divergences are resolved or recorded, and the implementation log contains reproducible evidence for the verification phase.
