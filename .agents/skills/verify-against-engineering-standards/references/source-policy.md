# Standards source policy

- Prefer the issuing body's official page. Secondary summaries cannot establish the current version.
- The registry pins `version`, `url`, `checked_at`, and `refresh_days`. This makes a review reproducible while forcing periodic revalidation.
- A changed official page does not automatically rewrite requirements or checklist rules. Open a governed delta, describe the source change, affected checks, migration impact, and evidence.
- SWEBOK supplies software-engineering lifecycle knowledge areas. Vendor Well-Architected frameworks supply workload-specific cloud practices. They complement rather than replace product requirements.
- Cloud frameworks evolve continuously. Google explicitly describes continuous updates; therefore passing a historical checklist without a freshness check must not be reported as current best-practice compliance.

Primary entry points are maintained in `assets/standards.registry.json` and generated into `docs/standards/SOURCES.md`.
