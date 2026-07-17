# テスト計画

## 品質リスク

旧security語義の残存、rename漏れ、research-to-rule不整合、配布profile欠落、曖昧な指摘を欠陥扱いすること。

## テストレベルと責任

| レベル | 対象 | 技法 | 環境 | 実施者 |
|---|---|---|---|---|
| contract | Skill/references | required/forbidden terms | local | codex |
| integration | manifest/catalog/install | inventory/copy | temp directory | codex |
| repository | 全体 | catalog/validator/audit | local/CI | codex |

## 要求別テスト

| テストID | 要求ID | 条件 | 期待結果 | 自動化 |
|---|---|---|---|---|
| TEST-001 | REQ-001,003 | required stanceとsecurity固有語彙 | requiredあり/forbiddenなし | yes |
| TEST-002 | REQ-002,004,005 | source/playbook/report assertions | 全対象・規則あり | yes |
| TEST-003 | REQ-006 | install/catalog equality | rename後Skillのみ配布 | yes |

## セキュリティ・AI評価

security testingは非該当。LLM judgeを使う場合の順序交換と独立確認のみ一般的な評価bias対策として残す。

## 完了基準

quick_validate、全unit tests、catalog、validator、audit、GitHub Actionsが成功し、旧名参照がない。
