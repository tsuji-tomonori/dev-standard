#!/usr/bin/env python3
"""Validate the lightweight three-pillar reference repository contract."""

from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / ".agents" / "skills"
DEFAULT_SKILLS = {
    "chat-first-development",
    "generate-implementation-design",
    "inspect-quality-gates",
    "maintain-canonical-requirements",
}
GUARDRAILS = {
    "generate-implementation-design",
    "inspect-quality-gates",
    "maintain-canonical-requirements",
}


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def load_json(path: Path, failures: list[str]) -> dict[str, object]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"{path.relative_to(ROOT)}: {exc}", failures)
        return {}
    if not isinstance(value, dict):
        fail(f"{path.relative_to(ROOT)}: root must be an object", failures)
        return {}
    return value


def frontmatter(path: Path, failures: list[str]) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        fail(f"{path.relative_to(ROOT)}: YAML frontmatter missing", failures)
        return {}
    values: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip().strip('"')
    return values


def validate_skills(failures: list[str]) -> None:
    actual = {
        path.name
        for path in SKILLS_ROOT.iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    }
    manifest = load_json(ROOT / "distribution" / "manifest.json", failures)
    inventory = set(manifest.get("inventory", {}).get("skills", [])) if manifest else set()
    formal = load_json(ROOT / "spec" / "skills" / "skills.json", failures)
    contracts = formal.get("contracts", []) if formal else []
    formal_names = {
        item.get("name")
        for item in contracts
        if isinstance(item, dict) and isinstance(item.get("name"), str)
    }
    if actual != inventory:
        fail(f"Skill inventory drift: tree={sorted(actual)} manifest={sorted(inventory)}", failures)
    if actual != formal_names:
        fail(f"Skill formalization drift: tree={sorted(actual)} formal={sorted(formal_names)}", failures)

    for name in sorted(actual):
        skill = SKILLS_ROOT / name / "SKILL.md"
        metadata = frontmatter(skill, failures)
        if metadata.get("name") != name:
            fail(f"{name}: frontmatter name does not match directory", failures)
        if len(metadata.get("description", "")) < 40:
            fail(f"{name}: description is incomplete", failures)
        text = skill.read_text(encoding="utf-8")
        if "spec/skills/skills.qnt" not in text or f'name: "{name}"' not in text:
            fail(f"{name}: Quint trace missing", failures)
        openai = SKILLS_ROOT / name / "agents" / "openai.yaml"
        if name != "japanese-git-commit-gitmoji" and not openai.is_file():
            fail(f"{name}: agents/openai.yaml missing", failures)

    guardrails = {
        item["name"]
        for item in contracts
        if isinstance(item, dict) and item.get("guardrail") is True
    }
    defaults = {
        item["name"]
        for item in contracts
        if isinstance(item, dict) and item.get("defaultProfile") is True
    }
    if guardrails != GUARDRAILS:
        fail(f"formal guardrails must be exactly three: {sorted(guardrails)}", failures)
    if defaults != DEFAULT_SKILLS:
        fail(f"formal default profile must contain four Skills: {sorted(defaults)}", failures)
    for item in contracts:
        if not isinstance(item, dict):
            fail("Skill contract must be an object", failures)
            continue
        if item.get("requiresCi") is not False or item.get("requiresMergeRule") is not False:
            fail(f"{item.get('name')}: portable repository policy must remain host-owned", failures)


def validate_manifest(failures: list[str]) -> None:
    manifest = load_json(ROOT / "distribution" / "manifest.json", failures)
    profiles = manifest.get("profiles", {}) if manifest else {}
    if not isinstance(profiles, dict):
        fail("manifest profiles are invalid", failures)
        return
    for profile, entries in profiles.items():
        if not isinstance(entries, list):
            fail(f"{profile}: mappings must be a list", failures)
            continue
        for entry in entries:
            if not isinstance(entry, dict) or set(entry) != {"source", "destination"}:
                fail(f"{profile}: invalid mapping", failures)
                continue
            source = str(entry["source"])
            destination = str(entry["destination"])
            if not (ROOT / source).exists():
                fail(f"{profile}: missing source {source}", failures)
            normalized = f"{source}\n{destination}".lower()
            for forbidden in [".github/", "branch-policy", "governance/reviews", "required-check"]:
                if forbidden in normalized:
                    fail(f"{profile}: repository policy asset is not portable: {source}", failures)

    for profile in ["default", "chat-first"]:
        entries = profiles.get(profile, [])
        names = {
            Path(str(entry["source"])).name
            for entry in entries
            if str(entry.get("source", "")).startswith(".agents/skills/")
        }
        if names != DEFAULT_SKILLS:
            fail(f"{profile}: must contain only the entry Skill and three pillars", failures)


