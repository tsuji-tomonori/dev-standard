# as-built設計標準

- 標準ID: `DEVSTD-AS-BUILT`
- 版: `2026-09-06`
- 適用対象: このrepositoryから標準を導入するrepository
- 機械可読checkの正本: `governance/checks/catalog.yaml`
- 永続要件の正本: `spec/requirements/requirements.qnt`
- 永続要件の機械可読view: `spec/requirements/requirements.json`
- 判断記録: `docs/decisions/ADR-0001-as-built-design-authority-and-scope.md`

本標準は、実装と1対1で対応する設計情報を実装成果物から決定論的に生成し、乖離をcheck modeで検知するための実装規約・テスト規約を定める。永続要件、check定義、開発フローの第二正本にはしない。check modeはローカルで実行でき、導入先に既存CIがある場合だけそこで再利用できる。本標準はCI、required check、branch、merge ruleを要求しない。

## 1. 適用モデル

この文書は人が読む標準ビューである。要件IDの定義は`spec/requirements/requirements.qnt`、その機械可読viewは`spec/requirements/requirements.json`、check ID・class・timing・trigger・enforcementは`governance/checks/catalog.yaml`を参照する。

この標準を配布または改訂しただけでは、dev-standard自身や導入先repositoryの既存コードへ以下のレイアウト規約やテスト構造を遡及強制しない。repositoryが具体的なartifact・code scopeを採用する場合はscope・除外を対象repositoryの既存方式で記録し、Advisoryから実測を開始する。既存コードへ適用する場合は、移行範囲と互換性を別変更として定義する。

### 1.1 規範語彙

| 語彙 | 意味 |
|---|---|
| MUST / MUST NOT | 採用済みscope内で満たす、または禁止する規範上の必須条件 |
| SHOULD / SHOULD NOT | 採用済みscope内で通常満たす推奨条件。逸脱する場合は具体的理由を記録する |
| MAY | 選択可能で、未採用を違反としない条件 |

規範行は`<領域>-<DO|DONT>-NNN`形式の一意なRule IDを持つ。規範行と自動検査の対応は本書の`Check ID`列で示し、実行定義はcatalogへ集約する。規範行では「適切に」「必要に応じて」「原則として」など、機械的な判定条件を欠く語を使用しない。

### 1.2 規範強度・採用scope・enforcement

規範強度、採用scope、check classは独立した軸である。

| 軸 | 決定するもの | 正本 |
|---|---|---|
| 規範強度 | 採用済みscopeで何をMUST / SHOULD / MAYとするか | 本書のRule ID付き規範行 |
| 採用scope | どのartifact・code pathへ規範を適用するか、何を除外するか | 対象repositoryの既存方式 |
| enforcement state | いつ、どのriskで検査するか | 選択したcommandと検査範囲 |

`Invariant` / `Risk-selected` / `Advisory` / `Periodic`は規範語彙の別名ではない。MUSTに対応するcheckを段階導入中にAdvisoryとして評価しても、MUSTをSHOULDへ弱めたことにはならない。未採用scopeには規範を適用せず、採用または移行中scopeでは実測結果、欠陥予防効果、安定性、運用costを根拠にenforcementを昇格する。

標準contract自体の定義・改訂は`as_built_standard_change: true`、repositoryへの採用・scope拡張は`as_built_adoption: true`で表す。両方に該当する変更だけ両flagをtrueにする。

## 2. 基本原則

