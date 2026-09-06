#!/usr/bin/env python3
"""Generate and verify dev-standard's Quint-backed requirements and Skill contracts."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

try:
    from .render_requirements import RequirementsRenderError, render_serialized_json
    from .render_skills import (
        interface_sha256,
        manual_body_sha256,
        payload_sha256,
        render_skill_manual,
        validate_contract_catalog,
        validate_skill_tree,
    )
    from .safe_io import (
        SafeIOError,
        atomic_batch_write_cas,
        read_bytes_nofollow,
        read_bytes_nofollow_pinned,
        snapshot_file_pinned,
        trusted_root,
    )
    from .spec_mapping import MappingError, assert_bijective_catalog
except ImportError:  # Support direct execution as ``python tools/quintflow.py``.
    from render_requirements import RequirementsRenderError, render_serialized_json
    from render_skills import (
        interface_sha256,
        manual_body_sha256,
        payload_sha256,
        render_skill_manual,
        validate_contract_catalog,
        validate_skill_tree,
    )
    from safe_io import (
        SafeIOError,
        atomic_batch_write_cas,
        read_bytes_nofollow,
        read_bytes_nofollow_pinned,
        snapshot_file_pinned,
        trusted_root,
    )
    from spec_mapping import MappingError, assert_bijective_catalog

ROOT = Path(__file__).resolve().parents[1]
QUINT = ROOT / "node_modules" / ".bin" / "quint"
REQUIREMENTS_QNT = ROOT / "spec" / "requirements" / "requirements.qnt"
REQUIREMENTS_JSON = ROOT / "spec" / "requirements" / "requirements.json"
REQUIREMENTS_DOC = ROOT / "docs" / "requirements" / "REQUIREMENTS.md"
SKILLS_QNT = ROOT / "spec" / "skills" / "skills.qnt"
SKILLS_JSON = ROOT / "spec" / "skills" / "skills.json"
SKILLS_ROOT = ROOT / ".agents" / "skills"
REQUIREMENTS_TEMPLATE_QNT = (
    SKILLS_ROOT
    / "maintain-canonical-requirements"
    / "assets"
    / "requirements.template.qnt"
)
GENERATOR_IMPLEMENTATION_INPUTS = {
    ROOT / "tools" / "quintflow.py",
    ROOT / "tools" / "render_requirements.py",
    ROOT / "tools" / "render_skills.py",
    ROOT / "tools" / "safe_io.py",
    ROOT / "tools" / "spec_mapping.py",
}
QUINT_VERSION = "0.32.0"
SKILL_TRACE_RE = re.compile(r"^\.agents/skills/([^/]+)(?:/|$)")
REQUIREMENT_INVARIANTS = ["catalogWellFormed", "lifecycleRefinesCatalog"]
SKILL_INVARIANTS = [
    "formalContractsHold",
    "workflowOrderIsConsistent",
    "portablePolicyIsUntouched",
]


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


def extract_requirements() -> dict[str, Any]:
    return assert_bijective_catalog(extract_state(REQUIREMENTS_QNT, "catalog"))


def extract_skills() -> dict[str, Any]:
    contracts = extract_state(SKILLS_QNT, "contracts")
    validate_contract_catalog(contracts)
    return {
        "schema_version": 1,
        "quint_version": QUINT_VERSION,
        "source": "spec/skills/skills.qnt",
        "contracts": sorted(contracts, key=lambda item: item["name"]),
        "invariants": [
            "contractsAreComplete",
            "threePillarsOnly",
            "repositoryPolicyIsHostOwned",
            "defaultPortableSetIsMinimal",
            "dependenciesAreClosed",
            "runnerConformanceIsExplicit",
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


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def generation_read_paths(
    output_paths: set[Path],
    requirement_traces: set[Path] | None = None,
) -> list[Path]:
    """Return every repository source consumed by ``generate`` but not updated by it."""

    inputs = {
        REQUIREMENTS_QNT,
        REQUIREMENTS_TEMPLATE_QNT,
        SKILLS_QNT,
        *GENERATOR_IMPLEMENTATION_INPUTS,
        *(requirement_traces or set()),
    }
    for path in SKILLS_ROOT.rglob("*"):
        relative = path.relative_to(SKILLS_ROOT)
        if "__pycache__" in relative.parts or path.suffix == ".pyc":
            continue
        if path.is_symlink() or path.is_file():
            inputs.add(path)
    return sorted(inputs - output_paths)


def requirement_trace_paths(catalog: dict[str, Any]) -> set[Path]:
    """Return regular-file trace inputs after structural catalog validation."""

    return {
        ROOT.joinpath(*value.split("/"))
        for requirement in catalog["requirements"]
        if requirement.get("status", "active") == "active"
        for key in ("design", "implementation", "tests")
        for value in requirement["traces"][key]
    }


def generated_output_paths() -> list[Path]:
    """Return the complete deterministic publication/check surface."""

    return [
        REQUIREMENTS_JSON,
        REQUIREMENTS_DOC,
        SKILLS_JSON,
        *sorted(SKILLS_ROOT.glob("*/SKILL.md")),
    ]


def skill_manual_outputs(catalog: dict[str, Any]) -> dict[Path, str]:
    """Verify Skill payload bindings and return generated formal manual views."""

    policy_errors = validate_skill_tree(SKILLS_ROOT)
    if policy_errors:
        raise QuintFlowError("portable Skill policy violations:\n" + "\n".join(policy_errors))

    outputs: dict[Path, str] = {}
    for contract in catalog["contracts"]:
        name = contract["name"]
        skill_root = SKILLS_ROOT / name
        manual_path = skill_root / "SKILL.md"
        try:
            manual = read_bytes_nofollow(manual_path, root=ROOT).decode("utf-8")
            actual = {
                "manualBodySha256": manual_body_sha256(manual),
                "payloadSha256": payload_sha256(contract, skill_root),
                "interfaceSha256": interface_sha256(skill_root),
            }
        except (OSError, UnicodeDecodeError, ValueError) as exc:
            raise QuintFlowError(f"{name}: cannot verify Skill content binding: {exc}") from exc
        mismatches = {
            key: {"contract": contract.get(key), "actual": value}
            for key, value in actual.items()
            if contract.get(key) != value
        }
        if mismatches:
            raise QuintFlowError(f"{name}: Skill content digest drift: {mismatches}")
        outputs[manual_path] = render_skill_manual(manual, contract)
    return outputs


def derived_outputs(
    requirements: dict[str, Any] | None = None,
    skills: dict[str, Any] | None = None,
    specflow: Any | None = None,
) -> dict[Path, str]:
    requirements = extract_requirements() if requirements is None else requirements
    requirements_json = canonical_json(requirements)
    specflow = load_specflow() if specflow is None else specflow
    specflow.validate_catalog(requirements, trace_root=ROOT)
    skills = extract_skills() if skills is None else skills
    skills_json = canonical_json(skills)
    skills_view = json.loads(skills_json)
    outputs = {
        REQUIREMENTS_JSON: requirements_json,
        REQUIREMENTS_DOC: render_serialized_json(requirements_json, specflow),
        SKILLS_JSON: skills_json,
    }
    outputs.update(skill_manual_outputs(skills_view))
    return outputs


def typecheck() -> None:
    for path in [REQUIREMENTS_QNT, REQUIREMENTS_TEMPLATE_QNT, SKILLS_QNT]:
        quint("typecheck", str(path.relative_to(ROOT)))


def verify_requirement_catalog_invariants() -> None:
    """Evaluate non-temporal catalog invariants before deriving any output."""

    for path in [REQUIREMENTS_QNT, REQUIREMENTS_TEMPLATE_QNT]:
        quint(
            "run",
            str(path.relative_to(ROOT)),
            "--backend=typescript",
            "--max-samples=1",
            "--max-steps=0",
            "--invariants",
            *REQUIREMENT_INVARIANTS,
            "--verbosity=0",
            capture=True,
        )


def _bounded_diagnostic(value: str, limit: int = 12_000) -> str:
    value = value.strip()
    if len(value) <= limit:
        return value
    half = (limit - 40) // 2
    return value[:half] + "\n... diagnostic truncated ...\n" + value[-half:]


def verify_with_apalache(spec: Path, invariants: list[str], *, max_steps: int) -> None:
    """Run bounded verification and retain failure diagnostics before cleanup."""

    if not QUINT.is_file():
        raise QuintFlowError("Quint is not installed; run `npm ci --ignore-scripts`")
    with tempfile.TemporaryDirectory(prefix="dev-standard-quint-verify-") as directory:
        output = Path(directory) / "verification.json"
        command = [
            str(QUINT),
            "verify",
            str(spec.relative_to(ROOT)),
            "--backend=apalache",
            f"--max-steps={max_steps}",
            "--invariants",
            *invariants,
            f"--out={output}",
        ]
        result = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode == 0:
            return
        diagnostics = [result.stderr, result.stdout]
        if output.is_file():
            try:
                diagnostics.append(output.read_text(encoding="utf-8", errors="replace"))
            except OSError as exc:
                diagnostics.append(f"cannot read Apalache output: {exc}")
        detail = _bounded_diagnostic("\n".join(value for value in diagnostics if value))
        if not detail:
            detail = "Apalache returned no diagnostic output"
        raise QuintFlowError(
            f"bounded verification failed ({result.returncode}): {' '.join(command)}\n{detail}"
        )


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


def verify_requirement_skill_traces(requirements: dict[str, Any], skills: dict[str, Any]) -> None:
    """Require Skill requirementIds and active requirement path traces to agree exactly."""

    active = {
        item["id"]: item
        for item in requirements["requirements"]
        if item["status"] == "active"
    }
    contracts = {contract["name"]: contract for contract in skills["contracts"]}
    declared: set[tuple[str, str]] = set()
    for name, contract in contracts.items():
        requirement_ids = contract.get("requirementIds")
        if not isinstance(requirement_ids, list) or any(not isinstance(value, str) for value in requirement_ids):
            raise QuintFlowError(f"{name}: requirementIds must be a string list")
        for requirement_id in requirement_ids:
            if requirement_id not in active:
                raise QuintFlowError(f"{name}: requirementIds contains unknown or inactive {requirement_id}")
            declared.add((name, requirement_id))

    traced: set[tuple[str, str]] = set()
    for requirement_id, requirement in active.items():
        for values in requirement["traces"].values():
            for value in values:
                match = SKILL_TRACE_RE.match(value)
                if match is None:
                    continue
                name = match.group(1)
                if name not in contracts:
                    raise QuintFlowError(f"{requirement_id}: trace refers to unknown Skill {name}")
                traced.add((name, requirement_id))

    if declared != traced:
        missing = [f"{name}:{rid}" for name, rid in sorted(traced - declared)]
        stale = [f"{name}:{rid}" for name, rid in sorted(declared - traced)]
        raise QuintFlowError(f"requirement/Skill trace drift: missing={missing} stale={stale}")


def generate() -> None:
    output_paths = generated_output_paths()
    output_set = set(output_paths)
    with trusted_root(ROOT) as root_fd:
        expected = {
            path: snapshot_file_pinned(path, root=ROOT, root_fd=root_fd)
            for path in output_paths
        }
        read_preconditions = {
            path: snapshot_file_pinned(path, root=ROOT, root_fd=root_fd)
            for path in generation_read_paths(output_set)
        }
        requirements = extract_requirements()
        skills = extract_skills()
        specflow = load_specflow()
        # Establish lexical/type validity without touching trace files, then add
        # every resolved trace to the read-only CAS preconditions before the
        # full validation reads it.
        specflow.validate_catalog(requirements, trace_root=None)
        for path in generation_read_paths(
            output_set,
            requirement_trace_paths(requirements),
        ):
            if path not in read_preconditions:
                read_preconditions[path] = snapshot_file_pinned(
                    path,
                    root=ROOT,
                    root_fd=root_fd,
                )
        typecheck()
        verify_requirement_catalog_invariants()
        outputs = derived_outputs(requirements, skills, specflow)
        verify_skill_coverage(skills)
        verify_requirement_skill_traces(requirements, skills)
        atomic_batch_write_cas(
            {path: content.encode("utf-8") for path, content in outputs.items()},
            expected,
            root=ROOT,
            lock_name=".devflow/run/quintflow-generate.lock",
            pinned_root_fd=root_fd,
            read_preconditions=read_preconditions,
        )
    for path in outputs:
        print(f"generated {path.relative_to(ROOT)}")


def check() -> None:
    output_paths = generated_output_paths()
    output_set = set(output_paths)
    with trusted_root(ROOT) as root_fd:
        read_snapshots = {
            path: snapshot_file_pinned(path, root=ROOT, root_fd=root_fd)
            for path in [*generation_read_paths(output_set), *output_paths]
        }
        requirements = extract_requirements()
        skills = extract_skills()
        specflow = load_specflow()
        specflow.validate_catalog(requirements, trace_root=None)
        for path in requirement_trace_paths(requirements):
            if path not in read_snapshots:
                read_snapshots[path] = snapshot_file_pinned(
                    path,
                    root=ROOT,
                    root_fd=root_fd,
                )
        typecheck()
        verify_requirement_catalog_invariants()
        outputs = derived_outputs(requirements, skills, specflow)
        verify_skill_coverage(skills)
        verify_requirement_skill_traces(requirements, skills)
        drift: list[str] = []
        for path, expected in outputs.items():
            try:
                actual = read_bytes_nofollow_pinned(
                    path,
                    root=ROOT,
                    root_fd=root_fd,
                )
            except (OSError, SafeIOError):
                actual = None
            if actual != expected.encode("utf-8"):
                drift.append(str(path.relative_to(ROOT)))
        changed = [
            str(path.relative_to(ROOT))
            for path, before in read_snapshots.items()
            if snapshot_file_pinned(path, root=ROOT, root_fd=root_fd) != before
        ]
    if changed:
        raise QuintFlowError(f"generation read-set changed during check: {', '.join(changed)}")
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
        *SKILL_INVARIANTS,
        "--verbosity=1",
    )


def verify() -> None:
    test()
    verify_with_apalache(REQUIREMENTS_QNT, REQUIREMENT_INVARIANTS, max_steps=4)
    verify_with_apalache(REQUIREMENTS_TEMPLATE_QNT, REQUIREMENT_INVARIANTS, max_steps=4)
    verify_with_apalache(SKILLS_QNT, SKILL_INVARIANTS, max_steps=3)
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
    except (
        MappingError,
        QuintFlowError,
        RequirementsRenderError,
        SafeIOError,
        ValueError,
    ) as exc:
        print(f"ERROR: {exc}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
