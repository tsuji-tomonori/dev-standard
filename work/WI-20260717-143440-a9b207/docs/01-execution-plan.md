# 自律実行計画

## 承認対象

- Work item: WI-20260717-143440-a9b207
- タイトル: 永続要件・実装由来設計・標準検証フレームを追加
- 対象プロファイル: CORE, CLOUD-COMMON, AWS-DELTA
- 初回承認者: tsuji-tomonori

この計画は、要件定義およびトレーサビリティと一体で初回承認する。承認後は、記載した権限境界内で追加の工程承認を求めず、完了まで自律実行する。

## 許可する操作

- repository内のspec、generated docs、Skills、tools、schemas、standards registry、manifest、tests、CI、work evidenceの編集
- 公式一次資料のread-only調査、dependency導入、local verification、Git commit、GitHub branch/PR/CI操作

## 許可しない操作

- cloud deploy、database接続、mainへの直接push、PR merge、第三者system変更、秘密情報の取得

## 作業分解

| ID | 作業 | 変更対象 | 検証 | 完了条件 |
|---|---|---|---|---|
| PLAN-001 | 3本柱を正本要件化 | spec/schema/docs | specflow validate/check | 永続要件正本とgenerated docs一致 |
| PLAN-002 | 対話要件保守Skill | Skill/research | quick validation/contract tests | delta作成・適用・収束手順が明確 |
| PLAN-003 | FastAPI/CDK設計生成 | designflow/Skill | AST/OpenAPI/SQL/CFN fixtures | 全指定docsとdigest生成 |
| PLAN-004 | standard verification | registry/standardsflow/Skill | schema/freshness tests | 公式source版・鮮度・証拠規則あり |
| PLAN-005 | 移植・統合 | manifest/README/FLOW/AGENTS | install/repo tests | folder/profile copyで利用可能 |
| PLAN-006 | adversarial review/公開 | tests/work/GitHub | make verify/CI | work closed、ready PR、CI green |

## 外部副作用

| 操作 | 対象 | 影響 | rollback |
|---|---|---|---|
| dependency install | repository-local venv/CI | PyYAML/SQLGlot追加 | requirements revert |
| GitHub PR作成 | tsuji-tomonori/dev-standard | review可能なbranchを公開 | PR close/revert |

## 既定の判断

| 判断点 | 追加確認せず採用する既定値 | 根拠 |
|---|---|---|
| 永続正本形式 | JSON | 標準libraryだけで厳格・決定的に扱える |
| requirement削除 | retired tombstone | ID・判断履歴・traceを失わない |
| docs正本 | machine-readable specのみ | generated docsの二重編集を防ぐ |
| SQL解析 | SQLGlot AST | regexでは構文上のread/writeを保証できない |
| CFN入力 | synth済みYAML/JSON | CDK sourceよりdeployment contractに近い |

## 検証計画

- specflow/designflow/standardsflow unit/integration tests、Skill validation、catalog、repository validator、audit、GitHub Actions。

## 停止条件

- 権限境界外の不可逆操作または外部権限が不可欠になった場合は実行せず、ブロッカーとして記録する。
- 公式sourceまたはdependency取得が不能で決定的な代替がない場合。

## 完了定義

- [ ] REQ-001〜014/NFR-001〜005が直接証拠でPass
- [ ] generated docsが正本・実装から再生成可能でdriftなし
- [ ] work item closed、PR ready、remote CI success
