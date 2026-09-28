# lazunex基準のSlotKeeper差分監査と標準是正

調査日: **2026-09-26**。この文書は固定版の比較結果であり、導入先の実装完了報告ではない。
要件の正本は `spec/requirements/requirements.qnt` のまま維持する。ここでは根拠と採用判断を記録する。

## 1. 結論

差異の主因は、lazunexの章立てだけが引き継がれ、内容の導出・責務の分離・要件単位の意味検査が導入先で十分に接続されなかったことである。
SlotKeeperのIMPLEMENTATION_REQUEST.mdはdev-standardの比較時点のmainを固定しているため、単なる旧版利用ではない。

1. **参照元の置換**: 採用台帳はlazunexではなくKotoRelayの27ファイルを対象とし、単一の `TECH-DESIGN` に集約している。[根拠][S-ADOPTION]
2. **形と意味の乖離**: 6帳票・章・リンク・生成driftが揃っていても、具体的sample、実到達ログ、テストとassertionの対応、責務境界を保証していない。[生成器][S-DESIGN]
3. **CRUDの表現相違**: lazunexの正本となる閲覧形態は「API × 資源」の行列。SlotKeeperの縦持ち一覧と疑似的な有向図は同等ではない。[参照][L-CRUD] / [対象][S-CSV]

このPRは **dev-standardの要件・Skill・配布検査・回帰テストを修正する**。lazunex/SlotKeeper本体、DB、AWS、公開設定、branch/merge方針は変更しない。
新しい標準が導入先の業務実装を自動的に修復するわけではない。SlotKeeperは本台帳に沿ったadapterと業務コードの是正が別途必要である。

## 2. 固定版と網羅範囲

| repository | commit | 追跡ファイル数 | 比較の役割 |
|---|---|---:|---|
| lazunex | `096e1e580ab1c0670c57e4febad2bd9fdd4698ee` | 868 | 文書・責務・検査能力の基準 |
| SlotKeeper | `1b7590fb671df765e62fcf82f158a0ba94bd713d` | 268 | 是正対象の比較版 |
| dev-standard | `5788b8671a74d08a230ade5d25c4719335cd7f71` | 比較基準 | 既存の要件・共通検査と配布境界 |

全**1,136ファイル**のパスとGit blob SHAを [inventory.json](inventory.json) に固定し、読取専用の再照合で一致を確認した。
全公開operationの帳票集合は [observations.json](observations.json) に記録した。参照tools全**52ファイル**の対応は [tools-comparison.md](tools-comparison.md) にある。
これは「全ファイルの内容が業務的に等価である」「全行の意味解析・実行テストを完了した」という主張ではない。異なる業務のliteralやテスト件数を一致させる比較でもない。

| 比較軸 | lazunex | SlotKeeper | 解釈 |
|---|---:|---:|---|
| 帳票に現れるoperation | 13 | 9 | 機能数の差は欠陥ではない |
| 6帳票があるoperation | 12 | 9 | lazunexのhealthはinterfaceのみ。対象のhealthの6帳票は維持する |
| API SQLファイル | 96 | 22 | SQL数そのものの一致は求めない |
| CRUD CSV | DB + 外部3種 = 4 | 集約された縦持ち1 | 表現と保存先分類を是正する |
| interfaceの具体sample代替文 | 0 | 全9operation | 「OpenAPI参照」では実sampleに代えられない |

`sample_placeholder` は指定の代替文の有無を示す観測であり、参照の全sampleをschema検証した結果ではない。
生成物を実装と併読し、下記は再発原因を共有する単位で集約した。各operationの全出力パスはobservationsから辿れる。

### 正とする範囲

lazunexの**文書に必要な情報量、API単位の所有、router/business/query/integrationの責務、検査の観点**を正とする。
Pythonのファイル名、MySQL、API Hubの業務語彙、AWSサービス種別、旧互換shim、生成器の不具合は新規実装へ無条件に複製しない。
適切な言語固有adapterで同等の責務と情報を実現する。技術選択を理由に情報量や検査を減らす場合は「同等」と扱わない。

## 3. 差分台帳

判定の「是正」は導入先で必要な変更、「維持」は既存の良い実装、「適応」は理由を要件に記録して許容する変更、「参照補正」はlazunex側の不足を継承しない判断である。
要件IDはdev-standard正本への追跡であり、本表だけを第二の要件正本にしない。

