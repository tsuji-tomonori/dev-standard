# Skills and agents installation

## Recommended: copy, open, chat

No installer command is required.

1. Copy the `.agents/skills` folder into the target repository at the same path.
2. Open the target repository with the AI development agent.
3. Describe the desired change in ordinary language. The `chat-first-development` skill detects the request and owns setup, requirements, the one initial authorization, design, implementation, tests, PR creation, and CI verification.

For the full deterministic governance flow, also copy these entries while preserving their relative paths:

- `.codex/agents` (optional read-only reviewers);
- `governance`;
- `docs/templates`;
- `tools`;
- `checklist.xlsx`;
- `requirements.txt`.

If the target has no `AGENTS.md`, copy `distribution/snippets/AGENTS.governance.md` as `AGENTS.md`. If it already has one, leave it intact: the chat-first skill will propose a delimited compatible addition in the first reviewed change. The same rule applies to `.codex/config.toml`.

The user never needs to run Python, a setup script, tests, Git, or lifecycle commands. The AI performs repository-local preparation automatically. If only the chat-first skill was copied, it uses a lightweight work record rather than stopping for missing governance files.

## Current standard paths

| Asset | Canonical source in this repository | Copy destination | Portability |
|---|---|---|---|
| Reusable skill | `.agents/skills/<name>/` | `<target>/.agents/skills/<name>/` | Open skill layout; preferred for reuse across repositories |
| Codex custom agent | `.codex/agents/<name>.toml` | `<target>/.codex/agents/<name>.toml` | Codex-specific; project-scoped and auto-discovered |
| Codex hooks | `.codex/hooks/`, `.codex/hooks.json` | same paths | Codex-specific; requires trusted project and `hooks = true` |
| Governance runtime | `governance/`, `docs/templates/`, `tools/devflow.py`, `checklist.xlsx`, `requirements.txt` | same paths | Required by the lifecycle governance skills |

Do not move repository skills to `.codex/skills`. Current Codex discovery scans repository `.agents/skills` directories. Personal skills use `$HOME/.agents/skills`; this installer intentionally does not write there. Custom agents are standalone TOML files under `.codex/agents` and do not need duplicate entries in `.codex/config.toml`.

## Choose a profile

| Profile | Use when | Copies |
|---|---|---|
| `chat-first` | Natural-language development with automatic setup is needed | chat-first orchestrator and calibrated listening skills |
| `communication` | Only calibrated listening and articulation are needed | one standalone skill |
| `commit-style` | Only Japanese gitmoji commit guidance is needed | one standalone skill |
| `skills` | All skills are wanted and dependencies will be handled separately | `.agents/skills` |
| `agents` | Read-only Codex reviewers are wanted | `.codex/agents` |
| `governance` | Full governed lifecycle is needed | all skills and reviewers, policy/catalog, workbook, templates, harness, dependency pin, `AGENTS.md` merge reference |
| `codex-hooks` | Session and retrospective hooks are wanted | hook scripts and hook declaration |
| `full` | The target should use the complete reference set | all skills, agents, hooks, governance runtime |

The machine-readable source of these mappings is [`distribution/manifest.json`](../distribution/manifest.json).

## Optional maintainer automation

The manifest-driven installer remains available for maintainers and CI. It is not part of the chat-first user workflow. The AI may invoke it internally when the reference repository is available.

Preview first; the default performs no writes:

```bash
python3 tools/install_reference.py \
  --target /absolute/path/to/target-repository \
  --profile communication \
  --profile agents
```

Apply the reviewed plan:

```bash
python3 tools/install_reference.py \
  --target /absolute/path/to/target-repository \
  --profile communication \
  --profile agents \
  --apply
```

The installer refuses differing existing files before copying anything. Use `--force` only after reviewing the dry-run and target diff. It never writes to `/`, the home directory, or a global skill location.

## Manual copy

Copy one portable skill:

```bash
mkdir -p TARGET/.agents/skills
cp -R .agents/skills/calibrated-collaborative-listening TARGET/.agents/skills/
```

Copy all Codex custom agents:

```bash
mkdir -p TARGET/.codex/agents
cp .codex/agents/*.toml TARGET/.codex/agents/
```

For hooks, also merge this setting into the target's existing `.codex/config.toml`; do not replace the entire file. The `codex-hooks` and `full` profiles install the same content as `.codex/config.reference.toml` for review:

```toml
[features]
hooks = true
```

Optional cost bounds can be merged when they fit the target workload:

```toml
[agents]
max_threads = 3
max_depth = 1
interrupt_message = true
```

## Dependency notes

- `calibrated-collaborative-listening` and `japanese-git-commit-gitmoji` are standalone.
- `govern-development-request`, `author-lifecycle-docs`, `authorize-autonomous-execution`, `inspect-quality-gates`, and `retrospect-and-improve` depend on the governance runtime. Use the `governance` profile.
- Custom reviewers expect lifecycle documents and checklist evidence when used with governance, but their TOML files can be copied independently.
- Target-specific `AGENTS.md` and `.codex/config.toml` should be merged intentionally. The installer never overwrites them. The `governance` profile writes `AGENTS.governance.reference.md`, and hook-enabled profiles write `.codex/config.reference.toml`; review and merge the applicable sections, then remove the reference copies if desired.

## Verify the target

From the target repository:

```bash
python3 tools/devflow.py catalog --check      # governance/full profile
python3 tools/devflow.py audit                # governance/full profile
```

For a standalone skill, run the current skill validator available in the Codex skill-creator workflow and confirm the skill appears after reopening or refreshing the repository.

## Update or remove

Run the installer again without `--apply` to preview drift. To update, review the diff and use `--apply --force`. Removal is intentionally manual so the installer cannot delete target-owned files or configuration.

## Official references

- [Codex skills](https://learn.chatgpt.com/docs/build-skills)
- [Codex custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Codex project configuration](https://learn.chatgpt.com/docs/config-file/config-basic)
