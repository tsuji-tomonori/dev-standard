# as-built設計標準

- 標準ID: `DEVSTD-AS-BUILT`
- 版: `2026-09-23`
- 永続要件の唯一の編集対象: `spec/requirements/requirements.qnt`
- 機械可読view: `spec/requirements/requirements.json`

本標準は、言語非依存の要件を導入先のadapterへ接続するための案内である。要件の定義と適用条件はQuint正本を参照する。導入先の言語、framework、source配置、解析器、型検査器、test frameworkは導入先が所有する。dev-standardはadapterの宣言と生成物の整合を検査する。

## 契約と実装の境界

[adapter契約](../../.agents/skills/generate-implementation-design/references/adapter-contract.md)に従い、schema version 2の`.dev-standard/design.json`へcapability、適用要件ID、生成command、`--check` command、出力の所有root、帳票構成profile、参照tools棚卸しを宣言する。実装がないsurfaceだけを根拠付きで非該当とし、未接続・未対応surfaceは未完了として返す。

導入先adapterは、endpointの実接続、責務と所有者、実call graph、保存先へのCRUD、例外から応答と運用ログへの経路、実在testの自然言語検証単位を実装から抽出する。言語固有の構造解析・query解析・interface出力・型検査は導入先commandが担い、dev-standardに固有解析器を追加しない。適用範囲の全sourceを走査し、動的呼出し等で解決できない経路を「アクセスなし」や定型sequenceへ置き換えない。

## 導入手順

1. [導入・復旧手順](../../.agents/skills/generate-implementation-design/references/adoption.md)から実装surfaceと適用要件を棚卸しする。
2. 固定revisionの参照toolsを全件比較し、用途、content hash、言語固有前提、採用区分、理由、導入先の実接続先を記録する。対応できない要件は明示的なgapとする。
3. 参照実装を基に導入先repositoryでadapterを実装する。lazunexの固定SHA `096e1e580ab1c0670c57e4febad2bd9fdd4698ee`の52ファイルは[全件棚卸し](../../.agents/skills/generate-implementation-design/assets/reference-tools/lazunex-096e1e5.json)を参照する。他の参照実装も同じschemaで評価できる。
4. [APIの6帳票契約](../../.agents/skills/generate-implementation-design/references/api-documents.md)に従い、版付き構成profileで章・順序・必須節・繰返し節・非該当表現を定義し、グループ→API→帳票の階層と索引を生成する。
5. 実commandを接続して初回生成し、言語非依存の検査器と導入先の意味検査・実行testを実行する。

## 確認する証拠

検査器はmanifestとschema、active要件集合とmappingの一致、symlinkと管理外出力の拒否、生成物の欠落を確認する。作業コピー上で生成を2回実行してbyte一致を比較し、宣言した`--check` commandで実装と既存生成物のdriftを検出する。commandは導入先が所有する信頼済みcodeであり、作業コピーはprocessの外部作用を隔離するsandboxではない。

帳票は見出しの章構成・順序・階層・索引・旧生成物・リンク切れを検査する。CRUDのCSV・表・図・根拠は同一モデルから生成する。参照tools棚卸しは全件集合、重複、hash、要件対応を確認する。参照repositoryとの再照合は固定revisionに対して行う。

報告は構成適合、設計drift、実行テスト、未検証範囲を分ける。静的な契約適合と実装の意味的正しさを混同せず、未実行・未対応・失敗を成功へ読み替えない。品質portalには親子関係、現在位置、階層を保持する検索、CSV取得を接続する。

## 既存標準からの移行

旧版の`GEN-*`、`ALIGN-*`、言語固有Rule IDは現行の独立規範として適用しない。維持する義務はQuintの`REQ-ASBUILT-*`、`REQ-DESIGN-*`、`REQ-EVIDENCE-*`へ再定義している。検査catalogのIDは変更に関係する検査を選ぶための参照であり、旧Rule IDを再導入する根拠にはしない。

旧`designflow.py`・`qualityflow.py`を使用していた導入先は、adapter実装とmanifestを接続し、生成物と検査の移行を確認する。旧`tools/portable_python.py`と専用runtimeは不要になる。installerは既存fileを自動削除しないため、導入先で変更差分と所有者を確認して旧assetを除去する。既存のbranch、CI workflow、required check、merge rule、PR templateは変更しない。
