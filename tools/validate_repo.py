#!/usr/bin/env python3
"""Validate repository-local skills, agents, hooks, policy, and templates."""

from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def frontmatter(path: Path, failures: list[str]) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        fail(f"{path.relative_to(ROOT)}: YAML frontmatter missing", failures)
        return {}
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"')
    return values


def validate_skills(failures: list[str]) -> None:
    skills_root = ROOT / ".agents" / "skills"
    expected = {
        "govern-development-request",
        "author-lifecycle-docs",
        "inspect-quality-gates",
        "authorize-autonomous-execution",
        "calibrated-collaborative-listening",
        "chat-first-development",
        "retrospect-and-improve",
        "japanese-git-commit-gitmoji",
    }
    actual = {path.name for path in skills_root.iterdir() if path.is_dir() and (path / "SKILL.md").is_file()}
    for name in sorted(expected - actual):
        fail(f"missing skill: {name}", failures)
    for name in sorted(actual):
        skill = skills_root / name
        metadata = frontmatter(skill / "SKILL.md", failures)
        if metadata.get("name") != name:
            fail(f"{name}: frontmatter name does not match directory", failures)
        description = metadata.get("description", "")
        if len(description) < 40 or "TODO" in description:
            fail(f"{name}: description is incomplete", failures)
        if name != "japanese-git-commit-gitmoji":
            openai = skill / "agents" / "openai.yaml"
            if not openai.is_file():
                fail(f"{name}: agents/openai.yaml missing", failures)
            elif f"${name}" not in openai.read_text(encoding="utf-8"):
                fail(f"{name}: default_prompt must mention ${name}", failures)
        if "[TODO" in (skill / "SKILL.md").read_text(encoding="utf-8"):
            fail(f"{name}: SKILL.md contains an unresolved template TODO", failures)


