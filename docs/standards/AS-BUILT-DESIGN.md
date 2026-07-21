# as-built設計標準

- 標準ID: `DEVSTD-AS-BUILT`
- 版: `2026-07-21`
- 適用対象: このrepositoryから標準を導入するrepository
- 機械可読checkの正本: `governance/checks/catalog.yaml`
- 永続要件の正本: `spec/requirements/requirements.json`
- 判断記録: `docs/decisions/ADR-0001-as-built-design-authority-and-scope.md`

本標準は、実装と1対1で対応する設計情報を実装成果物から決定論的に生成し、乖離をcheck modeとCIで検知するための実装規約・テスト規約を定める。永続要件、check定義、開発フローの第二正本にはしない。

## 1. 適用モデル

この文書は人が読む標準ビューである。要件IDの意味は`spec/requirements/requirements.json`、check ID・class・timing・trigger・enforcementは`governance/checks/catalog.yaml`を参照する。

この標準を配布しただけでは、dev-standard自身の既存`tools/`コードへ以下のレイアウト規約やテスト構造を遡及強制しない。導入先は変更対象とartifactに応じてcheckを選択し、Advisoryから実測を開始する。既存コードへ適用する場合は、移行範囲と互換性を別変更として定義する。

### 1.1 規範語彙

| 語彙 | 意味 |
|---|---|
| MUST / MUST NOT | 適用triggerに該当し、対応checkがblockingの場合に満たす必須条件 |
| SHOULD / SHOULD NOT | Advisoryとして評価し、修正・Issue・残存リスクへ収束させる条件 |
| MAY | 選択可能で、未採用を違反としない条件 |

規範行は`<領域>-<DO|DONT>-NNN`形式の一意なRule IDを持つ。規範行と自動検査の対応は本書の`Check ID`列で示し、実行定義はcatalogへ集約する。規範行では「適切に」「必要に応じて」「原則として」など、機械的な判定条件を欠く語を使用しない。

## 2. 基本原則

| Rule ID | Norm | 規則 | Check ID |
|---|---|---|---|
| `GEN-DO-001` | MUST | 設計情報をルーティング定義、OpenAPI、SQL、DDL、例外分岐、テスト、実行結果などの宣言済み一次情報から生成する。 | `FAST-006` |
| `GEN-DONT-001` | MUST NOT | 実装から生成できる現在状態を手書き設計書として複製しない。 | `FAST-006` |
| `GEN-DO-002` | MUST | 同一入力からバイト一致する出力を生成し、列挙順を固定し、タイムスタンプ・乱数・環境依存絶対パスを出力へ含めない。 | `FAST-006` |
| `GEN-DO-003` | MUST | 生成ロジックを1系統に保ち、書込み用generate modeと非0終了するcheck modeで共有する。 | `FAST-006` |
| `GEN-DO-004` | MUST | check modeは差分がある生成物のrepository相対pathを列挙する。 | `FAST-006` |
| `GEN-DO-005` | MUST | Python等のプログラムコードはASTまたは同等の構造解析で抽出し、正規表現を宣言構文が固定された入力に限定する。 | `FAST-021` |
| `GEN-DO-006` | MUST | 自動生成物を`docs/design/generated/`へ隔離し、Markdown生成物を`.gen.md`で終端し、全Markdown生成物の先頭へ直接編集禁止・generate command・check commandを含むバナーを出力する。 | `FAST-006` |
| `GEN-DO-007` | MUST | README等へ生成内容を埋め込む場合は開始・終了markerの間だけを差し替える。 | `FAST-021` |
| `GEN-DO-008` | MUST | 対象列挙、table利用判定、error分岐導出など複数generatorが使う抽出ロジックを共有する。 | `FAST-021` |
| `GEN-DO-009` | SHOULD | generator自身のCLI仕様と処理flowを同じgenerator群から生成する。 | `FAST-021` |

## 3. 生成対象と一次情報

最低生成対象を次に示す。導入先が該当artifactを持たない場合、その対象は生成対象へ宣言しない。宣言済み対象はgenerate/check契約へ含める。