| Rule ID | Norm | 規則 | Check ID |
|---|---|---|---|
| `GEN-DO-001` | MUST | 設計情報をルーティング定義、OpenAPI、SQL、DDL、例外分岐、テスト、実行結果などの宣言済み一次情報から生成する。 | `FAST-006` |
| `GEN-DONT-001` | MUST NOT | 実装から生成できる現在状態を手書き設計書として複製しない。 | `FAST-006` |
| `GEN-DO-002` | MUST | 同一入力からバイト一致する出力を生成し、列挙順を固定し、タイムスタンプ・乱数・環境依存絶対パスを出力へ含めない。 | `FAST-006` |
| `GEN-DO-003` | MUST | 生成ロジックを1系統に保ち、書込み用generate modeと非0終了するcheck modeで共有する。 | `FAST-006` |
| `GEN-DO-004` | MUST | check modeはrepository内へ候補・lock・一時fileを作らず、差分がある生成物のrepository相対pathを列挙する。 | `FAST-006` |
| `GEN-DO-005` | MUST | Python等のプログラムコードはASTまたは同等の構造解析で抽出し、supported AST/CFGを明示する。分岐を構造として保持し、未呼出しnested定義、dynamic dispatch、short-circuit、loop等のunsupported surfaceを線形化せず拒否する。正規表現は宣言構文が固定された入力に限定する。 | `FAST-021` |
| `GEN-DO-006` | MUST | 自動生成物を`docs/design/generated/`へ隔離し、Markdown生成物を`.gen.md`で終端し、全Markdown生成物の先頭へ直接編集禁止・generate command・check commandを含むバナーを出力する。 | `FAST-006` |
| `GEN-DO-007` | MUST | README等へ生成内容を埋め込む場合は開始・終了markerの間だけを差し替える。 | `FAST-021` |
| `GEN-DO-008` | MUST | 対象列挙、table利用判定、error分岐導出など複数generatorが使う抽出ロジックを共有する。 | `FAST-021` |
| `GEN-DO-009` | SHOULD | generator自身のCLI仕様と処理flowを同じgenerator群から生成する。 | `FAST-021` |
| `GEN-DO-010` | MUST | canonical requirements JSON、生成scopeへ明示したapplicable active requirement ID集合、artifact側requirement metadata、明示trace、portable pytest collection manifestを完全照合し、requirement ID→operation/resource→collectable test nodeの決定的trace viewを生成する。catalog内の非applicable active要件を過剰要求せず、未知・inactive要件、未知artifact、manifestにないtest node、片方向だけのlinkを拒否する。 | `FAST-006` |

## 3. 生成対象と一次情報

最低生成対象を次に示す。Dev標準の導入・実装では、実際のAPI・data・infra・frontendを棚卸しし、実装が存在する必要領域をgenerate/check契約へ含める。generator未宣言・未接続は省略理由にしない。不足は既存generatorまたはproject adapterで補い、補完できない領域は未完了として報告する。実装が存在しない領域だけを理由付きで非該当とする。[導入・復旧手順](../../.agents/skills/generate-implementation-design/references/adoption.md)を適用し、レイアウト・定量閾値等の任意規約の採用とは区別する。

| 生成対象 | 一次情報 | 抽出契約 | 要件ID |
|---|---|---|---|
| API設計書 | router/handler AST、framework OpenAPI、sample定数、生SQL | handlerを起点に呼出順、構造化分岐、global error return、path/query/header parameter、interface、sample、unit-test観点を導出する。sequence図と処理stepを手書きしない。 | `REQ-ASBUILT-004` |
| API一覧 | handler decorator等の設計metadata | ASTまたはOpenAPIから重複のないoperation一覧を生成する。 | `REQ-ASBUILT-005` |
| CRUD図 | endpointから明示参照するSQL、外部client呼出AST | SELECT=R、INSERT=C、UPDATE=U、DELETE=Dとしてtable×APIと外部連携先×APIを導出し、未対応・多重対応・basename衝突・MERGE等のunsupported statementを拒否する。 | `REQ-ASBUILT-006` |
| DB設計書 | repository内の正本DDL、endpoint別SQL | table・column・table/column foreign keyを含むconstraint・ER関係をDDLから生成し、書込みAPIをSQL解析から導出する。 | `REQ-ASBUILT-007` |
| E2E scenario設計書 | E2E testのGiven/When/Then構造 | test codeをscenarioの正本としてstepと期待状態を生成する。 | `REQ-ASBUILT-008` |
| test evidence view | 対象repositoryが所有する結果JSON | status、response、DB結果、mock受信結果への参照だけを整形する。結果本文は保存せず、外部viewは導入先が既に所有し選択した場合だけ使う。 | `REQ-ASBUILT-009` |
| tool設計書 | tool entrypoint AST、呼出先docstring先頭1行 | CLI、制御flow、関数責務を生成する。 | `REQ-ASBUILT-010` |
| error case定義 | API設計生成時に導出したerror分岐 | literal code/case IDから生成scope全体で一意なmachine-readable IDを出力し、E2Eの`covers`宣言と網羅性checkへ使用する。 | `REQ-ASBUILT-011` |
| requirement trace | canonical requirements JSON、applicable ID集合、OpenAPI operationまたはCloudFormation resource metadata、明示trace JSON、test source | applicable active requirement IDから実装artifactを経てportable pytest collection nodeへ至るlinkを検査し、test manifestと決定的な表を生成する。 | `REQ-ASBUILT-020` |

