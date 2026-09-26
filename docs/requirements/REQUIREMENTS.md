<!-- tools/quintflow.pyによる自動生成。spec/requirements/requirements.qntを編集すること。 -->
# dev-standard 要件一覧

- スキーマ版: 1
- カタログ版: 19
- Product(JSON): <code>"dev-standard"</code>
- 更新日(JSON): <code>"2026-09-26"</code>
- 正本: `spec/requirements/requirements.qnt`
- 機械可読view: `spec/requirements/requirements.json`

| ID | 版 | 状態 | 種別 | 原子的な義務 | 検証方法 |
|---|---:|---|---|---|---|
| <code>"REQ-ASBUILT-001"</code> | 2 | 有効 | 品質 | 導入先repositoryの設計・静的解析adapterは、同一入力からバイト一致する設計出力を**生成する**（<code>"generate"</code>） | 言語非依存契約テストと導入先adapter検証 |
| <code>"REQ-ASBUILT-002"</code> | 2 | 有効 | 品質 | 導入先repositoryの設計・静的解析adapterは、一つの生成logicを共有するgenerate modeとcheck modeを**提供する**（<code>"provide"</code>） | 言語非依存契約テストと導入先adapter検証 |
| <code>"REQ-ASBUILT-003"</code> | 3 | 有効 | 制約 | 導入先repositoryの設計・静的解析adapterは、宣言された専用出力rootで所有が明示された直接編集禁止の生成設計を**分離する**（<code>"separate"</code>） | 言語非依存契約テストと導入先adapter検証 |
| <code>"REQ-ASBUILT-004"</code> | 4 | 有効 | 機能 | 導入先repositoryの設計・静的解析adapterは、実装と公開interfaceとsampleとデータ操作から得たAPI詳細設計を**導出する**（<code>"derive"</code>） | 言語非依存契約テストと導入先adapter検証 |
| <code>"REQ-ASBUILT-005"</code> | 3 | 有効 | 機能 | 導入先repositoryの設計・静的解析adapterは、endpoint metadataから得た重複のないAPI一覧を**導出する**（<code>"derive"</code>） | 言語非依存契約テストと導入先adapter検証 |
| <code>"REQ-ASBUILT-006"</code> | 4 | 有効 | データ | 導入先repositoryの設計・静的解析adapterは、実行経路の保存先アクセスから得たAPIと保存先のCRUD関係を**導出する**（<code>"derive"</code>） | 言語非依存契約テストと導入先adapter検証 |
| <code>"REQ-ASBUILT-007"</code> | 5 | 有効 | データ | 導入先repositoryの設計・静的解析adapterは、正本のデータ定義と実アクセスから得た保存構造・制約・関連・書込みAPIを**導出する**（<code>"derive"</code>） | 言語非依存契約テストと導入先adapter検証 |
| <code>"REQ-ASBUILT-008"</code> | 4 | 有効 | 機能 | 導入先repositoryの設計・静的解析adapterは、E2E testのGiven When Then構造から得たscenario設計を**導出する**（<code>"derive"</code>） | 言語非依存契約テストと導入先adapter検証 |
| <code>"REQ-ASBUILT-009"</code> | 5 | 有効 | 運用 | 導入先repositoryの設計・静的解析adapterは、対象repositoryが所有する結果JSONから得た参照限定test evidence viewを**導出する**（<code>"derive"</code>） | 言語非依存契約テストと導入先adapter検証 |
| <code>"REQ-ASBUILT-010"</code> | 4 | 有効 | 機能 | 導入先repositoryの設計・静的解析adapterは、tool entrypointの実装と説明から得たCLI仕様とflowを**導出する**（<code>"derive"</code>） | 言語非依存契約テストと導入先adapter検証 |
| <code>"REQ-ASBUILT-011"</code> | 4 | 有効 | データ | 導入先repositoryの設計・静的解析adapterは、API error分岐から得たcatalog全体で一意なID付きmachine-readable error caseを**生成する**（<code>"generate"</code>） | 言語非依存契約テストと導入先adapter検証 |
| <code>"REQ-ASBUILT-012"</code> | 4 | 有効 | 品質 | 導入先repositoryの設計・静的解析adapterは、endpoint登録と設計metadataとerror sampleの三点整合を**検証する**（<code>"verify"</code>） | 言語非依存契約テストと導入先adapter検証 |
| <code>"REQ-ASBUILT-013"</code> | 4 | 有効 | 品質 | 導入先repositoryの設計・静的解析adapterは、設計掲載sampleと実response assertionの対応を**検証する**（<code>"verify"</code>） | 言語非依存契約テストと導入先adapter検証 |
| <code>"REQ-ASBUILT-014"</code> | 4 | 有効 | 品質 | 導入先repositoryの設計・静的解析adapterは、DBまたは外部変更effectを持つAPIとeffect別E2E状態assertの対応を**検証する**（<code>"verify"</code>） | 言語非依存契約テストと導入先adapter検証 |
| <code>"REQ-ASBUILT-015"</code> | 3 | 有効 | 品質 | 導入先repositoryの設計・静的解析adapterは、前提・操作・期待結果と自然言語の説明を持つ独立した検証単位を**構成する**（<code>"structure"</code>） | 言語非依存契約テストと導入先adapter検証 |
| <code>"REQ-ASBUILT-016"</code> | 4 | 有効 | 品質 | 導入先repositoryの設計・静的解析adapterは、C0命令網羅95%以上とC1分岐網羅90%以上のcoverageを**計測する**（<code>"measure"</code>） | 言語非依存契約テストと導入先adapter検証 |
| <code>"REQ-ASBUILT-017"</code> | 2 | 有効 | 制約 | as-built規約は、Rule IDからcatalog check IDへ接続された機械可読check定義を**維持する**（<code>"maintain"</code>） | repository契約テスト |
| <code>"REQ-ASBUILT-018"</code> | 3 | 有効 | 運用 | 導入先repositoryの設計・静的解析adapterは、理由付きRule ID抑制箇所の監査一覧を**生成する**（<code>"generate"</code>） | 言語非依存契約テストと導入先adapter検証 |
| <code>"REQ-ASBUILT-019"</code> | 4 | 有効 | 運用 | inspect-quality-gates runnerは、選択したtest・static analysis・規約check・coverageの結果と未検証範囲を示す一つのlocal summaryまたは対象所有viewを**提供する**（<code>"provide"</code>） | 契約テスト |
| <code>"REQ-ASBUILT-020"</code> | 4 | 有効 | 品質 | 導入先repositoryの設計・静的解析adapterは、宣言したactive requirement集合とartifact・実在test識別子の完全な明示traceを**妥当性確認する**（<code>"validate"</code>） | 言語非依存契約テストと導入先adapter検証 |
| <code>"REQ-ASBUILT-021"</code> | 2 | 有効 | 品質 | 導入先repositoryの設計・静的解析adapterは、必要な実装領域のgenerator接続、Markdown生成、欠落とdrift検査を**検証する**（<code>"verify"</code>） | 言語非依存契約テストと導入先adapter検証 |
| <code>"REQ-DESIGN-007"</code> | 2 | 有効 | 品質 | 導入先repositoryの設計・静的解析adapterは、operationが所有するSQL正本からの型付きquery生成を**検証する**（<code>"verify"</code>） | 言語非依存契約テストと導入先adapter検証 |
| <code>"REQ-DOCS-002"</code> | 2 | 有効 | 品質 | 導入先repositoryの設計・静的解析adapterは、利用者指定に従う説明コメント・処理単位の説明・生成ヘッダーを**検証する**（<code>"verify"</code>） | 言語非依存契約テストと導入先adapter検証 |
| <code>"REQ-DESIGN-001"</code> | 5 | 有効 | 制約 | 導入先repositoryの設計・静的解析adapterは、endpoint層の全体フローと個別処理単位の具体処理に分離したoperationを**構成する**（<code>"structure"</code>） | 言語非依存契約テストと導入先adapter検証 |
| <code>"REQ-DESIGN-002"</code> | 3 | 有効 | 機能 | 導入先repositoryの設計・静的解析adapterは、endpoint起点の実call graphから得たoperationシーケンス図を**導出する**（<code>"derive"</code>） | 言語非依存契約テストと導入先adapter検証 |
| <code>"REQ-DESIGN-003"</code> | 3 | 有効 | インターフェース | 導入先repositoryの設計・静的解析adapterは、実装に接続された公開interface定義からのAPIと入出力一覧を**導出する**（<code>"derive"</code>） | 言語非依存契約テストと導入先adapter検証 |
| <code>"REQ-DESIGN-004"</code> | 3 | 有効 | データ | 導入先repositoryの設計・静的解析adapterは、実行する保存先操作の意味解析から得たqueryとCRUD設計を**解析する**（<code>"parse"</code>） | 言語非依存契約テストと導入先adapter検証 |
| <code>"REQ-DESIGN-005"</code> | 3 | 有効 | 機能 | 導入先repositoryの設計・静的解析adapterは、実デプロイartifactからのresourceとparameter一覧を**導出する**（<code>"derive"</code>） | 言語非依存契約テストと導入先adapter検証 |
| <code>"REQ-DESIGN-006"</code> | 4 | 有効 | 品質 | 導入先repositoryの設計・静的解析adapterは、実装成果物と自動生成された詳細設計の差分を**検出する**（<code>"detect"</code>） | 言語非依存契約テストと導入先adapter検証 |
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
| <code>"REQ-PORTABLE-003"</code> | 2 | 有効 | 制約 | portable Skillとruntimeは、外部または不可逆な操作を利用者が明示した依頼と必要な承認の範囲だけに限定することを**制約する**（<code>"constrain"</code>） | 契約テストとmutation test |
| <code>"REQ-QUALITY-001"</code> | 2 | 有効 | 運用 | 品質フレームは、SWEBOKとクラウド・AI公式資料の監査可能な出典台帳を**維持する**（<code>"maintain"</code>） | 自動検査 |
| <code>"REQ-QUALITY-002"</code> | 5 | 有効 | 品質 | 品質フローは、変更と受入条件に関係する検査だけによる成果物検証を**検証する**（<code>"verify"</code>） | 契約テスト |
| <code>"REQ-QUALITY-003"</code> | 3 | 有効 | 品質 | チェックリスト生成フローは、一項目・一統制・一証跡で独立判定できるチェック項目を**維持する**（<code>"maintain"</code>） | 自動テストと批判的レビュー |
| <code>"REQ-QUALITY-004"</code> | 1 | 有効 | 制約 | portable blocking guardrailは、要件正本、as-built生成、選択checkの3本柱だけを対象にすることを**制約する**（<code>"constrain"</code>） | Quint invariant verification |
| <code>"REQ-QUINT-001"</code> | 3 | 有効 | 制約 | 永続要件は、Quint仕様を唯一の編集対象としJSONを派生物として維持することを**維持する**（<code>"maintain"</code>） | Quint typecheckと生成drift検査 |
| <code>"REQ-QUINT-002"</code> | 3 | 有効 | 機能 | 要件生成器は、Quintから全fieldとList順を保持するJSONを生成し、そのserialized JSONから人向けMarkdownを生成することを**生成する**（<code>"generate"</code>） | 決定的生成とgolden mappingテスト |
| <code>"REQ-QUINT-003"</code> | 3 | 有効 | 品質 | Skill形式仕様は、すべてのSkillを一対一のQuint契約とactive要件の双方向traceへ対応付けることを**形式化する**（<code>"formalize"</code>） | Quint testと双方向集合比較 |
| <code>"REQ-REPO-001"</code> | 3 | 廃止 | 制約 | dev-standardのbranch運用は、mainへのsquashとdevへのmerge commitを分離したbranch別統合契約を**強制する**（<code>"enforce"</code>） | CIとGitHub ruleset監査 |
| <code>"REQ-REPO-002"</code> | 3 | 廃止 | 運用 | release operatorとCIは、release前後のancestor関係、tip tree条件、freezeを含むreconciliation transactionを**維持する**（<code>"maintain"</code>） | branch graph回帰テストとCI |
| <code>"REQ-REPO-003"</code> | 3 | 廃止 | 制約 | dev-standardの二層branch試行は、2回のrelease cycleに限定しportable profileへ既定配布しない二層branch試行を**制約する**（<code>"constrain"</code>） | repository contract testと試行後review |
| <code>"REQ-SKILL-001"</code> | 1 | 有効 | 制約 | right-size-executionは、Estimate、ExecuteおよびExpandを一体化した再利用可能な実行制御契約を**提供する**（<code>"provide"</code>） | 自動検査 |
| <code>"REQ-SKILL-002"</code> | 1 | 有効 | 品質 | Skill検証基盤は、SKILL.mdの主要behavior constraintが代表trajectoryで実行された証拠を**検証する**（<code>"verify"</code>） | 自動benchmark |
| <code>"REQ-WORKBOOK-001"</code> | 2 | 有効 | 運用 | チェックリスト生成フローは、実データ範囲だけを集計し決定的に再現できるレビュー用ワークブックを**生成する**（<code>"generate"</code>） | 自動検査と描画確認 |
| <code>"REQ-ASBUILT-022"</code> | 2 | 有効 | 品質 | 導入先repositoryの設計・静的解析adapterは、全operationに対応する詳細設計・interface・ログmessage・query・sequence・unit-test詳細の6帳票を**生成する**（<code>"generate"</code>） | 言語非依存契約テストと導入先adapter検証 |
| <code>"REQ-EVIDENCE-001"</code> | 1 | 有効 | 品質 | 開発開始フローは、製品要件からframeworkに応じた品質portalと公開準備を初期構築することを**提供する**（<code>"provide"</code>） | 契約・adapter・生成drift検証 |
| <code>"REQ-EVIDENCE-002"</code> | 1 | 有効 | 品質 | 品質report生成処理は、collectorと実行結果に対応する失敗を隠さない共通reportを**生成する**（<code>"generate"</code>） | 契約・adapter・生成drift検証 |
| <code>"REQ-EVIDENCE-003"</code> | 1 | 有効 | 品質 | 品質report公開処理は、同一revision/runの選別済みartifactだけを公開対象にすることを**制約する**（<code>"constrain"</code>） | 契約・adapter・生成drift検証 |
| <code>"REQ-ASBUILT-023"</code> | 2 | 有効 | 制約 | 導入先repositoryのadapterは、6帳票の章・順序・必須節・繰返し節・非該当表現を**検証する**（<code>"verify"</code>） | 言語非依存契約検査と導入先adapterの正例・負例検証 |
| <code>"REQ-ASBUILT-024"</code> | 2 | 有効 | 機能 | 導入先repositoryのadapterは、API×保存先モデルからのCSV・表・図・根拠を**検証する**（<code>"verify"</code>） | 言語非依存契約検査と導入先adapterの正例・負例検証 |
| <code>"REQ-ASBUILT-025"</code> | 1 | 有効 | 制約 | 導入先repositoryのadapterは、group→API→帳票の階層と索引を**検証する**（<code>"verify"</code>） | 言語非依存契約検査と導入先adapterの正例・負例検証 |
| <code>"REQ-ASBUILT-026"</code> | 3 | 有効 | 機能 | 導入先repositoryのadapterは、実call graphの呼出順・条件・例外・transactionを**検証する**（<code>"verify"</code>） | 言語非依存契約検査と導入先adapterの正例・負例検証 |
| <code>"REQ-ASBUILT-027"</code> | 3 | 有効 | 機能 | 導入先repositoryのadapterは、例外型→捕捉/再送出→HTTP status/body→ログID/level/message/運用対応を**検証する**（<code>"verify"</code>） | 言語非依存契約検査と導入先adapterの正例・負例検証 |
| <code>"REQ-ASBUILT-028"</code> | 3 | 有効 | 機能 | 導入先repositoryのadapterは、実在testへ対応する具体的Given/When/Thenを**検証する**（<code>"verify"</code>） | 言語非依存契約検査と導入先adapterの正例・負例検証 |
| <code>"REQ-ASBUILT-029"</code> | 2 | 有効 | 制約 | 導入先repositoryのadapterは、capabilityごとの生成command・check command・出力root・要件ID・棚卸しリンクを**検証する**（<code>"verify"</code>） | 言語非依存契約検査と導入先adapterの正例・負例検証 |
| <code>"REQ-ASBUILT-030"</code> | 2 | 有効 | 制約 | 導入先repositoryのadapterは、固定revisionの全file用途と採用判断および実接続先を**検証する**（<code>"verify"</code>） | 言語非依存契約検査と導入先adapterの正例・負例検証 |
| <code>"REQ-ASBUILT-031"</code> | 2 | 有効 | 制約 | 導入先repositoryのadapterは、構成適合・設計drift・実行test・未検証範囲の独立した報告を**検証する**（<code>"verify"</code>） | 言語非依存契約検査と導入先adapterの正例・負例検証 |
| <code>"REQ-ASBUILT-032"</code> | 2 | 有効 | 制約 | 導入先repositoryのadapterは、path・理由・support statusを持つ未対応surfaceを**検証する**（<code>"verify"</code>） | 言語非依存契約検査と導入先adapterの正例・負例検証 |
| <code>"REQ-ASBUILT-033"</code> | 1 | 有効 | 機能 | 導入先repositoryのadapterは、内部捕捉後に正常HTTP statusの失敗結果へ変換する実経路を**検証する**（<code>"verify"</code>） | 言語非依存契約検査と導入先adapterの正例・負例検証 |
| <code>"REQ-ASBUILT-034"</code> | 2 | 有効 | 制約 | 導入先repositoryのadapterは、一意な全file集合と要件へのtoolまたは明示gap対応を**検証する**（<code>"verify"</code>） | 言語非依存契約検査と導入先adapterの正例・負例検証 |
| <code>"REQ-ASBUILT-035"</code> | 2 | 有効 | 制約 | 導入先repositoryのadapterは、generatorが完全所有するrootと明示出力集合を**検証する**（<code>"verify"</code>） | 言語非依存契約検査と導入先adapterの正例・負例検証 |
| <code>"REQ-DESIGN-008"</code> | 1 | 有効 | 制約 | 導入先repositoryのadapterは、1 operation 1 所有単位を**検証する**（<code>"verify"</code>） | 言語非依存契約検査と導入先adapterの正例・負例検証 |
| <code>"REQ-DESIGN-009"</code> | 3 | 有効 | 制約 | 導入先repositoryのadapterは、endpoint・個別処理・query・応答組立・schema・contract・sampleの実参照を**検証する**（<code>"verify"</code>） | 言語非依存契約検査と導入先adapterの正例・負例検証 |
| <code>"REQ-DESIGN-010"</code> | 1 | 有効 | 制約 | 導入先repositoryのadapterは、明示された共有責務の所有者と依存方向を**検証する**（<code>"verify"</code>） | 言語非依存契約検査と導入先adapterの正例・負例検証 |
| <code>"REQ-DESIGN-011"</code> | 2 | 有効 | 制約 | 導入先repositoryのadapterは、endpoint層が所有する順序・分岐・反復・例外・transactionを**検証する**（<code>"verify"</code>） | 言語非依存契約検査と導入先adapterの正例・負例検証 |
| <code>"REQ-DESIGN-012"</code> | 1 | 有効 | 制約 | 導入先repositoryのadapterは、各SQLの束縛引数だけを表す専用型を**検証する**（<code>"verify"</code>） | 言語非依存契約検査と導入先adapterの正例・負例検証 |
| <code>"REQ-DESIGN-013"</code> | 1 | 有効 | 制約 | 導入先repositoryのadapterは、ログcatalogと型付きcontextの許容fieldを**検証する**（<code>"verify"</code>） | 言語非依存契約検査と導入先adapterの正例・負例検証 |
| <code>"REQ-DESIGN-014"</code> | 2 | 有効 | 制約 | 導入先repositoryのadapterは、endpoint層に置けるsymbol集合と全source走査を**検証する**（<code>"verify"</code>） | 言語非依存契約検査と導入先adapterの正例・負例検証 |
| <code>"REQ-DESIGN-015"</code> | 2 | 有効 | 制約 | 導入先repositoryのadapterは、operation所有単位間の依存境界を**検証する**（<code>"verify"</code>） | 言語非依存契約検査と導入先adapterの正例・負例検証 |
| <code>"REQ-DESIGN-016"</code> | 1 | 有効 | 制約 | 導入先repositoryのadapterは、owner付きSQLとquery生成先を**検証する**（<code>"verify"</code>） | 言語非依存契約検査と導入先adapterの正例・負例検証 |
| <code>"REQ-DESIGN-017"</code> | 2 | 有効 | 制約 | 導入先repositoryのadapterは、各SQLの実投影とNULLに一致した専用結果型を**検証する**（<code>"verify"</code>） | 言語非依存契約検査と導入先adapterの正例・負例検証 |
| <code>"REQ-DESIGN-018"</code> | 1 | 有効 | 制約 | 導入先repositoryのadapterは、同期・非同期呼出しの意味ある戻り値を**検証する**（<code>"verify"</code>） | 要件と棚卸し対応の検査および導入先adapterの受入検査 |
| <code>"REQ-DESIGN-019"</code> | 1 | 有効 | 制約 | 導入先repositoryのadapterは、判定処理の入力と実処理に対応する真偽結果を**検証する**（<code>"verify"</code>） | 要件と棚卸し対応の検査および導入先adapterの受入検査 |
| <code>"REQ-DESIGN-020"</code> | 1 | 有効 | 制約 | 導入先repositoryのadapterは、API業務フローの捕捉対象を**検証する**（<code>"verify"</code>） | 要件と棚卸し対応の検査および導入先adapterの受入検査 |
| <code>"REQ-DESIGN-021"</code> | 1 | 有効 | 制約 | 導入先repositoryのadapterは、個別業務処理から送出する例外を**検証する**（<code>"verify"</code>） | 要件と棚卸し対応の検査および導入先adapterの受入検査 |
| <code>"REQ-DESIGN-022"</code> | 1 | 有効 | 制約 | 導入先repositoryのadapterは、選択profileに含まれる処理単位の責務説明を**検証する**（<code>"verify"</code>） | 要件と棚卸し対応の検査および導入先adapterの受入検査 |
| <code>"REQ-DESIGN-023"</code> | 1 | 有効 | 制約 | 導入先repositoryのadapterは、個別処理とendpoint・共有workflowの依存方向を**検証する**（<code>"verify"</code>） | 要件と棚卸し対応の検査および導入先adapterの受入検査 |
| <code>"REQ-DESIGN-024"</code> | 2 | 有効 | 制約 | 導入先repositoryのadapterは、固定参照と導入先の構成profile対応を**検証する**（<code>"verify"</code>） | 要件と棚卸し対応の検査および導入先adapterの受入検査 |
| <code>"REQ-ASBUILT-036"</code> | 1 | 有効 | 品質 | 導入先repositoryの設計adapterと共通契約検査器は、固定参照の個別受入条件と現在sourceに対応する正例・負例の結果を**検証する**（<code>"verify"</code>） | 共通契約の正負例と導入先の意味検査実行 |
| <code>"REQ-DESIGN-025"</code> | 1 | 有効 | 制約 | 導入先repositoryのadapterは、責務配置変更の前後で維持する観測可能な契約を**検証する**（<code>"verify"</code>） | 要件と棚卸し対応の検査および導入先adapterの受入検査 |
| <code>"REQ-EVIDENCE-004"</code> | 2 | 有効 | 機能 | 導入先の品質portal adapterは、group→API→帳票の親子関係と現在位置を**検証する**（<code>"verify"</code>） | 言語非依存契約検査と導入先adapterの正例・負例検証 |

## REQ-ASBUILT-001: as-built生成の決定論性

要件ID(JSON): <code>"REQ-ASBUILT-001"</code>
タイトル(JSON): <code>"as-built生成の決定論性"</code>
主体(JSON): <code>"導入先repositoryの設計・静的解析adapter"</code>
対象(JSON): <code>"同一入力からバイト一致する設計出力"</code>
導入先repositoryの設計・静的解析adapterは、同一入力からバイト一致する設計出力を**生成する**。
行為enum: <code>"generate"</code>

根拠: 差分によるdrift検知には非決定要素を除いた再現可能な出力が必要である。
根拠(JSON): <code>"差分によるdrift検知には非決定要素を除いた再現可能な出力が必要である。"</code>

項目版: 2 / 状態: `active` / 種別: `quality`
変更識別子: <code>"CHG-20260923-language-agnostic-adapters"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-ASBUILT-001-1"</code> 前提: 同一revisionの宣言済み一次情報がある。条件: generatorを複数回実行する。期待結果: 列挙順が固定され、時刻・乱数・環境依存pathを含まないバイト一致出力になる。
  - criterion(JSON Object): <code>{"given":"同一revisionの宣言済み一次情報がある","id":"AC-ASBUILT-001-1","then":"列挙順が固定され、時刻・乱数・環境依存pathを含まないバイト一致出力になる","when":"generatorを複数回実行する"}</code>

