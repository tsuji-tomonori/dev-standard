<!-- tools/quintflow.pyによる自動生成。spec/requirements/requirements.qntを編集すること。 -->
# dev-standard 要件一覧

- カタログ版: 10
- 更新日: 2026-08-27
- 正本: `spec/requirements/requirements.qnt`
- 機械可読view: `spec/requirements/requirements.json`

| ID | 版 | 状態 | 種別 | 原子的な義務 | 検証方法 |
|---|---:|---|---|---|---|
| `REQ-ASBUILT-001` | 1 | 有効 | 品質 | as-built設計generatorは、同一入力からバイト一致する設計出力を**生成する** | 自動テスト |
| `REQ-ASBUILT-002` | 1 | 有効 | 品質 | as-built設計generatorは、一つの生成logicを共有するgenerate modeとcheck modeを**提供する** | 自動テスト |
| `REQ-ASBUILT-003` | 1 | 有効 | 制約 | as-built生成物は、docs/design/generated/配下の直接編集禁止banner付き.gen.md設計を**分離する** | repository検査 |
| `REQ-ASBUILT-004` | 1 | 有効 | 機能 | as-built設計generatorは、handler ASTとOpenAPIとsampleとSQLから得たAPI詳細設計を**導出する** | 自動テスト |
| `REQ-ASBUILT-005` | 1 | 有効 | 機能 | as-built設計generatorは、handler metadataから得た重複のないAPI一覧を**導出する** | 自動テスト |
| `REQ-ASBUILT-006` | 1 | 有効 | データ | as-built設計generatorは、SQLと外部client呼出から得たtableおよび外部連携先のCRUD関係を**導出する** | 自動テスト |
| `REQ-ASBUILT-007` | 2 | 有効 | データ | as-built設計generatorは、正本DDLとSQLから得たtable定義とER関係と書込みAPIを**導出する** | 自動テスト |
| `REQ-ASBUILT-008` | 2 | 有効 | 機能 | as-built設計generatorは、E2E testのGiven When Then構造から得たscenario設計を**導出する** | 自動テスト |
| `REQ-ASBUILT-009` | 2 | 有効 | 運用 | as-built設計generatorは、外部report基盤の結果JSONから得たtest evidence viewを**導出する** | 契約テスト |
| `REQ-ASBUILT-010` | 2 | 有効 | 機能 | as-built設計generatorは、tool entrypoint ASTとdocstringから得たCLI仕様とflowを**導出する** | 自動テスト |
| `REQ-ASBUILT-011` | 2 | 有効 | データ | as-built設計generatorは、API error分岐から得た一意ID付きmachine-readable error caseを**生成する** | 自動テスト |
| `REQ-ASBUILT-012` | 2 | 有効 | 品質 | as-built整合checkは、handler登録と設計metadataとerror sampleの三点整合を**検証する** | 静的解析 |
| `REQ-ASBUILT-013` | 2 | 有効 | 品質 | as-built整合checkは、設計掲載sampleと実response assertionの対応を**検証する** | AST静的解析 |
| `REQ-ASBUILT-014` | 2 | 有効 | 品質 | as-built整合checkは、CUD操作を持つAPIとE2E状態assertの対応を**検証する** | 静的解析とE2E契約テスト |
| `REQ-ASBUILT-015` | 2 | 有効 | 品質 | 導入先repositoryのtestは、AAAまたはGWTとdocstringと1 case 1関数を持つtestを**構成する** | AST静的解析 |
| `REQ-ASBUILT-016` | 2 | 有効 | 品質 | 導入先repositoryのunit testは、C0命令網羅95%以上とC1分岐網羅90%以上のcoverageを**計測する** | coverage toolとreview contract |
| `REQ-ASBUILT-017` | 1 | 有効 | 制約 | as-built規約は、Rule IDからcatalog check IDへ接続された機械可読check定義を**維持する** | repository契約テスト |
| `REQ-ASBUILT-018` | 2 | 有効 | 運用 | as-built規約checkは、理由付きRule ID抑制箇所の監査一覧を**生成する** | 定期repository audit |
| `REQ-ASBUILT-019` | 2 | 有効 | 運用 | 導入先repositoryの品質検証は、testとstatic analysisと規約checkとcoverageを表示する外部report viewを**提供する** | CI契約レビュー |
| `REQ-DESIGN-001` | 2 | 有効 | 制約 | FastAPI実装フレームは、router.pyのオーケストレーションとfunctions.pyの具体処理に分けたoperationを**構成する** | 自動テスト |
| `REQ-DESIGN-002` | 2 | 有効 | 機能 | 設計生成器は、FastAPI routerの構文木から得たoperationシーケンス図を**導出する** | 自動テスト |
| `REQ-DESIGN-003` | 2 | 有効 | インターフェース | 設計生成器は、OpenAPI文書からのAPIとインターフェースの一覧を**導出する** | 自動テスト |
| `REQ-DESIGN-004` | 2 | 有効 | データ | 設計生成器は、生SQLからのquery objectとCRUD文書を**解析する** | 自動テスト |
| `REQ-DESIGN-005` | 2 | 有効 | 機能 | 設計生成器は、合成済みCloudFormationからのresourceとparameter一覧を**導出する** | 自動テスト |
| `REQ-DESIGN-006` | 3 | 有効 | 品質 | 設計フローは、実装成果物と自動生成された詳細設計の差分を**検出する** | 自動テスト |
| `REQ-DISC-001` | 2 | 有効 | 機能 | 開発エージェントは、適切な対話を通じたユーザーの意図する成果を**探り当てる** | 契約レビュー |
| `REQ-DISC-002` | 2 | 有効 | データ | 要件カタログは、正本要件IDごとの一つの原子的な義務を**維持する** | 自動テスト |
| `REQ-DISC-003` | 3 | 有効 | 機能 | 仕様管理フローは、版を進めて検証するQuint要件の追加、更新、廃止を**維持する** | Quint検証と自動テスト |
| `REQ-DISC-004` | 3 | 有効 | 機能 | 仕様管理フローは、QuintからJSONを経由した日本語の人間向け要件文書を**生成する** | 自動テスト |
| `REQ-DISC-005` | 1 | 有効 | 機能 | 要件管理Skillは、solution候補と権限ある永続要件を**分離する** | 自動テスト |
| `REQ-DOCS-001` | 1 | 有効 | 品質 | 文書生成フローは、識別子と固有名詞を除いて日本語で統一された利用者向け文書を**提供する** | 自動検査 |
| `REQ-EXEC-001` | 2 | 有効 | 運用 | 開発実行基盤は、相互に独立した変更範囲、保証水準、計算資源および実行方式を**推定する** | 自動テスト |
| `REQ-EXEC-002` | 2 | 有効 | 品質 | 開発実行基盤は、risk tag、成果物、外部副作用および不可逆性から導出したassurance下限を**強制する** | 自動テスト |
| `REQ-EXEC-003` | 2 | 有効 | 品質 | 開発実行基盤は、通常のルート判断と決定的metadataによる初期Estimateを**経路選択する** | 自動テスト |
| `REQ-EXEC-004` | 2 | 有効 | 品質 | 開発実行基盤は、実行制御へ入力するconfidenceの根拠とscoreを**制約する** | 自動テスト |
| `REQ-EXEC-005` | 1 | 有効 | 品質 | 開発実行基盤は、scope、assurance、成果物、risk、受入条件および必須gateから成るrequired verificationを**導出する** | 自動テスト |
| `REQ-EXEC-006` | 1 | 有効 | 品質 | 開発実行基盤は、初期profileを覆す新証拠に対応する一つの実行軸を**拡張する** | 自動テスト |
| `REQ-EXEC-007` | 1 | 有効 | 品質 | 開発実行基盤は、成功条件、required verificationおよびassurance floor充足後の正のコスト活動を**停止する** | 自動テスト |
| `REQ-EXEC-008` | 1 | 有効 | 品質 | 開発実行基盤は、推定、Estimate overhead、実績、Expand、品質および停止後活動の生指標を**計測する** | 自動テストとbenchmark |
| `REQ-EXEC-009` | 1 | 有効 | 品質 | 標準検証基盤は、version固定selectorによるチェック候補と選択漏れ監査sampleを**選択する** | 自動テストとbenchmark |
| `REQ-EXEC-010` | 1 | 有効 | 制約 | 実行効率制御は、telemetry、shadow、soft routing、assurance enforcement、calibrationおよび限定blockingの導入順序を**段階適用する** | 自動テスト |
| `REQ-FRAME-001` | 3 | 有効 | 制約 | リポジトリは、一時的な作業記録と永続的な製品要件を**分離する** | 自動検査 |
| `REQ-PORTABLE-001` | 3 | 有効 | 運用 | 移植可能なSkills集は、別リポジトリへのcopy-and-chat方式の導入を**実現する** | 自動テスト |
| `REQ-PORTABLE-002` | 1 | 有効 | 制約 | portable installerと既定profileは、導入先のbranch、merge rule、CI workflowを追加も変更もしないことを**維持する** | installer isolation test |
| `REQ-QUALITY-001` | 2 | 有効 | 運用 | 品質フレームは、SWEBOKとクラウド・AI公式資料の監査可能な出典台帳を**維持する** | 自動検査 |
| `REQ-QUALITY-002` | 3 | 有効 | 品質 | 品質フローは、変更と受入条件に関係する検査だけによる成果物検証を**検証する** | 契約テスト |
| `REQ-QUALITY-003` | 2 | 有効 | 品質 | チェックリスト生成フローは、一項目・一統制・一証跡で独立判定できるチェック項目を**維持する** | 自動テストと批判的レビュー |
| `REQ-QUALITY-004` | 1 | 有効 | 制約 | portable blocking guardrailは、要件正本、as-built生成、選択checkの3本柱だけを対象にすることを**制約する** | Quint invariant verification |
| `REQ-QUINT-001` | 1 | 有効 | 制約 | 永続要件は、Quint仕様を唯一の編集対象としJSONを派生物として維持することを**維持する** | Quint typecheckと生成drift検査 |
| `REQ-QUINT-002` | 1 | 有効 | 機能 | 要件生成器は、Quintから正規化JSONを生成し、そのJSONから人向けMarkdownを生成することを**生成する** | 決定的生成テスト |
| `REQ-QUINT-003` | 1 | 有効 | 品質 | Skill形式仕様は、すべてのSkillを一対一のQuint契約へ対応付けることを**形式化する** | Quint testとinventory集合比較 |
| `REQ-REPO-001` | 2 | 廃止 | 制約 | dev-standardのbranch運用は、mainへのsquashとdevへのmerge commitを分離したbranch別統合契約を**強制する** | CIとGitHub ruleset監査 |
| `REQ-REPO-002` | 2 | 廃止 | 運用 | release operatorとCIは、release前後のancestor関係、tip tree条件、freezeを含むreconciliation transactionを**維持する** | branch graph回帰テストとCI |
| `REQ-REPO-003` | 2 | 廃止 | 制約 | dev-standardの二層branch試行は、2回のrelease cycleに限定しportable profileへ既定配布しない二層branch試行を**制約する** | repository contract testと試行後review |
| `REQ-SKILL-001` | 1 | 有効 | 制約 | right-size-executionは、Estimate、ExecuteおよびExpandを一体化した再利用可能な実行制御契約を**提供する** | 自動検査 |
| `REQ-SKILL-002` | 1 | 有効 | 品質 | Skill検証基盤は、SKILL.mdの主要behavior constraintが代表trajectoryで実行された証拠を**検証する** | 自動benchmark |
| `REQ-WORKBOOK-001` | 2 | 有効 | 運用 | チェックリスト生成フローは、実データ範囲だけを集計し決定的に再現できるレビュー用ワークブックを**生成する** | 自動検査と描画確認 |

