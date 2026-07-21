# 成果物とチェックのライフサイクル

## 1. 基本原則

開発時に生成する情報を、次の3種類へ分離する。

1. **現在状態の正本**: 今後も最新状態を維持する。
2. **変更時点の証跡**: その変更を説明・監査するため固定し、後から書き換えない。
3. **一時実行状態**: 作業再開にだけ使い、完了後に削除する。

このsample / reference repositoryではtop-levelの`work/<id>/`を使用しない。一時状態が必要な場合だけ、gitignoreされた`.devflow/run/`を使用する。

regulated runtimeの実装、template、schema、validatorはportable assetである。liveなwork itemは導入先repositoryで生成し、このrepositoryの履歴sampleとして残さない。

## 2. 要件とdocumentation

永続要件は、[要件分類標準](standards/REQUIREMENT-CLASSIFICATION.md)に従って`product` / `project`、`functional` / `nonfunctional`を判定する。

文書の存在、内容、品質、更新、配布、廃止は原則`project / nonfunctional`として管理する。文書fileは要件の実現手段または生成表示であり、要件正本ではない。

恒久文書には対応するproject NFRから次が到達できる必要がある。

- audience
- purpose
- authority
- update trigger
- verification
- maintenance rule
- retirement condition

工程があるという理由だけで文書を作らない。

## 3. すべての変更で必ず残すもの

### 3.1 実際の成果物

コード、設定、テスト、migration、要件正本、生成設計、project NFRにより必要な運用・保守文書など、依頼された変更そのもの。

### 3.2 コミットコメント

正式にはGitのcommit messageである。Change ManifestとRequirement / Design Impactの独立ファイルを作らず、コミット本文へ次を記録する。

- 目的
- 変更内容
- 要件影響
- 設計影響
- チェックリスト結果のパス
- 検証契約
- 互換性と残存リスク

Commit Commentは変更時点の証跡であり、コミット後にメンテナンスしない。訂正は新しいコミットで行う。

### 3.3 レビュー用チェック結果

選択されたチェック結果だけを`governance/reviews/<change-id>.yaml`へ保存する。

check定義の唯一の機械可読正本は`governance/checks/catalog.yaml`とする。Excelはカタログから生成する一覧・検討用の派生表示であり、ID、class、timing、trigger、合格条件の判定には使用しない。

- 未選択項目をN/Aとして保存しない。
- N/Aは、選択後の詳細確認で適用外と判明した場合だけ使う。
- CIログ、テスト件数、coverage全文は保存しない。
- `Invariant`、`Risk-selected`、`Advisory`を区別する。

このファイルも変更時点の証跡であり、後から最新化しない。誤りが判明した場合は新しいコミットで訂正履歴を残す。

### 3.4 CI結果

単体テスト、build、lint、type check、security scan、coverage、deployment結果の正本はGitHub Actionsなどの外部サービスとする。

リポジトリには次だけを残す。

- CI workflow定義
- テストコードとsynthetic test data
- Commit Commentに記載した検証契約
- レビュー結果YAMLに記載したcheck名または証拠参照

生ログや実行結果の複製は保存しない。

## 4. 条件付きで維持する正本

| 成果物 | 更新条件 | 維持方法 |
|---|---|---|
| `spec/requirements/requirements.json` | product behavior、project constraint、受入条件、非機能閾値、権限要求が変わる | add / update / retireで最新状態を維持 |
| `docs/requirements/REQUIREMENTS.md` | 要件正本が変わる | 正本から自動生成し、直接編集しない |
| `docs/standards/REQUIREMENT-CLASSIFICATION.md` | product / project、functional / nonfunctional、documentation NFRの判断規則が変わる | 人向け標準として維持し、個々の要件は正本へ置く |
| `docs/design/generated/` | 対応する実装、OpenAPI、SQL、CloudFormation、型・route等が変わる | 実装から再生成し、driftをCIで拒否 |
| `docs/standards/AS-BUILT-DESIGN.md` | as-built生成・実装・テスト規約またはcheck選択基準が変わる | 人向け標準として維持し、機械可読な強制度・triggerはcheck catalogへ置く |
| `docs/decisions/ADR-*.md` | 将来を制約し、コードだけでは理由が分からない判断を行う | 本文を上書きせず、accepted / superseded / deprecatedを管理 |
| 運用・保守・documentation | 対応するproject NFRのtriggerが成立する | audience、authority、verification、retirementを保った既存正本を更新 |
| Issue | 将来作業、未解決欠陥、持越すAdvisoryがある | 完了または取消まで維持 |

## 5. 保存しないもの

次の変更ごとの文書は既定では生成しない。

- 要求原文の複製
- 要件差分の適用後コピー
- 手書きトレーサビリティ表
- Git管理された実行計画
- 変更ごとのアーキテクチャ文書
- 手書き詳細設計
- 手書きテスト計画
- implementation log
- test report
- security review report
- release report
- 毎変更のretrospective
- repository固有のlive work item

必要な情報は、要件正本、生成設計、ADR、Commit Comment、レビュー結果、Git差分、PR、CI、Issueのいずれかへ収束させる。

## 6. 実行プロファイル

### 直接実行（direct）

局所的で可逆、外部副作用がない変更。対象テストと変更範囲の静的検査を行う。

### 保証付き実行（assured）

複数モジュール、公開API、DB、IaC、依存、共有UI、governance、distributionなど。変更固有のRisk-selected checkと、必要時だけ独立レビューを追加する。

### 規制・高保証実行（regulated）

認証・認可、個人情報、データ損失、productionの不可逆操作、法令・契約上の統制、高額操作など。導入先ではwork item、初回承認、hash chain、工程監査を追加できる。

この参照repositoryではportable runtimeだけを維持し、live work itemは保存しない。

## 7. チェックのタイミング

### 変更開始前: Impact Check

要件scope/category、設計、公開契約、distribution、DB、認証・認可、外部副作用、不可逆性を判定し、profileとselected checkを決める。

### 実装中: Fast Feedback Check

変更スライスごとに、targeted test、build、lint、type check、生成物drift、work境界、manifest整合などの自動検査を実行する。

### PR作成前: Affected-scope Check

要件・設計影響、documentation lifecycle、受入条件、変更範囲、互換性、選択チェック、残存リスクをレビューし、結果YAMLを保存する。

### Merge前: Revision Integrity Check

現在HEADに対するCI、生成物、blocking check、Commit Comment、権限境界を確認する。設計レビューを最初から繰り返さない。

### Deploy後: Operational Check

production deploy、migration、外部連携、データ変更がある導入先だけで、smoke test、主要指標、rollback可否を外部サービスで確認する。

### 定期: Governance Audit

false blocker、escaped defect、selector miss、Skill競合、不要成果物、repository固有workの再混入、標準出典の陳腐化、実行コストを月次またはリリース単位で確認する。

## 8. チェックの強制度

- **Invariant**: triggerに該当した場合は必ずPassが必要。
- **Risk-selected**: 変更リスクから選択された場合だけblocking。
- **Advisory**: 修正、Issue化、または残存リスクとして明示できる。
- **Periodic**: 個々のPRではなく定期監査で扱う。

`governance/reviews/validate.py`で、schema、catalog ID/class、blocking fail、Advisory処理、証拠参照、Commit Comment、現在HEADとの対応をCI検査する。