要求源(JSON List): <code>["user:2026-07-21","docs/standards/AS-BUILT-DESIGN.md","user:2026-09-23-language-agnostic-adapters"]</code>
検証方法: 言語非依存契約テストと導入先adapter検証
検証証跡: manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する
検証(JSON Object): <code>{"evidence":"manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する","method":"言語非依存契約テストと導入先adapter検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/AS-BUILT-DESIGN.md",".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>["governance/checks/catalog.yaml",".agents/skills/generate-implementation-design/scripts/check_design.py"]</code>
- テスト: <code>["tests/test_review_contract.py","tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-002: generateとcheckの二相契約

要件ID(JSON): <code>"REQ-ASBUILT-002"</code>
タイトル(JSON): <code>"generateとcheckの二相契約"</code>
主体(JSON): <code>"導入先repositoryの設計・静的解析adapter"</code>
対象(JSON): <code>"一つの生成logicを共有するgenerate modeとcheck mode"</code>
導入先repositoryの設計・静的解析adapterは、一つの生成logicを共有するgenerate modeとcheck modeを**提供する**。
行為enum: <code>"provide"</code>

根拠: 生成と検査を別実装にすると両者の意味が乖離する。
根拠(JSON): <code>"生成と検査を別実装にすると両者の意味が乖離する。"</code>

項目版: 2 / 状態: `active` / 種別: `quality`
変更識別子: <code>"CHG-20260923-language-agnostic-adapters"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-ASBUILT-002-1"</code> 前提: 宣言済み生成対象と既存生成物がある。条件: check modeを実行する。期待結果: 生成logicを再利用して既存生成物と比較し、差分pathを列挙して非0終了する。
  - criterion(JSON Object): <code>{"given":"宣言済み生成対象と既存生成物がある","id":"AC-ASBUILT-002-1","then":"生成logicを再利用して既存生成物と比較し、差分pathを列挙して非0終了する","when":"check modeを実行する"}</code>

要求源(JSON List): <code>["user:2026-07-21","docs/standards/AS-BUILT-DESIGN.md","user:2026-09-23-language-agnostic-adapters"]</code>
検証方法: 言語非依存契約テストと導入先adapter検証
検証証跡: manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する
検証(JSON Object): <code>{"evidence":"manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する","method":"言語非依存契約テストと導入先adapter検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/AS-BUILT-DESIGN.md",".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>["governance/checks/catalog.yaml",".agents/skills/generate-implementation-design/scripts/check_design.py"]</code>
- テスト: <code>["tests/test_review_contract.py","tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-003: 生成設計の隔離と識別

要件ID(JSON): <code>"REQ-ASBUILT-003"</code>
タイトル(JSON): <code>"生成設計の隔離と識別"</code>
主体(JSON): <code>"導入先repositoryの設計・静的解析adapter"</code>
対象(JSON): <code>"宣言された専用出力rootで所有が明示された直接編集禁止の生成設計"</code>
導入先repositoryの設計・静的解析adapterは、宣言された専用出力rootで所有が明示された直接編集禁止の生成設計を**分離する**。
行為enum: <code>"separate"</code>

根拠: 専用path、命名、更新commandにより手書き設計との混在と直接編集を防げる。
根拠(JSON): <code>"専用path、命名、更新commandにより手書き設計との混在と直接編集を防げる。"</code>

項目版: 3 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"CHG-20260926-lazunex-conformance"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-ASBUILT-003-1"</code> 前提: Markdown形式のas-built設計を生成する。条件: 生成物の配置と識別を検査する。期待結果: manifestが宣言する専用rootと出力集合に限り、生成元と更新commandを識別できる直接編集禁止表示を持つ。同じ現在状態の手書き設計を正本化しない。
  - criterion(JSON Object): <code>{"given":"Markdown形式のas-built設計を生成する","id":"AC-ASBUILT-003-1","then":"manifestが宣言する専用rootと出力集合に限り、生成元と更新commandを識別できる直接編集禁止表示を持つ。同じ現在状態の手書き設計を正本化しない","when":"生成物の配置と識別を検査する"}</code>
- <code>"AC-ASBUILT-003-2"</code> 前提: 固定版の参照実装と導入先の実sourceがある。条件: 生成帳票を公開または閲覧する。期待結果: 自動生成である表示、生成元と再生成command、直接編集禁止を各帳票に残す。手書きの背景・判断と現在実装の自動生成事実を区別し、raw JSONへのリンクだけを人向け設計の代わりにしない。。
  - criterion(JSON Object): <code>{"given":"固定版の参照実装と導入先の実sourceがある","id":"AC-ASBUILT-003-2","then":"自動生成である表示、生成元と再生成command、直接編集禁止を各帳票に残す。手書きの背景・判断と現在実装の自動生成事実を区別し、raw JSONへのリンクだけを人向け設計の代わりにしない。","when":"生成帳票を公開または閲覧する"}</code>

要求源(JSON List): <code>["user:2026-07-21","docs/standards/AS-BUILT-DESIGN.md","user:2026-09-23-language-agnostic-adapters","user:2026-09-26-lazunex-authoritative"]</code>
検証方法: 言語非依存契約テストと導入先adapter検証
検証証跡: manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する
検証(JSON Object): <code>{"evidence":"manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する","method":"言語非依存契約テストと導入先adapter検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/AS-BUILT-DESIGN.md",".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/SKILL.md","governance/checks/catalog.yaml",".agents/skills/generate-implementation-design/scripts/check_design.py"]</code>
- テスト: <code>["tests/test_review_contract.py","tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-004: API詳細設計の導出

要件ID(JSON): <code>"REQ-ASBUILT-004"</code>
タイトル(JSON): <code>"API詳細設計の導出"</code>
主体(JSON): <code>"導入先repositoryの設計・静的解析adapter"</code>
対象(JSON): <code>"実装と公開interfaceとsampleとデータ操作から得たAPI詳細設計"</code>
導入先repositoryの設計・静的解析adapterは、実装と公開interfaceとsampleとデータ操作から得たAPI詳細設計を**導出する**。
行為enum: <code>"derive"</code>

根拠: APIのinterfaceと実行flowを同じ一次情報から導出すると実装との1対1対応を維持できる。
根拠(JSON): <code>"APIのinterfaceと実行flowを同じ一次情報から導出すると実装との1対1対応を維持できる。"</code>

項目版: 4 / 状態: `active` / 種別: `functional`
変更識別子: <code>"CHG-20260926-lazunex-conformance"</code>
分類: scope=<code>"project"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-ASBUILT-004-1"</code> 前提: 実装と公開interface定義がある。条件: 導入先adapterがAPI詳細設計を生成する。期待結果: endpoint起点のinterface、処理step、全branchを保つ制御flow、error分岐、message、unit-test観点を実装から導出する。
  - criterion(JSON Object): <code>{"given":"実装と公開interface定義がある","id":"AC-ASBUILT-004-1","then":"endpoint起点のinterface、処理step、全branchを保つ制御flow、error分岐、message、unit-test観点を実装から導出する","when":"導入先adapterがAPI詳細設計を生成する"}</code>
- <code>"AC-ASBUILT-004-2"</code> 前提: 固定版の参照実装と導入先の実sourceがある。条件: 6帳票の意味内容を検査する。期待結果: 正常入力のHeader/Path/Query/Bodyを同時に保持し、前提条件、DB・外部資源の項目ごとの変更値と取得元、応答項目と取得元を表示する。requestBodyとparametersの片方の選択、SQL名だけの変更説明、response schemaだけの取得元説明を拒否する。。
  - criterion(JSON Object): <code>{"given":"固定版の参照実装と導入先の実sourceがある","id":"AC-ASBUILT-004-2","then":"正常入力のHeader/Path/Query/Bodyを同時に保持し、前提条件、DB・外部資源の項目ごとの変更値と取得元、応答項目と取得元を表示する。requestBodyとparametersの片方の選択、SQL名だけの変更説明、response schemaだけの取得元説明を拒否する。","when":"6帳票の意味内容を検査する"}</code>

要求源(JSON List): <code>["user:2026-07-21","docs/standards/AS-BUILT-DESIGN.md","user:2026-09-23-language-agnostic-adapters","user:2026-09-26-lazunex-authoritative"]</code>
検証方法: 言語非依存契約テストと導入先adapter検証
検証証跡: manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する
検証(JSON Object): <code>{"evidence":"manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する","method":"言語非依存契約テストと導入先adapter検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/AS-BUILT-DESIGN.md",".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/SKILL.md","governance/checks/catalog.yaml",".agents/skills/generate-implementation-design/scripts/check_design.py"]</code>
- テスト: <code>["tests/test_review_contract.py","tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-005: API一覧の導出

要件ID(JSON): <code>"REQ-ASBUILT-005"</code>
タイトル(JSON): <code>"API一覧の導出"</code>
主体(JSON): <code>"導入先repositoryの設計・静的解析adapter"</code>
対象(JSON): <code>"endpoint metadataから得た重複のないAPI一覧"</code>
導入先repositoryの設計・静的解析adapterは、endpoint metadataから得た重複のないAPI一覧を**導出する**。
行為enum: <code>"derive"</code>

根拠: route metadataを正本にすると別管理のAPI台帳を不要にできる。
根拠(JSON): <code>"route metadataを正本にすると別管理のAPI台帳を不要にできる。"</code>

項目版: 3 / 状態: `active` / 種別: `functional`
変更識別子: <code>"CHG-20260926-lazunex-conformance"</code>
分類: scope=<code>"project"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-ASBUILT-005-1"</code> 前提: endpoint定義に設計metadataがある。条件: API一覧を生成する。期待結果: operation、API番号、権限、業務概要を重複なく列挙する。
  - criterion(JSON Object): <code>{"given":"endpoint定義に設計metadataがある","id":"AC-ASBUILT-005-1","then":"operation、API番号、権限、業務概要を重複なく列挙する","when":"API一覧を生成する"}</code>
- <code>"AC-ASBUILT-005-2"</code> 前提: 固定版の参照実装と導入先の実sourceがある。条件: API一覧を人向けに表示する。期待結果: method/path/operation ID/業務概要/権限と各API索引を対応付ける。sourceのsummaryやdescriptionの欠落を固定のAPI名から捏造せず、欠落または非該当を明示する。。
  - criterion(JSON Object): <code>{"given":"固定版の参照実装と導入先の実sourceがある","id":"AC-ASBUILT-005-2","then":"method/path/operation ID/業務概要/権限と各API索引を対応付ける。sourceのsummaryやdescriptionの欠落を固定のAPI名から捏造せず、欠落または非該当を明示する。","when":"API一覧を人向けに表示する"}</code>

要求源(JSON List): <code>["user:2026-07-21","docs/standards/AS-BUILT-DESIGN.md","user:2026-09-23-language-agnostic-adapters","user:2026-09-26-lazunex-authoritative"]</code>
検証方法: 言語非依存契約テストと導入先adapter検証
検証証跡: manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する
検証(JSON Object): <code>{"evidence":"manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する","method":"言語非依存契約テストと導入先adapter検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/AS-BUILT-DESIGN.md",".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/SKILL.md","governance/checks/catalog.yaml",".agents/skills/generate-implementation-design/scripts/check_design.py"]</code>
- テスト: <code>["tests/test_review_contract.py","tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-006: CRUD関係の導出

要件ID(JSON): <code>"REQ-ASBUILT-006"</code>
タイトル(JSON): <code>"CRUD関係の導出"</code>
主体(JSON): <code>"導入先repositoryの設計・静的解析adapter"</code>
対象(JSON): <code>"実行経路の保存先アクセスから得たAPIと保存先のCRUD関係"</code>
導入先repositoryの設計・静的解析adapterは、実行経路の保存先アクセスから得たAPIと保存先のCRUD関係を**導出する**。
行為enum: <code>"derive"</code>

根拠: 静的解析されたデータ操作をAPIへ接続するとCRUD図を手書きせず維持できる。
根拠(JSON): <code>"静的解析されたデータ操作をAPIへ接続するとCRUD図を手書きせず維持できる。"</code>

項目版: 4 / 状態: `active` / 種別: `data`
変更識別子: <code>"CHG-20260923-independent-review-fixes"</code>
分類: scope=<code>"project"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-ASBUILT-006-1"</code> 前提: APIから保存先アクセスへの実接続がある。条件: 導入先adapterがCRUDモデルを生成する。期待結果: create/read/update/deleteと参照先・変更先を区別し、SQL以外の保存先も対象にする。動的呼出しや未解析操作をアクセスなしへ推定せず、根拠付き未解決として返す。
  - criterion(JSON Object): <code>{"given":"APIから保存先アクセスへの実接続がある","id":"AC-ASBUILT-006-1","then":"create/read/update/deleteと参照先・変更先を区別し、SQL以外の保存先も対象にする。動的呼出しや未解析操作をアクセスなしへ推定せず、根拠付き未解決として返す","when":"導入先adapterがCRUDモデルを生成する"}</code>
- <code>"AC-ASBUILT-006-2"</code> 前提: 該当する実装と選択profileがある。条件: 導入先adapterの正例と負例を検証する。期待結果: 導入先adapterはJOIN等の参照先RとINSERT/UPDATE/DELETE等の変更先C/U/Dを区別する。API追加・保存先操作変更・削除の正例と負例でCRUD集合の更新を検証し、構築時操作をAPI実行時アクセスへ混入させない。
  - criterion(JSON Object): <code>{"given":"該当する実装と選択profileがある","id":"AC-ASBUILT-006-2","then":"導入先adapterはJOIN等の参照先RとINSERT/UPDATE/DELETE等の変更先C/U/Dを区別する。API追加・保存先操作変更・削除の正例と負例でCRUD集合の更新を検証し、構築時操作をAPI実行時アクセスへ混入させない","when":"導入先adapterの正例と負例を検証する"}</code>

要求源(JSON List): <code>["user:2026-07-21","docs/standards/AS-BUILT-DESIGN.md","user:2026-09-23-language-agnostic-adapters"]</code>
検証方法: 言語非依存契約テストと導入先adapter検証
検証証跡: manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する
検証(JSON Object): <code>{"evidence":"manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する","method":"言語非依存契約テストと導入先adapter検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/AS-BUILT-DESIGN.md",".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/SKILL.md","governance/checks/catalog.yaml",".agents/skills/generate-implementation-design/scripts/check_design.py"]</code>
- テスト: <code>["tests/test_review_contract.py","tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-007: DB設計の導出

要件ID(JSON): <code>"REQ-ASBUILT-007"</code>
タイトル(JSON): <code>"DB設計の導出"</code>
主体(JSON): <code>"導入先repositoryの設計・静的解析adapter"</code>
対象(JSON): <code>"正本のデータ定義と実アクセスから得た保存構造・制約・関連・書込みAPI"</code>
導入先repositoryの設計・静的解析adapterは、正本のデータ定義と実アクセスから得た保存構造・制約・関連・書込みAPIを**導出する**。
行為enum: <code>"derive"</code>

根拠: DDLとSQLを一次情報にするとDB設計の二重管理を避けられる。
根拠(JSON): <code>"DDLとSQLを一次情報にするとDB設計の二重管理を避けられる。"</code>

項目版: 5 / 状態: `active` / 種別: `data`
変更識別子: <code>"CHG-20260926-lazunex-conformance"</code>
分類: scope=<code>"project"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-ASBUILT-007-1"</code> 前提: 保存構造の正本とAPIのアクセス実装がある。条件: 導入先adapterがデータ設計を生成する。期待結果: 保存先、項目、制約、項目単位の関連元・関連先と書込みAPIを正本から導出する。未解析の関連を推測で補わない。
  - criterion(JSON Object): <code>{"given":"保存構造の正本とAPIのアクセス実装がある","id":"AC-ASBUILT-007-1","then":"保存先、項目、制約、項目単位の関連元・関連先と書込みAPIを正本から導出する。未解析の関連を推測で補わない","when":"導入先adapterがデータ設計を生成する"}</code>
- <code>"AC-ASBUILT-007-2"</code> 前提: 固定版の参照実装と導入先の実sourceがある。条件: テーブル仕様とERを生成する。期待結果: 項目の和名・物理名・型・NULL・PK/unique/default/indexと関連を導出し、物理FKと理由付き論理関連を区別する。カードやDDL全文だけを関連線のあるER図の代わりにせず、存在しないFKを推測しない。。
  - criterion(JSON Object): <code>{"given":"固定版の参照実装と導入先の実sourceがある","id":"AC-ASBUILT-007-2","then":"項目の和名・物理名・型・NULL・PK/unique/default/indexと関連を導出し、物理FKと理由付き論理関連を区別する。カードやDDL全文だけを関連線のあるER図の代わりにせず、存在しないFKを推測しない。","when":"テーブル仕様とERを生成する"}</code>

要求源(JSON List): <code>["user:2026-07-21","docs/standards/AS-BUILT-DESIGN.md","user:2026-09-23-language-agnostic-adapters","user:2026-09-26-lazunex-authoritative"]</code>
検証方法: 言語非依存契約テストと導入先adapter検証
検証証跡: manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する
検証(JSON Object): <code>{"evidence":"manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する","method":"言語非依存契約テストと導入先adapter検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/AS-BUILT-DESIGN.md",".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>["governance/checks/catalog.yaml",".agents/skills/generate-implementation-design/scripts/check_design.py"]</code>
- テスト: <code>["tests/test_review_contract.py","tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-008: E2E scenario設計の導出

要件ID(JSON): <code>"REQ-ASBUILT-008"</code>
タイトル(JSON): <code>"E2E scenario設計の導出"</code>
主体(JSON): <code>"導入先repositoryの設計・静的解析adapter"</code>
対象(JSON): <code>"E2E testのGiven When Then構造から得たscenario設計"</code>
導入先repositoryの設計・静的解析adapterは、E2E testのGiven When Then構造から得たscenario設計を**導出する**。
行為enum: <code>"derive"</code>

根拠: test codeをscenarioの正本にすると実行可能な仕様と設計表示を一致させられる。
根拠(JSON): <code>"test codeをscenarioの正本にすると実行可能な仕様と設計表示を一致させられる。"</code>

項目版: 4 / 状態: `active` / 種別: `functional`
変更識別子: <code>"CHG-20260926-lazunex-conformance"</code>
分類: scope=<code>"project"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-ASBUILT-008-1"</code> 前提: E2E testにGiven、When、Then sectionがある。条件: scenario設計を生成する。期待結果: 前提、操作、期待状態をtest codeから順序どおり生成する。
  - criterion(JSON Object): <code>{"given":"E2E testにGiven、When、Then sectionがある","id":"AC-ASBUILT-008-1","then":"前提、操作、期待状態をtest codeから順序どおり生成する","when":"scenario設計を生成する"}</code>
- <code>"AC-ASBUILT-008-2"</code> 前提: 固定版の参照実装と導入先の実sourceがある。条件: E2Eの設計を生成する。期待結果: 実test codeの順序付きstep、前提、操作、HTTP/画面/DB/外部の期待状態とcase IDを対応付ける。テストタイトルやタグの一覧だけをstep設計の代わりにしない。。
  - criterion(JSON Object): <code>{"given":"固定版の参照実装と導入先の実sourceがある","id":"AC-ASBUILT-008-2","then":"実test codeの順序付きstep、前提、操作、HTTP/画面/DB/外部の期待状態とcase IDを対応付ける。テストタイトルやタグの一覧だけをstep設計の代わりにしない。","when":"E2Eの設計を生成する"}</code>

要求源(JSON List): <code>["user:2026-07-21","docs/standards/AS-BUILT-DESIGN.md","user:2026-09-23-language-agnostic-adapters","user:2026-09-26-lazunex-authoritative"]</code>
検証方法: 言語非依存契約テストと導入先adapter検証
検証証跡: manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する
検証(JSON Object): <code>{"evidence":"manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する","method":"言語非依存契約テストと導入先adapter検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/AS-BUILT-DESIGN.md",".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>["governance/checks/catalog.yaml",".agents/skills/generate-implementation-design/scripts/check_design.py"]</code>
- テスト: <code>["tests/test_review_contract.py","tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-009: test evidence viewの対象所有集約

要件ID(JSON): <code>"REQ-ASBUILT-009"</code>
タイトル(JSON): <code>"test evidence viewの対象所有集約"</code>
主体(JSON): <code>"導入先repositoryの設計・静的解析adapter"</code>
対象(JSON): <code>"対象repositoryが所有する結果JSONから得た参照限定test evidence view"</code>
導入先repositoryの設計・静的解析adapterは、対象repositoryが所有する結果JSONから得た参照限定test evidence viewを**導出する**。
行為enum: <code>"derive"</code>

根拠: 結果本文を複製せず、localまたは導入先が既に所有し選択したviewだけを使えばportable runtimeへ外部report基盤を強制しない。
根拠(JSON): <code>"結果本文を複製せず、localまたは導入先が既に所有し選択したviewだけを使えばportable runtimeへ外部report基盤を強制しない。"</code>

項目版: 5 / 状態: `active` / 種別: `operational`
変更識別子: <code>"CHG-20260923-language-agnostic-adapters"</code>
分類: scope=<code>"product"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-ASBUILT-009-1"</code> 前提: 対象repositoryが所有するtest結果JSONがある。条件: test evidence viewを生成する。期待結果: status、API response、DB結果、mock受信結果への参照だけを整形し、結果本文を保存せず、新しい外部report基盤を要求しない。
  - criterion(JSON Object): <code>{"given":"対象repositoryが所有するtest結果JSONがある","id":"AC-ASBUILT-009-1","then":"status、API response、DB結果、mock受信結果への参照だけを整形し、結果本文を保存せず、新しい外部report基盤を要求しない","when":"test evidence viewを生成する"}</code>

要求源(JSON List): <code>["user:2026-07-21","user:2026-08-27","docs/standards/AS-BUILT-DESIGN.md","user:2026-09-23-language-agnostic-adapters"]</code>
検証方法: 言語非依存契約テストと導入先adapter検証
検証証跡: manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する
検証(JSON Object): <code>{"evidence":"manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する","method":"言語非依存契約テストと導入先adapter検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/AS-BUILT-DESIGN.md",".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>["governance/checks/catalog.yaml",".agents/skills/generate-implementation-design/scripts/check_design.py"]</code>
- テスト: <code>["tests/test_review_contract.py","tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-010: generator tool設計の導出

要件ID(JSON): <code>"REQ-ASBUILT-010"</code>
タイトル(JSON): <code>"generator tool設計の導出"</code>
主体(JSON): <code>"導入先repositoryの設計・静的解析adapter"</code>
対象(JSON): <code>"tool entrypointの実装と説明から得たCLI仕様とflow"</code>
導入先repositoryの設計・静的解析adapterは、tool entrypointの実装と説明から得たCLI仕様とflowを**導出する**。
行為enum: <code>"derive"</code>

根拠: generator自身を同じ方式で可視化すると抽出可能性をdogfoodingできる。
根拠(JSON): <code>"generator自身を同じ方式で可視化すると抽出可能性をdogfoodingできる。"</code>

項目版: 4 / 状態: `active` / 種別: `functional`
変更識別子: <code>"CHG-20260926-lazunex-conformance"</code>
分類: scope=<code>"project"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-ASBUILT-010-1"</code> 前提: tool entrypointと呼出先関数に処理単位の説明がある。条件: tool設計を生成する。期待結果: CLI argument、制御flow、関数責務を導入先の実装解析と処理単位の説明から生成する。
  - criterion(JSON Object): <code>{"given":"tool entrypointと呼出先関数に処理単位の説明がある","id":"AC-ASBUILT-010-1","then":"CLI argument、制御flow、関数責務を導入先の実装解析と処理単位の説明から生成する","when":"tool設計を生成する"}</code>
- <code>"AC-ASBUILT-010-2"</code> 前提: 固定版の参照実装と導入先の実sourceがある。条件: 導入先の設計生成・検査toolsを説明する。期待結果: 各CLIの引数、入力正本、生成物、check/更新方法、制御flowと実testへの対応を残す。参照toolへの接続先pathだけをtools自身の設計・試験仕様の代用にしない。。
  - criterion(JSON Object): <code>{"given":"固定版の参照実装と導入先の実sourceがある","id":"AC-ASBUILT-010-2","then":"各CLIの引数、入力正本、生成物、check/更新方法、制御flowと実testへの対応を残す。参照toolへの接続先pathだけをtools自身の設計・試験仕様の代用にしない。","when":"導入先の設計生成・検査toolsを説明する"}</code>

要求源(JSON List): <code>["user:2026-07-21","docs/standards/AS-BUILT-DESIGN.md","user:2026-09-23-language-agnostic-adapters","user:2026-09-26-lazunex-authoritative"]</code>
検証方法: 言語非依存契約テストと導入先adapter検証
検証証跡: manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する
検証(JSON Object): <code>{"evidence":"manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する","method":"言語非依存契約テストと導入先adapter検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/AS-BUILT-DESIGN.md",".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>["governance/checks/catalog.yaml",".agents/skills/generate-implementation-design/scripts/check_design.py"]</code>
- テスト: <code>["tests/test_review_contract.py","tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-011: error case定義の生成

要件ID(JSON): <code>"REQ-ASBUILT-011"</code>
タイトル(JSON): <code>"error case定義の生成"</code>
主体(JSON): <code>"導入先repositoryの設計・静的解析adapter"</code>
対象(JSON): <code>"API error分岐から得たcatalog全体で一意なID付きmachine-readable error case"</code>
導入先repositoryの設計・静的解析adapterは、API error分岐から得たcatalog全体で一意なID付きmachine-readable error caseを**生成する**。
行為enum: <code>"generate"</code>

根拠: error分岐を機械可読にするとE2Eとの1対1 coverageを検査できる。
根拠(JSON): <code>"error分岐を機械可読にするとE2Eとの1対1 coverageを検査できる。"</code>

項目版: 4 / 状態: `active` / 種別: `data`
変更識別子: <code>"CHG-20260923-language-agnostic-adapters"</code>
分類: scope=<code>"project"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-ASBUILT-011-1"</code> 前提: API endpointに正規化されたerror分岐がある。条件: API設計を生成する。期待結果: 各error分岐へ安定IDを付けたmachine-readable定義を出力し、error IDの重複をoperation内だけでなく生成catalog全体で拒否する。
  - criterion(JSON Object): <code>{"given":"API endpointに正規化されたerror分岐がある","id":"AC-ASBUILT-011-1","then":"各error分岐へ安定IDを付けたmachine-readable定義を出力し、error IDの重複をoperation内だけでなく生成catalog全体で拒否する","when":"API設計を生成する"}</code>

要求源(JSON List): <code>["user:2026-07-21","docs/standards/AS-BUILT-DESIGN.md","user:2026-09-23-language-agnostic-adapters"]</code>
検証方法: 言語非依存契約テストと導入先adapter検証
検証証跡: manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する
検証(JSON Object): <code>{"evidence":"manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する","method":"言語非依存契約テストと導入先adapter検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/AS-BUILT-DESIGN.md",".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>["governance/checks/catalog.yaml",".agents/skills/generate-implementation-design/scripts/check_design.py"]</code>
- テスト: <code>["tests/test_review_contract.py","tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-012: 実装仕様sample三点整合

要件ID(JSON): <code>"REQ-ASBUILT-012"</code>
タイトル(JSON): <code>"実装仕様sample三点整合"</code>
主体(JSON): <code>"導入先repositoryの設計・静的解析adapter"</code>
対象(JSON): <code>"endpoint登録と設計metadataとerror sampleの三点整合"</code>
導入先repositoryの設計・静的解析adapterは、endpoint登録と設計metadataとerror sampleの三点整合を**検証する**。
行為enum: <code>"verify"</code>

根拠: 実装、interface情報、設計掲載sampleの片落ちを静的に検出する必要がある。
根拠(JSON): <code>"実装、interface情報、設計掲載sampleの片落ちを静的に検出する必要がある。"</code>

項目版: 4 / 状態: `active` / 種別: `quality`
変更識別子: <code>"CHG-20260926-lazunex-conformance"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-ASBUILT-012-1"</code> 前提: API endpoint、OpenAPI metadata、error sampleがある。条件: 公開API変更の整合checkを実行する。期待結果: endpoint登録漏れ、metadata欠落、error分岐に対応するsample不足を検出する。
  - criterion(JSON Object): <code>{"given":"API endpoint、OpenAPI metadata、error sampleがある","id":"AC-ASBUILT-012-1","then":"endpoint登録漏れ、metadata欠落、error分岐に対応するsample不足を検出する","when":"公開API変更の整合checkを実行する"}</code>
- <code>"AC-ASBUILT-012-2"</code> 前提: 固定版の参照実装と導入先の実sourceがある。条件: interfaceとsampleを生成・検査する。期待結果: 参照schemaを展開した項目表に型・必須・制約・説明を保持し、公開status/分岐ごとの具体的RequestとResponseの対を実契約へ照合する。OpenAPI参照という文だけのsample、未解決参照型、全operationへ根拠なく配る固定sampleを拒否する。。
  - criterion(JSON Object): <code>{"given":"固定版の参照実装と導入先の実sourceがある","id":"AC-ASBUILT-012-2","then":"参照schemaを展開した項目表に型・必須・制約・説明を保持し、公開status/分岐ごとの具体的RequestとResponseの対を実契約へ照合する。OpenAPI参照という文だけのsample、未解決参照型、全operationへ根拠なく配る固定sampleを拒否する。","when":"interfaceとsampleを生成・検査する"}</code>

要求源(JSON List): <code>["user:2026-07-21","docs/standards/AS-BUILT-DESIGN.md","user:2026-09-23-language-agnostic-adapters","user:2026-09-26-lazunex-authoritative"]</code>
検証方法: 言語非依存契約テストと導入先adapter検証
検証証跡: manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する
検証(JSON Object): <code>{"evidence":"manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する","method":"言語非依存契約テストと導入先adapter検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/AS-BUILT-DESIGN.md",".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>["governance/checks/catalog.yaml",".agents/skills/verify-against-engineering-standards/references/as-built-design-check-selection.md",".agents/skills/generate-implementation-design/scripts/check_design.py"]</code>
- テスト: <code>["tests/test_review_contract.py","tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-013: sampleとtestの整合

要件ID(JSON): <code>"REQ-ASBUILT-013"</code>
タイトル(JSON): <code>"sampleとtestの整合"</code>
主体(JSON): <code>"導入先repositoryの設計・静的解析adapter"</code>
対象(JSON): <code>"設計掲載sampleと実response assertionの対応"</code>
導入先repositoryの設計・静的解析adapterは、設計掲載sampleと実response assertionの対応を**検証する**。
行為enum: <code>"verify"</code>

根拠: 設計書に掲載する例をtest済みに限定すると表示と振る舞いの乖離を防げる。
根拠(JSON): <code>"設計書に掲載する例をtest済みに限定すると表示と振る舞いの乖離を防げる。"</code>

項目版: 4 / 状態: `active` / 種別: `quality`
変更識別子: <code>"CHG-20260926-lazunex-conformance"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-ASBUILT-013-1"</code> 前提: 正常または異常response sampleがある。条件: sample整合checkを実行する。期待結果: 各sampleが対応testから参照され、実responseとのassertに使用されていることを検出する。
  - criterion(JSON Object): <code>{"given":"正常または異常response sampleがある","id":"AC-ASBUILT-013-1","then":"各sampleが対応testから参照され、実responseとのassertに使用されていることを検出する","when":"sample整合checkを実行する"}</code>
- <code>"AC-ASBUILT-013-2"</code> 前提: 固定版の参照実装と導入先の実sourceがある。条件: sampleと実testを対応付ける。期待結果: sample IDとcollectorの正確なcase ID、使用したresponse/status/body assertを対応付ける。ファイル名やtest名の部分一致、無関係な認証testへのfallback、存在するがassertに使わないsampleを拒否する。。
  - criterion(JSON Object): <code>{"given":"固定版の参照実装と導入先の実sourceがある","id":"AC-ASBUILT-013-2","then":"sample IDとcollectorの正確なcase ID、使用したresponse/status/body assertを対応付ける。ファイル名やtest名の部分一致、無関係な認証testへのfallback、存在するがassertに使わないsampleを拒否する。","when":"sampleと実testを対応付ける"}</code>

要求源(JSON List): <code>["user:2026-07-21","docs/standards/AS-BUILT-DESIGN.md","user:2026-09-23-language-agnostic-adapters","user:2026-09-26-lazunex-authoritative"]</code>
検証方法: 言語非依存契約テストと導入先adapter検証
検証証跡: manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する
検証(JSON Object): <code>{"evidence":"manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する","method":"言語非依存契約テストと導入先adapter検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/AS-BUILT-DESIGN.md",".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>["governance/checks/catalog.yaml",".agents/skills/verify-against-engineering-standards/references/as-built-design-check-selection.md",".agents/skills/generate-implementation-design/scripts/check_design.py"]</code>
- テスト: <code>["tests/test_review_contract.py","tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-014: CRUDとE2E状態検証の整合

要件ID(JSON): <code>"REQ-ASBUILT-014"</code>
タイトル(JSON): <code>"CRUDとE2E状態検証の整合"</code>
主体(JSON): <code>"導入先repositoryの設計・静的解析adapter"</code>
対象(JSON): <code>"DBまたは外部変更effectを持つAPIとeffect別E2E状態assertの対応"</code>
導入先repositoryの設計・静的解析adapterは、DBまたは外部変更effectを持つAPIとeffect別E2E状態assertの対応を**検証する**。
行為enum: <code>"verify"</code>

根拠: API responseだけでなく永続状態と外部状態を検証してデータ更新の回帰を検出する必要がある。
根拠(JSON): <code>"API responseだけでなく永続状態と外部状態を検証してデータ更新の回帰を検出する必要がある。"</code>

項目版: 4 / 状態: `active` / 種別: `quality`
変更識別子: <code>"CHG-20260923-language-agnostic-adapters"</code>
分類: scope=<code>"product"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-ASBUILT-014-1"</code> 前提: CRUD図でDBまたは外部変更effectを持つAPIがある。条件: CRUD E2E整合checkを実行する。期待結果: DB writeはDB状態、external writeは外部状態を個別にassertし、異常系も各effectの状態不変または理由付き許可変化をassertする。
  - criterion(JSON Object): <code>{"given":"CRUD図でDBまたは外部変更effectを持つAPIがある","id":"AC-ASBUILT-014-1","then":"DB writeはDB状態、external writeは外部状態を個別にassertし、異常系も各effectの状態不変または理由付き許可変化をassertする","when":"CRUD E2E整合checkを実行する"}</code>

要求源(JSON List): <code>["user:2026-07-21","user:2026-08-27","docs/standards/AS-BUILT-DESIGN.md","user:2026-09-23-language-agnostic-adapters"]</code>
検証方法: 言語非依存契約テストと導入先adapter検証
検証証跡: manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する
検証(JSON Object): <code>{"evidence":"manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する","method":"言語非依存契約テストと導入先adapter検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/AS-BUILT-DESIGN.md",".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>["governance/checks/catalog.yaml",".agents/skills/verify-against-engineering-standards/references/as-built-design-check-selection.md",".agents/skills/generate-implementation-design/scripts/check_design.py"]</code>
- テスト: <code>["tests/test_review_contract.py","tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-015: 解析可能なtest構造

要件ID(JSON): <code>"REQ-ASBUILT-015"</code>
タイトル(JSON): <code>"解析可能なtest構造"</code>
主体(JSON): <code>"導入先repositoryの設計・静的解析adapter"</code>
対象(JSON): <code>"前提・操作・期待結果と自然言語の説明を持つ独立した検証単位"</code>
導入先repositoryの設計・静的解析adapterは、前提・操作・期待結果と自然言語の説明を持つ独立した検証単位を**構成する**。
行為enum: <code>"structure"</code>

根拠: 構造化されたtest codeをscenario設計とレビュー観点の一次情報にできる。
根拠(JSON): <code>"構造化されたtest codeをscenario設計とレビュー観点の一次情報にできる。"</code>

項目版: 3 / 状態: `active` / 種別: `quality`
変更識別子: <code>"CHG-20260923-language-agnostic-adapters"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-ASBUILT-015-1"</code> 前提: as-built標準を採用したtest codeがある。条件: test構造checkを実行する。期待結果: unit testのAAA、E2EのGWT、処理単位の説明、1 case 1検証単位を評価し、導入時はAdvisoryとして報告する。
  - criterion(JSON Object): <code>{"given":"as-built標準を採用したtest codeがある","id":"AC-ASBUILT-015-1","then":"unit testのAAA、E2EのGWT、処理単位の説明、1 case 1検証単位を評価し、導入時はAdvisoryとして報告する","when":"test構造checkを実行する"}</code>

要求源(JSON List): <code>["user:2026-07-21","docs/standards/AS-BUILT-DESIGN.md","user:2026-09-23-language-agnostic-adapters"]</code>
検証方法: 言語非依存契約テストと導入先adapter検証
検証証跡: manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する
検証(JSON Object): <code>{"evidence":"manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する","method":"言語非依存契約テストと導入先adapter検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/AS-BUILT-DESIGN.md",".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>["governance/checks/catalog.yaml",".agents/skills/verify-against-engineering-standards/references/as-built-design-check-selection.md",".agents/skills/generate-implementation-design/scripts/check_design.py"]</code>
- テスト: <code>["tests/test_review_contract.py","tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-016: unit test coverage目標

要件ID(JSON): <code>"REQ-ASBUILT-016"</code>
タイトル(JSON): <code>"unit test coverage目標"</code>
主体(JSON): <code>"導入先repositoryの設計・静的解析adapter"</code>
対象(JSON): <code>"C0命令網羅95%以上とC1分岐網羅90%以上のcoverage"</code>
導入先repositoryの設計・静的解析adapterは、C0命令網羅95%以上とC1分岐網羅90%以上のcoverageを**計測する**。
行為enum: <code>"measure"</code>

根拠: 高い命令・分岐網羅を測定目標にしつつ、導入直後のfalse blockerを避けて効果を実測する。
根拠(JSON): <code>"高い命令・分岐網羅を測定目標にしつつ、導入直後のfalse blockerを避けて効果を実測する。"</code>

項目版: 4 / 状態: `active` / 種別: `quality`
変更識別子: <code>"CHG-20260923-language-agnostic-adapters"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-ASBUILT-016-1"</code> 前提: as-built標準を採用したunit test suiteがある。条件: coverageを測定する。期待結果: C0 95%以上とC1 90%以上をAdvisoryとして評価し、実測に基づく昇格判断まで無条件blockingにしない。
  - criterion(JSON Object): <code>{"given":"as-built標準を採用したunit test suiteがある","id":"AC-ASBUILT-016-1","then":"C0 95%以上とC1 90%以上をAdvisoryとして評価し、実測に基づく昇格判断まで無条件blockingにしない","when":"coverageを測定する"}</code>

要求源(JSON List): <code>["user:2026-07-21","docs/standards/AS-BUILT-DESIGN.md","user:2026-09-23-language-agnostic-adapters"]</code>
検証方法: 言語非依存契約テストと導入先adapter検証
検証証跡: manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する
検証(JSON Object): <code>{"evidence":"manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する","method":"言語非依存契約テストと導入先adapter検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/AS-BUILT-DESIGN.md",".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>["governance/checks/catalog.yaml",".agents/skills/generate-implementation-design/scripts/check_design.py"]</code>
- テスト: <code>["tests/test_review_contract.py","tests/test_design_adoption.py"]</code>
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
主体(JSON): <code>"導入先repositoryの設計・静的解析adapter"</code>
対象(JSON): <code>"理由付きRule ID抑制箇所の監査一覧"</code>
導入先repositoryの設計・静的解析adapterは、理由付きRule ID抑制箇所の監査一覧を**生成する**。
行為enum: <code>"generate"</code>

根拠: 例外を一覧化するとsilent suppressionと恒久化した例外を定期監査できる。
根拠(JSON): <code>"例外を一覧化するとsilent suppressionと恒久化した例外を定期監査できる。"</code>

項目版: 3 / 状態: `active` / 種別: `operational`
変更識別子: <code>"CHG-20260923-language-agnostic-adapters"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-ASBUILT-018-1"</code> 前提: コードにignore Rule ID commentがある。条件: 抑制一覧を生成してGovernance Auditを実行する。期待結果: 全抑制path、Rule ID、理由を列挙し、理由欠落、孤児、反復を検出する。
  - criterion(JSON Object): <code>{"given":"コードにignore Rule ID commentがある","id":"AC-ASBUILT-018-1","then":"全抑制path、Rule ID、理由を列挙し、理由欠落、孤児、反復を検出する","when":"抑制一覧を生成してGovernance Auditを実行する"}</code>

要求源(JSON List): <code>["user:2026-07-21","docs/standards/AS-BUILT-DESIGN.md","user:2026-09-23-language-agnostic-adapters"]</code>
検証方法: 言語非依存契約テストと導入先adapter検証
検証証跡: manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する
検証(JSON Object): <code>{"evidence":"manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する","method":"言語非依存契約テストと導入先adapter検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/AS-BUILT-DESIGN.md",".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>["governance/checks/catalog.yaml",".agents/skills/generate-implementation-design/scripts/check_design.py"]</code>
- テスト: <code>["tests/test_review_contract.py","tests/test_design_adoption.py"]</code>
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
主体(JSON): <code>"導入先repositoryの設計・静的解析adapter"</code>
対象(JSON): <code>"宣言したactive requirement集合とartifact・実在test識別子の完全な明示trace"</code>
導入先repositoryの設計・静的解析adapterは、宣言したactive requirement集合とartifact・実在test識別子の完全な明示traceを**妥当性確認する**。
行為enum: <code>"validate"</code>

根拠: 宣言集合との照合と実在testの確認を分離し、特定言語のtest命名へ固定せず追跡漏れを検出する。
根拠(JSON): <code>"宣言集合との照合と実在testの確認を分離し、特定言語のtest命名へ固定せず追跡漏れを検出する。"</code>

項目版: 4 / 状態: `active` / 種別: `quality`
変更識別子: <code>"CHG-20260926-lazunex-conformance"</code>
分類: scope=<code>"product"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-ASBUILT-020-1"</code> 前提: canonical requirementsと適用ID集合とartifact/test traceがある。条件: 導入先adapterと契約検査器がtraceを検査する。期待結果: 未知・inactive・重複ID、未mapping、宣言外mappingを拒否する。導入先adapterは未知artifact・存在しないtest識別子・重複link・metadataとの不一致を拒否し、検査器はそのcheck接続を要求する。実装から要件充足を捏造しない。
  - criterion(JSON Object): <code>{"given":"canonical requirementsと適用ID集合とartifact/test traceがある","id":"AC-ASBUILT-020-1","then":"未知・inactive・重複ID、未mapping、宣言外mappingを拒否する。導入先adapterは未知artifact・存在しないtest識別子・重複link・metadataとの不一致を拒否し、検査器はそのcheck接続を要求する。実装から要件充足を捏造しない","when":"導入先adapterと契約検査器がtraceを検査する"}</code>
- <code>"AC-ASBUILT-020-2"</code> 前提: 固定版の参照実装と導入先の実sourceがある。条件: 参照品質要件を導入先の要件へ対応させる。期待結果: 参照の各要件IDを個別のactiveな導入先受入条件IDへ写像する。複数の独立した参照要件を単一の包括的受入条件へ潰すこと、存在しないcollector IDへの対応、未検証をgaps空で隠すことを拒否する。。
  - criterion(JSON Object): <code>{"given":"固定版の参照実装と導入先の実sourceがある","id":"AC-ASBUILT-020-2","then":"参照の各要件IDを個別のactiveな導入先受入条件IDへ写像する。複数の独立した参照要件を単一の包括的受入条件へ潰すこと、存在しないcollector IDへの対応、未検証をgaps空で隠すことを拒否する。","when":"参照品質要件を導入先の要件へ対応させる"}</code>

要求源(JSON List): <code>["user:2026-08-27","docs/standards/AS-BUILT-DESIGN.md","user:2026-09-23-language-agnostic-adapters","user:2026-09-26-lazunex-authoritative"]</code>
検証方法: 言語非依存契約テストと導入先adapter検証
検証証跡: manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する
検証(JSON Object): <code>{"evidence":"manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する","method":"言語非依存契約テストと導入先adapter検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/AS-BUILT-DESIGN.md",".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/scripts/check_design.py"]</code>
- テスト: <code>["tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-021: 導入時のas-built Markdown生成完了

要件ID(JSON): <code>"REQ-ASBUILT-021"</code>
タイトル(JSON): <code>"導入時のas-built Markdown生成完了"</code>
主体(JSON): <code>"導入先repositoryの設計・静的解析adapter"</code>
対象(JSON): <code>"必要な実装領域のgenerator接続、Markdown生成、欠落とdrift検査"</code>
導入先repositoryの設計・静的解析adapterは、必要な実装領域のgenerator接続、Markdown生成、欠落とdrift検査を**検証する**。
行為enum: <code>"verify"</code>

根拠: 既存generatorだけを起動条件にすると初回導入で生成が省略されるため、接続と生成物の完了確認を2本目の柱に含める。
根拠(JSON): <code>"既存generatorだけを起動条件にすると初回導入で生成が省略されるため、接続と生成物の完了確認を2本目の柱に含める。"</code>

項目版: 2 / 状態: `active` / 種別: `quality`
変更識別子: <code>"CHG-20260923-language-agnostic-adapters"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-ASBUILT-021-1"</code> 前提: 実装を伴う初回導入または設計に影響する変更がある。条件: 導入完了を判定する。期待結果: API・data・infra・frontend等を棚卸しし、必要領域はgeneratorまたはadapterを接続して人向けMarkdownを生成する。実装のない領域だけを理由付きで非該当とし、未接続・未対応の必要領域を完了扱いにしない。
  - criterion(JSON Object): <code>{"given":"実装を伴う初回導入または設計に影響する変更がある","id":"AC-ASBUILT-021-1","then":"API・data・infra・frontend等を棚卸しし、必要領域はgeneratorまたはadapterを接続して人向けMarkdownを生成する。実装のない領域だけを理由付きで非該当とし、未接続・未対応の必要領域を完了扱いにしない","when":"導入完了を判定する"}</code>
- <code>"AC-ASBUILT-021-2"</code> 前提: 導入先所有の生成契約と実装がある。条件: 通常の検証入口で設計検査を実行する。期待結果: 契約欠落・未分類・未完了・必要なMarkdown欠落/空・drift・checkによる書換えを非0終了で拒否する。CIは導入先運用に従い、CIがなくてもローカルで検証する。
  - criterion(JSON Object): <code>{"given":"導入先所有の生成契約と実装がある","id":"AC-ASBUILT-021-2","then":"契約欠落・未分類・未完了・必要なMarkdown欠落/空・drift・checkによる書換えを非0終了で拒否する。CIは導入先運用に従い、CIがなくてもローカルで検証する","when":"通常の検証入口で設計検査を実行する"}</code>
- <code>"AC-ASBUILT-021-3"</code> 前提: 作業を再開または完了報告する。条件: 設計生成の証拠を確認する。期待結果: 実際の生成Markdown、対象revision、実行commandと結果、残存領域を確認する。install receiptや過去会話の完了報告を生成の証拠に代用しない。
  - criterion(JSON Object): <code>{"given":"作業を再開または完了報告する","id":"AC-ASBUILT-021-3","then":"実際の生成Markdown、対象revision、実行commandと結果、残存領域を確認する。install receiptや過去会話の完了報告を生成の証拠に代用しない","when":"設計生成の証拠を確認する"}</code>

要求源(JSON List): <code>["user:2026-09-06","user:2026-09-23-language-agnostic-adapters"]</code>
検証方法: 言語非依存契約テストと導入先adapter検証
検証証跡: manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する
検証(JSON Object): <code>{"evidence":"manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する","method":"言語非依存契約テストと導入先adapter検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/adoption.md",".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/scripts/check_design.py",".agents/skills/chat-first-development/SKILL.md","distribution/snippets/AGENTS.governance.md"]</code>
- テスト: <code>["tests/test_design_adoption.py","tests/test_portable_distribution.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DESIGN-007: SQLのAPI別正本と型付きquery生成

要件ID(JSON): <code>"REQ-DESIGN-007"</code>
タイトル(JSON): <code>"SQLのAPI別正本と型付きquery生成"</code>
主体(JSON): <code>"導入先repositoryの設計・静的解析adapter"</code>
対象(JSON): <code>"operationが所有するSQL正本からの型付きquery生成"</code>
導入先repositoryの設計・静的解析adapterは、operationが所有するSQL正本からの型付きquery生成を**検証する**。
行為enum: <code>"verify"</code>

根拠: SQLの所有と生成元を明示し、移設や型生成による意味変更を防ぐ。
根拠(JSON): <code>"SQLの所有と生成元を明示し、移設や型生成による意味変更を防ぐ。"</code>

項目版: 2 / 状態: `active` / 種別: `quality`
変更識別子: <code>"CHG-20260923-language-agnostic-adapters"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-DESIGN-007-1"</code> 前提: SQLを使うAPIを導入または変更する。条件: 導入先adapterがquery生成と関係する検査を実行する。期待結果: operation所有のSQLとデータ定義から型付きqueryを生成し、lint・binding・NULL・行数・戻り型・transaction/rollback・生成driftを検証する。適用済みmigration本文とchecksumを保持し、SQLがない場合は理由付き非該当とする。
  - criterion(JSON Object): <code>{"given":"SQLを使うAPIを導入または変更する","id":"AC-DESIGN-007-1","then":"operation所有のSQLとデータ定義から型付きqueryを生成し、lint・binding・NULL・行数・戻り型・transaction/rollback・生成driftを検証する。適用済みmigration本文とchecksumを保持し、SQLがない場合は理由付き非該当とする","when":"導入先adapterがquery生成と関係する検査を実行する"}</code>

要求源(JSON List): <code>["user:2026-09-06","user:2026-09-23-language-agnostic-adapters"]</code>
検証方法: 言語非依存契約テストと導入先adapter検証
検証証跡: manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する
検証(JSON Object): <code>{"evidence":"manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する","method":"言語非依存契約テストと導入先adapter検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/scripts/check_design.py",".agents/skills/chat-first-development/SKILL.md",".agents/skills/inspect-quality-gates/SKILL.md"]</code>
- テスト: <code>["tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DOCS-002: 説明コメントと生成ヘッダーの日本語

要件ID(JSON): <code>"REQ-DOCS-002"</code>
タイトル(JSON): <code>"説明コメントと生成ヘッダーの日本語"</code>
主体(JSON): <code>"導入先repositoryの設計・静的解析adapter"</code>
対象(JSON): <code>"利用者指定に従う説明コメント・処理単位の説明・生成ヘッダー"</code>
導入先repositoryの設計・静的解析adapterは、利用者指定に従う説明コメント・処理単位の説明・生成ヘッダーを**検証する**。
行為enum: <code>"verify"</code>

根拠: コメントの存在検査だけでは英語を検出できず、生成元が英語なら再生成で戻るため、言語指定と生成元修正を完了条件に含める。
根拠(JSON): <code>"コメントの存在検査だけでは英語を検出できず、生成元が英語なら再生成で戻るため、言語指定と生成元修正を完了条件に含める。"</code>

項目版: 2 / 状態: `active` / 種別: `quality`
変更識別子: <code>"CHG-20260923-language-agnostic-adapters"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-DOCS-002-1"</code> 前提: 説明または生成物の説明を作成・変更する。条件: 導入先adapterまたは差分レビューが説明言語を検証する。期待結果: 別言語の明示指示がなければ日本語とし、識別子・機械指示・ライセンス・実行時文字列は維持する。生成物の説明は生成元を修正して再生成し、検査対象と結果を示す。日本語文字の存在だけで意味品質を保証しない。
  - criterion(JSON Object): <code>{"given":"説明または生成物の説明を作成・変更する","id":"AC-DOCS-002-1","then":"別言語の明示指示がなければ日本語とし、識別子・機械指示・ライセンス・実行時文字列は維持する。生成物の説明は生成元を修正して再生成し、検査対象と結果を示す。日本語文字の存在だけで意味品質を保証しない","when":"導入先adapterまたは差分レビューが説明言語を検証する"}</code>

要求源(JSON List): <code>["user:2026-09-06","user:2026-09-23-language-agnostic-adapters"]</code>
検証方法: 言語非依存契約テストと導入先adapter検証
検証証跡: manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する
検証(JSON Object): <code>{"evidence":"manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する","method":"言語非依存契約テストと導入先adapter検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/scripts/check_design.py",".agents/skills/chat-first-development/SKILL.md",".agents/skills/inspect-quality-gates/SKILL.md"]</code>
- テスト: <code>["tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DESIGN-001: endpoint層と個別処理単位の分離

要件ID(JSON): <code>"REQ-DESIGN-001"</code>
タイトル(JSON): <code>"endpoint層と個別処理単位の分離"</code>
主体(JSON): <code>"導入先repositoryの設計・静的解析adapter"</code>
対象(JSON): <code>"endpoint層の全体フローと個別処理単位の具体処理に分離したoperation"</code>
導入先repositoryの設計・静的解析adapterは、endpoint層の全体フローと個別処理単位の具体処理に分離したoperationを**構成する**。
行為enum: <code>"structure"</code>

根拠: 安定したoperation境界により、処理フローの導出と詳細設計の決定的な検査ができる。
根拠(JSON): <code>"安定したoperation境界により、処理フローの導出と詳細設計の決定的な検査ができる。"</code>

項目版: 5 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"CHG-20260926-lazunex-conformance"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-DESIGN-001-1"</code> 前提: API operationを実装している。条件: 導入先adapterが責務構成を検査する。期待結果: endpoint層が全体フローを所有し、個別処理単位が具体処理を所有する。特定言語のファイル名で適合を判定しない。
  - criterion(JSON Object): <code>{"given":"API operationを実装している","id":"AC-DESIGN-001-1","then":"endpoint層が全体フローを所有し、個別処理単位が具体処理を所有する。特定言語のファイル名で適合を判定しない","when":"導入先adapterが責務構成を検査する"}</code>
- <code>"AC-DESIGN-001-2"</code> 前提: 固定版の参照実装と導入先の実sourceがある。条件: lazunex基準の責務境界を実装する。期待結果: endpointは処理順・認可分岐・例外/transaction境界を、個別業務処理は判定・DB/provider境界・応答組立を所有する。言語に応じて配置名を変えても、endpoint内のquery wrapper呼出し、入力hashや条件比較・応答model組立等の業務処理集約を同等構成と扱わない。。
  - criterion(JSON Object): <code>{"given":"固定版の参照実装と導入先の実sourceがある","id":"AC-DESIGN-001-2","then":"endpointは処理順・認可分岐・例外/transaction境界を、個別業務処理は判定・DB/provider境界・応答組立を所有する。言語に応じて配置名を変えても、endpoint内のquery wrapper呼出し、入力hashや条件比較・応答model組立等の業務処理集約を同等構成と扱わない。","when":"lazunex基準の責務境界を実装する"}</code>

要求源(JSON List): <code>["user:2026-07-17","user:2026-09-23-language-agnostic-adapters","user:2026-09-26-lazunex-authoritative"]</code>
検証方法: 言語非依存契約テストと導入先adapter検証
検証証跡: manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する
検証(JSON Object): <code>{"evidence":"manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する","method":"言語非依存契約テストと導入先adapter検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/SKILL.md"]</code>
- テスト: <code>["tests/test_design_adoption.py"]</code>
- 参照資料: <code>["SWEBOK-V4A"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DESIGN-002: 実call graphからのシーケンス図導出

要件ID(JSON): <code>"REQ-DESIGN-002"</code>
タイトル(JSON): <code>"実call graphからのシーケンス図導出"</code>
主体(JSON): <code>"導入先repositoryの設計・静的解析adapter"</code>
対象(JSON): <code>"endpoint起点の実call graphから得たoperationシーケンス図"</code>
導入先repositoryの設計・静的解析adapterは、endpoint起点の実call graphから得たoperationシーケンス図を**導出する**。
行為enum: <code>"derive"</code>

根拠: 実装から導出したフロー文書はソースとの整合を維持できる。
根拠(JSON): <code>"実装から導出したフロー文書はソースとの整合を維持できる。"</code>

項目版: 3 / 状態: `active` / 種別: `functional`
変更識別子: <code>"CHG-20260923-language-agnostic-adapters"</code>
分類: scope=<code>"project"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-DESIGN-002-1"</code> 前提: endpointと到達可能な処理単位がある。条件: 導入先adapterがsequenceを生成する。期待結果: 実call graphの呼出順・条件・反復・例外・transactionを保持する。定型図や呼出先のソート集合を実flowの代用にしない。
  - criterion(JSON Object): <code>{"given":"endpointと到達可能な処理単位がある","id":"AC-DESIGN-002-1","then":"実call graphの呼出順・条件・反復・例外・transactionを保持する。定型図や呼出先のソート集合を実flowの代用にしない","when":"導入先adapterがsequenceを生成する"}</code>

要求源(JSON List): <code>["user:2026-07-17","user:2026-09-23-language-agnostic-adapters"]</code>
検証方法: 言語非依存契約テストと導入先adapter検証
検証証跡: manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する
検証(JSON Object): <code>{"evidence":"manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する","method":"言語非依存契約テストと導入先adapter検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/scripts/check_design.py"]</code>
- テスト: <code>["tests/test_design_adoption.py"]</code>
- 参照資料: <code>["SWEBOK-V4A"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DESIGN-003: 公開interfaceからの設計導出

要件ID(JSON): <code>"REQ-DESIGN-003"</code>
タイトル(JSON): <code>"公開interfaceからの設計導出"</code>
主体(JSON): <code>"導入先repositoryの設計・静的解析adapter"</code>
対象(JSON): <code>"実装に接続された公開interface定義からのAPIと入出力一覧"</code>
導入先repositoryの設計・静的解析adapterは、実装に接続された公開interface定義からのAPIと入出力一覧を**導出する**。
行為enum: <code>"derive"</code>

根拠: 実装に接続したinterface定義を正本にして手書き一覧の二重保守を避ける。
根拠(JSON): <code>"実装に接続したinterface定義を正本にして手書き一覧の二重保守を避ける。"</code>

項目版: 3 / 状態: `active` / 種別: `interface`
変更識別子: <code>"CHG-20260923-language-agnostic-adapters"</code>
分類: scope=<code>"project"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-DESIGN-003-1"</code> 前提: 実装に接続された公開interface定義がある。条件: 導入先adapterがinterface設計を生成する。期待結果: operation IDを重複させずAPI、request、response、参照schemaを保持する。OpenAPIを用いる導入先ではその互換性を検証する。
  - criterion(JSON Object): <code>{"given":"実装に接続された公開interface定義がある","id":"AC-DESIGN-003-1","then":"operation IDを重複させずAPI、request、response、参照schemaを保持する。OpenAPIを用いる導入先ではその互換性を検証する","when":"導入先adapterがinterface設計を生成する"}</code>

要求源(JSON List): <code>["user:2026-09-23-language-agnostic-adapters"]</code>
検証方法: 言語非依存契約テストと導入先adapter検証
検証証跡: manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する
検証(JSON Object): <code>{"evidence":"manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する","method":"言語非依存契約テストと導入先adapter検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/scripts/check_design.py"]</code>
- テスト: <code>["tests/test_design_adoption.py"]</code>
- 参照資料: <code>["SWEBOK-V4A"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DESIGN-004: 保存先操作からのデータ設計導出

要件ID(JSON): <code>"REQ-DESIGN-004"</code>
タイトル(JSON): <code>"保存先操作からのデータ設計導出"</code>
主体(JSON): <code>"導入先repositoryの設計・静的解析adapter"</code>
対象(JSON): <code>"実行する保存先操作の意味解析から得たqueryとCRUD設計"</code>
導入先repositoryの設計・静的解析adapterは、実行する保存先操作の意味解析から得たqueryとCRUD設計を**解析する**。
行為enum: <code>"parse"</code>

根拠: 操作の構造的な根拠を持ち、無効または未対応の操作を推測で補わない。
根拠(JSON): <code>"操作の構造的な根拠を持ち、無効または未対応の操作を推測で補わない。"</code>

項目版: 3 / 状態: `active` / 種別: `data`
変更識別子: <code>"CHG-20260923-language-agnostic-adapters"</code>
分類: scope=<code>"project"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-DESIGN-004-1"</code> 前提: 実行可能な保存先操作がある。条件: 導入先adapterが操作を解析する。期待結果: 操作の引数・結果・対象・参照先と変更先を解析し、queryとCRUDモデルを生成する。SQL等の構文解析は導入先が所有し、parse不能を拒否する。
  - criterion(JSON Object): <code>{"given":"実行可能な保存先操作がある","id":"AC-DESIGN-004-1","then":"操作の引数・結果・対象・参照先と変更先を解析し、queryとCRUDモデルを生成する。SQL等の構文解析は導入先が所有し、parse不能を拒否する","when":"導入先adapterが操作を解析する"}</code>

要求源(JSON List): <code>["user:2026-09-23-language-agnostic-adapters"]</code>
検証方法: 言語非依存契約テストと導入先adapter検証
検証証跡: manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する
検証(JSON Object): <code>{"evidence":"manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する","method":"言語非依存契約テストと導入先adapter検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/scripts/check_design.py"]</code>
- テスト: <code>["tests/test_design_adoption.py"]</code>
- 参照資料: <code>["SWEBOK-V4A"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DESIGN-005: デプロイ設計の生成

要件ID(JSON): <code>"REQ-DESIGN-005"</code>
タイトル(JSON): <code>"デプロイ設計の生成"</code>
主体(JSON): <code>"導入先repositoryの設計・静的解析adapter"</code>
対象(JSON): <code>"実デプロイartifactからのresourceとparameter一覧"</code>
導入先repositoryの設計・静的解析adapterは、実デプロイartifactからのresourceとparameter一覧を**導出する**。
行為enum: <code>"derive"</code>

根拠: 実際にデプロイに使うartifactを正本にして構成の二重保守を防ぐ。
根拠(JSON): <code>"実際にデプロイに使うartifactを正本にして構成の二重保守を防ぐ。"</code>

項目版: 3 / 状態: `active` / 種別: `functional`
変更識別子: <code>"CHG-20260923-language-agnostic-adapters"</code>
分類: scope=<code>"project"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-DESIGN-005-1"</code> 前提: デプロイ対象artifactがある。条件: 導入先adapterがinfra設計を生成する。期待結果: resource、parameterとartifact digestを実デプロイartifactから導出する。特定のIaC言語やcloud providerを前提にしない。
  - criterion(JSON Object): <code>{"given":"デプロイ対象artifactがある","id":"AC-DESIGN-005-1","then":"resource、parameterとartifact digestを実デプロイartifactから導出する。特定のIaC言語やcloud providerを前提にしない","when":"導入先adapterがinfra設計を生成する"}</code>

要求源(JSON List): <code>["user:2026-09-23-language-agnostic-adapters"]</code>
検証方法: 言語非依存契約テストと導入先adapter検証
検証証跡: manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する
検証(JSON Object): <code>{"evidence":"manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する","method":"言語非依存契約テストと導入先adapter検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/scripts/check_design.py"]</code>
- テスト: <code>["tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DESIGN-006: 実装と設計の差分検出

要件ID(JSON): <code>"REQ-DESIGN-006"</code>
タイトル(JSON): <code>"実装と設計の差分検出"</code>
主体(JSON): <code>"導入先repositoryの設計・静的解析adapter"</code>
対象(JSON): <code>"実装成果物と自動生成された詳細設計の差分"</code>
導入先repositoryの設計・静的解析adapterは、実装成果物と自動生成された詳細設計の差分を**検出する**。
行為enum: <code>"detect"</code>

根拠: digestと決定論的なバイト比較により実装と設計の1対1再現性を強制し、更新漏れの対象pathを特定する。
根拠(JSON): <code>"digestと決定論的なバイト比較により実装と設計の1対1再現性を強制し、更新漏れの対象pathを特定する。"</code>

項目版: 4 / 状態: `active` / 種別: `quality`
変更識別子: <code>"CHG-20260923-language-agnostic-adapters"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-DESIGN-006-1"</code> 前提: 宣言済みの自動生成設計がある。条件: 設計check modeを実行する。期待結果: source SHA-256 manifestとクリーンな再生成結果がバイト単位で一致し、差分時は対象pathを列挙して非0終了する。
  - criterion(JSON Object): <code>{"given":"宣言済みの自動生成設計がある","id":"AC-DESIGN-006-1","then":"source SHA-256 manifestとクリーンな再生成結果がバイト単位で一致し、差分時は対象pathを列挙して非0終了する","when":"設計check modeを実行する"}</code>

要求源(JSON List): <code>["user:2026-07-17","user:2026-07-21","docs/standards/AS-BUILT-DESIGN.md","user:2026-09-23-language-agnostic-adapters"]</code>
検証方法: 言語非依存契約テストと導入先adapter検証
検証証跡: manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する
検証(JSON Object): <code>{"evidence":"manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する","method":"言語非依存契約テストと導入先adapter検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/SKILL.md","docs/standards/AS-BUILT-DESIGN.md",".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/scripts/check_design.py","governance/checks/catalog.yaml"]</code>
- テスト: <code>["tests/test_design_adoption.py","tests/test_review_contract.py"]</code>
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

項目版: 2 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"user:2026-09-05"</code>
分類: scope=<code>"product"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-PORTABLE-003-1"</code> 前提: 外部systemへの書込みまたは不可逆な操作が開発手順に現れる。条件: portable Skillまたはruntimeが実行可否を判断する。期待結果: 利用者がその結果を明示的に依頼し、対象systemに必要な権限が確認できる場合だけ実行し、それ以外はrepository内の成果物またはhandoffに留める。
  - criterion(JSON Object): <code>{"given":"外部systemへの書込みまたは不可逆な操作が開発手順に現れる","id":"AC-PORTABLE-003-1","then":"利用者がその結果を明示的に依頼し、対象systemに必要な権限が確認できる場合だけ実行し、それ以外はrepository内の成果物またはhandoffに留める","when":"portable Skillまたはruntimeが実行可否を判断する"}</code>
- <code>"AC-PORTABLE-003-2"</code> 前提: 同じ対象と外部作用への明示依頼・承認が会話または対象所有記録にあり、撤回・失効していない。条件: 後続の手順で同じ権限境界を確認する。期待結果: 既存承認を再利用し、形式的な再承認や別Skillの導入を要求しない。範囲拡張、失効、対象側の必須承認は省略しない。
  - criterion(JSON Object): <code>{"given":"同じ対象と外部作用への明示依頼・承認が会話または対象所有記録にあり、撤回・失効していない","id":"AC-PORTABLE-003-2","then":"既存承認を再利用し、形式的な再承認や別Skillの導入を要求しない。範囲拡張、失効、対象側の必須承認は省略しない","when":"後続の手順で同じ権限境界を確認する"}</code>

要求源(JSON List): <code>["user:2026-09-05","user:2026-08-27","user:2026-08-29","AGENTS.md"]</code>
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

項目版: 3 / 状態: `active` / 種別: `quality`
変更識別子: <code>"user:2026-09-05"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-QUINT-003-1"</code> 前提: Skill directoryとQuint契約catalogがある。条件: 形式契約検査を実行する。期待結果: 双方の名前集合が完全一致し、各SKILL.mdから契約へtraceできる。
  - criterion(JSON Object): <code>{"given":"Skill directoryとQuint契約catalogがある","id":"AC-QUINT-003-1","then":"双方の名前集合が完全一致し、各SKILL.mdから契約へtraceできる","when":"形式契約検査を実行する"}</code>
- <code>"AC-QUINT-003-2"</code> 前提: active要件がSkill pathをtraceするかSkill契約がrequirement IDを宣言する。条件: trace整合検査を実行する。期待結果: 要件からSkill pathへの組とSkillからactive requirement IDへの組が完全一致し、未知またはretired IDを拒否する。
  - criterion(JSON Object): <code>{"given":"active要件がSkill pathをtraceするかSkill契約がrequirement IDを宣言する","id":"AC-QUINT-003-2","then":"要件からSkill pathへの組とSkillからactive requirement IDへの組が完全一致し、未知またはretired IDを拒否する","when":"trace整合検査を実行する"}</code>
- <code>"AC-QUINT-003-3"</code> 前提: Skillを実行時に読み込む。条件: Quint契約のviewを生成する。期待結果: 入口には起動条件と実行境界と正本参照だけを表示し、詳細field・asset一覧・digestは生成catalogで保持する。簡略表示後も全field検査、digest照合、配布先drift検知を維持する。
  - criterion(JSON Object): <code>{"given":"Skillを実行時に読み込む","id":"AC-QUINT-003-3","then":"入口には起動条件と実行境界と正本参照だけを表示し、詳細field・asset一覧・digestは生成catalogで保持する。簡略表示後も全field検査、digest照合、配布先drift検知を維持する","when":"Quint契約のviewを生成する"}</code>

要求源(JSON List): <code>["user:2026-09-05","user:2026-08-27","user:2026-08-29","https://quint.sh/docs/what-does-quint-do","docs/decisions/ADR-0004-quint-three-pillar-portability.md"]</code>
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

## REQ-ASBUILT-022: 全operationの6帳票集合

要件ID(JSON): <code>"REQ-ASBUILT-022"</code>
タイトル(JSON): <code>"全operationの6帳票集合"</code>
主体(JSON): <code>"導入先repositoryの設計・静的解析adapter"</code>
対象(JSON): <code>"全operationに対応する詳細設計・interface・ログmessage・query・sequence・unit-test詳細の6帳票"</code>
導入先repositoryの設計・静的解析adapterは、全operationに対応する詳細設計・interface・ログmessage・query・sequence・unit-test詳細の6帳票を**生成する**。
行為enum: <code>"generate"</code>

根拠: ファイル存在や関数一覧だけではDB入出力・ログ・テスト要因が欠落しても完了になる。
根拠(JSON): <code>"ファイル存在や関数一覧だけではDB入出力・ログ・テスト要因が欠落しても完了になる。"</code>

項目版: 2 / 状態: `active` / 種別: `quality`
変更識別子: <code>"CHG-20260923-language-agnostic-adapters"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-ASBUILT-022-1"</code> 前提: API実装が存在する。条件: 導入先adapterが生成し契約検査器が帳票集合を照合する。期待結果: 全operationに6帳票を対応付け、欠落・余剰operationを拒否する。実装がない内容にも章と非該当理由を残し、未対応を非該当へ偽装しない。
  - criterion(JSON Object): <code>{"given":"API実装が存在する","id":"AC-ASBUILT-022-1","then":"全operationに6帳票を対応付け、欠落・余剰operationを拒否する。実装がない内容にも章と非該当理由を残し、未対応を非該当へ偽装しない","when":"導入先adapterが生成し契約検査器が帳票集合を照合する"}</code>

要求源(JSON List): <code>["user:2026-09-06-api-six-documents","https://github.com/tsuji-tomonori/rag-sample/tree/main/docs/spec/40.apis","user:2026-09-23-language-agnostic-adapters"]</code>
検証方法: 言語非依存契約テストと導入先adapter検証
検証証跡: manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する
検証(JSON Object): <code>{"evidence":"manifestの接続・結果契約をdev-standardで検査し、意味解析の正例・負例は導入先のcheck commandで検証する","method":"言語非依存契約テストと導入先adapter検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>["docs/standards/AS-BUILT-DESIGN.md",".agents/skills/generate-implementation-design/references/api-documents.md",".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/scripts/check_design.py"]</code>
- テスト: <code>["tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-EVIDENCE-001: 品質portalの既定初期構築

要件ID(JSON): <code>"REQ-EVIDENCE-001"</code>
タイトル(JSON): <code>"品質portalの既定初期構築"</code>
主体(JSON): <code>"開発開始フロー"</code>
対象(JSON): <code>"製品要件からframeworkに応じた品質portalと公開準備を初期構築すること"</code>
開発開始フローは、製品要件からframeworkに応じた品質portalと公開準備を初期構築することを**提供する**。
行為enum: <code>"provide"</code>

根拠: 利用者が開発基盤の個別設定を毎回指定する負担をなくす。
根拠(JSON): <code>"利用者が開発基盤の個別設定を毎回指定する負担をなくす。"</code>

項目版: 1 / 状態: `active` / 種別: `quality`
変更識別子: <code>"CHG-20260906-default-evidence-portal"</code>
分類: scope=<code>"product"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-EVIDENCE-001-1"</code> 前提: 新規開発またはDev標準導入を依頼された。条件: agentが初期実装を行う。期待結果: 実test一覧・実行結果・静的解析・coverage・生成設計書のadapterと閲覧siteを接続し、空templateを完成としない。
  - criterion(JSON Object): <code>{"given":"新規開発またはDev標準導入を依頼された","id":"AC-EVIDENCE-001-1","then":"実test一覧・実行結果・静的解析・coverage・生成設計書のadapterと閲覧siteを接続し、空templateを完成としない","when":"agentが初期実装を行う"}</code>
- <code>"AC-EVIDENCE-001-2"</code> 前提: 新規GitHub projectまたは既存CIを持つprojectがある。条件: 公開準備を行う。期待結果: 新規ではPages用target-owned設定を初期構築し、既存では現行CIと公開先を維持して接続する。installerはworkflowをコピーせず、実公開は対象権限に従う。
  - criterion(JSON Object): <code>{"given":"新規GitHub projectまたは既存CIを持つprojectがある","id":"AC-EVIDENCE-001-2","then":"新規ではPages用target-owned設定を初期構築し、既存では現行CIと公開先を維持して接続する。installerはworkflowをコピーせず、実公開は対象権限に従う","when":"公開準備を行う"}</code>

要求源(JSON List): <code>["user:2026-09-06","https://github.com/tsuji-tomonori/CornellNoteWebv2/tree/dev"]</code>
検証方法: 契約・adapter・生成drift検証
検証証跡: 共通reportと2系統runnerの回帰検証
検証(JSON Object): <code>{"evidence":"共通reportと2系統runnerの回帰検証","method":"契約・adapter・生成drift検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/inspect-quality-gates/references/evidence-portal.md"]</code>
- 実装: <code>[".agents/skills/inspect-quality-gates/scripts/evidence.py",".agents/skills/inspect-quality-gates/scripts/test_evidence.py",".agents/skills/chat-first-development/SKILL.md"]</code>
- テスト: <code>["tests/test_evidence_portal.py"]</code>
- 参照資料: <code>[]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-EVIDENCE-002: エビデンスの実測対応

要件ID(JSON): <code>"REQ-EVIDENCE-002"</code>
タイトル(JSON): <code>"エビデンスの実測対応"</code>
主体(JSON): <code>"品質report生成処理"</code>
対象(JSON): <code>"collectorと実行結果に対応する失敗を隠さない共通report"</code>
品質report生成処理は、collectorと実行結果に対応する失敗を隠さない共通reportを**生成する**。
行為enum: <code>"generate"</code>

根拠: 一覧から漏れたtestや未実行を全件成功と誤認することを防ぐ。
根拠(JSON): <code>"一覧から漏れたtestや未実行を全件成功と誤認することを防ぐ。"</code>

項目版: 1 / 状態: `active` / 種別: `quality`
変更識別子: <code>"CHG-20260906-default-evidence-portal"</code>
分類: scope=<code>"product"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-EVIDENCE-002-1"</code> 前提: collectorと実行結果がある。条件: 共通reportへ変換する。期待結果: 安定case IDを照合し、失敗・skip・未実行・flaky・missingを区別して保持する。
  - criterion(JSON Object): <code>{"given":"collectorと実行結果がある","id":"AC-EVIDENCE-002-1","then":"安定case IDを照合し、失敗・skip・未実行・flaky・missingを区別して保持する","when":"共通reportへ変換する"}</code>
- <code>"AC-EVIDENCE-002-2"</code> 前提: E2E・coverage・設計書が該当する。条件: 閲覧siteを生成する。期待結果: GWTの説明と拡大画像、coverageのmetric別実測分母分子、検索・章一覧・目次・Mermaidを持つ設計HTMLへ移動できる。
  - criterion(JSON Object): <code>{"given":"E2E・coverage・設計書が該当する","id":"AC-EVIDENCE-002-2","then":"GWTの説明と拡大画像、coverageのmetric別実測分母分子、検索・章一覧・目次・Mermaidを持つ設計HTMLへ移動できる","when":"閲覧siteを生成する"}</code>

要求源(JSON List): <code>["user:2026-09-06","https://github.com/tsuji-tomonori/CornellNoteWebv2/tree/dev"]</code>
検証方法: 契約・adapter・生成drift検証
検証証跡: 共通reportと2系統runnerの回帰検証
検証(JSON Object): <code>{"evidence":"共通reportと2系統runnerの回帰検証","method":"契約・adapter・生成drift検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/inspect-quality-gates/references/evidence-portal.md"]</code>
- 実装: <code>[".agents/skills/inspect-quality-gates/scripts/evidence.py",".agents/skills/inspect-quality-gates/scripts/test_evidence.py",".agents/skills/chat-first-development/SKILL.md"]</code>
- テスト: <code>["tests/test_evidence_portal.py"]</code>
- 参照資料: <code>[]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-EVIDENCE-003: 公開成果のrun境界

要件ID(JSON): <code>"REQ-EVIDENCE-003"</code>
タイトル(JSON): <code>"公開成果のrun境界"</code>
主体(JSON): <code>"品質report公開処理"</code>
対象(JSON): <code>"同一revision/runの選別済みartifactだけを公開対象にすること"</code>
品質report公開処理は、同一revision/runの選別済みartifactだけを公開対象にすることを**制約する**。
行為enum: <code>"constrain"</code>

根拠: 古い成功表示や非公開log混入を防ぎ検査失敗を隠さない。
根拠(JSON): <code>"古い成功表示や非公開log混入を防ぎ検査失敗を隠さない。"</code>

項目版: 1 / 状態: `active` / 種別: `quality`
変更識別子: <code>"CHG-20260906-default-evidence-portal"</code>
分類: scope=<code>"product"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-EVIDENCE-003-1"</code> 前提: reportを生成する。条件: 公開用artifactを作る。期待結果: revision一致と欠落・driftを検査し、明示allowlist外のfileとsymlink・path逸脱を拒否する。
  - criterion(JSON Object): <code>{"given":"reportを生成する","id":"AC-EVIDENCE-003-1","then":"revision一致と欠落・driftを検査し、明示allowlist外のfileとsymlink・path逸脱を拒否する","when":"公開用artifactを作る"}</code>
- <code>"AC-EVIDENCE-003-2"</code> 前提: CI検査が失敗した。条件: report生成と公開jobを実行する。期待結果: 有効な失敗reportを生成でき、元の検査失敗を維持する。PR/forkを公開せずtrustedな対象branchと既存権限だけで公開する。
  - criterion(JSON Object): <code>{"given":"CI検査が失敗した","id":"AC-EVIDENCE-003-2","then":"有効な失敗reportを生成でき、元の検査失敗を維持する。PR/forkを公開せずtrustedな対象branchと既存権限だけで公開する","when":"report生成と公開jobを実行する"}</code>

要求源(JSON List): <code>["user:2026-09-06","https://github.com/tsuji-tomonori/CornellNoteWebv2/tree/dev"]</code>
検証方法: 契約・adapter・生成drift検証
検証証跡: 共通reportと2系統runnerの回帰検証
検証(JSON Object): <code>{"evidence":"共通reportと2系統runnerの回帰検証","method":"契約・adapter・生成drift検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/inspect-quality-gates/references/evidence-portal.md"]</code>
- 実装: <code>[".agents/skills/inspect-quality-gates/scripts/evidence.py",".agents/skills/inspect-quality-gates/scripts/test_evidence.py",".agents/skills/chat-first-development/SKILL.md"]</code>
- テスト: <code>["tests/test_evidence_portal.py"]</code>
- 参照資料: <code>[]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-023: 版付き帳票構成profile

要件ID(JSON): <code>"REQ-ASBUILT-023"</code>
タイトル(JSON): <code>"版付き帳票構成profile"</code>
主体(JSON): <code>"導入先repositoryのadapter"</code>
対象(JSON): <code>"6帳票の章・順序・必須節・繰返し節・非該当表現"</code>
導入先repositoryのadapterは、6帳票の章・順序・必須節・繰返し節・非該当表現を**検証する**。
行為enum: <code>"verify"</code>

根拠: 版付き帳票構成profileを明示的な契約にして欠落や推測による成功判定を防ぐ。
根拠(JSON): <code>"版付き帳票構成profileを明示的な契約にして欠落や推測による成功判定を防ぐ。"</code>

項目版: 2 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"CHG-20260923-independent-review-fixes"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-ASBUILT-023-1"</code> 前提: 該当する実装surfaceとadapter manifestがある。条件: 導入先adapterの契約適合を検証する。期待結果: version付きprofileを選択し、見出し階層、章の欠落・順序違い・重複、必須節と繰返し節、非該当理由の欠落を拒否する。構成適合を意味的完全性と区別する。
  - criterion(JSON Object): <code>{"given":"該当する実装surfaceとadapter manifestがある","id":"AC-ASBUILT-023-1","then":"version付きprofileを選択し、見出し階層、章の欠落・順序違い・重複、必須節と繰返し節、非該当理由の欠落を拒否する。構成適合を意味的完全性と区別する","when":"導入先adapterの契約適合を検証する"}</code>
- <code>"AC-ASBUILT-023-2"</code> 前提: 該当する実装と選択profileがある。条件: 導入先adapterの正例と負例を検証する。期待結果: profile自身のgrammar配列、固定節・繰返し節、見出しlevel、最小件数、理由付き非該当表現を検証する。同じID・版の公開済み章契約を削除・改変して適合検査を回避するprofileを拒否する。
  - criterion(JSON Object): <code>{"given":"該当する実装と選択profileがある","id":"AC-ASBUILT-023-2","then":"profile自身のgrammar配列、固定節・繰返し節、見出しlevel、最小件数、理由付き非該当表現を検証する。同じID・版の公開済み章契約を削除・改変して適合検査を回避するprofileを拒否する","when":"導入先adapterの正例と負例を検証する"}</code>

要求源(JSON List): <code>["https://github.com/tsuji-tomonori/dev-standard/issues/67","user:2026-09-23-language-agnostic-adapters"]</code>
検証方法: 言語非依存契約検査と導入先adapterの正例・負例検証
検証証跡: manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する
検証(JSON Object): <code>{"evidence":"manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する","method":"言語非依存契約検査と導入先adapterの正例・負例検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/scripts/check_design.py"]</code>
- テスト: <code>["tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-024: CRUD出力の同一モデル対応

要件ID(JSON): <code>"REQ-ASBUILT-024"</code>
タイトル(JSON): <code>"CRUD出力の同一モデル対応"</code>
主体(JSON): <code>"導入先repositoryのadapter"</code>
対象(JSON): <code>"API×保存先モデルからのCSV・表・図・根拠"</code>
導入先repositoryのadapterは、API×保存先モデルからのCSV・表・図・根拠を**検証する**。
行為enum: <code>"verify"</code>

根拠: CRUD出力の同一モデル対応を明示的な契約にして欠落や推測による成功判定を防ぐ。
根拠(JSON): <code>"CRUD出力の同一モデル対応を明示的な契約にして欠落や推測による成功判定を防ぐ。"</code>

項目版: 2 / 状態: `active` / 種別: `functional`
変更識別子: <code>"CHG-20260926-lazunex-conformance"</code>
分類: scope=<code>"project"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-ASBUILT-024-1"</code> 前提: 該当する実装surfaceとadapter manifestがある。条件: 導入先adapterの契約適合を検証する。期待結果: CSV・表・図・根拠を一つのモデルから決定的に生成し、全operationのアクセスなしを明示する。形式間の行・操作・根拠の不一致と未解決をアクセスなしとする報告を拒否する。
  - criterion(JSON Object): <code>{"given":"該当する実装surfaceとadapter manifestがある","id":"AC-ASBUILT-024-1","then":"CSV・表・図・根拠を一つのモデルから決定的に生成し、全operationのアクセスなしを明示する。形式間の行・操作・根拠の不一致と未解決をアクセスなしとする報告を拒否する","when":"導入先adapterの契約適合を検証する"}</code>
- <code>"AC-ASBUILT-024-2"</code> 前提: 固定版の参照実装と導入先の実sourceがある。条件: lazunex基準のCRUDを表示する。期待結果: APIを行、資源を列、セルをC/R/U/D順の組合せとする行列を正規表示にする。全operationとDDL・外部資源台帳の全資源を母集合とし、未使用列と空セルを落とさない。DBと外部サービス別に同じモデルのCSV・Markdown行列を生成する。縦持ちedge一覧は行列の代わりにしない。。
  - criterion(JSON Object): <code>{"given":"固定版の参照実装と導入先の実sourceがある","id":"AC-ASBUILT-024-2","then":"APIを行、資源を列、セルをC/R/U/D順の組合せとする行列を正規表示にする。全operationとDDL・外部資源台帳の全資源を母集合とし、未使用列と空セルを落とさない。DBと外部サービス別に同じモデルのCSV・Markdown行列を生成する。縦持ちedge一覧は行列の代わりにしない。","when":"lazunex基準のCRUDを表示する"}</code>
- <code>"AC-ASBUILT-024-3"</code> 前提: CRUD行列と補助関係図を生成する。条件: version付きモデルを射影する。期待結果: model v2ではAPIと資源のnodeを共有し、Rは資源からAPI、C/U/DはAPIから資源へ表示する。MarkdownはMermaid fenceを持ち、no_accessを架空資源へのNONE辺にせず理由として保持する。旧v1の縦持ち形式は明示した移行診断だけに残す。。
  - criterion(JSON Object): <code>{"given":"CRUD行列と補助関係図を生成する","id":"AC-ASBUILT-024-3","then":"model v2ではAPIと資源のnodeを共有し、Rは資源からAPI、C/U/DはAPIから資源へ表示する。MarkdownはMermaid fenceを持ち、no_accessを架空資源へのNONE辺にせず理由として保持する。旧v1の縦持ち形式は明示した移行診断だけに残す。","when":"version付きモデルを射影する"}</code>

要求源(JSON List): <code>["https://github.com/tsuji-tomonori/dev-standard/issues/67","user:2026-09-23-language-agnostic-adapters","user:2026-09-26-lazunex-authoritative"]</code>
検証方法: 言語非依存契約検査と導入先adapterの正例・負例検証
検証証跡: manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する
検証(JSON Object): <code>{"evidence":"manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する","method":"言語非依存契約検査と導入先adapterの正例・負例検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/scripts/check_design.py"]</code>
- テスト: <code>["tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-025: API帳票の所有階層

要件ID(JSON): <code>"REQ-ASBUILT-025"</code>
タイトル(JSON): <code>"API帳票の所有階層"</code>
主体(JSON): <code>"導入先repositoryのadapter"</code>
対象(JSON): <code>"group→API→帳票の階層と索引"</code>
導入先repositoryのadapterは、group→API→帳票の階層と索引を**検証する**。
行為enum: <code>"verify"</code>

根拠: API帳票の所有階層を明示的な契約にして欠落や推測による成功判定を防ぐ。
根拠(JSON): <code>"API帳票の所有階層を明示的な契約にして欠落や推測による成功判定を防ぐ。"</code>

項目版: 1 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"CHG-20260923-language-agnostic-adapters"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-ASBUILT-025-1"</code> 前提: 該当する実装surfaceとadapter manifestがある。条件: 導入先adapterの契約適合を検証する。期待結果: 全operationをgroup→API→6帳票の階層と索引に対応付け、旧生成物の残存・未索引帳票・link切れ・operation集合不一致を拒否する。
  - criterion(JSON Object): <code>{"given":"該当する実装surfaceとadapter manifestがある","id":"AC-ASBUILT-025-1","then":"全operationをgroup→API→6帳票の階層と索引に対応付け、旧生成物の残存・未索引帳票・link切れ・operation集合不一致を拒否する","when":"導入先adapterの契約適合を検証する"}</code>

要求源(JSON List): <code>["https://github.com/tsuji-tomonori/dev-standard/issues/67","user:2026-09-23-language-agnostic-adapters"]</code>
検証方法: 言語非依存契約検査と導入先adapterの正例・負例検証
検証証跡: manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する
検証(JSON Object): <code>{"evidence":"manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する","method":"言語非依存契約検査と導入先adapterの正例・負例検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/scripts/check_design.py"]</code>
- テスト: <code>["tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-026: 実順序によるシーケンス生成

要件ID(JSON): <code>"REQ-ASBUILT-026"</code>
タイトル(JSON): <code>"実順序によるシーケンス生成"</code>
主体(JSON): <code>"導入先repositoryのadapter"</code>
対象(JSON): <code>"実call graphの呼出順・条件・例外・transaction"</code>
導入先repositoryのadapterは、実call graphの呼出順・条件・例外・transactionを**検証する**。
行為enum: <code>"verify"</code>

根拠: 実順序によるシーケンス生成を明示的な契約にして欠落や推測による成功判定を防ぐ。
根拠(JSON): <code>"実順序によるシーケンス生成を明示的な契約にして欠落や推測による成功判定を防ぐ。"</code>

項目版: 3 / 状態: `active` / 種別: `functional`
変更識別子: <code>"CHG-20260926-lazunex-conformance"</code>
分類: scope=<code>"project"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-ASBUILT-026-1"</code> 前提: 該当する実装surfaceとadapter manifestがある。条件: 導入先adapterの契約適合を検証する。期待結果: 順序・分岐・反復・例外・transactionの実装変更を図へ反映し、保存先操作の矢印へ正本の目的を使用する。未解決callを明示し、存在しない処理や定型図での補完を成功扱いにしない。
  - criterion(JSON Object): <code>{"given":"該当する実装surfaceとadapter manifestがある","id":"AC-ASBUILT-026-1","then":"順序・分岐・反復・例外・transactionの実装変更を図へ反映し、保存先操作の矢印へ正本の目的を使用する。未解決callを明示し、存在しない処理や定型図での補完を成功扱いにしない","when":"導入先adapterの契約適合を検証する"}</code>
- <code>"AC-ASBUILT-026-2"</code> 前提: SQLを採用したoperationのシーケンスを生成する。条件: 保存先操作の矢印labelを導出する。期待結果: SQL正本に記述された操作目的の一文説明を矢印labelへ使用し、説明欠落を拒否する。説明言語は別指定がなければ日本語とし、SQL名や実行式だけを目的説明の代わりにしない。
  - criterion(JSON Object): <code>{"given":"SQLを採用したoperationのシーケンスを生成する","id":"AC-ASBUILT-026-2","then":"SQL正本に記述された操作目的の一文説明を矢印labelへ使用し、説明欠落を拒否する。説明言語は別指定がなければ日本語とし、SQL名や実行式だけを目的説明の代わりにしない","when":"保存先操作の矢印labelを導出する"}</code>
- <code>"AC-ASBUILT-026-3"</code> 前提: 固定版の参照実装と導入先の実sourceがある。条件: helper・callback・transaction境界がある実行flowを図示する。期待結果: 評価順・early return・認可・例外・commit/rollback・retryの実到達経路を保持する。補助関数やDB層の変更も図へ反映し、ast.walk等の単なる探索順、固定retry文、正常statusへの定型矢印で未解析部分を埋めない。。
  - criterion(JSON Object): <code>{"given":"固定版の参照実装と導入先の実sourceがある","id":"AC-ASBUILT-026-3","then":"評価順・early return・認可・例外・commit/rollback・retryの実到達経路を保持する。補助関数やDB層の変更も図へ反映し、ast.walk等の単なる探索順、固定retry文、正常statusへの定型矢印で未解析部分を埋めない。","when":"helper・callback・transaction境界がある実行flowを図示する"}</code>

要求源(JSON List): <code>["https://github.com/tsuji-tomonori/dev-standard/issues/69","user:2026-09-23-language-agnostic-adapters","user:2026-09-26-lazunex-authoritative"]</code>
検証方法: 言語非依存契約検査と導入先adapterの正例・負例検証
検証証跡: manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する
検証(JSON Object): <code>{"evidence":"manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する","method":"言語非依存契約検査と導入先adapterの正例・負例検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/SKILL.md"]</code>
- テスト: <code>["tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-027: 例外応答と運用ログの対応

要件ID(JSON): <code>"REQ-ASBUILT-027"</code>
タイトル(JSON): <code>"例外応答と運用ログの対応"</code>
主体(JSON): <code>"導入先repositoryのadapter"</code>
対象(JSON): <code>"例外型→捕捉/再送出→HTTP status/body→ログID/level/message/運用対応"</code>
導入先repositoryのadapterは、例外型→捕捉/再送出→HTTP status/body→ログID/level/message/運用対応を**検証する**。
行為enum: <code>"verify"</code>

根拠: 例外応答と運用ログの対応を明示的な契約にして欠落や推測による成功判定を防ぐ。
根拠(JSON): <code>"例外応答と運用ログの対応を明示的な契約にして欠落や推測による成功判定を防ぐ。"</code>

項目版: 3 / 状態: `active` / 種別: `functional`
変更識別子: <code>"CHG-20260926-lazunex-conformance"</code>
分類: scope=<code>"project"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-ASBUILT-027-1"</code> 前提: 該当する実装surfaceとadapter manifestがある。条件: 導入先adapterの契約適合を検証する。期待結果: 実行経路に沿って例外型、捕捉または再送出、HTTP status/body、ログID・level・message・運用対応を照合する。未知の動的応答や未対応catchは未検証として返す。
  - criterion(JSON Object): <code>{"given":"該当する実装surfaceとadapter manifestがある","id":"AC-ASBUILT-027-1","then":"実行経路に沿って例外型、捕捉または再送出、HTTP status/body、ログID・level・message・運用対応を照合する。未知の動的応答や未対応catchは未検証として返す","when":"導入先adapterの契約適合を検証する"}</code>
- <code>"AC-ASBUILT-027-2"</code> 前提: 該当する実装と選択profileがある。条件: 導入先adapterの正例と負例を検証する。期待結果: HTTP境界と内部捕捉の実logger呼出しを追跡し、応答status/bodyとログcatalogのID・型・運用対応の一致を正例と負例で検証する。実装にないログ呼出しを帳票へ補完しない。
  - criterion(JSON Object): <code>{"given":"該当する実装と選択profileがある","id":"AC-ASBUILT-027-2","then":"HTTP境界と内部捕捉の実logger呼出しを追跡し、応答status/bodyとログcatalogのID・型・運用対応の一致を正例と負例で検証する。実装にないログ呼出しを帳票へ補完しない","when":"導入先adapterの正例と負例を検証する"}</code>
- <code>"AC-ASBUILT-027-3"</code> 前提: 固定版の参照実装と導入先の実sourceがある。条件: message帳票を実loggerと照合する。期待結果: 実出力箇所に結び付いた安定message ID、level、発生条件、項目型、マスク、運用対応と応答変換を表示する。request結果の共通ログだけで個別異常のcatalogを満たしたとせず、公開された共通statusと各operationで実到達するstatusを区別する。。
  - criterion(JSON Object): <code>{"given":"固定版の参照実装と導入先の実sourceがある","id":"AC-ASBUILT-027-3","then":"実出力箇所に結び付いた安定message ID、level、発生条件、項目型、マスク、運用対応と応答変換を表示する。request結果の共通ログだけで個別異常のcatalogを満たしたとせず、公開された共通statusと各operationで実到達するstatusを区別する。","when":"message帳票を実loggerと照合する"}</code>

要求源(JSON List): <code>["https://github.com/tsuji-tomonori/dev-standard/issues/70","user:2026-09-23-language-agnostic-adapters","user:2026-09-26-lazunex-authoritative"]</code>
検証方法: 言語非依存契約検査と導入先adapterの正例・負例検証
検証証跡: manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する
検証(JSON Object): <code>{"evidence":"manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する","method":"言語非依存契約検査と導入先adapterの正例・負例検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/SKILL.md"]</code>
- テスト: <code>["tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-028: 自然言語の検証単位

要件ID(JSON): <code>"REQ-ASBUILT-028"</code>
タイトル(JSON): <code>"自然言語の検証単位"</code>
主体(JSON): <code>"導入先repositoryのadapter"</code>
対象(JSON): <code>"実在testへ対応する具体的Given/When/Then"</code>
導入先repositoryのadapterは、実在testへ対応する具体的Given/When/Thenを**検証する**。
行為enum: <code>"verify"</code>

根拠: 自然言語の検証単位を明示的な契約にして欠落や推測による成功判定を防ぐ。
根拠(JSON): <code>"自然言語の検証単位を明示的な契約にして欠落や推測による成功判定を防ぐ。"</code>

項目版: 3 / 状態: `active` / 種別: `functional`
変更識別子: <code>"CHG-20260926-lazunex-conformance"</code>
分類: scope=<code>"project"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-ASBUILT-028-1"</code> 前提: 該当する実装surfaceとadapter manifestがある。条件: 導入先adapterの契約適合を検証する。期待結果: 認証・入力制約・分岐・例外から導出した必須要因と要素ごとに前提・操作・期待結果を自然言語で記述し、実在test識別子へ対応付ける。必要な期待ログとDB状態を含め、未対応要因を拒否する。
  - criterion(JSON Object): <code>{"given":"該当する実装surfaceとadapter manifestがある","id":"AC-ASBUILT-028-1","then":"認証・入力制約・分岐・例外から導出した必須要因と要素ごとに前提・操作・期待結果を自然言語で記述し、実在test識別子へ対応付ける。必要な期待ログとDB状態を含め、未対応要因を拒否する","when":"導入先adapterの契約適合を検証する"}</code>
- <code>"AC-ASBUILT-028-2"</code> 前提: 該当する実装と選択profileがある。条件: 導入先adapterの正例と負例を検証する。期待結果: 実test collectorの各検証単位に対応する自然言語Given/When/Thenの欠落・重複を拒否する。式やfixture名だけを説明の代わりにせず、既定の説明言語で前提・操作・期待結果を読むことができる。
  - criterion(JSON Object): <code>{"given":"該当する実装と選択profileがある","id":"AC-ASBUILT-028-2","then":"実test collectorの各検証単位に対応する自然言語Given/When/Thenの欠落・重複を拒否する。式やfixture名だけを説明の代わりにせず、既定の説明言語で前提・操作・期待結果を読むことができる","when":"導入先adapterの正例と負例を検証する"}</code>
- <code>"AC-ASBUILT-028-3"</code> 前提: 固定版の参照実装と導入先の実sourceがある。条件: 要因と組合せを実検証単位へ対応させる。期待結果: 条件の成立/不成立、入力境界、例外・暗黙認証から得た個別要因/要素、到達する組合せ、期待ログ・状態・応答を実collectorのparametrize後のIDへ対応させる。汎用の一要因、test関数名の拾い読み、describe名だけで要因とassertの網羅を主張しない。。
  - criterion(JSON Object): <code>{"given":"固定版の参照実装と導入先の実sourceがある","id":"AC-ASBUILT-028-3","then":"条件の成立/不成立、入力境界、例外・暗黙認証から得た個別要因/要素、到達する組合せ、期待ログ・状態・応答を実collectorのparametrize後のIDへ対応させる。汎用の一要因、test関数名の拾い読み、describe名だけで要因とassertの網羅を主張しない。","when":"要因と組合せを実検証単位へ対応させる"}</code>

要求源(JSON List): <code>["https://github.com/tsuji-tomonori/dev-standard/issues/70","user:2026-09-23-language-agnostic-adapters","user:2026-09-26-lazunex-authoritative"]</code>
検証方法: 言語非依存契約検査と導入先adapterの正例・負例検証
検証証跡: manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する
検証(JSON Object): <code>{"evidence":"manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する","method":"言語非依存契約検査と導入先adapterの正例・負例検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/SKILL.md"]</code>
- テスト: <code>["tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-029: adapter manifestの完全性

要件ID(JSON): <code>"REQ-ASBUILT-029"</code>
タイトル(JSON): <code>"adapter manifestの完全性"</code>
主体(JSON): <code>"導入先repositoryのadapter"</code>
対象(JSON): <code>"capabilityごとの生成command・check command・出力root・要件ID・棚卸しリンク"</code>
導入先repositoryのadapterは、capabilityごとの生成command・check command・出力root・要件ID・棚卸しリンクを**検証する**。
行為enum: <code>"verify"</code>

根拠: adapter manifestの完全性を明示的な契約にして欠落や推測による成功判定を防ぐ。
根拠(JSON): <code>"adapter manifestの完全性を明示的な契約にして欠落や推測による成功判定を防ぐ。"</code>

項目版: 2 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"CHG-20260926-lazunex-conformance"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-ASBUILT-029-1"</code> 前提: 該当する実装surfaceとadapter manifestがある。条件: 導入先adapterの契約適合を検証する。期待結果: manifestの存在とschema適合を要求し、各capabilityに生成command、検査command、出力root、対応active要件ID、参照棚卸しリンクを宣言する。非該当は実装が存在しない理由を記録し、適用要件集合の未知・inactive・未mapping・余剰を拒否する。
  - criterion(JSON Object): <code>{"given":"該当する実装surfaceとadapter manifestがある","id":"AC-ASBUILT-029-1","then":"manifestの存在とschema適合を要求し、各capabilityに生成command、検査command、出力root、対応active要件ID、参照棚卸しリンクを宣言する。非該当は実装が存在しない理由を記録し、適用要件集合の未知・inactive・未mapping・余剰を拒否する","when":"導入先adapterの契約適合を検証する"}</code>
- <code>"AC-ASBUILT-029-2"</code> 前提: 固定版の参照実装と導入先の実sourceがある。条件: 参照API profileを初回導入または更新する。期待結果: 通常の完了判定にはschema v3の参照適合mappingと意味検査commandを接続する。schema v2の旧帳票診断はlegacy-layout-onlyとして明示し、参照適合・実装完了とは表示しない。v3からlegacyへの検査迂回を拒否する。。
  - criterion(JSON Object): <code>{"given":"固定版の参照実装と導入先の実sourceがある","id":"AC-ASBUILT-029-2","then":"通常の完了判定にはschema v3の参照適合mappingと意味検査commandを接続する。schema v2の旧帳票診断はlegacy-layout-onlyとして明示し、参照適合・実装完了とは表示しない。v3からlegacyへの検査迂回を拒否する。","when":"参照API profileを初回導入または更新する"}</code>

要求源(JSON List): <code>["https://github.com/tsuji-tomonori/dev-standard/issues/72","user:2026-09-23-language-agnostic-adapters","user:2026-09-26-lazunex-authoritative"]</code>
検証方法: 言語非依存契約検査と導入先adapterの正例・負例検証
検証証跡: manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する
検証(JSON Object): <code>{"evidence":"manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する","method":"言語非依存契約検査と導入先adapterの正例・負例検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/scripts/check_design.py"]</code>
- テスト: <code>["tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-030: 参照tools全件棚卸し

要件ID(JSON): <code>"REQ-ASBUILT-030"</code>
タイトル(JSON): <code>"参照tools全件棚卸し"</code>
主体(JSON): <code>"導入先repositoryのadapter"</code>
対象(JSON): <code>"固定revisionの全file用途と採用判断および実接続先"</code>
導入先repositoryのadapterは、固定revisionの全file用途と採用判断および実接続先を**検証する**。
行為enum: <code>"verify"</code>

根拠: 参照tools全件棚卸しを明示的な契約にして欠落や推測による成功判定を防ぐ。
根拠(JSON): <code>"参照tools全件棚卸しを明示的な契約にして欠落や推測による成功判定を防ぐ。"</code>

項目版: 2 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"CHG-20260926-lazunex-conformance"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-ASBUILT-030-1"</code> 前提: 該当する実装surfaceとadapter manifestがある。条件: 導入先adapterの契約適合を検証する。期待結果: 選んだ参照実装の固定commit SHAと全file一覧を記録し、各fileのpath・blob SHAまたはSHA-256・用途・分類・要件ID・adopt/adapt/extend/not-adopted・理由・言語固有前提・導入先の実接続先を保持する。非採用にも具体的理由を要求する。
  - criterion(JSON Object): <code>{"given":"該当する実装surfaceとadapter manifestがある","id":"AC-ASBUILT-030-1","then":"選んだ参照実装の固定commit SHAと全file一覧を記録し、各fileのpath・blob SHAまたはSHA-256・用途・分類・要件ID・adopt/adapt/extend/not-adopted・理由・言語固有前提・導入先の実接続先を保持する。非採用にも具体的理由を要求する","when":"導入先adapterの契約適合を検証する"}</code>
- <code>"AC-ASBUILT-030-2"</code> 前提: 固定版の参照実装と導入先の実sourceがある。条件: 参照を選択して導入先へ適用する。期待結果: 利用者が正と指定したrepositoryと固定SHAを主参照として保持し、その全tools集合を照合する。KotoRelay等の二次参照は補助として追加できるが、主参照の台帳を二次参照だけで置換しない。参照変更は要件の明示変更として扱う。。
  - criterion(JSON Object): <code>{"given":"固定版の参照実装と導入先の実sourceがある","id":"AC-ASBUILT-030-2","then":"利用者が正と指定したrepositoryと固定SHAを主参照として保持し、その全tools集合を照合する。KotoRelay等の二次参照は補助として追加できるが、主参照の台帳を二次参照だけで置換しない。参照変更は要件の明示変更として扱う。","when":"参照を選択して導入先へ適用する"}</code>

要求源(JSON List): <code>["https://github.com/tsuji-tomonori/dev-standard/issues/72","user:2026-09-23-language-agnostic-adapters","user:2026-09-26-lazunex-authoritative"]</code>
検証方法: 言語非依存契約検査と導入先adapterの正例・負例検証
検証証跡: manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する
検証(JSON Object): <code>{"evidence":"manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する","method":"言語非依存契約検査と導入先adapterの正例・負例検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/adapter-contract.md",".agents/skills/generate-implementation-design/assets/reference-inventory.schema.json"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/scripts/reference_inventory.py"]</code>
- テスト: <code>["tests/test_reference_inventory.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-031: 検証報告の分離

要件ID(JSON): <code>"REQ-ASBUILT-031"</code>
タイトル(JSON): <code>"検証報告の分離"</code>
主体(JSON): <code>"導入先repositoryのadapter"</code>
対象(JSON): <code>"構成適合・設計drift・実行test・未検証範囲の独立した報告"</code>
導入先repositoryのadapterは、構成適合・設計drift・実行test・未検証範囲の独立した報告を**検証する**。
行為enum: <code>"verify"</code>

根拠: 検証報告の分離を明示的な契約にして欠落や推測による成功判定を防ぐ。
根拠(JSON): <code>"検証報告の分離を明示的な契約にして欠落や推測による成功判定を防ぐ。"</code>

項目版: 2 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"CHG-20260926-lazunex-conformance"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-ASBUILT-031-1"</code> 前提: 該当する実装surfaceとadapter manifestがある。条件: 導入先adapterの契約適合を検証する。期待結果: 構成適合、設計drift、実行テスト、未検証範囲を分けて報告する。章の存在やcheck commandの成功から、実行テスト成功または意味解析の完全性を推定しない。
  - criterion(JSON Object): <code>{"given":"該当する実装surfaceとadapter manifestがある","id":"AC-ASBUILT-031-1","then":"構成適合、設計drift、実行テスト、未検証範囲を分けて報告する。章の存在やcheck commandの成功から、実行テスト成功または意味解析の完全性を推定しない","when":"導入先adapterの契約適合を検証する"}</code>
- <code>"AC-ASBUILT-031-2"</code> 前提: 固定版の参照実装と導入先の実sourceがある。条件: 適合結果を集約する。期待結果: 構成・drift・新規実行した参照適合・業務実行テスト・適用外/未検証を分ける。generatorの定数passや過去のreport、test pathが存在することだけから意味検査または業務テストの成功を推論しない。Advisoryの未実行/失敗は必須検査の成功へ混ぜず、閾値を無条件blockingへ昇格しない。。
  - criterion(JSON Object): <code>{"given":"固定版の参照実装と導入先の実sourceがある","id":"AC-ASBUILT-031-2","then":"構成・drift・新規実行した参照適合・業務実行テスト・適用外/未検証を分ける。generatorの定数passや過去のreport、test pathが存在することだけから意味検査または業務テストの成功を推論しない。Advisoryの未実行/失敗は必須検査の成功へ混ぜず、閾値を無条件blockingへ昇格しない。","when":"適合結果を集約する"}</code>

要求源(JSON List): <code>["https://github.com/tsuji-tomonori/dev-standard/issues/70","user:2026-09-23-language-agnostic-adapters","user:2026-09-26-lazunex-authoritative"]</code>
検証方法: 言語非依存契約検査と導入先adapterの正例・負例検証
検証証跡: manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する
検証(JSON Object): <code>{"evidence":"manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する","method":"言語非依存契約検査と導入先adapterの正例・負例検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/scripts/check_design.py",".agents/skills/inspect-quality-gates/SKILL.md"]</code>
- テスト: <code>["tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-032: 未対応surfaceの未完了判定

要件ID(JSON): <code>"REQ-ASBUILT-032"</code>
タイトル(JSON): <code>"未対応surfaceの未完了判定"</code>
主体(JSON): <code>"導入先repositoryのadapter"</code>
対象(JSON): <code>"path・理由・support statusを持つ未対応surface"</code>
導入先repositoryのadapterは、path・理由・support statusを持つ未対応surfaceを**検証する**。
行為enum: <code>"verify"</code>

根拠: 未対応surfaceの未完了判定を明示的な契約にして欠落や推測による成功判定を防ぐ。
根拠(JSON): <code>"未対応surfaceの未完了判定を明示的な契約にして欠落や推測による成功判定を防ぐ。"</code>

項目版: 2 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"CHG-20260926-lazunex-conformance"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-ASBUILT-032-1"</code> 前提: 該当する実装surfaceとadapter manifestがある。条件: 導入先adapterの契約適合を検証する。期待結果: 未対応surfaceをpath・理由・support status付きで報告し、未対応構文のdiagnosticには位置と構文種別を含める。導入先adapterで補完するまで必要surfaceを未完了とし、成功または非該当に読み替えない。
  - criterion(JSON Object): <code>{"given":"該当する実装surfaceとadapter manifestがある","id":"AC-ASBUILT-032-1","then":"未対応surfaceをpath・理由・support status付きで報告し、未対応構文のdiagnosticには位置と構文種別を含める。導入先adapterで補完するまで必要surfaceを未完了とし、成功または非該当に読み替えない","when":"導入先adapterの契約適合を検証する"}</code>
- <code>"AC-ASBUILT-032-2"</code> 前提: 固定版の参照実装と導入先の実sourceがある。条件: 解析対象sourceを分類する。期待結果: 公開登録だけでなく全sourceから定義・呼出し・SQL・provider・test集合を独立に列挙して照合する。新規helper、alias、入れ子、非同期、未登録endpoint、未解決外部readを省略せず、unsupportedを空配列やアクセスなしへ固定する実装を負例で検出する。。
  - criterion(JSON Object): <code>{"given":"固定版の参照実装と導入先の実sourceがある","id":"AC-ASBUILT-032-2","then":"公開登録だけでなく全sourceから定義・呼出し・SQL・provider・test集合を独立に列挙して照合する。新規helper、alias、入れ子、非同期、未登録endpoint、未解決外部readを省略せず、unsupportedを空配列やアクセスなしへ固定する実装を負例で検出する。","when":"解析対象sourceを分類する"}</code>

要求源(JSON List): <code>["https://github.com/tsuji-tomonori/dev-standard/issues/72","user:2026-09-23-language-agnostic-adapters","user:2026-09-26-lazunex-authoritative"]</code>
検証方法: 言語非依存契約検査と導入先adapterの正例・負例検証
検証証跡: manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する
検証(JSON Object): <code>{"evidence":"manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する","method":"言語非依存契約検査と導入先adapterの正例・負例検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/scripts/check_design.py"]</code>
- テスト: <code>["tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-033: 正常status内の失敗経路

要件ID(JSON): <code>"REQ-ASBUILT-033"</code>
タイトル(JSON): <code>"正常status内の失敗経路"</code>
主体(JSON): <code>"導入先repositoryのadapter"</code>
対象(JSON): <code>"内部捕捉後に正常HTTP statusの失敗結果へ変換する実経路"</code>
導入先repositoryのadapterは、内部捕捉後に正常HTTP statusの失敗結果へ変換する実経路を**検証する**。
行為enum: <code>"verify"</code>

根拠: 正常status内の失敗経路を明示的な契約にして欠落や推測による成功判定を防ぐ。
根拠(JSON): <code>"正常status内の失敗経路を明示的な契約にして欠落や推測による成功判定を防ぐ。"</code>

項目版: 1 / 状態: `active` / 種別: `functional`
変更識別子: <code>"CHG-20260923-language-agnostic-adapters"</code>
分類: scope=<code>"project"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-ASBUILT-033-1"</code> 前提: 該当する実装surfaceとadapter manifestがある。条件: 導入先adapterの契約適合を検証する。期待結果: 内部捕捉後に200/201等の正常statusで失敗結果を返す経路とworker継続条件を保持して文書化する。例外が常にHTTP異常statusへ至ると推定しない。
  - criterion(JSON Object): <code>{"given":"該当する実装surfaceとadapter manifestがある","id":"AC-ASBUILT-033-1","then":"内部捕捉後に200/201等の正常statusで失敗結果を返す経路とworker継続条件を保持して文書化する。例外が常にHTTP異常statusへ至ると推定しない","when":"導入先adapterの契約適合を検証する"}</code>

要求源(JSON List): <code>["https://github.com/tsuji-tomonori/dev-standard/issues/70","user:2026-09-23-language-agnostic-adapters"]</code>
検証方法: 言語非依存契約検査と導入先adapterの正例・負例検証
検証証跡: manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する
検証(JSON Object): <code>{"evidence":"manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する","method":"言語非依存契約検査と導入先adapterの正例・負例検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/SKILL.md"]</code>
- テスト: <code>["tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-034: 棚卸しの網羅照合

要件ID(JSON): <code>"REQ-ASBUILT-034"</code>
タイトル(JSON): <code>"棚卸しの網羅照合"</code>
主体(JSON): <code>"導入先repositoryのadapter"</code>
対象(JSON): <code>"一意な全file集合と要件へのtoolまたは明示gap対応"</code>
導入先repositoryのadapterは、一意な全file集合と要件へのtoolまたは明示gap対応を**検証する**。
行為enum: <code>"verify"</code>

根拠: 棚卸しの網羅照合を明示的な契約にして欠落や推測による成功判定を防ぐ。
根拠(JSON): <code>"棚卸しの網羅照合を明示的な契約にして欠落や推測による成功判定を防ぐ。"</code>

項目版: 2 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"CHG-20260926-lazunex-conformance"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-ASBUILT-034-1"</code> 前提: 該当する実装surfaceとadapter manifestがある。条件: 導入先adapterの契約適合を検証する。期待結果: 固定された件数・path一意性・digest・要件ID実在を検証し、宣言した全適用要件がいずれかのtoolまたは理由付きgapへ対応することを照合する。任意の参照root再照合で欠落・余剰・SHA不一致を拒否し、人向け表をJSONから決定的に生成する。
  - criterion(JSON Object): <code>{"given":"該当する実装surfaceとadapter manifestがある","id":"AC-ASBUILT-034-1","then":"固定された件数・path一意性・digest・要件ID実在を検証し、宣言した全適用要件がいずれかのtoolまたは理由付きgapへ対応することを照合する。任意の参照root再照合で欠落・余剰・SHA不一致を拒否し、人向け表をJSONから決定的に生成する","when":"導入先adapterの契約適合を検証する"}</code>
- <code>"AC-ASBUILT-034-2"</code> 前提: 固定版の参照実装と導入先の実sourceがある。条件: tools棚卸しの接続先を評価する。期待結果: 同じ大きなgeneratorとtest fileを全行に記入しただけで採用済みと判定しない。各参照要件を満たす実解析・出力・正例/負例のcollector IDへ対応し、宣言したpath/blob集合を主参照の固定全件集合と照合する。。
  - criterion(JSON Object): <code>{"given":"固定版の参照実装と導入先の実sourceがある","id":"AC-ASBUILT-034-2","then":"同じ大きなgeneratorとtest fileを全行に記入しただけで採用済みと判定しない。各参照要件を満たす実解析・出力・正例/負例のcollector IDへ対応し、宣言したpath/blob集合を主参照の固定全件集合と照合する。","when":"tools棚卸しの接続先を評価する"}</code>

要求源(JSON List): <code>["https://github.com/tsuji-tomonori/dev-standard/issues/72","user:2026-09-23-language-agnostic-adapters","user:2026-09-26-lazunex-authoritative"]</code>
検証方法: 言語非依存契約検査と導入先adapterの正例・負例検証
検証証跡: manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する
検証(JSON Object): <code>{"evidence":"manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する","method":"言語非依存契約検査と導入先adapterの正例・負例検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/adapter-contract.md",".agents/skills/generate-implementation-design/assets/reference-inventory.schema.json"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/scripts/reference_inventory.py"]</code>
- テスト: <code>["tests/test_reference_inventory.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-035: 生成出力の所有境界

要件ID(JSON): <code>"REQ-ASBUILT-035"</code>
タイトル(JSON): <code>"生成出力の所有境界"</code>
主体(JSON): <code>"導入先repositoryのadapter"</code>
対象(JSON): <code>"generatorが完全所有するrootと明示出力集合"</code>
導入先repositoryのadapterは、generatorが完全所有するrootと明示出力集合を**検証する**。
行為enum: <code>"verify"</code>

根拠: 生成出力の所有境界を明示的な契約にして欠落や推測による成功判定を防ぐ。
根拠(JSON): <code>"生成出力の所有境界を明示的な契約にして欠落や推測による成功判定を防ぐ。"</code>

項目版: 2 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"CHG-20260923-independent-review-fixes"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-ASBUILT-035-1"</code> 前提: 該当する実装surfaceとadapter manifestがある。条件: 導入先adapterの契約適合を検証する。期待結果: symlink、root間の重複、directory置換、管理外pathと未宣言の出力を拒否する。生成を2回実行してbyte一致を検証し、checkが既存生成物を変更した場合は失敗とする。
  - criterion(JSON Object): <code>{"given":"該当する実装surfaceとadapter manifestがある","id":"AC-ASBUILT-035-1","then":"symlink、root間の重複、directory置換、管理外pathと未宣言の出力を拒否する。生成を2回実行してbyte一致を検証し、checkが既存生成物を変更した場合は失敗とする","when":"導入先adapterの契約適合を検証する"}</code>
- <code>"AC-ASBUILT-035-2"</code> 前提: 該当する実装と選択profileがある。条件: 導入先adapterの正例と負例を検証する。期待結果: 作業用コピーで非破壊checkの後、所有出力を毎回空にしてクリーン生成を2回行う。各回の生成集合とbyteを既存出力へ照合し、manifestと既存出力に残るがgeneratorの対象から削除されたfileも拒否する。
  - criterion(JSON Object): <code>{"given":"該当する実装と選択profileがある","id":"AC-ASBUILT-035-2","then":"作業用コピーで非破壊checkの後、所有出力を毎回空にしてクリーン生成を2回行う。各回の生成集合とbyteを既存出力へ照合し、manifestと既存出力に残るがgeneratorの対象から削除されたfileも拒否する","when":"導入先adapterの正例と負例を検証する"}</code>

要求源(JSON List): <code>["https://github.com/tsuji-tomonori/dev-standard/issues/72","user:2026-09-23-language-agnostic-adapters"]</code>
検証方法: 言語非依存契約検査と導入先adapterの正例・負例検証
検証証跡: manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する
検証(JSON Object): <code>{"evidence":"manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する","method":"言語非依存契約検査と導入先adapterの正例・負例検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/scripts/check_design.py"]</code>
- テスト: <code>["tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DESIGN-008: operationの単一所有

要件ID(JSON): <code>"REQ-DESIGN-008"</code>
タイトル(JSON): <code>"operationの単一所有"</code>
主体(JSON): <code>"導入先repositoryのadapter"</code>
対象(JSON): <code>"1 operation 1 所有単位"</code>
導入先repositoryのadapterは、1 operation 1 所有単位を**検証する**。
行為enum: <code>"verify"</code>

根拠: operationの単一所有を明示的な契約にして欠落や推測による成功判定を防ぐ。
根拠(JSON): <code>"operationの単一所有を明示的な契約にして欠落や推測による成功判定を防ぐ。"</code>

項目版: 1 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"CHG-20260923-language-agnostic-adapters"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-DESIGN-008-1"</code> 前提: 該当する実装surfaceとadapter manifestがある。条件: 導入先adapterの契約適合を検証する。期待結果: 選択profileのoperation粒度で公開operationと所有単位を1対1に照合し、重複所有・所有欠落・無関係operationの集約を拒否する。
  - criterion(JSON Object): <code>{"given":"該当する実装surfaceとadapter manifestがある","id":"AC-DESIGN-008-1","then":"選択profileのoperation粒度で公開operationと所有単位を1対1に照合し、重複所有・所有欠落・無関係operationの集約を拒否する","when":"導入先adapterの契約適合を検証する"}</code>

要求源(JSON List): <code>["https://github.com/tsuji-tomonori/dev-standard/issues/68","user:2026-09-23-language-agnostic-adapters"]</code>
検証方法: 言語非依存契約検査と導入先adapterの正例・負例検証
検証証跡: manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する
検証(JSON Object): <code>{"evidence":"manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する","method":"言語非依存契約検査と導入先adapterの正例・負例検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/SKILL.md"]</code>
- テスト: <code>["tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DESIGN-009: 責務の実接続

要件ID(JSON): <code>"REQ-DESIGN-009"</code>
タイトル(JSON): <code>"責務の実接続"</code>
主体(JSON): <code>"導入先repositoryのadapter"</code>
対象(JSON): <code>"endpoint・個別処理・query・応答組立・schema・contract・sampleの実参照"</code>
導入先repositoryのadapterは、endpoint・個別処理・query・応答組立・schema・contract・sampleの実参照を**検証する**。
行為enum: <code>"verify"</code>

根拠: 責務の実接続を明示的な契約にして欠落や推測による成功判定を防ぐ。
根拠(JSON): <code>"責務の実接続を明示的な契約にして欠落や推測による成功判定を防ぐ。"</code>

項目版: 3 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"CHG-20260926-lazunex-conformance"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-DESIGN-009-1"</code> 前提: 該当する実装surfaceとadapter manifestがある。条件: 導入先adapterの契約適合を検証する。期待結果: 責務間の実callまたは実参照を検査し、空file・未使用import・コメントだけの宣言・未参照処理・古い集約実装への単純委譲を適合としない。静的解決不能は未検証にする。
  - criterion(JSON Object): <code>{"given":"該当する実装surfaceとadapter manifestがある","id":"AC-DESIGN-009-1","then":"責務間の実callまたは実参照を検査し、空file・未使用import・コメントだけの宣言・未参照処理・古い集約実装への単純委譲を適合としない。静的解決不能は未検証にする","when":"導入先adapterの契約適合を検証する"}</code>
- <code>"AC-DESIGN-009-2"</code> 前提: 該当する実装と選択profileがある。条件: 導入先adapterの正例と負例を検証する。期待結果: endpointから個別処理・所有query・入力応答型・応答builder・contract・sampleへの実接続を照合する。応答builderを定義またはimportしただけで呼ばない負例、空の必須責務、未参照contract/sample、旧集約処理への単純委譲を拒否する。
  - criterion(JSON Object): <code>{"given":"該当する実装と選択profileがある","id":"AC-DESIGN-009-2","then":"endpointから個別処理・所有query・入力応答型・応答builder・contract・sampleへの実接続を照合する。応答builderを定義またはimportしただけで呼ばない負例、空の必須責務、未参照contract/sample、旧集約処理への単純委譲を拒否する","when":"導入先adapterの正例と負例を検証する"}</code>
- <code>"AC-DESIGN-009-3"</code> 前提: 固定版の参照実装と導入先の実sourceがある。条件: operation所有を具体化する。期待結果: 入力/応答型・契約・sample・応答組立・業務処理・生成queryの所有と実参照を追跡する。全API固有型を共有domainへ集約する場合や生成物を手書き処理に混在させる場合は責務ごとの差分と理由を明記する。ファイル数だけを合わせた空実装は拒否する。。
  - criterion(JSON Object): <code>{"given":"固定版の参照実装と導入先の実sourceがある","id":"AC-DESIGN-009-3","then":"入力/応答型・契約・sample・応答組立・業務処理・生成queryの所有と実参照を追跡する。全API固有型を共有domainへ集約する場合や生成物を手書き処理に混在させる場合は責務ごとの差分と理由を明記する。ファイル数だけを合わせた空実装は拒否する。","when":"operation所有を具体化する"}</code>

要求源(JSON List): <code>["https://github.com/tsuji-tomonori/dev-standard/issues/68","user:2026-09-23-language-agnostic-adapters","user:2026-09-26-lazunex-authoritative"]</code>
検証方法: 言語非依存契約検査と導入先adapterの正例・負例検証
検証証跡: manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する
検証(JSON Object): <code>{"evidence":"manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する","method":"言語非依存契約検査と導入先adapterの正例・負例検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/SKILL.md"]</code>
- テスト: <code>["tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DESIGN-010: 共有責務の所有者

要件ID(JSON): <code>"REQ-DESIGN-010"</code>
タイトル(JSON): <code>"共有責務の所有者"</code>
主体(JSON): <code>"導入先repositoryのadapter"</code>
対象(JSON): <code>"明示された共有責務の所有者と依存方向"</code>
導入先repositoryのadapterは、明示された共有責務の所有者と依存方向を**検証する**。
行為enum: <code>"verify"</code>

根拠: 共有責務の所有者を明示的な契約にして欠落や推測による成功判定を防ぐ。
根拠(JSON): <code>"共有責務の所有者を明示的な契約にして欠落や推測による成功判定を防ぐ。"</code>

項目版: 1 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"CHG-20260923-language-agnostic-adapters"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-DESIGN-010-1"</code> 前提: 該当する実装surfaceとadapter manifestがある。条件: 導入先adapterの契約適合を検証する。期待結果: 共有責務ごとに所有者と許容する依存方向を明示し、未宣言の共有化および共有責務からAPIへの逆依存を拒否する。
  - criterion(JSON Object): <code>{"given":"該当する実装surfaceとadapter manifestがある","id":"AC-DESIGN-010-1","then":"共有責務ごとに所有者と許容する依存方向を明示し、未宣言の共有化および共有責務からAPIへの逆依存を拒否する","when":"導入先adapterの契約適合を検証する"}</code>

要求源(JSON List): <code>["https://github.com/tsuji-tomonori/dev-standard/issues/68","user:2026-09-23-language-agnostic-adapters"]</code>
検証方法: 言語非依存契約検査と導入先adapterの正例・負例検証
検証証跡: manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する
検証(JSON Object): <code>{"evidence":"manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する","method":"言語非依存契約検査と導入先adapterの正例・負例検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/SKILL.md"]</code>
- テスト: <code>["tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DESIGN-011: endpointの全体フロー責務

要件ID(JSON): <code>"REQ-DESIGN-011"</code>
タイトル(JSON): <code>"endpointの全体フロー責務"</code>
主体(JSON): <code>"導入先repositoryのadapter"</code>
対象(JSON): <code>"endpoint層が所有する順序・分岐・反復・例外・transaction"</code>
導入先repositoryのadapterは、endpoint層が所有する順序・分岐・反復・例外・transactionを**検証する**。
行為enum: <code>"verify"</code>

根拠: endpointの全体フロー責務を明示的な契約にして欠落や推測による成功判定を防ぐ。
根拠(JSON): <code>"endpointの全体フロー責務を明示的な契約にして欠落や推測による成功判定を防ぐ。"</code>

項目版: 2 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"CHG-20260926-lazunex-conformance"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-DESIGN-011-1"</code> 前提: 該当する実装surfaceとadapter manifestがある。条件: 導入先adapterの契約適合を検証する。期待結果: endpoint層の全体flowが個別処理へ逆流する呼出し、個別処理内のoperation transaction、endpoint層からDB/providerへの直接I/O呼出しを検出する。非同期workerにも同じ責務境界を適用する。
  - criterion(JSON Object): <code>{"given":"該当する実装surfaceとadapter manifestがある","id":"AC-DESIGN-011-1","then":"endpoint層の全体flowが個別処理へ逆流する呼出し、個別処理内のoperation transaction、endpoint層からDB/providerへの直接I/O呼出しを検出する。非同期workerにも同じ責務境界を適用する","when":"導入先adapterの契約適合を検証する"}</code>
- <code>"AC-DESIGN-011-2"</code> 前提: 固定版の参照実装と導入先の実sourceがある。条件: endpointから呼ぶ保存先操作を評価する。期待結果: query wrapperもDB access境界とみなし、endpoint内の入れ子callbackやalias経由を含め直接呼出しを拒否する。transaction実行helperが共有であってもoperationの順序と成功応答時点をendpoint側から追跡できるようにする。参照のframework名や固定retry回数は移植しない。。
  - criterion(JSON Object): <code>{"given":"固定版の参照実装と導入先の実sourceがある","id":"AC-DESIGN-011-2","then":"query wrapperもDB access境界とみなし、endpoint内の入れ子callbackやalias経由を含め直接呼出しを拒否する。transaction実行helperが共有であってもoperationの順序と成功応答時点をendpoint側から追跡できるようにする。参照のframework名や固定retry回数は移植しない。","when":"endpointから呼ぶ保存先操作を評価する"}</code>

要求源(JSON List): <code>["https://github.com/tsuji-tomonori/dev-standard/issues/69","user:2026-09-23-language-agnostic-adapters","user:2026-09-26-lazunex-authoritative"]</code>
検証方法: 言語非依存契約検査と導入先adapterの正例・負例検証
検証証跡: manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する
検証(JSON Object): <code>{"evidence":"manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する","method":"言語非依存契約検査と導入先adapterの正例・負例検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/SKILL.md"]</code>
- テスト: <code>["tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DESIGN-012: SQLごとの厳格な引数型

要件ID(JSON): <code>"REQ-DESIGN-012"</code>
タイトル(JSON): <code>"SQLごとの厳格な引数型"</code>
主体(JSON): <code>"導入先repositoryのadapter"</code>
対象(JSON): <code>"各SQLの束縛引数だけを表す専用型"</code>
導入先repositoryのadapterは、各SQLの束縛引数だけを表す専用型を**検証する**。
行為enum: <code>"verify"</code>

根拠: SQLごとの厳格な引数型を明示的な契約にして欠落や推測による成功判定を防ぐ。
根拠(JSON): <code>"SQLごとの厳格な引数型を明示的な契約にして欠落や推測による成功判定を防ぐ。"</code>

項目版: 1 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"CHG-20260923-language-agnostic-adapters"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-DESIGN-012-1"</code> 前提: 該当する実装surfaceとadapter manifestがある。条件: 導入先adapterの契約適合を検証する。期待結果: 各SQLの実際の束縛引数から専用型を生成し、余剰引数・型・NULL不一致を拒否する。未対応構文を汎用型で補完せず、SQL変更時の生成driftを検出する。
  - criterion(JSON Object): <code>{"given":"該当する実装surfaceとadapter manifestがある","id":"AC-DESIGN-012-1","then":"各SQLの実際の束縛引数から専用型を生成し、余剰引数・型・NULL不一致を拒否する。未対応構文を汎用型で補完せず、SQL変更時の生成driftを検出する","when":"導入先adapterの契約適合を検証する"}</code>

要求源(JSON List): <code>["https://github.com/tsuji-tomonori/dev-standard/issues/69","user:2026-09-23-language-agnostic-adapters"]</code>
検証方法: 言語非依存契約検査と導入先adapterの正例・負例検証
検証証跡: manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する
検証(JSON Object): <code>{"evidence":"manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する","method":"言語非依存契約検査と導入先adapterの正例・負例検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/SKILL.md"]</code>
- テスト: <code>["tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DESIGN-013: ログのprivacy境界

要件ID(JSON): <code>"REQ-DESIGN-013"</code>
タイトル(JSON): <code>"ログのprivacy境界"</code>
主体(JSON): <code>"導入先repositoryのadapter"</code>
対象(JSON): <code>"ログcatalogと型付きcontextの許容field"</code>
導入先repositoryのadapterは、ログcatalogと型付きcontextの許容fieldを**検証する**。
行為enum: <code>"verify"</code>

根拠: ログのprivacy境界を明示的な契約にして欠落や推測による成功判定を防ぐ。
根拠(JSON): <code>"ログのprivacy境界を明示的な契約にして欠落や推測による成功判定を防ぐ。"</code>

項目版: 1 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"CHG-20260923-language-agnostic-adapters"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-DESIGN-013-1"</code> 前提: 該当する実装surfaceとadapter manifestがある。条件: 導入先adapterの契約適合を検証する。期待結果: ログcatalogの例外型・必須項目・context型・field値型を照合し、生例外・token・request body・未宣言field・未知の動的contextの出力を拒否する。誤型と機密を含む例外の負例を導入先で実行し、静的証拠と本番privacy保証を区別する。
  - criterion(JSON Object): <code>{"given":"該当する実装surfaceとadapter manifestがある","id":"AC-DESIGN-013-1","then":"ログcatalogの例外型・必須項目・context型・field値型を照合し、生例外・token・request body・未宣言field・未知の動的contextの出力を拒否する。誤型と機密を含む例外の負例を導入先で実行し、静的証拠と本番privacy保証を区別する","when":"導入先adapterの契約適合を検証する"}</code>

要求源(JSON List): <code>["https://github.com/tsuji-tomonori/dev-standard/issues/70","user:2026-09-23-language-agnostic-adapters"]</code>
検証方法: 言語非依存契約検査と導入先adapterの正例・負例検証
検証証跡: manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する
検証(JSON Object): <code>{"evidence":"manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する","method":"言語非依存契約検査と導入先adapterの正例・負例検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/SKILL.md"]</code>
- テスト: <code>["tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DESIGN-014: endpoint専用profileの全source適用

要件ID(JSON): <code>"REQ-DESIGN-014"</code>
タイトル(JSON): <code>"endpoint専用profileの全source適用"</code>
主体(JSON): <code>"導入先repositoryのadapter"</code>
対象(JSON): <code>"endpoint層に置けるsymbol集合と全source走査"</code>
導入先repositoryのadapterは、endpoint層に置けるsymbol集合と全source走査を**検証する**。
行為enum: <code>"verify"</code>

根拠: endpoint専用profileの全source適用を明示的な契約にして欠落や推測による成功判定を防ぐ。
根拠(JSON): <code>"endpoint専用profileの全source適用を明示的な契約にして欠落や推測による成功判定を防ぐ。"</code>

項目版: 2 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"CHG-20260923-independent-review-fixes"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-DESIGN-014-1"</code> 前提: 該当する実装surfaceとadapter manifestがある。条件: 導入先adapterの契約適合を検証する。期待結果: version付きprofileでendpoint層の許可symbol集合と適用対象を宣言し、全sourceを走査する。未登録endpoint・紛れ込んだ補助処理・動的定義等の負例を検証し、命名や登録済み経路だけで対象を限定しない。
  - criterion(JSON Object): <code>{"given":"該当する実装surfaceとadapter manifestがある","id":"AC-DESIGN-014-1","then":"version付きprofileでendpoint層の許可symbol集合と適用対象を宣言し、全sourceを走査する。未登録endpoint・紛れ込んだ補助処理・動的定義等の負例を検証し、命名や登録済み経路だけで対象を限定しない","when":"導入先adapterの契約適合を検証する"}</code>
- <code>"AC-DESIGN-014-2"</code> 前提: 該当する実装と選択profileがある。条件: 導入先adapterの正例と負例を検証する。期待結果: 実登録集合と全sourceの定義集合を照合し、同期/非同期の補助関数、メソッド、クラス、入れ子、lambda、未登録endpointの負例を拒否する。全体フローは許可されたendpointまたは所有者付き共有workflowに保持する。
  - criterion(JSON Object): <code>{"given":"該当する実装と選択profileがある","id":"AC-DESIGN-014-2","then":"実登録集合と全sourceの定義集合を照合し、同期/非同期の補助関数、メソッド、クラス、入れ子、lambda、未登録endpointの負例を拒否する。全体フローは許可されたendpointまたは所有者付き共有workflowに保持する","when":"導入先adapterの正例と負例を検証する"}</code>

要求源(JSON List): <code>["https://github.com/tsuji-tomonori/dev-standard/issues/72","user:2026-09-23-language-agnostic-adapters"]</code>
検証方法: 言語非依存契約検査と導入先adapterの正例・負例検証
検証証跡: manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する
検証(JSON Object): <code>{"evidence":"manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する","method":"言語非依存契約検査と導入先adapterの正例・負例検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/SKILL.md"]</code>
- テスト: <code>["tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DESIGN-015: API間直接依存の禁止

要件ID(JSON): <code>"REQ-DESIGN-015"</code>
タイトル(JSON): <code>"API間直接依存の禁止"</code>
主体(JSON): <code>"導入先repositoryのadapter"</code>
対象(JSON): <code>"operation所有単位間の依存境界"</code>
導入先repositoryのadapterは、operation所有単位間の依存境界を**検証する**。
行為enum: <code>"verify"</code>

根拠: API間直接依存の禁止を明示的な契約にして欠落や推測による成功判定を防ぐ。
根拠(JSON): <code>"API間直接依存の禁止を明示的な契約にして欠落や推測による成功判定を防ぐ。"</code>

項目版: 2 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"CHG-20260923-independent-review-fixes"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-DESIGN-015-1"</code> 前提: 該当する実装surfaceとadapter manifestがある。条件: 導入先adapterの契約適合を検証する。期待結果: API所有単位から別API所有単位への直接参照・呼出しを検出して拒否する。共有処理は所有者が明示された共有責務を経由させる。
  - criterion(JSON Object): <code>{"given":"該当する実装surfaceとadapter manifestがある","id":"AC-DESIGN-015-1","then":"API所有単位から別API所有単位への直接参照・呼出しを検出して拒否する。共有処理は所有者が明示された共有責務を経由させる","when":"導入先adapterの契約適合を検証する"}</code>
- <code>"AC-DESIGN-015-2"</code> 前提: 該当する実装と選択profileがある。条件: 導入先adapterの正例と負例を検証する。期待結果: import別名・相対import等の言語固有の参照表現を実所有先へ解決する。同期/非同期の呼出しについて、正当な共有責務参照を通し、別名や相対参照で隠した別APIへの依存を負例として拒否する。解決不能を依存なしと推定しない。
  - criterion(JSON Object): <code>{"given":"該当する実装と選択profileがある","id":"AC-DESIGN-015-2","then":"import別名・相対import等の言語固有の参照表現を実所有先へ解決する。同期/非同期の呼出しについて、正当な共有責務参照を通し、別名や相対参照で隠した別APIへの依存を負例として拒否する。解決不能を依存なしと推定しない","when":"導入先adapterの正例と負例を検証する"}</code>

要求源(JSON List): <code>["https://github.com/tsuji-tomonori/dev-standard/issues/68","user:2026-09-23-language-agnostic-adapters"]</code>
検証方法: 言語非依存契約検査と導入先adapterの正例・負例検証
検証証跡: manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する
検証(JSON Object): <code>{"evidence":"manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する","method":"言語非依存契約検査と導入先adapterの正例・負例検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/SKILL.md"]</code>
- テスト: <code>["tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DESIGN-016: SQL所有先の識別

要件ID(JSON): <code>"REQ-DESIGN-016"</code>
タイトル(JSON): <code>"SQL所有先の識別"</code>
主体(JSON): <code>"導入先repositoryのadapter"</code>
対象(JSON): <code>"owner付きSQLとquery生成先"</code>
導入先repositoryのadapterは、owner付きSQLとquery生成先を**検証する**。
行為enum: <code>"verify"</code>

根拠: SQL所有先の識別を明示的な契約にして欠落や推測による成功判定を防ぐ。
根拠(JSON): <code>"SQL所有先の識別を明示的な契約にして欠落や推測による成功判定を防ぐ。"</code>

項目版: 1 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"CHG-20260923-language-agnostic-adapters"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-DESIGN-016-1"</code> 前提: 該当する実装surfaceとadapter manifestがある。条件: 導入先adapterの契約適合を検証する。期待結果: SQLのownerとquery生成先を対応付け、全体共通生成先への集約と同一生成symbolの上書きを拒否する。異なるownerの同名SQLを別識別子として保持する。
  - criterion(JSON Object): <code>{"given":"該当する実装surfaceとadapter manifestがある","id":"AC-DESIGN-016-1","then":"SQLのownerとquery生成先を対応付け、全体共通生成先への集約と同一生成symbolの上書きを拒否する。異なるownerの同名SQLを別識別子として保持する","when":"導入先adapterの契約適合を検証する"}</code>

要求源(JSON List): <code>["https://github.com/tsuji-tomonori/dev-standard/issues/68","user:2026-09-23-language-agnostic-adapters"]</code>
検証方法: 言語非依存契約検査と導入先adapterの正例・負例検証
検証証跡: manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する
検証(JSON Object): <code>{"evidence":"manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する","method":"言語非依存契約検査と導入先adapterの正例・負例検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/SKILL.md"]</code>
- テスト: <code>["tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DESIGN-017: SQL投影と結果型の一致

要件ID(JSON): <code>"REQ-DESIGN-017"</code>
タイトル(JSON): <code>"SQL投影と結果型の一致"</code>
主体(JSON): <code>"導入先repositoryのadapter"</code>
対象(JSON): <code>"各SQLの実投影とNULLに一致した専用結果型"</code>
導入先repositoryのadapterは、各SQLの実投影とNULLに一致した専用結果型を**検証する**。
行為enum: <code>"verify"</code>

根拠: SQL投影と結果型の一致を明示的な契約にして欠落や推測による成功判定を防ぐ。
根拠(JSON): <code>"SQL投影と結果型の一致を明示的な契約にして欠落や推測による成功判定を防ぐ。"</code>

項目版: 2 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"CHG-20260926-lazunex-conformance"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-DESIGN-017-1"</code> 前提: 該当する実装surfaceとadapter manifestがある。条件: 導入先adapterの契約適合を検証する。期待結果: 各SQLの列・式・alias・join・集約・NULL可能性から結果型を生成し、全table行型の流用による投影差異を拒否する。SQL/データ定義変更、生成物欠落と手編集を検出する。
  - criterion(JSON Object): <code>{"given":"該当する実装surfaceとadapter manifestがある","id":"AC-DESIGN-017-1","then":"各SQLの列・式・alias・join・集約・NULL可能性から結果型を生成し、全table行型の流用による投影差異を拒否する。SQL/データ定義変更、生成物欠落と手編集を検出する","when":"導入先adapterの契約適合を検証する"}</code>
- <code>"AC-DESIGN-017-2"</code> 前提: 固定版の参照実装と導入先の実sourceがある。条件: SELECT/RETURNINGの投影が変わる。期待結果: 結果型はSQL投影そのものから生成し、部分列の取得を完全な業務row modelへ合わせるためだけに列を増やさない。列別名、NULL拡張、集約・式・RETURNINGの未対応を明示し、headerに手書きした結果型名だけを一次情報とみなさない。。
  - criterion(JSON Object): <code>{"given":"固定版の参照実装と導入先の実sourceがある","id":"AC-DESIGN-017-2","then":"結果型はSQL投影そのものから生成し、部分列の取得を完全な業務row modelへ合わせるためだけに列を増やさない。列別名、NULL拡張、集約・式・RETURNINGの未対応を明示し、headerに手書きした結果型名だけを一次情報とみなさない。","when":"SELECT/RETURNINGの投影が変わる"}</code>

要求源(JSON List): <code>["https://github.com/tsuji-tomonori/dev-standard/issues/69","user:2026-09-23-language-agnostic-adapters","user:2026-09-26-lazunex-authoritative"]</code>
検証方法: 言語非依存契約検査と導入先adapterの正例・負例検証
検証証跡: manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する
検証(JSON Object): <code>{"evidence":"manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する","method":"言語非依存契約検査と導入先adapterの正例・負例検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/SKILL.md"]</code>
- テスト: <code>["tests/test_design_adoption.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DESIGN-018: 意味ある戻り値の利用

要件ID(JSON): <code>"REQ-DESIGN-018"</code>
タイトル(JSON): <code>"意味ある戻り値の利用"</code>
主体(JSON): <code>"導入先repositoryのadapter"</code>
対象(JSON): <code>"同期・非同期呼出しの意味ある戻り値"</code>
導入先repositoryのadapterは、同期・非同期呼出しの意味ある戻り値を**検証する**。
行為enum: <code>"verify"</code>

根拠: 意味ある戻り値の利用を原子的な義務にし、配置や生成driftの成功による検査漏れを防ぐ。
根拠(JSON): <code>"意味ある戻り値の利用を原子的な義務にし、配置や生成driftの成功による検査漏れを防ぐ。"</code>

項目版: 1 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"CHG-20260923-independent-review-fixes"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-DESIGN-018-1"</code> 前提: 戻り値を持つ処理を同期または非同期で呼び出す。条件: 導入先adapterが該当する構成契約を検査する。期待結果: 呼出し実体と戻り契約を解決し、意味ある結果を単独式として破棄する呼出しを拒否する。awaitや別名呼出しも同じ基準で検査する。
  - criterion(JSON Object): <code>{"given":"戻り値を持つ処理を同期または非同期で呼び出す","id":"AC-DESIGN-018-1","then":"呼出し実体と戻り契約を解決し、意味ある結果を単独式として破棄する呼出しを拒否する。awaitや別名呼出しも同じ基準で検査する","when":"導入先adapterが該当する構成契約を検査する"}</code>
- <code>"AC-DESIGN-018-2"</code> 前提: 導入先言語のadapterを接続する。条件: 受入検査の正例と負例を実行する。期待結果: 条件・後続処理・応答への結果利用を正例、同期呼出しの単独破棄とawait結果の単独破棄を負例として接続する。検証専用の処理は実体が必要な検証を行い値なしで戻ることを照合し、型注釈の変更だけで意味ある戻り値を隠す負例を拒否する。
  - criterion(JSON Object): <code>{"given":"導入先言語のadapterを接続する","id":"AC-DESIGN-018-2","then":"条件・後続処理・応答への結果利用を正例、同期呼出しの単独破棄とawait結果の単独破棄を負例として接続する。検証専用の処理は実体が必要な検証を行い値なしで戻ることを照合し、型注釈の変更だけで意味ある戻り値を隠す負例を拒否する","when":"受入検査の正例と負例を実行する"}</code>

要求源(JSON List): <code>["https://github.com/tsuji-tomonori/dev-standard/issues/72","user:2026-09-23-independent-review-fixes"]</code>
検証方法: 要件と棚卸し対応の検査および導入先adapterの受入検査
検証証跡: 参照repositoryではactive IDとtool/gap対応を検査する。言語固有の意味解析・正例・負例・実行テストは導入先の実接続と結果を確認し、未接続を成功としない
検証(JSON Object): <code>{"evidence":"参照repositoryではactive IDとtool/gap対応を検査する。言語固有の意味解析・正例・負例・実行テストは導入先の実接続と結果を確認し、未接続を成功としない","method":"要件と棚卸し対応の検査および導入先adapterの受入検査"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/SKILL.md",".agents/skills/generate-implementation-design/assets/reference-tools/lazunex-096e1e5.json"]</code>
- テスト: <code>["tests/test_reference_inventory.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DESIGN-019: 判定処理の定数真偽値拒否

要件ID(JSON): <code>"REQ-DESIGN-019"</code>
タイトル(JSON): <code>"判定処理の定数真偽値拒否"</code>
主体(JSON): <code>"導入先repositoryのadapter"</code>
対象(JSON): <code>"判定処理の入力と実処理に対応する真偽結果"</code>
導入先repositoryのadapterは、判定処理の入力と実処理に対応する真偽結果を**検証する**。
行為enum: <code>"verify"</code>

根拠: 判定処理の定数真偽値拒否を原子的な義務にし、配置や生成driftの成功による検査漏れを防ぐ。
根拠(JSON): <code>"判定処理の定数真偽値拒否を原子的な義務にし、配置や生成driftの成功による検査漏れを防ぐ。"</code>

項目版: 1 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"CHG-20260923-independent-review-fixes"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-DESIGN-019-1"</code> 前提: 真偽値を返す判定処理がある。条件: 導入先adapterが該当する構成契約を検査する。期待結果: 同期・非同期の判定処理がすべての正常終了経路で同じ定数真偽値だけを返す場合を拒否する。入力や実処理の判定結果に依存する真偽値を正例とする。
  - criterion(JSON Object): <code>{"given":"真偽値を返す判定処理がある","id":"AC-DESIGN-019-1","then":"同期・非同期の判定処理がすべての正常終了経路で同じ定数真偽値だけを返す場合を拒否する。入力や実処理の判定結果に依存する真偽値を正例とする","when":"導入先adapterが該当する構成契約を検査する"}</code>
- <code>"AC-DESIGN-019-2"</code> 前提: 導入先言語のadapterを接続する。条件: 受入検査の正例と負例を実行する。期待結果: 常に真または常に偽を返す処理を同期・非同期それぞれの負例にする。条件に応じて真と偽を返す処理は通す。例外による検証専用処理は値なしの契約と実体を照合する。
  - criterion(JSON Object): <code>{"given":"導入先言語のadapterを接続する","id":"AC-DESIGN-019-2","then":"常に真または常に偽を返す処理を同期・非同期それぞれの負例にする。条件に応じて真と偽を返す処理は通す。例外による検証専用処理は値なしの契約と実体を照合する","when":"受入検査の正例と負例を実行する"}</code>

要求源(JSON List): <code>["https://github.com/tsuji-tomonori/dev-standard/issues/72","user:2026-09-23-independent-review-fixes"]</code>
検証方法: 要件と棚卸し対応の検査および導入先adapterの受入検査
検証証跡: 参照repositoryではactive IDとtool/gap対応を検査する。言語固有の意味解析・正例・負例・実行テストは導入先の実接続と結果を確認し、未接続を成功としない
検証(JSON Object): <code>{"evidence":"参照repositoryではactive IDとtool/gap対応を検査する。言語固有の意味解析・正例・負例・実行テストは導入先の実接続と結果を確認し、未接続を成功としない","method":"要件と棚卸し対応の検査および導入先adapterの受入検査"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/SKILL.md",".agents/skills/generate-implementation-design/assets/reference-tools/lazunex-096e1e5.json"]</code>
- テスト: <code>["tests/test_reference_inventory.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DESIGN-020: 包括的な例外捕捉の拒否

要件ID(JSON): <code>"REQ-DESIGN-020"</code>
タイトル(JSON): <code>"包括的な例外捕捉の拒否"</code>
主体(JSON): <code>"導入先repositoryのadapter"</code>
対象(JSON): <code>"API業務フローの捕捉対象"</code>
導入先repositoryのadapterは、API業務フローの捕捉対象を**検証する**。
行為enum: <code>"verify"</code>

根拠: 包括的な例外捕捉の拒否を原子的な義務にし、配置や生成driftの成功による検査漏れを防ぐ。
根拠(JSON): <code>"包括的な例外捕捉の拒否を原子的な義務にし、配置や生成driftの成功による検査漏れを防ぐ。"</code>

項目版: 1 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"CHG-20260923-independent-review-fixes"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-DESIGN-020-1"</code> 前提: 選択profileのAPI業務フローに例外捕捉がある。条件: 導入先adapterが該当する構成契約を検査する。期待結果: 宣言した具体的な例外型または閉じた例外集合による捕捉を許可し、全例外・基底例外を含む包括的捕捉を拒否する。
  - criterion(JSON Object): <code>{"given":"選択profileのAPI業務フローに例外捕捉がある","id":"AC-DESIGN-020-1","then":"宣言した具体的な例外型または閉じた例外集合による捕捉を許可し、全例外・基底例外を含む包括的捕捉を拒否する","when":"導入先adapterが該当する構成契約を検査する"}</code>
- <code>"AC-DESIGN-020-2"</code> 前提: 導入先言語のadapterを接続する。条件: 受入検査の正例と負例を実行する。期待結果: 同期・非同期の処理で宣言済み例外の捕捉を正例とし、型指定なし・基底例外・別名や集合に隠れた包括的捕捉を負例として検証する。未知の例外集合は未対応として報告する。
  - criterion(JSON Object): <code>{"given":"導入先言語のadapterを接続する","id":"AC-DESIGN-020-2","then":"同期・非同期の処理で宣言済み例外の捕捉を正例とし、型指定なし・基底例外・別名や集合に隠れた包括的捕捉を負例として検証する。未知の例外集合は未対応として報告する","when":"受入検査の正例と負例を実行する"}</code>

要求源(JSON List): <code>["https://github.com/tsuji-tomonori/dev-standard/issues/72","user:2026-09-23-independent-review-fixes"]</code>
検証方法: 要件と棚卸し対応の検査および導入先adapterの受入検査
検証証跡: 参照repositoryではactive IDとtool/gap対応を検査する。言語固有の意味解析・正例・負例・実行テストは導入先の実接続と結果を確認し、未接続を成功としない
検証(JSON Object): <code>{"evidence":"参照repositoryではactive IDとtool/gap対応を検査する。言語固有の意味解析・正例・負例・実行テストは導入先の実接続と結果を確認し、未接続を成功としない","method":"要件と棚卸し対応の検査および導入先adapterの受入検査"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/SKILL.md",".agents/skills/generate-implementation-design/assets/reference-tools/lazunex-096e1e5.json"]</code>
- テスト: <code>["tests/test_reference_inventory.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DESIGN-021: 業務層の通信例外分離

要件ID(JSON): <code>"REQ-DESIGN-021"</code>
タイトル(JSON): <code>"業務層の通信例外分離"</code>
主体(JSON): <code>"導入先repositoryのadapter"</code>
対象(JSON): <code>"個別業務処理から送出する例外"</code>
導入先repositoryのadapterは、個別業務処理から送出する例外を**検証する**。
行為enum: <code>"verify"</code>

根拠: 業務層の通信例外分離を原子的な義務にし、配置や生成driftの成功による検査漏れを防ぐ。
根拠(JSON): <code>"業務層の通信例外分離を原子的な義務にし、配置や生成driftの成功による検査漏れを防ぐ。"</code>

項目版: 1 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"CHG-20260923-independent-review-fixes"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-DESIGN-021-1"</code> 前提: HTTP等の通信境界から個別業務処理を呼ぶ。条件: 導入先adapterが該当する構成契約を検査する。期待結果: 個別業務処理からHTTP例外等の通信層固有例外を直接送出する実装を拒否し、業務例外から通信応答への変換を境界層が所有することを検査する。
  - criterion(JSON Object): <code>{"given":"HTTP等の通信境界から個別業務処理を呼ぶ","id":"AC-DESIGN-021-1","then":"個別業務処理からHTTP例外等の通信層固有例外を直接送出する実装を拒否し、業務例外から通信応答への変換を境界層が所有することを検査する","when":"導入先adapterが該当する構成契約を検査する"}</code>
- <code>"AC-DESIGN-021-2"</code> 前提: 導入先言語のadapterを接続する。条件: 受入検査の正例と負例を実行する。期待結果: 同期・非同期の業務例外と境界層での応答変換を正例とし、業務層で通信例外を直接生成・送出する負例を別名参照も含めて検証する。特定frameworkの例外クラス名だけに依存しない。
  - criterion(JSON Object): <code>{"given":"導入先言語のadapterを接続する","id":"AC-DESIGN-021-2","then":"同期・非同期の業務例外と境界層での応答変換を正例とし、業務層で通信例外を直接生成・送出する負例を別名参照も含めて検証する。特定frameworkの例外クラス名だけに依存しない","when":"受入検査の正例と負例を実行する"}</code>

要求源(JSON List): <code>["https://github.com/tsuji-tomonori/dev-standard/issues/72","user:2026-09-23-independent-review-fixes"]</code>
検証方法: 要件と棚卸し対応の検査および導入先adapterの受入検査
検証証跡: 参照repositoryではactive IDとtool/gap対応を検査する。言語固有の意味解析・正例・負例・実行テストは導入先の実接続と結果を確認し、未接続を成功としない
検証(JSON Object): <code>{"evidence":"参照repositoryではactive IDとtool/gap対応を検査する。言語固有の意味解析・正例・負例・実行テストは導入先の実接続と結果を確認し、未接続を成功としない","method":"要件と棚卸し対応の検査および導入先adapterの受入検査"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/SKILL.md",".agents/skills/generate-implementation-design/assets/reference-tools/lazunex-096e1e5.json"]</code>
- テスト: <code>["tests/test_reference_inventory.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DESIGN-022: 処理単位の説明欠落検出

要件ID(JSON): <code>"REQ-DESIGN-022"</code>
タイトル(JSON): <code>"処理単位の説明欠落検出"</code>
主体(JSON): <code>"導入先repositoryのadapter"</code>
対象(JSON): <code>"選択profileに含まれる処理単位の責務説明"</code>
導入先repositoryのadapterは、選択profileに含まれる処理単位の責務説明を**検証する**。
行為enum: <code>"verify"</code>

根拠: 処理単位の説明欠落検出を原子的な義務にし、配置や生成driftの成功による検査漏れを防ぐ。
根拠(JSON): <code>"処理単位の説明欠落検出を原子的な義務にし、配置や生成driftの成功による検査漏れを防ぐ。"</code>

項目版: 1 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"CHG-20260923-independent-review-fixes"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-DESIGN-022-1"</code> 前提: 設計生成または責務検査の対象処理がある。条件: 導入先adapterが該当する構成契約を検査する。期待結果: 処理単位に対応する自然言語の責務説明を要求し、欠落と空の説明を拒否する。docstring・文書コメント等の形式は導入先言語に合わせる。
  - criterion(JSON Object): <code>{"given":"設計生成または責務検査の対象処理がある","id":"AC-DESIGN-022-1","then":"処理単位に対応する自然言語の責務説明を要求し、欠落と空の説明を拒否する。docstring・文書コメント等の形式は導入先言語に合わせる","when":"導入先adapterが該当する構成契約を検査する"}</code>
- <code>"AC-DESIGN-022-2"</code> 前提: 導入先言語のadapterを接続する。条件: 受入検査の正例と負例を実行する。期待結果: 同期・非同期の処理について実体に対応する説明を正例、説明なしと空白だけの説明を負例として検証する。説明の言語は既存の説明言語要件に従う。
  - criterion(JSON Object): <code>{"given":"導入先言語のadapterを接続する","id":"AC-DESIGN-022-2","then":"同期・非同期の処理について実体に対応する説明を正例、説明なしと空白だけの説明を負例として検証する。説明の言語は既存の説明言語要件に従う","when":"受入検査の正例と負例を実行する"}</code>

要求源(JSON List): <code>["https://github.com/tsuji-tomonori/dev-standard/issues/72","user:2026-09-23-independent-review-fixes"]</code>
検証方法: 要件と棚卸し対応の検査および導入先adapterの受入検査
検証証跡: 参照repositoryではactive IDとtool/gap対応を検査する。言語固有の意味解析・正例・負例・実行テストは導入先の実接続と結果を確認し、未接続を成功としない
検証(JSON Object): <code>{"evidence":"参照repositoryではactive IDとtool/gap対応を検査する。言語固有の意味解析・正例・負例・実行テストは導入先の実接続と結果を確認し、未接続を成功としない","method":"要件と棚卸し対応の検査および導入先adapterの受入検査"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/SKILL.md",".agents/skills/generate-implementation-design/assets/reference-tools/lazunex-096e1e5.json"]</code>
- テスト: <code>["tests/test_reference_inventory.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DESIGN-023: 個別処理からフローへの逆依存禁止

要件ID(JSON): <code>"REQ-DESIGN-023"</code>
タイトル(JSON): <code>"個別処理からフローへの逆依存禁止"</code>
主体(JSON): <code>"導入先repositoryのadapter"</code>
対象(JSON): <code>"個別処理とendpoint・共有workflowの依存方向"</code>
導入先repositoryのadapterは、個別処理とendpoint・共有workflowの依存方向を**検証する**。
行為enum: <code>"verify"</code>

根拠: 個別処理からフローへの逆依存禁止を原子的な義務にし、配置や生成driftの成功による検査漏れを防ぐ。
根拠(JSON): <code>"個別処理からフローへの逆依存禁止を原子的な義務にし、配置や生成driftの成功による検査漏れを防ぐ。"</code>

項目版: 1 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"CHG-20260923-independent-review-fixes"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-DESIGN-023-1"</code> 前提: endpointまたはworker共有workflowが個別処理を呼ぶ。条件: 導入先adapterが該当する構成契約を検査する。期待結果: 個別処理からendpointまたは共有workflowへの参照・呼出しを拒否する。全体フローを個別処理へ移したり共有workflowへの委譲で制約を回避したりしない。
  - criterion(JSON Object): <code>{"given":"endpointまたはworker共有workflowが個別処理を呼ぶ","id":"AC-DESIGN-023-1","then":"個別処理からendpointまたは共有workflowへの参照・呼出しを拒否する。全体フローを個別処理へ移したり共有workflowへの委譲で制約を回避したりしない","when":"導入先adapterが該当する構成契約を検査する"}</code>
- <code>"AC-DESIGN-023-2"</code> 前提: 導入先言語のadapterを接続する。条件: 受入検査の正例と負例を実行する。期待結果: 所有者付き共有workflowから個別処理への呼出しを正例とし、個別処理からendpoint・共有workflowへの別名/相対参照と同期/非同期呼出しを負例にする。設計generatorは正当な共有workflowの実call graphを追跡する。
  - criterion(JSON Object): <code>{"given":"導入先言語のadapterを接続する","id":"AC-DESIGN-023-2","then":"所有者付き共有workflowから個別処理への呼出しを正例とし、個別処理からendpoint・共有workflowへの別名/相対参照と同期/非同期呼出しを負例にする。設計generatorは正当な共有workflowの実call graphを追跡する","when":"受入検査の正例と負例を実行する"}</code>

要求源(JSON List): <code>["https://github.com/tsuji-tomonori/dev-standard/issues/72","user:2026-09-23-independent-review-fixes"]</code>
検証方法: 要件と棚卸し対応の検査および導入先adapterの受入検査
検証証跡: 参照repositoryではactive IDとtool/gap対応を検査する。言語固有の意味解析・正例・負例・実行テストは導入先の実接続と結果を確認し、未接続を成功としない
検証(JSON Object): <code>{"evidence":"参照repositoryではactive IDとtool/gap対応を検査する。言語固有の意味解析・正例・負例・実行テストは導入先の実接続と結果を確認し、未接続を成功としない","method":"要件と棚卸し対応の検査および導入先adapterの受入検査"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/SKILL.md",".agents/skills/generate-implementation-design/assets/reference-tools/lazunex-096e1e5.json"]</code>
- テスト: <code>["tests/test_reference_inventory.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DESIGN-024: 参照構成の適用範囲記録

要件ID(JSON): <code>"REQ-DESIGN-024"</code>
タイトル(JSON): <code>"参照構成の適用範囲記録"</code>
主体(JSON): <code>"導入先repositoryのadapter"</code>
対象(JSON): <code>"固定参照と導入先の構成profile対応"</code>
導入先repositoryのadapterは、固定参照と導入先の構成profile対応を**検証する**。
行為enum: <code>"verify"</code>

根拠: 参照構成の適用範囲記録を原子的な義務にし、配置や生成driftの成功による検査漏れを防ぐ。
根拠(JSON): <code>"参照構成の適用範囲記録を原子的な義務にし、配置や生成driftの成功による検査漏れを防ぐ。"</code>

項目版: 2 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"CHG-20260926-lazunex-conformance"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-DESIGN-024-1"</code> 前提: 参照実装への追従を利用者が指定する。条件: 導入先adapterが該当する構成契約を検査する。期待結果: 固定SHA、operation粒度、責務、適用する規則と理由付き適用外を導入先要件と版付きprofileへ対応付ける。配置だけでなく例外境界・型付きlogger・query型・生成帳票の意味も比較対象とする。
  - criterion(JSON Object): <code>{"given":"参照実装への追従を利用者が指定する","id":"AC-DESIGN-024-1","then":"固定SHA、operation粒度、責務、適用する規則と理由付き適用外を導入先要件と版付きprofileへ対応付ける。配置だけでなく例外境界・型付きlogger・query型・生成帳票の意味も比較対象とする","when":"導入先adapterが該当する構成契約を検査する"}</code>
- <code>"AC-DESIGN-024-2"</code> 前提: 導入先言語のadapterを接続する。条件: 受入検査の正例と負例を実行する。期待結果: 実装、生成器、責務規則、関連テストを比較して適用範囲を確定する。既存の明示制約を優先し、参照固有の言語・framework・業務定数・命名辞書・テスト雛形・固定数量閾値を根拠なく全projectへ固定しない。
  - criterion(JSON Object): <code>{"given":"導入先言語のadapterを接続する","id":"AC-DESIGN-024-2","then":"実装、生成器、責務規則、関連テストを比較して適用範囲を確定する。既存の明示制約を優先し、参照固有の言語・framework・業務定数・命名辞書・テスト雛形・固定数量閾値を根拠なく全projectへ固定しない","when":"受入検査の正例と負例を実行する"}</code>
- <code>"AC-DESIGN-024-3"</code> 前提: 固定版の参照実装と導入先の実sourceがある。条件: 参照と導入先で構成・文書品質が異なる。期待結果: 実装・生成文書・生成器・規則・testの固定版を比較し、是正必須、業務/技術上の適応、同等保持、参照自体の未解決を分ける。lazunexの意味品質を基準とする一方、health例外、互換shim、固有DB、古い生成図の不整合を無批判に共通義務へ昇格しない。。
  - criterion(JSON Object): <code>{"given":"固定版の参照実装と導入先の実sourceがある","id":"AC-DESIGN-024-3","then":"実装・生成文書・生成器・規則・testの固定版を比較し、是正必須、業務/技術上の適応、同等保持、参照自体の未解決を分ける。lazunexの意味品質を基準とする一方、health例外、互換shim、固有DB、古い生成図の不整合を無批判に共通義務へ昇格しない。","when":"参照と導入先で構成・文書品質が異なる"}</code>

要求源(JSON List): <code>["https://github.com/tsuji-tomonori/dev-standard/issues/68","user:2026-09-23-independent-review-fixes","https://github.com/tsuji-tomonori/dev-standard/issues/69","https://github.com/tsuji-tomonori/dev-standard/issues/70","user:2026-09-26-lazunex-authoritative"]</code>
検証方法: 要件と棚卸し対応の検査および導入先adapterの受入検査
検証証跡: 参照repositoryではactive IDとtool/gap対応を検査する。言語固有の意味解析・正例・負例・実行テストは導入先の実接続と結果を確認し、未接続を成功としない
検証(JSON Object): <code>{"evidence":"参照repositoryではactive IDとtool/gap対応を検査する。言語固有の意味解析・正例・負例・実行テストは導入先の実接続と結果を確認し、未接続を成功としない","method":"要件と棚卸し対応の検査および導入先adapterの受入検査"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/SKILL.md",".agents/skills/generate-implementation-design/assets/reference-tools/lazunex-096e1e5.json"]</code>
- テスト: <code>["tests/test_reference_inventory.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-ASBUILT-036: 参照適合の個別要件と新規実行証拠

要件ID(JSON): <code>"REQ-ASBUILT-036"</code>
タイトル(JSON): <code>"参照適合の個別要件と新規実行証拠"</code>
主体(JSON): <code>"導入先repositoryの設計adapterと共通契約検査器"</code>
対象(JSON): <code>"固定参照の個別受入条件と現在sourceに対応する正例・負例の結果"</code>
導入先repositoryの設計adapterと共通契約検査器は、固定参照の個別受入条件と現在sourceに対応する正例・負例の結果を**検証する**。
行為enum: <code>"verify"</code>

根拠: 見出し・接続path・定数passだけでは意味品質の欠落を防げないため、参照の各義務を失わず実行する。
根拠(JSON): <code>"見出し・接続path・定数passだけでは意味品質の欠落を防げないため、参照の各義務を失わず実行する。"</code>

項目版: 1 / 状態: `active` / 種別: `quality`
変更識別子: <code>"CHG-20260926-lazunex-conformance"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-ASBUILT-036-1"</code> 前提: 版付き参照適合profileが選択されている。条件: mappingを検査する。期待結果: 主参照の固定repository/SHAと全tools集合、全参照要件とactiveな個別受入条件を照合し、主参照の置換・欠落・重複・包括条件への潰し込みを拒否する。適用外も明示要件と理由を持ち、未実装を免除しない。。
  - criterion(JSON Object): <code>{"given":"版付き参照適合profileが選択されている","id":"AC-ASBUILT-036-1","then":"主参照の固定repository/SHAと全tools集合、全参照要件とactiveな個別受入条件を照合し、主参照の置換・欠落・重複・包括条件への潰し込みを拒否する。適用外も明示要件と理由を持ち、未実装を免除しない。","when":"mappingを検査する"}</code>
- <code>"AC-ASBUILT-036-2"</code> 前提: 導入先の意味検査commandが接続されている。条件: 共通の完了検査を実行する。期待結果: 新規一時reportへ検査を実行し、現在の宣言sourceと契約入力のdigest、collectorの正確なID、source位置、正例と負例、各要件結果を照合する。no-op、保存済みpass、未収集ID、fail/skipped/not-run、要件やtestの対応漏れを成功としない。。
  - criterion(JSON Object): <code>{"given":"導入先の意味検査commandが接続されている","id":"AC-ASBUILT-036-2","then":"新規一時reportへ検査を実行し、現在の宣言sourceと契約入力のdigest、collectorの正確なID、source位置、正例と負例、各要件結果を照合する。no-op、保存済みpass、未収集ID、fail/skipped/not-run、要件やtestの対応漏れを成功としない。","when":"共通の完了検査を実行する"}</code>
- <code>"AC-ASBUILT-036-3"</code> 前提: 意味解析は導入先が所有し、共通検査器はその結果契約を検査する。条件: 結果と制約を報告する。期待結果: 実解析の正当性と全source発見の責任を導入先へ残し、共通schema検査を意味的証明や業務E2E成功と表示しない。適用外の判定にも実行済みの適用範囲の正負例を要求し、Advisoryは必須検査と別に報告する。。
  - criterion(JSON Object): <code>{"given":"意味解析は導入先が所有し、共通検査器はその結果契約を検査する","id":"AC-ASBUILT-036-3","then":"実解析の正当性と全source発見の責任を導入先へ残し、共通schema検査を意味的証明や業務E2E成功と表示しない。適用外の判定にも実行済みの適用範囲の正負例を要求し、Advisoryは必須検査と別に報告する。","when":"結果と制約を報告する"}</code>

要求源(JSON List): <code>["user:2026-09-26-lazunex-authoritative","docs/audits/lazunex-slotkeeper/README.md"]</code>
検証方法: 共通契約の正負例と導入先の意味検査実行
検証証跡: 固定参照・要件対応・fresh report・実test ID・source digestを共通側で照合し、業務固有の意味解析と回帰は導入先で検証する。
検証(JSON Object): <code>{"evidence":"固定参照・要件対応・fresh report・実test ID・source digestを共通側で照合し、業務固有の意味解析と回帰は導入先で検証する。","method":"共通契約の正負例と導入先の意味検査実行"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/conformance.md","docs/audits/lazunex-slotkeeper/README.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/SKILL.md",".agents/skills/generate-implementation-design/scripts/check_design.py",".agents/skills/generate-implementation-design/scripts/conformance.py"]</code>
- テスト: <code>["tests/test_lazunex_conformance.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-DESIGN-025: 責務移行時の既存挙動維持

要件ID(JSON): <code>"REQ-DESIGN-025"</code>
タイトル(JSON): <code>"責務移行時の既存挙動維持"</code>
主体(JSON): <code>"導入先repositoryのadapter"</code>
対象(JSON): <code>"責務配置変更の前後で維持する観測可能な契約"</code>
導入先repositoryのadapterは、責務配置変更の前後で維持する観測可能な契約を**検証する**。
行為enum: <code>"verify"</code>

根拠: 責務移行時の既存挙動維持を原子的な義務にし、配置や生成driftの成功による検査漏れを防ぐ。
根拠(JSON): <code>"責務移行時の既存挙動維持を原子的な義務にし、配置や生成driftの成功による検査漏れを防ぐ。"</code>

項目版: 1 / 状態: `active` / 種別: `constraint`
変更識別子: <code>"CHG-20260923-independent-review-fixes"</code>
分類: scope=<code>"project"</code> / category=<code>"nonfunctional"</code>

受入条件:
- <code>"AC-DESIGN-025-1"</code> 前提: APIや共有workflowの責務配置を変更する。条件: 導入先adapterが該当する構成契約を検査する。期待結果: 変更前後の公開interface、transaction成功・失敗時の効果、外部呼出し前後の認可条件を同じ対象revisionの関係する実行テストで検証する。配置や設計driftの成功を挙動互換の証拠としない。
  - criterion(JSON Object): <code>{"given":"APIや共有workflowの責務配置を変更する","id":"AC-DESIGN-025-1","then":"変更前後の公開interface、transaction成功・失敗時の効果、外部呼出し前後の認可条件を同じ対象revisionの関係する実行テストで検証する。配置や設計driftの成功を挙動互換の証拠としない","when":"導入先adapterが該当する構成契約を検査する"}</code>
- <code>"AC-DESIGN-025-2"</code> 前提: 導入先言語のadapterを接続する。条件: 受入検査の正例と負例を実行する。期待結果: 導入先で該当するcommit/rollback・外部呼出しとtransactionの境界・再認可・既存HTTP契約の正例と負例、実保存先の回帰、既存E2Eと証跡閲覧を接続する。未実行は未検証と報告し、特定DB・Compose・CI・公開方法を強制しない。
  - criterion(JSON Object): <code>{"given":"導入先言語のadapterを接続する","id":"AC-DESIGN-025-2","then":"導入先で該当するcommit/rollback・外部呼出しとtransactionの境界・再認可・既存HTTP契約の正例と負例、実保存先の回帰、既存E2Eと証跡閲覧を接続する。未実行は未検証と報告し、特定DB・Compose・CI・公開方法を強制しない","when":"受入検査の正例と負例を実行する"}</code>

要求源(JSON List): <code>["https://github.com/tsuji-tomonori/dev-standard/issues/69","user:2026-09-23-independent-review-fixes"]</code>
検証方法: 要件と棚卸し対応の検査および導入先adapterの受入検査
検証証跡: 参照repositoryではactive IDとtool/gap対応を検査する。言語固有の意味解析・正例・負例・実行テストは導入先の実接続と結果を確認し、未接続を成功としない
検証(JSON Object): <code>{"evidence":"参照repositoryではactive IDとtool/gap対応を検査する。言語固有の意味解析・正例・負例・実行テストは導入先の実接続と結果を確認し、未接続を成功としない","method":"要件と棚卸し対応の検査および導入先adapterの受入検査"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/generate-implementation-design/references/adapter-contract.md"]</code>
- 実装: <code>[".agents/skills/generate-implementation-design/SKILL.md",".agents/skills/generate-implementation-design/assets/reference-tools/lazunex-096e1e5.json"]</code>
- テスト: <code>["tests/test_reference_inventory.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>

## REQ-EVIDENCE-004: 品質エビデンスの階層閲覧

要件ID(JSON): <code>"REQ-EVIDENCE-004"</code>
タイトル(JSON): <code>"品質エビデンスの階層閲覧"</code>
主体(JSON): <code>"導入先の品質portal adapter"</code>
対象(JSON): <code>"group→API→帳票の親子関係と現在位置"</code>
導入先の品質portal adapterは、group→API→帳票の親子関係と現在位置を**検証する**。
行為enum: <code>"verify"</code>

根拠: 品質エビデンスの階層閲覧を明示的な契約にして欠落や推測による成功判定を防ぐ。
根拠(JSON): <code>"品質エビデンスの階層閲覧を明示的な契約にして欠落や推測による成功判定を防ぐ。"</code>

項目版: 2 / 状態: `active` / 種別: `functional`
変更識別子: <code>"CHG-20260923-independent-review-fixes"</code>
分類: scope=<code>"project"</code> / category=<code>"functional"</code>

受入条件:
- <code>"AC-EVIDENCE-004-1"</code> 前提: 該当する実装surfaceとadapter manifestがある。条件: 導入先adapterの契約適合を検証する。期待結果: 階層を辿る操作、検索後の親階層と現在位置、帳票間link、CRUD図とCSV取得を提供する。導入先のブラウザ検証で操作を確認し、既存CIと公開規則を維持する。
  - criterion(JSON Object): <code>{"given":"該当する実装surfaceとadapter manifestがある","id":"AC-EVIDENCE-004-1","then":"階層を辿る操作、検索後の親階層と現在位置、帳票間link、CRUD図とCSV取得を提供する。導入先のブラウザ検証で操作を確認し、既存CIと公開規則を維持する","when":"導入先adapterの契約適合を検証する"}</code>
- <code>"AC-EVIDENCE-004-2"</code> 前提: 該当する実装と選択profileがある。条件: 導入先adapterの正例と負例を検証する。期待結果: グループ→API→帳票、検索後の親階層・現在位置、帳票間移動、CRUD図、CSV取得をGWTスクリーンショット付きのブラウザE2Eで確認する。生成例の可読性も確認し、実公開は既存権限に従う。
  - criterion(JSON Object): <code>{"given":"該当する実装と選択profileがある","id":"AC-EVIDENCE-004-2","then":"グループ→API→帳票、検索後の親階層・現在位置、帳票間移動、CRUD図、CSV取得をGWTスクリーンショット付きのブラウザE2Eで確認する。生成例の可読性も確認し、実公開は既存権限に従う","when":"導入先adapterの正例と負例を検証する"}</code>

要求源(JSON List): <code>["https://github.com/tsuji-tomonori/dev-standard/issues/67","user:2026-09-23-language-agnostic-adapters"]</code>
検証方法: 言語非依存契約検査と導入先adapterの正例・負例検証
検証証跡: manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する
検証(JSON Object): <code>{"evidence":"manifest接続と報告契約を検証し、意味解析と実行時の妥当性は導入先の検査結果を区別して確認する","method":"言語非依存契約検査と導入先adapterの正例・負例検証"}</code>
トレース(JSON List、順序保持):
- 設計: <code>[".agents/skills/inspect-quality-gates/references/evidence-portal.md"]</code>
- 実装: <code>[".agents/skills/inspect-quality-gates/scripts/evidence.py",".agents/skills/inspect-quality-gates/assets/evidence.js"]</code>
- テスト: <code>["tests/test_evidence_portal.py"]</code>
- 参照資料: <code>["DEVSTD-AS-BUILT"]</code>
廃止理由: <code>""</code>
後継要件: <code>""</code>
