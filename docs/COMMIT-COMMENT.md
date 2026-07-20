# Commit Comment契約

このリポジトリでは利用者の呼称に合わせて`Commit Comment`と記載するが、Gitの正式名称は**commit message**である。

## 1. 目的

Commit Commentは次を代替する。

- Change Manifest
- Requirement Impact Result
- Design Impact Result
- 変更ごとのimplementation log

CIの実行結果や生ログは代替しない。CI結果の正本はGitHub Actionsなどの外部サービスとする。

## 2. 形式

```text
<gitmoji> <type>(<scope>): <日本語の要約>

目的:
- <この変更で得る結果>

変更内容:
- <意味単位の主要変更>

要件影響:
- あり | なし
- 要件ID: <REQ-... | none>
- 理由: <判定根拠>

設計影響:
- あり | なし
- 対象: <生成設計、ADR、公開契約、構成等 | none>
- 生成設計: <更新先 | 対象外>
- ADR: <ADR番号 | 不要とした理由>

チェックリスト:
- governance/reviews/<change-id>.yaml

検証契約:
- GitHub Actions: <workflowまたはrequired check名>
- ローカル: <必要な場合だけ実行した決定的検査>
- 結果の正本: GitHub Actions等

互換性・残存リスク:
- <互換性、移行、未検証範囲、既知制約>

Requirements: <REQ IDs | none>
Design-Impact: <none | generated | adr | contract | governance | mixed>
Review-Checklist: governance/reviews/<change-id>.yaml
Refs: <Issue / ADR。該当時だけ>
```

## 3. 記載規則

### 1行目

- `<gitmoji> <type>(<scope>): <日本語の要約>`を使用する。
- typeはConventional Commitsに従う。
- 一つの主目的を表す。
- 破壊的変更は`!`と`BREAKING CHANGE:`で明示する。

### 目的

手順ではなく、利用者または開発上の結果を書く。

### 変更内容

3～6項目を目安とする。ファイル一覧や作業ログをそのまま列挙しない。

### 要件影響

必ず`あり`または`なし`を記載する。

`あり`の場合:

- 変更した要件IDを示す。
- 正本へadd / update / retireを適用する。

`なし`の場合:

- 外部挙動、業務ルール、受入条件、非機能閾値、権限要求が変わらない理由を書く。
- `なし`だけで終わらせない。

### 設計影響

必ず`あり`または`なし`を記載する。

`あり`の場合は、次のどれが変わるかを示す。

- 実装由来の生成設計
- ADR
- 公開API・イベント契約
- データモデル
- infrastructure resource
- 開発・運用上の恒久構成

コードから自明でない長期判断がある場合だけADRを作る。ADRが不要なら理由を書く。

### チェックリスト

選択チェック結果のリポジトリパスを一つ以上示す。未選択項目の一覧は書かない。

### 検証契約

コミット時点でまだ完了していないCIを`Pass`と書かない。実行されるworkflowまたはrequired check名を記載し、実結果は外部CIへ委ねる。

ローカル結果を書く場合も、合否の要約だけにし、生ログを本文へ貼り付けない。

### 互換性・残存リスク

次を該当時に書く。

- breaking change
- migration
- rollback
- consumer影響
- 未検証環境
- 既知のadvisory
- 旧構成の移行対象外

## 4. 完成例

```text
🧭 refactor(governance): work依存を廃止して変更証跡をコミットへ集約

目的:
- 正本、変更時点の監査証跡、一時実行状態を分離する
- 変更ごとの重複文書を廃止し、人の確認対象を減らす

変更内容:
- Change Manifestを構造化Commit Commentへ統合
- Requirement / Design ImpactをCommit Commentの必須節へ統合
- CI結果はGitHub Actionsを正本とし、リポジトリへ保存しない
- 選択チェック結果だけをgovernance/reviews/へ保存

要件影響:
- なし
- 要件ID: none
- 理由: 製品の外部挙動と受入条件を変更しない開発プロセス整理

設計影響:
- あり
- 対象: 開発統制とレビュー証跡の構成
- 生成設計: 対象外
- ADR: 不要（リポジトリ運用規約として直接定義）

チェックリスト:
- governance/reviews/CHG-20260718-artifact-governance.yaml

検証契約:
- GitHub Actions: make verify, review-schema, generated-drift
- 結果の正本: GitHub Actions
- 生ログ・単体テスト結果はリポジトリへ保存しない

互換性・残存リスク:
- 旧work itemの自動移行は対象外
- regulated profileの既存監査機能は条件付きで維持

Requirements: none
Design-Impact: governance
Review-Checklist: governance/reviews/CHG-20260718-artifact-governance.yaml
```

## 5. スカッシュマージ

Commit CommentをChange Manifestの正本とするPRは**squash merge必須**とする。最終squash commitの本文へPR全体の内容を統合し、中間コミットやPR本文だけに要件・設計影響を残さない。

merge commitまたはrebase mergeを使用するリポジトリでは、PR内の全commitを同じCommit Comment契約で検査する別workflowが必要である。
