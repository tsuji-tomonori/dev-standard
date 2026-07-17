# テスト計画

## 品質リスク

natural-language trigger漏れ、user command転嫁、unsafe bootstrap、runtime欠落停止、既存gate regressionを主要riskとする。

## テストレベルと責任

| レベル | 対象 | 技法 | 環境 | 実施者 |
|---|---|---|---|---|
| Contract | skill/root instruction | required phrase/assertion | repository | automation |
| Installation | chat-first profile | temp target copy | temp directory | automation |
| Regression | governance/skills | unit/catalog/audit | repository | automation |
| Integration | PR/CI | GitHub Actions | remote | automation |

## 要求別テスト

| テストID | 要求ID | 条件 | 期待結果 | 自動化 |
|---|---|---|---|---|
| CHAT-T1 | CHAT-001/003/004 | umbrella skill text | broad trigger、one approval、PR/CI completion | yes |
| CHAT-T2 | CHAT-002/006 | bootstrap reference/root instructions | local-only、no user command、no silent overwrite | yes |
| CHAT-T3 | CHAT-005/N4 | chat-first profile temp apply | two self-starting skillsだけcopy | yes |
| CHAT-T4 | CHAT-007 | full verify/audit | existing gates success | yes |

## セキュリティ・AI評価

authorization非捏造、calibrated clarification、minimal prompt、bounded reviewer modelのexisting testsを継続する。

## 完了基準

25+ tests、validator、catalog、audit、compile、diff check、GitHub Actionsが全て成功しHigh/Critical issueがないこと。
