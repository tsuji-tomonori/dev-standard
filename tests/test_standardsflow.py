from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module():
    path = ROOT / ".agents/skills/verify-against-engineering-standards/scripts/standardsflow.py"
    spec = importlib.util.spec_from_file_location("standardsflow", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


standardsflow = load_module()


class StandardsflowTest(unittest.TestCase):
    def test_self_hosted_registry_is_valid_fresh_and_generated(self) -> None:
        registry = standardsflow.load(ROOT / "governance/standards/registry.json")
        standardsflow.freshness(registry, date(2026, 7, 21))
        generated = (ROOT / "docs/standards/SOURCES.md").read_text(encoding="utf-8")
        self.assertEqual(generated, standardsflow.render(registry))
        asset = (ROOT / ".agents/skills/verify-against-engineering-standards/assets/standards.registry.json").read_bytes()
        canonical = (ROOT / "governance/standards/registry.json").read_bytes()
        self.assertEqual(asset, canonical)
        by_id = {source["id"]: source for source in registry["sources"]}
        self.assertEqual(by_id["SWEBOK-V4A"]["version"], "4.0a / 2025-09")
        self.assertEqual(
            by_id["SWEBOK-V4A"]["artifact_sha256"],
            "b3cb8028fecb9607f757504c861947fa3bf423087ea8bf08c58020f0ba3596dc",
        )
        self.assertTrue({"AWS-GENAI-LENS", "AWS-RAI-LENS", "AWS-ML-LENS", "AWS-AGENTIC-LENS"} <= set(by_id))
        self.assertEqual(by_id["DEVSTD-AS-BUILT"]["authority"], "dev-standard maintainers")
        standard = ROOT / "docs" / "standards" / "AS-BUILT-DESIGN.md"
        self.assertEqual(by_id["DEVSTD-AS-BUILT"]["artifact_sha256"], hashlib.sha256(standard.read_bytes()).hexdigest())

    def test_aws_cdk_as_built_standard_is_registered_and_mapped(self) -> None:
        registry = standardsflow.load(ROOT / "governance/standards/registry.json")
        by_id = {source["id"]: source for source in registry["sources"]}
        standard = ROOT / "docs" / "standards" / "AWS-CDK-AS-BUILT-DESIGN.md"
        self.assertEqual(
            by_id["DEVSTD-AWS-CDK-AS-BUILT"]["artifact_sha256"],
            hashlib.sha256(standard.read_bytes()).hexdigest(),
        )
        content = standard.read_text(encoding="utf-8")
        selection = (
            ROOT
            / ".agents"
            / "skills"
            / "verify-against-engineering-standards"
            / "references"
            / "as-built-design-check-selection.md"
        ).read_text(encoding="utf-8")
        for required in [
            "docs/design/generated/cdk/",
            "synthesized template",
            "CDK-DO-020",
            "CDK-DO-033",
            "CDK-DO-047",
            "IMP-009",
            "FAST-006",
            "FAST-012",
            "AUD-008",
        ]:
            self.assertIn(required, content)
        for required in ["AWS-CDK-AS-BUILT-DESIGN.md", "IMP-009", "FAST-012", "FAST-023"]:
            self.assertIn(required, selection)

    def test_expired_source_blocks_current_best_practice_claim(self) -> None:
        registry = standardsflow.load(ROOT / "governance/standards/registry.json")
        with self.assertRaises(standardsflow.StandardsError):
            standardsflow.freshness(registry, date(2027, 7, 18))

    def test_nonofficial_source_is_rejected(self) -> None:
        value = json.loads((ROOT / "governance/standards/registry.json").read_text(encoding="utf-8"))
        value["sources"][0]["url"] = "https://example.com/swebok"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "registry.json"
            path.write_text(json.dumps(value), encoding="utf-8")
            with self.assertRaises(standardsflow.StandardsError):
                standardsflow.load(path)

    def test_repository_owned_source_requires_canonical_url_and_hash(self) -> None:
        value = json.loads((ROOT / "governance/standards/registry.json").read_text(encoding="utf-8"))
        owned = next(source for source in value["sources"] if source["id"] == "DEVSTD-AS-BUILT")
        owned["url"] = "https://github.com/another-owner/another-repo/blob/main/standard.md"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "registry.json"
            path.write_text(json.dumps(value), encoding="utf-8")
            with self.assertRaises(standardsflow.StandardsError):
                standardsflow.load(path)

        value = json.loads((ROOT / "governance/standards/registry.json").read_text(encoding="utf-8"))
        owned = next(source for source in value["sources"] if source["id"] == "DEVSTD-AS-BUILT")
        owned["artifact_sha256"] = None
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "registry.json"
            path.write_text(json.dumps(value), encoding="utf-8")
            with self.assertRaises(standardsflow.StandardsError):
                standardsflow.load(path)

    def test_missing_scope_or_invalid_artifact_hash_is_rejected(self) -> None:
        value = json.loads((ROOT / "governance/standards/registry.json").read_text(encoding="utf-8"))
        value["sources"][0].pop("scope")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "registry.json"
            path.write_text(json.dumps(value), encoding="utf-8")
            with self.assertRaises(standardsflow.StandardsError):
                standardsflow.load(path)

        value = json.loads((ROOT / "governance/standards/registry.json").read_text(encoding="utf-8"))
        value["sources"][0]["artifact_sha256"] = "not-a-hash"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "registry.json"
            path.write_text(json.dumps(value), encoding="utf-8")
            with self.assertRaises(standardsflow.StandardsError):
                standardsflow.load(path)


if __name__ == "__main__":
    unittest.main()