### 3.1 参照・適合判定

| ID | lazunex基準とSlotKeeperの差 | 判定・必要な是正 | 正本要件 |
|---|---|---|---|
| REF-01 | 参照tools52件に対して、対象台帳はKotoRelay27件。[台帳][S-ADOPTION] | **是正**: 固定lazunexの全path/blobをprimaryとして保持。KotoRelayは補助参照に限る | REQ-ASBUILT-030/034/036 |
| REF-02 | 異なる責務・帳票の基準が全てTECH-DESIGNの1受入条件へ潰れる。[manifest][S-MANIFEST] | **是正**: 各参照ruleに別の導入先受入条件を割り当て、未対応と非該当を区別する | REQ-ASBUILT-029/036 |
| REF-03 | 多数のtoolが同じ数ファイルへ接続され、パスの実在だけでは能力が分からない。[台帳][S-ADOPTION] | **是正**: 実collector ID、正例・負例、実行結果をrule別に対応付ける | REQ-ASBUILT-020/036 |
| REF-04 | reportのconfiguration/design_driftは生成器が固定passを書き、unsupportedは常に空。[生成器][S-DESIGN] | **是正**: 保存済みreportと独立した意味検査を実行。source digest・収集単位・検査結果を照合する | REQ-ASBUILT-031/032/036 |
| REF-05 | 共通v2検査の成功をAPI意味適合と混同できる | **是正**: API導入の既定入口はmanifest v3。v2は明示した旧形式診断であり完了扱いしない | REQ-ASBUILT-029/036 |

### 3.2 API帳票の内容

| ID | lazunex基準とSlotKeeperの差 | 判定・必要な是正 | 正本要件 |
|---|---|---|---|
| DOC-01 | 参照の入力・制約・具体値に対し、対象detailはrequestBodyがあればparametersを落とす。[参照][L-DETAIL] / [対象][S-DESIGN] | **是正**: Headers/Path/Query/Bodyの同時存在を全て保ち、必須・型・制約を項目表にする | REQ-ASBUILT-004 |
| DOC-02 | 対象の正常前提はdocstring、リソース変更はSQL種別と表名のみ | **是正**: 入力・既存値・定数・計算値等の由来と、更新列・条件・処理順を実装から辿れるようにする | REQ-ASBUILT-004/024 |
| DOC-03 | 対象interfaceはraw OpenAPI JSONと未展開の参照が中心。[参照][L-IF] / [対象][S-DESIGN] | **是正**: schema参照を解決し、項目単位の説明・制約・response statusを閲覧できるようにする | REQ-ASBUILT-004/023 |
| DOC-04 | 全9APIのsampleがMETHOD/PATHと「OpenAPI参照」に置換。[参照samples][L-SAMPLE] / [対象生成][S-DESIGN] | **是正**: schemaに適合する具体Request/Response対を安全な値で生成し、status・実テストへ結ぶ | REQ-ASBUILT-012/013 |
| DOC-05 | 公開response catalogと実到達の成功・失敗経路が分かれていない。[対象app][S-APP] | **是正**: 宣言したstatusと観測/解析した経路を区別し、全APIに同じ例外を推測で配らない | REQ-ASBUILT-027/033 |
| DOC-06 | 対象messagesはrequest_result固定文と共通status列挙。[参照][L-MSG] / [対象][S-DESIGN] | **是正**: message ID、level、発生条件、型付き出力項目、例外・応答・運用対処を対応付ける | REQ-ASBUILT-010/027; REQ-DESIGN-013 |
| DOC-07 | 対象queryはSQLヘッダ3行の文字列とSQL全文中心。[参照][L-QUERYDOC] / [対象][S-DESIGN] | **是正**: 引数・戻り値・列の型、NULL、投影、条件を構造化しSQL/DDLへ追跡させる | REQ-DESIGN-004/012/017 |
| DOC-08 | 対象sequenceは特定q関数とtransactionだけを扱い、一般helper・認証依存・early return等を十分に説明しない。[生成器][S-DESIGN] | **是正**: 実際の評価順、分岐、return、catch、境界を保持。未解析経路を成功にしない | REQ-ASBUILT-026/032 |
| DOC-09 | retry/commit説明を固定文で図へ埋め込む。[生成器][S-DESIGN] / [実装][S-DB] | **是正**: transaction実装の境界・上限・失敗と照合し、共通処理も根拠を持たせる | REQ-ASBUILT-026; REQ-DESIGN-011 |
| DOC-10 | 参照のF01等の要因・要素に対し、対象は「入力・権限・状態・競合」1見出し。[参照][L-FACTORS] / [対象][S-DESIGN] | **是正**: 個別要因、要素、成立する組合せ、期待応答・状態・ログを実ケースへ結ぶ | REQ-ASBUILT-022/028 |
| DOC-11 | 対象のケース選択はresource/reservation/auth等の名前部分一致とanonymousへのfallback。[対象][S-DESIGN] | **是正**: 関係のないテストを付けて欠落を隠さず、operation/因子/assertionの明示対応を検査する | REQ-ASBUILT-013/020/028 |
| DOC-12 | 生成rootは隔離されるがAPI54帳票には個別の生成元・更新command・直接編集禁止表示がない | **是正**: 各帳票から導出元と再生成方法を識別できる表示を付ける。参照にも表示の一部欠落があるため強い既存要件を維持 | REQ-ASBUILT-003 |
| DOC-13 | 対象は全9APIの6帳票とgroup/API索引を生成する | **維持**: 参照healthのinterfaceのみへ退行させない。ファイル名・root名の文字列一致ではなく情報とリンクを揃える | REQ-ASBUILT-023/025 |