## 4. 整合性check

| Rule ID | Norm | 規則 | Check ID / class |
|---|---|---|---|
| `ALIGN-DO-001` | MUST | 宣言済み生成対象の入力変更時にcheck modeを実行し、driftをblockingにする。 | `FAST-006` / Invariant |
| `ALIGN-DO-002` | MUST | API・OpenAPI・sample変更時に、handler登録、設計metadata、error分岐、error sampleの三点整合を検査する。 | `FAST-016` / Risk-selected |
| `ALIGN-DO-003` | MUST | 設計へ掲載する正常・異常sampleが対応testから参照され、branch-awareかつ再代入で失効するprovenanceにより実responseとのassertへ接続されることを検査する。明示adapterはauthority IDと認識済みruntime client呼出を持つ場合だけ信頼する。 | `FAST-017` / Risk-selected |
| `ALIGN-DO-004` | MUST | CRUD図でDBのC/U/Dを持つAPIはDB状態を、変更を伴う外部連携を持つAPIは外部状態を、それぞれ対応するE2E assertionで検証する。異常系もeffectごとに状態不変または理由付き許可変化を検証する。 | `FAST-018` / Risk-selected |
| `ALIGN-DO-005` | MUST | formatter、type、lint、unit test、coverage、design check、sample整合、E2E整合から、変更に関係すると選択されたcheckだけを個別または明示した集合で実行できるようにする。 | catalogで選択されたcheck |
| `ALIGN-DO-006` | MUST | 各as-built checkは個別結果をstdoutへ返し、選択結果の集約は`inspect-quality-gates`へ一本化する。導入先が既存の外部report viewを所有し選択した場合だけ、そのviewへ参照を渡す。portable runtimeはCI固有の外部pathへ直接書き込まない。 | `FAST-023` |

`FAST-016`から`FAST-018`は対象artifactとriskに応じて選択する。該当しないPRで形式的なN/Aを作らない。

## 5. 実装規約

SQLを使うAPIへのDev標準導入・新規作成・再編では、[SQLと説明コメントの契約](../../.agents/skills/generate-implementation-design/references/sql-and-language.md)を完了条件として適用する（`REQ-DESIGN-007`、`REQ-DOCS-002`）。API別SQLを正本にDDL/SQL由来の型付きqueryを生成し、関連lint・境界・生成差分・DBテストを検証する。説明コメント・docstring・生成ヘッダーは別言語の明示指示がなければ日本語とし、生成元から修正する。

### 5.1 endpoint縦割り

| Rule ID | Norm | 規則 | Check ID |
|---|---|---|---|
| `IMPL-DO-001` | SHOULD | endpointごとにdirectoryを分け、`router.py`、任意の`functions.py`、`schemas.py`、`samples.py`、`sql/NNN_<name>.sql`、`generated/queries.py`を配置する。 | `FAST-021` |
| `IMPL-DO-002` | SHOULD | `router.py`へroute定義、業務処理のorchestration、設計metadataを置き、処理順序を1関数から追跡可能にする。 | `FAST-021` |
| `IMPL-DO-003` | SHOULD | `functions.py`をrouterから直接呼ぶ単一責務関数だけで構成し、全関数へflow labelになるdocstring先頭1行を付ける。 | `FAST-021` |
| `IMPL-DONT-001` | SHOULD NOT | `functions.py`にclassまたは静的に追跡できないdynamic dispatchを置かない。補助関数間の呼出はASTで再帰展開できる直接呼出に限定し、循環呼出を作らない。 | `FAST-021` |
| `IMPL-DO-004` | SHOULD | request/response型を`schemas.py`、OpenAPIとtestが共有する正常・異常sample定数を`samples.py`へ置く。 | `FAST-021` |
| `IMPL-DO-005` | SHOULD | SQLを`sql/NNN_<name>.sql`へ1file 1 supported statementで置き、先頭行へ自然言語の概要commentを付け、operationから一意なrepository-relative pathで明示参照する。basename参照はSQL root内で一意の場合だけ使用する。 | `FAST-021` |
| `IMPL-DONT-002` | MUST NOT | `generated/queries.py`を直接編集しない。 | `FAST-006` |
| `IMPL-DO-006` | SHOULD | API番号、権限、業務概要等の設計metadataをroute decoratorの拡張属性へ置き、別の手書き契約書を作らない。 | `FAST-016` |

