# 成果物とチェックのライフサイクル

## 1. 基本原則

開発時に生成する情報を、次の3種類へ分離する。

1. **現在状態の正本**: 今後も最新状態を維持する。
2. **変更時点の証跡**: その変更を説明・監査するため固定し、後から書き換えない。
3. **一時実行状態**: 作業再開にだけ使い、完了後に削除する。

恒久的な`work/<id>/`は使用しない。一時状態が必要な場合だけ、gitignoreされた`.devflow/run/`を使用する。

## 2. すべての変更で必ず残すもの

### 2.1 実際の成果物

コード、設定、テスト、migration、要件正本、生成設計、運用文書など、依頼された変更そのもの。

### 2.2 Commit Comment

正式にはGitのcommit messageである。Change ManifestとRequirement / Design Impactの独立ファイルを作らず、コミット本文へ次を記録する。

- 目的
- 変更内容
- 要件影響
- 設計影響
- チェックリスト結果のパス
- 検証契約
- 互換性と残存リスク

Commit Commentは変更時点の証跡であり、コミット後にメンテナンスしない。訂正は新しいコミットで行う。

### 2.3 レビュー用チェック結果

選択されたチェック結果だけを`governance/reviews/<change-id>.yaml`へ保存する。

- 未選択項目をN/Aとして保存しない。
- N/Aは、選択後の詳細確認で適用外と判明した場合だけ使う。
- CIログ、テスト件数、coverage全文は保存しない。
- `Invariant`、`Risk-selected`、`Advisory`を区別する。

このファイルも変更時点の証跡であり、後から最新化しない。誤りが判明した場合は新しいコミットで訂正履歴を残す。

### 2.4 CI結果

単体テスト、build、lint、type check、security scan、coverage、deployment結果の正本はGitHub Actionsなどの外部サービスとする。

リポジトリには次だけを残す。

- CI workflow定義
- テストコードとテストデータ
- Commit Commentに記載した検証契約
- レビュー結果YAMLに記載したcheck名または証拠参照

生ログや実行結果の複製は保存しない。

## 3. 条件付きで維持する正本

| 成果物 | 更新条件 | 維持方法 |
|---|---|---|
| `spec/requirements/requirements.json` | 外部挙動、業務ルール、受入条件、非機能閾値、権限要求が変わる | add / update / retireで最新状態を維持 |
| `docs/requirements/REQUIREMENTS.md` | 要件正本が変わる | 正本から自動生成し、直接編集しない |
| `docs/design/generated/` | 対応する実装、OpenAPI、SQL、CloudFormation、型・route等が変わる | 実装から再生成し、driftをCIで拒否 |
| `docs/decisions/ADR-*.md` | 将来を制約し、コードだけでは理由が分からない判断を行う | 本文を上書きせず、accepted / superseded / deprecatedを管理 |
| 運用・保守文書 | 恒久的な監視、復旧、migration、互換性、runbookが変わる | 既存正本を更新する |
| Issue | 将来作業、未解決欠陥、持越すAdvisoryがある | 完了または取消まで維持 |

## 4. 保存しないもの

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

必要な情報は、要件正本、生成設計、ADR、Commit Comment、レビュー結果、Git差分、PR、CI、Issueのいずれかへ収束させる。

## 5. 実行プロファイル

### direct

局所的で可逆、外部副作用がない変更。対象テストと変更範囲の静的検査を行う。

### assured

複数モジュール、公開API、DB、IaC、依存、共有UIなど。変更固有のRisk-selected checkと、必要時だけ独立レビューを追加する。

### regulated

認証・認可、個人情報、データ損失、productionの不可逆操作、法令・契約上の統制、高額操作など。既存のwork item、初回承認、hash chain、工程監査はこのprofileでのみ使用できる。

## 6. チェックのタイミング

### 変更開始前: Impact Check

要件、設計、公開契約、DB、認証・認可、外部副作用、不可逆性を判定し、profileとselected checkを決める。

### 実装中: Fast Feedback Check

変更スライスごとに、targeted test、build、lint、type check、生成物driftなどの自動検査を実行する。

### PR作成前: Affected-scope Check

要件・設計影響、受入条件、変更範囲、互換性、選択チェック、残存リスクをレビューし、結果YAMLを保存する。

### Merge前: Revision Integrity Check

現在HEADに対するCI、生成物、blocking check、Commit Comment、権限境界を確認する。設計レビューを最初から繰り返さない。

### Deploy後: Operational Check

production deploy、migration、外部連携、データ変更がある場合だけ、smoke test、主要指標、rollback可否を外部サービスで確認する。

### 定期: Governance Audit

false blocker、escaped defect、selector miss、Skill競合、不要成果物、標準出典の陳腐化、実行コストを月次またはリリース単位で確認する。

## 7. チェックの強制度

- **Invariant**: triggerに該当した場合は必ずPassが必要。
- **Risk-selected**: 変更リスクから選択された場合だけblocking。
- **Advisory**: 修正、Issue化、または残存リスクとして明示できる。
- **Periodic**: 個々のPRではなく定期監査で扱う。
