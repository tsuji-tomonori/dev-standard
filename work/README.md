# `work/`ディレクトリについて

このディレクトリにコミットされている既存work itemは、commit `e85312a`で通常開発を`direct` / `assured` / `regulated`へ分離する前に作成された履歴証跡です。移行経緯を追跡できるよう保持していますが、現行の通常変更で複製するtemplateまたは実装例ではありません。

現行ルールは次のとおりです。

- `direct`と`assured`では、恒久的な`work/<id>/`、初回承認、lifecycle文書、hash chain、phase gateを作成しません。
- 変更ごとの証跡は、実際の成果物、構造化Commit Comment、`governance/reviews/<change-id>.yaml`、GitHub Actions等の外部CIへ集約します。
- 再開用の一時状態が必要な場合だけ、gitignoreされた`.devflow/run/`を使用し、変更完了後に削除します。
- 新しい`work/<id>/`は、authentication、authorization、PII、data loss、不可逆なproduction操作、法令・契約統制、高額操作、明示的な高保証要求等により`regulated`を選択した場合だけ作成します。
- 既存work itemは変更時点の証跡です。現在の規約へ合わせる目的で内容を書き換えません。

詳細は[`README.md`](../README.md)の「`work/`の扱い」と[`docs/GOVERNANCE.md`](../docs/GOVERNANCE.md)を参照してください。
