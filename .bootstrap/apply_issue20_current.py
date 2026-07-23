from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
OURS = Path("/tmp/issue20-ours")


def run(*args: str) -> str:
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False)
    if result.returncode:
        print(result.stdout, end="")
        print(result.stderr, end="", file=sys.stderr)
        raise SystemExit(f"command failed ({result.returncode}): {' '.join(args)}")
    return result.stdout


def copy_uncontested_files() -> None:
    print("phase: copy uncontested payload files")
    skip = {
        Path(".agents/skills/maintain-canonical-requirements/assets/requirements.schema.json"),
        Path(".github/workflows/governance.yml"),
        Path("README.md"),
        Path("docs/reference/development.md"),
        Path("docs/requirements/REQUIREMENTS.md"),
        Path("spec/requirements/requirements.json"),
        Path("tests/test_specflow.py"),
    }
    for source in sorted(path for path in OURS.rglob("*") if path.is_file()):
        relative = source.relative_to(OURS)
        if relative in skip:
            continue
        target = ROOT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def merge_readme() -> None:
    print("phase: merge README document links")
    path = ROOT / "README.md"
    text = path.read_text(encoding="utf-8")
    canonical = "- [正本要件と解決手段の境界設計](docs/reference/canonical-requirements.md)\n"
    branch = "- [二層branch履歴の管理された試行](docs/decisions/ADR-0002-two-layer-branch-history.md)\n"
    if branch not in text:
        if canonical not in text:
            raise SystemExit("canonical requirements link anchor is missing")
        text = text.replace(canonical, canonical + branch, 1)
    path.write_text(text, encoding="utf-8")


def merge_development() -> None:
    print("phase: merge development contract sections")
    path = ROOT / "docs/reference/development.md"
    current = path.read_text(encoding="utf-8")
    ours = (OURS / "docs/reference/development.md").read_text(encoding="utf-8")
    start = "\n## branchとrelease transaction\n"
    end = "\n## Review結果\n"
    if start not in ours or end not in ours:
        raise SystemExit("branch transaction section is missing from payload")
    section = start + ours.split(start, 1)[1].split(end, 1)[0]
    if start not in current:
        if current.count(end) != 1:
            raise SystemExit("development Review section anchor is missing")
        current = current.replace(end, section + end, 1)
    path.write_text(current, encoding="utf-8")


def merge_governance() -> None:
    print("phase: preserve current pre-commit gates in Governance")
    text = (OURS / ".github/workflows/governance.yml").read_text(encoding="utf-8")
    needle = "      - run: pip install -r requirements.txt\n"
    insertion = (
        needle
        + "      - name: Validate pre-commit configuration\n"
        + "        run: pre-commit validate-config\n"
        + "      - name: Run pre-commit checks\n"
        + "        run: pre-commit run --all-files --show-diff-on-failure\n"
    )
    if text.count(needle) != 1:
        raise SystemExit("unexpected Governance dependency-install step count")
    (ROOT / ".github/workflows/governance.yml").write_text(
        text.replace(needle, insertion, 1), encoding="utf-8"
    )


def merge_requirements() -> None:
    print("phase: merge canonical requirements by ID")
    target = ROOT / "spec/requirements/requirements.json"
    current = json.loads(target.read_text(encoding="utf-8"))
    ours = json.loads(
        (OURS / "spec/requirements/requirements.json").read_text(encoding="utf-8")
    )
    required_ids = {"REQ-REPO-001", "REQ-REPO-002", "REQ-REPO-003"}
    additions = [item for item in ours["requirements"] if item["id"] in required_ids]
    if {item["id"] for item in additions} != required_ids:
        raise SystemExit("Issue 20 requirements are incomplete")
    by_id = {item["id"]: item for item in current["requirements"]}
    for item in additions:
        existing = by_id.get(item["id"])
        if existing is not None and existing != item:
            raise SystemExit(f"conflicting requirement: {item['id']}")
        by_id[item["id"]] = item
    current["catalog_revision"] = int(current["catalog_revision"]) + 1
    current["updated_at"] = "2026-07-24"
    current["requirements"] = sorted(by_id.values(), key=lambda item: item["id"])
    target.write_text(
        json.dumps(current, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def merge_specflow_tests() -> None:
    print("phase: merge specflow regression assertions")
    path = ROOT / "tests/test_specflow.py"
    text = path.read_text(encoding="utf-8")
    old = '        self.assertEqual(len(catalog["requirements"]), 49)\n'
    if text.count(old) != 1:
        raise SystemExit("unexpected current requirement-count assertion")
    text = text.replace(
        old, '        self.assertEqual(len(catalog["requirements"]), 52)\n', 1
    )
    anchor = '        self.assertIn("issue:25", solution_requirement["source_refs"])\n'
    insertion = anchor + '''\n        branch_requirement = next(\n            item for item in catalog["requirements"] if item["id"] == "REQ-REPO-001"\n        )\n        self.assertEqual(branch_requirement["scope"], "project")\n        self.assertEqual(branch_requirement["category"], "nonfunctional")\n        self.assertEqual(branch_requirement["source_refs"], ["issue:20"])\n'''
    if text.count(anchor) != 1:
        raise SystemExit("solution-neutral requirement assertion anchor is missing")
    path.write_text(text.replace(anchor, insertion, 1), encoding="utf-8")


def validate_changed_paths() -> None:
    print("phase: validate exact changed-file scope")
    expected = {
        ".github/PULL_REQUEST_TEMPLATE.md",
        ".github/branch-policy.json",
        ".github/workflows/governance.yml",
        "AGENTS.md",
        "README.md",
        "docs/README.md",
        "docs/decisions/ADR-0002-two-layer-branch-history.md",
        "docs/reference/commit-message.md",
        "docs/reference/development.md",
        "docs/requirements/REQUIREMENTS.md",
        "governance/reviews/CHG-20260724-two-layer-branch-trial.yaml",
        "governance/reviews/README.md",
        "governance/reviews/validate.py",
        "spec/requirements/requirements.json",
        "tests/test_branch_policy.py",
        "tests/test_reference_repository_contract.py",
        "tests/test_review_contract.py",
        "tests/test_specflow.py",
        "tools/branch_policy.py",
        "tools/validate_repo.py",
    }
    actual = set(run("git", "diff", "--cached", "--name-only").splitlines())
    if actual != expected:
        print("missing:", sorted(expected - actual), file=sys.stderr)
        print("unexpected:", sorted(actual - expected), file=sys.stderr)
        raise SystemExit("changed-file scope mismatch")
    run("git", "diff", "--cached", "--check")


def main() -> None:
    copy_uncontested_files()
    merge_readme()
    merge_development()
    merge_governance()
    merge_requirements()
    merge_specflow_tests()
    print("phase: regenerate requirements view")
    run(
        sys.executable,
        ".agents/skills/maintain-canonical-requirements/scripts/specflow.py",
        "generate",
    )
    run("git", "add", "-A")
    validate_changed_paths()
    print("Issue 20 payload rebased onto current main")


if __name__ == "__main__":
    main()