### 3.3 CRUD行列と図

| ID | lazunex基準とSlotKeeperの差 | 判定・必要な是正 | 正本要件 |
|---|---|---|---|
| CRUD-01 | 参照はAPI×全DDLテーブルの横持ち。対象はoperation/resource/accessの縦持ち。[参照][L-CRUD] / [対象][S-CSV] | **是正**: CSV/Markdownを行列へ。縦持ちモデルは内部表現として保持できる | REQ-ASBUILT-006/024 |
| CRUD-02 | 参照DBは39テーブル列を保持。対象はアクセス行からしか資源集合を得られず未使用表が落ちる | **是正**: 全資源inventoryと全operationを独立宣言し、空セルとno-access理由を保持する | REQ-ASBUILT-024/032 |
| CRUD-03 | 参照は外部サービス3種も別行列。対象はDB SQLのみ。[参照][L-EXT] / [対象][S-DESIGN] | **是正**: DB/外部種別と保存先group別の行列を生成。認証通信等は意味を分類し、非該当は理由と適用性テストで説明する | REQ-ASBUILT-006/024/036 |
| CRUD-04 | 参照セルはC→R→U→D順。対象モデルのsortは文字順になり得る | **是正**: 複数操作は集合で保持し、表示順をCRUDに固定する | REQ-ASBUILT-024 |
| CRUD-05 | 対象CRUD図はMermaid fenceなし、同じAPI/表を行ごとに再作成。[図][S-GRAPH] | **是正**: 補助図はMermaid fence、安定ID、一意node、保存先groupで描く。主成果物の行列を置換しない | REQ-ASBUILT-024 |
| CRUD-06 | 対象はRもAPI→表方向、healthを「-」へのNONEとして描く | **是正**: データ方向をR=資源→API、C/U/D=API→資源と明示。非アクセスを架空の資源/edgeにしない | REQ-ASBUILT-024 |
| CRUD-07 | 対象のSQL接続はファイル全体の正規表現、証拠行は一律4行目、unresolvedは固定空 | **是正**: 呼出所有と到達性、SQL句/SDK操作の実位置を解析。unknownはno-accessに変換せず失敗にする | REQ-ASBUILT-024/032; REQ-DESIGN-009/016 |
| CRUD-08 | 対象にもmodel/CSV/表/図/evidenceの一致検査はある | **維持・補強**: 同一モデルからの決定的生成は維持。意味が間違ったモデル同士の一致だけでは完了にしない | REQ-ASBUILT-001/024/036 |

### 3.4 実装構成・責務

