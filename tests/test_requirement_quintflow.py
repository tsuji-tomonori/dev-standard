from __future__ import annotations

import subprocess
import unittest
from pathlib import Path
from unittest import mock

from tools import quintflow


class RequirementQuintflowTest(unittest.TestCase):
    def test_generation_read_set_covers_formal_sources_skill_payloads_and_traces(self) -> None:
        outputs = {
            quintflow.REQUIREMENTS_JSON,
            quintflow.REQUIREMENTS_DOC,
            quintflow.SKILLS_JSON,
            quintflow.SKILLS_DOC,
            *quintflow.SKILLS_ROOT.glob("*/SKILL.md"),
        }
        catalog = {
            "requirements": [
                {
                    "traces": {
                        "design": ["README.md"],
                        "implementation": ["tools/quintflow.py"],
                        "tests": ["tests/test_requirement_quintflow.py"],
                        "standards": ["QUINT-0.32"],
                    }
                }
            ]
        }
        traces = quintflow.requirement_trace_paths(catalog)
        read_set = set(quintflow.generation_read_paths(outputs, traces))
        self.assertTrue(
            {
                quintflow.REQUIREMENTS_QNT,
                quintflow.REQUIREMENTS_TEMPLATE_QNT,
                quintflow.SKILLS_QNT,
                quintflow.ROOT / "README.md",
                *quintflow.GENERATOR_IMPLEMENTATION_INPUTS,
            }.issubset(read_set)
        )
        for path in quintflow.SKILLS_ROOT.rglob("*"):
            if path.is_file() and path not in outputs and path.suffix != ".pyc":
                with self.subTest(skill_input=path.relative_to(quintflow.ROOT)):
                    self.assertIn(path, read_set)
        self.assertEqual(
            set(quintflow.SKILLS_ROOT.glob("*/SKILL.md")),
            {path for path in outputs if path.name == "SKILL.md"},
        )

    def test_generate_passes_trace_inputs_as_read_only_preconditions(self) -> None:
        requirements = {
            "requirements": [
                {
                    "traces": {
                        "design": ["README.md"],
                        "implementation": [],
                        "tests": [],
                        "standards": [],
                    }
                }
            ]
        }
        skills = {"contracts": []}
        outputs = {
            quintflow.REQUIREMENTS_JSON: '{"requirements": []}',
            quintflow.REQUIREMENTS_DOC: "requirements\n",
            quintflow.SKILLS_JSON: '{"contracts": []}',
            quintflow.SKILLS_DOC: "skills\n",
        }
        specflow = mock.Mock()
        with mock.patch.object(quintflow, "snapshot_file_pinned", return_value=mock.sentinel.snapshot), mock.patch.object(
            quintflow, "extract_requirements", return_value=requirements
        ), mock.patch.object(quintflow, "extract_skills", return_value=skills), mock.patch.object(
            quintflow, "load_specflow", return_value=specflow
        ), mock.patch.object(quintflow, "typecheck"), mock.patch.object(
            quintflow, "verify_requirement_catalog_invariants"
        ), mock.patch.object(quintflow, "derived_outputs", return_value=outputs), mock.patch.object(
            quintflow, "verify_skill_coverage"
        ), mock.patch.object(quintflow, "verify_requirement_skill_traces"), mock.patch.object(
            quintflow, "atomic_batch_write_cas"
        ) as publish:
            quintflow.generate()
        read_preconditions = publish.call_args.kwargs["read_preconditions"]
        self.assertIn(quintflow.ROOT / "README.md", read_preconditions)
        self.assertNotIn(quintflow.REQUIREMENTS_JSON, read_preconditions)
        self.assertIn(quintflow.REQUIREMENTS_QNT, read_preconditions)

    def test_check_rejects_qnt_or_trace_change_after_validation(self) -> None:
        requirements = {
            "requirements": [
                {
                    "traces": {
                        "design": ["README.md"],
                        "implementation": [],
                        "tests": [],
                        "standards": [],
                    }
                }
            ]
        }
        skills = {"contracts": []}
        outputs = {
            quintflow.REQUIREMENTS_JSON: '{"requirements": []}',
            quintflow.REQUIREMENTS_DOC: "requirements\n",
            quintflow.SKILLS_JSON: '{"contracts": []}',
            quintflow.SKILLS_DOC: "skills\n",
        }
        for race_path in [quintflow.REQUIREMENTS_QNT, quintflow.ROOT / "README.md"]:
            with self.subTest(race_path=race_path.relative_to(quintflow.ROOT)):
                observations: dict[Path, int] = {}

                def snapshot(path: Path, **_: object) -> object:
                    observations[path] = observations.get(path, 0) + 1
                    if path == race_path and observations[path] > 1:
                        return mock.sentinel.changed
                    return mock.sentinel.before

                def read_output(path: Path, **_: object) -> bytes:
                    return outputs[path].encode("utf-8")

                specflow = mock.Mock()
                with mock.patch.object(
                    quintflow,
                    "snapshot_file_pinned",
                    side_effect=snapshot,
                ), mock.patch.object(
                    quintflow, "read_bytes_nofollow_pinned", side_effect=read_output
                ), mock.patch.object(
                    quintflow, "extract_requirements", return_value=requirements
                ), mock.patch.object(
                    quintflow, "extract_skills", return_value=skills
                ), mock.patch.object(
                    quintflow, "load_specflow", return_value=specflow
                ), mock.patch.object(quintflow, "typecheck"), mock.patch.object(
                    quintflow, "verify_requirement_catalog_invariants"
                ), mock.patch.object(
                    quintflow, "derived_outputs", return_value=outputs
                ), mock.patch.object(quintflow, "verify_skill_coverage"), mock.patch.object(
                    quintflow, "verify_requirement_skill_traces"
                ):
                    with self.assertRaisesRegex(
                        quintflow.QuintFlowError,
                        "generation read-set changed during check",
                    ):
                        quintflow.check()

    def test_catalog_invariants_are_checked_for_authority_and_template(self) -> None:
        with mock.patch.object(quintflow, "quint") as invoke:
            quintflow.verify_requirement_catalog_invariants()
        self.assertEqual(2, invoke.call_count)
        paths = [call.args[1] for call in invoke.call_args_list]
        self.assertEqual(
            [
                "spec/requirements/requirements.qnt",
                ".agents/skills/maintain-canonical-requirements/assets/requirements.template.qnt",
            ],
            paths,
        )
        for call in invoke.call_args_list:
            self.assertIn("catalogWellFormed", call.args)
            self.assertIn("lifecycleRefinesCatalog", call.args)
            self.assertTrue(call.kwargs["capture"])

    def test_apalache_failure_retains_output_file_diagnostic(self) -> None:
        def fail(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
            output_arg = next(value for value in command if value.startswith("--out="))
            Path(output_arg.removeprefix("--out=")).write_text(
                '{"status":"violation","message":"catalog refinement failed"}',
                encoding="utf-8",
            )
            return subprocess.CompletedProcess(command, 1, stdout="checker failed", stderr="")

        with mock.patch.object(quintflow, "QUINT", Path(__file__)), mock.patch(
            "tools.quintflow.subprocess.run", side_effect=fail
        ):
            with self.assertRaisesRegex(
                quintflow.QuintFlowError, "catalog refinement failed"
            ):
                quintflow.verify_with_apalache(
                    quintflow.REQUIREMENTS_QNT,
                    quintflow.REQUIREMENT_INVARIANTS,
                    max_steps=4,
                )

    def test_verify_covers_requirements_and_skills_models(self) -> None:
        with mock.patch.object(quintflow, "test"), mock.patch.object(
            quintflow, "verify_with_apalache"
        ) as verify:
            quintflow.verify()
        self.assertEqual(
            [
                mock.call(
                    quintflow.REQUIREMENTS_QNT,
                    quintflow.REQUIREMENT_INVARIANTS,
                    max_steps=4,
                ),
                mock.call(
                    quintflow.REQUIREMENTS_TEMPLATE_QNT,
                    quintflow.REQUIREMENT_INVARIANTS,
                    max_steps=4,
                ),
                mock.call(quintflow.SKILLS_QNT, quintflow.SKILL_INVARIANTS, max_steps=3),
            ],
            verify.call_args_list,
        )


if __name__ == "__main__":
    unittest.main()
