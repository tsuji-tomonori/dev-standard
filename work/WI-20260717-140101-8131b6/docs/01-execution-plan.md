# 自律実行計画

## 承認対象

- Work item: WI-20260717-140101-8131b6
- タイトル: 敵対的検証Skillを批判的レビューへ再定義
- 対象プロファイル: CORE
- 初回承認者: tsuji-tomonori

この計画は、要件定義およびトレーサビリティと一体で初回承認する。承認後は、記載した権限境界内で追加の工程承認を求めず、完了まで自律実行する。

## 許可する操作

- repository内のSkill、references、manifest、docs、tests、work evidenceの編集
- local verification、Git commit、既存PR branch更新、CI確認、PR説明更新

## 許可しない操作

- PR #3のマージ、mainへの直接push、第三者システムへの攻撃、秘密情報の操作

## 作業分解

| ID | 作業 | 変更対象 | 検証 | 完了条件 |
|---|---|---|---|---|
| PLAN-001 | 語義を研究規則へ変換 | research-basis | source-to-rule review | security red-team依存を除去 |
| PLAN-002 | Skillをadversarial-reviewへ再設計 | .agents/skills | quick_validate/contract tests | 反証レビュー手順が成立 |
| PLAN-003 | 配布と一覧を同期 | manifest/docs/chat-first | install/repo tests | 全参照が一致 |
| PLAN-004 | 検証と公開 | tests/work/PR | make verify/GitHub Actions | CI green、work closed |

## 外部副作用

| 操作 | 対象 | 影響 | rollback |
|---|---|---|---|
| PR branch更新 | GitHub PR #3 | review差分とCIを更新 | 追加commitをrevert |

## 既定の判断

| 判断点 | 追加確認せず採用する既定値 | 根拠 |
|---|---|---|
| Skill名 | `adversarial-review` | セキュリティ意味との混同を避ける |
| レビュー姿勢 | 誤りを作業仮説とするが結論は証拠で決める | 反証性と公平性を両立 |

## 検証計画

- skill quick validation、28+ unit tests、catalog、repository validator、audit、GitHub Actionsを実行する。

## 停止条件

- 権限境界外の不可逆操作または外部権限が不可欠になった場合は実行せず、ブロッカーとして記録する。
- 研究根拠や既存PRの更新権限が利用不能な場合。

## 完了定義

- [ ] REQ-001〜006/NFR-001〜003を満たす
- [ ] work item closed、PR ready、remote CI success
