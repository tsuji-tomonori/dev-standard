# Skills catalog

Copy a skill folder to `<target>/.agents/skills/<name>/`. The `SKILL.md` metadata determines automatic triggering; users normally do not need to name a skill.

| Skill | Purpose and trigger | Dependencies | Copy source |
|---|---|---|---|
| `adversarial-validation` | Falsify requirements, designs, code, tests, mitigations, and AI/agent behavior; use for red teaming, robustness, high-risk release, or independent challenge | Standalone; can consume lifecycle evidence | `.agents/skills/adversarial-validation` |
| `author-lifecycle-docs` | Create and maintain phase documents and traceability | Full governance runtime | `.agents/skills/author-lifecycle-docs` |
| `authorize-autonomous-execution` | Record the one explicit requester authorization | Full governance runtime | `.agents/skills/authorize-autonomous-execution` |
| `calibrated-collaborative-listening` | Infer and gently confirm ambiguous intent without sycophancy or meaning loss | Standalone | `.agents/skills/calibrated-collaborative-listening` |
| `chat-first-development` | Turn an ordinary development conversation into setup, requirements, implementation, tests, PR, and CI | Standalone lightweight mode; full runtime preferred | `.agents/skills/chat-first-development` |
| `govern-development-request` | Orchestrate the single-authorization governed lifecycle | Full governance runtime | `.agents/skills/govern-development-request` |
| `inspect-quality-gates` | Inspect deterministic phase gates and evidence | Full governance runtime | `.agents/skills/inspect-quality-gates` |
| `japanese-git-commit-gitmoji` | Produce Japanese Git commits using the repository's gitmoji convention | Standalone | `.agents/skills/japanese-git-commit-gitmoji` |
| `retrospect-and-improve` | Generate retrospectives and governed improvement proposals | Full governance runtime | `.agents/skills/retrospect-and-improve` |

## Collections

- Minimal conversational development: `chat-first-development`, `calibrated-collaborative-listening`, and `adversarial-validation` (the `chat-first` profile).
- Defensive challenge only: copy `adversarial-validation` by itself.
- Full governed lifecycle: copy all skills plus the runtime listed in [INSTALLATION.md](INSTALLATION.md).
- Codex custom reviewer agents are separate and live under `.codex/agents`; they are listed in [INSTALLATION.md](INSTALLATION.md).
