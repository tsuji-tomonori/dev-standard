# テスト計画

## 品質リスク

confirmation reviewへの退化、single judge bias、unsafe attack instruction、source/rule断線、Skills list drift、existing flow regression。

## テストレベルと責任

| レベル | 対象 | 技法 | 環境 | 実施者 |
|---|---|---|---|---|
| Skill contract | workflow/decision/boundary | required assertions | repository | automation |
| Research trace | sources/findings/rules | source presence/map review | repository/web | automation+manual |
| Catalog | skill directories/table/manifest | set equality | repository | automation |
| Regression | existing governance/chat/install | unit/validator/audit | repository | automation |

## 要求別テスト

| テストID | 要求ID | 条件 | 期待結果 | 自動化 |
|---|---|---|---|---|
| ADV-T1 | ADV-001〜007/N1〜N4 | skill/references contract | threat/oracle/portfolio/artifact/retest/safety terms exist | yes |
| ADV-T2 | ADV-008 | directory/catalog comparison | exact set equality | yes |
| ADV-T3 | ADV-003/N3 | bias rule assertions | order swap、repeat、independent escalation | yes |
| ADV-T4 | all | full verify/skill validate/CI | success | yes |

## セキュリティ・AI評価

AI red-team case generationはauthorized test contextだけ。benign utility、multi-turn、indirect injection、synthetic exfiltration、judge bias controlをrubric化する。

## 完了基準

28 tests、validator、skill quick validation、catalog/audit、CI success。source/rule mapとsafety boundaryに欠落なし。
