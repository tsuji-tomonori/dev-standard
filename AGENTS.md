# リポジトリ指示

## 目的

このリポジトリは、他のリポジトリへ移植するSkills、agents、標準、schema、generator、check、templateの参照集である。このリポジトリ自身を変更するときは、最初に`$maintain-reference-repository`を適用する。

## 既定フロー

feature、fix、refactor、設計相談は`$chat-first-development`を入口にする。

1. `$right-size-execution`で`direct`、`assured`、`regulated`を選ぶ。
2. 要件、設計、配布、互換性、権限への影響を判定する。
3. 永続要件が変わる場合だけ`$maintain-canonical-requirements`を使う。
4. 変更に必要なcheckだけを選び、実装と対象検証を行う。
5. 対応実装では`$generate-implementation-design`でas-built設計を生成する。
6. `governance/reviews/<change-id>.yaml`へselected check結果を保存する。
7. `$japanese-git-commit-gitmoji`でCommit Commentを作り、PRと現在HEADのCI結果を確認する。

詳細は`docs/reference/development.md`を参照する。

## 正本

- 永続要件: `spec/requirements/requirements.json`
- 人向け要件: `docs/requirements/REQUIREMENTS.md`（生成物）
- 要件分類: `docs/standards/REQUIREMENT-CLASSIFICATION.md`
- as-built設計標準: `docs/standards/AS-BUILT-DESIGN.md`
- 生成設計: `docs/design/generated/`
- 長期判断: `docs/decisions/`
- check定義: `governance/checks/catalog.yaml`
- review結果: `governance/reviews/<change-id>.yaml`
- Commit Comment形式: `docs/reference/commit-message.md`

同じ現在状態を複数の手書き文書へ複製しない。

## 実行プロファイル

- `direct`: 局所的、可逆、外部副作用なし。対象test、build、lint、type、driftを実行する。
- `assured`: 公開契約、DB、IaC、dependency、共有UI、generator、要件、governance、distributionに影響する。関連するRisk-selected checkを追加する。
- `regulated`: 認証・認可、PII、データ損失、不可逆production操作、法令・契約統制、高額操作、明示的な高保証要求に使用する。

## 記録と境界

すべての変更で、実際の成果物、Commit Comment、review YAML、外部CI結果を残す。CIの生ログやreport全文をGitへ複製しない。

通常変更で恒久的な`work/<id>/`、実行計画、implementation log、test reportを作らない。一時状態が必要な場合だけgitignoreされた`.devflow/run/`を使い、完了後に削除する。

- secrets、PII、production dump、会話transcriptをコミットしない。
- 明示権限なしにproduction deploy、削除、公開、merge、高額操作を行わない。
- 対象リポジトリ固有のbuild、test、ownership、security、commit規約を維持する。
- gateを通すためにtest、型、lint、security controlを弱めない。
- モデル名を文書へ固定せず、必要能力、コスト、read-only境界から選ぶ。
