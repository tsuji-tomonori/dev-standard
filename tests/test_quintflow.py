from __future__ import annotations

import copy
import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from tools.quintflow import (
    REQUIREMENTS_TEMPLATE_QNT,
    QuintFlowError,
    extract_requirements,
    extract_skills,
    extract_state,
    verify_requirement_skill_traces,
)
from tools.render_requirements import RequirementsRenderError, render_serialized_json
from tools.render_skills import (
    GENERATED_BLOCK_END,
    GENERATED_BLOCK_START,
    REPOSITORY_POLICY_FIELDS,
    manual_body_sha256,
    payload_sha256,
    render_skill_block,
    render_skills,
    validate_manual_host_paths,
    validate_manual_policy,
    validate_policy_tree,
    validate_skill_tree,
    validate_structured_policy,
    without_generated_block,
)
from tools.spec_mapping import MappingError, catalog_to_json
from tools.validate_repo import validate_manifest_document

ROOT = Path(__file__).resolve().parents[1]


def load_specflow():
    path = ROOT / ".agents/skills/maintain-canonical-requirements/scripts/specflow.py"
    spec = importlib.util.spec_from_file_location("quintflow_test_specflow", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class QuintFlowContractTest(unittest.TestCase):
    def test_requirement_ids_and_skill_path_traces_are_bidirectional(self) -> None:
        requirements = {
            "requirements": [
                {
                    "id": "REQ-GOLDEN-001",
                    "status": "active",
                    "traces": {
                        "design": [".agents/skills/golden-skill/SKILL.md"],
                        "implementation": [],
                        "tests": [],
                        "standards": [],
                    },
                },
                {
                    "id": "REQ-RETIRED-001",
                    "status": "retired",
                    "traces": {
                        "design": [".agents/skills/golden-skill/SKILL.md"],
                        "implementation": [],
                        "tests": [],
                        "standards": [],
                    },
                },
            ]
        }
        skills = {"contracts": [{"name": "golden-skill", "requirementIds": ["REQ-GOLDEN-001"]}]}
        verify_requirement_skill_traces(requirements, skills)

        skills["contracts"][0]["requirementIds"] = []
        with self.assertRaises(QuintFlowError):
            verify_requirement_skill_traces(requirements, skills)
        skills["contracts"][0]["requirementIds"] = ["REQ-RETIRED-001"]
        with self.assertRaises(QuintFlowError):
            verify_requirement_skill_traces(requirements, skills)

    def test_skill_contract_golden_renders_every_semantic_and_digest_field(self) -> None:
        contract = {
            "name": "golden-skill",
            "role": "golden-role",
            "pillar": "auxiliary",
            "guardrail": False,
            "repositoryBlocking": False,
            "defaultPortable": False,
            "repositoryPolicy": {
                "ciWorkflow": False,
                "requiredCheck": False,
                "branchProtection": False,
                "ruleset": False,
                "mergeStrategy": False,
                "prTemplate": False,
                "commitFormat": False,
            },
            "applicability": "when-explicitly-requested",
            "activationContexts": ["explicit-review-request"],
            "authority": "artifact-authority",
            "sideEffect": "none",
            "externalEffect": False,
            "failureState": "report-bounded",
            "precondition": "golden precondition",
            "postcondition": "golden postcondition",
            "inputs": ["golden-input"],
            "outputs": ["golden-output"],
            "obligationIds": ["golden-obligation"],
            "prohibitions": ["do not invent golden evidence"],
            "requiredAssets": ["references/golden.md"],
            "dependencies": ["golden-dependency"],
            "requirementIds": ["REQ-GOLDEN-001"],
            "manualBodySha256": "1" * 64,
            "payloadSha256": "2" * 64,
            "interfaceSha256": "3" * 64,
        }
        rendered = render_skill_block(contract)
        for expected in [
            GENERATED_BLOCK_START,
            GENERATED_BLOCK_END,
            "golden-role",
            "artifact-authority",
            "report-bounded",
            "golden-input",
            "golden-output",
            "golden-obligation",
            "do not invent golden evidence",
            "references/golden.md",
            "golden-dependency",
            "when-explicitly-requested",
            "explicit-review-request",
            "REQ-GOLDEN-001",
            "1" * 64,
            "2" * 64,
            "3" * 64,
        ]:
            self.assertIn(expected, rendered)
        for field in REPOSITORY_POLICY_FIELDS:
            self.assertIn(f"repository policy `{field}`: false", rendered)
        self.assertIn("外部作用capability: no", rendered)
        self.assertNotIn("適用profile", rendered)

        aggregate = render_skills(extract_skills())
        self.assertIn("起動context: `explicit-review-request`", aggregate)
        self.assertIn("Repository policy: `ciWorkflow=false`", aggregate)
        self.assertIn("falseは未モデル化の外部作用", aggregate)
        self.assertNotIn("適用profile", aggregate)

        malformed = dict(contract)
        malformed["repositoryPolicy"] = {"ciWorkflow": False}
        with self.assertRaises(ValueError):
            render_skill_block(malformed)
        malformed = dict(contract)
        malformed["repositoryPolicy"] = {
            **contract["repositoryPolicy"],
            "requiredCheck": "false",
        }
        with self.assertRaises(ValueError):
            render_skill_block(malformed)

    def test_manual_digest_excludes_generated_block_without_host_path_collisions(self) -> None:
        canonical = "# Skill\n\nUse `<host-skill-path>/scripts/example.py`.\n"
        hosted = "# Skill\r\n\r\nUse `<host-skill-path>/scripts/example.py`.\r\n"
        generated = (
            hosted.rstrip("\r\n")
            + "\r\n\r\n"
            + GENERATED_BLOCK_START
            + "\r\nstale generated data\r\n"
            + GENERATED_BLOCK_END
            + "\r\n"
        )
        self.assertEqual(without_generated_block(generated), hosted.replace("\r\n", "\n"))
        self.assertEqual(manual_body_sha256(generated), manual_body_sha256(canonical))
        agents_literal = canonical.replace("<host-skill-path>", ".agents/skills/example")
        claude_literal = canonical.replace("<host-skill-path>", ".claude/skills/example")
        self.assertNotEqual(
            manual_body_sha256(agents_literal),
            manual_body_sha256(claude_literal),
        )
        self.assertTrue(validate_manual_host_paths(agents_literal))
        self.assertTrue(validate_manual_host_paths(claude_literal))
        self.assertEqual(validate_manual_host_paths(canonical), [])
        with self.assertRaises(ValueError):
            without_generated_block(f"manual\n{GENERATED_BLOCK_START}\nmissing end\n")

    def test_payload_digest_is_order_independent_and_rejects_symlink_escape(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "skill"
            (root / "references").mkdir(parents=True)
            (root / "references/a.md").write_text("alpha\n", encoding="utf-8")
            (root / "references/b.md").write_text("beta\n", encoding="utf-8")
            first = {"name": "fixture", "requiredAssets": ["references/b.md", "references/a.md"]}
            second = {"name": "fixture", "requiredAssets": ["references/a.md", "references/b.md"]}
            self.assertEqual(payload_sha256(first, root), payload_sha256(second, root))
            with self.assertRaises(ValueError):
                payload_sha256(
                    {"name": "fixture", "requiredAssets": ["references/a.md"]},
                    root,
                )

            (root / "references/undeclared.md").write_text("undeclared\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                payload_sha256(first, root)
            (root / "references/undeclared.md").unlink()

            outside = Path(directory) / "outside.md"
            outside.write_text("outside\n", encoding="utf-8")
            os.symlink(outside, root / "references/escape.md")
            with self.assertRaises(ValueError):
                payload_sha256({"name": "fixture", "requiredAssets": ["references/escape.md"]}, root)

    def test_manual_policy_scanner_rejects_forcing_but_accepts_host_owned_boundaries(self) -> None:
        rejected = [
            "CI must be enabled for every adopter.",
            "Run CI before every merge.",
            "Use squash merge for all pull requests.",
            "Require a merge queue before completion.",
            "Branch protection is mandatory.",
            "The commit message format is required.",
            "Do not add CI and require a merge queue.",
            "The user selected this Skill, then require review approvals.",
            "CI must not be disabled.",
            "CIを必須にする。",
            "branch protectionを設定する。",
        ]
        for text in rejected:
            with self.subTest(text=text):
                self.assertTrue(validate_manual_policy(text, "fixture.md"))

        accepted = [
            "Do not add CI or require a merge rule.",
            "Do not run CI or use squash merge as a portable prerequisite.",
            "The target repository's existing CI may provide additional evidence.",
            "Run CI when the target repository explicitly selects it.",
            "Use squash merge when the target repository explicitly selects it.",
            "Use this commit style when the user explicitly selects it.",
            "利用者がmergeを依頼した場合だけ、対象repositoryが既に定める規則に従う。",
            "CI workflow、required check、branch protection、merge ruleを追加も変更もしない。",
        ]
        for text in accepted:
            with self.subTest(text=text):
                self.assertEqual(validate_manual_policy(text, "fixture.md"), [])

    def test_json_policy_scanner_covers_nested_keys_and_ci_only_verification(self) -> None:
        rejected = [
            '{"requires_ci": true}',
            '{"repositoryPolicy": {"ciWorkflow": true}}',
            '{"repositoryPolicy": {"prTemplate": "required.md"}}',
            '{"repositoryPolicy.mergeStrategy": "squash"}',
            '{"policy": {"requires_merge_rule": true}}',
            '{"branchProtection": {"enabled": true}}',
            '{"branch_protection_enabled": true}',
            '{"required_status_checks": ["lint"]}',
            '{"merge_queue_enabled": true}',
            '{"github": {"actions": {"required": true}}}',
            '{"github.actions.required": true}',
            '{"verification": "github-actions"}',
            '{"functional_verification": ["ci"]}',
            '{"required_checks": ["lint"]}',
        ]
        for text in rejected:
            with self.subTest(text=text):
                self.assertTrue(validate_structured_policy(text, "fixture.json"))
        for text in [
            '{"requires_ci": false}',
            '{"repositoryPolicy": {"ciWorkflow": false, "prTemplate": false}}',
            '{"policy": {"requires_merge_rule": false}}',
            '{"branchProtection": {"enabled": false}}',
            '{"branch_protection_enabled": false}',
            '{"required_status_checks": []}',
            '{"merge_queue_enabled": false}',
            '{"github": {"actions": {"required": false}}}',
            '{"github.actions.required": false}',
            '{"coverage": {"branch_percent": 90}}',
            '{"verification": "selected-local-or-existing-target-check"}',
        ]:
            with self.subTest(text=text):
                self.assertEqual(validate_structured_policy(text, "fixture.json"), [])

    def test_yaml_policy_scanner_is_nested_and_fail_closed(self) -> None:
        rejected = [
            "ci:\n  required: true\n",
            "policy:\n  merge_rule: required\n",
            "'requires_ci': true\n",
            '"requires_ci": true\n',
            "policy: {requires_ci: true}\n",
            "checks: [github-actions]\n",
            "verification:\n  - github-actions\n",
        ]
        for text in rejected:
            with self.subTest(text=text):
                self.assertTrue(validate_structured_policy(text, "fixture.yaml"))
        accepted = "ci:\n  required: false\nverification: selected-local-or-existing-target-check\n"
        self.assertEqual(validate_structured_policy(accepted, "fixture.yaml"), [])

    def test_python_policy_scanner_covers_calls_attributes_and_subscripts(self) -> None:
        rejected = [
            "enforce_ci()\n",
            "configure_ci(required=True)\n",
            "github.update_branch_protection(owner='o', repository='r')\n",
            "set_merge_queue(True)\n",
            "settings.ci.required = True\n",
            'settings["ci"]["required"] = True\n',
            'settings["ci"] = {"required": True}\n',
            'policy = {"requires_merge_rule": True}\n',
            "import subprocess\nsubprocess.run(['gh', 'api', 'repos/o/r/branches/main/protection', '--method', 'PUT'])\n",
            "import subprocess\nsubprocess.check_call('gh api --method=PATCH repos/o/r/rulesets/1', shell=True)\n",
            "import subprocess\nsubprocess.run(['gh', 'api', 'repos/o/r/merge-queue', '-f', 'enabled=true'])\n",
            "import subprocess\nsubprocess.run(['gh', 'api', '-Fenabled=true', 'repos/o/r/branches/main/protection'])\n",
            "import subprocess\nsubprocess.run(['gh', 'api', '--input', 'policy.json', 'repos/o/r/rulesets'])\n",
            "import os\nos.system('gh api repos/o/r/branches/main/protection --method PUT')\n",
            "import subprocess as sp\nsp.run(['gh', 'api', 'repos/o/r/rulesets', '--method', 'POST'])\n",
            "from subprocess import run\nrun(['gh', 'api', 'repos/o/r/rulesets', '--method', 'POST'])\n",
            "from subprocess import run as execute\nexecute(['gh', 'api', 'repos/o/r/rulesets', '--method', 'POST'])\n",
            "from os import system\nsystem('gh api repos/o/r/branches/main/protection --method PUT')\n",
            "import subprocess\nendpoint = make_endpoint()\nsubprocess.run(['gh', 'api', endpoint, '--method', 'PUT'])\n",
            "import subprocess\nendpoint = make_endpoint()\nsubprocess.run(['gh', 'api', '--method', 'PUT', endpoint])\n",
            "import subprocess\nendpoint = make_endpoint()\nsubprocess.run(['gh', 'api', '--input', 'policy.json', endpoint])\n",
        ]
        for text in rejected:
            with self.subTest(text=text):
                self.assertTrue(validate_structured_policy(text, "fixture.py"))
        accepted = [
            "settings.ci.required = False\nconfigure_ci(required=False)\nbranch_percent = 90\n",
            "github.get_branch_protection(owner='o', repository='r')\n",
            "import subprocess\nsubprocess.run(['gh', 'api', 'repos/o/r/branches/main/protection'])\n",
            "import subprocess\nvalue = get_value()\nsubprocess.run(['gh', 'api', 'repos/o/r/issues/1', '-f', value])\n",
            "import subprocess\nsubprocess.run(['echo', 'gh api repos/o/r/branches/main/protection --method PUT'])\n",
        ]
        for text in accepted:
            with self.subTest(text=text):
                self.assertEqual(validate_structured_policy(text, "fixture.py"), [])

    def test_policy_tree_rejects_directory_symlinks_before_directory_filtering(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "portable"
            outside = Path(directory) / "outside"
            root.mkdir()
            outside.mkdir()
            (root / "linked").symlink_to(outside, target_is_directory=True)
            errors = validate_policy_tree(root)
            self.assertTrue(errors)
            self.assertIn("symlink", errors[0])

    def test_toml_policy_scanner_covers_nested_github_settings(self) -> None:
        rejected = [
            "[github.actions]\nrequired = true\n",
            "[repositoryPolicy]\nciWorkflow = true\n",
            '[repositoryPolicy]\nprTemplate = "required.md"\n',
        ]
        for text in rejected:
            with self.subTest(text=text):
                self.assertTrue(validate_structured_policy(text, "fixture.toml"))
        accepted = (
            "[github.actions]\nrequired = false\n"
            'developer_instructions = "Use local checks or existing target-owned evidence."\n'
        )
        self.assertEqual(validate_structured_policy(accepted, "fixture.toml"), [])

    def test_all_portable_skill_assets_preserve_repository_policy_ownership(self) -> None:
        self.assertEqual(validate_skill_tree(ROOT / ".agents/skills"), [])

    def test_manifest_never_distributes_repository_policy(self) -> None:
        manifest = json.loads((ROOT / "distribution/manifest.json").read_text(encoding="utf-8"))
        failures: list[str] = []
        validate_manifest_document(manifest, ROOT, failures)
        self.assertEqual(failures, [])
        expected_default = {
            ".agents/skills/chat-first-development",
            ".agents/skills/maintain-canonical-requirements",
            ".agents/skills/generate-implementation-design",
            ".agents/skills/inspect-quality-gates",
        }
        for profile in ["default", "chat-first"]:
            self.assertEqual(
                {entry["source"] for entry in manifest["profiles"][profile]},
                expected_default,
            )

    def test_manifest_expands_directory_leaves_and_rejects_policy_paths(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle = root / "bundle"
            bundle.mkdir()
            (bundle / "standard.md").write_text(
                "Existing target-owned checks may be used; do not require CI.\n",
                encoding="utf-8",
            )
            (bundle / "reviewer.toml").write_text(
                'developer_instructions = "Use bounded local evidence."\n',
                encoding="utf-8",
            )
            (root / "spec/skills").mkdir(parents=True)
            (root / "spec/skills/skills.qnt").write_text("module skills {}\n", encoding="utf-8")
            (root / "spec/skills/skills.json").write_text("{}\n", encoding="utf-8")
            (root / "tools").mkdir()
            (root / "tools/runner.py").write_text(
                '_load_pinned_tool("helper")\n',
                encoding="utf-8",
            )
            (root / "tools/helper.py").write_text("VALUE = 1\n", encoding="utf-8")

            manifest = {
                "profiles": {
                    "fixture": [{"source": "bundle", "destination": "portable"}],
                },
                "formal_skill_contracts": {
                    "mappings": [
                        {
                            "source": "spec/skills/skills.qnt",
                            "destination": "spec/skills/skills.qnt",
                        },
                        {
                            "source": "spec/skills/skills.json",
                            "destination": "spec/skills/skills.json",
                        },
                    ],
                },
                "portable_runtime": {
                    "runner": {
                        "source": "tools/runner.py",
                        "destination": "tools/runner.py",
                        "local_imports": "derive-from-_load_pinned_tool-calls",
                    },
                    "mappings": [],
                },
            }
            failures: list[str] = []
            validate_manifest_document(manifest, root, failures)
            self.assertEqual(failures, [])

            forbidden_leaves = [
                ".github/workflows/ci.yml",
                ".gitlab/merge_request_templates/default.md",
                ".gitlab-ci.yml",
                "ci.yml",
                "governance/reviews/template.yaml",
                ".husky/pre-commit",
                "PULL_REQUEST_TEMPLATE.md",
                "merge_request_template.md",
                "pull-request-template.md",
                "hooks/post-commit",
                "config/branch-protection.json",
                "config/ruleset.yaml",
                "config/merge-queue.toml",
            ]
            for relative in forbidden_leaves:
                with self.subTest(relative=relative):
                    path = bundle / relative
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text("enabled: true\n", encoding="utf-8")
                    failures = []
                    validate_manifest_document(manifest, root, failures)
                    self.assertTrue(failures)
                    path.unlink()

            root_mapping = json.loads(json.dumps(manifest))
            root_mapping["profiles"]["fixture"] = [
                {"source": ".", "destination": "portable"}
            ]
            failures = []
            validate_manifest_document(root_mapping, root, failures)
            self.assertTrue(failures)

            aliased_mapping = json.loads(json.dumps(manifest))
            aliased_mapping["profiles"]["fixture"] = [
                {"source": "./bundle", "destination": "portable"}
            ]
            failures = []
            validate_manifest_document(aliased_mapping, root, failures)
            self.assertTrue(failures)

            protected_destination = json.loads(json.dumps(manifest))
            protected_destination["profiles"]["fixture"] = [
                {"source": "bundle", "destination": ".github/actions"}
            ]
            failures = []
            validate_manifest_document(protected_destination, root, failures)
            self.assertTrue(failures)

            (root / "alternate.md").write_text("Bounded portable guidance.\n", encoding="utf-8")
            collision = json.loads(json.dumps(manifest))
            collision["profiles"]["fixture"] = [
                {"source": "bundle/standard.md", "destination": "portable/standard.md"},
                {"source": "alternate.md", "destination": "portable/standard.md"},
            ]
            failures = []
            validate_manifest_document(collision, root, failures)
            self.assertTrue(any("destination collision" in error for error in failures))

    def test_all_quint_requirement_fields_have_a_golden_json_mapping(self) -> None:
        source = {
            "schemaVersion": 1,
            "catalogRevision": 73,
            "product": "golden-product",
            "updatedAt": "2026-08-29",
            "requirements": [
                {
                    "id": "REQ-GOLDEN-001",
                    "revision": 17,
                    "status": "retired",
                    "kind": "functional",
                    "title": "Golden title",
                    "subject": "Golden subject",
                    "actionName": "generate",
                    "objectName": "Golden object",
                    "rationale": "Golden rationale",
                    "sourceRefs": ["source-alpha"],
                    "acceptanceCriteria": [
                        {"id": "AC-GOLDEN-001-1", "given": "Given alpha", "when_": "When beta", "expected": "Then gamma"}
                    ],
                    "verification": {"method": "Method delta", "evidence": "Evidence epsilon"},
                    "traces": {
                        "design": ["design/zeta"],
                        "implementation": ["implementation/eta"],
                        "tests": ["tests/theta"],
                        "standards": ["standard-iota"],
                    },
                    "lastChangedBy": "change-kappa",
                    "retirementReason": "retirement-lambda",
                    "supersededBy": "REQ-GOLDEN-002",
                    "scopeName": "product",
                    "categoryName": "functional",
                }
            ],
        }
        self.assertEqual(
            catalog_to_json(source),
            {
                "schema_version": 1,
                "catalog_revision": 73,
                "product": "golden-product",
                "updated_at": "2026-08-29",
                "requirements": [
                    {
                        "id": "REQ-GOLDEN-001",
                        "revision": 17,
                        "status": "retired",
                        "type": "functional",
                        "title": "Golden title",
                        "subject": "Golden subject",
                        "action": "generate",
                        "object": "Golden object",
                        "rationale": "Golden rationale",
                        "source_refs": ["source-alpha"],
                        "acceptance_criteria": [
                            {"id": "AC-GOLDEN-001-1", "given": "Given alpha", "when": "When beta", "then": "Then gamma"}
                        ],
                        "verification": {"method": "Method delta", "evidence": "Evidence epsilon"},
                        "traces": {
                            "design": ["design/zeta"],
                            "implementation": ["implementation/eta"],
                            "tests": ["tests/theta"],
                            "standards": ["standard-iota"],
                        },
                        "last_changed_by": "change-kappa",
                        "retirement_reason": "retirement-lambda",
                        "superseded_by": "REQ-GOLDEN-002",
                        "scope": "product",
                        "category": "functional",
                    }
                ],
            },
        )

    def test_mapping_rejects_unmapped_quint_fields(self) -> None:
        source = {
            "schemaVersion": 1,
            "catalogRevision": 0,
            "product": "fixture",
            "updatedAt": "2026-08-29",
            "requirements": [],
            "futureField": "must-not-be-dropped",
        }
        with self.assertRaises(MappingError):
            catalog_to_json(source)

    def test_markdown_is_rendered_only_from_serialized_json_with_golden_semantics(self) -> None:
        catalog = {
            "schema_version": 1,
            "catalog_revision": 1,
            "product": "golden-render",
            "updated_at": "2026-08-29",
            "requirements": [
                {
                    "id": "REQ-GOLDEN-001",
                    "revision": 1,
                    "status": "retired",
                    "type": "functional",
                    "title": "Title alpha",
                    "subject": "Subject beta",
                    "action": "generate",
                    "object": "Object gamma",
                    "rationale": "Rationale delta",
                    "source_refs": ["Source epsilon"],
                    "acceptance_criteria": [
                        {"id": "AC-GOLDEN-001-1", "given": "Given zeta", "when": "When eta", "then": "Then theta"}
                    ],
                    "verification": {"method": "Method iota", "evidence": "Evidence kappa"},
                    "traces": {
                        "design": ["design/lambda"],
                        "implementation": ["implementation/mu"],
                        "tests": ["tests/nu"],
                        "standards": ["standard-xi"],
                    },
                    "last_changed_by": "change-omicron",
                    "retirement_reason": "Retirement pi",
                    "superseded_by": "",
                    "scope": "product",
                    "category": "functional",
                }
            ],
        }
        serialized = json.dumps(catalog, ensure_ascii=False, sort_keys=True)
        rendered = render_serialized_json(serialized, load_specflow())
        for expected in [
            "# golden-render 要件一覧",
            "- スキーマ版: 1",
            "- カタログ版: 1",
            '- Product(JSON): <code>"golden-render"</code>',
            '- 更新日(JSON): <code>"2026-08-29"</code>',
            "## REQ-GOLDEN-001: Title alpha",
            '要件ID(JSON): <code>"REQ-GOLDEN-001"</code>',
            'タイトル(JSON): <code>"Title alpha"</code>',
            '主体(JSON): <code>"Subject beta"</code>',
            '対象(JSON): <code>"Object gamma"</code>',
            "Subject betaは、Object gammaを**生成する**。",
            '行為enum: <code>"generate"</code>',
            "根拠: Rationale delta",
            '根拠(JSON): <code>"Rationale delta"</code>',
            "項目版: 1 / 状態: `retired` / 種別: `functional`",
            '変更識別子: <code>"change-omicron"</code>',
            '分類: scope=<code>"product"</code> / category=<code>"functional"</code>',
            "前提: Given zeta。条件: When eta。期待結果: Then theta。",
            "criterion(JSON Object): <code>{",
            '要求源(JSON List): <code>["Source epsilon"]</code>',
            "検証証跡: Evidence kappa",
            "検証(JSON Object): <code>{",
            '設計: <code>["design/lambda"]</code>',
            '実装: <code>["implementation/mu"]</code>',
            'テスト: <code>["tests/nu"]</code>',
            '参照資料: <code>["standard-xi"]</code>',
            '廃止理由: <code>"Retirement pi"</code>',
        ]:
            self.assertIn(expected, rendered)
        with self.assertRaises(RequirementsRenderError):
            render_serialized_json(catalog, load_specflow())  # type: ignore[arg-type]

    def test_requirement_schema_and_specflow_have_an_explicit_differential_boundary(self) -> None:
        schema = json.loads(
            (
                ROOT
                / ".agents/skills/maintain-canonical-requirements/assets/requirements.schema.json"
            ).read_text(encoding="utf-8")
        )
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        specflow = load_specflow()
        canonical = extract_requirements()
        template = catalog_to_json(extract_state(REQUIREMENTS_TEMPLATE_QNT, "catalog"))

        for label, catalog in [("source", canonical), ("template", template)]:
            with self.subTest(golden=label):
                self.assertEqual(list(validator.iter_errors(catalog)), [])
                self.assertEqual(
                    specflow.validate_catalog(copy.deepcopy(catalog), trace_root=ROOT),
                    catalog,
                )
        example = json.loads(
            (
                ROOT
                / ".agents/skills/maintain-canonical-requirements/assets/documentation-project-nfr.example.json"
            ).read_text(encoding="utf-8")
        )
        requirement_schema = {
            "$schema": schema["$schema"],
            "$ref": "#/$defs/requirement",
            "$defs": schema["$defs"],
        }
        self.assertEqual(
            list(Draft202012Validator(requirement_schema).iter_errors(example)),
            [],
        )
        specflow.validate_requirement(copy.deepcopy(example), set(), ROOT)

        shared_rejections: list[tuple[str, dict[str, Any]]] = []

        def rejected(label: str, mutate: Any) -> None:
            candidate = copy.deepcopy(canonical)
            mutate(candidate)
            shared_rejections.append((label, candidate))

        rejected("catalog-extra-field", lambda value: value.__setitem__("future", True))
        rejected("schema-version-bool", lambda value: value.__setitem__("schema_version", True))
        rejected("catalog-revision-bool", lambda value: value.__setitem__("catalog_revision", True))
        rejected("catalog-revision-zero", lambda value: value.__setitem__("catalog_revision", 0))
        rejected("empty-product", lambda value: value.__setitem__("product", ""))
        rejected("empty-updated-at", lambda value: value.__setitem__("updated_at", ""))
        rejected("empty-catalog", lambda value: value.__setitem__("requirements", []))
        rejected("missing-title", lambda value: value["requirements"][0].pop("title"))
        rejected(
            "requirement-extra-field",
            lambda value: value["requirements"][0].__setitem__("future", "unmapped"),
        )
        rejected(
            "revision-bool",
            lambda value: value["requirements"][0].__setitem__("revision", True),
        )
        rejected("invalid-revision", lambda value: value["requirements"][0].__setitem__("revision", 0))
        rejected("invalid-status", lambda value: value["requirements"][0].__setitem__("status", "future"))
        rejected("invalid-type", lambda value: value["requirements"][0].__setitem__("type", "future"))
        rejected("invalid-action", lambda value: value["requirements"][0].__setitem__("action", "invent"))
        for field in ["id", "title", "subject", "object", "rationale", "last_changed_by"]:
            rejected(
                f"empty-{field}",
                lambda value, field=field: value["requirements"][0].__setitem__(field, ""),
            )
        rejected("empty-source", lambda value: value["requirements"][0].__setitem__("source_refs", []))
        rejected(
            "duplicate-source",
            lambda value: value["requirements"][0]["source_refs"].append(
                value["requirements"][0]["source_refs"][0]
            ),
        )
        rejected(
            "criterion-extra-field",
            lambda value: value["requirements"][0]["acceptance_criteria"][0].__setitem__(
                "future", "unmapped"
            ),
        )
        rejected(
            "empty-criterion-given",
            lambda value: value["requirements"][0]["acceptance_criteria"][0].__setitem__(
                "given", ""
            ),
        )
        rejected(
            "empty-verification-evidence",
            lambda value: value["requirements"][0]["verification"].__setitem__(
                "evidence", ""
            ),
        )
        rejected(
            "empty-trace-value",
            lambda value: value["requirements"][0]["traces"].__setitem__(
                "design", [""]
            ),
        )
        rejected(
            "duplicate-trace",
            lambda value: value["requirements"][0]["traces"]["design"].append(
                value["requirements"][0]["traces"]["design"][0]
            ),
        )
        rejected(
            "classification-half-pair",
            lambda value: value["requirements"][0].update(
                {"scope": "product", "category": ""}
            ),
        )
        active_index = next(
            index
            for index, requirement in enumerate(canonical["requirements"])
            if requirement["status"] == "active"
        )
        rejected(
            "active-retirement-reason",
            lambda value: value["requirements"][active_index].__setitem__(
                "retirement_reason", "not retired"
            ),
        )

        for label, candidate in shared_rejections:
            with self.subTest(shared_rejection=label):
                self.assertTrue(list(validator.iter_errors(candidate)))
                with self.assertRaises(specflow.SpecError):
                    specflow.validate_catalog(candidate, trace_root=ROOT)

        schema_only_boundaries: list[tuple[str, dict[str, Any]]] = []
        duplicate_id = copy.deepcopy(canonical)
        duplicate_id["requirements"].append(copy.deepcopy(duplicate_id["requirements"][0]))
        schema_only_boundaries.append(("global-id-uniqueness", duplicate_id))

        duplicate_ac = copy.deepcopy(canonical)
        duplicate_ac["requirements"][1]["acceptance_criteria"][0]["id"] = (
            duplicate_ac["requirements"][0]["acceptance_criteria"][0]["id"]
        )
        schema_only_boundaries.append(("global-acceptance-id-uniqueness", duplicate_ac))

        missing_trace = copy.deepcopy(canonical)
        missing_trace["requirements"][0]["traces"]["design"] = [
            "docs/design/generated/does-not-exist.md"
        ]
        schema_only_boundaries.append(("trace-file-existence", missing_trace))

        retired_index = next(
            index
            for index, requirement in enumerate(canonical["requirements"])
            if requirement["status"] == "retired"
        )
        missing_successor = copy.deepcopy(canonical)
        missing_successor["requirements"][retired_index]["superseded_by"] = "REQ-MISSING-999"
        schema_only_boundaries.append(("supersession-graph", missing_successor))

        for label, candidate in schema_only_boundaries:
            with self.subTest(specflow_only_rejection=label):
                self.assertEqual(list(validator.iter_errors(candidate)), [])
                with self.assertRaises(specflow.SpecError):
                    specflow.validate_catalog(candidate, trace_root=ROOT)

    def test_requirements_quint_declares_atomicity_and_retirement_invariants(self) -> None:
        text = (ROOT / "spec/requirements/requirements.qnt").read_text(encoding="utf-8")
        for invariant in [
            "requirementIdsAreUnique",
            "requirementsAreStructurallyComplete",
            "classificationIsPaired",
            "retirementFieldsAreConsistent",
            "lifecycleRevisionTransitionIsSound",
            "lifecycleRefinesCatalog",
            "traceLinksAreUnique",
            "RequirementOperation",
            "foldBatchOperations",
            "batchResurrectionOperation",
            "catalogWellFormed",
        ]:
            self.assertIn(invariant, text)

    def test_distributed_requirement_template_is_quint_and_not_json(self) -> None:
        assets = ROOT / ".agents/skills/maintain-canonical-requirements/assets"
        template = assets / "requirements.template.qnt"
        self.assertTrue(template.is_file())
        self.assertFalse((assets / "requirements.template.json").exists())
        text = template.read_text(encoding="utf-8")
        for invariant in [
            "requirementIdsAreUnique",
            "requirementsAreStructurallyComplete",
            "classificationIsPaired",
            "requirementsAreTyped",
            "acceptanceCriteriaAreComplete",
            "acceptanceCriterionIdsAreUnique",
            "retirementFieldsAreConsistent",
            "RequirementOperation",
            "foldBatchOperations",
            "batchResurrectionOperation",
            "lifecycleRevisionTransitionIsSound",
            "lifecycleRefinesCatalog",
            "catalogWellFormed",
        ]:
            self.assertIn(invariant, text)

    def test_skill_quint_declares_portability_and_three_pillar_invariants(self) -> None:
        text = (ROOT / "spec/skills/skills.qnt").read_text(encoding="utf-8")
        for invariant in [
            "contractsAreComplete",
            "threePillarsOnly",
            "repositoryPolicyIsHostOwned",
            "runnerConformanceIsExplicit",
            "defaultPortableSetIsMinimal",
            "workflowOrderIsConsistent",
            "portablePolicyIsUntouched",
        ]:
            self.assertIn(invariant, text)
        self.assertRegex(
            text,
            r"(?s)run policyMutationRejectedTest.*requestPolicyMutation\(\"ci-workflow\"\)"
            r".*rejectPolicyMutation.*policyDecision == \"rejected-host-owned\"",
        )

    def test_derived_documents_declare_their_sources(self) -> None:
        skills = json.loads((ROOT / "spec/skills/skills.json").read_text(encoding="utf-8"))
        self.assertEqual(skills["source"], "spec/skills/skills.qnt")
        self.assertEqual(skills["quint_version"], "0.32.0")
        self.assertIn("dependenciesAreClosed", skills["invariants"])
        self.assertIn("runnerConformanceIsExplicit", skills["invariants"])
        requirements_doc = (ROOT / "docs/requirements/REQUIREMENTS.md").read_text(encoding="utf-8")
        skills_doc = (ROOT / "docs/reference/FORMAL-SPECIFICATIONS.md").read_text(encoding="utf-8")
        self.assertIn("requirements.qntを編集すること", requirements_doc)
        self.assertIn("skills.qntを編集すること", skills_doc)


if __name__ == "__main__":
    unittest.main()
