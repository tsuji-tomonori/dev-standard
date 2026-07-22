from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ProfileBoundaryContractTest(unittest.TestCase):
    def test_chat_first_reference_keeps_ordinary_changes_out_of_work_records(self) -> None:
        reference = (
            ROOT
            / ".agents"
            / "skills"
            / "chat-first-development"
            / "references"
            / "bootstrap-and-conversation.md"
        ).read_text(encoding="utf-8")

        for required in [
            "# 開発開始と対話の契約",
            "`direct`と`assured`では、恒久的な`work/<id>/`を作成しない",
            "通常の初回承認を要求せず",
            "`.devflow/run/`",
            "## Regulatedの記録",
            "AIが安全にsetupを修復できる場合",
            "明示的な権限なしにmergeしない",
        ]:
            self.assertIn(required, reference)

        for legacy in [
            "# Bootstrap and conversation contract",
            "Create `work/<id>/` with concise Markdown files",
            "If the runtime is absent, create a lightweight work record",
            "Produce one compact authorization package after the requirements are coherent.",
            "Do not stop",
            "Do not merge unless explicitly authorized.",
            "Lightweight record",
        ]:
            self.assertNotIn(legacy, reference)

    def test_contributing_uses_profile_specific_flow(self) -> None:
        text = (ROOT / ".github" / "CONTRIBUTING.md").read_text(encoding="utf-8")

        for required in [
            "`direct`、`assured`、`regulated`",
            "governance/reviews/<change-id>.yaml",
            "公開API",
            "authority boundary",
        ]:
            self.assertIn(required, text)

        self.assertNotIn("1. `tools/devflow.py init`でwork itemを作成する。", text)

    def test_pull_request_template_makes_regulated_fields_conditional(self) -> None:
        text = (ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md").read_text(encoding="utf-8")

        self.assertIn("## 変更証跡", text)
        self.assertIn("Review YAML: `governance/reviews/<change-id>.yaml`", text)
        self.assertIn("## Regulatedの場合のみ", text)
        self.assertFalse(text.lstrip().startswith("## Work item"))
        self.assertLess(text.index("## 変更証跡"), text.index("## Regulatedの場合のみ"))

    def test_reference_repository_explains_current_state_without_history(self) -> None:
        root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
        development = (ROOT / "docs" / "reference" / "development.md").read_text(encoding="utf-8")

        self.assertFalse((ROOT / "work").exists())
        self.assertIn("docs/design/generated/", development)
        self.assertIn("同じ現在状態", (ROOT / "AGENTS.md").read_text(encoding="utf-8"))
        self.assertNotIn("過去案件", root_readme)
        self.assertNotIn("旧work", root_readme + development)


if __name__ == "__main__":
    unittest.main()
