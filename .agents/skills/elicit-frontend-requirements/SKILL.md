---
name: elicit-frontend-requirements
description: Discover and specify human-centred frontend UI and UX requirements with people who may not know design terminology. Use when a frontend feature, screen, flow, redesign, design system, accessibility concern, or vague request such as "make it easier to use" needs requirements. Reuse calibrated listening and canonical-requirement skills, ask only consequential novice-friendly questions, separate needs from solution preferences, and produce testable requirements before visual design or implementation.
---

# Elicit Frontend Requirements

Turn an incomplete frontend request into human-centred, testable requirements without requiring the requester to act like a designer.

## Required composition

- Use `$calibrated-collaborative-listening` for ambiguous, conflicting, emotionally charged, or incompletely expressed intent. Do not reproduce its general listening rules here.
- Use `$maintain-canonical-requirements` to persist every durable obligation as an atomic add, update, or retire operation. This skill does not create a second requirements authority.
- Use `$author-lifecycle-docs` to maintain `docs/01-requirements.md`, `docs/01-traceability.md`, and `docs/01-execution-plan.md` in a governed work item.
- Use `$verify-against-engineering-standards` when accessibility, ergonomics, platform conventions, legal obligations, or other external guidance materially affects the requirements.
- Use `$adversarial-review` before completion when a wrong requirement could exclude users, hide a critical state, or cause expensive redesign.

Read `references/evidence-map.md` when maintaining this skill, explaining its research basis, or selecting a human-factors method.

## Workflow

1. Inspect the product and repository before interviewing. Identify existing screens, navigation, terminology, design tokens, components, supported devices, accessibility conventions, analytics or research evidence, and related canonical requirement IDs. Do not ask the requester to restate facts already present.
2. State the likely outcome as a correctable hypothesis in the requester's vocabulary. Separate the user problem from an assumed UI solution.
3. Establish the context of use:
   - people and roles, including differences in expertise, ability, language, and access needs;
   - primary and secondary tasks, frequency, urgency, consequence of error, and recovery needs;
   - device, viewport, input method, environment, network, interruption, and privacy constraints;
   - information required to decide and act, including sensitive, missing, delayed, or uncertain data.
4. Ask only questions whose answers change scope, interaction, priority, accessibility, risk, or acceptance criteria. Ask one bounded question at a time by default.
5. Translate design jargon into concrete contrasts. For example, ask whether the priority is rapid comparison across many records or calm step-by-step completion; explain the trade-off and allow "either is acceptable". Do not ask the requester to choose typography scales, spacing tokens, component names, or ARIA techniques.
6. Elicit observable work rather than opinions alone. Ask what the person is trying to complete, what they need to notice, what mistakes are costly, what currently causes hesitation, and what a successful outcome looks like.
7. Use examples, sketches, existing screens, or two to three small alternative descriptions when words are insufficient. Treat reactions as evidence about goals and trade-offs, not as permission to copy an example blindly.
8. Classify every finding as one of:
   - verified fact;
   - user decision;
   - user need or task;
   - constraint;
   - preference;
   - design hypothesis;
   - unresolved consequential decision.
9. Define the frontend requirement set. Cover only applicable dimensions:
   - task and information hierarchy;
   - navigation and wayfinding;
   - data entry and validation;
   - default, loading, empty, partial, error, success, disabled, permission-denied, and recovery states;
   - responsiveness, input modalities, keyboard operation, zoom and reflow;
   - content language, terminology, localization, and help;
   - accessibility and assistive-technology expectations;
   - trust, privacy, destructive actions, confirmation, and auditability;
   - perceived and measured performance;
   - brand or visual-character constraints without prematurely fixing styling details.
10. Express usability as outcomes in a specified context, not as adjectives such as intuitive, modern, simple, or user-friendly. Define appropriate evidence such as task completion, error prevention or recovery, time or interaction limits when justified, comprehension, satisfaction, or an expert review criterion.
11. Atomize durable obligations with `$maintain-canonical-requirements`. Trace each requirement to the original request or research evidence and forward to planned design, implementation, and tests.
12. Record excluded scope, assumptions, unresolved items, and the smallest viable evaluation plan. Do not invent personas, disabilities, user counts, browser support, or business priorities as facts.

## Novice-friendly interview rules

- Begin with work, users, and consequences; visual taste comes later.
- Prefer recognition over recall: provide examples or bounded contrasts when the requester lacks vocabulary.
- Explain why a consequential question matters in one sentence.
- Accept uncertainty. Record a reversible default when the choice can safely be deferred.
- Do not present a design recommendation as something the requester previously asked for.
- Do not equate the requester's personal preference with the needs of all users.
- Do not force consensus between conflicting user groups; record the conflict and the decision owner.

## Requirement quality gates

A frontend requirement is not ready when it:

- names a solution without the user outcome or constraint that justifies it;
- uses untestable adjectives without a measurable or reviewable meaning;
- omits an applicable failure, empty, loading, permission, or recovery state;
- assumes mouse, vision, color perception, memory, language, or device capability without evidence;
- combines independent obligations in one requirement ID;
- has no trace to a user need, source, decision, or standard;
- cannot be mapped to a design decision and a verification method.

## Completion

Complete only when the requester can recognize or cheaply correct the formulation, consequential ambiguity is resolved or explicitly owned, durable obligations exist in the canonical requirement catalog, the work-item documents and trace are current, and the next design phase has a bounded problem rather than a collection of style requests.