### 5.2 layer分離

| Rule ID | Norm | 規則 | Check ID |
|---|---|---|---|
| `LAYER-DO-001` | SHOULD | router関数へDI、SQL wrapper呼出、外部client呼出、commit、rollback、error response、補助関数呼出を順序どおり記述する。 | `FAST-021` |
| `LAYER-DONT-001` | SHOULD NOT | router関数から生SQL、外部SDK、標準logger、`print`を直接使用しない。 | `FAST-021` |
| `LAYER-DONT-002` | SHOULD NOT | router関数で未正規化の`raise`または例外の握り潰しを行わない。許可する例外処理はrollback、重大log、正規化error response returnの順序に限定する。 | `FAST-021` |
| `LAYER-DO-002` | SHOULD | 外部SDKまたはHTTP clientのimportをservices層へ限定する。 | `FAST-021` |

### 5.3 DBアクセス

| Rule ID | Norm | 規則 | Check ID |
|---|---|---|---|
| `DB-DO-001` | SHOULD | queryの正本を名前付きparameterを使うSQL fileとし、CRUD解析対象にする。 | `FAST-010` |
| `DB-DO-002` | SHOULD | unit test用DBとproduction系DBの両方で実行できるdialect-neutral SQLを使用する。 | `FAST-021` |
| `DB-DO-003` | SHOULD | dialect依存SQLを識別tag付き別fileへ分離し、実行helperで選択する。 | `FAST-021` |
| `DB-DONT-001` | SHOULD NOT | 現在日時をDB関数から取得せず、applicationからparameterで渡す。 | `FAST-021` |

### 5.4 運用log

| Rule ID | Norm | 規則 | Check ID |
|---|---|---|---|
| `LOG-DO-001` | SHOULD | 全logを単一の運用logger経由で出力し、文字列literalの`message_id`を付与する。 | `FAST-021` |
| `LOG-DO-002` | SHOULD | `message_id`を`^[a-z0-9_]+(\.[a-z0-9_]+)+$`へ一致させる。 | `FAST-021` |
| `LOG-DO-003` | SHOULD | warning以上のlogへ発生条件、運用影響、対処を渡し、同名runbookへ概要、level、message例、発生条件、運用影響、確認手順、対処手順を記載する。 | `FAST-021` |
| `LOG-DO-004` | SHOULD | warning以上のmessage IDとrunbookを双方向に検査し、欠落と孤児文書を検出する。 | `FAST-021` |

### 5.5 generator tool規約

| Rule ID | Norm | 規則 | Check ID |
|---|---|---|---|
| `TOOL-DO-001` | SHOULD | generator entrypointを`tools.py`へ置き、制御flow、関数呼出、出力だけを記述する。 | `FAST-021` |
| `TOOL-DONT-001` | SHOULD NOT | `tools.py`へ式計算、文字列組立、file IOの具体処理を記述しない。 | `FAST-021` |
| `TOOL-DO-002` | SHOULD | generatorの実処理を`functions.py`の単一責務関数へ分け、全関数へdocstringを付ける。 | `FAST-021` |

### 5.6 定量閾値

標準値を次に示す。導入先が値を採用する場合、規約文書とmachine-readable設定を一致させる。変更理由は対象repositoryの既存方式またはADRへ記録する。生成コードとtestコードは対象外とする。

| 指標 | application層 | tool層 |
|---|---:|---:|
| 循環的複雑度/関数 | 10 | 12 |
| 制御nest深さ | 3 | 4 |
| 関数logical line | 50、routerのみ200 | 30 |
| file logical line | 400 | 500 |
| 引数数 | 3、routerはDI分を除外 | 8 |
| return数/関数 | 4、routerを除外 | 5 |
| 条件式内の`and`/`or` | 2 | 2 |
| 三項演算子nest | 0 | 0 |

| Rule ID | Norm | 規則 | Check ID |
|---|---|---|---|
| `LIMIT-DO-001` | SHOULD | 採用した定量閾値をmachine-readable設定へ保存する。 | `FAST-022` |
| `LIMIT-DO-002` | MUST | 定量閾値を変更した場合、標準値と設定値の一致checkを選択する。 | `FAST-022` |
| `LIMIT-DO-003` | SHOULD | 引数上限を超える入力を型とfield説明を持つparameter modelへまとめる。 | `FAST-021` |

## 6. 規約の機械化

