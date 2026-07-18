---
name: test-frontend-experience
description: Verify a frontend experience against canonical requirements, detailed design, implementation, accessibility, usability, visual quality, responsiveness, performance, and supported environments. Use for frontend test planning and execution, UI review, accessibility audit, keyboard and screen-reader checks, visual regression, component and end-to-end tests, or release evidence. Separate automated findings from human observation, test complete tasks and states, and trace every verdict to reproducible evidence.
---

# Test Frontend Experience

Determine whether the implemented frontend enables the intended people to complete the intended work in the specified context, not merely whether it renders or passes an automated scanner.

## Required inputs and composition

- Read the original request, canonical requirements, `docs/03-detailed-design.md`, `docs/03-test-plan.md`, `docs/04-implementation-log.md`, supported-environment decisions, and the implementation under test.
- Use `$elicit-frontend-requirements` when expected outcomes, users, context, or acceptance criteria are still undefined.
- Use `$design-frontend-experience` when observed failure is caused by an absent or contradictory design contract.
- Use `$author-lifecycle-docs` to maintain `docs/05-test-report.md` and actual evidence trace.
- Use `$verify-against-engineering-standards` for versioned accessibility, platform, performance, security, and organizational guidance.
- Use `$adversarial-review` to challenge consequential Pass claims, broad N/A decisions, and tests that cover only the happy path.

Read `references/evidence-map.md` when choosing evaluation methods, maintaining this skill, or explaining what a test can and cannot prove.

## Test strategy

Select only applicable layers, but do not omit a layer merely because another layer passed:

1. **Static and build checks**: types, lint, invalid markup patterns, forbidden token or component use, bundle or build failures, and deterministic design-system rules.
2. **Unit tests**: state transitions, formatters, validation, reducers, hooks, and isolated logic where failure can be diagnosed without a browser.
3. **Component tests**: rendered semantics, accessible names, keyboard and pointer behavior, variants, content states, focus movement, and event contracts.
4. **Integration and end-to-end tests**: complete user tasks across routing, data, permissions, errors, retries, persistence, and backend boundaries.
5. **Visual and responsive evaluation**: approved visual invariants, representative content, themes, zoom, reflow, viewport pressure, and unintended layout changes.
6. **Accessibility evaluation**: automated rules plus keyboard walkthrough, focus inspection, content and heading structure, contrast, zoom and reflow, reduced motion, and assistive-technology checks appropriate to the risk and support matrix.
7. **Usability evaluation**: expert walkthrough and, when consequence warrants it, representative-participant task observation. Measure behavior separately from preference or satisfaction.
8. **Performance evaluation**: loading, responsiveness, visual stability, resource size, and degraded-network behavior against approved budgets or evidence-based thresholds.

## Workflow

1. Construct a traceable test matrix from requirements and design. Each row names:
   - requirement and design IDs;
   - user or role and task;
   - precondition, data, permission, environment, viewport, input method, and assistive technology when applicable;
   - action and expected user-visible outcome;
   - evidence method and pass threshold;
   - automated, expert-reviewed, or participant-observed classification.
2. Prioritize by user harm, business consequence, frequency, irreversibility, complexity, change surface, and uncertainty. Test the highest-risk task and failure path early.
3. Verify complete states and transitions, not screenshots alone. Cover applicable loading, empty, partial, stale, offline, validation, system error, conflict, permission, success, undo, retry, cancellation, and recovery paths.
4. Test semantics and keyboard operation from the rendered interface:
   - headings, landmarks, lists, tables, forms, labels, descriptions, and accessible names;
   - logical tab order and no keyboard trap;
   - visible and unobscured focus;
   - expected keyboard commands for composite widgets;
   - focus entry, error movement, route change, dialog close, and restoration;
   - dynamic status and error announcements when required.
5. Test visual accessibility and adaptation:
   - text and non-text contrast where applicable;
   - no information conveyed by color, position, shape, sound, or motion alone;
   - text resize, browser zoom, reflow, orientation, spacing overrides, and localization expansion according to scope;
   - target and gesture alternatives where applicable;
   - prefers-reduced-motion or equivalent behavior.
6. Run automated accessibility checks on representative pages and states, but classify their result only as “no detected violations within tool coverage” or as findings. Never convert that result alone into an accessibility Pass.
7. Evaluate visual quality against the approved design contract:
   - hierarchy, alignment, rhythm, density, typography, color roles, imagery, and motion;
   - design-token and component consistency;
   - visual regression across supported states and themes;
   - absence of clipping, overlap, unexpected scroll, layout shift, and placeholder content.
8. Evaluate usability by task. Observe whether the person can identify the next action, understand system status, prevent or recover from errors, and complete the goal. Record completion, errors, assistance, hesitation, route, time when meaningful, and comments separately.
9. Distinguish evidence:
   - behavior observed directly;
   - participant self-report;
   - automated assertion;
   - expert judgment;
   - inferred risk.
   Do not use a satisfaction score to conceal task failure or a fast completion time to conceal confusion or exclusion.
10. Verify supported environment coverage. Use the repository's declared browser, device, rendering, locale, theme, and input matrix. Do not claim universal compatibility from one Chromium viewport.
11. Record every finding with location, severity, violated requirement or decision, evidence, user impact, reproduction, proposed correction, owner, and retest method. A Fail remains in history after correction; add a separate Pass retest.
12. Repair in-scope implementation defects and rerun the affected layer plus any invalidated upstream or downstream tests. Route missing requirements or material design changes to the appropriate skill rather than adjusting expectations after seeing the result.
13. Update `docs/05-test-report.md` with executed scope, unexecuted scope and rationale, environment, versions, data, evidence links, findings, residual risks, and release recommendation.

## Accessibility verdict rules

- Automated checks are necessary feedback but have incomplete rule and state coverage.
- Component-library accessibility does not prove whole-flow accessibility.
- Conformance claims require evidence for all applicable criteria and supported content, not a sample with no detected failures.
- Assistive-technology testing should match declared support and risk; do not pretend expertise or coverage that was not available.
- Record browser and assistive-technology versions because behavior can vary.
- User testing with disabled participants complements but does not replace standards-based inspection, and inspection does not replace real-use observation.

## Usability verdict rules

- Define participants or reviewers, tasks, context, success criteria, and stopping rules before interpreting results.
- Do not coach during a measured task unless assistance is itself recorded as an outcome.
- Separate learnability, efficiency, error tolerance, comprehension, satisfaction, and visual appeal.
- Small qualitative studies can reveal severe problems but do not justify unsupported population percentages.
- Aesthetic appeal can improve perceived usability; verify task performance independently.

## Completion

Complete when every applicable requirement has a Pass, Fail, or evidence-backed N/A; critical tasks and applicable failure paths were exercised; automated and human evidence are distinguished; accessibility, usability, responsive, visual, and performance claims are no broader than executed coverage; findings have owners and retest methods; and `docs/05-test-report.md` provides reproducible evidence and an explicit residual-risk or release recommendation.