| 生成対象 | 一次情報 | 抽出契約 | 要件ID |
|---|---|---|---|
| API設計書 | router/handler AST、framework OpenAPI、sample定数、生SQL | handlerを起点に呼出順、分岐、error return、interface、sample、unit-test観点を導出する。sequence図と処理stepを手書きしない。 | `REQ-ASBUILT-004` |
| API一覧 | handler decorator等の設計metadata | ASTまたはOpenAPIから重複のないoperation一覧を生成する。 | `REQ-ASBUILT-005` |
| CRUD図 | endpoint別SQL、外部client呼出AST | SELECT=R、INSERT=C、UPDATE=U、DELETE=Dとしてtable×APIと外部連携先×APIを導出する。 | `REQ-ASBUILT-006` |
| DB設計書 | repository内の正本DDL、endpoint別SQL | table・column・constraint・ER関係をDDLから生成し、書込みAPIをSQL解析から導出する。 | `REQ-ASBUILT-007` |
| E2E scenario設計書 | E2E testのGiven/When/Then構造 | test codeをscenarioの正本としてstepと期待状態を生成する。 | `REQ-ASBUILT-008` |
| test evidence view | 外部report基盤の結果JSON | status、response、DB結果、mock受信結果への参照を整形する。実行結果をrepositoryへ保存しない。 | `REQ-ASBUILT-009` |
| tool設計書 | tool entrypoint AST、呼出先docstring先頭1行 | CLI、制御flow、関数責務を生成する。 | `REQ-ASBUILT-010` |
| error case定義 | API設計生成時に導出したerror分岐 | machine-readable IDを出力し、E2Eの`covers`宣言と網羅性checkへ使用する。 | `REQ-ASBUILT-011` |

## 4. 整合性check

| Rule ID | Norm | 規則 | Check ID / class |
|---|---|---|---|
| `ALIGN-DO-001` | MUST | 宣言済み生成対象の入力変更時にcheck modeを実行し、driftをblockingにする。 | `FAST-006` / Invariant |
| `ALIGN-DO-002` | MUST | API・OpenAPI・sample変更時に、handler登録、設計metadata、error分岐、error sampleの三点整合を検査する。 | `FAST-016` / Risk-selected |
| `ALIGN-DO-003` | MUST | 設計へ掲載する正常・異常sampleが対応testから参照され、実responseとのassertに使われることを検査する。 | `FAST-017` / Risk-selected |
| `ALIGN-DO-004` | MUST | CRUD図でC/U/Dを持つAPIのE2E正常系がDBまたは外部連携先の状態を検証することを検査する。 | `FAST-018` / Risk-selected |
| `ALIGN-DO-005` | MUST | formatter、type、lint、unit test、選択されたcoverage、design check、sample整合、E2E整合をrepositoryのtask runnerから選択実行できるようにする。 | catalogで選択されたcheck |
| `ALIGN-DO-006` | MUST | 選択したtest、static analysis、規約check、coverageの結果を単一の外部workflowまたはreport viewへ集約し、repositoryには結果本文を複製しない。 | `FAST-023` |

`FAST-016`から`FAST-018`は対象artifactとriskに応じて選択する。該当しないPRで形式的なN/Aを作らない。

## 5. 実装規約

### 5.1 endpoint縦割り

| Rule ID | Norm | 規則 | Check ID |
|---|---|---|---|
| `IMPL-DO-001` | SHOULD | endpointごとにdirectoryを分け、`router.py`、任意の`functions.py`、`schemas.py`、`samples.py`、`sql/NNN_<name>.sql`、`generated/queries.py`を配置する。 | `FAST-021` |
| `IMPL-DO-002` | SHOULD | `router.py`へroute定義、業務処理のorchestration、設計metadataを置き、処理順序を1関数から追跡可能にする。 | `FAST-021` |
| `IMPL-DO-003` | SHOULD | `functions.py`をrouterから直接呼ぶ単一責務関数だけで構成し、全関数へflow labelになるdocstring先頭1行を付ける。 | `FAST-021` |
| `IMPL-DONT-001` | SHOULD NOT | `functions.py`にclassを定義せず、同一file内の補助関数から別の補助関数を呼び出さない。 | `FAST-021` |
| `IMPL-DO-004` | SHOULD | request/response型を`schemas.py`、OpenAPIとtestが共有する正常・異常sample定数を`samples.py`へ置く。 | `FAST-021` |
| `IMPL-DO-005` | SHOULD | SQLを`sql/NNN_<name>.sql`へ1file 1 statementで置き、先頭行へ自然言語の概要commentを付ける。 | `FAST-021` |
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

標準値を次に示す。導入先が値を採用する場合、規約文書とmachine-readable設定を一致させる。引下げは許可し、引上げはCommit CommentまたはADRへ理由を記録する。生成コードとtestコードは対象外とする。

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
| `RULE-DO-001` | MUST | checkのID、class、timing、trigger、acceptance、enforcementを`governance/checks/catalog.yaml`だけで定義する。 | `REV-007` |
| `RULE-DONT-001` | MUST NOT | Markdown checker tagをcheck定義の第二正本として使用しない。 | `REV-007` |
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
| `UT-DO-006` | MUST | `samples.py`の正常・異常sampleを実responseとのassertへ接続する。 | `FAST-017` |

