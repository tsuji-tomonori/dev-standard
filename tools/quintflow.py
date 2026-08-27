#!/usr/bin/env python3
"""Generate and verify dev-standard's Quint-backed requirements and Skill contracts."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
QUINT = ROOT / "node_modules" / ".bin" / "quint"
REQUIREMENTS_QNT = ROOT / "spec" / "requirements" / "requirements.qnt"
REQUIREMENTS_JSON = ROOT / "spec" / "requirements" / "requirements.json"
REQUIREMENTS_DOC = ROOT / "docs" / "requirements" / "REQUIREMENTS.md"
SKILLS_QNT = ROOT / "spec" / "skills" / "skills.qnt"
SKILLS_JSON = ROOT / "spec" / "skills" / "skills.json"
SKILLS_DOC = ROOT / "docs" / "reference" / "FORMAL-SPECIFICATIONS.md"
SKILLS_ROOT = ROOT / ".agents" / "skills"
REQUIREMENTS_TEMPLATE_QNT = (
    SKILLS_ROOT
    / "maintain-canonical-requirements"
    / "assets"
    / "requirements.template.qnt"
)
QUINT_VERSION = "0.32.0"


class QuintFlowError(RuntimeError):
    pass


def run(command: list[str], *, capture: bool = False) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=capture,
        check=False,
    )
    if result.returncode:
        output = ((result.stdout or "") + (result.stderr or "")).strip()
        raise QuintFlowError(f"command failed ({result.returncode}): {' '.join(command)}\n{output}")
    return result


def quint(*args: str, capture: bool = False) -> subprocess.CompletedProcess[str]:
    if not QUINT.is_file():
        raise QuintFlowError("Quint is not installed; run `npm ci --ignore-scripts`")
    return run([str(QUINT), *args], capture=capture)


def normalize_itf(value: Any) -> Any:
    if isinstance(value, list):
        return [normalize_itf(item) for item in value]
    if isinstance(value, dict):
        if set(value) == {"#bigint"}:
            return int(value["#bigint"])
        return {key: normalize_itf(item) for key, item in value.items()}
    return value


def extract_state(spec: Path, variable: str) -> Any:
    with tempfile.TemporaryDirectory(prefix="dev-standard-quint-") as directory:
        trace = Path(directory) / "trace.itf.json"
        quint(
            "run",
            str(spec.relative_to(ROOT)),
            "--backend=typescript",
            "--max-samples=1",
            "--max-steps=0",
            "--verbosity=0",
            f"--out-itf={trace}",
        )
        try:
            raw = json.loads(trace.read_text(encoding="utf-8"))
            return normalize_itf(raw["states"][0][variable])
        except (OSError, json.JSONDecodeError, KeyError, IndexError, TypeError) as exc:
            raise QuintFlowError(f"cannot extract {variable} from {spec}: {exc}") from exc


def requirement_to_json(item: dict[str, Any]) -> dict[str, Any]:
    criteria = [
        {
            "id": value["id"],
            "given": value["given"],
            "when": value["when_"],
            "then": value["expected"],
        }
        for value in item["acceptanceCriteria"]
    ]
    result: dict[str, Any] = {
        "id": item["id"],
        "revision": item["revision"],
        "status": item["status"],
        "type": item["kind"],
        "title": item["title"],
        "subject": item["subject"],
        "action": item["actionName"],
        "object": item["objectName"],
        "rationale": item["rationale"],
        "source_refs": item["sourceRefs"],
        "acceptance_criteria": criteria,
        "verification": item["verification"],
        "traces": item["traces"],
        "last_changed_by": item["lastChangedBy"],
    }
    optional = {
        "retirement_reason": item["retirementReason"],
        "superseded_by": item["supersededBy"],
        "scope": item["scopeName"],
        "category": item["categoryName"],
    }
    result.update({key: value for key, value in optional.items() if value != ""})
    return result


def extract_requirements() -> dict[str, Any]:
    catalog = extract_state(REQUIREMENTS_QNT, "catalog")
    requirements = sorted(
        (requirement_to_json(item) for item in catalog["requirements"]),
        key=lambda item: item["id"],
    )
    return {
        "schema_version": catalog["schemaVersion"],
        "catalog_revision": catalog["catalogRevision"],
        "product": catalog["product"],
        "updated_at": catalog["updatedAt"],
        "requirements": requirements,
    }


def extract_skills() -> dict[str, Any]:
    contracts = extract_state(SKILLS_QNT, "contracts")
    return {
        "schema_version": 1,
        "quint_version": QUINT_VERSION,
        "source": "spec/skills/skills.qnt",
        "contracts": sorted(contracts, key=lambda item: item["name"]),
        "invariants": [
            "contractsAreComplete",
            "threePillarsOnly",
            "repositoryPolicyIsHostOwned",
            "defaultProfileIsMinimal",
            "workflowOrderIsConsistent",
            "portablePolicyIsUntouched",
        ],
    }


def load_specflow() -> Any:
    path = SKILLS_ROOT / "maintain-canonical-requirements" / "scripts" / "specflow.py"
    spec = importlib.util.spec_from_file_location("dev_standard_specflow", path)
    if spec is None or spec.loader is None:
        raise QuintFlowError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def render_skills(catalog: dict[str, Any]) -> str:
    lines = [
        "<!-- tools/quintflow.pyによる自動生成。spec/skills/skills.qntを編集すること。 -->",
        "# Skills形式仕様",
        "",
        "全Skillの機械可読契約と3本柱の不変条件を、人向けに表示した派生文書です。",
        "",
        "- 正本: `spec/skills/skills.qnt`",
        f"- Quint: `{catalog['quint_version']}`",
        f"- Skill数: {len(catalog['contracts'])}",
        "",
        "| Skill | 役割 | 柱 | Guardrail | 既定配布 |",
        "|---|---|---|---|---|",
    ]
    pillar_labels = {
        "requirements": "要件正本",
        "design": "as-built設計",
        "checks": "選択check",
        "auxiliary": "補助",
    }
    for contract in catalog["contracts"]:
        lines.append(
            f"| `{contract['name']}` | {contract['role']} | "
            f"{pillar_labels[contract['pillar']]} | "
            f"{'blocking' if contract['guardrail'] else 'なし'} | "
            f"{'含む' if contract['defaultProfile'] else '含めない'} |"
        )
    lines += [
        "",
        "## 検証する不変条件",
        "",
        "- 全Skill directoryと形式契約が一対一で対応する。",
        "- blocking guardrailは要件正本、as-built設計、選択checkの3本柱だけに属する。",
        "- portable契約はCI workflow、branch rule、merge方式を要求しない。",
        "- 既定profileは入口Skillと3本柱の4 Skillだけである。",
        "- 要件、設計、checkの順序を飛び越えた完了状態へ到達しない。",
        "",
        "## 各Skillの契約",
    ]
    for contract in catalog["contracts"]:
        lines += [
            "",
            f"### {contract['name']}",
            "",
            f"- 前提: {contract['precondition']}",
            f"- 事後条件: {contract['postcondition']}",
            f"- Authority: `{contract['authority']}`",
            f"- 副作用: `{contract['sideEffect']}`",
            f"- 入力: {', '.join(f'`{value}`' for value in contract['inputs'])}",
            f"- 出力: {', '.join(f'`{value}`' for value in contract['outputs'])}",
        ]
    return "\n".join(lines) + "\n"


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f"{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def derived_outputs() -> dict[Path, str]:
    requirements = extract_requirements()
    requirements_json = canonical_json(requirements)
    requirements_view = json.loads(requirements_json)
    specflow = load_specflow()
    specflow.validate_catalog(requirements_view)
    skills = extract_skills()
    skills_json = canonical_json(skills)
    skills_view = json.loads(skills_json)
    return {
        REQUIREMENTS_JSON: requirements_json,
        REQUIREMENTS_DOC: specflow.render(requirements_view),
        SKILLS_JSON: skills_json,
        SKILLS_DOC: render_skills(skills_view),
    }


def typecheck() -> None:
    for path in [REQUIREMENTS_QNT, REQUIREMENTS_TEMPLATE_QNT, SKILLS_QNT]:
        quint("typecheck", str(path.relative_to(ROOT)))


def verify_skill_coverage(skills: dict[str, Any]) -> None:
    formalized = {item["name"] for item in skills["contracts"]}
    actual = {
        path.name
        for path in SKILLS_ROOT.iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    }
    if formalized != actual:
        raise QuintFlowError(
            "Skill formalization coverage drift: "
            f"missing={sorted(actual - formalized)} stale={sorted(formalized - actual)}"
        )
    for name in sorted(actual):
        text = (SKILLS_ROOT / name / "SKILL.md").read_text(encoding="utf-8")
        if "spec/skills/skills.qnt" not in text or f'name: "{name}"' not in text:
            raise QuintFlowError(f"{name}: SKILL.md does not trace to its Quint contract")


def generate() -> None:
    typecheck()
    outputs = derived_outputs()
    skills = json.loads(outputs[SKILLS_JSON])
    verify_skill_coverage(skills)
    for path, content in outputs.items():
        atomic_write(path, content)
        print(f"generated {path.relative_to(ROOT)}")


def check() -> None:
    typecheck()
    outputs = derived_outputs()
    verify_skill_coverage(json.loads(outputs[SKILLS_JSON]))
    drift = [
        str(path.relative_to(ROOT))
        for path, expected in outputs.items()
        if not path.is_file() or path.read_text(encoding="utf-8") != expected
    ]
    if drift:
        raise QuintFlowError(f"generated artifact drift: {', '.join(drift)}")
    print("Quint sources, derived JSON, generated docs, and Skill coverage are current")


def test() -> None:
    check()
    for path in [REQUIREMENTS_QNT, REQUIREMENTS_TEMPLATE_QNT, SKILLS_QNT]:
        quint(
            "test",
            str(path.relative_to(ROOT)),
            "--backend=typescript",
            "--max-samples=100",
            "--verbosity=1",
        )
    quint(
        "run",
        str(SKILLS_QNT.relative_to(ROOT)),
        "--backend=typescript",
        "--max-samples=500",
        "--max-steps=3",
        "--invariants",
        "formalContractsHold",
        "workflowOrderIsConsistent",
        "portablePolicyIsUntouched",
        "--verbosity=1",
    )


def verify() -> None:
    test()
    with tempfile.TemporaryDirectory(prefix="dev-standard-quint-verify-") as directory:
        output = Path(directory) / "verification.json"
        quint(
            "verify",
            str(SKILLS_QNT.relative_to(ROOT)),
            "--backend=apalache",
            "--max-steps=3",
            "--invariants",
            "formalContractsHold",
            "workflowOrderIsConsistent",
            "portablePolicyIsUntouched",
            f"--out={output}",
        )
    print("Quint bounded verification completed")


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("command", choices=["generate", "check", "test", "verify"])
    return value


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        globals()[args.command]()
        return 0
    except QuintFlowError as exc:
        print(f"ERROR: {exc}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
