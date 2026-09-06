# dev-standard lightweight guardrails

portableなblocking guardrailは次の3本だけです。

1. durableな要件を`spec/requirements/requirements.qnt`へ原子的に保つ。
2. 導入・実装変更時に現在状態のMarkdown設計を実装artifactから決定的に生成する。初回はgenerator/adapterを接続し、必要な生成物の欠落・drift検査まで行う。未接続や未対応を完了扱いにしない。
3. 変更と受入条件に関係する検査だけを実行する。

通常の入口は`$chat-first-development`です。Quint正本からJSONを生成し、そのJSONから人向けMarkdownを生成します。生成viewは直接編集しません。

dev-standardは、このrepositoryのbranch、merge方式、CI/CD workflow、required check、PR template、commit形式を追加も変更もしません。既存のrepository指示と権限境界を優先してください。