## REQ-ASBUILT-001: as-built生成の決定論性

as-built設計generatorは、同一入力からバイト一致する設計出力を**生成する**。

根拠: 差分によるdrift検知には非決定要素を除いた再現可能な出力が必要である。

受入条件:
- `AC-ASBUILT-001-1` 前提: 同一revisionの宣言済み一次情報がある。条件: generatorを複数回実行する。期待結果: 列挙順が固定され、時刻・乱数・環境依存pathを含まないバイト一致出力になる。

要求源: user:2026-07-21, docs/standards/AS-BUILT-DESIGN.md
検証証跡: 同一fixtureを複数回生成したbyte比較
トレース: 設計=docs/standards/AS-BUILT-DESIGN.md; 実装=governance/checks/catalog.yaml,.agents/skills/generate-implementation-design/scripts/designflow.py; テスト=tests/test_review_contract.py,tests/test_designflow.py; 参照資料=DEVSTD-AS-BUILT

## REQ-ASBUILT-002: generateとcheckの二相契約

as-built設計generatorは、一つの生成logicを共有するgenerate modeとcheck modeを**提供する**。

根拠: 生成と検査を別実装にすると両者の意味が乖離する。

受入条件:
- `AC-ASBUILT-002-1` 前提: 宣言済み生成対象と既存生成物がある。条件: check modeを実行する。期待結果: 生成logicを再利用して既存生成物と比較し、差分pathを列挙して非0終了する。

要求源: user:2026-07-21, docs/standards/AS-BUILT-DESIGN.md
検証証跡: write modeとcheck modeの同一出力およびdrift終了code
トレース: 設計=docs/standards/AS-BUILT-DESIGN.md; 実装=governance/checks/catalog.yaml,.agents/skills/generate-implementation-design/scripts/designflow.py; テスト=tests/test_review_contract.py,tests/test_designflow.py; 参照資料=DEVSTD-AS-BUILT

## REQ-ASBUILT-003: 生成設計の隔離と識別

as-built生成物は、docs/design/generated/配下の直接編集禁止banner付き.gen.md設計を**分離する**。

根拠: 専用path、命名、更新commandにより手書き設計との混在と直接編集を防げる。

受入条件:
- `AC-ASBUILT-003-1` 前提: Markdown形式のas-built設計を生成する。条件: 生成物の配置と先頭行を検査する。期待結果: docs/design/generated/配下の.gen.mdでありgenerate/check commandを含む直接編集禁止bannerがあり、同じ現在状態の手書き設計が存在しない。

要求源: user:2026-07-21, docs/standards/AS-BUILT-DESIGN.md
検証証跡: 生成path、file名、banner、重複設計scan
トレース: 設計=docs/standards/AS-BUILT-DESIGN.md; 実装=.agents/skills/generate-implementation-design/SKILL.md,governance/checks/catalog.yaml,.agents/skills/generate-implementation-design/scripts/designflow.py; テスト=tests/test_review_contract.py,tests/test_designflow.py; 参照資料=DEVSTD-AS-BUILT

## REQ-ASBUILT-004: API詳細設計の導出

as-built設計generatorは、handler ASTとOpenAPIとsampleとSQLから得たAPI詳細設計を**導出する**。

根拠: APIのinterfaceと実行flowを同じ一次情報から導出すると実装との1対1対応を維持できる。

受入条件:
- `AC-ASBUILT-004-1` 前提: handler、framework OpenAPI、sample定数、生SQLがある。条件: API設計を生成する。期待結果: interface、sequence、処理step、error分岐、message、unit-test観点をhandler起点で生成する。

要求源: user:2026-07-21, docs/standards/AS-BUILT-DESIGN.md
検証証跡: API fixtureからの生成内容assert
トレース: 設計=docs/standards/AS-BUILT-DESIGN.md; 実装=.agents/skills/generate-implementation-design/SKILL.md,governance/checks/catalog.yaml,.agents/skills/generate-implementation-design/scripts/designflow.py; テスト=tests/test_review_contract.py,tests/test_designflow.py; 参照資料=DEVSTD-AS-BUILT

## REQ-ASBUILT-005: API一覧の導出

as-built設計generatorは、handler metadataから得た重複のないAPI一覧を**導出する**。

根拠: route metadataを正本にすると別管理のAPI台帳を不要にできる。

受入条件:
- `AC-ASBUILT-005-1` 前提: handler decoratorに設計metadataがある。条件: API一覧を生成する。期待結果: operation、API番号、権限、業務概要を重複なく列挙する。

要求源: user:2026-07-21, docs/standards/AS-BUILT-DESIGN.md
検証証跡: metadata fixtureからのAPI一覧assert
トレース: 設計=docs/standards/AS-BUILT-DESIGN.md; 実装=.agents/skills/generate-implementation-design/SKILL.md,governance/checks/catalog.yaml,.agents/skills/generate-implementation-design/scripts/designflow.py; テスト=tests/test_review_contract.py,tests/test_designflow.py; 参照資料=DEVSTD-AS-BUILT

## REQ-ASBUILT-006: CRUD関係の導出

as-built設計generatorは、SQLと外部client呼出から得たtableおよび外部連携先のCRUD関係を**導出する**。

根拠: 静的解析されたデータ操作をAPIへ接続するとCRUD図を手書きせず維持できる。

受入条件:
- `AC-ASBUILT-006-1` 前提: endpoint別SQLと外部client呼出がある。条件: CRUD設計を生成する。期待結果: SELECTをR、INSERTをC、UPDATEをU、DELETEをDとしてtable×APIと外部連携先×APIを生成する。

要求源: user:2026-07-21, docs/standards/AS-BUILT-DESIGN.md
検証証跡: SQLおよびclient fixtureからのCRUD matrix assert
トレース: 設計=docs/standards/AS-BUILT-DESIGN.md; 実装=.agents/skills/generate-implementation-design/SKILL.md,governance/checks/catalog.yaml,.agents/skills/generate-implementation-design/scripts/designflow.py; テスト=tests/test_review_contract.py,tests/test_designflow.py; 参照資料=DEVSTD-AS-BUILT

## REQ-ASBUILT-007: DB設計の導出

as-built設計generatorは、正本DDLとSQLから得たtable定義とER関係と書込みAPIを**導出する**。

根拠: DDLとSQLを一次情報にするとDB設計の二重管理を避けられる。

受入条件:
- `AC-ASBUILT-007-1` 前提: repository内に正本DDLとendpoint別SQLがある。条件: DB設計を生成する。期待結果: table、column、constraint、ER関係をDDLから生成し、columnへの書込みAPIをSQL解析から導出する。

要求源: user:2026-07-21, docs/standards/AS-BUILT-DESIGN.md
検証証跡: DDLおよびSQL fixtureからのDB設計assert
トレース: 設計=docs/standards/AS-BUILT-DESIGN.md; 実装=governance/checks/catalog.yaml,.agents/skills/generate-implementation-design/scripts/designflow.py; テスト=tests/test_review_contract.py,tests/test_designflow.py; 参照資料=DEVSTD-AS-BUILT

