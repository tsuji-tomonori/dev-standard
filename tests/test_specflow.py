from __future__ import annotations

import copy
import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools.quintflow import extract_requirements

ROOT = Path(__file__).resolve().parents[1]


def load_module():
    path = ROOT / ".agents/skills/maintain-canonical-requirements/scripts/specflow.py"
    spec = importlib.util.spec_from_file_location("specflow", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


specflow = load_module()
_SOURCE_CATALOG: dict[str, object] | None = None


def source_catalog() -> dict[str, object]:
    global _SOURCE_CATALOG
    if _SOURCE_CATALOG is None:
        _SOURCE_CATALOG = extract_requirements()
    return copy.deepcopy(_SOURCE_CATALOG)


class SpecflowTest(unittest.TestCase):
    def test_retired_traces_preserve_history_without_requiring_current_files(self) -> None:
        catalog = source_catalog()
        retired = next(item for item in catalog["requirements"] if item["id"] == "REQ-REPO-001")
        retired["traces"]["design"] = ["docs/removed-historical-decision.md"]
        before = copy.deepcopy(retired)
        specflow.validate_catalog(catalog)
        self.assertEqual(retired, before)
        self.assertNotIn(
            ROOT / "docs/removed-historical-decision.md",
            specflow.trace_input_paths(catalog, trace_root=ROOT),
        )
        for unsafe in ["../outside.md", "/outside.md", "docs//old.md"]:
            retired["traces"]["design"] = [unsafe]
            with self.subTest(path=unsafe), self.assertRaises(specflow.SpecError):
                specflow.validate_catalog(catalog)
        retired["traces"]["design"] = before["traces"]["design"]
        retired.update(status="active", retirement_reason="", superseded_by="")
        with self.assertRaisesRegex(specflow.SpecError, "not a regular repository file"):
            specflow.validate_catalog(catalog)

    def test_generated_json_is_valid_and_markdown_is_current(self) -> None:
        catalog = specflow.validate_catalog(
            specflow.read_json(ROOT / "spec/requirements/requirements.json")
        )
        generated = (ROOT / "docs/requirements/REQUIREMENTS.md").read_text(encoding="utf-8")
        self.assertEqual(generated, specflow.render(catalog))
        self.assertEqual(catalog["catalog_revision"], source_catalog()["catalog_revision"])
        self.assertGreaterEqual(len(catalog["requirements"]), 59)
        self.assertEqual(sum(item["status"] == "retired" for item in catalog["requirements"]), 3)
        self.assertIn("正本: `spec/requirements/requirements.qnt`", generated)

    def test_action_enum_is_rejected_but_semantic_atomicity_is_human_reviewed(self) -> None:
        catalog = source_catalog()
        invalid = copy.deepcopy(catalog)
        invalid["requirements"][0]["action"] = "separate and persist"
        with self.assertRaises(specflow.SpecError):
            specflow.validate_catalog(invalid)
        structurally_complete = copy.deepcopy(catalog)
        structurally_complete["requirements"][0]["object"] += "; and another obligation"
        self.assertIs(
            structurally_complete,
            specflow.validate_catalog(structurally_complete),
        )

    def test_retirement_requires_an_explicit_tombstone(self) -> None:
        catalog = source_catalog()
        invalid = copy.deepcopy(catalog)
        item = next(value for value in invalid["requirements"] if value["id"] == "REQ-REPO-001")
        del item["retirement_reason"]
        with self.assertRaises(specflow.SpecError):
            specflow.validate_catalog(invalid)

    def test_json_cli_cannot_mutate_the_quint_authority(self) -> None:
        choices = specflow.parser()._subparsers._group_actions[0].choices
        self.assertEqual(set(choices), {"validate", "generate", "check"})
        self.assertNotIn("apply", choices)

    def test_add_trace_update_and_retire_advance_revisions(self) -> None:
        original = source_catalog()
        added = copy.deepcopy(original["requirements"][0])
        added.update(
            {
                "id": "REQ-LIFECYCLE-001",
                "revision": 1,
                "status": "active",
                "title": "lifecycle fixture",
                "last_changed_by": "ignored-on-add",
            }
        )
        added["acceptance_criteria"][0]["id"] = "AC-LIFECYCLE-001-1"
        catalog = specflow.apply_change(
            original,
            {
                "base_catalog_revision": original["catalog_revision"],
                "changed_at": "2026-08-29",
                "work_item": "CHG-LIFECYCLE-ADD",
                "operations": [{"op": "add", "requirement": added}],
            },
        )
        item = next(value for value in catalog["requirements"] if value["id"] == added["id"])
        self.assertEqual(catalog["catalog_revision"], original["catalog_revision"] + 1)
        self.assertEqual(item["revision"], 1)
        self.assertEqual(item["last_changed_by"], "CHG-LIFECYCLE-ADD")

        changed_traces = copy.deepcopy(item["traces"])
        changed_traces["tests"] = ["tests/test_specflow.py", "tests/test_spec_mapping.py"]
        updated = specflow.apply_change(
            catalog,
            {
                "base_catalog_revision": catalog["catalog_revision"],
                "changed_at": "2026-08-29",
                "work_item": "CHG-LIFECYCLE-TRACE",
                "operations": [
                    {
                        "op": "trace",
                        "id": item["id"],
                        "expected_revision": 1,
                        "traces": changed_traces,
                    }
                ],
            },
        )
        item = next(value for value in updated["requirements"] if value["id"] == added["id"])
        self.assertEqual(updated["catalog_revision"], catalog["catalog_revision"] + 1)
        self.assertEqual(item["revision"], 2)
        self.assertEqual(item["traces"], changed_traces)

        retired = specflow.apply_change(
            updated,
            {
                "base_catalog_revision": updated["catalog_revision"],
                "changed_at": "2026-08-29",
                "work_item": "CHG-LIFECYCLE-RETIRE",
                "operations": [
                    {
                        "op": "retire",
                        "id": item["id"],
                        "expected_revision": 2,
                        "reason": "fixture completed",
                    }
                ],
            },
        )
        item = next(value for value in retired["requirements"] if value["id"] == added["id"])
        self.assertEqual(retired["catalog_revision"], updated["catalog_revision"] + 1)
        self.assertEqual(item["revision"], 3)
        self.assertEqual(item["status"], "retired")
        self.assertEqual(item["retirement_reason"], "fixture completed")

    def test_lifecycle_rejects_noop_duplicate_and_invalid_add_revision(self) -> None:
        catalog = source_catalog()
        item = copy.deepcopy(catalog["requirements"][0])
        with self.assertRaises(specflow.SpecError):
            specflow.apply_change(
                catalog,
                {
                    "base_catalog_revision": catalog["catalog_revision"],
                    "changed_at": "2026-08-29",
                    "work_item": "CHG-NOOP",
                    "operations": [
                        {
                            "op": "trace",
                            "id": item["id"],
                            "expected_revision": item["revision"],
                            "traces": copy.deepcopy(item["traces"]),
                        }
                    ],
                },
            )
        item["id"] = "REQ-LIFECYCLE-INVALID"
        item["revision"] = 2
        with self.assertRaises(specflow.SpecError):
            specflow.apply_change(
                catalog,
                {
                    "base_catalog_revision": catalog["catalog_revision"],
                    "changed_at": "2026-08-29",
                    "work_item": "CHG-BAD-ADD",
                    "operations": [{"op": "add", "requirement": item}],
                },
            )

    def test_update_and_trace_reject_retired_requirements(self) -> None:
        catalog = source_catalog()
        item = next(value for value in catalog["requirements"] if value["status"] == "retired")
        common = {
            "base_catalog_revision": catalog["catalog_revision"],
            "changed_at": "2026-08-29",
            "work_item": "CHG-RETIRED-REJECTION",
        }
        with self.assertRaises(specflow.SpecError):
            specflow.apply_change(
                catalog,
                {
                    **common,
                    "operations": [
                        {
                            "op": "update",
                            "id": item["id"],
                            "expected_revision": item["revision"],
                            "changes": {"title": "must not change"},
                        }
                    ],
                },
            )
        with self.assertRaises(specflow.SpecError):
            specflow.apply_change(
                catalog,
                {
                    **common,
                    "operations": [
                        {
                            "op": "trace",
                            "id": item["id"],
                            "expected_revision": item["revision"],
                            "traces": copy.deepcopy(item["traces"]),
                        }
                    ],
                },
            )

    def test_catalog_and_item_compare_and_swap_are_both_required(self) -> None:
        catalog = source_catalog()
        item = next(value for value in catalog["requirements"] if value["status"] == "active")
        change = {
            "base_catalog_revision": catalog["catalog_revision"] - 1,
            "changed_at": "2026-08-29",
            "work_item": "CHG-STALE",
            "operations": [
                {
                    "op": "update",
                    "id": item["id"],
                    "expected_revision": item["revision"],
                    "changes": {"title": "changed"},
                }
            ],
        }
        with self.assertRaises(specflow.SpecError):
            specflow.apply_change(catalog, change)
        change["base_catalog_revision"] = catalog["catalog_revision"]
        change["operations"][0]["expected_revision"] = item["revision"] - 1
        with self.assertRaises(specflow.SpecError):
            specflow.apply_change(catalog, change)

    def test_trace_duplicates_and_unresolved_paths_are_rejected_together(self) -> None:
        catalog = source_catalog()
        duplicate = copy.deepcopy(catalog)
        item = next(value for value in duplicate["requirements"] if value["status"] == "active")
        item["traces"]["tests"] = ["tests/test_specflow.py", "tests/test_specflow.py"]
        with self.assertRaises(specflow.SpecError):
            specflow.validate_catalog(duplicate)

        missing = copy.deepcopy(catalog)
        item = next(value for value in missing["requirements"] if value["status"] == "active")
        item["traces"]["tests"] = ["tests/does-not-exist.py"]
        with self.assertRaises(specflow.SpecError):
            specflow.validate_catalog(missing)

    def test_requirements_phase_allows_downstream_trace_handoff(self) -> None:
        catalog = source_catalog()
        item = next(value for value in catalog["requirements"] if value["status"] == "active")
        item["traces"]["implementation"] = []
        item["traces"]["tests"] = []
        self.assertIs(catalog, specflow.validate_catalog(catalog))

    def test_trace_rejects_leaf_and_ancestor_symlink_aliases(self) -> None:
        catalog = source_catalog()
        with tempfile.TemporaryDirectory(prefix="specflow-trace-", dir=ROOT) as directory:
            fixture = Path(directory)
            real_directory = fixture / "real"
            real_directory.mkdir()
            real_file = real_directory / "test.py"
            real_file.write_text("# fixture\n", encoding="utf-8")
            leaf_alias = fixture / "leaf.py"
            leaf_alias.symlink_to(real_file.relative_to(fixture))
            ancestor_alias = fixture / "alias"
            ancestor_alias.symlink_to(real_directory.name, target_is_directory=True)

            for alias in [leaf_alias, ancestor_alias / real_file.name]:
                invalid = copy.deepcopy(catalog)
                item = next(
                    value for value in invalid["requirements"] if value["status"] == "active"
                )
                item["traces"]["tests"] = [os.fspath(alias.relative_to(ROOT))]
                with self.assertRaises(specflow.SpecError):
                    specflow.validate_catalog(invalid)

    def test_check_rejects_symlinked_generated_output(self) -> None:
        with tempfile.TemporaryDirectory(prefix="specflow-check-", dir=ROOT) as directory:
            alias = Path(directory) / "requirements.md"
            alias.symlink_to(ROOT / "docs/requirements/REQUIREMENTS.md")
            self.assertEqual(
                2,
                specflow.main(
                    [
                        "check",
                        "--spec",
                        os.fspath(ROOT / "spec/requirements/requirements.json"),
                        "--out",
                        os.fspath(alias),
                    ]
                ),
            )

    def test_retirement_fields_and_successor_are_consistent(self) -> None:
        catalog = source_catalog()
        retired_index = next(
            index
            for index, value in enumerate(catalog["requirements"])
            if value["status"] == "retired"
        )
        active = next(
            value
            for value in catalog["requirements"][retired_index + 1 :]
            if value["status"] == "active"
        )
        invalid = copy.deepcopy(catalog)
        target = next(value for value in invalid["requirements"] if value["id"] == active["id"])
        target["retirement_reason"] = "not retired"
        with self.assertRaises(specflow.SpecError):
            specflow.validate_catalog(invalid)

        invalid = copy.deepcopy(catalog)
        retired = invalid["requirements"][retired_index]
        retired["superseded_by"] = "REQ-DOES-NOT-EXIST"
        with self.assertRaises(specflow.SpecError):
            specflow.validate_catalog(invalid)

        valid = copy.deepcopy(catalog)
        retired = valid["requirements"][retired_index]
        retired["superseded_by"] = active["id"]
        self.assertIs(valid, specflow.validate_catalog(valid))

    def test_exact_fields_positive_revisions_and_allowed_actions_match_contract(self) -> None:
        catalog = source_catalog()
        self.assertEqual(
            specflow.ACTIONS,
            {
                "constrain",
                "derive",
                "detect",
                "discover",
                "enable",
                "enforce",
                "estimate",
                "expand",
                "formalize",
                "generate",
                "maintain",
                "measure",
                "parse",
                "preserve",
                "provide",
                "route",
                "select",
                "separate",
                "stage",
                "stop",
                "structure",
                "validate",
                "verify",
            },
        )
        for field in specflow.REQUIREMENT_FIELDS:
            with self.subTest(missing_field=field):
                invalid = copy.deepcopy(catalog)
                invalid["requirements"][0].pop(field)
                with self.assertRaises(specflow.SpecError):
                    specflow.validate_catalog(invalid)
        for path, value in [
            (("catalog_revision",), True),
            (("requirements", 0, "revision"), True),
            (("catalog_revision",), 0),
            (("requirements", 0, "revision"), 0),
        ]:
            with self.subTest(path=path, value=value):
                invalid = copy.deepcopy(catalog)
                target = invalid
                for component in path[:-1]:
                    target = target[component]
                target[path[-1]] = value
                with self.assertRaises(specflow.SpecError):
                    specflow.validate_catalog(invalid)

    def test_trace_requires_canonical_repository_relative_regular_files(self) -> None:
        catalog = source_catalog()
        for trace in [
            ".",
            "tests",
            "tests/./test_specflow.py",
            "tests/../tests/test_specflow.py",
            "/tests/test_specflow.py",
            "tests\\test_specflow.py",
        ]:
            with self.subTest(trace=trace):
                invalid = copy.deepcopy(catalog)
                invalid["requirements"][0]["traces"]["tests"] = [trace]
                with self.assertRaises(specflow.SpecError):
                    specflow.validate_catalog(invalid)

    def test_supersession_chain_may_cross_retired_items_but_ends_active(self) -> None:
        base = copy.deepcopy(source_catalog()["requirements"][0])
        base["traces"] = {
            "design": [],
            "implementation": [],
            "tests": [],
            "standards": ["QUINT-0.32"],
        }

        def item(rid: str, criterion_id: str) -> dict[str, object]:
            value = copy.deepcopy(base)
            value.update(
                {
                    "id": rid,
                    "acceptance_criteria": [
                        {
                            "id": criterion_id,
                            "given": "catalog",
                            "when": "validated",
                            "then": "chain is valid",
                        }
                    ],
                    "status": "active",
                    "retirement_reason": "",
                    "superseded_by": "",
                }
            )
            return value

        first = item("REQ-CHAIN-1", "AC-CHAIN-1")
        second = item("REQ-CHAIN-2", "AC-CHAIN-2")
        terminal = item("REQ-CHAIN-3", "AC-CHAIN-3")
        first.update(
            {
                "status": "retired",
                "retirement_reason": "replaced by second",
                "superseded_by": "REQ-CHAIN-2",
            }
        )
        second.update(
            {
                "status": "retired",
                "retirement_reason": "replaced by terminal",
                "superseded_by": "REQ-CHAIN-3",
            }
        )
        catalog = {
            "schema_version": 1,
            "catalog_revision": 1,
            "product": "chain-fixture",
            "updated_at": "fixture",
            "requirements": [first, second, terminal],
        }
        self.assertIs(catalog, specflow.validate_catalog(catalog))

        for label, mutate in [
            ("cycle", lambda value: value["requirements"][1].__setitem__("superseded_by", "REQ-CHAIN-1")),
            ("dangling", lambda value: value["requirements"][1].__setitem__("superseded_by", "REQ-MISSING")),
            (
                "retired-terminal",
                lambda value: value["requirements"][1].__setitem__("superseded_by", ""),
            ),
        ]:
            with self.subTest(label=label):
                invalid = copy.deepcopy(catalog)
                mutate(invalid)
                with self.assertRaises(specflow.SpecError):
                    specflow.validate_catalog(invalid)

    def test_multi_operation_change_is_one_atomic_catalog_transition(self) -> None:
        original = source_catalog()
        active = [item for item in original["requirements"] if item["status"] == "active"]
        first, second = active[:2]
        changed_traces = copy.deepcopy(second["traces"])
        changed_traces["tests"] = ["tests/test_specflow.py"]
        if changed_traces == second["traces"]:
            changed_traces["tests"] = ["tests/test_spec_mapping.py"]
        change = {
            "base_catalog_revision": original["catalog_revision"],
            "changed_at": "batch-change",
            "work_item": "CHG-BATCH",
            "operations": [
                {
                    "op": "update",
                    "id": first["id"],
                    "expected_revision": first["revision"],
                    "changes": {"title": first["title"] + " updated"},
                },
                {
                    "op": "trace",
                    "id": second["id"],
                    "expected_revision": second["revision"],
                    "traces": changed_traces,
                },
            ],
        }
        before = copy.deepcopy(original)
        updated = specflow.apply_change(original, change)
        self.assertEqual(original, before)
        self.assertEqual(updated["catalog_revision"], before["catalog_revision"] + 1)
        updated_by_id = {item["id"]: item for item in updated["requirements"]}
        self.assertEqual(updated_by_id[first["id"]]["revision"], first["revision"] + 1)
        self.assertEqual(updated_by_id[second["id"]]["revision"], second["revision"] + 1)
        untouched_id = active[2]["id"]
        self.assertEqual(updated_by_id[untouched_id], active[2])

        for label, mutation in [
            (
                "stale-second-item",
                lambda value: value["operations"][1].__setitem__(
                    "expected_revision", second["revision"] - 1
                ),
            ),
            (
                "duplicate-touch",
                lambda value: value["operations"][1].update(
                    {
                        "id": first["id"],
                        "expected_revision": first["revision"],
                    }
                ),
            ),
            (
                "invalid-final",
                lambda value: value["operations"][0]["changes"].__setitem__("title", ""),
            ),
        ]:
            with self.subTest(label=label):
                invalid_change = copy.deepcopy(change)
                mutation(invalid_change)
                unchanged = copy.deepcopy(original)
                with self.assertRaises(specflow.SpecError):
                    specflow.apply_change(original, invalid_change)
                self.assertEqual(original, unchanged)

    def test_renderer_escapes_structure_and_preserves_enum_and_list_boundaries(self) -> None:
        catalog = source_catalog()
        catalog["requirements"] = [copy.deepcopy(catalog["requirements"][0])]
        item = catalog["requirements"][0]
        catalog["product"] = "product | `code`\n## injected <script>"
        catalog["updated_at"] = "date | boundary"
        item["id"] = "REQ | `id`\n## injected"
        item["title"] = "title | <b>bold</b>\n## injected"
        item["subject"] = "subject | injected"
        item["acceptance_criteria"][0].update(
            {
                "id": "AC | one",
                "given": "given\n## injected",
                "when": "when | value",
                "then": "then `value` <tag>",
            }
        )
        item["traces"] = {
            "design": [],
            "implementation": [],
            "tests": [],
            "standards": ["standard | one", "standard two"],
        }
        specflow.validate_catalog(catalog, trace_root=None)
        rendered = specflow.render(catalog)
        self.assertEqual(rendered.count("<!-- tools/quintflow.pyによる自動生成。"), 1)
        self.assertNotIn("\n## injected", rendered)
        for escaped in ["&#124;", "&#96;", "&lt;script&gt;", "<br>"]:
            self.assertIn(escaped, rendered)
        self.assertIn('要求源(JSON List): <code>[', rendered)
        self.assertIn('参照資料: <code>[', rendered)

        preserve = copy.deepcopy(catalog)
        preserve["requirements"][0]["action"] = "preserve"
        maintain = copy.deepcopy(catalog)
        maintain["requirements"][0]["action"] = "maintain"
        self.assertNotEqual(specflow.render(preserve), specflow.render(maintain))
        self.assertIn('<code>"preserve"</code>', specflow.render(preserve))
        self.assertIn('<code>"maintain"</code>', specflow.render(maintain))

    def test_generate_rejects_input_change_before_atomic_publication(self) -> None:
        with tempfile.TemporaryDirectory(prefix="specflow-generate-", dir=ROOT) as directory:
            fixture = Path(directory)
            spec_path = fixture / "requirements.json"
            output_path = fixture / "requirements.md"
            spec_path.write_text(
                json.dumps(source_catalog(), ensure_ascii=False),
                encoding="utf-8",
            )
            output_path.write_text("old output\n", encoding="utf-8")
            real_atomic_write = specflow.atomic_write_cas

            def mutate_input(*args, **kwargs):
                spec_path.write_text(spec_path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
                return real_atomic_write(*args, **kwargs)

            with mock.patch.object(specflow, "atomic_write_cas", side_effect=mutate_input):
                result = specflow.main(
                    ["generate", "--spec", os.fspath(spec_path), "--out", os.fspath(output_path)]
                )
            self.assertEqual(result, 2)
            self.assertEqual(output_path.read_text(encoding="utf-8"), "old output\n")

    def test_generate_rejects_trace_deletion_or_exchange_before_publication(self) -> None:
        for race in ["delete", "exchange"]:
            with self.subTest(race=race), tempfile.TemporaryDirectory(
                prefix="specflow-trace-race-", dir=ROOT
            ) as directory:
                fixture = Path(directory)
                trace_path = fixture / "trace.py"
                trace_path.write_text("# original trace\n", encoding="utf-8")
                spec_path = fixture / "requirements.json"
                output_path = fixture / "requirements.md"
                catalog = source_catalog()
                catalog["requirements"][0]["traces"]["tests"] = [
                    os.fspath(trace_path.relative_to(ROOT))
                ]
                spec_path.write_text(
                    json.dumps(catalog, ensure_ascii=False),
                    encoding="utf-8",
                )
                output_path.write_text("old output\n", encoding="utf-8")
                real_atomic_write = specflow.atomic_write_cas

                def mutate_trace(*args, **kwargs):
                    trace_path.unlink()
                    if race == "exchange":
                        trace_path.write_text("# replacement trace\n", encoding="utf-8")
                    return real_atomic_write(*args, **kwargs)

                with mock.patch.object(
                    specflow,
                    "atomic_write_cas",
                    side_effect=mutate_trace,
                ):
                    result = specflow.main(
                        [
                            "generate",
                            "--spec",
                            os.fspath(spec_path),
                            "--out",
                            os.fspath(output_path),
                        ]
                    )
                self.assertEqual(result, 2)
                self.assertEqual(output_path.read_text(encoding="utf-8"), "old output\n")

    def test_check_refuses_a_verdict_if_input_changes_during_render(self) -> None:
        with tempfile.TemporaryDirectory(prefix="specflow-check-stable-", dir=ROOT) as directory:
            fixture = Path(directory)
            spec_path = fixture / "requirements.json"
            output_path = fixture / "requirements.md"
            catalog = source_catalog()
            spec_path.write_text(json.dumps(catalog, ensure_ascii=False), encoding="utf-8")
            output_path.write_text(specflow.render(catalog), encoding="utf-8")
            real_render = specflow.render

            def mutate_input(value):
                spec_path.write_text(spec_path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
                return real_render(value)

            with mock.patch.object(specflow, "render", side_effect=mutate_input):
                result = specflow.main(
                    ["check", "--spec", os.fspath(spec_path), "--out", os.fspath(output_path)]
                )
            self.assertEqual(result, 2)


if __name__ == "__main__":
    unittest.main()
