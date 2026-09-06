# dev-standard

AI開発agentへこのrepositoryを参照させると、対象プロジェクトに合わせて次の3要素を導入・実行するためのSkills集です。

1. **要件**: 永続する挙動・制約・受入条件を `spec/requirements/requirements.qnt` に保ちます。可逆な実装判断は固定しません。
2. **実装由来の設計**: API・data・infra・frontendの実装から必要なas-built設計を生成し、欠落・差分を検査します。
3. **関係する検査**: 変更と受入条件に必要なtest・lint・型検査・build・生成検査を選んで実行します。

## 使い方

対象プロジェクトで、例えば次のように依頼します。

> https://github.com/tsuji-tomonori/dev-standard を参照して、［作りたいもの・要件］を実装してください。既存構成に合わせて3本柱を導入し、要件の生成、実装由来の設計の初回生成、関連する検査まで完了してください。

agentは[導入ガイド](docs/guides/getting-started.md)と `chat-first-development` から始めます。既定配布は入口と3本柱の4 Skillです。補助Skillは用途がある場合だけ選びます。利用者に内部commandやファイルコピーを委ねて停止しません。

installerはSkillと実行基盤を配置します。**配置だけでは導入完了ではありません。** agentが実際の要件・技術構成を調べ、必要なgenerator/adapterを接続し、設計Markdownを生成して検査します。未対応の必要領域は未完了として示します。詳細な生成物・検査・完了報告の条件は[導入ガイド](docs/guides/getting-started.md)を参照してください。

導入先のbranch、merge方式、CI/CD、commit形式、既存指示は導入先が所有します。既存CIとの接続はその運用と権限に従い、CIがなければローカル検証を使います。

## 保守

このrepositoryを変更するagentは `AGENTS.md` と `maintain-reference-repository` に従います。[文書索引](docs/README.md)に、維持する文書の利用者・目的・更新条件と、更新しない履歴の所在をまとめています。