## REQ-ASBUILT-008: E2E scenario設計の導出

as-built設計generatorは、E2E testのGiven When Then構造から得たscenario設計を**導出する**。

根拠: test codeをscenarioの正本にすると実行可能な仕様と設計表示を一致させられる。

受入条件:
- `AC-ASBUILT-008-1` 前提: E2E testにGiven、When、Then sectionがある。条件: scenario設計を生成する。期待結果: 前提、操作、期待状態をtest codeから順序どおり生成する。

要求源: user:2026-07-21, docs/standards/AS-BUILT-DESIGN.md
検証証跡: E2E fixtureからのscenario出力assert
トレース: 設計=docs/standards/AS-BUILT-DESIGN.md; 実装=governance/checks/catalog.yaml,.agents/skills/generate-implementation-design/scripts/designflow.py; テスト=tests/test_review_contract.py,tests/test_designflow.py; 参照資料=DEVSTD-AS-BUILT

## REQ-ASBUILT-009: test evidence viewの外部集約

as-built設計generatorは、外部report基盤の結果JSONから得たtest evidence viewを**導出する**。

根拠: 実行結果を外部正本から整形すればrepositoryへtest reportを複製せず追跡できる。

受入条件:
- `AC-ASBUILT-009-1` 前提: 外部report基盤にtest結果JSONがある。条件: test evidence viewを生成する。期待結果: status、API response、DB結果、mock受信結果への参照を整形し、実行結果本文をrepositoryへ保存しない。

要求源: user:2026-07-21, docs/standards/AS-BUILT-DESIGN.md
検証証跡: report fixtureとrepository非保存規則のassert
トレース: 設計=docs/standards/AS-BUILT-DESIGN.md; 実装=governance/checks/catalog.yaml,.agents/skills/generate-implementation-design/scripts/designflow.py; テスト=tests/test_review_contract.py,tests/test_designflow.py; 参照資料=DEVSTD-AS-BUILT

## REQ-ASBUILT-010: generator tool設計の導出

as-built設計generatorは、tool entrypoint ASTとdocstringから得たCLI仕様とflowを**導出する**。

根拠: generator自身を同じ方式で可視化すると抽出可能性をdogfoodingできる。

受入条件:
- `AC-ASBUILT-010-1` 前提: tool entrypointと呼出先関数にdocstringがある。条件: tool設計を生成する。期待結果: CLI argument、制御flow、関数責務をASTとdocstring先頭1行から生成する。

要求源: user:2026-07-21, docs/standards/AS-BUILT-DESIGN.md
検証証跡: tool fixtureからのCLIおよびflow assert
トレース: 設計=docs/standards/AS-BUILT-DESIGN.md; 実装=governance/checks/catalog.yaml,.agents/skills/generate-implementation-design/scripts/designflow.py; テスト=tests/test_review_contract.py,tests/test_designflow.py; 参照資料=DEVSTD-AS-BUILT

## REQ-ASBUILT-011: error case定義の生成

as-built設計generatorは、API error分岐から得た一意ID付きmachine-readable error caseを**生成する**。

根拠: error分岐を機械可読にするとE2Eとの1対1 coverageを検査できる。

受入条件:
- `AC-ASBUILT-011-1` 前提: API handlerに正規化されたerror分岐がある。条件: API設計を生成する。期待結果: 各error分岐へ安定IDを付けたmachine-readable定義を出力する。

要求源: user:2026-07-21, docs/standards/AS-BUILT-DESIGN.md
検証証跡: error branch fixtureからのcase ID出力assert
トレース: 設計=docs/standards/AS-BUILT-DESIGN.md; 実装=governance/checks/catalog.yaml,.agents/skills/generate-implementation-design/scripts/designflow.py; テスト=tests/test_review_contract.py,tests/test_designflow.py; 参照資料=DEVSTD-AS-BUILT

## REQ-ASBUILT-012: 実装仕様sample三点整合

as-built整合checkは、handler登録と設計metadataとerror sampleの三点整合を**検証する**。

根拠: 実装、interface情報、設計掲載sampleの片落ちを静的に検出する必要がある。

受入条件:
- `AC-ASBUILT-012-1` 前提: API handler、OpenAPI metadata、error sampleがある。条件: 公開API変更の整合checkを実行する。期待結果: handler登録漏れ、metadata欠落、error分岐に対応するsample不足を検出する。

要求源: user:2026-07-21, docs/standards/AS-BUILT-DESIGN.md
検証証跡: 不整合fixtureを拒否するcheck結果
トレース: 設計=docs/standards/AS-BUILT-DESIGN.md; 実装=governance/checks/catalog.yaml,.agents/skills/verify-against-engineering-standards/references/as-built-design-check-selection.md,.agents/skills/generate-implementation-design/scripts/qualityflow.py; テスト=tests/test_review_contract.py,tests/test_qualityflow.py; 参照資料=DEVSTD-AS-BUILT

## REQ-ASBUILT-013: sampleとtestの整合

as-built整合checkは、設計掲載sampleと実response assertionの対応を**検証する**。

根拠: 設計書に掲載する例をtest済みに限定すると表示と振る舞いの乖離を防げる。

受入条件:
- `AC-ASBUILT-013-1` 前提: 正常または異常response sampleがある。条件: sample整合checkを実行する。期待結果: 各sampleが対応testから参照され、実responseとのassertに使用されていることを検出する。

要求源: user:2026-07-21, docs/standards/AS-BUILT-DESIGN.md
検証証跡: 未参照sampleと未assert sampleを拒否するcheck結果
トレース: 設計=docs/standards/AS-BUILT-DESIGN.md; 実装=governance/checks/catalog.yaml,.agents/skills/verify-against-engineering-standards/references/as-built-design-check-selection.md,.agents/skills/generate-implementation-design/scripts/qualityflow.py; テスト=tests/test_review_contract.py,tests/test_qualityflow.py; 参照資料=DEVSTD-AS-BUILT

## REQ-ASBUILT-014: CRUDとE2E状態検証の整合

as-built整合checkは、CUD操作を持つAPIとE2E状態assertの対応を**検証する**。

根拠: API responseだけでなく永続状態と外部状態を検証してデータ更新の回帰を検出する必要がある。

受入条件:
- `AC-ASBUILT-014-1` 前提: CRUD図でC、U、Dを持つAPIがある。条件: CRUD E2E整合checkを実行する。期待結果: 正常系E2EがDBまたは外部連携先の変更状態をassertし、異常系が状態不変または理由付き許可変化をassertする。

要求源: user:2026-07-21, docs/standards/AS-BUILT-DESIGN.md
検証証跡: 状態assert欠落fixtureを拒否するcheck結果
トレース: 設計=docs/standards/AS-BUILT-DESIGN.md; 実装=governance/checks/catalog.yaml,.agents/skills/verify-against-engineering-standards/references/as-built-design-check-selection.md,.agents/skills/generate-implementation-design/scripts/qualityflow.py; テスト=tests/test_review_contract.py,tests/test_qualityflow.py; 参照資料=DEVSTD-AS-BUILT

## REQ-ASBUILT-015: 解析可能なtest構造

導入先repositoryのtestは、AAAまたはGWTとdocstringと1 case 1関数を持つtestを**構成する**。

根拠: 構造化されたtest codeをscenario設計とレビュー観点の一次情報にできる。

受入条件:
- `AC-ASBUILT-015-1` 前提: as-built標準を採用したtest codeがある。条件: test構造checkを実行する。期待結果: unit testのAAA、E2EのGWT、docstring、1 case 1関数を評価し、導入時はAdvisoryとして報告する。

要求源: user:2026-07-21, docs/standards/AS-BUILT-DESIGN.md
検証証跡: test構造fixtureとAdvisory結果
トレース: 設計=docs/standards/AS-BUILT-DESIGN.md; 実装=governance/checks/catalog.yaml,.agents/skills/verify-against-engineering-standards/references/as-built-design-check-selection.md,.agents/skills/generate-implementation-design/scripts/qualityflow.py; テスト=tests/test_review_contract.py,tests/test_qualityflow.py; 参照資料=DEVSTD-AS-BUILT

## REQ-ASBUILT-016: unit test coverage目標

導入先repositoryのunit testは、C0命令網羅95%以上とC1分岐網羅90%以上のcoverageを**計測する**。

根拠: 高い命令・分岐網羅を測定目標にしつつ、導入直後のfalse blockerを避けて効果を実測する。

受入条件:
- `AC-ASBUILT-016-1` 前提: as-built標準を採用したunit test suiteがある。条件: coverageを測定する。期待結果: C0 95%以上とC1 90%以上をAdvisoryとして評価し、実測に基づく昇格判断まで無条件blockingにしない。

要求源: user:2026-07-21, docs/standards/AS-BUILT-DESIGN.md
検証証跡: C0 C1測定結果への外部CI参照とAdvisory分類
トレース: 設計=docs/standards/AS-BUILT-DESIGN.md; 実装=governance/checks/catalog.yaml,.agents/skills/retrospect-and-improve/SKILL.md,.agents/skills/generate-implementation-design/scripts/qualityflow.py,.github/workflows/governance.yml; テスト=tests/test_review_contract.py,tests/test_qualityflow.py; 参照資料=DEVSTD-AS-BUILT

