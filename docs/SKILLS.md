# Skills catalog

Copy a folder to `<target>/.agents/skills/<name>/`. `SKILL.md` metadata determines automatic triggering; users normally describe the problem without naming a skill.

| Skill | Purpose and trigger | Dependencies | Copy source |
|---|---|---|---|
| `adversarial-review` | Critically challenge requirements, design, implementation, tests, and documents under the assumption that defects may exist | Standalone | `.agents/skills/adversarial-review` |
| `author-lifecycle-docs` | Maintain request-local phase documents, canonical delta, plan, and traceability | Full governance runtime | `.agents/skills/author-lifecycle-docs` |
| `authorize-autonomous-execution` | Record the one explicit requester authorization for delta and execution plan | Full governance runtime | `.agents/skills/authorize-autonomous-execution` |
| `calibrated-collaborative-listening` | Infer and gently confirm ambiguous intent without sycophancy, patronizing, or meaning loss | Standalone | `.agents/skills/calibrated-collaborative-listening` |
| `chat-first-development` | Turn ordinary conversation into automatic setup, requirements, design, implementation, tests, PR, and CI | Development-framework skills; full runtime preferred | `.agents/skills/chat-first-development` |
| `generate-implementation-design` | Generate FastAPI sequence/OpenAPI/SQL design and CDK CloudFormation design with drift checks | Bundled PyYAML/SQLGlot dependency pin | `.agents/skills/generate-implementation-design` |
| `govern-development-request` | Orchestrate the single-authorization governed lifecycle | Full governance runtime | `.agents/skills/govern-development-request` |
| `inspect-quality-gates` | Inspect deterministic phase gates and evidence contracts | Full governance runtime | `.agents/skills/inspect-quality-gates` |
| `japanese-git-commit-gitmoji` | Produce Japanese Git commits with the repository's gitmoji convention | Standalone | `.agents/skills/japanese-git-commit-gitmoji` |
| `maintain-canonical-requirements` | Discover intent and persist atomic add/update/retire requirements outside work items | Listening skill recommended; bundled schema/script | `.agents/skills/maintain-canonical-requirements` |
| `retrospect-and-improve` | Generate retrospectives and authorized improvement proposals | Full governance runtime | `.agents/skills/retrospect-and-improve` |
| `verify-against-engineering-standards` | Verify artifacts against fresh, versioned SWEBOK/cloud official sources and evidence-based checklists | Standards registry; adversarial review recommended | `.agents/skills/verify-against-engineering-standards` |

## Collections

- Atomic requirements: `maintain-canonical-requirements` + `calibrated-collaborative-listening`.
- Implementation-derived design: `generate-implementation-design`.
- Standards validation: `verify-against-engineering-standards` + `adversarial-review`.
- Three-pillar framework: the six skills above (`development-framework`).
- Complete conversational development: three-pillar framework + `chat-first-development` (`chat-first`).
- Full governed lifecycle: all skills plus the runtime listed in [INSTALLATION.md](INSTALLATION.md).

Codex custom reviewer agents are separate under `.codex/agents`; skills remain portable and do not require those agents to function.