| Rule ID | Norm | 規則 | Check ID |
|---|---|---|---|
| `RULE-DO-001` | MUST | checkのID、class、timing、trigger、acceptance、enforcementを`governance/checks/catalog.yaml`だけで定義する。 | `FAST-024` |
| `RULE-DONT-001` | MUST NOT | Markdown checker tagをcheck定義の第二正本として使用しない。 | `FAST-024` |
| `RULE-DO-002` | MUST | 汎用linterで表現できる規則をlinterへ委譲し、標準Rule ID、catalog check、linter設定の対応を検査する。 | `FAST-022` |
| `RULE-DO-003` | SHOULD | 行単位の抑制を`ignore[<RULE-ID>] 理由`形式にし、抑制箇所を生成一覧へ集約する。 | `AUD-008` |
| `RULE-DONT-002` | MUST NOT | 理由を持たないsilent suppressionを許可しない。 | `AUD-008` |

抑制一覧と採用checklistは機械生成可能なビューであり、catalogを置き換えない。抑制の反復、失効、不要化はGovernance Auditで確認する。

## 7. テスト規約

### 7.1 unit test規約

| Rule ID | Norm | 規則 | Check ID |
|---|---|---|---|
| `UT-DO-001` | SHOULD | `test_`関数の本体へ`# 1. 初期化`、`# 2. テストの実行`、`# 3. アサーション`をこの順で各1回記述する。 | `FAST-020` |
| `UT-DO-002` | SHOULD | 全test関数のdocstringへ前提と期待結果を1文で記述する。 | `FAST-020` |
| `UT-DO-003` | SHOULD | fixture、data投入関数、request builder、stubへ準備内容のdocstringを付け、data投入関数ではtableとkey値を記述する。 | `FAST-020` |
| `UT-DONT-001` | SHOULD NOT | test caseを`parametrize`またはloopで複数case実行せず、1 case 1 test関数にする。 | `FAST-020` |
| `UT-DO-004` | SHOULD | unit testを正本DDLから生成したin-memory DBと外部HTTP stubで実行し、実DBと実mock serverへ接続しない。 | `FAST-020` |
| `UT-DO-005` | SHOULD | C0命令網羅95%以上、C1分岐網羅90%以上を採用目標にする。 | `FAST-019` |
| `UT-DO-006` | MUST | `samples.py`の正常・異常sampleを、全到達分岐でprovenanceを保持する実responseとのassertへ接続し、fabricated valueへの再代入後はpassさせない。 | `FAST-017` |

`FAST-019`は採用またはscope拡張時のenforcement stateをAdvisoryから開始する。これは対応する規範強度を弱める意味ではない。実測で欠陥予防効果、測定安定性、運用costが確認された後だけ、`retrospect-and-improve`に従いRisk-selectedまたはInvariantへの昇格を検討する。

### 7.2 E2E test規約

| Rule ID | Norm | 規則 | Check ID |
|---|---|---|---|
| `E2E-DO-001` | SHOULD | E2E testへ`# Given(前提)`、`# When(操作)`、`# Then(結果)`をこの順で記述する。 | `FAST-020` |
| `E2E-DONT-001` | SHOULD NOT | E2E caseを`parametrize`またはloopで複数case実行せず、1 case 1 test関数にする。 | `FAST-020` |
| `E2E-DO-002` | MUST | API response、mock受信状態、DB SELECT結果の保存先を対象repositoryの既存方式で選び、設計viewには参照だけを含める。外部report基盤を新設または必須化しない。 | `FAST-023` |
| `E2E-DO-003` | MUST | 各error E2E testが`covers(<case-id>)`でerror case定義との対応を宣言し、未網羅caseを検出する。 | `FAST-018` |
| `E2E-DO-004` | MUST | 異常系で実行前後のDBと外部連携状態をeffect別に比較し、それぞれ状態不変または理由付きの許可変化をassertする。 | `FAST-018` |
| `E2E-DO-005` | SHOULD | 外部連携先の障害をmock serverのfault injectionで発生させる。 | `FAST-020` |

## 8. 開発フローへの接続

本書は独立した工程オーケストレーションを定義しない。入口は `chat-first-development` とする。下表の四軸は検査を選ぶ判断観点であり、`right-size-execution` の起動・runner・記録作成を通常変更に必須化しない。既存の有効な承認は再利用する。