## REQ-ASBUILT-017: as-built check定義の単一正本

as-built規約は、Rule IDからcatalog check IDへ接続された機械可読check定義を**維持する**。

根拠: Markdown tagとcatalogの二重定義を避けるとclass、trigger、enforcementを一か所で変更できる。

受入条件:
- `AC-ASBUILT-017-1` 前提: as-built標準に規範Rule IDがある。条件: check mappingを検査する。期待結果: check ID、class、timing、trigger、acceptance、enforcementがcatalogだけで定義され、標準が対応check IDを参照する。

要求源: user:2026-07-21, docs/standards/AS-BUILT-DESIGN.md
検証証跡: 標準Rule IDとcatalog IDの対応assert
トレース: 設計=docs/standards/AS-BUILT-DESIGN.md; 実装=governance/checks/catalog.yaml,docs/standards/AS-BUILT-DESIGN.md; テスト=tests/test_review_contract.py; 参照資料=DEVSTD-AS-BUILT

## REQ-ASBUILT-018: 抑制例外の可視化

as-built規約checkは、理由付きRule ID抑制箇所の監査一覧を**生成する**。

根拠: 例外を一覧化するとsilent suppressionと恒久化した例外を定期監査できる。

受入条件:
- `AC-ASBUILT-018-1` 前提: コードにignore Rule ID commentがある。条件: 抑制一覧を生成してGovernance Auditを実行する。期待結果: 全抑制path、Rule ID、理由を列挙し、理由欠落、孤児、反復を検出する。

要求源: user:2026-07-21, docs/standards/AS-BUILT-DESIGN.md
検証証跡: 抑制inventoryとAUD-008結果
トレース: 設計=docs/standards/AS-BUILT-DESIGN.md; 実装=governance/checks/catalog.yaml,.agents/skills/generate-implementation-design/scripts/qualityflow.py; テスト=tests/test_review_contract.py,tests/test_qualityflow.py; 参照資料=DEVSTD-AS-BUILT

## REQ-ASBUILT-019: 品質結果の外部集約

導入先repositoryの品質検証は、testとstatic analysisと規約checkとcoverageを表示する外部report viewを**提供する**。

根拠: 品質結果を一画面で追跡しつつ生logとtest reportのrepository複製を避けられる。

受入条件:
- `AC-ASBUILT-019-1` 前提: 複数の品質checkをCIで実行する。条件: 品質結果を報告する。期待結果: 外部report基盤へ結果を集約し、repositoryにはworkflow名、check ID、証拠pathだけを記録する。

要求源: user:2026-07-21, docs/standards/AS-BUILT-DESIGN.md
検証証跡: workflow参照とrepository非複製確認
トレース: 設計=docs/standards/AS-BUILT-DESIGN.md; 実装=governance/reviews/README.md,.agents/skills/generate-implementation-design/scripts/qualityflow.py,.github/workflows/governance.yml; テスト=tests/test_review_contract.py,tests/test_qualityflow.py; 参照資料=DEVSTD-AS-BUILT

## REQ-DESIGN-001: FastAPI operation構成

FastAPI実装フレームは、router.pyのオーケストレーションとfunctions.pyの具体処理に分けたoperationを**構成する**。

根拠: 安定したoperation境界により、処理フローの導出と詳細設計の決定的な検査ができる。

受入条件:
- `AC-DESIGN-001-1` 前提: FastAPI operationを実装している。条件: ソース構成を検査する。期待結果: router.pyが処理の流れを公開し、functions.pyが具体処理を持つ。

要求源: user:2026-07-17
検証証跡: routerのAST契約テスト
トレース: 設計=.agents/skills/generate-implementation-design/references/fastapi-contract.md; 実装=.agents/skills/generate-implementation-design/SKILL.md; テスト=tests/test_designflow.py; 参照資料=SWEBOK-V4A

## REQ-DESIGN-002: routerからのシーケンス図導出

設計生成器は、FastAPI routerの構文木から得たoperationシーケンス図を**導出する**。

根拠: 実装から導出したフロー文書はソースとの整合を維持できる。

受入条件:
- `AC-DESIGN-002-1` 前提: router.pyに有効なroute関数がある。条件: FastAPI設計生成器を実行する。期待結果: 生成Mermaidが実行時の呼出順を保ち、decoratorを除外する。

要求源: user:2026-07-17
検証証跡: シーケンス出力のアサーション
トレース: 設計=.agents/skills/generate-implementation-design/references/fastapi-contract.md; 実装=.agents/skills/generate-implementation-design/scripts/designflow.py; テスト=tests/test_designflow.py; 参照資料=SWEBOK-V4A

## REQ-DESIGN-003: OpenAPIからのインターフェース設計導出

設計生成器は、OpenAPI文書からのAPIとインターフェースの一覧を**導出する**。

根拠: OpenAPIを実行可能なIF正本とすることで、手作業カタログの重複を避ける。

受入条件:
- `AC-DESIGN-003-1` 前提: アプリケーションが生成したOpenAPI文書がある。条件: FastAPI設計生成器を実行する。期待結果: operation IDを重複させずにAPI、request、response、schema文書を生成する。

要求源: user:2026-07-17, OpenAPI Specification 3.1.1, FastAPI OpenAPI documentation
検証証跡: OpenAPI fixtureの出力アサーション
トレース: 設計=.agents/skills/generate-implementation-design/references/fastapi-contract.md; 実装=.agents/skills/generate-implementation-design/scripts/designflow.py; テスト=tests/test_designflow.py; 参照資料=SWEBOK-V4A

## REQ-DESIGN-004: SQLからのデータ設計導出

設計生成器は、生SQLからのquery objectとCRUD文書を**解析する**。

根拠: AST解析は構造的な証跡を作り、無効なSQLを推測せず拒否する。

受入条件:
- `AC-DESIGN-004-1` 前提: 実行可能な生SQLファイルがある。条件: FastAPI設計生成器を実行する。期待結果: SQL構文木からquery objectとtable CRUD関係を生成する。

要求源: user:2026-07-17, SQLGlot documentation
検証証跡: SQL AST fixtureとCRUD出力のアサーション
トレース: 設計=.agents/skills/generate-implementation-design/references/fastapi-contract.md; 実装=.agents/skills/generate-implementation-design/scripts/designflow.py; テスト=tests/test_designflow.py; 参照資料=SWEBOK-V4A

## REQ-DESIGN-005: CDKデプロイ設計の生成

設計生成器は、合成済みCloudFormationからのresourceとparameter一覧を**導出する**。

根拠: 合成されたデプロイテンプレートが具体的なインフラストラクチャIFである。

受入条件:
- `AC-DESIGN-005-1` 前提: AWS CDK stackがCloudFormation YAMLまたはJSONを合成している。条件: CDK設計生成器を実行する。期待結果: テンプレートからresourceとparameterの詳細文書を生成する。

要求源: user:2026-07-17, AWS CDK synth documentation, CloudFormation template anatomy
検証証跡: CloudFormation fixtureの出力アサーション
トレース: 設計=.agents/skills/generate-implementation-design/references/cdk-contract.md; 実装=.agents/skills/generate-implementation-design/scripts/designflow.py; テスト=tests/test_designflow.py; 参照資料=AWS-WAF

## REQ-DESIGN-006: 実装と設計の差分検出

設計フローは、実装成果物と自動生成された詳細設計の差分を**検出する**。

根拠: digestと決定論的なバイト比較により実装と設計の1対1再現性を強制し、更新漏れの対象pathを特定する。

受入条件:
- `AC-DESIGN-006-1` 前提: 宣言済みの自動生成設計がある。条件: 設計check modeを実行する。期待結果: source SHA-256 manifestとクリーンな再生成結果がバイト単位で一致し、差分時は対象pathを列挙して非0終了する。

要求源: user:2026-07-17, user:2026-07-21, docs/standards/AS-BUILT-DESIGN.md
検証証跡: 変更済みsourceを用いたdriftと差分pathの検出テスト
トレース: 設計=.agents/skills/generate-implementation-design/SKILL.md,docs/standards/AS-BUILT-DESIGN.md; 実装=.agents/skills/generate-implementation-design/scripts/designflow.py,governance/checks/catalog.yaml; テスト=tests/test_designflow.py,tests/test_review_contract.py; 参照資料=SWEBOK-V4A,DEVSTD-AS-BUILT

## REQ-DISC-001: 研究に裏付けられた意図の探索

開発エージェントは、適切な対話を通じたユーザーの意図する成果を**探り当てる**。

根拠: 言語化しきれていない要求を負担なく探り当てるには、心地よい傾聴と精密な言語化が必要である。

受入条件:
- `AC-DISC-001-1` 前提: ユーザーの要求が不完全または曖昧である。条件: 解釈差が成果を変える。期待結果: 推定した目的、制約、葛藤、最小限の重要質問を迎合せず提示する。

要求源: user:2026-07-17, Design Council Double Diamond, calibrated listening research
検証証跡: Skill指示と研究根拠
トレース: 設計=.agents/skills/maintain-canonical-requirements/references/research-basis.md; 実装=.agents/skills/maintain-canonical-requirements/SKILL.md,.agents/skills/calibrated-collaborative-listening/SKILL.md; テスト=tests/test_skills.py; 参照資料=SWEBOK-V4A

## REQ-DISC-002: 原子的な永続要件

要件カタログは、正本要件IDごとの一つの原子的な義務を**維持する**。

