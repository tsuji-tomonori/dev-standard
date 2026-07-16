# Work item contract

Every `work/<ID>` contains:

- `state.json`: immutable ID/profiles plus current phase and status.
- `docs/`: lifecycle documents created from `docs/templates/`.
- `review/checklist-results.json`: every catalog item selected by profile.
- `evidence/`: safe, redacted local evidence when appropriate.
- `approvals.jsonl`: artifact-digest-bound human decisions.
- `events.jsonl`: phase and checklist event history.
- `reports/`: generated inspections.

The harness is authoritative for phase order and gate state. A work item is done only at `closed`; passing tests alone is not completion.

Profile selection rules:

- Unknown deployment platform: use `CORE`; record the platform question.
- Any public cloud: add the chosen vendor delta.
- Multiple providers: add every used provider delta and explain boundaries in architecture.
- Any AI inference, training, RAG, embedding, model evaluation, or autonomous tool use: add `AI-CONDITIONAL`.
