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
            "`direct`と`assured`では、恒久的な`work/<id>/`を作成しない",
            "通常の初回承認を要求せず",
            "`.devflow/run/`",
            "## Regulatedの記録",
        ]:
            self.assertIn(required, reference)

        for legacy in [
            "Create `work/<id>/` with concise Markdown files",
            "If the runtime is absent, create a lightweight work record",
            "Produce one compact authorization package after the requirements are coherent.",
        ]:
            self.assertNotIn(legacy, reference)

    def test_contributing_uses_profile_specific_flow(self) -> None:
        text = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")

        for required in [
            "### 直接実行",
            "### 保証付き実行",
            "### 規制・高保証実行",
            "governance/reviews/<change-id>.yaml",
            "この場合に限り、`tools/devflow.py init`",
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

    def test_historical_work_and_standard_design_paths_are_explained(self) -> None:
        work_readme = (ROOT / "work" / "README.md").read_text(encoding="utf-8")
        root_readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn("分離する前に作成された履歴証跡", work_readme)
        self.assertIn("現行の通常変更で複製するtemplateまたは実装例ではありません", work_readme)
        self.assertIn("導入先repositoryを含む標準配置の契約", root_readme)
        self.assertIn("directoryを存在させるための空file", root_readme)


if __name__ == "__main__":
    unittest.main()