def validate_agents(failures: list[str]) -> None:
    expected = {
        "requirements-reviewer",
        "architecture-reviewer",
        "security-reviewer",
        "test-reviewer",
        "operations-reviewer",
        "gate-auditor",
        "improvement-coach",
    }
    root = ROOT / ".codex" / "agents"
    actual = {path.stem for path in root.glob("*.toml")} if root.exists() else set()
    for name in sorted(expected - actual):
        fail(f"missing custom agent: {name}", failures)
    for path in sorted(root.glob("*.toml")) if root.exists() else []:
        try:
            value = tomllib.loads(path.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError as exc:
            fail(f"{path.relative_to(ROOT)}: invalid TOML: {exc}", failures)
            continue
        for key in ["name", "description", "developer_instructions"]:
            if not value.get(key):
                fail(f"{path.relative_to(ROOT)}: {key} missing", failures)
        if value.get("name") != path.stem:
            fail(f"{path.relative_to(ROOT)}: agent name must match filename", failures)
        if value.get("model") != "gpt-5.6-terra":
            fail(f"{path.relative_to(ROOT)}: custom reviewer must use gpt-5.6-terra", failures)
        if value.get("model_reasoning_effort") not in {"low", "medium", "high"}:
            fail(f"{path.relative_to(ROOT)}: reasoning effort must be explicitly cost-bounded", failures)
        if value.get("model_verbosity") != "low":
            fail(f"{path.relative_to(ROOT)}: reviewer output must use low verbosity", failures)
        if len(str(value.get("developer_instructions", ""))) > 900:
            fail(f"{path.relative_to(ROOT)}: reviewer prompt exceeds minimal prompt budget", failures)
        if "reviewer" in path.stem or path.stem == "gate-auditor":
            if value.get("sandbox_mode") != "read-only":
                fail(f"{path.relative_to(ROOT)}: reviewer must be read-only", failures)


def validate_repo(failures: list[str]) -> None:
    policy = json.loads((ROOT / "governance" / "policy.json").read_text(encoding="utf-8"))
    catalog = json.loads((ROOT / "governance" / "checklist" / "catalog.json").read_text(encoding="utf-8"))
    phases = set(policy["phase_order"])
    if policy["phase_order"][-1] != "closed":
        fail("phase_order must end with closed", failures)
    authorization = policy.get("authorization", {})
    authorization_phase = authorization.get("phase")
    authorization_role = authorization.get("role")
    if authorization_phase != "requirements" or authorization_role != "requester":
        fail("single authorization must be requirements / requester", failures)
    for phase, definition in policy["phases"].items():
        expected = [authorization_role] if phase == authorization_phase else []
        if definition.get("required_approvals") != expected:
            fail(f"{phase}: unexpected phase approvals; expected {expected}", failures)
    if "docs/01-execution-plan.md" not in policy["phases"]["requirements"]["required_docs"]:
        fail("requirements must bind docs/01-execution-plan.md", failures)
    for item in catalog["items"]:
        if item["phase"] not in phases:
            fail(f"catalog item {item['id']} has unknown phase", failures)
    ids = [item["id"] for item in catalog["items"]]
    if len(ids) != len(set(ids)) or len(ids) != catalog["item_count"]:
        fail("catalog item count or ID uniqueness mismatch", failures)
    required_templates = {Path(path).name for phase in policy["phases"].values() for path in phase["required_docs"]}
    actual_templates = {path.name for path in (ROOT / "docs" / "templates").glob("*.md")}
    for name in sorted(required_templates - actual_templates):
        fail(f"missing lifecycle template: {name}", failures)
    try:
        hooks = json.loads((ROOT / ".codex" / "hooks.json").read_text(encoding="utf-8"))
        for event in ["SessionStart", "Stop"]:
            if event not in hooks.get("hooks", {}):
                fail(f"hook event missing: {event}", failures)
    except FileNotFoundError:
        fail(".codex/hooks.json missing", failures)
    except json.JSONDecodeError as exc:
        fail(f".codex/hooks.json invalid: {exc}", failures)
    for path in ["AGENTS.md", "README.md", ".github/workflows/governance.yml"]:
        if not (ROOT / path).is_file():
            fail(f"required repository file missing: {path}", failures)
    operating_policy = ROOT / "docs" / "AI-OPERATING-POLICY.md"
    if not operating_policy.is_file():
        fail("docs/AI-OPERATING-POLICY.md missing", failures)
    else:
        text = operating_policy.read_text(encoding="utf-8")
        for term in ["gpt-5.6-terra", "gpt-5.6-luna", "validation contract", "Minimal-prompt regression checklist"]:
            if term not in text:
                fail(f"AI operating policy missing: {term}", failures)
    try:
        codex_config = tomllib.loads((ROOT / ".codex" / "config.toml").read_text(encoding="utf-8"))
        agents_config = codex_config.get("agents", {})
        if agents_config.get("max_threads", 0) > 3:
            fail("agents.max_threads must remain cost-bounded at 3 or fewer", failures)
        if agents_config.get("max_depth") != 1:
            fail("agents.max_depth must remain 1", failures)
        unexpected = sorted(key for key, value in agents_config.items() if isinstance(value, dict))
        if unexpected:
            fail(f"custom agents must be standalone .codex/agents files, not config mappings: {unexpected}", failures)
    except (FileNotFoundError, tomllib.TOMLDecodeError) as exc:
        fail(f".codex/config.toml invalid: {exc}", failures)
    try:
        manifest = json.loads((ROOT / "distribution" / "manifest.json").read_text(encoding="utf-8"))
        inventory = manifest["inventory"]
        skill_names = sorted(path.name for path in (ROOT / ".agents" / "skills").iterdir() if (path / "SKILL.md").is_file())
        agent_names = sorted(path.stem for path in (ROOT / ".codex" / "agents").glob("*.toml"))
        if sorted(inventory["skills"]) != skill_names:
            fail("distribution manifest skill inventory is stale", failures)
        if sorted(inventory["agents"]) != agent_names:
            fail("distribution manifest agent inventory is stale", failures)
        for required in ["chat-first", "communication", "commit-style", "skills", "agents", "governance", "codex-hooks", "full"]:
            if required not in manifest["profiles"]:
                fail(f"distribution manifest profile missing: {required}", failures)
        if manifest["standard_paths"].get("portable_skills") != ".agents/skills/<skill-name>/SKILL.md":
            fail("portable skill standard path is invalid", failures)
        if manifest["standard_paths"].get("codex_project_agents") != ".codex/agents/<agent-name>.toml":
            fail("Codex custom agent standard path is invalid", failures)
    except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError) as exc:
        fail(f"distribution/manifest.json invalid: {exc}", failures)
    if not (ROOT / "docs" / "INSTALLATION.md").is_file():
        fail("docs/INSTALLATION.md missing", failures)
    else:
        installation = (ROOT / "docs" / "INSTALLATION.md").read_text(encoding="utf-8")
        for term in ["copy, open, chat", "No installer command is required", "never needs to run Python"]:
            if term not in installation:
                fail(f"chat-first installation guidance missing: {term}", failures)
    validate_agents(failures)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skills-only", action="store_true")
    args = parser.parse_args()
    failures: list[str] = []
    validate_skills(failures)
    if not args.skills_only:
        validate_repo(failures)
    if failures:
        for message in failures:
            print(f"FAIL: {message}")
        return 1
    print("repository validation OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
