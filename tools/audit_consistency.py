#!/usr/bin/env python3
"""Audit Skills, docs, traces, host adapters, and generated-design contracts."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tomllib
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
AUTO_REQUIREMENTS = {
    *(f"REQ-ASBUILT-{number:03d}" for number in range(1, 20)),
    *(f"REQ-DESIGN-{number:03d}" for number in range(1, 7)),
    "REQ-DISC-004",
    "REQ-DOCS-001",
    "REQ-QUALITY-001",
    "REQ-WORKBOOK-001",
}
QUALITY_COMMANDS = {
    "api": "FAST-016",
    "samples": "FAST-017",
    "crud-e2e": "FAST-018",
    "coverage": "FAST-019",
    "test-structure": "FAST-020",
    "implementation": "FAST-021",
    "thresholds": "FAST-022",
    "report": "FAST-023",
    "suppressions": "AUD-008",
}


def finding(check_id: str, message: str, path: str) -> dict[str, str]:
    """Create a stable audit finding."""

    return {"check_id": check_id, "severity": "blocking", "message": message, "path": path}


def load_json(path: Path) -> dict[str, Any]:
    """Read one JSON object."""

    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return value


def frontmatter_description(path: Path) -> str:
    """Read one single-line Skill description."""

    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return ""
    for line in match.group(1).splitlines():
        if line.startswith("description:"):
            return line.split(":", 1)[1].strip().strip('"')
    return ""


def audit_descriptions(findings: list[dict[str, str]], metrics: dict[str, Any]) -> None:
    """Keep Skill discovery metadata concise enough for host context budgets."""

    descriptions: dict[str, int] = {}
    for skill in sorted((ROOT / ".agents/skills").glob("*/SKILL.md")):
        description = frontmatter_description(skill)
        descriptions[skill.parent.name] = len(description)
        if len(description) > 300:
            findings.append(finding("AUD-SKILL-DESCRIPTION", "description exceeds 300 characters", skill.relative_to(ROOT).as_posix()))
    total = sum(descriptions.values())
    if total > 5000:
        findings.append(finding("AUD-SKILL-DESCRIPTION", f"description total exceeds 5000 characters: {total}", ".agents/skills"))
    metrics["skill_count"] = len(descriptions)
    metrics["skill_description_characters"] = total
    metrics["skill_description_max"] = max(descriptions.values(), default=0)


def audit_agents(findings: list[dict[str, str]]) -> None:
    """Require host-selected models and profile-aware gate instructions."""

    for path in sorted((ROOT / ".codex/agents").glob("*.toml")):
        value = tomllib.loads(path.read_text(encoding="utf-8"))
        if "model" in value:
            findings.append(finding("AUD-AGENT-MODEL", "reviewer pins a model instead of inheriting the host choice", path.relative_to(ROOT).as_posix()))
    gate = (ROOT / ".codex/agents/gate-auditor.toml").read_text(encoding="utf-8")
    for phrase in ["For direct or assured work", "For regulated work"]:
        if phrase not in gate:
            findings.append(finding("AUD-GATE-PROFILE", f"gate auditor lacks profile boundary: {phrase}", ".codex/agents/gate-auditor.toml"))


def audit_prompts(findings: list[dict[str, str]]) -> None:
    """Reject known prompt regressions that broaden authorization or gates."""

    forbidden = [
        "obtain one compact authorization",
        "every preceding gate",
        "complete the current phase documents",
        "review this session",
        "Authorize once then execute every lifecycle quality gate",
    ]
    for path in sorted((ROOT / ".agents/skills").glob("*/agents/openai.yaml")):
        text = path.read_text(encoding="utf-8")
        for phrase in forbidden:
            if phrase in text:
                findings.append(finding("AUD-PROMPT-BOUNDARY", f"prompt contains stale broad instruction: {phrase}", path.relative_to(ROOT).as_posix()))
    right_size = (ROOT / ".agents/skills/right-size-execution/SKILL.md").read_text(encoding="utf-8")
    if "同時拡張" in right_size or "一回の判断では一軸だけ" not in right_size:
        findings.append(finding("AUD-EXPANSION", "execution expansion is not constrained to one axis per decision", ".agents/skills/right-size-execution/SKILL.md"))


def trace_paths(requirement: dict[str, Any]) -> list[tuple[str, str]]:
    """Return repository paths from a requirement trace map."""

    result: list[tuple[str, str]] = []
    for kind, paths in requirement.get("traces", {}).items():
        if kind == "standards":
            continue
        for path in paths:
            result.append((kind, str(path)))
    return result


def audit_requirements(findings: list[dict[str, str]], metrics: dict[str, Any]) -> None:
    """Require every active trace and every auto-generation executor to exist."""

    document = load_json(ROOT / "spec/requirements/requirements.json")
    requirements = [item for item in document["requirements"] if item.get("status") == "active"]
    missing = 0
    by_id = {item["id"]: item for item in requirements}
    for requirement in requirements:
        for kind, path in trace_paths(requirement):
            if not (ROOT / path).exists():
                missing += 1
                findings.append(finding("AUD-TRACE", f"{requirement['id']} {kind} trace does not exist", path))
    for requirement_id in sorted(AUTO_REQUIREMENTS):
        requirement = by_id.get(requirement_id)
        if requirement is None:
            findings.append(finding("AUD-AUTO-REQUIREMENT", "declared auto-generation requirement is missing or inactive", requirement_id))
            continue
        tests = requirement.get("traces", {}).get("tests", [])
        implementations = requirement.get("traces", {}).get("implementation", [])
        if not tests or not implementations:
            findings.append(finding("AUD-AUTO-REQUIREMENT", "auto-generation requirement lacks implementation or test trace", requirement_id))
    metrics["requirement_count"] = len(requirements)
    metrics["auto_generation_requirement_count"] = len(AUTO_REQUIREMENTS)
    metrics["missing_trace_count"] = missing


def audit_host_generation(findings: list[dict[str, str]], metrics: dict[str, Any]) -> None:
    """Require deterministic Codex/Claude generation and reject tracked outputs."""

    adapters = load_json(ROOT / "distribution/host-adapters.json")
    hosts = adapters.get("hosts", {})
    if sorted(hosts) != ["claude-code", "codex"]:
        findings.append(finding("AUD-HOST-GENERATION", "host adapter inventory must contain Codex and Claude Code", "distribution/host-adapters.json"))
    workflow = (ROOT / ".github/workflows/host-assets.yml").read_text(encoding="utf-8")
    for token in ["tools/generate_host_assets.py check", "--host codex", "--host claude-code", "upload-artifact"]:
        if token not in workflow:
            findings.append(finding("AUD-HOST-GENERATION", f"host workflow missing: {token}", ".github/workflows/host-assets.yml"))
    precommit = (ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8")
    if "tools/generate_host_assets.py check" not in precommit:
        findings.append(finding("AUD-HOST-COMMIT", "pre-commit does not reject generated host assets", ".pre-commit-config.yaml"))
    generated_paths = {str(adapters["generated_root"]), ".claude/skills", ".claude/agents"}
    process = subprocess.run(["git", "ls-files", "--", *sorted(generated_paths)], cwd=ROOT, text=True, capture_output=True, check=False)
    if process.returncode or process.stdout.strip():
        findings.append(finding("AUD-HOST-COMMIT", "generated host assets are tracked or Git inspection failed", process.stdout.strip() or process.stderr.strip()))
    metrics["host_count"] = len(hosts)


def audit_portability(findings: list[dict[str, str]]) -> None:
    """Keep repository-specific branch trial details out of portable profiles."""

    manifest = load_json(ROOT / "distribution/manifest.json")
    forbidden = ["Reconciliation-Type:", "Trial-Activation:", "Issue #20", "dev → main", ".github/branch-policy.json"]
    for profile in ["default", "chat-first"]:
        for entry in manifest["profiles"][profile]:
            source = ROOT / entry["source"]
            if not source.is_file() or source.suffix != ".md":
                continue
            text = source.read_text(encoding="utf-8")
            for token in forbidden:
                if token in text:
                    findings.append(finding("AUD-PORTABILITY", f"{profile} contains repository branch trial detail: {token}", entry["source"]))


def audit_generated_design(findings: list[dict[str, str]]) -> None:
    """Require safe output ownership and executable quality contracts."""

    designflow = (ROOT / ".agents/skills/generate-implementation-design/scripts/designflow.py").read_text(encoding="utf-8")
    for token in ["validate_output_path", "validate_managed_bundle", "docs\" / \"design\" / \"generated", "ERROR_CASES.gen.json", "DB_DESIGN.gen.md", "E2E_SCENARIOS.gen.md", "TEST_EVIDENCE.gen.md", "TOOLS.gen.md"]:
        if token not in designflow:
            findings.append(finding("AUD-DESIGN-GENERATOR", f"design generator contract missing: {token}", ".agents/skills/generate-implementation-design/scripts/designflow.py"))
    qualityflow = (ROOT / ".agents/skills/generate-implementation-design/scripts/qualityflow.py").read_text(encoding="utf-8")
    tests = (ROOT / "tests/test_qualityflow.py").read_text(encoding="utf-8")
    for command, check_id in QUALITY_COMMANDS.items():
        if f'"{command}"' not in qualityflow or check_id not in qualityflow:
            findings.append(finding("AUD-QUALITY-EXECUTOR", f"quality executor missing: {check_id}/{command}", ".agents/skills/generate-implementation-design/scripts/qualityflow.py"))
        if check_id not in tests and command not in tests:
            findings.append(finding("AUD-QUALITY-FIXTURE", f"quality failure fixture missing: {check_id}/{command}", "tests/test_qualityflow.py"))


def audit_docs(findings: list[dict[str, str]], metrics: dict[str, Any]) -> None:
    """Reject known stale paths, empty placeholders, and stale audit scope."""

    for path in sorted((ROOT / ".agents/skills").glob("*/references/learned-rules.md")):
        if len(path.read_text(encoding="utf-8").splitlines()) <= 1:
            findings.append(finding("AUD-EMPTY-DOC", "empty learned-rules placeholder", path.relative_to(ROOT).as_posix()))
    stale_tokens = ["docs/COMMIT-COMMENT.md", "docs/ARTIFACTS-AND-CHECKS.md", "docs/INSTALLATION.md", "docs/GOVERNANCE.md", "docs/FLOW.md"]
    for path in sorted([ROOT / "AGENTS.md", ROOT / "README.md", *(ROOT / "docs").rglob("*.md"), *(ROOT / ".agents/skills").rglob("*.md")]):
        text = path.read_text(encoding="utf-8")
        for token in stale_tokens:
            if token in text:
                findings.append(finding("AUD-STALE-PATH", f"document references removed path: {token}", path.relative_to(ROOT).as_posix()))
    audit = (ROOT / "docs/reference/skill-evidence-audit.md").read_text(encoding="utf-8")
    if "tools/audit_consistency.py" not in audit or "2026-08-02" not in audit:
        findings.append(finding("AUD-EVIDENCE-DOC", "Skill evidence audit lacks current automated audit contract", "docs/reference/skill-evidence-audit.md"))
    metrics["document_count"] = len([path for path in ROOT.rglob("*.md") if not {".git", ".venv", ".devflow"}.intersection(path.parts)])


def audit_makefile(findings: list[dict[str, str]]) -> None:
    """Require a clean-checkout verification entrypoint."""

    text = (ROOT / "Makefile").read_text(encoding="utf-8")
    verify = next((line for line in text.splitlines() if line.startswith("verify:")), "")
    if "setup" not in verify:
        findings.append(finding("AUD-VERIFY", "make verify does not bootstrap dependencies", "Makefile"))
    if "/home/" in text or "SKILL_VALIDATOR" in text:
        findings.append(finding("AUD-VERIFY", "Makefile contains a personal absolute dependency", "Makefile"))


def metrics_inventory(metrics: dict[str, Any]) -> None:
    """Count canonical checks and Skill-level checklist rows for the audit workbook."""

    catalog = load_json(ROOT / "governance/checklist/catalog.json")
    metrics["technical_check_count"] = int(catalog["item_count"])
    check_catalog = (ROOT / "governance/checks/catalog.yaml").read_text(encoding="utf-8")
    metrics["governance_check_count"] = len(re.findall(r"^- id: ", check_catalog, re.MULTILINE))
    item_pattern = re.compile(r"^(?:[-*] |\d+\. |\|)")
    metrics["skill_item_count"] = sum(
        1
        for path in (ROOT / ".agents/skills").rglob("*.md")
        for line in path.read_text(encoding="utf-8").splitlines()
        if item_pattern.match(line) and not line.startswith("|---")
    )


def run_audit() -> dict[str, Any]:
    """Run every consistency family and return one machine-readable verdict."""

    findings: list[dict[str, str]] = []
    metrics: dict[str, Any] = {}
    audit_descriptions(findings, metrics)
    audit_agents(findings)
    audit_prompts(findings)
    audit_requirements(findings, metrics)
    audit_host_generation(findings, metrics)
    audit_portability(findings)
    audit_generated_design(findings)
    audit_docs(findings, metrics)
    audit_makefile(findings)
    metrics_inventory(metrics)
    return {
        "schema_version": 1,
        "overall": "合格" if not findings else "不合格",
        "blocking_findings": len(findings),
        "findings": findings,
        "metrics": metrics,
    }


def main() -> int:
    """Print the audit and optionally append the verdict to GitHub Actions."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--github-summary", action="store_true")
    args = parser.parse_args()
    try:
        result = run_audit()
    except (OSError, ValueError, KeyError, json.JSONDecodeError, tomllib.TOMLDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"総合判定: {result['overall']} / blocking={result['blocking_findings']}")
        for item in result["findings"]:
            print(f"FAIL {item['check_id']}: {item['path']}: {item['message']}")
        for key, value in result["metrics"].items():
            print(f"{key}: {value}")
    if args.github_summary and (target := os.environ.get("GITHUB_STEP_SUMMARY")):
        with Path(target).open("a", encoding="utf-8") as stream:
            stream.write("## Skills・文書整合性監査\n\n")
            stream.write(f"- 総合判定: {result['overall']}\n")
            stream.write(f"- blocking findings: {result['blocking_findings']}\n")
            for key, value in result["metrics"].items():
                stream.write(f"- {key}: {value}\n")
    return 0 if result["overall"] == "合格" else 1


if __name__ == "__main__":
    sys.exit(main())