根拠: 原子的な要件は独立した変更、検証、トレーサビリティを可能にする。

受入条件:
- `AC-DISC-002-1` 前提: 永続的な義務が受け入れられている。条件: 要件を永続化する。期待結果: 一つのID、主体、正規化action、対象、状態、受入条件、検証、traceを正本に持つ。

要求源: user:2026-07-17, SWEBOK Software Requirements
検証証跡: 複合または不完全な義務をスキーマ検証が拒否する記録
トレース: 設計=.agents/skills/maintain-canonical-requirements/assets/requirements.schema.json; 実装=.agents/skills/maintain-canonical-requirements/scripts/specflow.py; テスト=tests/test_specflow.py; 参照資料=SWEBOK-V4A

## REQ-DISC-003: 安全な要件ライフサイクル変更

仕様管理フローは、版を進めて検証するQuint要件の追加、更新、廃止を**維持する**。

根拠: 一次言語を一つに保ち、版更新、完全検証、廃止墓標により更新消失と履歴消去を防ぐ。

受入条件:
- `AC-DISC-003-1` 前提: Quint要件を追加または更新する。条件: 変更を確定する。期待結果: catalogRevisionと対象revisionを進め、typecheckと不変条件検査を通してからJSONとMarkdownを再生成する。
- `AC-DISC-003-2` 前提: 正本だった要件の削除が要求される。条件: 変更を受け入れる。期待結果: 理由付きの廃止墓標として項目を残す。

要求源: user:2026-07-17, user:2026-08-27
検証証跡: 型検査、生成drift、廃止墓標の検査
トレース: 設計=.agents/skills/maintain-canonical-requirements/SKILL.md; 実装=spec/requirements/requirements.qnt,tools/quintflow.py; テスト=tests/test_quintflow.py,tests/test_specflow.py; 参照資料=SWEBOK-V4A,QUINT-0.32

## REQ-DISC-004: 要件文書の自動生成

仕様管理フローは、QuintからJSONを経由した日本語の人間向け要件文書を**生成する**。

根拠: 生成ビューは競合する編集可能な正本を作らずに読者へ情報を提供する。

受入条件:
- `AC-DISC-004-1` 前提: Quint正本が有効である。条件: 文書生成と差分検査を実行する。期待結果: Quintから正規化JSONを生成し、そのJSONから日本語文書をバイト一致で再現する。

要求源: user:2026-07-17, user:2026-08-27
検証証跡: 生成文書の完全一致検査
トレース: 設計=docs/requirements/REQUIREMENTS.md; 実装=tools/quintflow.py,.agents/skills/maintain-canonical-requirements/scripts/specflow.py; テスト=tests/test_quintflow.py,tests/test_specflow.py; 参照資料=SWEBOK-V4A,QUINT-0.32

## REQ-DISC-005: solution候補と永続要件の境界

要件管理Skillは、solution候補と権限ある永続要件を**分離する**。

根拠: 結果や品質ではなく可逆な実装手段を正本へ固定すると設計裁量と変更容易性を失う一方、契約、法令、互換性、既存基盤、support境界または親判断に基づく正当な制約は保持する必要があるため。

分類: `product` / `functional`

受入条件:
- `AC-DISC-005-1` 前提: technology、architecture、tool、path、process、工程または成果物を名指しする要件候補がある。条件: 正本への反映可否を判定する。期待結果: underlying outcome、necessity、authority、lifetime、scope、placementを判定し、可逆なsolution choiceを永続要件へ固定しない。
- `AC-DISC-005-2` 前提: exact technology、architectureまたはproject process自体が権限ある永続制約である。条件: 永続要件として保持する。期待結果: source_refs、必要性を示すrationale、scopeとcategory、verificationを記録する。
- `AC-DISC-005-3` 前提: 親要件または承認済みarchitecture decisionが下位scopeを拘束する。条件: 下位の永続義務として保持する。期待結果: 親要件またはdecision、下位scope、verificationへtraceしたderived requirementとして記録し、上位stakeholder requirementへ過剰一般化しない。

要求源: user:2026-07-24, issue:25, NASA Systems Engineering Handbook Appendix, NASA SWE-050, SWEBOK-V4A, Nuseibeh:10.1109/2.910904, Chen-Babar-Nuseibeh:10.1109/MS.2012.174
検証証跡: solution-only instruction、権限あるtechnology constraint、quality-of-service、ADR、derived requirement、product identityのpositive / negative contract test
トレース: 設計=docs/standards/REQUIREMENT-CLASSIFICATION.md,docs/reference/development.md,.agents/skills/maintain-canonical-requirements/references/research-basis.md; 実装=.agents/skills/maintain-canonical-requirements/SKILL.md,.agents/skills/chat-first-development/SKILL.md,.agents/skills/elicit-frontend-requirements/SKILL.md,.codex/agents/requirements-reviewer.toml,.agents/skills/maintain-canonical-requirements/assets/requirements.schema.json; テスト=tests/test_skills.py,tests/test_specflow.py; 参照資料=SWEBOK-V4A

## REQ-DOCS-001: 日本語の利用者向け文書

文書生成フローは、識別子と固有名詞を除いて日本語で統一された利用者向け文書を**提供する**。

根拠: 導入・運用・監査の文書言語を統一し、意味の取り違えと二重保守を防ぐ。

受入条件:
- `AC-DOCS-001-1` 前提: 利用者向けMarkdownまたは生成文書がある。条件: リポジトリ検証を実行する。期待結果: 見出しと説明が日本語であり、生成物が日本語テンプレートから再現される。

要求源: user:2026-07-18
検証証跡: 日本語文書検査と生成差分テスト
トレース: 設計=docs/README.md; 実装=.agents/skills/maintain-canonical-requirements/scripts/specflow.py,.agents/skills/verify-against-engineering-standards/scripts/standardsflow.py; テスト=tests/test_validate_repo.py,tests/test_specflow.py,tests/test_standardsflow.py; 参照資料=SWEBOK-V4A

## REQ-EXEC-001: 多軸execution profileの推定

開発実行基盤は、相互に独立した変更範囲、保証水準、計算資源および実行方式を**推定する**。

根拠: 局所的だが重大な変更と、広範囲だが機械的な変更を単一レベルで混同しないため。

受入条件:
- `AC-EXEC-001-1` 前提: repository変更依頼と決定的metadataがある。条件: 実装前profileを生成する。期待結果: scope、assurance、compute、modeを直接根拠とともに独立記録し、同一入力とpolicyから同一profileを生成する。

要求源: user:2026-07-18, arXiv:2607.13034, arXiv:2407.01489
検証証跡: 多軸独立性、schema適合性および再現性の回帰テスト
トレース: 設計=.agents/skills/right-size-execution/references/execution-dimensions.md; 実装=.agents/skills/right-size-execution/scripts/executionflow.py,.agents/skills/right-size-execution/assets/execution-policy.json,.agents/skills/right-size-execution/assets/execution-profile.schema.json; テスト=tests/test_executionflow.py; 参照資料=SWEBOK-V4A

## REQ-EXEC-002: 保証水準の下限制御

開発実行基盤は、risk tag、成果物、外部副作用および不可逆性から導出したassurance下限を**強制する**。

根拠: 重大性は探索範囲ではなく必要な保証の深さへ反映すべきである。

受入条件:
- `AC-EXEC-002-1` 前提: 変更特徴とrisk tagがある。条件: assuranceを推定または監査する。期待結果: criticalまたはelevatedの下限を決定し、高リスクだけを理由にscopeをrepositoryへ広げない。

要求源: user:2026-07-18, SWEBOK-V4A
検証証跡: local-criticalとrepository-standardの交差ケース
トレース: 設計=.agents/skills/right-size-execution/references/execution-dimensions.md; 実装=.agents/skills/right-size-execution/scripts/executionflow.py,.agents/skills/right-size-execution/assets/execution-policy.json; テスト=tests/test_executionflow.py; 参照資料=SWEBOK-V4A

## REQ-EXEC-003: 追加LLM呼出しを伴わない初期推定

開発実行基盤は、通常のルート判断と決定的metadataによる初期Estimateを**経路選択する**。

根拠: Estimate自体が余分なLLMコストになり、単純な作業の利点を失うことを防ぐため。

受入条件:
- `AC-EXEC-003-1` 前提: 依頼文、path、manifestまたは依存metadataがある。条件: 初期profileを推定する。期待結果: Estimate専用LLMを呼ばず、結果を変える不明点だけmetadata probeを最大一回実行して費用を記録する。

要求源: user:2026-07-18, ACL:2024.naacl-long.389
検証証跡: probe上限、再利用可能なprobe証拠およびEstimate overheadの検査
トレース: 設計=.agents/skills/right-size-execution/SKILL.md; 実装=.agents/skills/right-size-execution/scripts/executionflow.py; テスト=tests/test_executionflow.py; 参照資料=SWEBOK-V4A

## REQ-EXEC-004: 校正可能な確信度

開発実行基盤は、実行制御へ入力するconfidenceの根拠とscoreを**制約する**。

根拠: 未校正のLLM自己申告値を閾値判定に使わず、観測特徴または実績で校正したrouterだけを使うため。

受入条件:
- `AC-EXEC-004-1` 前提: 校正済みrouterが未導入である。条件: confidenceを記録する。期待結果: deterministic feature evidenceとbandを記録しscoreをnullにする。

