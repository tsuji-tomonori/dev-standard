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
        standardsflow.freshness(registry, date(2026, 7, 17))
        generated = (ROOT / "docs/standards/SOURCES.md").read_text(encoding="utf-8")
        self.assertEqual(generated, standardsflow.render(registry))
        asset = (ROOT / ".agents/skills/verify-against-engineering-standards/assets/standards.registry.json").read_bytes()
        canonical = (ROOT / "governance/standards/registry.json").read_bytes()
        self.assertEqual(asset, canonical)

    def test_expired_source_blocks_current_best_practice_claim(self) -> None:
        registry = standardsflow.load(ROOT / "governance/standards/registry.json")
        with self.assertRaises(standardsflow.StandardsError):
            standardsflow.freshness(registry, date(2027, 7, 17))

    def test_nonofficial_source_is_rejected(self) -> None:
        value = json.loads((ROOT / "governance/standards/registry.json").read_text(encoding="utf-8"))
        value["sources"][0]["url"] = "https://example.com/swebok"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "registry.json"
            path.write_text(json.dumps(value), encoding="utf-8")
            with self.assertRaises(standardsflow.StandardsError):
                standardsflow.load(path)


if __name__ == "__main__":
    unittest.main()