| ID | lazunex基準とSlotKeeperの差 | 判定・必要な是正 | 正本要件 |
|---|---|---|---|
| IMPL-01 | 参照はrouter→business functions→query/integration。対象endpoint内のwork callbackがqを直接呼ぶ。[参照][L-ROUTER] / [business][L-FUNCTIONS] / [対象][S-ENDPOINT] | **是正**: 全体順序とHTTP境界はendpoint、業務処理とSQL呼出はoperation所有businessへ。callback内も対象 | REQ-DESIGN-001/009/011 |
| IMPL-02 | 対象endpointでhash、入力の業務判定、保存結果からの応答組立を実施 | **是正**: business/response責務へ分け、移動後も冪等性・認可・OCC・commit後応答を維持する | REQ-DESIGN-009/011 |
| IMPL-03 | 参照はoperation所有schema/sample/contract等。対象はAPI固有の入出力型もdomain.pyへ集約。[対象][S-DOMAIN] | **是正**: API固有と共有domainを区別し所有を明示。ファイル名や関数名の完全一致は求めない | REQ-DESIGN-008/010/014/024 |
| IMPL-04 | 対象は登録endpointの一部構文のみ検査。未登録helper・同一fileの別定義・別名importへの網羅性がない。[生成器][S-DESIGN] | **是正**: 宣言source全体で定義・import・call・専用symbol所有とAPI間依存を検査する | REQ-DESIGN-014/015/016 |
| IMPL-05 | 参照はbool条件・無視戻り値・定数bool等の専用checker。対象guardには同等の負例がない。[参照規則][L-RULES] / [対象tests][S-GUARDS] | **是正**: 条件値、戻り値利用、例外捕捉、禁止依存の実source負例を用意する | REQ-DESIGN-018/019/020/021/022 |
| IMPL-06 | 対象DomainErrorはHTTP statusを含む。[domain][S-DOMAIN] / [境界][S-APP] | **是正**: 業務コード・業務例外とtransport上のresponse mappingの所有を分ける。公開API互換を保つ | REQ-DESIGN-009/021; REQ-ASBUILT-027 |
| IMPL-07 | 参照はintegrationのport/client/fake/schema/mapperと明示した境界。対象authは具体PyJWKClientを直接保持。[参照][L-INTEGRATIONS] / [対象][S-AUTH] | **是正**: 外部作用と差替・異常系テストの境界を明示する。既存FastAPI依存注入まで否定しない | REQ-DESIGN-009/010; REQ-ASBUILT-027 |
| IMPL-08 | 対象は共通middlewareのrequest_resultログ中心。参照は運用messageと型付きログ規約を検査。[参照][L-LOGRULE] / [対象][S-APP] | **是正**: 業務結果と運用ログの対応・level・ID・項目型を検査。token/目的/生例外等の非出力は維持 | REQ-DESIGN-013; REQ-ASBUILT-027 |
| IMPL-09 | SQL生成物の置場は参照generated配下＋互換shim、対象はoperation直下queries.py | **適応**: 生成所有・入力・出力全体のdriftが検査できれば直下を禁止しない。既存shimを新規要件にしない | REQ-ASBUILT-003/035; REQ-DESIGN-024 |
| IMPL-10 | 参照MySQL/AWS mockと対象PostgreSQL/DSQL/Keycloak・React/Astro/CDKが異なる | **適応・維持**: DB方言、認証方式、技術stackは対象要件。設計情報を同等にし、参照へ置換して機能/安全性を失わない | REQ-DESIGN-024; REQ-ASBUILT-036 |

### 3.5 SQL・検証・閲覧

