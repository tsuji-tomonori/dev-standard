# 実装・構成管理記録

## 変更概要

workflow schema 2を導入し、requirements/requesterの初回承認だけを人の工程判断とした。後続advanceとauditは、全先行gateと初回承認を現在の成果物で再検査する。repo-local傾聴skill、初回承認skill、実行計画template、文書、hooks、validator、testsを同じモデルへ更新した。

## 要求・設計との対応

| 変更 | 要求ID | 実装 | テスト・証跡 | commit方針 |
|---|---|---|---|---|
| 初回承認policy | AUT-002〜AUT-005 | `governance/policy.json`, `docs/templates/01-execution-plan.md` | policy validator、authorization test | governance実装commit |
| workflow schema・migration | AUT-006, AUT-007, AUT-011 | `tools/devflow.py` | legacy migration、prior gate recheck | governance実装commit |
| 後続Failのblocking | AUT-005, NFR-001 | `tools/devflow.py` | fail remains blocking test | governance実装commit |
| autonomous instructions | AUT-008〜AUT-012 | `AGENTS.md`, README、FLOW、GOVERNANCE、hooks、skills | repo validator、旧指示検索 | governance文書commit |
| 改善候補の非自動適用 | AUT-010 | `tools/devflow.py`, Stop hook, retrospective skill | pending proposal test | governance実装commit |
| 協働的傾聴skill | LIS-001〜LIS-008 | `.agents/skills/calibrated-collaborative-listening/**` | quick_validate、rubric評価 | skill commit |
| 初回承認skill | AUT-003〜AUT-005 | `.agents/skills/authorize-autonomous-execution/**` | quick_validate、repo validator | skill commit |
| 回帰・統合test | NFR-001〜NFR-005, NFR-008 | `tests/test_devflow.py`, `tools/validate_repo.py` | unittest、make verify、GitHub Actions | test commitまたは実装commitに同梱 |

## 主な実装詳細

- `require_current_workflow`はstateとpolicy schemaの不一致を具体的エラーにする。
- `authorization_definition`はpolicyの単一承認phase/roleを検証する。
- `preceding_phase_reports`はphase_orderの先行工程を現在のdigestで再計算する。
- `authorize`はphaseとroleを利用者入力にせず、requirements/requesterへ固定する。
- `cmd_approve`はcurrent phaseがrequirementsでない場合を拒否する。
- `cmd_migrate`はintake/requirementsの旧itemだけを明示移行し、旧承認を再利用しない。
- schema 2のFailはexceptionがあっても`CHECK_FAIL_BLOCKING`となる。
- automatic improvement apply functionsとcommandsを削除した。
- repo validatorは他phaseの承認、execution-plan欠落、期待skill欠落を検出する。

## 構成管理

- 構成item: policy、harness、tests、templates、repo instructions、hooks、custom agents、repo-local skills、work item成果物。
- 正本: Gitの追跡fileとGitHub main。work item ID、要求ID、commit、PRで変更を追跡する。
- branch: mainを起点とする短命feature branch。agent向け命名へ統一し、squash merge後に削除する。
- merge条件: local verify成功、GitHub Actions成功、conflictなし、秘密情報なし、初回承認と全先行gateが有効。
- commit: 日本語gitmoji規約に従い、governance実装、skill、work item証跡を目的別に分ける。
- baseline: merge commitを一意なbaselineとし、Git object hashから全SCI revisionを再現する。
- rollback: main上の重大回帰は専用revert PRで打ち消し、同じ品質gateを通す。
- status: `state.json`、inspection reports、events、approvals、Git status、PR checksで記録する。
- audit: `make verify`と`devflow audit`をmerge前後に実行する。

本変更はsource-onlyで、package、container、artifact repository、versioned customer release、複数environmentへのdeploymentを持たない。Git commitとPRが配布単位である。

## セキュア実装・依存関係

新しい外部依存は追加していない。既存Python標準ライブラリ、openpyxl、GitHub Actions構成を維持した。JSON stateは原子的置換、events/approvalsはappend-only hash chainを継続する。秘密情報、個人データ、本番data、非公開transcriptを含めていない。

## 設計との差異

設計との差異はない。互換性のため旧`approve` commandをaliasとして残したが、schema 2では単一requirements authorization以外を拒否するため、要求の承認回数を増やさない。

## 実行したローカル検査

- unittest 10件: 成功
- repository validator: 成功
- `calibrated-collaborative-listening` quick validation: 成功
- `authorize-autonomous-execution` quick validation: 成功
- audit: 成功

最終`make verify`、full diff、GitHub Actionsはverification/release工程で記録する。
