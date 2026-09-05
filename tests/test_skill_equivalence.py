from __future__ import annotations

import copy
import re
import unittest
from pathlib import Path
from typing import Any
from unittest import mock

import tools.quintflow as quintflow_module
from tools.quintflow import extract_skills
from tools.render_skills import (
    payload_sha256,
    render_skill_manual,
    render_skills,
    validate_contract_catalog,
    without_generated_block,
)

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / ".agents" / "skills"
SKILLS_QNT = ROOT / "spec" / "skills" / "skills.qnt"


def _dependency_cycle(contracts: list[dict[str, Any]]) -> list[str] | None:
    graph = {item["name"]: list(item["dependencies"]) for item in contracts}
    visiting: list[str] = []
    visited: set[str] = set()

    def visit(name: str) -> list[str] | None:
        if name in visiting:
            start = visiting.index(name)
            return [*visiting[start:], name]
        if name in visited:
            return None
        visiting.append(name)
        for dependency in graph[name]:
            cycle = visit(dependency)
            if cycle is not None:
                return cycle
        visiting.pop()
        visited.add(name)
        return None

    for name in graph:
        cycle = visit(name)
        if cycle is not None:
            return cycle
    return None


def _contract_source_fields(source: str) -> dict[str, list[str]]:
    catalog = source.split("pure val skillContracts: List[SkillContract] = [", 1)[1]
    catalog = catalog.split("pure val guardrailPillars", 1)[0]
    result: dict[str, list[str]] = {}
    for body in re.findall(r"(?ms)^    \{\n(.*?)^    \},$", catalog):
        names = re.findall(r'^\s+name: "([^"]+)",$', body, re.MULTILINE)
        if len(names) != 1:
            raise AssertionError("each Skill record must contain exactly one name field")
        result[names[0]] = re.findall(r"^\s{6}([A-Za-z][A-Za-z0-9]*):", body, re.MULTILINE)
    return result


class SkillEquivalenceTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contracts = {
            contract["name"]: contract for contract in extract_skills()["contracts"]
        }

    def test_all_18_manual_interface_payloads_are_bound_to_typed_contracts(self) -> None:
        skill_names = {
            path.name
            for path in SKILLS_ROOT.iterdir()
            if path.is_dir() and (path / "SKILL.md").is_file()
        }
        self.assertEqual(set(self.contracts), skill_names)
        self.assertEqual(len(skill_names), 18)
        evidence_audit = (ROOT / "docs/reference/skill-evidence-audit.md").read_text(
            encoding="utf-8"
        )
        for name, contract in self.contracts.items():
            with self.subTest(skill=name):
                manual = (SKILLS_ROOT / name / "SKILL.md").read_text(encoding="utf-8")
                body = without_generated_block(manual)
                interface = (SKILLS_ROOT / name / "agents/openai.yaml").read_text(
                    encoding="utf-8"
                )
                self.assertIn(f"name: {name}", body)
                self.assertIn(f'name: "{name}"', body)
                self.assertEqual(render_skill_manual(body, contract), manual)
                self.assertIn(contract["applicability"], manual)
                for context in contract["activationContexts"]:
                    self.assertIn(context, manual)
                self.assertIn(f"${name}", interface)
                self.assertIn(f"`{name}`", evidence_audit)
                payload_sha256(contract, SKILLS_ROOT / name)

    def test_repository_policy_and_runner_effect_flags_are_exact(self) -> None:
        policy_fields = {
            "ciWorkflow",
            "requiredCheck",
            "branchProtection",
            "ruleset",
            "mergeStrategy",
            "prTemplate",
            "commitFormat",
        }
        blockers = {
            "maintain-canonical-requirements",
            "generate-implementation-design",
            "inspect-quality-gates",
        }
        defaults = blockers | {"chat-first-development"}
        for name, contract in self.contracts.items():
            with self.subTest(skill=name):
                self.assertEqual(set(contract["repositoryPolicy"]), policy_fields)
                self.assertFalse(any(contract["repositoryPolicy"].values()))
                self.assertEqual(contract["repositoryBlocking"], name in blockers)
                self.assertEqual(contract["defaultPortable"], name in defaults)
                self.assertNotIn("direct", contract["activationContexts"])
                self.assertNotIn("assured", contract["activationContexts"])
                self.assertNotIn("regulated", contract["activationContexts"])
        self.assertEqual(
            {name for name, value in self.contracts.items() if value["externalEffect"]},
            {
                "chat-first-development",
                "inspect-quality-gates",
                "test-frontend-experience",
            },
        )
        self.assertEqual(
            set(self.contracts["chat-first-development"]["dependencies"]), blockers
        )
        for name, contract in self.contracts.items():
            if name != "chat-first-development":
                self.assertEqual(contract["dependencies"], [], name)
        self.assertEqual(
            self.contracts["govern-development-request"]["sideEffect"],
            "repository-write",
        )
        self.assertEqual(
            self.contracts["retrospect-and-improve"]["sideEffect"],
            "repository-confined-temporary-write",
        )
        self.assertEqual(
            self.contracts["verify-against-engineering-standards"]["sideEffect"],
            "repository-write",
        )

    def test_contract_collections_digests_and_dependencies_are_well_formed(self) -> None:
        list_fields = {
            "activationContexts",
            "inputs",
            "outputs",
            "obligationIds",
            "prohibitions",
            "requiredAssets",
            "dependencies",
            "requirementIds",
        }
        digest_fields = {"manualBodySha256", "payloadSha256", "interfaceSha256"}
        contracts = list(self.contracts.values())
        names = set(self.contracts)
        for contract in contracts:
            with self.subTest(skill=contract["name"]):
                for field in list_fields:
                    values = contract[field]
                    self.assertEqual(len(values), len(set(values)), field)
                for field in digest_fields:
                    self.assertRegex(contract[field], r"\A[0-9a-f]{64}\Z", field)
                self.assertLessEqual(set(contract["dependencies"]), names)
        self.assertIsNone(_dependency_cycle(contracts))

        counterexample = copy.deepcopy(contracts)
        counterexample[0]["dependencies"] = [counterexample[1]["name"]]
        counterexample[1]["dependencies"] = [counterexample[0]["name"]]
        self.assertIsNotNone(_dependency_cycle(counterexample))

    def test_quint_source_has_no_duplicate_contract_fields_or_policy_subjects(self) -> None:
        source = SKILLS_QNT.read_text(encoding="utf-8")
        expected_fields = {
            "name",
            "role",
            "pillar",
            "guardrail",
            "repositoryBlocking",
            "defaultPortable",
            "repositoryPolicy",
            "applicability",
            "activationContexts",
            "authority",
            "sideEffect",
            "externalEffect",
            "precondition",
            "postcondition",
            "inputs",
            "outputs",
            "obligationIds",
            "prohibitions",
            "requiredAssets",
            "dependencies",
            "failureState",
            "requirementIds",
            "manualBodySha256",
            "payloadSha256",
            "interfaceSha256",
        }
        records = _contract_source_fields(source)
        self.assertEqual(set(records), set(self.contracts))
        for name, fields in records.items():
            with self.subTest(skill=name):
                self.assertEqual(set(fields), expected_fields)
                self.assertEqual(len(fields), len(expected_fields))
        self.assertEqual(records["generate-implementation-design"].count("requiredAssets"), 1)

        policy_block = re.search(
            r"(?ms)pure val allowedPolicySubjects = Set\((.*?)^  \)", source
        )
        self.assertIsNotNone(policy_block)
        policy_subjects = re.findall(r'"([^"]+)"', policy_block.group(1))
        self.assertEqual(len(policy_subjects), len(set(policy_subjects)))
        self.assertEqual(policy_subjects.count("ruleset"), 1)

    def test_production_catalog_validator_rejects_structural_counterexamples(self) -> None:
        baseline = copy.deepcopy(list(self.contracts.values()))
        validate_contract_catalog(baseline)

        cases: list[tuple[str, list[dict[str, Any]], str]] = []

        missing = copy.deepcopy(baseline)
        missing[0].pop("role")
        cases.append(("missing-field", missing, "fields drift"))

        unknown_field = copy.deepcopy(baseline)
        unknown_field[0]["futureField"] = "unmapped"
        cases.append(("unknown-field", unknown_field, "fields drift"))

        wrong_type = copy.deepcopy(baseline)
        wrong_type[0]["guardrail"] = 0
        cases.append(("wrong-type", wrong_type, "must be boolean"))

        invalid_digest = copy.deepcopy(baseline)
        invalid_digest[0]["manualBodySha256"] = "A" * 64
        cases.append(("invalid-digest", invalid_digest, "64 lowercase hexadecimal"))

        duplicate_list = copy.deepcopy(baseline)
        duplicate_list[0]["outputs"].append(duplicate_list[0]["outputs"][0])
        cases.append(("duplicate-list", duplicate_list, "must contain unique values"))

        invalid_enum = copy.deepcopy(baseline)
        invalid_enum[0]["authority"] = "self-issued"
        cases.append(("invalid-enum", invalid_enum, "outside the typed enum"))

        policy_mutation = copy.deepcopy(baseline)
        policy_mutation[0]["repositoryPolicy"]["ruleset"] = True
        cases.append(("policy-mutation", policy_mutation, "must remain host-owned"))

        missing_skill = copy.deepcopy(baseline[:-1])
        cases.append(("missing-skill", missing_skill, "expected 18 Skills"))

        unknown_dependency = copy.deepcopy(baseline)
        unknown_dependency[0]["dependencies"] = ["missing-skill"]
        cases.append(("unknown-dependency", unknown_dependency, "unknown Skills"))

        self_dependency = copy.deepcopy(baseline)
        self_dependency[0]["dependencies"] = [self_dependency[0]["name"]]
        cases.append(("self-dependency", self_dependency, "must not depend on itself"))

        cyclic = copy.deepcopy(baseline)
        cyclic[0]["dependencies"] = [cyclic[1]["name"]]
        cyclic[1]["dependencies"] = [cyclic[0]["name"]]
        cases.append(("dependency-cycle", cyclic, "contain a cycle"))

        extra_blocker = copy.deepcopy(baseline)
        extra_blocker[0]["pillar"] = "requirements"
        extra_blocker[0]["guardrail"] = True
        extra_blocker[0]["repositoryBlocking"] = True
        cases.append(("extra-blocker", extra_blocker, "only the three named pillars"))

        for label, contracts, error in cases:
            with self.subTest(counterexample=label):
                with self.assertRaisesRegex(ValueError, error):
                    validate_contract_catalog(contracts)

        with self.assertRaisesRegex(ValueError, "64 lowercase hexadecimal"):
            render_skills({"quint_version": "0.32.0", "contracts": invalid_digest})
        with mock.patch.object(
            quintflow_module,
            "extract_state",
            return_value=invalid_digest,
        ):
            with self.assertRaisesRegex(ValueError, "64 lowercase hexadecimal"):
                quintflow_module.extract_skills()

    def test_reviewed_semantic_repairs_are_present_in_manual_and_contract(self) -> None:
        cases = {
            "adversarial-review": ["no finding", "no-finding"],
            "authorize-autonomous-execution": [
                "承認主体または対象組織が事前に所有する",
                "自己発行",
            ],
            "chat-first-development": ["PRの作成・更新・comment・review・merge", "明示"],
            "generate-implementation-design": [
                "applicable_requirement_ids",
                "未知ID",
                "余剰mapping",
                "unsupported_surface",
                "fail-closed",
            ],
            "govern-development-request": [
                "concrete duty",
                "init → authorize → verify → close",
                "strict prefix replay",
                "target-owned authority evidence JSON",
                "自己発行",
            ],
            "implement-frontend-experience": ["宣言済みgeneratorが変更artifactを扱うのに"],
            "inspect-quality-gates": [
                "対象repositoryが既に所有するcommand registry",
                "target-declared-external",
                "no_applicable_reason",
                "process_effect_isolation_provided",
            ],
            "japanese-git-commit-gitmoji": ["利用者または対象repository"],
            "maintain-canonical-requirements": ["未実装の下流artifactは捏造せず", "将来path"],
            "retrospect-and-improve": ["escaped defect", "lighter alternative", "auto_apply: false"],
            "test-frontend-experience": ["変更、受入条件、riskに該当する層だけ"],
            "verify-against-engineering-standards": [
                "assets/standards.registry.json",
                "repository外pathを拒否",
            ],
        }
        for name, markers in cases.items():
            body = without_generated_block(
                (SKILLS_ROOT / name / "SKILL.md").read_text(encoding="utf-8")
            )
            if name == "inspect-quality-gates":
                body += (SKILLS_ROOT / name / "references/runner-contract.md").read_text(encoding="utf-8")
            for marker in markers:
                with self.subTest(skill=name, marker=marker):
                    self.assertIn(marker, body)
        self.assertEqual(
            self.contracts["retrospect-and-improve"]["requirementIds"], []
        )
        self.assertIn(
            "explicit-user-or-target-repository-style",
            self.contracts["japanese-git-commit-gitmoji"]["authority"],
        )


if __name__ == "__main__":
    unittest.main()