| ID | lazunex基準とSlotKeeperの差 | 判定・必要な是正 | 正本要件 |
|---|---|---|---|
| SQL-01 | 参照はSQL/DDLからquery固有のParams/Result。対象はSQLヘッダ指定と共有行modelを利用。[参照][L-QUERY] / [対象][S-QUERIES] | **是正**: 各SQLの投影・型・NULLと結果型を対応させ、全行modelへの不要な拡張を強制しない | REQ-DESIGN-012/017 |
| SQL-02 | 対象にも厳密な引数照合、DDL検査、SELECT *拒否があるが解析対応範囲は限定的。[検査][S-SQL] | **維持・補強**: 対応SQL構文の正負例を明示し、未対応を型検証済みとしない | REQ-DESIGN-004/012/017; REQ-ASBUILT-032 |
| SQL-03 | 対象query生成checkは現存SQLから生成したfile中心で、削除operation等の旧生成物集合検査が不十分 | **是正**: query生成の所有root/出力集合にも欠落・変更・余剰の3種検査を適用する | REQ-ASBUILT-002/035 |
| TEST-01 | 対象の帳票収集はPython AST関数/Vitest describe/Playwright title中心。[生成器][S-DESIGN] | **是正**: 実collector単位・parameterized case・assertionの意味と対応させ、suite名を実caseと誤認しない | REQ-ASBUILT-013/020/028 |
| TEST-02 | 対象には実pytest collectorとrun identity・欠落/失敗判定が別途存在する。[collector][S-COLLECTOR] / [evidence][S-EVIDENCE] | **維持**: 既存の実行証跡を利用し、帳票の推測case一覧と混ぜない。共通適合テストの成功を業務テスト成功にしない | REQ-ASBUILT-031/036; REQ-EVIDENCE-002 |
| TEST-03 | 参照のE2Eはscenario・具体step/値・期待結果・evidenceの対応を生成/検査。対象は主にtitle/trace/実行portal。[参照][L-E2E] / [対象][S-DESIGN] | **是正**: 実手順、設定値、失敗の発生方法、状態変化・期待結果を説明し、実case/evidenceへ結ぶ | REQ-ASBUILT-008; REQ-EVIDENCE-002 |
| TEST-04 | 対象の既存guardはdrift/trace/SQL差分/証跡整合が中心。[tests][S-GUARDS] | **是正**: 見出しだけ同じsample、到達不能ログ、誤test対応、direct query、SQL返却型、constant bool等を変更して失敗することを試す | REQ-ASBUILT-036 |
| DATA-01 | 参照はテーブル別の詳細項目とER。対象はDATA.md＋database.jsonで型/NULL/PKとDDL全文中心。[参照][L-TABLE] / [対象][S-DATA] | **是正**: default/unique/index/説明/関連を閲覧単位へ導出し、DB契約との差を検査する | REQ-ASBUILT-007 |
| DATA-02 | 対象portalにentity cardと関係一覧・拡大操作はあるが、関係線を描くER構造ではない。[portal][S-PORTAL] / [参照][L-ER] | **是正**: ER関係表示とAPI CRUDを区別し、多重度/保証元を明示して閲覧可能にする。ブラウザ実行は本監査では未実施 | REQ-ASBUILT-007; REQ-EVIDENCE-004 |
| DATA-03 | 対象はlogical-relations.jsonのアプリ保証と物理FKを明確に区別する | **維持**: DSQLへ存在しない物理FKを追加/図示しない。物理制約と論理参照は別種別で保持する | REQ-ASBUILT-007 |
| VIEW-01 | 対象frontend/infra設計にはregex抽出・固定説明・raw CDK Propertiesがある。[生成器][S-DESIGN] | **補強**: 参照に同じsurfaceはないため単純copyせず、画面操作・権限/状態・API接続、インフラ責務を対象adapterで検証する | REQ-ASBUILT-021/029/032 |
| VIEW-02 | 対象のsource hash・非破壊check・旧帳票除去・公開allowlist・Compose入口は既に存在。[README][S-README] / [verify][S-VERIFY] | **維持**: 一致した部分まで巻き戻さない。公開やCIを新たなportable必須設定にしない | REQ-ASBUILT-001/002/035; REQ-EVIDENCE-002 |

上記は **48項目**（参照5、帳票13、CRUD8、構成10、SQL3、テスト4、データ3、閲覧2）の差分・採用判断である。

## 4. 参照の不足をそのまま正にしない

以下4件は上の是正差分とは別の「基準の解釈」である。

| ID | 確認内容 | 採用判断 |
|---|---|---|
| REF-GAP-01 | lazunexのDB CRUDは未知テーブルを、external CRUDは未知methodをcontinueで落とす。[DB][L-CRUD] / [外部][L-EXT] | 不採用。未対応/未解決をreportし、アクセスなしへ読み替えない |
| REF-GAP-02 | list_projectsの実装は権限NGでearly returnし、catchで別応答を返すが、生成sequenceは権限説明のalt内に正常処理等を平坦化している。[実装][L-ROUTER] / [図][L-SEQOUT] | 不採用。参照図のbyte再現ではなく、実制御flowを正とする。既存REQ-ASBUILT-026を弱めない |
| REF-GAP-03 | healthは両repositoryともmain/app側のsystem operation。参照では6帳票も揃わない。[参照][L-MAIN] / [対象][S-APP] | system operationの明示所有と非該当を認め、架空SQLやbusiness functionを作らない。対象の6帳票は維持 |
| REF-GAP-04 | 日本語識別子辞書、業務literal、pytest雛形、queries互換shim、MySQL/AWSサービス名は参照固有 | 可搬的な意味・責務だけ採用。Python専用解析器の再配布やMarkdown規範の第二正本化は行わない |

