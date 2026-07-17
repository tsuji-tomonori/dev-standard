# Skills catalog

Copy a skill folder to `<target>/.agents/skills/<name>/`. The `SKILL.md` metadata determines automatic triggering; users normally do not need to name a skill.

| Skill | Purpose and trigger | Dependencies | Copy source |
|---|---|---|---|
| `adversarial-review` | Assume mistakes may exist and critically challenge requirements, designs, code, tests, or documents with contradictions, omissions, counterexamples, and independent evidence | Standalone; can consume lifecycle evidence | `.agents/skills/adversarial-review` |
| `author-lifecycle-docs` | Create and maintain phase documents and traceability | Full governance runtime | `.agents/skills/author-lifecycle-docs` |
| `authorize-autonomous-execution` | Record the one explicit requester authorization | Full governance runtime | `.agents/skills/authorize-autonomous-execution` |
| `calibrated-collaborative-listening` | Infer and gently confirm ambiguous intent without sycophancy or meaning loss | Standalone | `.agents/skills/calibrated-collaborative-listening` |
| `chat-first-development` | Turn an ordinary development conversation into setup, requirements, implementation, tests, PR, and CI | Standalone lightweight mode; full runtime preferred | `.agents/skills/chat-first-development` |
| `govern-development-request` | Orchestrate the single-authorization governed lifecycle | Full governance runtime | `.agents/skills/govern-development-request` |
| `inspect-quality-gates` | Inspect deterministic phase gates and evidence | Full governance runtime | `.agents/skills/inspect-quality-gates` |
| `japanese-git-commit-gitmoji` | Produce Japanese Git commits using the repository's gitmoji convention | Standalone | `.agents/skills/japanese-git-commit-gitmoji` |
| `retrospect-and-improve` | Generate retrospectives and governed improvement proposals | Full governance runtime | `.agents/skills/retrospect-and-improve` |

## Collections

- Minimal conversational development: `chat-first-development`, `calibrated-collaborative-listening`, and `adversarial-review` (the `chat-first` profile).
- Critical challenge only: copy `adversarial-review` by itself.
- Full governed lifecycle: copy all skills plus the runtime listed in [INSTALLATION.md](INSTALLATION.md).
- Codex custom reviewer agents are separate and live under `.codex/agents`; they are listed in [INSTALLATION.md](INSTALLATION.md).
