# 参照実装の意味契約

参照の指定は配置だけの指定と解釈しない。固定SHAとoperation粒度に加え、routerの順序・分岐・例外・transaction、functionsの個別処理、schemas、response builder、SQL generator、型付きlogger、帳票の意味、実テストを比較する。各責務について適用・対象との差・adapter・具体的な適用外理由を導入先の既存設定へ残す。利用者の明示指定を一般的なSkill記述より優先する。既存の帳票構成profileだけの成功を意味上の適合と報告しない。

## routerの順序と境界

API全体とworkerで共有するフローの各入口を検査する。routerは名前のある個別stepを順番に呼び、分岐、フローの反復、例外境界とtransactionを所有する。functionsはDB/provider portを使う個別処理を担う。routerの反復を一律禁止しない。全体フローを一つのfunctions呼出しに隠さない。

API帳票モデルに次の`semantic_contract`を明示すると、共通generatorは手書きsequenceを使わず`api_flow.py`で実装から再構成する。`python_root`もモデルに必要。operation集合はOpenAPIと一致させる。

```json
{
  "operations": {
    "getItem": {
      "handler": "ops.items.read.router.get_item",
      "steps": ["ops.items.read.functions.load", "ops.items.read.response_builders.build"],
      "ports": ["db.execute"],
      "pure_calls": [],
      "transactions": ["transaction.commit", "transaction.rollback"],
      "sql_calls": {"ops.items.read.generated.queries.read": "src/ops/items/read/sql/read.sql"}
    }
  }
}
```

呼出しは解決済み完全名で指定する。内部実装をopaqueなport/pureとして隠せない。routerからDB/providerへ直接呼出し、step間の全体フロー委譲、step内のtransaction、複数のeffect呼出しを一つのstepへ集約した構造を拒否する。個別処理が複数effectを必要とする既存アルゴリズムは、境界を実証する対象adapterを用意する。workerの入口も`api_flow.inspect(index, config)`で同じ検査へ通す。

呼出し順は引数評価順を含む実ASTから抽出する。if、for/while、try/catch/else/finally、with、return/raiseをイベントとMermaidへ投影する。SQL矢印はSQL正本の先頭日本語コメントを使用する。未知call、再帰、動的call、comprehensionや短絡条件式は明示failする。定型の認可・commit・外部呼出しを追加しない。静的図はruntime実行証明ではない。

## SQLごとのParamsとRow

`sql_models.generate(ddl_text, {query_name: sql_text}, dialect)`は単一tableの明示列SELECT/INSERT/UPDATE/DELETEからquery専用のkeyword-only dataclassを返す。Paramsは実束縛名だけ、RowはSELECT投影列とaliasだけを持つ。型・NULLと余剰引数を実行時に拒否する。DDL全体の行型をquery引数・投影へ流用しない。

`semantic_contract.sql_models`に`ddl`、`queries`（query名→SQL path）、`output`、`dialect`を指定すると、現在のDDL/SQLから再生成して生成ファイルをbyte比較する。generatorの返り値を対象の既存生成commandでoutputへ書き出す。削除・手編集・SQL/DDL変更でcheckは失敗する。型をquery wrapperへ接続し、対象の型検査とDB実行で利用を実証する。

同梱実装はint/str/bool/floatの型と列レベルNULL/PK制約に限定する。JOIN、CTE、式投影、RETURNING、複合制約、未対応型は対象DDL/SQL adapterが必要であり、Anyやtable行型へfallbackしない。DB driverそのものを置き換えない。

PostgreSQL commit/rollback、provider呼出し前後の再認可、HTTP互換、Compose E2EとPagesは対象実装の同一commitで検証する。この標準repositoryの静的fixtureをKotoRelay等の実DB検証と同一視しない。CI・公開・merge規則は対象が所有する。

## 例外応答・型付き運用ログ・検証単位

参照のrouter例外境界と型付きloggerを適用範囲から無言で外さない。API帳票モデルの`error_contract.operations`（OpenAPIと同じ操作集合）に操作ごとの`handler`、解決済み`logger`名、`rules`を指定する。`rules`は実catch/raiseの`source`、実ログ呼出しの`log`、実return/raise/continueの`response`をそれぞれ`{path,line}`で結ぶ。全到達catch/raiseと運用ログが一致しなければ失敗する。例外がない限定入口は`no_exceptions_reason`で範囲を明示する。

```json
{
  "handler": "items.router.handle",
  "logger": "ops_logger.error",
  "rules": [{
    "source": {"path": "src/items/router.py", "line": 8},
    "log": {"path": "src/items/router.py", "line": 9},
    "response": {"path": "src/items/router.py", "line": 10}
  }]
}
```

ログは`ops_logger.error(catalog.MODEL_FAILED, context_model=Context(stage="model"))`形式とする。同梱検査はcatalog定数の`id, exception, status, code, message, level, operator_action, context_type`、実exception型、応答のstatus/code/message、contextの実classと注釈・field・値型を照合する。型付きlogger自体の実行時検査を対象で実装し、誤った型・機密を含む依存先例外の負例を実行する。通常アクセスログだけで運用ログ契約を満たしたことにしない。

内部catchの200/201等の安全な失敗結果を実statusのまま表示する。workerのcontinueはHTTP statusを発明しない。`http_handlers`は実`@app.exception_handler(Type)`を持つsymbolだけ受理し、再送出元の型と境界を照合する。実responseはliteral tuple `(status, {code,message})`または既知のFastAPI/Starlette HTTPExceptionのraiseを限定解決する。独自Problem/require、任意response constructor、動的応答、条件付きcatch、多態的dispatchは対象adapterが必要で、汎用の「例外を送出」で完了しない。

同梱privacy検査は注釈付きcontextの安全なliteral fieldだけを受理する。raw例外、f-string、JWT/body、`exc_info`、任意extra、動的contextを拒否する。動的なrequest ID等は対象のtyped loggerとtaint/redaction検証adapterで扱う。静的検査の成功は本番ログのprivacy証明ではない。

`error_contract`選択時の全caseは、実在するtest IDに対応したdocstringへ日本語の`Given:`、`When:`、`Then:`を各1行ずつ持つ。説明の欠落・重複・識別子だけの説明を拒否し、帳票に前提・操作・期待結果を表として表示する。ASTやassert式は根拠として残せるが説明の代用にしない。別言語の明示指定は対象adapterへ反映する。

共通帳票は例外型、捕捉/継続、実HTTP応答、ログID/レベル、確認・復旧、sourceを対応表で表示する。同じcatchに複数の動的outcomeがある場合はその集合を解決するadapterを用意する。公開Pagesの可読性は同じ生成HTMLをブラウザーで確認し、公開先での確認とローカルfixtureの証拠を区別する。標準側の変更だけで導入先Pagesを公開しない。
