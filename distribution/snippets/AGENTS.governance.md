# 統制ルールの統合用参照

以下のうち必要な規則を対象リポジトリの`AGENTS.md`へコピーする。対象固有のビルド、テスト、所有権、安全性の指示は維持する。

- 自然言語による機能追加、修正、リファクタリング、設計の依頼を`chat-first-development`の起動条件として扱い、Skill名やコマンドを要求しない。
- リポジトリ内の初期設定、依存準備、ライフサイクルコマンド、テスト、Git公開、CI確認はAIが行い、利用者へ実行を依頼しない。
- 新しい開発要求では、実装前に`govern-development-request`でwork item、要件、トレーサビリティ、自律実行計画を作る。
- work item作成前に`right-size-execution`でL1〜L3、risk floor、confidence、soft budget、最小検証を記録し、task固有のcheck項目だけを選ぶ。
- 意図探索と版競合を検査したadd/update/retire操作には`maintain-canonical-requirements`を使う。永続要件の唯一の正本は`spec/requirements/requirements.json`とし、`work/<id>`は要求ごとの文脈と証跡だけに使う。
- 要件、実行計画、権限境界、完了条件をまとめた初回承認を要求者へ一度だけ求める。
- 初回承認後は承認範囲内で自律実行する。重大なスコープ変更、権限不足、破壊的操作、外部調整、未解決の安全リスク、完了ゲート失敗だけで停止する。
- 各工程で`author-lifecycle-docs`、`authorize-autonomous-execution`、`inspect-quality-gates`、`retrospect-and-improve`を使う。
- `generate-implementation-design`でrouter/OpenAPI/SQL/CloudFormation成果物からFastAPI/CDKの詳細設計を生成し、生成差分を拒否する。
- `verify-against-engineering-standards`、選択したチェックリストプロファイル、`governance/standards/registry.json`の鮮度確認済み公式資料で要件、設計、実装、テストを検証する。
- `governance/policy.json`、`governance/checklist/catalog.json`、要件正本、各work itemの承認済み差分・計画ハッシュを権威ある情報として扱う。
- 範囲の限定された検査には、合格できる最小能力のモデルを使う。文書化された品質ゲートを満たせない場合だけ能力を引き上げる。
- 検証失敗または新証拠がある場合だけ一軸を一段拡張し、決定的成功後は必須final gate以外の探索を止める。
