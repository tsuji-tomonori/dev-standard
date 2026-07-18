---
name: design-frontend-experience
description: Design a traceable frontend experience from approved human-centred requirements before coding. Use for information architecture, task flows, wireframes, visual direction, responsive behavior, interaction states, content hierarchy, design tokens, components, motion, and accessibility design. Inspect and reuse the existing design system, record alternatives and rationale, and produce implementation-ready detailed design and test design without silently inventing product requirements.
---

# Design Frontend Experience

Convert approved frontend requirements into an implementation-ready interaction and visual contract.

## Required inputs and composition

- Read the user request, canonical requirement IDs, `docs/01-requirements.md`, `docs/01-traceability.md`, and relevant architecture and risk decisions before designing.
- Use `$elicit-frontend-requirements` when the problem, users, context, outcomes, or consequential preferences remain undefined. Do not cover a requirements gap with visual invention.
- Use `$author-lifecycle-docs` to maintain `docs/03-detailed-design.md` and `docs/03-test-plan.md`.
- Use `$verify-against-engineering-standards` for applicable accessibility, platform, ergonomic, and organizational design-system guidance.
- Use `$adversarial-review` for high-impact flows, destructive actions, security or privacy boundaries, complex data entry, or designs whose aesthetic direction may obscure usability.

Read `references/evidence-map.md` when selecting a design method, maintaining this skill, or explaining its basis.

## Workflow

1. Inspect the existing frontend before proposing changes:
   - routes, layouts, navigation, page and component structure;
   - design tokens, themes, typography, icons, spacing, breakpoints, motion, and component variants;
   - existing interaction conventions, validation, content language, accessibility patterns, and known exceptions;
   - Figma, screenshots, Storybook, design-system documentation, or Code Connect mappings when available.
2. Build a requirement-to-design matrix. Every applicable requirement must map to at least one task flow, screen or surface, state, component or content decision, and planned verification. Record non-visual requirements explicitly.
3. Design in this order:
   1. user task and completion path;
   2. information architecture and navigation;
   3. content hierarchy and terminology;
   4. interaction model and state transitions;
   5. responsive and input-modality behavior;
   6. accessibility semantics and focus behavior;
   7. visual direction, typography, color roles, spacing, density, imagery, and motion;
   8. design tokens, reusable components, variants, and composition rules.
4. For a consequential design choice, create at least two materially different alternatives when doing so could reveal a better task model or trade-off. Compare alternatives against requirements, context, accessibility, implementation cost, consistency, and risk. Do not create decorative variants that differ only in color.
5. Choose one coherent visual thesis appropriate to the product and users. Record the intended character and the one or two visual ideas that carry it. Avoid generic AI defaults, but do not sacrifice comprehension, platform conventions, or existing product coherence merely to be distinctive.
6. Prefer the existing design system. Reuse tokens and components before introducing new ones. When existing primitives cannot satisfy a requirement, record the gap, proposed addition, compatibility impact, migration path, and why local one-off styling is insufficient.
7. Specify complete states for each interactive element and surface as applicable:
   - initial and default;
   - hover, focus-visible, active or pressed, selected, and visited;
   - disabled and read-only;
   - loading, progressive loading, skeleton, and delayed response;
   - empty, no-results, partial, stale, and offline;
   - validation error, system error, permission denied, conflict, success, undo, and recovery.
8. Specify interaction behavior without relying on visuals alone:
   - semantic role and accessible name source;
   - keyboard sequence, focus entry, movement, return, and restoration;
   - pointer, touch, drag, gesture, and non-drag alternatives;
   - announcements for dynamic changes when needed;
   - destructive-action safeguards and reversible recovery;
   - reduced-motion behavior.
9. Specify responsive behavior as rules, not a list of screenshots. State what reflows, collapses, becomes scrollable, changes order, moves to another surface, or must remain visible. Use content and task pressure to choose breakpoints; do not invent arbitrary device support.
10. Specify real or representative content. Include long labels, localization expansion, missing values, validation text, permission differences, and realistic data density. Placeholder copy cannot prove hierarchy or layout resilience.
11. Define a token and component contract:
   - semantic color, typography, spacing, sizing, radius, elevation, opacity, motion, and layering roles;
   - component anatomy, variants, properties, composition, constraints, and prohibited misuse;
   - mapping to existing code or Figma components when available;
   - intentional exceptions with rationale and owner.
12. Place verification hooks in `docs/03-test-plan.md`: requirement ID, task, state, viewport or input context, expected result, evidence type, and whether automated, expert-reviewed, or participant-observed.
13. Record decisions and rejected alternatives. A screenshot alone is not a design specification; preserve behavior, state, content, token, component, and trace information in text or machine-readable artifacts.

## Design boundaries

- Do not implement production code in this skill except disposable prototypes explicitly used to resolve a design question.
- Do not change a canonical requirement silently. Return the discovered delta through `$maintain-canonical-requirements`; remain within the existing authorization boundary when the change is a derived correction, and stop only for materially new authority.
- Do not treat a Figma frame as complete when behavior, responsive rules, content states, or accessibility semantics are absent.
- Do not require pixel identity where the requirement is adaptive behavior; define what must be invariant and what may respond to context.
- Do not create a new design system for a local feature when the existing one can be extended safely.

## Implementation-readiness gates

The design is not ready when:

- a requirement has no mapped surface, flow, state, or verification;
- the primary task or information hierarchy cannot be explained without referring to decoration;
- errors, loading, empty data, permissions, or recovery are left to the implementer;
- responsive behavior is implied only by desktop and mobile pictures;
- keyboard, focus, semantic, or reduced-motion behavior is unspecified where applicable;
- new tokens or components duplicate existing primitives without rationale;
- visual direction is a list of adjectives rather than a coherent, testable set of decisions;
- critical copy remains placeholder text;
- design and test plan disagree.

## Completion

Complete when `docs/03-detailed-design.md` and `docs/03-test-plan.md` are current, every applicable requirement is traceable through design to a planned test, existing-system reuse and deviations are explicit, all consequential states and interactions are specified, and implementation can proceed without inventing product or design behavior.