外部作用・ログprivacy・既存の公開API/transaction保証と衝突する場合は、見た目を揃えるためにそれらを落とさない。
参照由来のREQ-ASBUILT-015/016は従来どおりadvisoryとし、今回の共通検査で新しい一律blocking gateに変えない。

## 5. 今回の標準修正

### 正本と実装の対応

- catalog revision 19: 既存23要件のrevisionを更新し、新規 **REQ-ASBUILT-036** を追加する。既存IDと受入条件を保持し、差分条件を追加する。
- `generate-implementation-design` のQuint契約・Skill・依存assets・hashと派生表示を同期する。既定Skill数、3本柱、導入先のCI/branch/merge所有は変えない。
- **manifest v3**: primary reference、固定baseline、ruleごとに別の導入先受入条件、独立した意味検査commandを必須化する。67参照ruleには補助的なruleも含む。非該当は対象要件・理由・適用性の正負例を必要とする。
- **CRUD model v2**: 全operation/全資源のinventory、DB/外部group、C/R/U/D集合、根拠、非アクセス、未解決状態から行列・保存先別行列・補助図を一貫生成する。
- 新規一時reportへ検査を実行し、共通側source digest・実在test位置・collector単位・正負例・欠落/失敗/skip/not-runを照合する。旧v2は `--legacy-layout-only` として明示的に診断するだけで、API適合完了とはしない。

詳細な機械契約と導入手順は [conformance.md](../../../.agents/skills/generate-implementation-design/references/conformance.md) を参照する。

### 完了と未完了の境界

このPRで実装するのは言語非依存の契約・出力表現・新規実行結果の検査である。
**52個のPython checkerを汎用移植したわけでも、67ruleの意味を共通検査器が解析するわけでもない。**
API/SQL/framework固有の意味検査は導入先adapterで実装する。fixtureの正負例は共通契約の回帰テストであり、SlotKeeperの業務適合証拠ではない。
trustedな実行commandが意図的に嘘の結果を生成することまでは暗号学的に防げない。source digestも宣言範囲の一致であって未宣言source不存在の証明ではない。
そのため、全source発見・fixtureの実意味・実テスト収集との対応は導入先レビューとadapter負例に残す。保存済み固定passへの後退は拒否する。

## 6. SlotKeeperを是正する実装順序

| 段階 | 必要な作業 | 次へ進む条件 |
|---|---|---|
| 1. 基準を固定 | 本監査版lazunexをprimaryにし全52toolsを棚卸し。67ruleを個別の導入先受入条件へ対応 | KotoRelay補助参照を残してもprimaryが一致し、曖昧な非該当/単一AC集約がない |
| 2. 責務を分離 | endpoint/business/query/response/integrationと共有domainの所有を決め、実装を移す | 認可、冪等性、OCC retry、原子的commit、privacyの回帰テストを保持 |
| 3. 導出と検査 | concrete samples、フィールド表、factor/assertion、例外/log、SQL/DDL、全source依存のadapterを実装 | 各ruleに実collectorで動く正例・負例。名前部分一致や固定説明へfallbackしない |
| 4. 出力を更新 | 6帳票、全資源CRUD/group行列、補助図、ER、E2E詳細、各surfaceの設計を再生成 | check非破壊、クリーン2回生成、欠落/変更/余剰なし、全source根拠あり |
| 5. 意味適合を実行 | manifest v3のconformance commandを接続し、別runのfresh reportを照合 | required rule全件の正負例pass、非該当の適用性正負例pass、未対応は未完了 |
| 6. 業務検証を分離 | 既存Compose入口で対象に必要なunit/integration/E2E等を実行 | 実行結果と設計適合を別に報告し、実AWS未実行は未検証のまま記す |

旧帳票を残したまま新形式だけ追加して「移行済み」にしない。移行前後の公開API・SQL型・例外応答の互換と生成所有を確認して切り替える。
この監査依頼はSlotKeeperの直接修正やmerge許可ではないため、本PRから対象repositoryの変更を開始しない。

## 7. 再現方法と検証範囲

固定commitをcheckoutした作業tree、またはその `git archive` 出力を渡す。ローカルの無関係なファイルを除いたexportを推奨する。

