<!-- tools/quintflow.pyによる自動生成。spec/requirements/requirements.qntを編集すること。 -->
# dev-standard 要件一覧

- スキーマ版: 1
- カタログ版: 12
- Product(JSON): <code>"dev-standard"</code>
- 更新日(JSON): <code>"2026-08-29"</code>
- 正本: `spec/requirements/requirements.qnt`
- 機械可読view: `spec/requirements/requirements.json`

| ID | 版 | 状態 | 種別 | 原子的な義務 | 検証方法 |
|---|---:|---|---|---|---|
| <code>"REQ-ASBUILT-001"</code> | 1 | 有効 | 品質 | as-built設計generatorは、同一入力からバイト一致する設計出力を**生成する**（<code>"generate"</code>） | 自動テスト |
| <code>"REQ-ASBUILT-002"</code> | 1 | 有効 | 品質 | as-built設計generatorは、一つの生成logicを共有するgenerate modeとcheck modeを**提供する**（<code>"provide"</code>） | 自動テスト |
| <code>"REQ-ASBUILT-003"</code> | 1 | 有効 | 制約 | as-built生成物は、docs/design/generated/配下の直接編集禁止banner付き.gen.md設計を**分離する**（<code>"separate"</code>） | repository検査 |
| <code>"REQ-ASBUILT-004"</code> | 2 | 有効 | 機能 | as-built設計generatorは、handler ASTとOpenAPIとsampleとSQLから得たAPI詳細設計を**導出する**（<code>"derive"</code>） | 自動テスト |
| <code>"REQ-ASBUILT-005"</code> | 1 | 有効 | 機能 | as-built設計generatorは、handler metadataから得た重複のないAPI一覧を**導出する**（<code>"derive"</code>） | 自動テスト |
| <code>"REQ-ASBUILT-006"</code> | 2 | 有効 | データ | as-built設計generatorは、SQLと外部client呼出から得たtableおよび外部連携先のCRUD関係を**導出する**（<code>"derive"</code>） | 自動テスト |
| <code>"REQ-ASBUILT-007"</code> | 3 | 有効 | データ | as-built設計generatorは、正本DDLとSQLから得たtable定義とER関係と書込みAPIを**導出する**（<code>"derive"</code>） | 自動テスト |
| <code>"REQ-ASBUILT-008"</code> | 2 | 有効 | 機能 | as-built設計generatorは、E2E testのGiven When Then構造から得たscenario設計を**導出する**（<code>"derive"</code>） | 自動テスト |
| <code>"REQ-ASBUILT-009"</code> | 4 | 有効 | 運用 | as-built設計generatorは、対象repositoryが所有する結果JSONから得た参照限定test evidence viewを**導出する**（<code>"derive"</code>） | 契約テスト |
| <code>"REQ-ASBUILT-010"</code> | 2 | 有効 | 機能 | as-built設計generatorは、tool entrypoint ASTとdocstringから得たCLI仕様とflowを**導出する**（<code>"derive"</code>） | 自動テスト |
| <code>"REQ-ASBUILT-011"</code> | 3 | 有効 | データ | as-built設計generatorは、API error分岐から得たcatalog全体で一意なID付きmachine-readable error caseを**生成する**（<code>"generate"</code>） | 自動テスト |
| <code>"REQ-ASBUILT-012"</code> | 2 | 有効 | 品質 | as-built整合checkは、handler登録と設計metadataとerror sampleの三点整合を**検証する**（<code>"verify"</code>） | 静的解析 |
| <code>"REQ-ASBUILT-013"</code> | 2 | 有効 | 品質 | as-built整合checkは、設計掲載sampleと実response assertionの対応を**検証する**（<code>"verify"</code>） | AST静的解析 |
| <code>"REQ-ASBUILT-014"</code> | 3 | 有効 | 品質 | as-built整合checkは、DBまたは外部変更effectを持つAPIとeffect別E2E状態assertの対応を**検証する**（<code>"verify"</code>） | 静的解析とE2E契約テスト |
| <code>"REQ-ASBUILT-015"</code> | 2 | 有効 | 品質 | 導入先repositoryのtestは、AAAまたはGWTとdocstringと1 case 1関数を持つtestを**構成する**（<code>"structure"</code>） | AST静的解析 |
| <code>"REQ-ASBUILT-016"</code> | 3 | 有効 | 品質 | 導入先repositoryのunit testは、C0命令網羅95%以上とC1分岐網羅90%以上のcoverageを**計測する**（<code>"measure"</code>） | coverage toolとreview contract |
| <code>"REQ-ASBUILT-017"</code> | 2 | 有効 | 制約 | as-built規約は、Rule IDからcatalog check IDへ接続された機械可読check定義を**維持する**（<code>"maintain"</code>） | repository契約テスト |
| <code>"REQ-ASBUILT-018"</code> | 2 | 有効 | 運用 | as-built規約checkは、理由付きRule ID抑制箇所の監査一覧を**生成する**（<code>"generate"</code>） | 定期repository audit |
| <code>"REQ-ASBUILT-019"</code> | 4 | 有効 | 運用 | inspect-quality-gates runnerは、選択したtest・static analysis・規約check・coverageの結果と未検証範囲を示す一つのlocal summaryまたは対象所有viewを**提供する**（<code>"provide"</code>） | 契約テスト |
| <code>"REQ-ASBUILT-020"</code> | 2 | 有効 | 品質 | as-built設計generatorは、schema version 2 trace JSONが適用対象として宣言したactive canonical requirement IDからartifactを経てportable pytest static nodeへ至る完全な明示traceを**妥当性確認する**（<code>"validate"</code>） | 自動テスト |
| <code>"REQ-DESIGN-001"</code> | 3 | 有効 | 制約 | FastAPI実装フレームは、router.pyのオーケストレーションとfunctions.pyの具体処理に分けたoperationを**構成する**（<code>"structure"</code>） | 自動テスト |
| <code>"REQ-DESIGN-002"</code> | 2 | 有効 | 機能 | 設計生成器は、FastAPI routerの構文木から得たoperationシーケンス図を**導出する**（<code>"derive"</code>） | 自動テスト |
| <code>"REQ-DESIGN-003"</code> | 2 | 有効 | インターフェース | 設計生成器は、OpenAPI文書からのAPIとインターフェースの一覧を**導出する**（<code>"derive"</code>） | 自動テスト |
| <code>"REQ-DESIGN-004"</code> | 2 | 有効 | データ | 設計生成器は、生SQLからのquery objectとCRUD文書を**解析する**（<code>"parse"</code>） | 自動テスト |
| <code>"REQ-DESIGN-005"</code> | 2 | 有効 | 機能 | 設計生成器は、合成済みCloudFormationからのresourceとparameter一覧を**導出する**（<code>"derive"</code>） | 自動テスト |
| <code>"REQ-DESIGN-006"</code> | 3 | 有効 | 品質 | 設計フローは、実装成果物と自動生成された詳細設計の差分を**検出する**（<code>"detect"</code>） | 自動テスト |
| <code>"REQ-DISC-001"</code> | 2 | 有効 | 機能 | 開発エージェントは、適切な対話を通じたユーザーの意図する成果を**探り当てる**（<code>"discover"</code>） | 契約レビュー |
| <code>"REQ-DISC-002"</code> | 4 | 有効 | データ | 要件カタログは、正本要件IDごとの一つの原子的な義務を**維持する**（<code>"maintain"</code>） | 構造自動テストとhuman semantic review |
| <code>"REQ-DISC-003"</code> | 6 | 有効 | 機能 | 仕様管理フローは、版と同時更新安全性を保つQuint要件の追加、更新、廃止を**維持する**（<code>"maintain"</code>） | Quint検証と自動テスト |
| <code>"REQ-DISC-004"</code> | 5 | 有効 | 機能 | 仕様管理フローは、QuintからJSONを経由した日本語の人間向け要件文書を**生成する**（<code>"generate"</code>） | 自動テスト |
| <code>"REQ-DISC-005"</code> | 2 | 有効 | 機能 | 要件管理Skillは、solution候補と権限ある永続要件を**分離する**（<code>"separate"</code>） | 自動テスト |
| <code>"REQ-DOCS-001"</code> | 1 | 有効 | 品質 | 文書生成フローは、識別子と固有名詞を除いて日本語で統一された利用者向け文書を**提供する**（<code>"provide"</code>） | 自動検査 |
| <code>"REQ-EXEC-001"</code> | 3 | 有効 | 運用 | 開発実行基盤は、相互に独立した変更範囲、保証水準、計算資源および実行方式を**推定する**（<code>"estimate"</code>） | 自動テスト |
| <code>"REQ-EXEC-002"</code> | 3 | 有効 | 品質 | 開発実行基盤は、risk tag、成果物、外部副作用および不可逆性から導出したassurance下限を**強制する**（<code>"enforce"</code>） | 自動テスト |
| <code>"REQ-EXEC-003"</code> | 3 | 有効 | 品質 | 開発実行基盤は、通常のルート判断と決定的metadataによる初期Estimateを**経路選択する**（<code>"route"</code>） | 自動テスト |
| <code>"REQ-EXEC-004"</code> | 2 | 有効 | 品質 | 開発実行基盤は、実行制御へ入力するconfidenceの根拠とscoreを**制約する**（<code>"constrain"</code>） | 自動テスト |
| <code>"REQ-EXEC-005"</code> | 2 | 有効 | 品質 | 開発実行基盤は、scope、assurance、成果物、risk、受入条件および対象repositoryが明示したgateの完全一致するverification projectionを**導出する**（<code>"derive"</code>） | 自動テスト |
| <code>"REQ-EXEC-006"</code> | 2 | 有効 | 品質 | 開発実行基盤は、初期profileを覆す新証拠に対応する一つの実行軸を**拡張する**（<code>"expand"</code>） | 自動テスト |
| <code>"REQ-EXEC-007"</code> | 2 | 有効 | 品質 | 開発実行基盤は、成功条件、required verificationおよびassurance floor充足後の正のコスト活動を**停止する**（<code>"stop"</code>） | 自動テスト |
| <code>"REQ-EXEC-008"</code> | 2 | 有効 | 品質 | 開発実行基盤は、明示選択時だけの推定、Estimate overhead、実績、Expand、品質および停止後活動の任意計測を**計測する**（<code>"measure"</code>） | 自動テストとbenchmark |
| <code>"REQ-EXEC-009"</code> | 3 | 有効 | 品質 | 標準検証基盤は、version固定selectorによるチェック候補と選択漏れ監査sampleを**選択する**（<code>"select"</code>） | 自動テストとbenchmark |
| <code>"REQ-EXEC-010"</code> | 2 | 有効 | 制約 | 実行効率制御は、repository blockerを増やさないtelemetry、shadow、soft routing、calibrationおよびadvisory診断の導入順序を**段階適用する**（<code>"stage"</code>） | 自動テスト |
| <code>"REQ-FRAME-001"</code> | 3 | 有効 | 制約 | リポジトリは、一時的な作業記録と永続的な製品要件を**分離する**（<code>"separate"</code>） | 自動検査 |
| <code>"REQ-PORTABLE-001"</code> | 5 | 有効 | 運用 | 移植可能なSkills集は、別リポジトリへのcopy-and-chat方式の導入を**実現する**（<code>"enable"</code>） | 自動E2Eテスト |
| <code>"REQ-PORTABLE-002"</code> | 1 | 有効 | 制約 | portable installerと既定profileは、導入先のbranch、merge rule、CI workflowを追加も変更もしないことを**維持する**（<code>"preserve"</code>） | installer isolation test |
| <code>"REQ-PORTABLE-003"</code> | 1 | 有効 | 制約 | portable Skillとruntimeは、外部または不可逆な操作を利用者が明示した依頼と必要な承認の範囲だけに限定することを**制約する**（<code>"constrain"</code>） | 契約テストとmutation test |
| <code>"REQ-QUALITY-001"</code> | 2 | 有効 | 運用 | 品質フレームは、SWEBOKとクラウド・AI公式資料の監査可能な出典台帳を**維持する**（<code>"maintain"</code>） | 自動検査 |
| <code>"REQ-QUALITY-002"</code> | 5 | 有効 | 品質 | 品質フローは、変更と受入条件に関係する検査だけによる成果物検証を**検証する**（<code>"verify"</code>） | 契約テスト |
| <code>"REQ-QUALITY-003"</code> | 3 | 有効 | 品質 | チェックリスト生成フローは、一項目・一統制・一証跡で独立判定できるチェック項目を**維持する**（<code>"maintain"</code>） | 自動テストと批判的レビュー |
| <code>"REQ-QUALITY-004"</code> | 1 | 有効 | 制約 | portable blocking guardrailは、要件正本、as-built生成、選択checkの3本柱だけを対象にすることを**制約する**（<code>"constrain"</code>） | Quint invariant verification |
| <code>"REQ-QUINT-001"</code> | 3 | 有効 | 制約 | 永続要件は、Quint仕様を唯一の編集対象としJSONを派生物として維持することを**維持する**（<code>"maintain"</code>） | Quint typecheckと生成drift検査 |
| <code>"REQ-QUINT-002"</code> | 3 | 有効 | 機能 | 要件生成器は、Quintから全fieldとList順を保持するJSONを生成し、そのserialized JSONから人向けMarkdownを生成することを**生成する**（<code>"generate"</code>） | 決定的生成とgolden mappingテスト |
| <code>"REQ-QUINT-003"</code> | 2 | 有効 | 品質 | Skill形式仕様は、すべてのSkillを一対一のQuint契約とactive要件の双方向traceへ対応付けることを**形式化する**（<code>"formalize"</code>） | Quint testと双方向集合比較 |
| <code>"REQ-REPO-001"</code> | 3 | 廃止 | 制約 | dev-standardのbranch運用は、mainへのsquashとdevへのmerge commitを分離したbranch別統合契約を**強制する**（<code>"enforce"</code>） | CIとGitHub ruleset監査 |
| <code>"REQ-REPO-002"</code> | 3 | 廃止 | 運用 | release operatorとCIは、release前後のancestor関係、tip tree条件、freezeを含むreconciliation transactionを**維持する**（<code>"maintain"</code>） | branch graph回帰テストとCI |
| <code>"REQ-REPO-003"</code> | 3 | 廃止 | 制約 | dev-standardの二層branch試行は、2回のrelease cycleに限定しportable profileへ既定配布しない二層branch試行を**制約する**（<code>"constrain"</code>） | repository contract testと試行後review |
| <code>"REQ-SKILL-001"</code> | 1 | 有効 | 制約 | right-size-executionは、Estimate、ExecuteおよびExpandを一体化した再利用可能な実行制御契約を**提供する**（<code>"provide"</code>） | 自動検査 |
| <code>"REQ-SKILL-002"</code> | 1 | 有効 | 品質 | Skill検証基盤は、SKILL.mdの主要behavior constraintが代表trajectoryで実行された証拠を**検証する**（<code>"verify"</code>） | 自動benchmark |
| <code>"REQ-WORKBOOK-001"</code> | 2 | 有効 | 運用 | チェックリスト生成フローは、実データ範囲だけを集計し決定的に再現できるレビュー用ワークブックを**生成する**（<code>"generate"</code>） | 自動検査と描画確認 |

## REQ-ASBUILT-001: as-built生成の決定論性

要件ID(JSON): <code>"REQ-ASBUILT-001"</code>
タイトル(JSON): <code>"as-built生成の決定論性"</code>
主体(JSON): <code>"as-built設計generator"</code>
対象(JSON): <code>"同一入力からバイト一致する設計出力"</code>
as-built設計generatorは、同一入力からバイト一致する設計出力を**生成する**。
行為enum: <code>"generate"</code>

根拠: 差分によるdrift検知には非決定要素を除いた再現可能な出力が必要である。
根拠(JSON): <code>"差分によるdrift検知には非決定要素を除いた再現可能な出力が必要である。"</code>

項目版: 1 / 状態: `active` / 種別: `quality`
変更識別子: <code>"CHG-20260721-as-built-design"</code>
分類: scope=<code>""</code> / category=<code>""</code>

受入条件:
- <code>"AC-ASBUILT-001-1"</code> 前提: 同一revisionの宣言済み一次情報がある。条件: generatorを複数回実行する。期待結果: 列挙順が固定され、時刻・乱数・環境依存pathを含まないバイト一致出力になる。
  - criterion(JSON Object): <code>{"given":"同一revisionの宣言済み一次情報がある","id":"AC-ASBUILT-001-1","then":"列挙順が固定され、時刻・乱数・環境依存pathを含まないバイト一致出力になる","when":"generatorを複数回実行する"}</code>

