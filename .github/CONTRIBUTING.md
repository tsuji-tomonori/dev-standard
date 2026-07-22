# コントリビューションガイド

## 変更前

このリポジトリを変更するときは[`maintain-reference-repository`](../.agents/skills/maintain-reference-repository/SKILL.md)を適用し、移植可能な資産とリポジトリ固有の一時情報を分けます。

開発契約は[`docs/reference/development.md`](../docs/reference/development.md)、Commit Comment形式は[`docs/reference/commit-message.md`](../docs/reference/commit-message.md)を参照してください。

## 基本フロー

1. `direct`、`assured`、`regulated`を選び、要件・設計・配布・互換性・authority boundaryへの影響を判定する。
2. 必要な成果物だけを変更する。永続要件が変わる場合だけ正本を更新する。
3. `governance/checks/catalog.yaml`から関連checkだけを選ぶ。
4. 変更範囲のtest、build、lint、type、生成物driftを実行する。
5. `governance/reviews/<change-id>.yaml`へselected check結果を保存する。
6. `make verify`を実行し、構造化Commit Commentでコミットする。
7. PRを作成し、現在HEADのGitHub Actionsを確認する。

公開API変更は通常`assured`で扱います。認証・認可、PII、データ損失、不可逆production操作、法令・契約統制、高額操作では`regulated`を使用します。

## 境界

- 既存consumerのpathや配布profileを変える場合は、migrationまたは互換性を明示する。
- 未選択checkをN/Aとして登録しない。
- CIの生ログやtest reportをコミットしない。
- secrets、PII、production evidenceをコミットしない。
- 明示権限なしにproduction deploy、削除、公開、merge、高額操作を行わない。
