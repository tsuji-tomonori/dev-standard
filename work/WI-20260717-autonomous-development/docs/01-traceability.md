# 要求トレーサビリティ

## 方針

この文書は、ユーザー要求から要求ID、予定実装、検証、証跡までを追跡する。初回承認時点では実装・テスト列を計画として記載し、工程ごとに実在パスと結果へ更新する。

| 要求ID | ユーザー要望・上位目的 | 予定設計・実装 | 予定検証 | 状態 |
|---|---|---|---|---|
| AUT-001〜AUT-004 | 最初の要件だけ承認 | policy、requirements template、approval digest、harness | requirements gate・digest単体テスト | 承認候補 |
| AUT-005〜AUT-009 | 以降は承認なく最後まで自走 | AGENTS、govern-development-request、advance/audit | 全工程E2E、先行ゲート回帰テスト | 承認候補 |
| AUT-010〜AUT-012 | 安全に自走し文書と実装を一致 | execution plan、schema判定、全ガイド・hooks | 互換性テスト、repo validation、全文検索 | 承認候補 |
| LIS-001〜LIS-004 | 曖昧な意図を融和的に言語化 | calibrated-collaborative-listening/SKILL.md | 曖昧・感情・対立ケースrubric | 承認候補 |
| LIS-005〜LIS-008 | 情報量を落とさず簡潔に核心を示す | semantic protocol、Japanese patterns、rubric | 意味保存圧縮・日本語ケースrubric | 承認候補 |
| NFR-001〜NFR-005 | 品質、監査、安全、保守、互換性 | harness、audit、tests、docs | unittest、make verify、audit | 承認候補 |
| NFR-006〜NFR-008 | skill品質、簡潔性、CI再現性 | skill references、validator、Actions | rubric、quick_validate、GitHub Actions | 承認候補 |

## 完了時に必要な証跡

- 変更ファイルと要求IDの対応表
- 全単体・統合テスト結果
- `make verify` と `python tools/devflow.py audit` の結果
- repo-local skill validation結果
- GitHub Actionsの必須check結果
- PR URL、merge commit、closed work itemの監査結果

## 未接続項目

- なし。実装パスとテストIDは設計工程で確定し、この文書を更新する。