def validate_repo(failures: list[str]) -> None:
    validate_skills(failures)
    validate_manifest(failures)

    required = [
        "AGENTS.md",
        "README.md",
        "package.json",
        "package-lock.json",
        "spec/requirements/requirements.qnt",
        "spec/requirements/requirements.json",
        "spec/skills/skills.qnt",
        "spec/skills/skills.json",
        "docs/requirements/REQUIREMENTS.md",
        "docs/reference/FORMAL-SPECIFICATIONS.md",
        "tools/quintflow.py",
        ".github/workflows/governance.yml",
    ]
    for path in required:
        if not (ROOT / path).is_file():
            fail(f"required repository file missing: {path}", failures)
    for removed in [".github/branch-policy.json", "tools/branch_policy.py", "tests/test_branch_policy.py"]:
        if (ROOT / removed).exists():
            fail(f"retired branch enforcement remains: {removed}", failures)

    requirements = load_json(ROOT / "spec" / "requirements" / "requirements.json", failures)
    by_id = {
        item.get("id"): item
        for item in requirements.get("requirements", [])
        if isinstance(item, dict)
    }
    for retired in ["REQ-REPO-001", "REQ-REPO-002", "REQ-REPO-003"]:
        if by_id.get(retired, {}).get("status") != "retired":
            fail(f"{retired}: branch enforcement requirement must be retired", failures)
    for active in ["REQ-QUINT-001", "REQ-QUINT-002", "REQ-QUINT-003", "REQ-PORTABLE-002", "REQ-QUALITY-004"]:
        if by_id.get(active, {}).get("status") != "active":
            fail(f"{active}: new three-pillar requirement must be active", failures)

    workflow = (ROOT / ".github" / "workflows" / "governance.yml").read_text(encoding="utf-8")
    jobs = workflow.split("jobs:\n", 1)[1] if "jobs:\n" in workflow else ""
    if len(re.findall(r"^  [a-zA-Z0-9_-]+:\s*$", jobs, re.MULTILINE)) != 1:
        fail("Governance workflow must contain one job", failures)
    for required_text in ["  verify:", "python-version: \"3.12\"", "node-version: \"24\"", "make verify"]:
        if required_text not in workflow:
            fail(f"Governance workflow missing: {required_text}", failures)
    for forbidden in ["branch-policy", "needs:", "required check", "governance/reviews"]:
        if forbidden in workflow:
            fail(f"Governance workflow contains retired enforcement: {forbidden}", failures)

    root_markdown = {path.name for path in ROOT.glob("*.md")}
    if root_markdown != {"README.md", "AGENTS.md"}:
        fail(f"root Markdown layout is invalid: {sorted(root_markdown)}", failures)
    docs_list = (ROOT / "docs" / "guides" / "getting-started.md").read_text(encoding="utf-8")
    listed = set(re.findall(r"^\| `([a-z0-9-]+)` \|", docs_list, re.MULTILINE))
    actual = {path.name for path in SKILLS_ROOT.iterdir() if (path / "SKILL.md").is_file()}
    if listed != actual:
        fail("getting-started Skill inventory drift", failures)

    try:
        config = tomllib.loads((ROOT / ".codex" / "config.toml").read_text(encoding="utf-8"))
        if config.get("agents", {}).get("max_threads", 0) > 3:
            fail("agents.max_threads must remain cost-bounded", failures)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        fail(f".codex/config.toml invalid: {exc}", failures)


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--skills-only", action="store_true")
    return value


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    failures: list[str] = []
    if args.skills_only:
        validate_skills(failures)
    else:
        validate_repo(failures)
    if failures:
        for message in failures:
            print(f"ERROR: {message}")
        return 2
    print("repository contract valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