| Rule ID | Norm | 規則 | 接続先 |
|---|---|---|---|
| `FLOW-DO-001` | MUST | 公開API、DB、generator、永続要件、governanceの変更範囲から`scope`を、artifact tagとrisk tagの和集合から`assurance`を独立に選び、対応するcheckだけを検証projectionへ含める。`compute`と`mode`は利用可能な証拠とauthority boundaryから別に選ぶ。 | `right-size-execution` |
| `FLOW-DONT-001` | MUST NOT | 公開API変更だけを理由にユーザー承認を要求しない。 | `authorize-autonomous-execution` |
| `FLOW-DO-002` | MUST | external write、production、削除、公開、merge、高額操作、または具体的な法令・契約上の義務ではauthority boundaryを明示し、実操作前に承認を得る。 | `authorize-autonomous-execution` |
| `FLOW-DONT-002` | MUST NOT | 通常のrepository変更へ日付+slug計画書、恒久work item、段階status更新を必須化しない。 | `chat-first-development` |
| `FLOW-DO-003` | MAY | 再開用の一時計画を`.devflow/run/`へ保存し、変更完了後に削除する。 | `chat-first-development` |
| `FLOW-DO-004` | MUST | コードから得られない長期判断をADRへ置き、変更説明とselected check結果は対象repositoryの既存方式へ簡潔に収束させる。 | `chat-first-development` |

## 9. 導入時のtrace

| 受入項目 | 要件ID | Check ID |
|---|---|---|
| 生成設計を`docs/design/generated/`へ隔離し、手書き複製を置かない | `REQ-ASBUILT-003` | `FAST-006` |
| 宣言済みgeneratorがcheck modeを持ちローカルまたは導入先が選んだ既存実行環境でdriftを検出する | `REQ-ASBUILT-001`, `REQ-ASBUILT-002` | `FAST-006` |
| 実装だけを変更して再生成しない場合にcheckが失敗する | `REQ-ASBUILT-002` | `FAST-006` |
| 規範Rule IDと選択可能なcheck定義が対象repositoryの既存方式へ接続される | `REQ-ASBUILT-017` | `FAST-024` |
| 抑制一覧を生成し監査する | `REQ-ASBUILT-018` | `AUD-008` |
| AAA/GWT、docstring、1 case 1関数を評価する | `REQ-ASBUILT-015` | `FAST-020` |
| C0 95%、C1 90%を採用目標として測定する | `REQ-ASBUILT-016` | `FAST-019` |
| sample、三点整合、CRUD/E2E整合を検査する | `REQ-ASBUILT-012`, `REQ-ASBUILT-013`, `REQ-ASBUILT-014` | `FAST-016`, `FAST-017`, `FAST-018` |
| applicable active requirement ID集合をoperation/resourceとportable pytest collection manifestのnodeへ完全追跡する | `REQ-ASBUILT-020` | `FAST-006` |
| test evidenceの参照だけをlocalまたは導入先が選択した既存viewへ集約する | `REQ-ASBUILT-009`, `REQ-ASBUILT-019` | `FAST-023` |

## 10. 変更管理

本標準の要件正本、Rule ID、既定path、生成対象、check mapping、generator contract、配布定義、traceを変更する場合は、変更範囲から四軸を選択し、`as_built_standard_change: true`に対応する`FAST-024`で正本間の整合を確認する。generatorの生成対象・出力も変える場合だけ`generated_change: true`と`FAST-006`を、定量閾値またはlinter delegationも変える場合だけ`quality_threshold_change: true`と`FAST-022`を検証projectionへ追加する。

repositoryが本標準を具体的なartifact・code scopeへ採用する、または適用scopeを拡張する場合は、採用scopeと除外を対象repositoryの既存方式で記録する。標準contractを変更しただけでは`FAST-019`〜`FAST-021`、`FAST-023`を選択しない。

checkをblockingへ昇格する判断は対象repositoryのauthorityに委任し、本標準のportable契約にはしない。

## APIの6帳票と単体テスト対応

APIの各operationには、詳細設計、OpenAPI interface、ログmessage、query、Mermaid sequence、要因別unit-test詳細の6帳票を生成する。内容・authority・adapterモデル・導入完了検査は[APIの6帳票契約](../../.agents/skills/generate-implementation-design/references/api-documents.md)に定める。関数呼出し一覧を詳細設計、HTTPエラー一覧をログ台帳、test node一覧を要因別テスト詳細の代わりにしない。