`FAST-019`は導入時にAdvisoryとする。実測で欠陥予防効果、測定安定性、運用costが確認された後だけ、`retrospect-and-improve`に従いRisk-selectedまたはInvariantへの昇格を検討する。

### 7.2 E2E test規約

| Rule ID | Norm | 規則 | Check ID |
|---|---|---|---|
| `E2E-DO-001` | SHOULD | E2E testへ`# Given(前提)`、`# When(操作)`、`# Then(結果)`をこの順で記述する。 | `FAST-020` |
| `E2E-DONT-001` | SHOULD NOT | E2E caseを`parametrize`またはloopで複数case実行せず、1 case 1 test関数にする。 | `FAST-020` |
| `E2E-DO-002` | MUST | API response、mock受信状態、DB SELECT結果を外部report基盤へ添付し、repositoryへ実行結果を保存しない。 | `FAST-023` |
| `E2E-DO-003` | MUST | 各error E2E testが`covers(<case-id>)`でerror case定義との対応を宣言し、未網羅caseを検出する。 | `FAST-018` |
| `E2E-DO-004` | MUST | 異常系で実行前後のDBとmock状態を比較し、状態不変または理由付きの許可変化をassertする。 | `FAST-018` |
| `E2E-DO-005` | SHOULD | 外部連携先の障害をmock serverのfault injectionで発生させる。 | `FAST-020` |

## 8. 開発フローへの接続

本書は独立した工程オーケストレーションを定義しない。実行profileと進行は`chat-first-development`および`right-size-execution`を正本とする。

| Rule ID | Norm | 規則 | 接続先 |
|---|---|---|---|
| `FLOW-DO-001` | MUST | 公開API、DB、generator、永続要件、governanceを変更する場合は`assured`を選択し、artifact固有のRisk-selected checkを追加する。 | `right-size-execution` |
| `FLOW-DONT-001` | MUST NOT | 公開API変更だけを理由にユーザー承認を要求しない。 | `authorize-autonomous-execution` |
| `FLOW-DO-002` | MUST | external write、production、削除、公開、merge、高額操作、regulated条件ではauthority boundaryを明示し、実操作前に承認を得る。 | `authorize-autonomous-execution` |
| `FLOW-DONT-002` | MUST NOT | directまたはassured変更へ日付+slug計画書、恒久work item、段階status更新を必須化しない。 | `chat-first-development` |
| `FLOW-DO-003` | MAY | 再開用の一時計画を`.devflow/run/`へ保存し、変更完了後に削除する。 | `chat-first-development` |
| `FLOW-DO-004` | MUST | コードから得られない長期判断をADR、変更説明をCommit Comment、selected check結果をreview YAML、実行結果を外部CIへ収束させる。 | `chat-first-development` |

## 9. 導入時のtrace

| 受入項目 | 要件ID | Check ID |
|---|---|---|
| 生成設計を`docs/design/generated/`へ隔離し、手書き複製を置かない | `REQ-ASBUILT-003` | `FAST-006` |
| 全宣言済みgeneratorがcheck modeを持ちCIでdriftを検出する | `REQ-ASBUILT-001`, `REQ-ASBUILT-002` | `FAST-006`, `MRG-002` |
| 実装だけを変更して再生成しない場合にcheckが失敗する | `REQ-ASBUILT-002` | `FAST-006` |
| 規範Rule IDとcheck定義がcatalogへ接続される | `REQ-ASBUILT-017` | `REV-007` |
| 抑制一覧を生成し監査する | `REQ-ASBUILT-018` | `AUD-008` |
| AAA/GWT、docstring、1 case 1関数を評価する | `REQ-ASBUILT-015` | `FAST-020` |
| C0 95%、C1 90%を採用目標として測定する | `REQ-ASBUILT-016` | `FAST-019` |
| sample、三点整合、CRUD/E2E整合を検査する | `REQ-ASBUILT-012`, `REQ-ASBUILT-013`, `REQ-ASBUILT-014` | `FAST-016`, `FAST-017`, `FAST-018` |
| test evidenceを外部report基盤へ集約しrepositoryへ複製しない | `REQ-ASBUILT-009`, `REQ-ASBUILT-019` | `FAST-023` |

## 10. 変更管理

この標準のRule ID、既定path、生成対象、閾値、check mappingを変更する場合は`assured`を選択する。標準本文とmachine-readable設定の差分を`FAST-022`で確認する。checkをblockingへ昇格する場合は、実測evidence、適用trigger、予想cost、rollback、再評価日を記録する。
