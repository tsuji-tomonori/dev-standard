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
