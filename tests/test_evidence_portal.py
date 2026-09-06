"""共通reportの失敗表示・安全な公開範囲・runner間の変換を検証する。"""

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / ".agents/skills/inspect-quality-gates/scripts"


def module(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


evidence = module("evidence")
adapter = module("test_evidence")


def fixture():
    data = {"schemaVersion": 1, "revision": "abc", "runId": "1", "generatedAt": "2026-09-06"}
    data.update({key: {"applicable": False, "reason": "fixture対象外", "items": []}
                 for key in evidence.CATEGORIES})
    data["tests"] = {"applicable": True, "inventory": ["unit::境界"], "items": [
        {"id": "unit::境界", "name": "境界を検証", "group": "unit", "status": "failed"}]}
    return data


class EvidenceTests(unittest.TestCase):
    def test_failed_build_can_publish_unavailable_evidence(self):
        data = fixture()
        for name in ("coverage", "design"):
            data[name] = {"applicable": True, "items": [
                {"id": name, "name": name, "status": "missing", "detail": "計測commandが失敗"}]}
        evidence.validate(data, "abc")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            evidence.render(data, root, root / "site")
            self.assertIn("未測定", (root / "site/coverage.html").read_text())
            self.assertIn("missing", (root / "site/index.html").read_text())

    def test_cli_check_rejects_drift_without_repairing(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            manifest = root / "evidence.json"
            manifest.write_text(json.dumps(fixture()))
            output = root / "site"
            args = [sys.executable, str(SCRIPTS / "evidence.py"), "build", "--manifest",
                    str(manifest), "--revision", "abc", "--output", str(output)]
            subprocess.run(args, check=True, capture_output=True)
            args[2] = "check"
            subprocess.run(args, check=True, capture_output=True)
            (output / "tests.html").write_text("drift")
            self.assertNotEqual(subprocess.run(args, capture_output=True).returncode, 0)
            self.assertEqual((output / "tests.html").read_text(), "drift")
            args[2] = "build"
            self.assertNotEqual(subprocess.run(args, capture_output=True).returncode, 0)
            self.assertEqual((output / "tests.html").read_text(), "drift")

    def test_design_base_links_and_allowlist(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "design").mkdir()
            (root / "design/index.html").write_text('<a href="/repo/design/chapter.html">章</a>')
            (root / "design/chapter.html").write_text('<h1>設計</h1>')
            data = fixture()
            data["siteBase"] = "/repo/"
            data["design"] = {"applicable": True, "items": [
                {"id": "docs", "name": "設計", "status": "passed", "path": "design/index.html"}],
                "files": ["design/index.html", "design/chapter.html"]}
            evidence.validate(data, "abc")
            evidence.render(data, root, root / "good")
            data["design"]["files"].remove("design/chapter.html")
            with self.assertRaisesRegex(ValueError, "broken internal link"):
                evidence.render(data, root, root / "broken")

    def test_missing_stale_inventory_and_coverage_are_rejected(self):
        for mutate in (
            lambda d: d.update(revision="old"),
            lambda d: d["tests"].update(items=[]),
            lambda d: d["tests"].update(inventory=[]),
            lambda d: d["e2e"].update(reason=""),
            lambda d: d.update(coverage={"applicable": True, "items": [
                {"id": "c", "name": "c", "status": "passed", "tool": "x",
                 "metric": "lines", "covered": 2, "total": 1}]}),
        ):
            data = fixture()
            mutate(data)
            with self.assertRaises(ValueError):
                evidence.validate(data, "abc")

    def test_failed_result_deterministic_and_no_unlisted_data(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "private.log").write_text("SECRET")
            data = fixture()
            data["tests"]["items"][0]["detail"] = '<script>alert("x")</script>'
            evidence.validate(data, "abc")
            evidence.render(data, root, root / "one")
            evidence.render(data, root, root / "two")
            self.assertIn("failed", (root / "one/index.html").read_text())
            self.assertIn("&lt;script&gt;", (root / "one/tests.html").read_text())
            self.assertFalse((root / "one/private.log").exists())
            for path in (root / "one").rglob("*"):
                if path.is_file():
                    self.assertEqual(path.read_bytes(), (root / "two" / path.relative_to(root / "one")).read_bytes())

    def test_gwt_and_path_boundary(self):
        data = fixture()
        data["e2e"] = copy.deepcopy(data["tests"])
        data["e2e"]["items"][0]["status"] = "passed"
        with self.assertRaises(ValueError):
            evidence.validate(data, "abc")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "real").write_text("x")
            (root / "link").symlink_to(root / "real")
            for name in ("../secret", "/etc/passwd", "link"):
                with self.assertRaises(ValueError):
                    evidence.source(root, name)

    def test_two_runner_adapters_preserve_missing_and_failure(self):
        inventory = [{"id": "u::a", "name": "正常系", "group": "u"},
                     {"id": "u::b", "name": "未実行", "group": "u"}]
        junit = '<testsuite><testcase classname="u" name="a"><failure>PRIVATE LOG</failure></testcase></testsuite>'
        vitest = json.dumps({"testResults": [{"name": "u", "assertionResults": [
            {"fullName": "a", "status": "failed", "failureMessages": ["PRIVATE LOG"]}]}]})
        for kind, raw in (("junit", junit), ("vitest", vitest)):
            result = adapter.convert(kind, raw, inventory)
            self.assertEqual([x["status"] for x in result["items"]], ["failed", "not-run"])
            self.assertNotIn("PRIVATE LOG", json.dumps(result))
            data = fixture()
            data["tests"] = result
            evidence.validate(data, "abc")
        with self.assertRaises(ValueError):
            adapter.convert("junit", junit, [])
        with self.assertRaises(ValueError):
            adapter.convert("junit", '<!DOCTYPE x><testsuite/>', inventory)


if __name__ == "__main__":
    unittest.main()