```bash
python tools/check_lazunex_audit.py --lazunex /path/to/lazunex-export --slotkeeper /path/to/SlotKeeper-export
python tools/quintflow.py generate
python tools/quintflow.py check
python -m unittest discover -s tests -p 'test_lazunex_conformance.py' -v
make verify PYTHON=python
```

監査では全1,136 blobの一致を実測した。標準検査の最終実行結果・commitはPRに記録する。
**SlotKeeper/lazunexのDocker Compose、実DB、実AWS、ブラウザE2Eは本監査では実行していない。**
文書・ソース・生成器・既存テスト定義の静的比較を、対象製品の実行成功と混同しない。

[L-CRUD]: https://github.com/tsuji-tomonori/lazunex/blob/096e1e580ab1c0670c57e4febad2bd9fdd4698ee/src/tools/generate_db_crud.py
[L-EXT]: https://github.com/tsuji-tomonori/lazunex/blob/096e1e580ab1c0670c57e4febad2bd9fdd4698ee/src/tools/generate_external_crud.py
[L-SEQ]: https://github.com/tsuji-tomonori/lazunex/blob/096e1e580ab1c0670c57e4febad2bd9fdd4698ee/src/tools/generate_api_sequences.py
[L-DETAIL]: https://github.com/tsuji-tomonori/lazunex/blob/096e1e580ab1c0670c57e4febad2bd9fdd4698ee/src/tools/generate_api_detail_design.py
[L-IF]: https://github.com/tsuji-tomonori/lazunex/blob/096e1e580ab1c0670c57e4febad2bd9fdd4698ee/src/tools/generate_openapi_if_specs.py
[L-FACTORS]: https://github.com/tsuji-tomonori/lazunex/blob/096e1e580ab1c0670c57e4febad2bd9fdd4698ee/src/tools/generate_api_unit_test_factors.py
[L-MSG]: https://github.com/tsuji-tomonori/lazunex/blob/096e1e580ab1c0670c57e4febad2bd9fdd4698ee/src/tools/generate_api_message_catalog.py
[L-QUERY]: https://github.com/tsuji-tomonori/lazunex/blob/096e1e580ab1c0670c57e4febad2bd9fdd4698ee/src/tools/generate_queries.py
[L-QUERYDOC]: https://github.com/tsuji-tomonori/lazunex/blob/096e1e580ab1c0670c57e4febad2bd9fdd4698ee/src/tools/generate_query_specs.py
[L-TABLE]: https://github.com/tsuji-tomonori/lazunex/blob/096e1e580ab1c0670c57e4febad2bd9fdd4698ee/src/tools/generate_db_table_specs.py
[L-ER]: https://github.com/tsuji-tomonori/lazunex/blob/096e1e580ab1c0670c57e4febad2bd9fdd4698ee/src/tools/generate_db_er_diagram.py
[L-ROUTER]: https://github.com/tsuji-tomonori/lazunex/blob/096e1e580ab1c0670c57e4febad2bd9fdd4698ee/src/app/apis/projects/list_projects/router.py
[L-FUNCTIONS]: https://github.com/tsuji-tomonori/lazunex/blob/096e1e580ab1c0670c57e4febad2bd9fdd4698ee/src/app/apis/projects/list_projects/functions.py
[L-SAMPLE]: https://github.com/tsuji-tomonori/lazunex/blob/096e1e580ab1c0670c57e4febad2bd9fdd4698ee/src/app/apis/projects/list_projects/samples.py
[L-SEQOUT]: https://github.com/tsuji-tomonori/lazunex/blob/096e1e580ab1c0670c57e4febad2bd9fdd4698ee/docs/spec/40.apis/projects/list_projects/sequence_gen.md
[L-MAIN]: https://github.com/tsuji-tomonori/lazunex/blob/096e1e580ab1c0670c57e4febad2bd9fdd4698ee/src/app/main.py
[L-RULES]: https://github.com/tsuji-tomonori/lazunex/blob/096e1e580ab1c0670c57e4febad2bd9fdd4698ee/src/tools/rulecheck/builtin_checks.py
[L-LOGRULE]: https://github.com/tsuji-tomonori/lazunex/blob/096e1e580ab1c0670c57e4febad2bd9fdd4698ee/docs/rule/coding/05_router_sequence_and_logging.md
[L-INTEGRATIONS]: https://github.com/tsuji-tomonori/lazunex/blob/096e1e580ab1c0670c57e4febad2bd9fdd4698ee/docs/rule/coding/08_integrations.md
[L-E2E]: https://github.com/tsuji-tomonori/lazunex/blob/096e1e580ab1c0670c57e4febad2bd9fdd4698ee/src/tools/generate_e2e_scenarios.py
[L-EVIDENCE]: https://github.com/tsuji-tomonori/lazunex/blob/096e1e580ab1c0670c57e4febad2bd9fdd4698ee/src/tools/check_e2e_case_evidences.py
[L-README]: https://github.com/tsuji-tomonori/lazunex/blob/096e1e580ab1c0670c57e4febad2bd9fdd4698ee/README.md
[S-ADOPTION]: https://github.com/tsuji-tomonori/SlotKeeper/blob/1b7590fb671df765e62fcf82f158a0ba94bd713d/.dev-standard/reference-adoption.json
[S-MANIFEST]: https://github.com/tsuji-tomonori/SlotKeeper/blob/1b7590fb671df765e62fcf82f158a0ba94bd713d/.dev-standard/design.json
[S-DESIGN]: https://github.com/tsuji-tomonori/SlotKeeper/blob/1b7590fb671df765e62fcf82f158a0ba94bd713d/tools/project/design.py
[S-ENDPOINT]: https://github.com/tsuji-tomonori/SlotKeeper/blob/1b7590fb671df765e62fcf82f158a0ba94bd713d/backend/src/slotkeeper/operations/reservations_create/endpoint.py
[S-DOMAIN]: https://github.com/tsuji-tomonori/SlotKeeper/blob/1b7590fb671df765e62fcf82f158a0ba94bd713d/backend/src/slotkeeper/domain.py
[S-DB]: https://github.com/tsuji-tomonori/SlotKeeper/blob/1b7590fb671df765e62fcf82f158a0ba94bd713d/backend/src/slotkeeper/db.py
[S-APP]: https://github.com/tsuji-tomonori/SlotKeeper/blob/1b7590fb671df765e62fcf82f158a0ba94bd713d/backend/src/slotkeeper/app.py
[S-AUTH]: https://github.com/tsuji-tomonori/SlotKeeper/blob/1b7590fb671df765e62fcf82f158a0ba94bd713d/backend/src/slotkeeper/auth.py
[S-QUERIES]: https://github.com/tsuji-tomonori/SlotKeeper/blob/1b7590fb671df765e62fcf82f158a0ba94bd713d/tools/project/queries.py
[S-SQL]: https://github.com/tsuji-tomonori/SlotKeeper/blob/1b7590fb671df765e62fcf82f158a0ba94bd713d/tools/project/sql_contract.py
[S-GUARDS]: https://github.com/tsuji-tomonori/SlotKeeper/blob/1b7590fb671df765e62fcf82f158a0ba94bd713d/tools/tests/test_guards.py
[S-COLLECTOR]: https://github.com/tsuji-tomonori/SlotKeeper/blob/1b7590fb671df765e62fcf82f158a0ba94bd713d/tools/project/collector.py
[S-EVIDENCE]: https://github.com/tsuji-tomonori/SlotKeeper/blob/1b7590fb671df765e62fcf82f158a0ba94bd713d/tools/project/evidence.py
[S-VERIFY]: https://github.com/tsuji-tomonori/SlotKeeper/blob/1b7590fb671df765e62fcf82f158a0ba94bd713d/tools/project/verify.py
[S-PORTAL]: https://github.com/tsuji-tomonori/SlotKeeper/blob/1b7590fb671df765e62fcf82f158a0ba94bd713d/portal/src/pages/database.astro
[S-CSV]: https://github.com/tsuji-tomonori/SlotKeeper/blob/1b7590fb671df765e62fcf82f158a0ba94bd713d/docs/design/generated/crud/matrix.csv
[S-GRAPH]: https://github.com/tsuji-tomonori/SlotKeeper/blob/1b7590fb671df765e62fcf82f158a0ba94bd713d/docs/design/generated/crud/diagram.md
[S-DATA]: https://github.com/tsuji-tomonori/SlotKeeper/blob/1b7590fb671df765e62fcf82f158a0ba94bd713d/docs/design/generated/DATA.md
[S-README]: https://github.com/tsuji-tomonori/SlotKeeper/blob/1b7590fb671df765e62fcf82f158a0ba94bd713d/README.md