要求源: user:2026-07-18, arXiv:2406.18665
検証証跡: 任意の自己申告scoreを拒否するschema・回帰テスト
トレース: 設計=.agents/skills/right-size-execution/references/execution-dimensions.md; 実装=.agents/skills/right-size-execution/assets/execution-profile.schema.json,.agents/skills/right-size-execution/scripts/executionflow.py; テスト=tests/test_executionflow.py; 参照資料=SWEBOK-V4A

## REQ-EXEC-005: 最小十分な検証の導出

開発実行基盤は、scope、assurance、成果物、risk、受入条件および必須gateから成るrequired verificationを**導出する**。

根拠: 機能影響の広さと必要保証の深さを分離しながら、重大な検証漏れを防ぐため。

受入条件:
- `AC-EXEC-005-1` 前提: schema適合profileと受入条件がある。条件: 検証集合を導出する。期待結果: scopeの機能検証、assurance追加検証、受入条件およびrepository必須gateの和集合を生成する。

要求源: user:2026-07-18, SWEBOK-V4A
検証証跡: 四つのscope-assurance交差ケースと不足検証の成功拒否
トレース: 設計=.agents/skills/right-size-execution/references/execution-dimensions.md; 実装=.agents/skills/right-size-execution/scripts/executionflow.py; テスト=tests/test_executionflow.py; 参照資料=SWEBOK-V4A

## REQ-EXEC-006: 根拠付きの単軸Expand

開発実行基盤は、初期profileを覆す新証拠に対応する一つの実行軸を**拡張する**。

根拠: 推定誤りを回復しながら、無関係な軸の同時拡張と一律回数上限による回復阻害を防ぐため。

受入条件:
- `AC-EXEC-006-1` 前提: 許可理由と直接証拠がある。条件: profileを拡張する。期待結果: scope、assurance、verification、review、computeのうち一軸だけを変更し、回数上限ではなくstagnationを検出する。

要求源: user:2026-07-18, arXiv:2607.13034
検証証跡: 三回を超え得る異軸Expandと重複証拠拒否の回帰テスト
トレース: 設計=.agents/skills/right-size-execution/references/expansion-contract.md; 実装=.agents/skills/right-size-execution/scripts/executionflow.py; テスト=tests/test_executionflow.py; 参照資料=SWEBOK-V4A

## REQ-EXEC-007: 成功後の停止

開発実行基盤は、成功条件、required verificationおよびassurance floor充足後の正のコスト活動を**停止する**。

根拠: 成功後の念のための探索や能力引上げを防ぎ、必須確定処理だけを許可するため。

受入条件:
- `AC-EXEC-007-1` 前提: すべてのrequired verificationが成功した。条件: decisive successを記録する。期待結果: 停止digestを作成し、確定処理以外の探索を拒否またはpost-success活動として監査する。

要求源: user:2026-07-18, arXiv:2607.13034
検証証跡: 検証不足の成功拒否と成功後Expand拒否
トレース: 設計=.agents/skills/right-size-execution/references/stopping-contract.md; 実装=.agents/skills/right-size-execution/scripts/executionflow.py; テスト=tests/test_executionflow.py; 参照資料=SWEBOK-V4A

## REQ-EXEC-008: 実行効率の計測

開発実行基盤は、推定、Estimate overhead、実績、Expand、品質および停止後活動の生指標を**計測する**。

根拠: 成功率と重大欠陥を制約にし、oracleなしの単一効率指標へ過適合しないため。

受入条件:
- `AC-EXEC-008-1` 前提: repository作業を実行している。条件: 効率reportを確定する。期待結果: tokenまたはproxy、時間、tool、read、probe、Expand、model、成功、escaped defectおよび停止後活動を保存し、oracleなしでACRRを表明しない。

要求源: user:2026-07-18, arXiv:2607.13034
検証証跡: 生指標、overrun、proxyおよびACRR境界の検査
トレース: 設計=.agents/skills/right-size-execution/references/measurement-contract.md; 実装=.agents/skills/right-size-execution/scripts/executionflow.py; テスト=tests/test_executionflow.py; 参照資料=SWEBOK-V4A

## REQ-EXEC-009: 監査可能なチェック選択

標準検証基盤は、version固定selectorによるチェック候補と選択漏れ監査sampleを**選択する**。

根拠: 未選択とN/Aを分離し、削減件数だけでなく重大controlの偽陰性を監査するため。

受入条件:
- `AC-EXEC-009-1` 前提: execution profileとversion固定catalogがある。条件: チェック候補を選択する。期待結果: assurance、artifact、risk、phase、changed path、always-onから選び、入力、選択digest、除外数、決定的監査sampleおよびmandatory missを保存する。

要求源: user:2026-07-18, SWEBOK-V4A
検証証跡: curated mandatory controlの選択漏れゼロと除外監査sample
トレース: 設計=.agents/skills/right-size-execution/SKILL.md; 実装=tools/devflow.py,governance/checklist/catalog.json,.agents/skills/right-size-execution/scripts/executionflow.py; テスト=tests/test_executionflow.py,tests/test_devflow.py; 参照資料=SWEBOK-V4A

## REQ-EXEC-010: 段階的な適用

実行効率制御は、telemetry、shadow、soft routing、assurance enforcement、calibrationおよび限定blockingの導入順序を**段階適用する**。

根拠: 未校正な効率規則が品質を損なうblocking gateになることを防ぐため。

受入条件:
- `AC-EXEC-010-1` 前提: 実運用の校正データが十分でない。条件: 効率profileを監査する。期待結果: shadow modeで効率違反を警告にし、schema破損とassurance不足だけをblockingにする。

要求源: user:2026-07-18, arXiv:2406.18665
検証証跡: shadow enforcementとassurance floor blockingの回帰テスト
トレース: 設計=.agents/skills/right-size-execution/references/measurement-contract.md; 実装=.agents/skills/right-size-execution/assets/execution-policy.json,.agents/skills/right-size-execution/scripts/executionflow.py; テスト=tests/test_executionflow.py; 参照資料=SWEBOK-V4A

## REQ-FRAME-001: workと正本の境界

リポジトリは、一時的な作業記録と永続的な製品要件を**分離する**。

根拠: work itemは実行文脈であり、暗黙に製品仕様の正本へ変わってはならない。

受入条件:
- `AC-FRAME-001-1` 前提: 統制対象の要求が存在する。条件: 要求を記録する。期待結果: workには要求断片、判断、計画、証跡だけが残り、永続要件は正本へ保存される。

要求源: user:2026-07-17
検証証跡: リポジトリ検証とSkill契約テスト
トレース: 設計=docs/reference/development.md; 実装=.agents/skills/maintain-canonical-requirements/SKILL.md; テスト=tests/test_specflow.py; 参照資料=SWEBOK-V4A

## REQ-PORTABLE-001: チャットだけで移植できる導入

移植可能なSkills集は、別リポジトリへのcopy-and-chat方式の導入を**実現する**。

根拠: 本リポジトリは再利用可能な参照集であり、利用者が内部ツールを手動操作せずに使える必要がある。

受入条件:
- `AC-PORTABLE-001-1` 前提: 対象Skillsフォルダを別リポジトリへコピーしている。条件: 利用者が自然言語で開発要求を相談する。期待結果: 通常のチャットから導入、要件、設計、実装、テスト、公開までを自動実行する。

要求源: user:2026-07-17
検証証跡: プロファイル導入とSkill検出テスト
トレース: 設計=docs/guides/getting-started.md,docs/decisions/ADR-0003-canonical-host-asset-generation.md; 実装=distribution/manifest.json,distribution/host-adapters.json,.agents/skills/chat-first-development/SKILL.md,tools/install_reference.py,tools/generate_host_assets.py,.github/workflows/host-assets.yml; テスト=tests/test_install_reference.py,tests/test_skills.py,tests/test_generate_host_assets.py; 参照資料=SWEBOK-V4A

## REQ-PORTABLE-002: 導入先repository policyの非強制

portable installerと既定profileは、導入先のbranch、merge rule、CI workflowを追加も変更もしないことを**維持する**。

根拠: 3本柱は開発成果物の整合性を扱い、repository運用方針は導入先のauthorityへ委任する。

分類: `product` / `nonfunctional`

受入条件:
- `AC-PORTABLE-002-1` 前提: 独自のbranch ruleとCI workflowを持つ導入先がある。条件: 既定profileを適用する。期待結果: 既存設定がbyte一致し、新しいworkflow、ruleset、merge方式が追加されない。

要求源: user:2026-08-27, https://quint.sh/docs/what-does-quint-do, docs/decisions/ADR-0004-quint-three-pillar-portability.md
検証証跡: 既存.github/workflowsとpolicy fixtureの適用前後byte比較
トレース: 設計=docs/decisions/ADR-0004-quint-three-pillar-portability.md; 実装=distribution/manifest.json,tools/install_reference.py; テスト=tests/test_install_reference.py,tests/test_profile_boundaries.py; 参照資料=QUINT-0.32

## REQ-QUALITY-001: 版管理された出典台帳

品質フレームは、SWEBOKとクラウド・AI公式資料の監査可能な出典台帳を**維持する**。

根拠: 正式名称、版、URL、参照範囲、差分、固定物ハッシュを保存することで、レビュー根拠を再現し更新を検知できる。

