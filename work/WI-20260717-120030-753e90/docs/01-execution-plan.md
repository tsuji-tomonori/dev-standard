# 自律実行計画

## 承認対象

- Work item: WI-20260717-120030-753e90
- タイトル: Chat-first zero-setup autonomous development
- 対象プロファイル: CORE, AI-CONDITIONAL
- 初回承認者: requester（本依頼）

この計画は、要件定義およびトレーサビリティと一体で初回承認する。承認後は、記載した権限境界内で追加の工程承認を求めず、完了まで自律実行する。

## 許可する操作

- root/skill/docs/distribution/tests/work evidenceの編集
- AI内部でのdependency setup、devflow実行、local verification
- feature branch commit、remote branch、PR、CI確認、PR metadata/comment更新

## 許可しない操作

- targetの既存active config/instructionsのsilent overwrite
- global/home install、production deploy、PR merge、secret操作
- single initial authorizationの廃止またはAIによる捏造

## 作業分解

| ID | 作業 | 変更対象 | 検証 | 完了条件 |
|---|---|---|---|---|
| PLAN-001 | chat-first UX contract | AGENTS, umbrella skill | content tests | natural-language trigger明記 |
| PLAN-002 | automatic bootstrap contract | skill reference, snippets | safety/static tests | AI ownership/stop rule明記 |
| PLAN-003 | copy-only quick start | README, INSTALLATION, manifest | validator | command不要の利用手順 |
| PLAN-004 | lifecycle integration | existing skills/docs | regression/audit | approval後PRまで自走 |
| PLAN-005 | publication | tests, work, GitHub | local/CI | ready PR、green CI、closed WI |

## 外部副作用

| 操作 | 対象 | 影響 | rollback |
|---|---|---|---|
| remote branch/PR | GitHub repository | reviewable change追加 | commit revert/PR close |
| dependency install | target-local environment | local cache/venv更新 | recreate/remove local environment |

## 既定の判断

| 判断点 | 追加確認せず採用する既定値 | 根拠 |
|---|---|---|
| 曖昧な実装詳細 | reversibleで最小の妥当案をAIが選ぶ | 質問負荷を下げる |
| bootstrap | repository-localのみ自動実行 | target/global stateを保護する |
| user interaction | 初回の自然言語承認以外は結果・blockerだけ | chat-first要件 |

## 検証計画

- skill/instruction contract tests、manifest/guide validator、23+ regression tests、catalog、audit、compile、GitHub Actions。

## 停止条件

- 権限境界外の不可逆操作または外部権限が不可欠になった場合は実行せず、ブロッカーとして記録する。
- copy元assetが不足し自己完結できない、またはGitHub write権限がない場合は具体的blockerを報告する。

## 完了定義

- [ ] CHAT-001〜007、CHAT-N1〜N4が証跡付きでpass
- [ ] user-facing quick startにPython commandがない
- [ ] PRがready/mergeable、CI success、work item closed