要求源(JSON List): <code>["user:2026-07-21","docs/standards/AS-BUILT-DESIGN.md"]</code>
検証方法: 自動テスト
検証証跡: 同一fixtureを複数回生成したbyte比較
検証(JSON Object): <code>{"evidence":"同一fixtureを複数回生成したbyte比較","method":"自動テスト"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/AS-BUILT-DESIGN.md"]</code>
- 実装: <code>["governance/checks/catalog.yaml",".agents/skills/generate-implementation-design/scripts/designflow.py"]</code>
- テスト: <code>["tests/test_review_contract.py","tests/test_designflow.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-002: generateとcheckの二相契約

要件ID(JSON): <code>"REQ-ASBUILT-002"</code>
タイトル(JSON): <code>"generateとcheckの二相契約"</code>
主体(JSON): <code>"as-built設計generator"</code>
対象(JSON): <code>"一つの生成logicを共有するgenerate modeとcheck mode"</code>
as-built設計generatorは、一つの生成logicを共有するgenerate modeとcheck modeを**提供する**。
行為enum: <code>"provide"</code>

根拠: 生成と検査を別実装にすると両者の意味が乖離する。
根拠(JSON): <code>"生成と検査を別実装にすると両者の意味が乖離する。"</code>

項目版: 1 / 状態: `active` / 種別: `quality`
変更識別子: <code>"CHG-20260721-as-built-design"</code>
分類: scope=<code>""</code> / category=<code>""</code>

受入条件:
- <code>"AC-ASBUILT-002-1"</code> 前提: 宣言済み生成対象と既存生成物がある。条件: check modeを実行する。期待結果: 生成logicを再利用して既存生成物と比較し、差分pathを列挙して非0終了する。
  - criterion(JSON Object): <code>{"given":"宣言済み生成対象と既存生成物がある","id":"AC-ASBUILT-002-1","then":"生成logicを再利用して既存生成物と比較し、差分pathを列挙して非0終了する","when":"check modeを実行する"}</code>

要求源(JSON List): <code>["user:2026-07-21","docs/standards/AS-BUILT-DESIGN.md"]</code>
検証方法: 自動テスト
検証証跡: write modeとcheck modeの同一出力およびdrift終了code
検証(JSON Object): <code>{"evidence":"write modeとcheck modeの同一出力およびdrift終了code","method":"自動テスト"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/AS-BUILT-DESIGN.md"]</code>
- 実装: <code>["governance/checks/catalog.yaml",".agents/skills/generate-implementation-design/scripts/designflow.py"]</code>
- テスト: <code>["tests/test_review_contract.py","tests/test_designflow.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-003: 生成設計の隔離と識別

要件ID(JSON): <code>"REQ-ASBUILT-003"</code>
タイトル(JSON): <code>"生成設計の隔離と識別"</code>
主体(JSON): <code>"as-built生成物"</code>
対象(JSON): <code>"docs/design/generated/配下の直接編集禁止banner付き.gen.md設計"</code>
as-built生成物は、docs/design/generated/配下の直接編集禁止banner付き.gen.md設計を**分離する**。
行為enum: <code>"separate"</code>

根拠: 専用path、命名、更新commandにより手書き設計との混在と直接編集を防げる。
根拠(JSON): <code>"専用path、命名、更新commandにより手書き設計との混在と直接編集を防げる。"</code>

項目版: 1 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"CHG-20260721-as-built-design"</code>
分類: scope=<code>""</code> / category=<code>""</code>

受入条件:
- <code>"AC-ASBUILT-003-1"</code> 前提: Markdown形式のas-built設計を生成する。条件: 生成物の配置と先頭行を検査する。期待結果: docs/design/generated/配下の.gen.mdでありgenerate/check commandを含む直接編集禁止bannerがあり、同じ現在状態の手書き設計が存在しない。
  - criterion(JSON Object): <code>{"given":"Markdown形式のas-built設計を生成する","id":"AC-ASBUILT-003-1","then":"docs/design/generated/配下の.gen.mdでありgenerate/check commandを含む直接編集禁止bannerがあり、同じ現在状態の手書き設計が存在しない","when":"生成物の配置と先頭行を検査する"}</code>

要求源(JSON List): <code>["user:2026-07-21","docs/standards/AS-BUILT-DESIGN.md"]</code>
検証方法: repository検査
検証証跡: 生成path、file名、banner、重複設計scan
検証(JSON Object): <code>{"evidence":"生成path、file名、banner、重複設計scan","method":"repository検査"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/AS-BUILT-DESIGN.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/SKILL.md","governance/checks/catalog.yaml",".agents/skills/generate-implementation-design/scripts/designflow.py"]</code>
- テスト: <code>["tests/test_review_contract.py","tests/test_designflow.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-004: API詳細設計の導出

要件ID(JSON): <code>"REQ-ASBUILT-004"</code>
タイトル(JSON): <code>"API詳細設計の導出"</code>
主体(JSON): <code>"as-built設計generator"</code>
対象(JSON): <code>"handler ASTとOpenAPIとsampleとSQLから得たAPI詳細設計"</code>
as-built設計generatorは、handler ASTとOpenAPIとsampleとSQLから得たAPI詳細設計を**導出する**。
行為enum: <code>"derive"</code>

根拠: APIのinterfaceと実行flowを同じ一次情報から導出すると実装との1対1対応を維持できる。
根拠(JSON): <code>"APIのinterfaceと実行flowを同じ一次情報から導出すると実装との1対1対応を維持できる。"</code>

項目版: 2 / 状態: `active` / 種別: `functional`
変更識別子: <code>"CHG-20260829-review-remediation"</code>
分類: scope=<code>""</code> / category=<code>""</code>

受入条件:
- <code>"AC-ASBUILT-004-1"</code> 前提: handler、framework OpenAPI、sample定数、生SQLがある。条件: API設計を生成する。期待結果: interface、sequence、全branchを保つcontrol-flow graph、処理step、error分岐、message、unit-test観点をhandler起点で生成する。
  - criterion(JSON Object): <code>{"given":"handler、framework OpenAPI、sample定数、生SQLがある","id":"AC-ASBUILT-004-1","then":"interface、sequence、全branchを保つcontrol-flow graph、処理step、error分岐、message、unit-test観点をhandler起点で生成する","when":"API設計を生成する"}</code>

要求源(JSON List): <code>["user:2026-07-21","docs/standards/AS-BUILT-DESIGN.md"]</code>
検証方法: 自動テスト
検証証跡: API fixtureからの生成内容assert
検証(JSON Object): <code>{"evidence":"API fixtureからの生成内容assert","method":"自動テスト"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/AS-BUILT-DESIGN.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/SKILL.md","governance/checks/catalog.yaml",".agents/skills/generate-implementation-design/scripts/designflow.py"]</code>
- テスト: <code>["tests/test_review_contract.py","tests/test_designflow.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-005: API一覧の導出

要件ID(JSON): <code>"REQ-ASBUILT-005"</code>
タイトル(JSON): <code>"API一覧の導出"</code>
主体(JSON): <code>"as-built設計generator"</code>
対象(JSON): <code>"handler metadataから得た重複のないAPI一覧"</code>
as-built設計generatorは、handler metadataから得た重複のないAPI一覧を**導出する**。
行為enum: <code>"derive"</code>

根拠: route metadataを正本にすると別管理のAPI台帳を不要にできる。
根拠(JSON): <code>"route metadataを正本にすると別管理のAPI台帳を不要にできる。"</code>

項目版: 1 / 状態: `active` / 種別: `functional`
変更識別子: <code>"CHG-20260721-as-built-design"</code>
分類: scope=<code>""</code> / category=<code>""</code>

受入条件:
- <code>"AC-ASBUILT-005-1"</code> 前提: handler decoratorに設計metadataがある。条件: API一覧を生成する。期待結果: operation、API番号、権限、業務概要を重複なく列挙する。
  - criterion(JSON Object): <code>{"given":"handler decoratorに設計metadataがある","id":"AC-ASBUILT-005-1","then":"operation、API番号、権限、業務概要を重複なく列挙する","when":"API一覧を生成する"}</code>

要求源(JSON List): <code>["user:2026-07-21","docs/standards/AS-BUILT-DESIGN.md"]</code>
検証方法: 自動テスト
検証証跡: metadata fixtureからのAPI一覧assert
検証(JSON Object): <code>{"evidence":"metadata fixtureからのAPI一覧assert","method":"自動テスト"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/AS-BUILT-DESIGN.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/SKILL.md","governance/checks/catalog.yaml",".agents/skills/generate-implementation-design/scripts/designflow.py"]</code>
- テスト: <code>["tests/test_review_contract.py","tests/test_designflow.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-006: CRUD関係の導出

要件ID(JSON): <code>"REQ-ASBUILT-006"</code>
タイトル(JSON): <code>"CRUD関係の導出"</code>
主体(JSON): <code>"as-built設計generator"</code>
対象(JSON): <code>"SQLと外部client呼出から得たtableおよび外部連携先のCRUD関係"</code>
as-built設計generatorは、SQLと外部client呼出から得たtableおよび外部連携先のCRUD関係を**導出する**。
行為enum: <code>"derive"</code>

根拠: 静的解析されたデータ操作をAPIへ接続するとCRUD図を手書きせず維持できる。
根拠(JSON): <code>"静的解析されたデータ操作をAPIへ接続するとCRUD図を手書きせず維持できる。"</code>

項目版: 2 / 状態: `active` / 種別: `data`
変更識別子: <code>"CHG-20260829-review-remediation"</code>
分類: scope=<code>""</code> / category=<code>""</code>

受入条件:
- <code>"AC-ASBUILT-006-1"</code> 前提: operationからSQLへの明示mappingと外部client呼出がある。条件: CRUD設計を生成する。期待結果: 明示mappingだけからSELECTをR、INSERTをC、UPDATEをU、DELETEをDとしてtable×APIと外部連携先×APIを生成し、未mapping SQL、parse不能SQLおよびsupport外のMERGEを黙って推定せずstructured unsupportedとして扱う。
  - criterion(JSON Object): <code>{"given":"operationからSQLへの明示mappingと外部client呼出がある","id":"AC-ASBUILT-006-1","then":"明示mappingだけからSELECTをR、INSERTをC、UPDATEをU、DELETEをDとしてtable×APIと外部連携先×APIを生成し、未mapping SQL、parse不能SQLおよびsupport外のMERGEを黙って推定せずstructured unsupportedとして扱う","when":"CRUD設計を生成する"}</code>

要求源(JSON List): <code>["user:2026-07-21","docs/standards/AS-BUILT-DESIGN.md"]</code>
検証方法: 自動テスト
検証証跡: SQLおよびclient fixtureからのCRUD matrix assert
検証(JSON Object): <code>{"evidence":"SQLおよびclient fixtureからのCRUD matrix assert","method":"自動テスト"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/AS-BUILT-DESIGN.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/SKILL.md","governance/checks/catalog.yaml",".agents/skills/generate-implementation-design/scripts/designflow.py"]</code>
- テスト: <code>["tests/test_review_contract.py","tests/test_designflow.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-007: DB設計の導出

要件ID(JSON): <code>"REQ-ASBUILT-007"</code>
タイトル(JSON): <code>"DB設計の導出"</code>
主体(JSON): <code>"as-built設計generator"</code>
対象(JSON): <code>"正本DDLとSQLから得たtable定義とER関係と書込みAPI"</code>
as-built設計generatorは、正本DDLとSQLから得たtable定義とER関係と書込みAPIを**導出する**。
行為enum: <code>"derive"</code>

根拠: DDLとSQLを一次情報にするとDB設計の二重管理を避けられる。
根拠(JSON): <code>"DDLとSQLを一次情報にするとDB設計の二重管理を避けられる。"</code>

項目版: 3 / 状態: `active` / 種別: `data`
変更識別子: <code>"CHG-20260829-review-remediation"</code>
分類: scope=<code>""</code> / category=<code>""</code>

受入条件:
- <code>"AC-ASBUILT-007-1"</code> 前提: repository内に正本DDLとendpoint別SQLがある。条件: DB設計を生成する。期待結果: table、column、constraint、column単位のforeign-key source/targetを含むER関係をDDLから生成し、columnへの書込みAPIをSQL解析から導出する。
  - criterion(JSON Object): <code>{"given":"repository内に正本DDLとendpoint別SQLがある","id":"AC-ASBUILT-007-1","then":"table、column、constraint、column単位のforeign-key source/targetを含むER関係をDDLから生成し、columnへの書込みAPIをSQL解析から導出する","when":"DB設計を生成する"}</code>

要求源(JSON List): <code>["user:2026-07-21","docs/standards/AS-BUILT-DESIGN.md"]</code>
検証方法: 自動テスト
検証証跡: DDLおよびSQL fixtureからのDB設計assert
検証(JSON Object): <code>{"evidence":"DDLおよびSQL fixtureからのDB設計assert","method":"自動テスト"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/AS-BUILT-DESIGN.md"]</code>
- 実装: <code>["governance/checks/catalog.yaml",".agents/skills/generate-implementation-design/scripts/designflow.py"]</code>
- テスト: <code>["tests/test_review_contract.py","tests/test_designflow.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-008: E2E scenario設計の導出

要件ID(JSON): <code>"REQ-ASBUILT-008"</code>
タイトル(JSON): <code>"E2E scenario設計の導出"</code>
主体(JSON): <code>"as-built設計generator"</code>
対象(JSON): <code>"E2E testのGiven When Then構造から得たscenario設計"</code>
as-built設計generatorは、E2E testのGiven When Then構造から得たscenario設計を**導出する**。
行為enum: <code>"derive"</code>

根拠: test codeをscenarioの正本にすると実行可能な仕様と設計表示を一致させられる。
根拠(JSON): <code>"test codeをscenarioの正本にすると実行可能な仕様と設計表示を一致させられる。"</code>

項目版: 2 / 状態: `active` / 種別: `functional`
変更識別子: <code>"CHG-20260802-skills-audit-remediation"</code>
分類: scope=<code>""</code> / category=<code>""</code>

受入条件:
- <code>"AC-ASBUILT-008-1"</code> 前提: E2E testにGiven、When、Then sectionがある。条件: scenario設計を生成する。期待結果: 前提、操作、期待状態をtest codeから順序どおり生成する。
  - criterion(JSON Object): <code>{"given":"E2E testにGiven、When、Then sectionがある","id":"AC-ASBUILT-008-1","then":"前提、操作、期待状態をtest codeから順序どおり生成する","when":"scenario設計を生成する"}</code>

要求源(JSON List): <code>["user:2026-07-21","docs/standards/AS-BUILT-DESIGN.md"]</code>
検証方法: 自動テスト
検証証跡: E2E fixtureからのscenario出力assert
検証(JSON Object): <code>{"evidence":"E2E fixtureからのscenario出力assert","method":"自動テスト"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/AS-BUILT-DESIGN.md"]</code>
- 実装: <code>["governance/checks/catalog.yaml",".agents/skills/generate-implementation-design/scripts/designflow.py"]</code>
- テスト: <code>["tests/test_review_contract.py","tests/test_designflow.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-009: test evidence viewの対象所有集約

要件ID(JSON): <code>"REQ-ASBUILT-009"</code>
タイトル(JSON): <code>"test evidence viewの対象所有集約"</code>
主体(JSON): <code>"as-built設計generator"</code>
対象(JSON): <code>"対象repositoryが所有する結果JSONから得た参照限定test evidence view"</code>
as-built設計generatorは、対象repositoryが所有する結果JSONから得た参照限定test evidence viewを**導出する**。
行為enum: <code>"derive"</code>

根拠: 結果本文を複製せず、localまたは導入先が既に所有し選択したviewだけを使えばportable runtimeへ外部report基盤を強制しない。
根拠(JSON): <code>"結果本文を複製せず、localまたは導入先が既に所有し選択したviewだけを使えばportable runtimeへ外部report基盤を強制しない。"</code>

項目版: 4 / 状態: `active` / 種別: `operational`
変更識別子: <code>"CHG-20260827-quint-three-pillar-guardrails"</code>
分類: scope=<code>"product"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-ASBUILT-009-1"</code> 前提: 対象repositoryが所有するtest結果JSONがある。条件: test evidence viewを生成する。期待結果: status、API response、DB結果、mock受信結果への参照だけを整形し、結果本文を保存せず、新しい外部report基盤を要求しない。
  - criterion(JSON Object): <code>{"given":"対象repositoryが所有するtest結果JSONがある","id":"AC-ASBUILT-009-1","then":"status、API response、DB結果、mock受信結果への参照だけを整形し、結果本文を保存せず、新しい外部report基盤を要求しない","when":"test evidence viewを生成する"}</code>

要求源(JSON List): <code>["user:2026-07-21","user:2026-08-27","docs/standards/AS-BUILT-DESIGN.md"]</code>
検証方法: 契約テスト
検証証跡: report fixtureとrepository非保存規則のassert
検証(JSON Object): <code>{"evidence":"report fixtureとrepository非保存規則のassert","method":"契約テスト"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/AS-BUILT-DESIGN.md"]</code>
- 実装: <code>["governance/checks/catalog.yaml",".agents/skills/generate-implementation-design/scripts/designflow.py"]</code>
- テスト: <code>["tests/test_review_contract.py","tests/test_designflow.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-010: generator tool設計の導出

要件ID(JSON): <code>"REQ-ASBUILT-010"</code>
タイトル(JSON): <code>"generator tool設計の導出"</code>
主体(JSON): <code>"as-built設計generator"</code>
対象(JSON): <code>"tool entrypoint ASTとdocstringから得たCLI仕様とflow"</code>
as-built設計generatorは、tool entrypoint ASTとdocstringから得たCLI仕様とflowを**導出する**。
行為enum: <code>"derive"</code>

根拠: generator自身を同じ方式で可視化すると抽出可能性をdogfoodingできる。
根拠(JSON): <code>"generator自身を同じ方式で可視化すると抽出可能性をdogfoodingできる。"</code>

項目版: 2 / 状態: `active` / 種別: `functional`
変更識別子: <code>"CHG-20260802-skills-audit-remediation"</code>
分類: scope=<code>""</code> / category=<code>""</code>

受入条件:
- <code>"AC-ASBUILT-010-1"</code> 前提: tool entrypointと呼出先関数にdocstringがある。条件: tool設計を生成する。期待結果: CLI argument、制御flow、関数責務をASTとdocstring先頭1行から生成する。
  - criterion(JSON Object): <code>{"given":"tool entrypointと呼出先関数にdocstringがある","id":"AC-ASBUILT-010-1","then":"CLI argument、制御flow、関数責務をASTとdocstring先頭1行から生成する","when":"tool設計を生成する"}</code>

要求源(JSON List): <code>["user:2026-07-21","docs/standards/AS-BUILT-DESIGN.md"]</code>
検証方法: 自動テスト
検証証跡: tool fixtureからのCLIおよびflow assert
検証(JSON Object): <code>{"evidence":"tool fixtureからのCLIおよびflow assert","method":"自動テスト"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/AS-BUILT-DESIGN.md"]</code>
- 実装: <code>["governance/checks/catalog.yaml",".agents/skills/generate-implementation-design/scripts/designflow.py"]</code>
- テスト: <code>["tests/test_review_contract.py","tests/test_designflow.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-011: error case定義の生成

要件ID(JSON): <code>"REQ-ASBUILT-011"</code>
タイトル(JSON): <code>"error case定義の生成"</code>
主体(JSON): <code>"as-built設計generator"</code>
対象(JSON): <code>"API error分岐から得たcatalog全体で一意なID付きmachine-readable error case"</code>
as-built設計generatorは、API error分岐から得たcatalog全体で一意なID付きmachine-readable error caseを**生成する**。
行為enum: <code>"generate"</code>

根拠: error分岐を機械可読にするとE2Eとの1対1 coverageを検査できる。
根拠(JSON): <code>"error分岐を機械可読にするとE2Eとの1対1 coverageを検査できる。"</code>

項目版: 3 / 状態: `active` / 種別: `data`
変更識別子: <code>"CHG-20260829-review-remediation"</code>
分類: scope=<code>""</code> / category=<code>""</code>

受入条件:
- <code>"AC-ASBUILT-011-1"</code> 前提: API handlerに正規化されたerror分岐がある。条件: API設計を生成する。期待結果: 各error分岐へ安定IDを付けたmachine-readable定義を出力し、error IDの重複をoperation内だけでなく生成catalog全体で拒否する。
  - criterion(JSON Object): <code>{"given":"API handlerに正規化されたerror分岐がある","id":"AC-ASBUILT-011-1","then":"各error分岐へ安定IDを付けたmachine-readable定義を出力し、error IDの重複をoperation内だけでなく生成catalog全体で拒否する","when":"API設計を生成する"}</code>

要求源(JSON List): <code>["user:2026-07-21","docs/standards/AS-BUILT-DESIGN.md"]</code>
検証方法: 自動テスト
検証証跡: error branch fixtureからのcase ID出力assert
検証(JSON Object): <code>{"evidence":"error branch fixtureからのcase ID出力assert","method":"自動テスト"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/AS-BUILT-DESIGN.md"]</code>
- 実装: <code>["governance/checks/catalog.yaml",".agents/skills/generate-implementation-design/scripts/designflow.py"]</code>
- テスト: <code>["tests/test_review_contract.py","tests/test_designflow.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-012: 実装仕様sample三点整合

要件ID(JSON): <code>"REQ-ASBUILT-012"</code>
タイトル(JSON): <code>"実装仕様sample三点整合"</code>
主体(JSON): <code>"as-built整合check"</code>
対象(JSON): <code>"handler登録と設計metadataとerror sampleの三点整合"</code>
as-built整合checkは、handler登録と設計metadataとerror sampleの三点整合を**検証する**。
行為enum: <code>"verify"</code>

根拠: 実装、interface情報、設計掲載sampleの片落ちを静的に検出する必要がある。
根拠(JSON): <code>"実装、interface情報、設計掲載sampleの片落ちを静的に検出する必要がある。"</code>

項目版: 2 / 状態: `active` / 種別: `quality`
変更識別子: <code>"CHG-20260802-skills-audit-remediation"</code>
分類: scope=<code>""</code> / category=<code>""</code>

受入条件:
- <code>"AC-ASBUILT-012-1"</code> 前提: API handler、OpenAPI metadata、error sampleがある。条件: 公開API変更の整合checkを実行する。期待結果: handler登録漏れ、metadata欠落、error分岐に対応するsample不足を検出する。
  - criterion(JSON Object): <code>{"given":"API handler、OpenAPI metadata、error sampleがある","id":"AC-ASBUILT-012-1","then":"handler登録漏れ、metadata欠落、error分岐に対応するsample不足を検出する","when":"公開API変更の整合checkを実行する"}</code>

要求源(JSON List): <code>["user:2026-07-21","docs/standards/AS-BUILT-DESIGN.md"]</code>
検証方法: 静的解析
検証証跡: 不整合fixtureを拒否するcheck結果
検証(JSON Object): <code>{"evidence":"不整合fixtureを拒否するcheck結果","method":"静的解析"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/AS-BUILT-DESIGN.md"]</code>
- 実装: <code>["governance/checks/catalog.yaml",".agents/skills/verify-against-engineering-standards/references/as-built-design-check-selection.md",".agents/skills/generate-implementation-design/scripts/qualityflow.py"]</code>
- テスト: <code>["tests/test_review_contract.py","tests/test_qualityflow.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-013: sampleとtestの整合

要件ID(JSON): <code>"REQ-ASBUILT-013"</code>
タイトル(JSON): <code>"sampleとtestの整合"</code>
主体(JSON): <code>"as-built整合check"</code>
対象(JSON): <code>"設計掲載sampleと実response assertionの対応"</code>
as-built整合checkは、設計掲載sampleと実response assertionの対応を**検証する**。
行為enum: <code>"verify"</code>

根拠: 設計書に掲載する例をtest済みに限定すると表示と振る舞いの乖離を防げる。
根拠(JSON): <code>"設計書に掲載する例をtest済みに限定すると表示と振る舞いの乖離を防げる。"</code>

項目版: 2 / 状態: `active` / 種別: `quality`
変更識別子: <code>"CHG-20260802-skills-audit-remediation"</code>
分類: scope=<code>""</code> / category=<code>""</code>

受入条件:
- <code>"AC-ASBUILT-013-1"</code> 前提: 正常または異常response sampleがある。条件: sample整合checkを実行する。期待結果: 各sampleが対応testから参照され、実responseとのassertに使用されていることを検出する。
  - criterion(JSON Object): <code>{"given":"正常または異常response sampleがある","id":"AC-ASBUILT-013-1","then":"各sampleが対応testから参照され、実responseとのassertに使用されていることを検出する","when":"sample整合checkを実行する"}</code>

要求源(JSON List): <code>["user:2026-07-21","docs/standards/AS-BUILT-DESIGN.md"]</code>
検証方法: AST静的解析
検証証跡: 未参照sampleと未assert sampleを拒否するcheck結果
検証(JSON Object): <code>{"evidence":"未参照sampleと未assert sampleを拒否するcheck結果","method":"AST静的解析"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/AS-BUILT-DESIGN.md"]</code>
- 実装: <code>["governance/checks/catalog.yaml",".agents/skills/verify-against-engineering-standards/references/as-built-design-check-selection.md",".agents/skills/generate-implementation-design/scripts/qualityflow.py"]</code>
- テスト: <code>["tests/test_review_contract.py","tests/test_qualityflow.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-014: CRUDとE2E状態検証の整合

要件ID(JSON): <code>"REQ-ASBUILT-014"</code>
タイトル(JSON): <code>"CRUDとE2E状態検証の整合"</code>
主体(JSON): <code>"as-built整合check"</code>
対象(JSON): <code>"DBまたは外部変更effectを持つAPIとeffect別E2E状態assertの対応"</code>
as-built整合checkは、DBまたは外部変更effectを持つAPIとeffect別E2E状態assertの対応を**検証する**。
行為enum: <code>"verify"</code>

根拠: API responseだけでなく永続状態と外部状態を検証してデータ更新の回帰を検出する必要がある。
根拠(JSON): <code>"API responseだけでなく永続状態と外部状態を検証してデータ更新の回帰を検出する必要がある。"</code>

項目版: 3 / 状態: `active` / 種別: `quality`
変更識別子: <code>"CHG-20260827-quint-three-pillar-guardrails"</code>
分類: scope=<code>"product"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-ASBUILT-014-1"</code> 前提: CRUD図でDBまたは外部変更effectを持つAPIがある。条件: CRUD E2E整合checkを実行する。期待結果: DB writeはDB状態、external writeは外部状態を個別にassertし、異常系も各effectの状態不変または理由付き許可変化をassertする。
  - criterion(JSON Object): <code>{"given":"CRUD図でDBまたは外部変更effectを持つAPIがある","id":"AC-ASBUILT-014-1","then":"DB writeはDB状態、external writeは外部状態を個別にassertし、異常系も各effectの状態不変または理由付き許可変化をassertする","when":"CRUD E2E整合checkを実行する"}</code>

要求源(JSON List): <code>["user:2026-07-21","user:2026-08-27","docs/standards/AS-BUILT-DESIGN.md"]</code>
検証方法: 静的解析とE2E契約テスト
検証証跡: 状態assert欠落fixtureを拒否するcheck結果
検証(JSON Object): <code>{"evidence":"状態assert欠落fixtureを拒否するcheck結果","method":"静的解析とE2E契約テスト"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/AS-BUILT-DESIGN.md"]</code>
- 実装: <code>["governance/checks/catalog.yaml",".agents/skills/verify-against-engineering-standards/references/as-built-design-check-selection.md",".agents/skills/generate-implementation-design/scripts/qualityflow.py"]</code>
- テスト: <code>["tests/test_review_contract.py","tests/test_qualityflow.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-015: 解析可能なtest構造

要件ID(JSON): <code>"REQ-ASBUILT-015"</code>
タイトル(JSON): <code>"解析可能なtest構造"</code>
主体(JSON): <code>"導入先repositoryのtest"</code>
対象(JSON): <code>"AAAまたはGWTとdocstringと1 case 1関数を持つtest"</code>
導入先repositoryのtestは、AAAまたはGWTとdocstringと1 case 1関数を持つtestを**構成する**。
行為enum: <code>"structure"</code>

根拠: 構造化されたtest codeをscenario設計とレビュー観点の一次情報にできる。
根拠(JSON): <code>"構造化されたtest codeをscenario設計とレビュー観点の一次情報にできる。"</code>

項目版: 2 / 状態: `active` / 種別: `quality`
変更識別子: <code>"CHG-20260802-skills-audit-remediation"</code>
分類: scope=<code>""</code> / category=<code>""</code>

受入条件:
- <code>"AC-ASBUILT-015-1"</code> 前提: as-built標準を採用したtest codeがある。条件: test構造checkを実行する。期待結果: unit testのAAA、E2EのGWT、docstring、1 case 1関数を評価し、導入時はAdvisoryとして報告する。
  - criterion(JSON Object): <code>{"given":"as-built標準を採用したtest codeがある","id":"AC-ASBUILT-015-1","then":"unit testのAAA、E2EのGWT、docstring、1 case 1関数を評価し、導入時はAdvisoryとして報告する","when":"test構造checkを実行する"}</code>

要求源(JSON List): <code>["user:2026-07-21","docs/standards/AS-BUILT-DESIGN.md"]</code>
検証方法: AST静的解析
検証証跡: test構造fixtureとAdvisory結果
検証(JSON Object): <code>{"evidence":"test構造fixtureとAdvisory結果","method":"AST静的解析"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/AS-BUILT-DESIGN.md"]</code>
- 実装: <code>["governance/checks/catalog.yaml",".agents/skills/verify-against-engineering-standards/references/as-built-design-check-selection.md",".agents/skills/generate-implementation-design/scripts/qualityflow.py"]</code>
- テスト: <code>["tests/test_review_contract.py","tests/test_qualityflow.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-016: unit test coverage目標

要件ID(JSON): <code>"REQ-ASBUILT-016"</code>
タイトル(JSON): <code>"unit test coverage目標"</code>
主体(JSON): <code>"導入先repositoryのunit test"</code>
対象(JSON): <code>"C0命令網羅95%以上とC1分岐網羅90%以上のcoverage"</code>
導入先repositoryのunit testは、C0命令網羅95%以上とC1分岐網羅90%以上のcoverageを**計測する**。
行為enum: <code>"measure"</code>

根拠: 高い命令・分岐網羅を測定目標にしつつ、導入直後のfalse blockerを避けて効果を実測する。
根拠(JSON): <code>"高い命令・分岐網羅を測定目標にしつつ、導入直後のfalse blockerを避けて効果を実測する。"</code>

項目版: 3 / 状態: `active` / 種別: `quality`
変更識別子: <code>"CHG-20260829-review-remediation"</code>
分類: scope=<code>""</code> / category=<code>""</code>

受入条件:
- <code>"AC-ASBUILT-016-1"</code> 前提: as-built標準を採用したunit test suiteがある。条件: coverageを測定する。期待結果: C0 95%以上とC1 90%以上をAdvisoryとして評価し、実測に基づく昇格判断まで無条件blockingにしない。
  - criterion(JSON Object): <code>{"given":"as-built標準を採用したunit test suiteがある","id":"AC-ASBUILT-016-1","then":"C0 95%以上とC1 90%以上をAdvisoryとして評価し、実測に基づく昇格判断まで無条件blockingにしない","when":"coverageを測定する"}</code>

要求源(JSON List): <code>["user:2026-07-21","docs/standards/AS-BUILT-DESIGN.md"]</code>
検証方法: coverage toolとreview contract
検証証跡: C0 C1測定結果への外部CI参照とAdvisory分類
検証(JSON Object): <code>{"evidence":"C0 C1測定結果への外部CI参照とAdvisory分類","method":"coverage toolとreview contract"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/AS-BUILT-DESIGN.md"]</code>
- 実装: <code>["governance/checks/catalog.yaml",".agents/skills/generate-implementation-design/scripts/qualityflow.py"]</code>
- テスト: <code>["tests/test_review_contract.py","tests/test_qualityflow.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-017: as-built check定義の単一正本

要件ID(JSON): <code>"REQ-ASBUILT-017"</code>
タイトル(JSON): <code>"as-built check定義の単一正本"</code>
主体(JSON): <code>"as-built規約"</code>
対象(JSON): <code>"Rule IDからcatalog check IDへ接続された機械可読check定義"</code>
as-built規約は、Rule IDからcatalog check IDへ接続された機械可読check定義を**維持する**。
行為enum: <code>"maintain"</code>

根拠: Markdown tagとcatalogの二重定義を避けるとclass、trigger、enforcementを一か所で変更できる。
根拠(JSON): <code>"Markdown tagとcatalogの二重定義を避けるとclass、trigger、enforcementを一か所で変更できる。"</code>

項目版: 2 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"CHG-20260721-as-built-design"</code>
分類: scope=<code>""</code> / category=<code>""</code>

受入条件:
- <code>"AC-ASBUILT-017-1"</code> 前提: as-built標準に規範Rule IDがある。条件: check mappingを検査する。期待結果: check ID、class、timing、trigger、acceptance、enforcementがcatalogだけで定義され、標準が対応check IDを参照する。
  - criterion(JSON Object): <code>{"given":"as-built標準に規範Rule IDがある","id":"AC-ASBUILT-017-1","then":"check ID、class、timing、trigger、acceptance、enforcementがcatalogだけで定義され、標準が対応check IDを参照する","when":"check mappingを検査する"}</code>

要求源(JSON List): <code>["user:2026-07-21","docs/standards/AS-BUILT-DESIGN.md"]</code>
検証方法: repository契約テスト
検証証跡: 標準Rule IDとcatalog IDの対応assert
検証(JSON Object): <code>{"evidence":"標準Rule IDとcatalog IDの対応assert","method":"repository契約テスト"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/AS-BUILT-DESIGN.md"]</code>
- 実装: <code>["governance/checks/catalog.yaml","docs/standards/AS-BUILT-DESIGN.md"]</code>
- テスト: <code>["tests/test_review_contract.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-018: 抑制例外の可視化

要件ID(JSON): <code>"REQ-ASBUILT-018"</code>
タイトル(JSON): <code>"抑制例外の可視化"</code>
主体(JSON): <code>"as-built規約check"</code>
対象(JSON): <code>"理由付きRule ID抑制箇所の監査一覧"</code>
as-built規約checkは、理由付きRule ID抑制箇所の監査一覧を**生成する**。
行為enum: <code>"generate"</code>

根拠: 例外を一覧化するとsilent suppressionと恒久化した例外を定期監査できる。
根拠(JSON): <code>"例外を一覧化するとsilent suppressionと恒久化した例外を定期監査できる。"</code>

項目版: 2 / 状態: `active` / 種別: `operational`
変更識別子: <code>"CHG-20260802-skills-audit-remediation"</code>
分類: scope=<code>""</code> / category=<code>""</code>

受入条件:
- <code>"AC-ASBUILT-018-1"</code> 前提: コードにignore Rule ID commentがある。条件: 抑制一覧を生成してGovernance Auditを実行する。期待結果: 全抑制path、Rule ID、理由を列挙し、理由欠落、孤児、反復を検出する。
  - criterion(JSON Object): <code>{"given":"コードにignore Rule ID commentがある","id":"AC-ASBUILT-018-1","then":"全抑制path、Rule ID、理由を列挙し、理由欠落、孤児、反復を検出する","when":"抑制一覧を生成してGovernance Auditを実行する"}</code>

要求源(JSON List): <code>["user:2026-07-21","docs/standards/AS-BUILT-DESIGN.md"]</code>
検証方法: 定期repository audit
検証証跡: 抑制inventoryとAUD-008結果
検証(JSON Object): <code>{"evidence":"抑制inventoryとAUD-008結果","method":"定期repository audit"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/AS-BUILT-DESIGN.md"]</code>
- 実装: <code>["governance/checks/catalog.yaml",".agents/skills/generate-implementation-design/scripts/qualityflow.py"]</code>
- テスト: <code>["tests/test_review_contract.py","tests/test_qualityflow.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-019: 選択品質結果の単一軽量集約

要件ID(JSON): <code>"REQ-ASBUILT-019"</code>
タイトル(JSON): <code>"選択品質結果の単一軽量集約"</code>
主体(JSON): <code>"inspect-quality-gates runner"</code>
対象(JSON): <code>"選択したtest・static analysis・規約check・coverageの結果と未検証範囲を示す一つのlocal summaryまたは対象所有view"</code>
inspect-quality-gates runnerは、選択したtest・static analysis・規約check・coverageの結果と未検証範囲を示す一つのlocal summaryまたは対象所有viewを**提供する**。
行為enum: <code>"provide"</code>

根拠: 選択検査の実行runner自体へ結果集約を一本化すれば別report generatorを配布せず、CIを強制せずに証跡範囲と残存riskを追跡できる。
根拠(JSON): <code>"選択検査の実行runner自体へ結果集約を一本化すれば別report generatorを配布せず、CIを強制せずに証跡範囲と残存riskを追跡できる。"</code>

項目版: 4 / 状態: `active` / 種別: `operational`
変更識別子: <code>"CHG-20260829-review-remediation"</code>
分類: scope=<code>"product"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-ASBUILT-019-1"</code> 前提: 品質checkの集合から変更に関係するcheckを選択してinspect runnerで実行する。条件: 品質結果を報告する。期待結果: 選択したcheck、covered acceptance、対象scope、未検証範囲、残存risk、plan digestだけを一つのlocal summaryへ集約し、対象repositoryが既に所有するviewが選択された場合だけそこへ提示し、CI固有pathへ直接書かない。
  - criterion(JSON Object): <code>{"given":"品質checkの集合から変更に関係するcheckを選択してinspect runnerで実行する","id":"AC-ASBUILT-019-1","then":"選択したcheck、covered acceptance、対象scope、未検証範囲、残存risk、plan digestだけを一つのlocal summaryへ集約し、対象repositoryが既に所有するviewが選択された場合だけそこへ提示し、CI固有pathへ直接書かない","when":"品質結果を報告する"}</code>

要求源(JSON List): <code>["user:2026-07-21","user:2026-08-27","docs/standards/AS-BUILT-DESIGN.md"]</code>
検証方法: 契約テスト
検証証跡: inspect result fixture、repository-confined optional JSON、CI固有writeと別report generatorの不存在
検証(JSON Object): <code>{"evidence":"inspect result fixture、repository-confined optional JSON、CI固有writeと別report generatorの不存在","method":"契約テスト"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/AS-BUILT-DESIGN.md"]</code>
- 実装: <code>[".agents/skills/inspect-quality-gates/scripts/inspect.py"]</code>
- テスト: <code>["tests/test_inspect_runner.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-020: 適用対象要件・実装artifact・test nodeの追跡完全性

要件ID(JSON): <code>"REQ-ASBUILT-020"</code>
タイトル(JSON): <code>"適用対象要件・実装artifact・test nodeの追跡完全性"</code>
主体(JSON): <code>"as-built設計generator"</code>
対象(JSON): <code>"schema version 2 trace JSONが適用対象として宣言したactive canonical requirement IDからartifactを経てportable pytest static nodeへ至る完全な明示trace"</code>
as-built設計generatorは、schema version 2 trace JSONが適用対象として宣言したactive canonical requirement IDからartifactを経てportable pytest static nodeへ至る完全な明示traceを**妥当性確認する**。
行為enum: <code>"validate"</code>

根拠: generatorがsupportするsurfaceへ範囲を限定しつつ、宣言された適用対象集合、artifact metadata、lexical no-follow path、生成TEST_MANIFEST.gen.jsonを相互照合して欠落やaliasを許さない。
根拠(JSON): <code>"generatorがsupportするsurfaceへ範囲を限定しつつ、宣言された適用対象集合、artifact metadata、lexical no-follow path、生成TEST_MANIFEST.gen.jsonを相互照合して欠落やaliasを許さない。"</code>

項目版: 2 / 状態: `active` / 種別: `quality`
変更識別子: <code>"CHG-20260829-review-remediation"</code>
分類: scope=<code>"product"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-ASBUILT-020-1"</code> 前提: canonical requirements JSON、schema_version 2と必須applicable_requirement_idsを持つ明示trace JSON、artifact metadata、pytest test sourceがある。条件: as-built設計とTEST_MANIFEST.gen.jsonを生成する。期待結果: applicable_requirement_idsの未知・inactive・duplicate、適用対象の未mapping、対象外要件の余剰mapping、未知artifact、lexical aliasまたはsymlink path、存在しないportable pytest static node、duplicate link、metadataとtraceの片方向不一致を拒否し、宣言集合と完全一致するrequirement→artifact→test node viewと決定的manifestを生成する。
  - criterion(JSON Object): <code>{"given":"canonical requirements JSON、schema_version 2と必須applicable_requirement_idsを持つ明示trace JSON、artifact metadata、pytest test sourceがある","id":"AC-ASBUILT-020-1","then":"applicable_requirement_idsの未知・inactive・duplicate、適用対象の未mapping、対象外要件の余剰mapping、未知artifact、lexical aliasまたはsymlink path、存在しないportable pytest static node、duplicate link、metadataとtraceの片方向不一致を拒否し、宣言集合と完全一致するrequirement→artifact→test node viewと決定的manifestを生成する","when":"as-built設計とTEST_MANIFEST.gen.jsonを生成する"}</code>

要求源(JSON List): <code>["user:2026-08-27","docs/standards/AS-BUILT-DESIGN.md"]</code>
検証方法: 自動テスト
検証証跡: schema v2、applicable集合、lexical no-follow、portable pytest static node、TEST_MANIFEST.gen.jsonのpositive fixtureと各failure mutant
検証(JSON Object): <code>{"evidence":"schema v2、applicable集合、lexical no-follow、portable pytest static node、TEST_MANIFEST.gen.jsonのpositive fixtureと各failure mutant","method":"自動テスト"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/AS-BUILT-DESIGN.md",".agents/skills/generate-implementation-design/references/fastapi-contract.md",".agents/skills/generate-implementation-design/references/cdk-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/scripts/designflow.py"]</code>
- テスト: <code>["tests/test_designflow.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DESIGN-001: FastAPI operation構成

要件ID(JSON): <code>"REQ-DESIGN-001"</code>
タイトル(JSON): <code>"FastAPI operation構成"</code>
主体(JSON): <code>"FastAPI実装フレーム"</code>
対象(JSON): <code>"router.pyのオーケストレーションとfunctions.pyの具体処理に分けたoperation"</code>
FastAPI実装フレームは、router.pyのオーケストレーションとfunctions.pyの具体処理に分けたoperationを**構成する**。
行為enum: <code>"structure"</code>

根拠: 安定したoperation境界により、処理フローの導出と詳細設計の決定的な検査ができる。
根拠(JSON): <code>"安定したoperation境界により、処理フローの導出と詳細設計の決定的な検査ができる。"</code>

項目版: 3 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"WI-20260718-checklist-japanese-docs"</code>
分類: scope=<code>""</code> / category=<code>""</code>

受入条件:
- <code>"AC-DESIGN-001-1"</code> 前提: FastAPI operationを実装している。条件: ソース構成を検査する。期待結果: router.pyが処理の流れを公開し、functions.pyが具体処理を持つ。
  - criterion(JSON Object): <code>{"given":"FastAPI operationを実装している","id":"AC-DESIGN-001-1","then":"router.pyが処理の流れを公開し、functions.pyが具体処理を持つ","when":"ソース構成を検査する"}</code>

要求源(JSON List): <code>["user:2026-07-17"]</code>
検証方法: 自動テスト
検証証跡: routerのAST契約テスト
検証(JSON Object): <code>{"evidence":"routerのAST契約テスト","method":"自動テスト"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/fastapi-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/SKILL.md"]</code>
- テスト: <code>["tests/test_designflow.py"]</code>
- 参照資料: <code>["SWEBOK-V4A"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DESIGN-002: routerからのシーケンス図導出

要件ID(JSON): <code>"REQ-DESIGN-002"</code>
タイトル(JSON): <code>"routerからのシーケンス図導出"</code>
主体(JSON): <code>"設計生成器"</code>
対象(JSON): <code>"FastAPI routerの構文木から得たoperationシーケンス図"</code>
設計生成器は、FastAPI routerの構文木から得たoperationシーケンス図を**導出する**。
行為enum: <code>"derive"</code>

根拠: 実装から導出したフロー文書はソースとの整合を維持できる。
根拠(JSON): <code>"実装から導出したフロー文書はソースとの整合を維持できる。"</code>

項目版: 2 / 状態: `active` / 種別: `functional`
変更識別子: <code>"WI-20260718-checklist-japanese-docs"</code>
分類: scope=<code>""</code> / category=<code>""</code>

受入条件:
- <code>"AC-DESIGN-002-1"</code> 前提: router.pyに有効なroute関数がある。条件: FastAPI設計生成器を実行する。期待結果: 生成Mermaidが実行時の呼出順を保ち、decoratorを除外する。
  - criterion(JSON Object): <code>{"given":"router.pyに有効なroute関数がある","id":"AC-DESIGN-002-1","then":"生成Mermaidが実行時の呼出順を保ち、decoratorを除外する","when":"FastAPI設計生成器を実行する"}</code>

要求源(JSON List): <code>["user:2026-07-17"]</code>
検証方法: 自動テスト
検証証跡: シーケンス出力のアサーション
検証(JSON Object): <code>{"evidence":"シーケンス出力のアサーション","method":"自動テスト"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/fastapi-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/scripts/designflow.py"]</code>
- テスト: <code>["tests/test_designflow.py"]</code>
- 参照資料: <code>["SWEBOK-V4A"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DESIGN-003: OpenAPIからのインターフェース設計導出

要件ID(JSON): <code>"REQ-DESIGN-003"</code>
タイトル(JSON): <code>"OpenAPIからのインターフェース設計導出"</code>
主体(JSON): <code>"設計生成器"</code>
対象(JSON): <code>"OpenAPI文書からのAPIとインターフェースの一覧"</code>
設計生成器は、OpenAPI文書からのAPIとインターフェースの一覧を**導出する**。
行為enum: <code>"derive"</code>

根拠: OpenAPIを実行可能なIF正本とすることで、手作業カタログの重複を避ける。
根拠(JSON): <code>"OpenAPIを実行可能なIF正本とすることで、手作業カタログの重複を避ける。"</code>

項目版: 2 / 状態: `active` / 種別: `interface`
変更識別子: <code>"WI-20260718-checklist-japanese-docs"</code>
分類: scope=<code>""</code> / category=<code>""</code>

受入条件:
- <code>"AC-DESIGN-003-1"</code> 前提: アプリケーションが生成したOpenAPI文書がある。条件: FastAPI設計生成器を実行する。期待結果: operation IDを重複させずにAPI、request、response、schema文書を生成する。
  - criterion(JSON Object): <code>{"given":"アプリケーションが生成したOpenAPI文書がある","id":"AC-DESIGN-003-1","then":"operation IDを重複させずにAPI、request、response、schema文書を生成する","when":"FastAPI設計生成器を実行する"}</code>

要求源(JSON List): <code>["user:2026-07-17","OpenAPI Specification 3.1.1","FastAPI OpenAPI documentation"]</code>
検証方法: 自動テスト
検証証跡: OpenAPI fixtureの出力アサーション
検証(JSON Object): <code>{"evidence":"OpenAPI fixtureの出力アサーション","method":"自動テスト"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/fastapi-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/scripts/designflow.py"]</code>
- テスト: <code>["tests/test_designflow.py"]</code>
- 参照資料: <code>["SWEBOK-V4A"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DESIGN-004: SQLからのデータ設計導出

要件ID(JSON): <code>"REQ-DESIGN-004"</code>
タイトル(JSON): <code>"SQLからのデータ設計導出"</code>
主体(JSON): <code>"設計生成器"</code>
対象(JSON): <code>"生SQLからのquery objectとCRUD文書"</code>
設計生成器は、生SQLからのquery objectとCRUD文書を**解析する**。
行為enum: <code>"parse"</code>

根拠: AST解析は構造的な証跡を作り、無効なSQLを推測せず拒否する。
根拠(JSON): <code>"AST解析は構造的な証跡を作り、無効なSQLを推測せず拒否する。"</code>

項目版: 2 / 状態: `active` / 種別: `data`
変更識別子: <code>"WI-20260718-checklist-japanese-docs"</code>
分類: scope=<code>""</code> / category=<code>""</code>

受入条件:
- <code>"AC-DESIGN-004-1"</code> 前提: 実行可能な生SQLファイルがある。条件: FastAPI設計生成器を実行する。期待結果: SQL構文木からquery objectとtable CRUD関係を生成する。
  - criterion(JSON Object): <code>{"given":"実行可能な生SQLファイルがある","id":"AC-DESIGN-004-1","then":"SQL構文木からquery objectとtable CRUD関係を生成する","when":"FastAPI設計生成器を実行する"}</code>

要求源(JSON List): <code>["user:2026-07-17","SQLGlot documentation"]</code>
検証方法: 自動テスト
検証証跡: SQL AST fixtureとCRUD出力のアサーション
検証(JSON Object): <code>{"evidence":"SQL AST fixtureとCRUD出力のアサーション","method":"自動テスト"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/fastapi-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/scripts/designflow.py"]</code>
- テスト: <code>["tests/test_designflow.py"]</code>
- 参照資料: <code>["SWEBOK-V4A"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DESIGN-005: CDKデプロイ設計の生成

要件ID(JSON): <code>"REQ-DESIGN-005"</code>
タイトル(JSON): <code>"CDKデプロイ設計の生成"</code>
主体(JSON): <code>"設計生成器"</code>
対象(JSON): <code>"合成済みCloudFormationからのresourceとparameter一覧"</code>
設計生成器は、合成済みCloudFormationからのresourceとparameter一覧を**導出する**。
行為enum: <code>"derive"</code>

根拠: 合成されたデプロイテンプレートが具体的なインフラストラクチャIFである。
根拠(JSON): <code>"合成されたデプロイテンプレートが具体的なインフラストラクチャIFである。"</code>

項目版: 2 / 状態: `active` / 種別: `functional`
変更識別子: <code>"WI-20260718-checklist-japanese-docs"</code>
分類: scope=<code>""</code> / category=<code>""</code>

受入条件:
- <code>"AC-DESIGN-005-1"</code> 前提: AWS CDK stackがCloudFormation YAMLまたはJSONを合成している。条件: CDK設計生成器を実行する。期待結果: テンプレートからresourceとparameterの詳細文書を生成する。
  - criterion(JSON Object): <code>{"given":"AWS CDK stackがCloudFormation YAMLまたはJSONを合成している","id":"AC-DESIGN-005-1","then":"テンプレートからresourceとparameterの詳細文書を生成する","when":"CDK設計生成器を実行する"}</code>

要求源(JSON List): <code>["user:2026-07-17","AWS CDK synth documentation","CloudFormation template anatomy"]</code>
検証方法: 自動テスト
検証証跡: CloudFormation fixtureの出力アサーション
検証(JSON Object): <code>{"evidence":"CloudFormation fixtureの出力アサーション","method":"自動テスト"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/cdk-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/scripts/designflow.py"]</code>
- テスト: <code>["tests/test_designflow.py"]</code>
- 参照資料: <code>["AWS-WAF"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DESIGN-006: 実装と設計の差分検出

要件ID(JSON): <code>"REQ-DESIGN-006"</code>
タイトル(JSON): <code>"実装と設計の差分検出"</code>
主体(JSON): <code>"設計フロー"</code>
対象(JSON): <code>"実装成果物と自動生成された詳細設計の差分"</code>
設計フローは、実装成果物と自動生成された詳細設計の差分を**検出する**。
行為enum: <code>"detect"</code>

根拠: digestと決定論的なバイト比較により実装と設計の1対1再現性を強制し、更新漏れの対象pathを特定する。
根拠(JSON): <code>"digestと決定論的なバイト比較により実装と設計の1対1再現性を強制し、更新漏れの対象pathを特定する。"</code>

項目版: 3 / 状態: `active` / 種別: `quality`
変更識別子: <code>"CHG-20260721-as-built-design"</code>
分類: scope=<code>""</code> / category=<code>""</code>

受入条件:
- <code>"AC-DESIGN-006-1"</code> 前提: 宣言済みの自動生成設計がある。条件: 設計check modeを実行する。期待結果: source SHA-256 manifestとクリーンな再生成結果がバイト単位で一致し、差分時は対象pathを列挙して非0終了する。
  - criterion(JSON Object): <code>{"given":"宣言済みの自動生成設計がある","id":"AC-DESIGN-006-1","then":"source SHA-256 manifestとクリーンな再生成結果がバイト単位で一致し、差分時は対象pathを列挙して非0終了する","when":"設計check modeを実行する"}</code>

要求源(JSON List): <code>["user:2026-07-17","user:2026-07-21","docs/standards/AS-BUILT-DESIGN.md"]</code>
検証方法: 自動テスト
検証証跡: 変更済みsourceを用いたdriftと差分pathの検出テスト
検証(JSON Object): <code>{"evidence":"変更済みsourceを用いたdriftと差分pathの検出テスト","method":"自動テスト"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/SKILL.md","docs/standards/AS-BUILT-DESIGN.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/scripts/designflow.py","governance/checks/catalog.yaml"]</code>
- テスト: <code>["tests/test_designflow.py","tests/test_review_contract.py"]</code>
- 参照資料: <code>["SWEBOK-V4A","DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DISC-001: 研究に裏付けられた意図の探索

要件ID(JSON): <code>"REQ-DISC-001"</code>
タイトル(JSON): <code>"研究に裏付けられた意図の探索"</code>
主体(JSON): <code>"開発エージェント"</code>
対象(JSON): <code>"適切な対話を通じたユーザーの意図する成果"</code>
開発エージェントは、適切な対話を通じたユーザーの意図する成果を**探り当てる**。
行為enum: <code>"discover"</code>

根拠: 言語化しきれていない要求を負担なく探り当てるには、心地よい傾聴と精密な言語化が必要である。
根拠(JSON): <code>"言語化しきれていない要求を負担なく探り当てるには、心地よい傾聴と精密な言語化が必要である。"</code>

項目版: 2 / 状態: `active` / 種別: `functional`
変更識別子: <code>"WI-20260718-checklist-japanese-docs"</code>
分類: scope=<code>""</code> / category=<code>""</code>

受入条件:
- <code>"AC-DISC-001-1"</code> 前提: ユーザーの要求が不完全または曖昧である。条件: 解釈差が成果を変える。期待結果: 推定した目的、制約、葛藤、最小限の重要質問を迎合せず提示する。
  - criterion(JSON Object): <code>{"given":"ユーザーの要求が不完全または曖昧である","id":"AC-DISC-001-1","then":"推定した目的、制約、葛藤、最小限の重要質問を迎合せず提示する","when":"解釈差が成果を変える"}</code>

要求源(JSON List): <code>["user:2026-07-17","Design Council Double Diamond","calibrated listening research"]</code>
検証方法: 契約レビュー
検証証跡: Skill指示と研究根拠
検証(JSON Object): <code>{"evidence":"Skill指示と研究根拠","method":"契約レビュー"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/maintain-canonical-requirements/references/research-basis.md"]</code>
- 実装: <code>[".agents/skills/maintain-canonical-requirements/SKILL.md",".agents/skills/calibrated-collaborative-listening/SKILL.md"]</code>
- テスト: <code>["tests/test_skills.py"]</code>
- 参照資料: <code>["SWEBOK-V4A"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DISC-002: 原子的な永続要件

要件ID(JSON): <code>"REQ-DISC-002"</code>
タイトル(JSON): <code>"原子的な永続要件"</code>
主体(JSON): <code>"要件カタログ"</code>
対象(JSON): <code>"正本要件IDごとの一つの原子的な義務"</code>
要件カタログは、正本要件IDごとの一つの原子的な義務を**維持する**。
行為enum: <code>"maintain"</code>

根拠: 原子的な要件は独立した変更、検証、トレーサビリティを可能にする。
根拠(JSON): <code>"原子的な要件は独立した変更、検証、トレーサビリティを可能にする。"</code>

項目版: 4 / 状態: `active` / 種別: `data`
変更識別子: <code>"CHG-20260829-review-remediation"</code>
分類: scope=<code>""</code> / category=<code>""</code>

受入条件:
- <code>"AC-DISC-002-1"</code> 前提: 永続的な義務が受け入れられている。条件: 要件を永続化する。期待結果: 一つのID、主体、正規化action、対象、状態、受入条件、検証、traceを正本に持つ構造的完全性を機械検査し、一つの意味的義務だけを表す原子性は権限あるhuman semantic reviewで確認する。
  - criterion(JSON Object): <code>{"given":"永続的な義務が受け入れられている","id":"AC-DISC-002-1","then":"一つのID、主体、正規化action、対象、状態、受入条件、検証、traceを正本に持つ構造的完全性を機械検査し、一つの意味的義務だけを表す原子性は権限あるhuman semantic reviewで確認する","when":"要件を永続化する"}</code>
- <code>"AC-DISC-002-2"</code> 前提: 要件にdesign、implementationまたはtests traceがある。条件: catalogを検証する。期待結果: 同一category内のduplicate linkとrepository内でlexical no-followにより解決しないpathを拒否する。
  - criterion(JSON Object): <code>{"given":"要件にdesign、implementationまたはtests traceがある","id":"AC-DISC-002-2","then":"同一category内のduplicate linkとrepository内でlexical no-followにより解決しないpathを拒否する","when":"catalogを検証する"}</code>
- <code>"AC-DISC-002-3"</code> 前提: active要件を実装前のrequirements phaseで確定する。条件: catalogを検証してdownstreamへ引き渡す。期待結果: 現時点のsource、verification、既存traceを保持し、まだ存在しないimplementationまたはtests pathを要求せず、下流artifactが作成されたphaseでtraceを独立更新する。
  - criterion(JSON Object): <code>{"given":"active要件を実装前のrequirements phaseで確定する","id":"AC-DISC-002-3","then":"現時点のsource、verification、既存traceを保持し、まだ存在しないimplementationまたはtests pathを要求せず、下流artifactが作成されたphaseでtraceを独立更新する","when":"catalogを検証してdownstreamへ引き渡す"}</code>

要求源(JSON List): <code>["user:2026-07-17","SWEBOK Software Requirements"]</code>
検証方法: 構造自動テストとhuman semantic review
検証証跡: 不完全な構造の拒否記録と、一つのIDが一つの意味的義務だけを表すreview記録
検証(JSON Object): <code>{"evidence":"不完全な構造の拒否記録と、一つのIDが一つの意味的義務だけを表すreview記録","method":"構造自動テストとhuman semantic review"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/maintain-canonical-requirements/assets/requirements.schema.json"]</code>
- 実装: <code>[".agents/skills/maintain-canonical-requirements/scripts/specflow.py"]</code>
- テスト: <code>["tests/test_specflow.py"]</code>
- 参照資料: <code>["SWEBOK-V4A"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DISC-003: 安全な要件ライフサイクル変更

要件ID(JSON): <code>"REQ-DISC-003"</code>
タイトル(JSON): <code>"安全な要件ライフサイクル変更"</code>
主体(JSON): <code>"仕様管理フロー"</code>
対象(JSON): <code>"版と同時更新安全性を保つQuint要件の追加、更新、廃止"</code>
仕様管理フローは、版と同時更新安全性を保つQuint要件の追加、更新、廃止を**維持する**。
行為enum: <code>"maintain"</code>

根拠: 一次言語を一つに保ち、版更新、完全検証、廃止墓標、compare-and-swapにより更新消失と履歴消去を防ぐ。
根拠(JSON): <code>"一次言語を一つに保ち、版更新、完全検証、廃止墓標、compare-and-swapにより更新消失と履歴消去を防ぐ。"</code>

項目版: 6 / 状態: `active` / 種別: `functional`
変更識別子: <code>"CHG-20260829-review-remediation"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-DISC-003-1"</code> 前提: 新しいQuint要件を追加する。条件: 変更を確定する。期待結果: catalogRevisionを一つ進め、対象をactiveかつrevision 1で追加する。
  - criterion(JSON Object): <code>{"given":"新しいQuint要件を追加する","id":"AC-DISC-003-1","then":"catalogRevisionを一つ進め、対象をactiveかつrevision 1で追加する","when":"変更を確定する"}</code>
- <code>"AC-DISC-003-2"</code> 前提: active要件の意味、分類またはverificationを変更する。条件: updateを確定する。期待結果: catalogRevisionと対象revisionをそれぞれ一つ進める。
  - criterion(JSON Object): <code>{"given":"active要件の意味、分類またはverificationを変更する","id":"AC-DISC-003-2","then":"catalogRevisionと対象revisionをそれぞれ一つ進める","when":"updateを確定する"}</code>
- <code>"AC-DISC-003-3"</code> 前提: 正本だった要件の削除が要求される。条件: 変更を受け入れる。期待結果: catalogRevisionと対象revisionをそれぞれ一つ進め、理由付きの廃止墓標として項目を残す。
  - criterion(JSON Object): <code>{"given":"正本だった要件の削除が要求される","id":"AC-DISC-003-3","then":"catalogRevisionと対象revisionをそれぞれ一つ進め、理由付きの廃止墓標として項目を残す","when":"変更を受け入れる"}</code>
- <code>"AC-DISC-003-4"</code> 前提: 生成開始後に別processが派生viewを変更する。条件: 要件JSONとMarkdownを公開する。期待結果: 開始時snapshotとの差を検出して全出力の上書きを拒否する。
  - criterion(JSON Object): <code>{"given":"生成開始後に別processが派生viewを変更する","id":"AC-DISC-003-4","then":"開始時snapshotとの差を検出して全出力の上書きを拒否する","when":"要件JSONとMarkdownを公開する"}</code>
- <code>"AC-DISC-003-5"</code> 前提: Quint要件変更がある。条件: 派生viewを公開する。期待結果: typecheckとcatalog不変条件検査を通した同一catalogからJSONとMarkdownを生成する。
  - criterion(JSON Object): <code>{"given":"Quint要件変更がある","id":"AC-DISC-003-5","then":"typecheckとcatalog不変条件検査を通した同一catalogからJSONとMarkdownを生成する","when":"派生viewを公開する"}</code>
- <code>"AC-DISC-003-6"</code> 前提: catalogRevisionまたは対象revisionが開始時の期待値と異なる。条件: add、update、trace updateまたはretireを試みる。期待結果: staleなcompare-and-swapとしてcatalogを変更せず拒否する。
  - criterion(JSON Object): <code>{"given":"catalogRevisionまたは対象revisionが開始時の期待値と異なる","id":"AC-DISC-003-6","then":"staleなcompare-and-swapとしてcatalogを変更せず拒否する","when":"add、update、trace updateまたはretireを試みる"}</code>
- <code>"AC-DISC-003-7"</code> 前提: retired要件がある。条件: update、trace updateまたは再retireを試みる。期待結果: 墓標を変更せず拒否する。
  - criterion(JSON Object): <code>{"given":"retired要件がある","id":"AC-DISC-003-7","then":"墓標を変更せず拒否する","when":"update、trace updateまたは再retireを試みる"}</code>
- <code>"AC-DISC-003-8"</code> 前提: active要件のtrace集合を変更する。条件: trace updateを確定する。期待結果: 独立したtrace操作としてcatalogRevisionと対象revisionをそれぞれ一つ進める。
  - criterion(JSON Object): <code>{"given":"active要件のtrace集合を変更する","id":"AC-DISC-003-8","then":"独立したtrace操作としてcatalogRevisionと対象revisionをそれぞれ一つ進める","when":"trace updateを確定する"}</code>
- <code>"AC-DISC-003-9"</code> 前提: activeまたはretired要件がある。条件: retirement fieldsを検証する。期待結果: activeのretirementReasonとsupersededByは空であり、retiredは理由を持ち、superseded chainはcatalog順で前進して循環せず、最終的にactive要件へ到達する。
  - criterion(JSON Object): <code>{"given":"activeまたはretired要件がある","id":"AC-DISC-003-9","then":"activeのretirementReasonとsupersededByは空であり、retiredは理由を持ち、superseded chainはcatalog順で前進して循環せず、最終的にactive要件へ到達する","when":"retirement fieldsを検証する"}</code>
- <code>"AC-DISC-003-10"</code> 前提: 一つのchangeに異なる要件への複数operationがある。条件: atomic batchを確定する。期待結果: catalogRevisionを一つだけ進め、各対象revisionを一つ進め、同一要件の二重touchまたはいずれかのstale CAS・不正値があればbatch全体を変更せず拒否する。
  - criterion(JSON Object): <code>{"given":"一つのchangeに異なる要件への複数operationがある","id":"AC-DISC-003-10","then":"catalogRevisionを一つだけ進め、各対象revisionを一つ進め、同一要件の二重touchまたはいずれかのstale CAS・不正値があればbatch全体を変更せず拒否する","when":"atomic batchを確定する"}</code>

要求源(JSON List): <code>["user:2026-07-17","user:2026-08-27","user:2026-08-29"]</code>
検証方法: Quint検証と自動テスト
検証証跡: add、update、trace update、retireの版遷移、CAS競合、型、生成drift、廃止墓標の検査
検証(JSON Object): <code>{"evidence":"add、update、trace update、retireの版遷移、CAS競合、型、生成drift、廃止墓標の検査","method":"Quint検証と自動テスト"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/maintain-canonical-requirements/SKILL.md"]</code>
- 実装: <code>["spec/requirements/requirements.qnt","tools/quintflow.py","tools/safe_io.py",".agents/skills/maintain-canonical-requirements/scripts/specflow.py"]</code>
- テスト: <code>["tests/test_quintflow.py","tests/test_specflow.py"]</code>
- 参照資料: <code>["SWEBOK-V4A","QUINT-0.32"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DISC-004: 要件文書の自動生成

要件ID(JSON): <code>"REQ-DISC-004"</code>
タイトル(JSON): <code>"要件文書の自動生成"</code>
主体(JSON): <code>"仕様管理フロー"</code>
対象(JSON): <code>"QuintからJSONを経由した日本語の人間向け要件文書"</code>
仕様管理フローは、QuintからJSONを経由した日本語の人間向け要件文書を**生成する**。
行為enum: <code>"generate"</code>

根拠: 生成ビューは競合する編集可能な正本を作らずに読者へ情報を提供する。
根拠(JSON): <code>"生成ビューは競合する編集可能な正本を作らずに読者へ情報を提供する。"</code>

項目版: 5 / 状態: `active` / 種別: `functional`
変更識別子: <code>"CHG-20260829-review-remediation"</code>
分類: scope=<code>"product"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-DISC-004-1"</code> 前提: Quint正本が有効である。条件: 文書生成と差分検査を実行する。期待結果: QuintからList順と空文字fieldを含む全fieldを保持したserialized JSONを生成し、そのserialized JSONを再parseした値だけから日本語文書をバイト一致で再現する。
  - criterion(JSON Object): <code>{"given":"Quint正本が有効である","id":"AC-DISC-004-1","then":"QuintからList順と空文字fieldを含む全fieldを保持したserialized JSONを生成し、そのserialized JSONを再parseした値だけから日本語文書をバイト一致で再現する","when":"文書生成と差分検査を実行する"}</code>
- <code>"AC-DISC-004-2"</code> 前提: QuintとJSONで各fieldに異なるgolden値、空optional値、順序の異なる複数要件がある。条件: 写像と逆写像を検査する。期待結果: catalog、要件、受入条件、verification、全trace、分類、廃止情報の各fieldとList順が欠落や入替えなく往復し、Markdown意味へ対応する。
  - criterion(JSON Object): <code>{"given":"QuintとJSONで各fieldに異なるgolden値、空optional値、順序の異なる複数要件がある","id":"AC-DISC-004-2","then":"catalog、要件、受入条件、verification、全trace、分類、廃止情報の各fieldとList順が欠落や入替えなく往復し、Markdown意味へ対応する","when":"写像と逆写像を検査する"}</code>

要求源(JSON List): <code>["user:2026-07-17","user:2026-08-27","user:2026-08-29"]</code>
検証方法: 自動テスト
検証証跡: 全field golden mapping、serialized JSON入力境界、Given When Then意味、生成文書の完全一致検査
検証(JSON Object): <code>{"evidence":"全field golden mapping、serialized JSON入力境界、Given When Then意味、生成文書の完全一致検査","method":"自動テスト"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/requirements/REQUIREMENTS.md"]</code>
- 実装: <code>["tools/quintflow.py","tools/spec_mapping.py","tools/render_requirements.py",".agents/skills/maintain-canonical-requirements/scripts/specflow.py"]</code>
- テスト: <code>["tests/test_quintflow.py","tests/test_specflow.py"]</code>
- 参照資料: <code>["SWEBOK-V4A","QUINT-0.32"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DISC-005: solution候補と永続要件の境界

要件ID(JSON): <code>"REQ-DISC-005"</code>
タイトル(JSON): <code>"solution候補と永続要件の境界"</code>
主体(JSON): <code>"要件管理Skill"</code>
対象(JSON): <code>"solution候補と権限ある永続要件"</code>
要件管理Skillは、solution候補と権限ある永続要件を**分離する**。
行為enum: <code>"separate"</code>

根拠: 結果や品質ではなく可逆な実装手段を正本へ固定すると設計裁量と変更容易性を失う一方、契約、法令、互換性、既存基盤、support境界または親判断に基づく正当な制約は保持する必要があるため。
根拠(JSON): <code>"結果や品質ではなく可逆な実装手段を正本へ固定すると設計裁量と変更容易性を失う一方、契約、法令、互換性、既存基盤、support境界または親判断に基づく正当な制約は保持する必要があるため。"</code>

項目版: 2 / 状態: `active` / 種別: `functional`
変更識別子: <code>"CHG-20260829-review-remediation"</code>
分類: scope=<code>"product"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-DISC-005-1"</code> 前提: technology、architecture、tool、path、process、工程または成果物を名指しする要件候補がある。条件: 正本への反映可否を判定する。期待結果: underlying outcome、necessity、authority、lifetime、scope、placementを判定し、可逆なsolution choiceを永続要件へ固定しない。
  - criterion(JSON Object): <code>{"given":"technology、architecture、tool、path、process、工程または成果物を名指しする要件候補がある","id":"AC-DISC-005-1","then":"underlying outcome、necessity、authority、lifetime、scope、placementを判定し、可逆なsolution choiceを永続要件へ固定しない","when":"正本への反映可否を判定する"}</code>
- <code>"AC-DISC-005-2"</code> 前提: exact technology、architectureまたはproject process自体が権限ある永続制約である。条件: 永続要件として保持する。期待結果: source_refs、必要性を示すrationale、scopeとcategory、verificationを記録する。
  - criterion(JSON Object): <code>{"given":"exact technology、architectureまたはproject process自体が権限ある永続制約である","id":"AC-DISC-005-2","then":"source_refs、必要性を示すrationale、scopeとcategory、verificationを記録する","when":"永続要件として保持する"}</code>
- <code>"AC-DISC-005-3"</code> 前提: 親要件または承認済みarchitecture decisionが下位scopeを拘束する。条件: 下位の永続義務として保持する。期待結果: 親要件またはdecision、下位scope、verificationへtraceしたderived requirementとして記録し、上位stakeholder requirementへ過剰一般化しない。
  - criterion(JSON Object): <code>{"given":"親要件または承認済みarchitecture decisionが下位scopeを拘束する","id":"AC-DISC-005-3","then":"親要件またはdecision、下位scope、verificationへtraceしたderived requirementとして記録し、上位stakeholder requirementへ過剰一般化しない","when":"下位の永続義務として保持する"}</code>

要求源(JSON List): <code>["user:2026-07-24","issue:25","NASA Systems Engineering Handbook Appendix","NASA SWE-050","SWEBOK-V4A","Nuseibeh:10.1109/2.910904","Chen-Babar-Nuseibeh:10.1109/MS.2012.174"]</code>
検証方法: 自動テスト
検証証跡: solution-only instruction、権限あるtechnology constraint、quality-of-service、ADR、derived requirement、product identityのpositive / negative contract test
検証(JSON Object): <code>{"evidence":"solution-only instruction、権限あるtechnology constraint、quality-of-service、ADR、derived requirement、product identityのpositive / negative contract test","method":"自動テスト"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/REQUIREMENT-CLASSIFICATION.md","docs/reference/development.md",".agents/skills/maintain-canonical-requirements/references/research-basis.md"]</code>
- 実装: <code>[".agents/skills/maintain-canonical-requirements/SKILL.md",".agents/skills/chat-first-development/SKILL.md",".agents/skills/elicit-frontend-requirements/SKILL.md",".agents/skills/maintain-canonical-requirements/assets/requirements.schema.json"]</code>
- テスト: <code>["tests/test_skills.py","tests/test_specflow.py"]</code>
- 参照資料: <code>["SWEBOK-V4A"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DOCS-001: 日本語の利用者向け文書

要件ID(JSON): <code>"REQ-DOCS-001"</code>
タイトル(JSON): <code>"日本語の利用者向け文書"</code>
主体(JSON): <code>"文書生成フロー"</code>
対象(JSON): <code>"識別子と固有名詞を除いて日本語で統一された利用者向け文書"</code>
文書生成フローは、識別子と固有名詞を除いて日本語で統一された利用者向け文書を**提供する**。
行為enum: <code>"provide"</code>

根拠: 導入・運用・監査の文書言語を統一し、意味の取り違えと二重保守を防ぐ。
根拠(JSON): <code>"導入・運用・監査の文書言語を統一し、意味の取り違えと二重保守を防ぐ。"</code>

項目版: 1 / 状態: `active` / 種別: `quality`
変更識別子: <code>"WI-20260718-checklist-japanese-docs"</code>
分類: scope=<code>""</code> / category=<code>""</code>

受入条件:
- <code>"AC-DOCS-001-1"</code> 前提: 利用者向けMarkdownまたは生成文書がある。条件: リポジトリ検証を実行する。期待結果: 見出しと説明が日本語であり、生成物が日本語テンプレートから再現される。
  - criterion(JSON Object): <code>{"given":"利用者向けMarkdownまたは生成文書がある","id":"AC-DOCS-001-1","then":"見出しと説明が日本語であり、生成物が日本語テンプレートから再現される","when":"リポジトリ検証を実行する"}</code>

要求源(JSON List): <code>["user:2026-07-18"]</code>
検証方法: 自動検査
検証証跡: 日本語文書検査と生成差分テスト
検証(JSON Object): <code>{"evidence":"日本語文書検査と生成差分テスト","method":"自動検査"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/README.md"]</code>
- 実装: <code>[".agents/skills/maintain-canonical-requirements/scripts/specflow.py",".agents/skills/verify-against-engineering-standards/scripts/standardsflow.py"]</code>
- テスト: <code>["tests/test_validate_repo.py","tests/test_specflow.py","tests/test_standardsflow.py"]</code>
- 参照資料: <code>["SWEBOK-V4A"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-EXEC-001: 多軸execution profileの推定

要件ID(JSON): <code>"REQ-EXEC-001"</code>
タイトル(JSON): <code>"多軸execution profileの推定"</code>
主体(JSON): <code>"開発実行基盤"</code>
対象(JSON): <code>"相互に独立した変更範囲、保証水準、計算資源および実行方式"</code>
開発実行基盤は、相互に独立した変更範囲、保証水準、計算資源および実行方式を**推定する**。
行為enum: <code>"estimate"</code>

根拠: 局所的だが重大な変更と、広範囲だが機械的な変更を単一レベルで混同しないため。
根拠(JSON): <code>"局所的だが重大な変更と、広範囲だが機械的な変更を単一レベルで混同しないため。"</code>

項目版: 3 / 状態: `active` / 種別: `operational`
変更識別子: <code>"user:2026-08-29"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-EXEC-001-1"</code> 前提: repository変更依頼と決定的metadataがある。条件: 実装前profileを生成する。期待結果: scope、assurance、compute、modeを直接根拠とともに独立記録し、同一入力とpolicyからtimestampを除く同一decision projectionを生成する。
  - criterion(JSON Object): <code>{"given":"repository変更依頼と決定的metadataがある","id":"AC-EXEC-001-1","then":"scope、assurance、compute、modeを直接根拠とともに独立記録し、同一入力とpolicyからtimestampを除く同一decision projectionを生成する","when":"実装前profileを生成する"}</code>

要求源(JSON List): <code>["user:2026-07-18","user:2026-08-29","arXiv:2607.13034","arXiv:2407.01489"]</code>
検証方法: 自動テスト
検証証跡: 多軸独立性、schema適合性および再現性の回帰テスト
検証(JSON Object): <code>{"evidence":"多軸独立性、schema適合性および再現性の回帰テスト","method":"自動テスト"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/right-size-execution/references/execution-dimensions.md"]</code>
- 実装: <code>[".agents/skills/right-size-execution/scripts/executionflow.py",".agents/skills/right-size-execution/assets/execution-policy.json",".agents/skills/right-size-execution/assets/execution-profile.schema.json"]</code>
- テスト: <code>["tests/test_executionflow.py"]</code>
- 参照資料: <code>["SWEBOK-V4A"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-EXEC-002: 保証水準の下限制御

要件ID(JSON): <code>"REQ-EXEC-002"</code>
タイトル(JSON): <code>"保証水準の下限制御"</code>
主体(JSON): <code>"開発実行基盤"</code>
対象(JSON): <code>"risk tag、成果物、外部副作用および不可逆性から導出したassurance下限"</code>
開発実行基盤は、risk tag、成果物、外部副作用および不可逆性から導出したassurance下限を**強制する**。
行為enum: <code>"enforce"</code>

根拠: 重大性は探索範囲ではなく必要な保証の深さへ反映すべきである。
根拠(JSON): <code>"重大性は探索範囲ではなく必要な保証の深さへ反映すべきである。"</code>

項目版: 3 / 状態: `active` / 種別: `quality`
変更識別子: <code>"user:2026-08-29"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-EXEC-002-1"</code> 前提: risk tagと成果物tagがある。条件: assuranceを推定または監査する。期待結果: 両集合のassurance floorの高い方を採用し、高riskだけでscopeを広げない。
  - criterion(JSON Object): <code>{"given":"risk tagと成果物tagがある","id":"AC-EXEC-002-1","then":"両集合のassurance floorの高い方を採用し、高riskだけでscopeを広げない","when":"assuranceを推定または監査する"}</code>

要求源(JSON List): <code>["user:2026-07-18","user:2026-08-29","SWEBOK-V4A"]</code>
検証方法: 自動テスト
検証証跡: artifact-only elevated、risk-wins critical、local-criticalの交差ケース
検証(JSON Object): <code>{"evidence":"artifact-only elevated、risk-wins critical、local-criticalの交差ケース","method":"自動テスト"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/right-size-execution/references/execution-dimensions.md"]</code>
- 実装: <code>[".agents/skills/right-size-execution/scripts/executionflow.py",".agents/skills/right-size-execution/assets/execution-policy.json"]</code>
- テスト: <code>["tests/test_executionflow.py"]</code>
- 参照資料: <code>["SWEBOK-V4A"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-EXEC-003: 追加LLM呼出しを伴わない初期推定

要件ID(JSON): <code>"REQ-EXEC-003"</code>
タイトル(JSON): <code>"追加LLM呼出しを伴わない初期推定"</code>
主体(JSON): <code>"開発実行基盤"</code>
対象(JSON): <code>"通常のルート判断と決定的metadataによる初期Estimate"</code>
開発実行基盤は、通常のルート判断と決定的metadataによる初期Estimateを**経路選択する**。
行為enum: <code>"route"</code>

根拠: Estimate自体が余分なLLMコストになり、単純な作業の利点を失うことを防ぐため。
根拠(JSON): <code>"Estimate自体が余分なLLMコストになり、単純な作業の利点を失うことを防ぐため。"</code>

項目版: 3 / 状態: `active` / 種別: `quality`
変更識別子: <code>"WI-20260718-right-size-execution-v2"</code>
分類: scope=<code>""</code> / category=<code>""</code>

受入条件:
- <code>"AC-EXEC-003-1"</code> 前提: 依頼文、path、manifestまたは依存metadataがある。条件: 初期profileを推定する。期待結果: Estimate専用LLMを呼ばず、結果を変える不明点だけmetadata probeを最大一回実行して費用を記録する。
  - criterion(JSON Object): <code>{"given":"依頼文、path、manifestまたは依存metadataがある","id":"AC-EXEC-003-1","then":"Estimate専用LLMを呼ばず、結果を変える不明点だけmetadata probeを最大一回実行して費用を記録する","when":"初期profileを推定する"}</code>

要求源(JSON List): <code>["user:2026-07-18","ACL:2024.naacl-long.389"]</code>
検証方法: 自動テスト
検証証跡: probe上限、再利用可能なprobe証拠およびEstimate overheadの検査
検証(JSON Object): <code>{"evidence":"probe上限、再利用可能なprobe証拠およびEstimate overheadの検査","method":"自動テスト"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/right-size-execution/SKILL.md"]</code>
- 実装: <code>[".agents/skills/right-size-execution/scripts/executionflow.py"]</code>
- テスト: <code>["tests/test_executionflow.py"]</code>
- 参照資料: <code>["SWEBOK-V4A"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-EXEC-004: 校正可能な確信度

要件ID(JSON): <code>"REQ-EXEC-004"</code>
タイトル(JSON): <code>"校正可能な確信度"</code>
主体(JSON): <code>"開発実行基盤"</code>
対象(JSON): <code>"実行制御へ入力するconfidenceの根拠とscore"</code>
開発実行基盤は、実行制御へ入力するconfidenceの根拠とscoreを**制約する**。
行為enum: <code>"constrain"</code>

根拠: 未校正のLLM自己申告値を閾値判定に使わず、観測特徴または実績で校正したrouterだけを使うため。
根拠(JSON): <code>"未校正のLLM自己申告値を閾値判定に使わず、観測特徴または実績で校正したrouterだけを使うため。"</code>

項目版: 2 / 状態: `active` / 種別: `quality`
変更識別子: <code>"WI-20260718-right-size-execution-v2"</code>
分類: scope=<code>""</code> / category=<code>""</code>

受入条件:
- <code>"AC-EXEC-004-1"</code> 前提: 校正済みrouterが未導入である。条件: confidenceを記録する。期待結果: deterministic feature evidenceとbandを記録しscoreをnullにする。
  - criterion(JSON Object): <code>{"given":"校正済みrouterが未導入である","id":"AC-EXEC-004-1","then":"deterministic feature evidenceとbandを記録しscoreをnullにする","when":"confidenceを記録する"}</code>

要求源(JSON List): <code>["user:2026-07-18","arXiv:2406.18665"]</code>
検証方法: 自動テスト
検証証跡: 任意の自己申告scoreを拒否するschema・回帰テスト
検証(JSON Object): <code>{"evidence":"任意の自己申告scoreを拒否するschema・回帰テスト","method":"自動テスト"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/right-size-execution/references/execution-dimensions.md"]</code>
- 実装: <code>[".agents/skills/right-size-execution/assets/execution-profile.schema.json",".agents/skills/right-size-execution/scripts/executionflow.py"]</code>
- テスト: <code>["tests/test_executionflow.py"]</code>
- 参照資料: <code>["SWEBOK-V4A"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-EXEC-005: 最小十分な検証の導出

要件ID(JSON): <code>"REQ-EXEC-005"</code>
タイトル(JSON): <code>"最小十分な検証の導出"</code>
主体(JSON): <code>"開発実行基盤"</code>
対象(JSON): <code>"scope、assurance、成果物、risk、受入条件および対象repositoryが明示したgateの完全一致するverification projection"</code>
開発実行基盤は、scope、assurance、成果物、risk、受入条件および対象repositoryが明示したgateの完全一致するverification projectionを**導出する**。
行為enum: <code>"derive"</code>

根拠: 機能影響の広さと必要保証の深さを分離しながら、重大な検証漏れを防ぐため。
根拠(JSON): <code>"機能影響の広さと必要保証の深さを分離しながら、重大な検証漏れを防ぐため。"</code>

項目版: 2 / 状態: `active` / 種別: `quality`
変更識別子: <code>"user:2026-08-29"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-EXEC-005-1"</code> 前提: schema適合profileと受入条件がある。条件: 検証集合を導出する。期待結果: scope、assurance、成果物、risk、受入条件および対象repositoryが明示したgateの決定的和集合だけをblocking集合とし、追加diagnosticを別のadvisory集合へ分離する。
  - criterion(JSON Object): <code>{"given":"schema適合profileと受入条件がある","id":"AC-EXEC-005-1","then":"scope、assurance、成果物、risk、受入条件および対象repositoryが明示したgateの決定的和集合だけをblocking集合とし、追加diagnosticを別のadvisory集合へ分離する","when":"検証集合を導出する"}</code>

要求源(JSON List): <code>["user:2026-07-18","user:2026-08-29","SWEBOK-V4A"]</code>
検証方法: 自動テスト
検証証跡: projection component、余分または不足checkの成功拒否、diagnostic非blocking
検証(JSON Object): <code>{"evidence":"projection component、余分または不足checkの成功拒否、diagnostic非blocking","method":"自動テスト"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/right-size-execution/references/execution-dimensions.md"]</code>
- 実装: <code>[".agents/skills/right-size-execution/scripts/executionflow.py"]</code>
- テスト: <code>["tests/test_executionflow.py"]</code>
- 参照資料: <code>["SWEBOK-V4A"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-EXEC-006: 根拠付きの単軸Expand

要件ID(JSON): <code>"REQ-EXEC-006"</code>
タイトル(JSON): <code>"根拠付きの単軸Expand"</code>
主体(JSON): <code>"開発実行基盤"</code>
対象(JSON): <code>"初期profileを覆す新証拠に対応する一つの実行軸"</code>
開発実行基盤は、初期profileを覆す新証拠に対応する一つの実行軸を**拡張する**。
行為enum: <code>"expand"</code>

根拠: 推定誤りを回復しながら、無関係な軸の同時拡張と一律回数上限による回復阻害を防ぐため。
根拠(JSON): <code>"推定誤りを回復しながら、無関係な軸の同時拡張と一律回数上限による回復阻害を防ぐため。"</code>

項目版: 2 / 状態: `active` / 種別: `quality`
変更識別子: <code>"user:2026-08-29"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-EXEC-006-1"</code> 前提: 許可理由と直接証拠がある。条件: profileを拡張する。期待結果: scope、assurance、verification、review、computeのうち一軸だけを変更し、stable failure identityの再登場をstagnationとして拒否し、各eventを前event digestへ連結する。
  - criterion(JSON Object): <code>{"given":"許可理由と直接証拠がある","id":"AC-EXEC-006-1","then":"scope、assurance、verification、review、computeのうち一軸だけを変更し、stable failure identityの再登場をstagnationとして拒否し、各eventを前event digestへ連結する","when":"profileを拡張する"}</code>

要求源(JSON List): <code>["user:2026-07-18","user:2026-08-29","arXiv:2607.13034"]</code>
検証方法: 自動テスト
検証証跡: 12回diagnosticのcount cap不存在、同identity別文言拒否、expansion chain tamperの回帰テスト
検証(JSON Object): <code>{"evidence":"12回diagnosticのcount cap不存在、同identity別文言拒否、expansion chain tamperの回帰テスト","method":"自動テスト"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/right-size-execution/references/expansion-contract.md"]</code>
- 実装: <code>[".agents/skills/right-size-execution/scripts/executionflow.py"]</code>
- テスト: <code>["tests/test_executionflow.py"]</code>
- 参照資料: <code>["SWEBOK-V4A"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-EXEC-007: 成功後の停止

要件ID(JSON): <code>"REQ-EXEC-007"</code>
タイトル(JSON): <code>"成功後の停止"</code>
主体(JSON): <code>"開発実行基盤"</code>
対象(JSON): <code>"成功条件、required verificationおよびassurance floor充足後の正のコスト活動"</code>
開発実行基盤は、成功条件、required verificationおよびassurance floor充足後の正のコスト活動を**停止する**。
行為enum: <code>"stop"</code>

根拠: 成功後の念のための探索や能力引上げを防ぎ、必須確定処理だけを許可するため。
根拠(JSON): <code>"成功後の念のための探索や能力引上げを防ぎ、必須確定処理だけを許可するため。"</code>

項目版: 2 / 状態: `active` / 種別: `quality`
変更識別子: <code>"user:2026-08-29"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-EXEC-007-1"</code> 前提: 選択projectionと完全一致するverificationがassurance-aligned modeで成功した。条件: decisive successを記録する。期待結果: projection、assurance、selector、全expansion chainを結ぶstop digestを作り、成功後expandを拒否またはpost-success活動として監査する。
  - criterion(JSON Object): <code>{"given":"選択projectionと完全一致するverificationがassurance-aligned modeで成功した","id":"AC-EXEC-007-1","then":"projection、assurance、selector、全expansion chainを結ぶstop digestを作り、成功後expandを拒否またはpost-success活動として監査する","when":"decisive successを記録する"}</code>

要求源(JSON List): <code>["user:2026-07-18","user:2026-08-29","arXiv:2607.13034"]</code>
検証方法: 自動テスト
検証証跡: 検証の不足または余分を伴う成功拒否、stop digest tamper、成功後Expand拒否
検証(JSON Object): <code>{"evidence":"検証の不足または余分を伴う成功拒否、stop digest tamper、成功後Expand拒否","method":"自動テスト"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/right-size-execution/references/stopping-contract.md"]</code>
- 実装: <code>[".agents/skills/right-size-execution/scripts/executionflow.py"]</code>
- テスト: <code>["tests/test_executionflow.py"]</code>
- 参照資料: <code>["SWEBOK-V4A"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-EXEC-008: 実行効率の計測

要件ID(JSON): <code>"REQ-EXEC-008"</code>
タイトル(JSON): <code>"実行効率の計測"</code>
主体(JSON): <code>"開発実行基盤"</code>
対象(JSON): <code>"明示選択時だけの推定、Estimate overhead、実績、Expand、品質および停止後活動の任意計測"</code>
開発実行基盤は、明示選択時だけの推定、Estimate overhead、実績、Expand、品質および停止後活動の任意計測を**計測する**。
行為enum: <code>"measure"</code>

根拠: 成功率と重大欠陥を制約にし、oracleなしの単一効率指標へ過適合しないため。
根拠(JSON): <code>"成功率と重大欠陥を制約にし、oracleなしの単一効率指標へ過適合しないため。"</code>

項目版: 2 / 状態: `active` / 種別: `quality`
変更識別子: <code>"user:2026-08-29"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-EXEC-008-1"</code> 前提: 利用者がtelemetry、benchmark、calibrationまたはauditを明示選択している。条件: 効率reportを確定する。期待結果: tokenまたはproxy、時間、tool、read、probe、Expand、model、成功、escaped defectおよび停止後活動を保存し、oracleなしでACRRを表明せず、通常作業に永続台帳を要求しない。
  - criterion(JSON Object): <code>{"given":"利用者がtelemetry、benchmark、calibrationまたはauditを明示選択している","id":"AC-EXEC-008-1","then":"tokenまたはproxy、時間、tool、read、probe、Expand、model、成功、escaped defectおよび停止後活動を保存し、oracleなしでACRRを表明せず、通常作業に永続台帳を要求しない","when":"効率reportを確定する"}</code>

要求源(JSON List): <code>["user:2026-07-18","user:2026-08-29","arXiv:2607.13034"]</code>
検証方法: 自動テストとbenchmark
検証証跡: 生指標、overrun、proxyおよびACRR境界の検査
検証(JSON Object): <code>{"evidence":"生指標、overrun、proxyおよびACRR境界の検査","method":"自動テストとbenchmark"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/right-size-execution/references/measurement-contract.md"]</code>
- 実装: <code>[".agents/skills/right-size-execution/scripts/executionflow.py"]</code>
- テスト: <code>["tests/test_executionflow.py"]</code>
- 参照資料: <code>["SWEBOK-V4A"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-EXEC-009: 監査可能なチェック選択

要件ID(JSON): <code>"REQ-EXEC-009"</code>
タイトル(JSON): <code>"監査可能なチェック選択"</code>
主体(JSON): <code>"標準検証基盤"</code>
対象(JSON): <code>"version固定selectorによるチェック候補と選択漏れ監査sample"</code>
標準検証基盤は、version固定selectorによるチェック候補と選択漏れ監査sampleを**選択する**。
行為enum: <code>"select"</code>

根拠: 未選択とN/Aを分離し、削減件数だけでなく重大controlの偽陰性を監査するため。
根拠(JSON): <code>"未選択とN/Aを分離し、削減件数だけでなく重大controlの偽陰性を監査するため。"</code>

項目版: 3 / 状態: `active` / 種別: `quality`
変更識別子: <code>"CHG-20260829-review-remediation"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-EXEC-009-1"</code> 前提: execution profileとversion固定catalogがある。条件: チェック候補を選択する。期待結果: assurance、artifact、risk、phase、changed path、対象所有gateから選び、各selected IDの選択根拠、入力、選択digest、除外数、決定的監査sample、mandatory missを保存し、CASでcommitmentを維持する。
  - criterion(JSON Object): <code>{"given":"execution profileとversion固定catalogがある","id":"AC-EXEC-009-1","then":"assurance、artifact、risk、phase、changed path、対象所有gateから選び、各selected IDの選択根拠、入力、選択digest、除外数、決定的監査sample、mandatory missを保存し、CASでcommitmentを維持する","when":"チェック候補を選択する"}</code>

要求源(JSON List): <code>["user:2026-07-18","user:2026-08-29","SWEBOK-V4A"]</code>
検証方法: 自動テストとbenchmark
検証証跡: 選択根拠、curated mandatory controlの選択漏れゼロ、除外監査sample、CAS競合拒否
検証(JSON Object): <code>{"evidence":"選択根拠、curated mandatory controlの選択漏れゼロ、除外監査sample、CAS競合拒否","method":"自動テストとbenchmark"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/right-size-execution/SKILL.md"]</code>
- 実装: <code>["governance/checklist/catalog.json",".agents/skills/right-size-execution/scripts/executionflow.py"]</code>
- テスト: <code>["tests/test_executionflow.py"]</code>
- 参照資料: <code>["SWEBOK-V4A"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-EXEC-010: 段階的な適用

要件ID(JSON): <code>"REQ-EXEC-010"</code>
タイトル(JSON): <code>"段階的な適用"</code>
主体(JSON): <code>"実行効率制御"</code>
対象(JSON): <code>"repository blockerを増やさないtelemetry、shadow、soft routing、calibrationおよびadvisory診断の導入順序"</code>
実行効率制御は、repository blockerを増やさないtelemetry、shadow、soft routing、calibrationおよびadvisory診断の導入順序を**段階適用する**。
行為enum: <code>"stage"</code>

根拠: 実行profileのschema、assurance、efficiency診断を第4のportable blockerへ昇格させず、未校正な効率規則が品質を損なうことを防ぐため。
根拠(JSON): <code>"実行profileのschema、assurance、efficiency診断を第4のportable blockerへ昇格させず、未校正な効率規則が品質を損なうことを防ぐため。"</code>

項目版: 2 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"user:2026-08-29"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-EXEC-010-1"</code> 前提: schema、assuranceまたはefficiencyの実行profile診断がある。条件: shadowまたは通常modeで診断を報告する。期待結果: diagnosticはrepository_blocking=falseのadvisory evidenceとなり、要件、as-built設計、選択check以外のportable blockerを作らない。
  - criterion(JSON Object): <code>{"given":"schema、assuranceまたはefficiencyの実行profile診断がある","id":"AC-EXEC-010-1","then":"diagnosticはrepository_blocking=falseのadvisory evidenceとなり、要件、as-built設計、選択check以外のportable blockerを作らない","when":"shadowまたは通常modeで診断を報告する"}</code>

要求源(JSON List): <code>["user:2026-07-18","user:2026-08-27","user:2026-08-29","arXiv:2406.18665"]</code>
検証方法: 自動テスト
検証証跡: schema、assurance、efficiency診断がadvisoryかつrepository_blocking=falseとなる回帰テスト
検証(JSON Object): <code>{"evidence":"schema、assurance、efficiency診断がadvisoryかつrepository_blocking=falseとなる回帰テスト","method":"自動テスト"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/right-size-execution/references/measurement-contract.md"]</code>
- 実装: <code>[".agents/skills/right-size-execution/assets/execution-policy.json",".agents/skills/right-size-execution/scripts/executionflow.py"]</code>
- テスト: <code>["tests/test_executionflow.py"]</code>
- 参照資料: <code>["SWEBOK-V4A"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-FRAME-001: workと正本の境界

要件ID(JSON): <code>"REQ-FRAME-001"</code>
タイトル(JSON): <code>"workと正本の境界"</code>
主体(JSON): <code>"リポジトリ"</code>
対象(JSON): <code>"一時的な作業記録と永続的な製品要件"</code>
リポジトリは、一時的な作業記録と永続的な製品要件を**分離する**。
行為enum: <code>"separate"</code>

根拠: work itemは実行文脈であり、暗黙に製品仕様の正本へ変わってはならない。
根拠(JSON): <code>"work itemは実行文脈であり、暗黙に製品仕様の正本へ変わってはならない。"</code>

項目版: 3 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"CHG-20260802-skills-audit-remediation"</code>
分類: scope=<code>""</code> / category=<code>""</code>

受入条件:
- <code>"AC-FRAME-001-1"</code> 前提: 統制対象の要求が存在する。条件: 要求を記録する。期待結果: workには要求断片、判断、計画、証跡だけが残り、永続要件は正本へ保存される。
  - criterion(JSON Object): <code>{"given":"統制対象の要求が存在する","id":"AC-FRAME-001-1","then":"workには要求断片、判断、計画、証跡だけが残り、永続要件は正本へ保存される","when":"要求を記録する"}</code>

要求源(JSON List): <code>["user:2026-07-17"]</code>
検証方法: 自動検査
検証証跡: リポジトリ検証とSkill契約テスト
検証(JSON Object): <code>{"evidence":"リポジトリ検証とSkill契約テスト","method":"自動検査"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/reference/development.md"]</code>
- 実装: <code>[".agents/skills/maintain-canonical-requirements/SKILL.md"]</code>
- テスト: <code>["tests/test_specflow.py"]</code>
- 参照資料: <code>["SWEBOK-V4A"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-PORTABLE-001: チャットだけで移植できる導入

要件ID(JSON): <code>"REQ-PORTABLE-001"</code>
タイトル(JSON): <code>"チャットだけで移植できる導入"</code>
主体(JSON): <code>"移植可能なSkills集"</code>
対象(JSON): <code>"別リポジトリへのcopy-and-chat方式の導入"</code>
移植可能なSkills集は、別リポジトリへのcopy-and-chat方式の導入を**実現する**。
行為enum: <code>"enable"</code>

根拠: 本リポジトリは再利用可能な参照集であり、利用者が内部ツールを手動操作せずに使える必要がある。
根拠(JSON): <code>"本リポジトリは再利用可能な参照集であり、利用者が内部ツールを手動操作せずに使える必要がある。"</code>

項目版: 5 / 状態: `active` / 種別: `operational`
変更識別子: <code>"CHG-20260829-review-remediation"</code>
分類: scope=<code>"product"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-PORTABLE-001-1"</code> 前提: 対象Skillsフォルダを別リポジトリへコピーしている。条件: 利用者が自然言語で開発要求を相談する。期待結果: 通常のチャットから導入、要件、設計、実装、テスト、依頼された公開までを自動実行する。
  - criterion(JSON Object): <code>{"given":"対象Skillsフォルダを別リポジトリへコピーしている","id":"AC-PORTABLE-001-1","then":"通常のチャットから導入、要件、設計、実装、テスト、依頼された公開までを自動実行する","when":"利用者が自然言語で開発要求を相談する"}</code>
- <code>"AC-PORTABLE-001-2"</code> 前提: 空の対象repositoryとdefault、fullまたはdefaultにregulated addonを合成したprofileとCodexまたはClaude hostの組合せがある。条件: profileを導入して配布closureをE2E検査する。期待結果: base profileの各Skill形式契約、必須asset、runner、固定されたQuint依存が導入先だけで解決し、defaultとfullでは3本柱、default+regulatedでは3本柱と明示選択したregulated補助機能のgenerateとcheckをsource repositoryのfileなしで実行できる。
  - criterion(JSON Object): <code>{"given":"空の対象repositoryとdefault、fullまたはdefaultにregulated addonを合成したprofileとCodexまたはClaude hostの組合せがある","id":"AC-PORTABLE-001-2","then":"base profileの各Skill形式契約、必須asset、runner、固定されたQuint依存が導入先だけで解決し、defaultとfullでは3本柱、default+regulatedでは3本柱と明示選択したregulated補助機能のgenerateとcheckをsource repositoryのfileなしで実行できる","when":"profileを導入して配布closureをE2E検査する"}</code>

要求源(JSON List): <code>["user:2026-07-17","user:2026-08-27","user:2026-08-29"]</code>
検証方法: 自動E2Eテスト
検証証跡: default、full、default+regulatedと両hostの空repository導入、参照closure、Quint generate/check、設計drift、selected check実行テスト
検証(JSON Object): <code>{"evidence":"default、full、default+regulatedと両hostの空repository導入、参照closure、Quint generate/check、設計drift、selected check実行テスト","method":"自動E2Eテスト"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/guides/getting-started.md","docs/decisions/ADR-0003-canonical-host-asset-generation.md"]</code>
- 実装: <code>["distribution/manifest.json","distribution/host-adapters.json",".agents/skills/chat-first-development/SKILL.md","tools/install_reference.py","tools/generate_host_assets.py",".github/workflows/host-assets.yml"]</code>
- テスト: <code>["tests/test_install_reference.py","tests/test_skills.py","tests/test_generate_host_assets.py","tests/test_profile_boundaries.py"]</code>
- 参照資料: <code>["SWEBOK-V4A"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-PORTABLE-002: 導入先repository policyの非強制

要件ID(JSON): <code>"REQ-PORTABLE-002"</code>
タイトル(JSON): <code>"導入先repository policyの非強制"</code>
主体(JSON): <code>"portable installerと既定profile"</code>
対象(JSON): <code>"導入先のbranch、merge rule、CI workflowを追加も変更もしないこと"</code>
portable installerと既定profileは、導入先のbranch、merge rule、CI workflowを追加も変更もしないことを**維持する**。
行為enum: <code>"preserve"</code>

根拠: 3本柱は開発成果物の整合性を扱い、repository運用方針は導入先のauthorityへ委任する。
根拠(JSON): <code>"3本柱は開発成果物の整合性を扱い、repository運用方針は導入先のauthorityへ委任する。"</code>

項目版: 1 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"CHG-20260827-quint-three-pillars"</code>
分類: scope=<code>"product"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-PORTABLE-002-1"</code> 前提: 独自のbranch ruleとCI workflowを持つ導入先がある。条件: 既定profileを適用する。期待結果: 既存設定がbyte一致し、新しいworkflow、ruleset、merge方式が追加されない。
  - criterion(JSON Object): <code>{"given":"独自のbranch ruleとCI workflowを持つ導入先がある","id":"AC-PORTABLE-002-1","then":"既存設定がbyte一致し、新しいworkflow、ruleset、merge方式が追加されない","when":"既定profileを適用する"}</code>

要求源(JSON List): <code>["user:2026-08-27","https://quint.sh/docs/what-does-quint-do","docs/decisions/ADR-0004-quint-three-pillar-portability.md"]</code>
検証方法: installer isolation test
検証証跡: 既存.github/workflowsとpolicy fixtureの適用前後byte比較
検証(JSON Object): <code>{"evidence":"既存.github/workflowsとpolicy fixtureの適用前後byte比較","method":"installer isolation test"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/decisions/ADR-0004-quint-three-pillar-portability.md"]</code>
- 実装: <code>["distribution/manifest.json","tools/install_reference.py"]</code>
- テスト: <code>["tests/test_install_reference.py","tests/test_profile_boundaries.py"]</code>
- 参照資料: <code>["QUINT-0.32"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-PORTABLE-003: 外部操作の明示権限境界

要件ID(JSON): <code>"REQ-PORTABLE-003"</code>
タイトル(JSON): <code>"外部操作の明示権限境界"</code>
主体(JSON): <code>"portable Skillとruntime"</code>
対象(JSON): <code>"外部または不可逆な操作を利用者が明示した依頼と必要な承認の範囲だけに限定すること"</code>
portable Skillとruntimeは、外部または不可逆な操作を利用者が明示した依頼と必要な承認の範囲だけに限定することを**制約する**。
行為enum: <code>"constrain"</code>

根拠: copy-and-chatで導入したガードレールが、要件更新や検査を理由に未依頼の公開、deploy、merge、外部記録または高額操作へ権限を広げてはならない。
根拠(JSON): <code>"copy-and-chatで導入したガードレールが、要件更新や検査を理由に未依頼の公開、deploy、merge、外部記録または高額操作へ権限を広げてはならない。"</code>

項目版: 1 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"user:2026-08-29"</code>
分類: scope=<code>"product"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-PORTABLE-003-1"</code> 前提: 外部systemへの書込みまたは不可逆な操作が開発手順に現れる。条件: portable Skillまたはruntimeが実行可否を判断する。期待結果: 利用者がその結果を明示的に依頼し、対象systemに必要な権限が確認できる場合だけ実行し、それ以外はrepository内の成果物またはhandoffに留める。
  - criterion(JSON Object): <code>{"given":"外部systemへの書込みまたは不可逆な操作が開発手順に現れる","id":"AC-PORTABLE-003-1","then":"利用者がその結果を明示的に依頼し、対象systemに必要な権限が確認できる場合だけ実行し、それ以外はrepository内の成果物またはhandoffに留める","when":"portable Skillまたはruntimeが実行可否を判断する"}</code>

要求源(JSON List): <code>["user:2026-08-27","user:2026-08-29","AGENTS.md"]</code>
検証方法: 契約テストとmutation test
検証証跡: 未依頼外部操作の拒否、明示依頼と権限を伴う操作の許可、外部anchor handoff境界の検査
検証(JSON Object): <code>{"evidence":"未依頼外部操作の拒否、明示依頼と権限を伴う操作の許可、外部anchor handoff境界の検査","method":"契約テストとmutation test"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["AGENTS.md"]</code>
- 実装: <code>[".agents/skills/chat-first-development/SKILL.md",".agents/skills/authorize-autonomous-execution/SKILL.md","tools/install_reference.py"]</code>
- テスト: <code>["tests/test_skills.py","tests/test_profile_boundaries.py","tests/test_install_reference.py"]</code>
- 参照資料: <code>[]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-QUALITY-001: 版管理された出典台帳

要件ID(JSON): <code>"REQ-QUALITY-001"</code>
タイトル(JSON): <code>"版管理された出典台帳"</code>
主体(JSON): <code>"品質フレーム"</code>
対象(JSON): <code>"SWEBOKとクラウド・AI公式資料の監査可能な出典台帳"</code>
品質フレームは、SWEBOKとクラウド・AI公式資料の監査可能な出典台帳を**維持する**。
行為enum: <code>"maintain"</code>

根拠: 正式名称、版、URL、参照範囲、差分、固定物ハッシュを保存することで、レビュー根拠を再現し更新を検知できる。
根拠(JSON): <code>"正式名称、版、URL、参照範囲、差分、固定物ハッシュを保存することで、レビュー根拠を再現し更新を検知できる。"</code>

項目版: 2 / 状態: `active` / 種別: `operational`
変更識別子: <code>"WI-20260718-checklist-japanese-docs"</code>
分類: scope=<code>""</code> / category=<code>""</code>

受入条件:
- <code>"AC-QUALITY-001-1"</code> 前提: 品質プロファイルを選択している。条件: 出典台帳を検証する。期待結果: 各資料が公式URL、版、参照日、更新間隔、適用範囲、変更確認日、前版との差分を持ち、固定参照物はSHA-256を持つ。
  - criterion(JSON Object): <code>{"given":"品質プロファイルを選択している","id":"AC-QUALITY-001-1","then":"各資料が公式URL、版、参照日、更新間隔、適用範囲、変更確認日、前版との差分を持ち、固定参照物はSHA-256を持つ","when":"出典台帳を検証する"}</code>
- <code>"AC-QUALITY-001-2"</code> 前提: 添付SWEBOKを参照する。条件: 版の同一性を検証する。期待結果: v4.0aの正式名称、18KA対応、固定SHA-256が台帳と一致する。
  - criterion(JSON Object): <code>{"given":"添付SWEBOKを参照する","id":"AC-QUALITY-001-2","then":"v4.0aの正式名称、18KA対応、固定SHA-256が台帳と一致する","when":"版の同一性を検証する"}</code>

要求源(JSON List): <code>["user:2026-07-17","SWEBOK V4","AWS Well-Architected","Azure Well-Architected","Google Cloud Well-Architected","OCI Best Practices"]</code>
検証方法: 自動検査
検証証跡: 公式host、鮮度、範囲、差分、ハッシュのテスト
検証(JSON Object): <code>{"evidence":"公式host、鮮度、範囲、差分、ハッシュのテスト","method":"自動検査"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/SOURCES.md"]</code>
- 実装: <code>[".agents/skills/verify-against-engineering-standards/scripts/standardsflow.py","governance/standards/registry.json"]</code>
- テスト: <code>["tests/test_standardsflow.py"]</code>
- 参照資料: <code>["SWEBOK-V4A","AWS-WAF","AWS-GENAI-LENS","AWS-RAI-LENS","AWS-ML-LENS","AWS-AGENTIC-LENS","AZURE-WAF","AZURE-AI-WAF","GCP-WAF","GCP-AIML-WAF","OCI-WAF"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-QUALITY-002: 変更範囲に対応する品質検査

要件ID(JSON): <code>"REQ-QUALITY-002"</code>
タイトル(JSON): <code>"変更範囲に対応する品質検査"</code>
主体(JSON): <code>"品質フロー"</code>
対象(JSON): <code>"変更と受入条件に関係する検査だけによる成果物検証"</code>
品質フローは、変更と受入条件に関係する検査だけによる成果物検証を**検証する**。
行為enum: <code>"verify"</code>

根拠: 関係する失敗を直接証跡で検出しつつ、無関係な全件検査と専用記録の負担を避ける。
根拠(JSON): <code>"関係する失敗を直接証跡で検出しつつ、無関係な全件検査と専用記録の負担を避ける。"</code>

項目版: 5 / 状態: `active` / 種別: `quality`
変更識別子: <code>"CHG-20260829-review-remediation"</code>
分類: scope=<code>"product"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-QUALITY-002-1"</code> 前提: 変更内容と受入条件が分かっている。条件: 品質検査を実行する。期待結果: 関係する最小のtest、lint、type check、buildまたはgeneratorだけを選び、PassまたはFailと直接証跡を簡潔に示す。
  - criterion(JSON Object): <code>{"given":"変更内容と受入条件が分かっている","id":"AC-QUALITY-002-1","then":"関係する最小のtest、lint、type check、buildまたはgeneratorだけを選び、PassまたはFailと直接証跡を簡潔に示す","when":"品質検査を実行する"}</code>
- <code>"AC-QUALITY-002-2"</code> 前提: 対象repositoryに該当する既存CIがない。条件: 選択した検査を実行する。期待結果: ローカルcommandを使い、新しいCI workflow、required check、review YAMLを要求しない。
  - criterion(JSON Object): <code>{"given":"対象repositoryに該当する既存CIがない","id":"AC-QUALITY-002-2","then":"ローカルcommandを使い、新しいCI workflow、required check、review YAMLを要求しない","when":"選択した検査を実行する"}</code>

要求源(JSON List): <code>["user:2026-07-17","user:2026-08-27","user:2026-08-29","SWEBOK V4","cloud vendor official guidance"]</code>
検証方法: 契約テスト
検証証跡: 選択検査とrepository policy非強制のテスト
検証(JSON Object): <code>{"evidence":"選択検査とrepository policy非強制のテスト","method":"契約テスト"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/inspect-quality-gates/SKILL.md",".agents/skills/inspect-quality-gates/references/gate-rules.md"]</code>
- 実装: <code>[".agents/skills/inspect-quality-gates/scripts/inspect.py"]</code>
- テスト: <code>["tests/test_skills.py","tests/test_review_contract.py","tests/test_inspect_runner.py"]</code>
- 参照資料: <code>["SWEBOK-V4A","AWS-WAF","AWS-GENAI-LENS","AWS-RAI-LENS","AWS-ML-LENS","AWS-AGENTIC-LENS","AZURE-WAF","AZURE-AI-WAF","GCP-WAF","GCP-AIML-WAF","OCI-WAF"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-QUALITY-003: 原子的なチェック統制

要件ID(JSON): <code>"REQ-QUALITY-003"</code>
タイトル(JSON): <code>"原子的なチェック統制"</code>
主体(JSON): <code>"チェックリスト生成フロー"</code>
対象(JSON): <code>"一項目・一統制・一証跡で独立判定できるチェック項目"</code>
チェックリスト生成フローは、一項目・一統制・一証跡で独立判定できるチェック項目を**維持する**。
行為enum: <code>"maintain"</code>

根拠: 複数統制を一行へ詰め込むと部分実装を一意にPassまたはFailと判定できない。
根拠(JSON): <code>"複数統制を一行へ詰め込むと部分実装を一意にPassまたはFailと判定できない。"</code>

項目版: 3 / 状態: `active` / 種別: `quality`
変更識別子: <code>"CHG-20260802-skills-audit-remediation"</code>
分類: scope=<code>""</code> / category=<code>""</code>

受入条件:
- <code>"AC-QUALITY-003-1"</code> 前提: チェック項目を追加または更新する。条件: ワークブックを生成・検証する。期待結果: 独立した合否条件を持つ統制へ分割され、既知の複合項目が再発しない。
  - criterion(JSON Object): <code>{"given":"チェック項目を追加または更新する","id":"AC-QUALITY-003-1","then":"独立した合否条件を持つ統制へ分割され、既知の複合項目が再発しない","when":"ワークブックを生成・検証する"}</code>

要求源(JSON List): <code>["user:2026-07-18","SWEBOK Software Quality"]</code>
検証方法: 自動テストと批判的レビュー
検証証跡: 原子性回帰テストとチェック項目カタログ
検証(JSON Object): <code>{"evidence":"原子性回帰テストとチェック項目カタログ","method":"自動テストと批判的レビュー"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["governance/reviews/README.md"]</code>
- 実装: <code>["update_checklist.py",".agents/skills/verify-against-engineering-standards/SKILL.md"]</code>
- テスト: <code>["tests/test_checklist.py"]</code>
- 参照資料: <code>["SWEBOK-V4A"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-QUALITY-004: 3本柱だけのportable guardrail

要件ID(JSON): <code>"REQ-QUALITY-004"</code>
タイトル(JSON): <code>"3本柱だけのportable guardrail"</code>
主体(JSON): <code>"portable blocking guardrail"</code>
対象(JSON): <code>"要件正本、as-built生成、選択checkの3本柱だけを対象にすること"</code>
portable blocking guardrailは、要件正本、as-built生成、選択checkの3本柱だけを対象にすることを**制約する**。
行為enum: <code>"constrain"</code>

根拠: 導入時の摩擦とfalse blockerを抑え、repository固有の工程を強制しない。
根拠(JSON): <code>"導入時の摩擦とfalse blockerを抑え、repository固有の工程を強制しない。"</code>

項目版: 1 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"CHG-20260827-quint-three-pillars"</code>
分類: scope=<code>"product"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-QUALITY-004-1"</code> 前提: 全Skillの形式契約がある。条件: Quint不変条件を検証する。期待結果: blocking guardrailは3本柱のいずれかに属し、補助Skillはblockingにならない。
  - criterion(JSON Object): <code>{"given":"全Skillの形式契約がある","id":"AC-QUALITY-004-1","then":"blocking guardrailは3本柱のいずれかに属し、補助Skillはblockingにならない","when":"Quint不変条件を検証する"}</code>
- <code>"AC-QUALITY-004-2"</code> 前提: portable contractを検証する。条件: merge ruleとCI requirementの属性を確認する。期待結果: すべてfalseである。
  - criterion(JSON Object): <code>{"given":"portable contractを検証する","id":"AC-QUALITY-004-2","then":"すべてfalseである","when":"merge ruleとCI requirementの属性を確認する"}</code>

要求源(JSON List): <code>["user:2026-08-27","https://quint.sh/docs/what-does-quint-do","docs/decisions/ADR-0004-quint-three-pillar-portability.md"]</code>
検証方法: Quint invariant verification
検証証跡: threePillarsOnlyとrepositoryPolicyIsHostOwnedの検証成功
検証(JSON Object): <code>{"evidence":"threePillarsOnlyとrepositoryPolicyIsHostOwnedの検証成功","method":"Quint invariant verification"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/decisions/ADR-0004-quint-three-pillar-portability.md"]</code>
- 実装: <code>["spec/skills/skills.qnt","distribution/manifest.json"]</code>
- テスト: <code>["tests/test_quintflow.py","tests/test_profile_boundaries.py"]</code>
- 参照資料: <code>["QUINT-0.32"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-QUINT-001: Quint要件正本

要件ID(JSON): <code>"REQ-QUINT-001"</code>
タイトル(JSON): <code>"Quint要件正本"</code>
主体(JSON): <code>"永続要件"</code>
対象(JSON): <code>"Quint仕様を唯一の編集対象としJSONを派生物として維持すること"</code>
永続要件は、Quint仕様を唯一の編集対象としJSONを派生物として維持することを**維持する**。
行為enum: <code>"maintain"</code>

根拠: 型検査と状態不変条件を要件記述の入口へ置き、手書きJSONの構造矛盾を防ぐ。
根拠(JSON): <code>"型検査と状態不変条件を要件記述の入口へ置き、手書きJSONの構造矛盾を防ぐ。"</code>

項目版: 3 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"CHG-20260829-review-remediation"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-QUINT-001-1"</code> 前提: 永続要件の意味、分類、verificationまたはtraceを変更する。条件: 要件正本を更新する。期待結果: Quint仕様と対象revisionが更新され、typecheckとcatalog invariant成功後に同じ内容のJSONが生成される。
  - criterion(JSON Object): <code>{"given":"永続要件の意味、分類、verificationまたはtraceを変更する","id":"AC-QUINT-001-1","then":"Quint仕様と対象revisionが更新され、typecheckとcatalog invariant成功後に同じ内容のJSONが生成される","when":"要件正本を更新する"}</code>
- <code>"AC-QUINT-001-2"</code> 前提: 要件catalogとadd、update、trace update、retireの抽象遷移がある。条件: bounded formal verificationを実行する。期待結果: catalogWellFormedとlifecycleRefinesCatalogをrequirements.qntでもApalache検証し、失敗時は一時出力を破棄する前にbounded diagnosticを報告する。
  - criterion(JSON Object): <code>{"given":"要件catalogとadd、update、trace update、retireの抽象遷移がある","id":"AC-QUINT-001-2","then":"catalogWellFormedとlifecycleRefinesCatalogをrequirements.qntでもApalache検証し、失敗時は一時出力を破棄する前にbounded diagnosticを報告する","when":"bounded formal verificationを実行する"}</code>

要求源(JSON List): <code>["user:2026-08-27","user:2026-08-29","https://quint.sh/docs/what-does-quint-do","docs/decisions/ADR-0004-quint-three-pillar-portability.md"]</code>
検証方法: Quint typecheckと生成drift検査
検証証跡: requirements.qntのtypecheck成功とrequirements.jsonのbyte一致
検証(JSON Object): <code>{"evidence":"requirements.qntのtypecheck成功とrequirements.jsonのbyte一致","method":"Quint typecheckと生成drift検査"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/decisions/ADR-0004-quint-three-pillar-portability.md"]</code>
- 実装: <code>["spec/requirements/requirements.qnt","tools/quintflow.py"]</code>
- テスト: <code>["tests/test_quintflow.py","tests/test_specflow.py"]</code>
- 参照資料: <code>["QUINT-0.32"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-QUINT-002: 要件表示の二段生成

要件ID(JSON): <code>"REQ-QUINT-002"</code>
タイトル(JSON): <code>"要件表示の二段生成"</code>
主体(JSON): <code>"要件生成器"</code>
対象(JSON): <code>"Quintから全fieldとList順を保持するJSONを生成し、そのserialized JSONから人向けMarkdownを生成すること"</code>
要件生成器は、Quintから全fieldとList順を保持するJSONを生成し、そのserialized JSONから人向けMarkdownを生成することを**生成する**。
行為enum: <code>"generate"</code>

根拠: 機械検証用表現と人向け表示の責務を分離しつつ、authorityを一本化する。
根拠(JSON): <code>"機械検証用表現と人向け表示の責務を分離しつつ、authorityを一本化する。"</code>

項目版: 3 / 状態: `active` / 種別: `functional`
変更識別子: <code>"CHG-20260829-review-remediation"</code>
分類: scope=<code>"product"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-QUINT-002-1"</code> 前提: 同一のQuint要件仕様がある。条件: 生成を二回実行する。期待結果: JSONとMarkdownがそれぞれバイト一致する。
  - criterion(JSON Object): <code>{"given":"同一のQuint要件仕様がある","id":"AC-QUINT-002-1","then":"JSONとMarkdownがそれぞれバイト一致する","when":"生成を二回実行する"}</code>
- <code>"AC-QUINT-002-2"</code> 前提: 生成済みJSONを変更する。条件: drift検査を実行する。期待結果: Quint正本との差異として失敗する。
  - criterion(JSON Object): <code>{"given":"生成済みJSONを変更する","id":"AC-QUINT-002-2","then":"Quint正本との差異として失敗する","when":"drift検査を実行する"}</code>
- <code>"AC-QUINT-002-3"</code> 前提: 全fieldに異なる値、空のretirement・classification field、順序の異なる複数要件を持つQuint fixtureがある。条件: JSONとMarkdownを生成してJSONからQuint表現へ逆写像する。期待結果: 明示写像で全fieldとList順を保持して完全往復し、serialized JSONを再parseした値だけをMarkdownへ渡してGiven When Thenを含む意味を保持する。
  - criterion(JSON Object): <code>{"given":"全fieldに異なる値、空のretirement・classification field、順序の異なる複数要件を持つQuint fixtureがある","id":"AC-QUINT-002-3","then":"明示写像で全fieldとList順を保持して完全往復し、serialized JSONを再parseした値だけをMarkdownへ渡してGiven When Thenを含む意味を保持する","when":"JSONとMarkdownを生成してJSONからQuint表現へ逆写像する"}</code>

要求源(JSON List): <code>["user:2026-08-27","user:2026-08-29","https://quint.sh/docs/what-does-quint-do","docs/decisions/ADR-0004-quint-three-pillar-portability.md"]</code>
検証方法: 決定的生成とgolden mappingテスト
検証証跡: 全field oracle、serialized JSON境界、一時出力とcommitted JSON・Markdownのbyte比較
検証(JSON Object): <code>{"evidence":"全field oracle、serialized JSON境界、一時出力とcommitted JSON・Markdownのbyte比較","method":"決定的生成とgolden mappingテスト"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/decisions/ADR-0004-quint-three-pillar-portability.md"]</code>
- 実装: <code>["tools/quintflow.py","tools/spec_mapping.py","tools/render_requirements.py",".agents/skills/maintain-canonical-requirements/scripts/specflow.py"]</code>
- テスト: <code>["tests/test_quintflow.py","tests/test_specflow.py"]</code>
- 参照資料: <code>["QUINT-0.32"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-QUINT-003: 全Skillの形式契約網羅

要件ID(JSON): <code>"REQ-QUINT-003"</code>
タイトル(JSON): <code>"全Skillの形式契約網羅"</code>
主体(JSON): <code>"Skill形式仕様"</code>
対象(JSON): <code>"すべてのSkillを一対一のQuint契約とactive要件の双方向traceへ対応付けること"</code>
Skill形式仕様は、すべてのSkillを一対一のQuint契約とactive要件の双方向traceへ対応付けることを**形式化する**。
行為enum: <code>"formalize"</code>

根拠: Skill追加時の形式仕様漏れ、削除後に残るstale契約、実装traceだけまたは自己申告requirement IDだけの片方向接続を機械検出する。
根拠(JSON): <code>"Skill追加時の形式仕様漏れ、削除後に残るstale契約、実装traceだけまたは自己申告requirement IDだけの片方向接続を機械検出する。"</code>

項目版: 2 / 状態: `active` / 種別: `quality`
変更識別子: <code>"user:2026-08-29"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-QUINT-003-1"</code> 前提: Skill directoryとQuint契約catalogがある。条件: 形式契約検査を実行する。期待結果: 双方の名前集合が完全一致し、各SKILL.mdから契約へtraceできる。
  - criterion(JSON Object): <code>{"given":"Skill directoryとQuint契約catalogがある","id":"AC-QUINT-003-1","then":"双方の名前集合が完全一致し、各SKILL.mdから契約へtraceできる","when":"形式契約検査を実行する"}</code>
- <code>"AC-QUINT-003-2"</code> 前提: active要件がSkill pathをtraceするかSkill契約がrequirement IDを宣言する。条件: trace整合検査を実行する。期待結果: 要件からSkill pathへの組とSkillからactive requirement IDへの組が完全一致し、未知またはretired IDを拒否する。
  - criterion(JSON Object): <code>{"given":"active要件がSkill pathをtraceするかSkill契約がrequirement IDを宣言する","id":"AC-QUINT-003-2","then":"要件からSkill pathへの組とSkillからactive requirement IDへの組が完全一致し、未知またはretired IDを拒否する","when":"trace整合検査を実行する"}</code>

要求源(JSON List): <code>["user:2026-08-27","user:2026-08-29","https://quint.sh/docs/what-does-quint-do","docs/decisions/ADR-0004-quint-three-pillar-portability.md"]</code>
検証方法: Quint testと双方向集合比較
検証証跡: skills.qntのtest成功、Skill inventory、requirementIdsとactive要件Skill path traceの完全一致検査
検証(JSON Object): <code>{"evidence":"skills.qntのtest成功、Skill inventory、requirementIdsとactive要件Skill path traceの完全一致検査","method":"Quint testと双方向集合比較"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/decisions/ADR-0004-quint-three-pillar-portability.md"]</code>
- 実装: <code>["spec/skills/skills.qnt","tools/quintflow.py"]</code>
- テスト: <code>["tests/test_quintflow.py","tests/test_skills.py"]</code>
- 参照資料: <code>["QUINT-0.32"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-REPO-001: mainとdevの役割および統合方式

要件ID(JSON): <code>"REQ-REPO-001"</code>
タイトル(JSON): <code>"mainとdevの役割および統合方式"</code>
主体(JSON): <code>"dev-standardのbranch運用"</code>
対象(JSON): <code>"mainへのsquashとdevへのmerge commitを分離したbranch別統合契約"</code>
dev-standardのbranch運用は、mainへのsquashとdevへのmerge commitを分離したbranch別統合契約を**強制する**。
行為enum: <code>"enforce"</code>

根拠: 利用者向けrelease履歴と到達可能なengineering履歴のauthorityを案件ごとのmerge判断に依存させないため。
根拠(JSON): <code>"利用者向けrelease履歴と到達可能なengineering履歴のauthorityを案件ごとのmerge判断に依存させないため。"</code>

項目版: 3 / 状態: `retired` / 種別: `constraint`
変更識別子: <code>"user:2026-08-29"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-REPO-001-1"</code> 前提: trial phaseでmainまたはdevをbaseとするPull Requestがある。条件: branch-policy checkを実行する。期待結果: mainはrepositoryのdevまたはhotfixだけをsquashで受け入れ、devはtopic、main、またはhotfix競合を解消したreconcile branchだけをmerge commitで受け入れ、その他の方向を拒否する。
  - criterion(JSON Object): <code>{"given":"trial phaseでmainまたはdevをbaseとするPull Requestがある","id":"AC-REPO-001-1","then":"mainはrepositoryのdevまたはhotfixだけをsquashで受け入れ、devはtopic、main、またはhotfix競合を解消したreconcile branchだけをmerge commitで受け入れ、その他の方向を拒否する","when":"branch-policy checkを実行する"}</code>
- <code>"AC-REPO-001-2"</code> 前提: mainまたはdevへpushがある。条件: push auditとGitHub rulesetを評価する。期待結果: mainのlinear historyとdevの一回一merge commit更新を監査し、削除またはforce pushを許可しない。
  - criterion(JSON Object): <code>{"given":"mainまたはdevへpushがある","id":"AC-REPO-001-2","then":"mainのlinear historyとdevの一回一merge commit更新を監査し、削除またはforce pushを許可しない","when":"push auditとGitHub rulesetを評価する"}</code>
- <code>"AC-REPO-001-3"</code> 前提: branch policyがbootstrap phaseであり、dev、ruleset、required checks、PR移行、operator確認が完了している。条件: trial phaseへ移行する。期待結果: mainへのactivation PRでpolicyと対応するactive review YAMLだけを変更し、全Activation-Checkを一度ずつ記録した後、bootstrap reconciliationで同じpolicyとreviewをdevへ伝播する。
  - criterion(JSON Object): <code>{"given":"branch policyがbootstrap phaseであり、dev、ruleset、required checks、PR移行、operator確認が完了している","id":"AC-REPO-001-3","then":"mainへのactivation PRでpolicyと対応するactive review YAMLだけを変更し、全Activation-Checkを一度ずつ記録した後、bootstrap reconciliationで同じpolicyとreviewをdevへ伝播する","when":"trial phaseへ移行する"}</code>
- <code>"AC-REPO-001-4"</code> 前提: 既存devがcurrent mainを祖先に持ち、両tip treeが一致し、まだbranch policyを含まない。条件: 二層branch契約をdev-firstでbootstrap導入する。期待結果: Issue #20を参照する初回bootstrap PRだけをdevへmerge commitで統合し、同じtreeをRelease-Type bootstrapのdevからmainへのsquashで導入できるが、Issueをcloseせず2回の通常releaseへ数えない。
  - criterion(JSON Object): <code>{"given":"既存devがcurrent mainを祖先に持ち、両tip treeが一致し、まだbranch policyを含まない","id":"AC-REPO-001-4","then":"Issue #20を参照する初回bootstrap PRだけをdevへmerge commitで統合し、同じtreeをRelease-Type bootstrapのdevからmainへのsquashで導入できるが、Issueをcloseせず2回の通常releaseへ数えない","when":"二層branch契約をdev-firstでbootstrap導入する"}</code>

要求源(JSON List): <code>["user:2026-07-24","issue:#20","docs/decisions/ADR-0002-two-layer-branch-history.md"]</code>
検証方法: CIとGitHub ruleset監査
検証証跡: branch方向、merge parent、commit subject、protected branch設定のCI結果
検証(JSON Object): <code>{"evidence":"branch方向、merge parent、commit subject、protected branch設定のCI結果","method":"CIとGitHub ruleset監査"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/decisions/ADR-0002-two-layer-branch-history.md","docs/reference/development.md"]</code>
- 実装: <code>[]</code>
- テスト: <code>[]</code>
- 参照資料: <code>[]</code>
廃止理由: <code>"導入先へmerge方式やbranch構成を強制しない3本柱境界へ移行したため"</code>
後継要件: <code>""</code>

## REQ-REPO-002: release後の祖先関係とtreeを回復するreconciliation契約

要件ID(JSON): <code>"REQ-REPO-002"</code>
タイトル(JSON): <code>"release後の祖先関係とtreeを回復するreconciliation契約"</code>
主体(JSON): <code>"release operatorとCI"</code>
対象(JSON): <code>"release前後のancestor関係、tip tree条件、freezeを含むreconciliation transaction"</code>
release operatorとCIは、release前後のancestor関係、tip tree条件、freezeを含むreconciliation transactionを**維持する**。
行為enum: <code>"maintain"</code>

根拠: squashで記録されない祖先関係を回復し、既出file差分とconflictの再評価を防ぎながら詳細commitを保持するため。
根拠(JSON): <code>"squashで記録されない祖先関係を回復し、既出file差分とconflictの再評価を防ぎながら詳細commitを保持するため。"</code>

項目版: 3 / 状態: `retired` / 種別: `operational`
変更識別子: <code>"user:2026-08-29"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-REPO-002-1"</code> 前提: devからmainへ通常releaseをsquash mergeした。条件: release reconciliationを完了する。期待結果: 次のtopic統合前にmainをdevへmergeし、mainがdevの祖先であり両tip treeが一致する。
  - criterion(JSON Object): <code>{"given":"devからmainへ通常releaseをsquash mergeした","id":"AC-REPO-002-1","then":"次のtopic統合前にmainをdevへmergeし、mainがdevの祖先であり両tip treeが一致する","when":"release reconciliationを完了する"}</code>
- <code>"AC-REPO-002-2"</code> 前提: mainへhotfixをsquash mergeしdevに未release変更がある。条件: hotfix reconciliationを完了する。期待結果: conflict-freeならmainをdevへ直接mergeし、mainをdevの祖先にするが両tip treeの一致は要求しない。
  - criterion(JSON Object): <code>{"given":"mainへhotfixをsquash mergeしdevに未release変更がある","id":"AC-REPO-002-2","then":"conflict-freeならmainをdevへ直接mergeし、mainをdevの祖先にするが両tip treeの一致は要求しない","when":"hotfix reconciliationを完了する"}</code>
- <code>"AC-REPO-002-3"</code> 前提: 通常releaseとreconciliationを2回行う。条件: branch graph回帰testを実行する。期待結果: 前回release済みfile差分が次回release diffへ再出現せず、詳細commitはdevから到達可能なまま残る。
  - criterion(JSON Object): <code>{"given":"通常releaseとreconciliationを2回行う","id":"AC-REPO-002-3","then":"前回release済みfile差分が次回release diffへ再出現せず、詳細commitはdevから到達可能なまま残る","when":"branch graph回帰testを実行する"}</code>
- <code>"AC-REPO-002-4"</code> 前提: hotfix後のmainをdevへ直接mergeするとconflictする。条件: hotfix conflict reconciliationを完了する。期待結果: freeze中のdevからreconcile branchを作り、prior devとcurrent mainをparentに持つ解消mergeをdevへ統合し、outer merge treeとhotfix変更pathを保持してours相当の破棄を拒否する。
  - criterion(JSON Object): <code>{"given":"hotfix後のmainをdevへ直接mergeするとconflictする","id":"AC-REPO-002-4","then":"freeze中のdevからreconcile branchを作り、prior devとcurrent mainをparentに持つ解消mergeをdevへ統合し、outer merge treeとhotfix変更pathを保持してours相当の破棄を拒否する","when":"hotfix conflict reconciliationを完了する"}</code>

要求源(JSON List): <code>["user:2026-07-24","issue:#20","Git FAQ: long-running squash merge","docs/decisions/ADR-0002-two-layer-branch-history.md"]</code>
検証方法: branch graph回帰テストとCI
検証証跡: 一時Git repositoryのancestor、direct tree、three-dot diff、到達可能commitのassert
検証(JSON Object): <code>{"evidence":"一時Git repositoryのancestor、direct tree、three-dot diff、到達可能commitのassert","method":"branch graph回帰テストとCI"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/decisions/ADR-0002-two-layer-branch-history.md","docs/reference/development.md"]</code>
- 実装: <code>[]</code>
- テスト: <code>[]</code>
- 参照資料: <code>[]</code>
廃止理由: <code>"repository固有のreconciliation契約を廃止し、GitHub標準設定へ委任したため"</code>
後継要件: <code>""</code>

## REQ-REPO-003: 試行範囲、非移植性、rollback

要件ID(JSON): <code>"REQ-REPO-003"</code>
タイトル(JSON): <code>"試行範囲、非移植性、rollback"</code>
主体(JSON): <code>"dev-standardの二層branch試行"</code>
対象(JSON): <code>"2回のrelease cycleに限定しportable profileへ既定配布しない二層branch試行"</code>
dev-standardの二層branch試行は、2回のrelease cycleに限定しportable profileへ既定配布しない二層branch試行を**制約する**。
行為enum: <code>"constrain"</code>

根拠: 長寿命devは一般解ではなく、追加操作とGitHub上の非原子的なlock制約を受容できるrepositoryだけで評価すべきため。
根拠(JSON): <code>"長寿命devは一般解ではなく、追加操作とGitHub上の非原子的なlock制約を受容できるrepositoryだけで評価すべきため。"</code>

項目版: 3 / 状態: `retired` / 種別: `constraint`
変更識別子: <code>"user:2026-08-29"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-REPO-003-1"</code> 前提: 二層branch契約のassetを配布profileへ追加しようとする。条件: distribution contractを検査する。期待結果: dev-standard固有のbranch policyとvalidatorをportable profileへ含めず、導入先の既定branch戦略を変更しない。
  - criterion(JSON Object): <code>{"given":"二層branch契約のassetを配布profileへ追加しようとする","id":"AC-REPO-003-1","then":"dev-standard固有のbranch policyとvalidatorをportable profileへ含めず、導入先の既定branch戦略を変更しない","when":"distribution contractを検査する"}</code>
- <code>"AC-REPO-003-2"</code> 前提: 2回のrelease試行が完了していない、または昇格条件を満たさない。条件: 試行結果を判断する。期待結果: 恒久採用と一般化を行わず、必要時はdevへの新規統合を停止して同期済み状態で凍結する。
  - criterion(JSON Object): <code>{"given":"2回のrelease試行が完了していない、または昇格条件を満たさない","id":"AC-REPO-003-2","then":"恒久採用と一般化を行わず、必要時はdevへの新規統合を停止して同期済み状態で凍結する","when":"試行結果を判断する"}</code>
- <code>"AC-REPO-003-3"</code> 前提: GitHub Actionsでmainとdevの状態を検査する。条件: authority boundaryを確認する。期待結果: required checkを原子的なcross-branch lockとは表明せず、単一operatorと明示freezeの限界を文書化する。
  - criterion(JSON Object): <code>{"given":"GitHub Actionsでmainとdevの状態を検査する","id":"AC-REPO-003-3","then":"required checkを原子的なcross-branch lockとは表明せず、単一operatorと明示freezeの限界を文書化する","when":"authority boundaryを確認する"}</code>
- <code>"AC-REPO-003-4"</code> 前提: branch policyがbootstrap phaseである。条件: 二層branch試行を開始する。期待結果: activation前に初回bootstrap導入以外のtopic mergeを拒否してbranch graph回帰testと外部GitHub設定を確認し、policyとactive reviewを両branchへ伝播した後の最初の小変更を1回目の管理されたdry runとして扱う。
  - criterion(JSON Object): <code>{"given":"branch policyがbootstrap phaseである","id":"AC-REPO-003-4","then":"activation前に初回bootstrap導入以外のtopic mergeを拒否してbranch graph回帰testと外部GitHub設定を確認し、policyとactive reviewを両branchへ伝播した後の最初の小変更を1回目の管理されたdry runとして扱う","when":"二層branch試行を開始する"}</code>
- <code>"AC-REPO-003-5"</code> 前提: 二層branch試行を停止する。条件: rollback transactionを完了する。期待結果: policyと対応するactive review YAMLだけを変更するrollback hotfixをmainへsquashし、hotfix reconciliationでdevへ伝播した後にbootstrapで新規topic統合と通常releaseを停止する。
  - criterion(JSON Object): <code>{"given":"二層branch試行を停止する","id":"AC-REPO-003-5","then":"policyと対応するactive review YAMLだけを変更するrollback hotfixをmainへsquashし、hotfix reconciliationでdevへ伝播した後にbootstrapで新規topic統合と通常releaseを停止する","when":"rollback transactionを完了する"}</code>
- <code>"AC-REPO-003-6"</code> 前提: branch policyまたはreview validatorを変更するPull Requestまたはprotected branch pushがある。条件: Governanceのevidenceまたはbranch-policy jobを実行する。期待結果: 利用可能な場合はPR baseまたはpush before側のvalidatorとdependencyで候補treeを検査し、候補validatorだけの自己緩和を当該判定へ使用しない。
  - criterion(JSON Object): <code>{"given":"branch policyまたはreview validatorを変更するPull Requestまたはprotected branch pushがある","id":"AC-REPO-003-6","then":"利用可能な場合はPR baseまたはpush before側のvalidatorとdependencyで候補treeを検査し、候補validatorだけの自己緩和を当該判定へ使用しない","when":"Governanceのevidenceまたはbranch-policy jobを実行する"}</code>
- <code>"AC-REPO-003-7"</code> 前提: Governance workflowを変更するPull Requestがある。条件: CIの自己統制境界を評価する。期待結果: workflow file自体をimmutableまたはtamper-proofとは表明せず、required checkのGitHub Actions由来sourceとworkflow差分を単一operatorが確認する。
  - criterion(JSON Object): <code>{"given":"Governance workflowを変更するPull Requestがある","id":"AC-REPO-003-7","then":"workflow file自体をimmutableまたはtamper-proofとは表明せず、required checkのGitHub Actions由来sourceとworkflow差分を単一operatorが確認する","when":"CIの自己統制境界を評価する"}</code>
- <code>"AC-REPO-003-8"</code> 前提: 既存の二層branch policyを変更するPull Requestまたはprotected branch pushがある。条件: baseまたはbefore側policyと候補policyを比較する。期待結果: 2回の管理された試行中はtrial.phase以外のmachine contract変更を拒否し、契約変更は試行停止後の別判断として扱う。
  - criterion(JSON Object): <code>{"given":"既存の二層branch policyを変更するPull Requestまたはprotected branch pushがある","id":"AC-REPO-003-8","then":"2回の管理された試行中はtrial.phase以外のmachine contract変更を拒否し、契約変更は試行停止後の別判断として扱う","when":"baseまたはbefore側policyと候補policyを比較する"}</code>

要求源(JSON List): <code>["user:2026-07-24","issue:#20","docs/decisions/ADR-0002-two-layer-branch-history.md"]</code>
検証方法: repository contract testと試行後review
検証証跡: trial設定、base/before validator選択、workflow自己統制限界、distribution非包含、昇格条件とrollbackの契約テスト
検証(JSON Object): <code>{"evidence":"trial設定、base/before validator選択、workflow自己統制限界、distribution非包含、昇格条件とrollbackの契約テスト","method":"repository contract testと試行後review"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/decisions/ADR-0002-two-layer-branch-history.md"]</code>
- 実装: <code>[]</code>
- テスト: <code>[]</code>
- 参照資料: <code>[]</code>
廃止理由: <code>"二層branch試行を終了し、portable guardrailからrepository policyを除外したため"</code>
後継要件: <code>""</code>

## REQ-SKILL-001: right-size-executionのSkill境界

要件ID(JSON): <code>"REQ-SKILL-001"</code>
タイトル(JSON): <code>"right-size-executionのSkill境界"</code>
主体(JSON): <code>"right-size-execution"</code>
対象(JSON): <code>"Estimate、ExecuteおよびExpandを一体化した再利用可能な実行制御契約"</code>
right-size-executionは、Estimate、ExecuteおよびExpandを一体化した再利用可能な実行制御契約を**提供する**。
行為enum: <code>"provide"</code>

根拠: Skill分割と既存工程責務の複製による選択・同期・contextコストを増やさないため。
根拠(JSON): <code>"Skill分割と既存工程責務の複製による選択・同期・contextコストを増やさないため。"</code>

項目版: 1 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"WI-20260718-right-size-execution-v2"</code>
分類: scope=<code>""</code> / category=<code>""</code>

受入条件:
- <code>"AC-SKILL-001-1"</code> 前提: Skillを配布する。条件: Skill構造を検査する。期待結果: 単一Skillが入力、出力、境界、判断規則、参照先、完了条件を持ち、要件管理、承認、標準合否、Git操作を複製しない。
  - criterion(JSON Object): <code>{"given":"Skillを配布する","id":"AC-SKILL-001-1","then":"単一Skillが入力、出力、境界、判断規則、参照先、完了条件を持ち、要件管理、承認、標準合否、Git操作を複製しない","when":"Skill構造を検査する"}</code>

要求源(JSON List): <code>["user:2026-07-18","arXiv:2602.12670","OpenAI:skills"]</code>
検証方法: 自動検査
検証証跡: Skill構造と責務境界の契約テスト
検証(JSON Object): <code>{"evidence":"Skill構造と責務境界の契約テスト","method":"自動検査"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/right-size-execution/SKILL.md"]</code>
- 実装: <code>[".agents/skills/right-size-execution/agents/openai.yaml"]</code>
- テスト: <code>["tests/test_skills.py"]</code>
- 参照資料: <code>["SWEBOK-V4A"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-SKILL-002: Skill制約のtrajectory検証

要件ID(JSON): <code>"REQ-SKILL-002"</code>
タイトル(JSON): <code>"Skill制約のtrajectory検証"</code>
主体(JSON): <code>"Skill検証基盤"</code>
対象(JSON): <code>"SKILL.mdの主要behavior constraintが代表trajectoryで実行された証拠"</code>
Skill検証基盤は、SKILL.mdの主要behavior constraintが代表trajectoryで実行された証拠を**検証する**。
行為enum: <code>"verify"</code>

根拠: テスト成功だけではSkill内の重要規則が実際に使われたことを保証できないため。
根拠(JSON): <code>"テスト成功だけではSkill内の重要規則が実際に使われたことを保証できないため。"</code>

項目版: 1 / 状態: `active` / 種別: `quality`
変更識別子: <code>"WI-20260718-right-size-execution-v2"</code>
分類: scope=<code>""</code> / category=<code>""</code>

受入条件:
- <code>"AC-SKILL-002-1"</code> 前提: 機械可読なbehavior constraintがある。条件: repository benchmarkを実行する。期待結果: 各constraintのconditionを発火させ、expected behaviorと実行証拠のcoverageを報告する。
  - criterion(JSON Object): <code>{"given":"機械可読なbehavior constraintがある","id":"AC-SKILL-002-1","then":"各constraintのconditionを発火させ、expected behaviorと実行証拠のcoverageを報告する","when":"repository benchmarkを実行する"}</code>

要求源(JSON List): <code>["user:2026-07-18","arXiv:2606.20659"]</code>
検証方法: 自動benchmark
検証証跡: behavior constraint coverageと未実行constraint一覧
検証(JSON Object): <code>{"evidence":"behavior constraint coverageと未実行constraint一覧","method":"自動benchmark"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/right-size-execution/assets/behavior-constraints.json"]</code>
- 実装: <code>[".agents/skills/right-size-execution/scripts/executionflow.py"]</code>
- テスト: <code>["tests/test_executionflow.py"]</code>
- 参照資料: <code>["SWEBOK-V4A"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-WORKBOOK-001: 再現可能で有界なワークブック

要件ID(JSON): <code>"REQ-WORKBOOK-001"</code>
タイトル(JSON): <code>"再現可能で有界なワークブック"</code>
主体(JSON): <code>"チェックリスト生成フロー"</code>
対象(JSON): <code>"実データ範囲だけを集計し決定的に再現できるレビュー用ワークブック"</code>
チェックリスト生成フローは、実データ範囲だけを集計し決定的に再現できるレビュー用ワークブックを**生成する**。
行為enum: <code>"generate"</code>

根拠: Excel全行参照は読込時に過大なメモリを消費し、固定集計値は項目追加時に陳腐化する。
根拠(JSON): <code>"Excel全行参照は読込時に過大なメモリを消費し、固定集計値は項目追加時に陳腐化する。"</code>

項目版: 2 / 状態: `active` / 種別: `operational`
変更識別子: <code>"CHG-20260802-skills-audit-remediation"</code>
分類: scope=<code>""</code> / category=<code>""</code>

受入条件:
- <code>"AC-WORKBOOK-001-1"</code> 前提: チェック項目の行数が変わる。条件: ワークブックを再生成する。期待結果: 集計式が各シートの実データ最終行へ更新され、実数と一致し、全列参照を含まない。
  - criterion(JSON Object): <code>{"given":"チェック項目の行数が変わる","id":"AC-WORKBOOK-001-1","then":"集計式が各シートの実データ最終行へ更新され、実数と一致し、全列参照を含まない","when":"ワークブックを再生成する"}</code>

要求源(JSON List): <code>["user:2026-07-18"]</code>
検証方法: 自動検査と描画確認
検証証跡: 数式範囲テスト、項目数照合、代表シートの描画結果
検証(JSON Object): <code>{"evidence":"数式範囲テスト、項目数照合、代表シートの描画結果","method":"自動検査と描画確認"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/README.md"]</code>
- 実装: <code>["update_checklist.py"]</code>
- テスト: <code>["tests/test_checklist.py"]</code>
- 参照資料: <code>["SWEBOK-V4A"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>