受入条件:
- `AC-QUALITY-001-1` 前提: 品質プロファイルを選択している。条件: 出典台帳を検証する。期待結果: 各資料が公式URL、版、参照日、更新間隔、適用範囲、変更確認日、前版との差分を持ち、固定参照物はSHA-256を持つ。
- `AC-QUALITY-001-2` 前提: 添付SWEBOKを参照する。条件: 版の同一性を検証する。期待結果: v4.0aの正式名称、18KA対応、固定SHA-256が台帳と一致する。

要求源: user:2026-07-17, SWEBOK V4, AWS Well-Architected, Azure Well-Architected, Google Cloud Well-Architected, OCI Best Practices
検証証跡: 公式host、鮮度、範囲、差分、ハッシュのテスト
トレース: 設計=docs/standards/SOURCES.md; 実装=.agents/skills/verify-against-engineering-standards/scripts/standardsflow.py,governance/standards/registry.json; テスト=tests/test_standardsflow.py; 参照資料=SWEBOK-V4A,AWS-WAF,AWS-GENAI-LENS,AWS-RAI-LENS,AWS-ML-LENS,AWS-AGENTIC-LENS,AZURE-WAF,AZURE-AI-WAF,GCP-WAF,GCP-AIML-WAF,OCI-WAF

## REQ-QUALITY-002: 変更範囲に対応する品質検査

品質フローは、変更と受入条件に関係する検査だけによる成果物検証を**検証する**。

根拠: 関係する失敗を直接証跡で検出しつつ、無関係な全件検査と専用記録の負担を避ける。

受入条件:
- `AC-QUALITY-002-1` 前提: 変更内容と受入条件が分かっている。条件: 品質検査を実行する。期待結果: 関係する最小のtest、lint、type check、buildまたはgeneratorだけを選び、PassまたはFailと直接証跡を簡潔に示す。
- `AC-QUALITY-002-2` 前提: 対象repositoryに該当する既存CIがない。条件: 選択した検査を実行する。期待結果: ローカルcommandを使い、新しいCI workflow、required check、review YAMLを要求しない。

要求源: user:2026-07-17, user:2026-08-27, SWEBOK V4, cloud vendor official guidance
検証証跡: 選択検査とrepository policy非強制のテスト
トレース: 設計=.agents/skills/inspect-quality-gates/SKILL.md,.agents/skills/inspect-quality-gates/references/gate-rules.md; 実装=.agents/skills/inspect-quality-gates/scripts/inspect.py; テスト=tests/test_skills.py,tests/test_review_contract.py; 参照資料=SWEBOK-V4A,AWS-WAF,AWS-GENAI-LENS,AWS-RAI-LENS,AWS-ML-LENS,AWS-AGENTIC-LENS,AZURE-WAF,AZURE-AI-WAF,GCP-WAF,GCP-AIML-WAF,OCI-WAF

## REQ-QUALITY-003: 原子的なチェック統制

チェックリスト生成フローは、一項目・一統制・一証跡で独立判定できるチェック項目を**維持する**。

根拠: 複数統制を一行へ詰め込むと部分実装を一意にPassまたはFailと判定できない。

受入条件:
- `AC-QUALITY-003-1` 前提: チェック項目を追加または更新する。条件: ワークブックを生成・検証する。期待結果: 独立した合否条件を持つ統制へ分割され、既知の複合項目が再発しない。

要求源: user:2026-07-18, SWEBOK Software Quality
検証証跡: 原子性回帰テストとチェック項目カタログ
トレース: 設計=governance/reviews/README.md; 実装=update_checklist.py,.agents/skills/verify-against-engineering-standards/SKILL.md; テスト=tests/test_checklist.py; 参照資料=SWEBOK-V4A

## REQ-QUALITY-004: 3本柱だけのportable guardrail

portable blocking guardrailは、要件正本、as-built生成、選択checkの3本柱だけを対象にすることを**制約する**。

根拠: 導入時の摩擦とfalse blockerを抑え、repository固有の工程を強制しない。

分類: `product` / `nonfunctional`

受入条件:
- `AC-QUALITY-004-1` 前提: 全Skillの形式契約がある。条件: Quint不変条件を検証する。期待結果: blocking guardrailは3本柱のいずれかに属し、補助Skillはblockingにならない。
- `AC-QUALITY-004-2` 前提: portable contractを検証する。条件: merge ruleとCI requirementの属性を確認する。期待結果: すべてfalseである。

要求源: user:2026-08-27, https://quint.sh/docs/what-does-quint-do, docs/decisions/ADR-0004-quint-three-pillar-portability.md
検証証跡: threePillarsOnlyとrepositoryPolicyIsHostOwnedの検証成功
トレース: 設計=docs/decisions/ADR-0004-quint-three-pillar-portability.md; 実装=spec/skills/skills.qnt,distribution/manifest.json; テスト=tests/test_quintflow.py,tests/test_profile_boundaries.py; 参照資料=QUINT-0.32

## REQ-QUINT-001: Quint要件正本

永続要件は、Quint仕様を唯一の編集対象としJSONを派生物として維持することを**維持する**。

根拠: 型検査と状態不変条件を要件記述の入口へ置き、手書きJSONの構造矛盾を防ぐ。

分類: `project` / `nonfunctional`

受入条件:
- `AC-QUINT-001-1` 前提: 永続要件の意味を変更する。条件: 要件正本を更新する。期待結果: Quint仕様が更新され、typecheck後に同じ内容のJSONが生成される。

要求源: user:2026-08-27, https://quint.sh/docs/what-does-quint-do, docs/decisions/ADR-0004-quint-three-pillar-portability.md
検証証跡: requirements.qntのtypecheck成功とrequirements.jsonのbyte一致
トレース: 設計=docs/decisions/ADR-0004-quint-three-pillar-portability.md; 実装=spec/requirements/requirements.qnt,tools/quintflow.py; テスト=tests/test_quintflow.py,tests/test_specflow.py; 参照資料=QUINT-0.32

## REQ-QUINT-002: 要件表示の二段生成

要件生成器は、Quintから正規化JSONを生成し、そのJSONから人向けMarkdownを生成することを**生成する**。

根拠: 機械検証用表現と人向け表示の責務を分離しつつ、authorityを一本化する。

分類: `product` / `functional`

受入条件:
- `AC-QUINT-002-1` 前提: 同一のQuint要件仕様がある。条件: 生成を二回実行する。期待結果: JSONとMarkdownがそれぞれバイト一致する。
- `AC-QUINT-002-2` 前提: 生成済みJSONを変更する。条件: drift検査を実行する。期待結果: Quint正本との差異として失敗する。

要求源: user:2026-08-27, https://quint.sh/docs/what-does-quint-do, docs/decisions/ADR-0004-quint-three-pillar-portability.md
検証証跡: 一時出力とcommitted JSON・Markdownのbyte比較
トレース: 設計=docs/decisions/ADR-0004-quint-three-pillar-portability.md; 実装=tools/quintflow.py,.agents/skills/maintain-canonical-requirements/scripts/specflow.py; テスト=tests/test_quintflow.py,tests/test_specflow.py; 参照資料=QUINT-0.32

## REQ-QUINT-003: 全Skillの形式契約網羅

Skill形式仕様は、すべてのSkillを一対一のQuint契約へ対応付けることを**形式化する**。

根拠: Skill追加時の形式仕様漏れと、削除後に残るstale契約を機械検出する。

分類: `project` / `nonfunctional`

受入条件:
- `AC-QUINT-003-1` 前提: Skill directoryとQuint契約catalogがある。条件: 形式契約検査を実行する。期待結果: 双方の名前集合が完全一致し、各SKILL.mdから契約へtraceできる。

要求源: user:2026-08-27, https://quint.sh/docs/what-does-quint-do, docs/decisions/ADR-0004-quint-three-pillar-portability.md
検証証跡: skills.qntのtest成功とskill coverage検査
トレース: 設計=docs/decisions/ADR-0004-quint-three-pillar-portability.md; 実装=spec/skills/skills.qnt,tools/quintflow.py; テスト=tests/test_quintflow.py,tests/test_skills.py; 参照資料=QUINT-0.32

## REQ-REPO-001: mainとdevの役割および統合方式

dev-standardのbranch運用は、mainへのsquashとdevへのmerge commitを分離したbranch別統合契約を**強制する**。

根拠: 利用者向けrelease履歴と到達可能なengineering履歴のauthorityを案件ごとのmerge判断に依存させないため。

分類: `project` / `nonfunctional`

受入条件:
- `AC-REPO-001-1` 前提: trial phaseでmainまたはdevをbaseとするPull Requestがある。条件: branch-policy checkを実行する。期待結果: mainはrepositoryのdevまたはhotfixだけをsquashで受け入れ、devはtopic、main、またはhotfix競合を解消したreconcile branchだけをmerge commitで受け入れ、その他の方向を拒否する。
- `AC-REPO-001-2` 前提: mainまたはdevへpushがある。条件: push auditとGitHub rulesetを評価する。期待結果: mainのlinear historyとdevの一回一merge commit更新を監査し、削除またはforce pushを許可しない。
- `AC-REPO-001-3` 前提: branch policyがbootstrap phaseであり、dev、ruleset、required checks、PR移行、operator確認が完了している。条件: trial phaseへ移行する。期待結果: mainへのactivation PRでpolicyと対応するactive review YAMLだけを変更し、全Activation-Checkを一度ずつ記録した後、bootstrap reconciliationで同じpolicyとreviewをdevへ伝播する。
- `AC-REPO-001-4` 前提: 既存devがcurrent mainを祖先に持ち、両tip treeが一致し、まだbranch policyを含まない。条件: 二層branch契約をdev-firstでbootstrap導入する。期待結果: Issue #20を参照する初回bootstrap PRだけをdevへmerge commitで統合し、同じtreeをRelease-Type bootstrapのdevからmainへのsquashで導入できるが、Issueをcloseせず2回の通常releaseへ数えない。

