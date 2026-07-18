---
name: chat-first-development
description: Start and complete repository development from ordinary natural-language conversation. Use for features, fixes, refactors, design concerns, and incomplete ideas. Select direct, assured, or regulated execution; maintain only durable requirements; generate as-built design from implementation; record selected checklist results in the repository; use structured Commit Comments as the change manifest and requirement/design impact record; and keep CI results in external services.
---

# Chat-first Development

自然言語の相談を唯一の利用者インターフェースとし、成果に必要な最小十分な経路を選ぶ。

## 既定成果物

すべてのrepository変更で次を残す。

1. 実際のコード、設定、テスト、要件、設計等の成果物
2. `docs/COMMIT-COMMENT.md`に従うCommit Comment
3. 選択チェック結果`governance/reviews/<change-id>.yaml`
4. GitHub Actions等の外部サービスにあるCI結果

恒久的な`work/<id>/`、変更ごとの実行計画、implementation log、test reportは既定では作らない。

一時実行状態が必要な場合だけ`.devflow/run/`へ置き、Git管理しない。

## Workflow

1. ユーザーの要求とrepositoryを確認し、結果を変える曖昧さだけを質問する。
2. `$right-size-execution`で`direct`、`assured`、`regulated`を選ぶ。
3. 要件影響と設計影響を仮判定する。
4. 永続要件が変わる場合だけ`$maintain-canonical-requirements`を使う。
5. 変更固有のcheckを選択し、未選択項目をN/Aにしない。
6. 実装し、対象範囲のfast feedbackを実行する。
7. FastAPI、CDKその他の対応対象では`$generate-implementation-design`でas-built設計を生成する。
8. PR前に`$inspect-quality-gates`で選択checkを確認し、review YAMLを保存する。
9. `$japanese-git-commit-gitmoji`で構造化Commit Commentを作成する。
10. PRを作成し、現在HEADのGitHub Actionsを確認する。CIログをrepositoryへ複製しない。
11. blocking failを修正し、advisoryは修正、Issue化、残存リスクのいずれかへ収束させる。
12. 成功後は追加探索を止める。

## Profile

### direct

次を満たす局所変更。

- 可逆
- 外部副作用なし
- 認証・認可、個人情報、データ損失へ影響しない
- 公開契約、DB schema、IaCの重大変更なし

対象test、build、lint、type check、生成物driftだけを実行する。初回承認、work item、独立reviewer、全repository scanは要求しない。

### assured

次のいずれかへ影響する変更。

- 複数module
- 公開API・event契約
- DB schema・migration
- IaC
- dependency・lockfile
- 共有component
- 重要なUI flow
- generator・永続要件・governance

影響固有のRisk-selected checkと、必要なrelated testを追加する。独立reviewerは高影響、oracle不足、検証失敗時だけ使う。

### regulated

次のいずれかに該当する変更。

- 認証・認可
- 個人情報・機密情報
- データ損失
- productionの不可逆操作
- 法令・契約上の統制
- 高額操作
- 明示的に高保証workflowが指定された

この場合だけ`$govern-development-request`、`$author-lifecycle-docs`、`$authorize-autonomous-execution`、hash chain、工程監査を使用できる。

## Requirement impact

外部挙動、業務ルール、受入条件、非機能閾値、権限要求が変わる場合だけ永続要件を更新する。

判定はCommit Commentへ必ず記録する。

## Design impact

実装由来生成設計、ADR、公開契約、data model、resource、恒久的な開発・運用構成への影響を判定し、Commit Commentへ必ず記録する。

詳細設計を手書きで複製しない。コードから生成できない長期判断だけADRにする。

## Check result

`governance/reviews/<change-id>.yaml`には選択されたcheckだけを保存する。

- `Invariant`: trigger該当時はPass必須
- `Risk-selected`: 選択された場合だけblocking
- `Advisory`: 修正、Issue化、残存リスクとして明示できる

CI実行結果は外部サービスを正本とし、YAMLにはcheck名や証拠pathだけを書く。

## Interaction contract

- 利用者へSkill名、work item、command、test実行を要求しない。
- 可逆な実装判断を質問へ変えない。
- 通常変更へ一律の初回承認を要求しない。
- 外部書込み、不可逆操作、production、重大な権限境界だけで明示承認を求める。
- 未確実性だけを理由に作業を停止しない。

## Safety boundaries

- secrets、個人情報、production dump、生ログをGitへ入れない。
- 明示権限なしにproduction deploy、merge、削除、高額操作を行わない。
- 対象repositoryの既存指示、build、test、commit規約を優先する。
- gateを通すためにtest、型、lint、security controlを弱めない。
