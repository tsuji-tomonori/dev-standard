# Skills and agents installation

## Recommended: copy, open, chat

No installer command is required.

1. Copy `.agents/skills` into the target repository at the same path.
2. Open the target repository with the AI development agent.
3. Describe the desired outcome in ordinary language.

The user never needs to run Python, an installer, setup, tests, Git, or lifecycle commands. The AI inspects the target, creates repository-local prerequisites, bootstraps the target's canonical requirements and standards registry, and owns internal commands.

Copying skills does not copy this reference repository's product requirements. On first use, `$maintain-canonical-requirements` creates the target-specific `spec/requirements/requirements.json` from its bundled empty template. It generates `docs/requirements/REQUIREMENTS.md`; `$verify-against-engineering-standards` similarly bootstraps `governance/standards/registry.json` from its bundled official-source registry.

For the full deterministic governance flow, also copy these entries while preserving relative paths:

- `.codex/agents` for optional read-only reviewers;
- `governance` for policy, checklist, and standards registry;
- `docs/templates`;
- `tools`;
- `checklist.xlsx`;
- `requirements.txt`.

If the target has no `AGENTS.md`, copy `distribution/snippets/AGENTS.governance.md` as `AGENTS.md`. If it already has one, leave it intact; the agent adds only a clearly delimited compatible section as part of the reviewed change. Apply the same preservation rule to `.codex/config.toml`.

## Current standard paths

| Asset | Reference source | Target | Rule |
|---|---|---|---|
| Reusable skill | `.agents/skills/<name>/` | `<target>/.agents/skills/<name>/` | current repository-scoped portable layout |
| Durable requirements | skill template | `<target>/spec/requirements/requirements.json` | target-specific, generated at first intake |
| Generated requirements | canonical catalog | `<target>/docs/requirements/REQUIREMENTS.md` | never edit directly |
| Generated implementation design | source/OpenAPI/SQL/CFn | `<target>/docs/design/generated/` | source digest and drift checked |
| Standards registry | skill asset or governance profile | `<target>/governance/standards/registry.json` | official source, version, check date, refresh interval |
| Codex custom agent | `.codex/agents/<name>.toml` | same path | optional project-scoped reviewer |
| Codex hooks | `.codex/hooks/`, `.codex/hooks.json` | same paths | optional trusted-project integration |

Repository skills belong in `.agents/skills`, not `.codex/skills`. Personal skills may use `$HOME/.agents/skills`, but this collection deliberately makes no global writes.

## Choose a copy profile

| Profile | Use when | Copies |
|---|---|---|
| `requirements` | Conversation, articulation, atomic durable requirements | canonical-requirements and calibrated-listening skills |
| `implementation-design` | FastAPI/CDK implementation-derived design | detailed-design generator skill |
| `standards-verification` | SWEBOK/cloud best-practice checks | standards and adversarial-review skills |
| `development-framework` | All three guarantees are needed | the five supporting skills above |
| `chat-first` | Ordinary conversation should orchestrate the complete flow | development framework plus chat-first orchestrator |
| `adversarial-review` | A standalone critical correctness review is needed | adversarial-review skill |
| `communication` | Only calibrated listening is needed | calibrated-listening skill |
| `commit-style` | Only Japanese gitmoji commits are needed | commit style skill |
| `skills` | Every portable skill is wanted | `.agents/skills` |
| `agents` | Read-only Codex reviewers are wanted | `.codex/agents` |
| `governance` | Deterministic phases, checks, authorization, and audit are needed | skills, agents, runtime, templates, dependency pin, merge reference |
| `codex-hooks` | Lifecycle hooks are wanted | hook scripts and declaration |
| `full` | The complete reference set is wanted | all skills, agents, hooks, and governance runtime |

Mappings are defined once in [`distribution/manifest.json`](../distribution/manifest.json).

## Dependencies and automatic bootstrap

- Listening, canonical requirements, adversarial review, and standards registry validation use the Python standard library or natural-language instructions.
- Implementation design pins PyYAML and SQLGlot in its own `requirements.txt`. The agent prepares them in a repository-local environment only when the generator is used.
- Governance skills additionally use `tools/devflow.py`, `checklist.xlsx`, and root `requirements.txt`.
- If only skill folders are present, chat-first uses a lightweight `work/<id>` record but still maintains the durable catalog outside `work/`.

Missing automation is an agent setup task, not a user question. Setup must not overwrite target-owned files, weaken checks, deploy production, merge a PR, or write global configuration without explicit authority.

## Optional maintainer installer

The manifest-driven installer is available for maintainers and CI; it is not part of the user workflow. Preview is the default and performs no writes:

```bash
python3 tools/install_reference.py \
  --target /absolute/path/to/target-repository \
  --profile development-framework
```

Apply a reviewed plan:

```bash
python3 tools/install_reference.py \
  --target /absolute/path/to/target-repository \
  --profile development-framework \
  --apply
```

The installer refuses differing existing files before any write. `--force` is only for a separately reviewed replacement. It never targets `/`, the home directory, or a global skill location.

## Update and removal

Copy or run the installer again to compare a newer collection. Requirements updates occur through revision-checked add/update/retire deltas, not by replacing the catalog. Remove copied skills manually so automation cannot delete target-owned files. Retire a durable requirement instead of erasing its history.

## Official layout references

- [Codex skills](https://learn.chatgpt.com/docs/build-skills)
- [Codex custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Codex project configuration](https://learn.chatgpt.com/docs/config-file/config-basic)