要求源: user:2026-07-24, issue:#20, docs/decisions/ADR-0002-two-layer-branch-history.md
検証証跡: branch方向、merge parent、commit subject、protected branch設定のCI結果
トレース: 設計=docs/decisions/ADR-0002-two-layer-branch-history.md,docs/reference/development.md; 実装=.github/branch-policy.json,.github/workflows/governance.yml,tools/branch_policy.py; テスト=tests/test_branch_policy.py,tests/test_reference_repository_contract.py; 参照資料=—
廃止理由: 導入先へmerge方式やbranch構成を強制しない3本柱境界へ移行したため

## REQ-REPO-002: release後の祖先関係とtreeを回復するreconciliation契約

release operatorとCIは、release前後のancestor関係、tip tree条件、freezeを含むreconciliation transactionを**維持する**。

根拠: squashで記録されない祖先関係を回復し、既出file差分とconflictの再評価を防ぎながら詳細commitを保持するため。

分類: `project` / `nonfunctional`

受入条件:
- `AC-REPO-002-1` 前提: devからmainへ通常releaseをsquash mergeした。条件: release reconciliationを完了する。期待結果: 次のtopic統合前にmainをdevへmergeし、mainがdevの祖先であり両tip treeが一致する。
- `AC-REPO-002-2` 前提: mainへhotfixをsquash mergeしdevに未release変更がある。条件: hotfix reconciliationを完了する。期待結果: conflict-freeならmainをdevへ直接mergeし、mainをdevの祖先にするが両tip treeの一致は要求しない。
- `AC-REPO-002-3` 前提: 通常releaseとreconciliationを2回行う。条件: branch graph回帰testを実行する。期待結果: 前回release済みfile差分が次回release diffへ再出現せず、詳細commitはdevから到達可能なまま残る。
- `AC-REPO-002-4` 前提: hotfix後のmainをdevへ直接mergeするとconflictする。条件: hotfix conflict reconciliationを完了する。期待結果: freeze中のdevからreconcile branchを作り、prior devとcurrent mainをparentに持つ解消mergeをdevへ統合し、outer merge treeとhotfix変更pathを保持してours相当の破棄を拒否する。

要求源: user:2026-07-24, issue:#20, Git FAQ: long-running squash merge, docs/decisions/ADR-0002-two-layer-branch-history.md
検証証跡: 一時Git repositoryのancestor、direct tree、three-dot diff、到達可能commitのassert
トレース: 設計=docs/decisions/ADR-0002-two-layer-branch-history.md,docs/reference/development.md; 実装=.github/branch-policy.json,.github/workflows/governance.yml,tools/branch_policy.py; テスト=tests/test_branch_policy.py; 参照資料=—
廃止理由: repository固有のreconciliation契約を廃止し、GitHub標準設定へ委任したため

## REQ-REPO-003: 試行範囲、非移植性、rollback

dev-standardの二層branch試行は、2回のrelease cycleに限定しportable profileへ既定配布しない二層branch試行を**制約する**。

根拠: 長寿命devは一般解ではなく、追加操作とGitHub上の非原子的なlock制約を受容できるrepositoryだけで評価すべきため。

分類: `project` / `nonfunctional`

受入条件:
- `AC-REPO-003-1` 前提: 二層branch契約のassetを配布profileへ追加しようとする。条件: distribution contractを検査する。期待結果: dev-standard固有のbranch policyとvalidatorをportable profileへ含めず、導入先の既定branch戦略を変更しない。
- `AC-REPO-003-2` 前提: 2回のrelease試行が完了していない、または昇格条件を満たさない。条件: 試行結果を判断する。期待結果: 恒久採用と一般化を行わず、必要時はdevへの新規統合を停止して同期済み状態で凍結する。
- `AC-REPO-003-3` 前提: GitHub Actionsでmainとdevの状態を検査する。条件: authority boundaryを確認する。期待結果: required checkを原子的なcross-branch lockとは表明せず、単一operatorと明示freezeの限界を文書化する。
- `AC-REPO-003-4` 前提: branch policyがbootstrap phaseである。条件: 二層branch試行を開始する。期待結果: activation前に初回bootstrap導入以外のtopic mergeを拒否してbranch graph回帰testと外部GitHub設定を確認し、policyとactive reviewを両branchへ伝播した後の最初の小変更を1回目の管理されたdry runとして扱う。
- `AC-REPO-003-5` 前提: 二層branch試行を停止する。条件: rollback transactionを完了する。期待結果: policyと対応するactive review YAMLだけを変更するrollback hotfixをmainへsquashし、hotfix reconciliationでdevへ伝播した後にbootstrapで新規topic統合と通常releaseを停止する。
- `AC-REPO-003-6` 前提: branch policyまたはreview validatorを変更するPull Requestまたはprotected branch pushがある。条件: Governanceのevidenceまたはbranch-policy jobを実行する。期待結果: 利用可能な場合はPR baseまたはpush before側のvalidatorとdependencyで候補treeを検査し、候補validatorだけの自己緩和を当該判定へ使用しない。
- `AC-REPO-003-7` 前提: Governance workflowを変更するPull Requestがある。条件: CIの自己統制境界を評価する。期待結果: workflow file自体をimmutableまたはtamper-proofとは表明せず、required checkのGitHub Actions由来sourceとworkflow差分を単一operatorが確認する。
- `AC-REPO-003-8` 前提: 既存の二層branch policyを変更するPull Requestまたはprotected branch pushがある。条件: baseまたはbefore側policyと候補policyを比較する。期待結果: 2回の管理された試行中はtrial.phase以外のmachine contract変更を拒否し、契約変更は試行停止後の別判断として扱う。

要求源: user:2026-07-24, issue:#20, docs/decisions/ADR-0002-two-layer-branch-history.md
検証証跡: trial設定、base/before validator選択、workflow自己統制限界、distribution非包含、昇格条件とrollbackの契約テスト
トレース: 設計=docs/decisions/ADR-0002-two-layer-branch-history.md; 実装=.github/branch-policy.json,.github/workflows/governance.yml,distribution/manifest.json,tools/branch_policy.py; テスト=tests/test_reference_repository_contract.py,tests/test_branch_policy.py; 参照資料=—
廃止理由: 二層branch試行を終了し、portable guardrailからrepository policyを除外したため

## REQ-SKILL-001: right-size-executionのSkill境界

right-size-executionは、Estimate、ExecuteおよびExpandを一体化した再利用可能な実行制御契約を**提供する**。

根拠: Skill分割と既存工程責務の複製による選択・同期・contextコストを増やさないため。

受入条件:
- `AC-SKILL-001-1` 前提: Skillを配布する。条件: Skill構造を検査する。期待結果: 単一Skillが入力、出力、境界、判断規則、参照先、完了条件を持ち、要件管理、承認、標準合否、Git操作を複製しない。

要求源: user:2026-07-18, arXiv:2602.12670, OpenAI:skills
検証証跡: Skill構造と責務境界の契約テスト
トレース: 設計=.agents/skills/right-size-execution/SKILL.md; 実装=.agents/skills/right-size-execution/agents/openai.yaml; テスト=tests/test_skills.py; 参照資料=SWEBOK-V4A

## REQ-SKILL-002: Skill制約のtrajectory検証

Skill検証基盤は、SKILL.mdの主要behavior constraintが代表trajectoryで実行された証拠を**検証する**。

根拠: テスト成功だけではSkill内の重要規則が実際に使われたことを保証できないため。

受入条件:
- `AC-SKILL-002-1` 前提: 機械可読なbehavior constraintがある。条件: repository benchmarkを実行する。期待結果: 各constraintのconditionを発火させ、expected behaviorと実行証拠のcoverageを報告する。

要求源: user:2026-07-18, arXiv:2606.20659
検証証跡: behavior constraint coverageと未実行constraint一覧
トレース: 設計=.agents/skills/right-size-execution/assets/behavior-constraints.json; 実装=.agents/skills/right-size-execution/scripts/executionflow.py; テスト=tests/test_executionflow.py; 参照資料=SWEBOK-V4A

## REQ-WORKBOOK-001: 再現可能で有界なワークブック

チェックリスト生成フローは、実データ範囲だけを集計し決定的に再現できるレビュー用ワークブックを**生成する**。

根拠: Excel全行参照は読込時に過大なメモリを消費し、固定集計値は項目追加時に陳腐化する。

受入条件:
- `AC-WORKBOOK-001-1` 前提: チェック項目の行数が変わる。条件: ワークブックを再生成する。期待結果: 集計式が各シートの実データ最終行へ更新され、実数と一致し、全列参照を含まない。

要求源: user:2026-07-18
検証証跡: 数式範囲テスト、項目数照合、代表シートの描画結果
トレース: 設計=docs/README.md; 実装=update_checklist.py; テスト=tests/test_checklist.py; 参照資料=SWEBOK-V4A
