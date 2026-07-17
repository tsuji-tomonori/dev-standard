# 詳細設計

## 対象・authority・用語

対象は3 Skillsと自己適用catalog/registry、distribution/CI統合である。正本要件 > implementation artifact > generated designの順にauthorityを持つ。`work`はrequest-local、`canonical`は永続正本、`derived`は再生成可能なview、`retire`は履歴保持型廃止を表す。

## インターフェース

| Interface | Input | Output | Error contract |
|---|---|---|---|
| `specflow validate/generate/check` | canonical JSON、任意のoutput path | validation result、Markdown | schema、atomicity、driftをexit 2で拒否 |
| `specflow apply` | canonical JSON、base revision付きchange JSON | revision増分済みcatalogとMarkdown | stale catalog/item、unknown operation、invalid candidateはwrite前に拒否 |
| `designflow fastapi` | source root、OpenAPI JSON/YAML、SQL root、output | sequence、API、IF、CRUD、query、manifest | missing router/functions、parse/operation ID/drift error |
| `designflow cdk` | synth済みCFn YAML/JSON、output | resource、parameter、manifest | YAML/JSON parse error、drift error |
| `standardsflow validate/generate/check` | registry、as-of date | source Markdown、freshness verdict | unofficial host、bad field、stale sourceを拒否 |
| `distribution/manifest.json` | profile name | copy mapping | unknown profile、escape、conflictをinstallerが拒否 |

CLIは利用者向けUIではなくagent/CI internal interfaceである。利用者は自然言語だけを使う。

## データモデル

Canonical catalog envelopeは`schema_version`、`catalog_revision`、`product`、`updated_at`、ordered `requirements`だけを許す。Requirementはstable `id`、item `revision`、`status`、`type`、`title`、単一行の`subject/action/object`、`rationale`、`source_refs`、Given/When/Then criteria、verification、design/implementation/tests/standards traces、changerを持つ。`retired`のみreason必須である。

Change setは`base_catalog_revision`、`changed_at`、`work_item`、nonempty operationsからなる。operationは厳密field setを持つ`add`、`update`、`retire`のいずれかである。

Standards registry sourceはID、authority、title、version、official HTTPS URL、checked date、positive refresh days、unique profilesを持つ。Generated design manifestはsource path/SHA-256と生成file一覧を持つ。

## 制御・状態・例外

Requirements applyはread -> revision compare -> deep-copy -> operation apply -> sort -> complete validation -> temporary write/fsync -> atomic replace -> derived view generationの順である。input objectはfailure時も変更しない。

FastAPI sequenceはroute decoratorをmetadataとして除外し、function bodyのcallをPython評価順（callee/argumentの内側から外側）で収集する。route最終statementはresponse producerのdirect callでなければならない。各routerにはsibling `functions.py`を要求し、両方をmanifestへ含める。

SQLは各statementをAST parseし、INSERT/UPDATE/DELETE targetへC/U/D、target以外の参照tableへRを付与する。CDKはunknown CloudFormation tagを構造値として保持し、`Resources`と`Parameters`だけをcatalog化する。

## 認証・認可・入力検証

runtime authenticationは非適用。外部write authorizationはwork itemの初回承認とexecution planで制御する。JSONはexact field allowlist、ID/date/action pattern、nonempty value、duplicate検査を行う。YAMLはsafe loader派生を使い任意constructorを実行しない。SQL/Pythonはparserを使い、shellとして実行しない。official source URLはissuer host allowlistを通す。

## 観測可能性

全CLIは成功対象または具体的errorをstdoutへ出し、0/2で判定可能にする。Generated manifest、unit test名、work checklist result、hash-chained events、GitHub Actionsを証跡とする。service metrics/log/alertはdeployable runtimeがないため非適用。

## 移行・互換性

既存skill layoutとgovernance schemaは維持する。新規targetはskill assetのcatalog revision 0 templateからbootstrapする。このreference自身はrevision 1で自己適用する。既存targetに正本がある場合は上書きせずrevision付きdeltaを使う。既存`AGENTS.md`と`.codex/config.toml`はinstallerが上書きしない。
