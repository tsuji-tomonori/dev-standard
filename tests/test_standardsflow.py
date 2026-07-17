from __future__ import annotations

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
        standardsflow.freshness(registry, date(2026, 7, 18))
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
