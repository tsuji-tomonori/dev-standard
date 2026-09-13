# 選択した参照構成の適合検査

Issue [#67](https://github.com/tsuji-tomonori/dev-standard/issues/67)と[#68](https://github.com/tsuji-tomonori/dev-standard/issues/68)の契約。参照追従を指定した導入先だけに適用する。既定配置へ無条件に強制しない。通常の開発に工程承認・追加CI・branch規則を導入しない。

## 固定profile

`assets/api-structure-lazunex-v1.json`はlazunex commit `096e1e580ab1c0670c57e4febad2bd9fdd4698ee` の6帳票から章名・階層・順序・動的節を抽出した構造契約。SQL名、message ID、case IDの繰返しは対象モデルの実在集合に一致させる。章を削除して非該当を表現せず、具体的理由を残す。参照先のSQLAlchemy、AWS呼出し、ログwrapper、HTTP sample、直積網羅は対象実装から確認できない限り移植しない。

`api-documents`の既存意味モデルへ次を追加すると共通rendererがprofileを使用する。従来モデルの出力は維持する。

```json
{
  "structure_profile": "lazunex-v1",
  "python_root": "src",
  "document_names": {"interface": "interface.gen.md"},
  "operations": [{
    "id": "getItem",
    "group": "items",
    "slug": "get-item",
    "router_implicit": "対象routerの入力検証・依存注入等を実装から記載する。",
    "no_samples_reason": "この対象はHTTP sampleを定義していない。",
    "accesses": [{
      "store": "inventory", "phase": "runtime",
      "sql": "src/items/sql/read.sql",
      "source": {"path": "src/items/generated/queries.py", "line": 8}
    }]
  }]
}
```

上記は追加fieldの説明用であり、実際には既存のsource、inputs、outputs、queries、messages、factors、cases、sequence等も必要。`samples`が存在するときは実装・実HTTP検証由来の値を渡す。`document_names`は既存の名前を維持する任意指定。group/slug/各名前は安全な単一path componentとする。共有rootや名前の勝手な推定を避け、選択profile・参照SHA・適用外理由を導入先要件へ記録する。

出力は`<group>/<slug>/<kind>_gen.md`（interfaceの既定名は`if_gen.md`）と閲覧用HTML、group/API索引、完全なOpenAPI、`crud/`のCSV・Markdown・SVG・HTML・モデルJSON。モデルを検証する処理と章を組み立てる処理を分離している。`--check`は階層全体を比較し、管理manifest外の旧成果物・link切れ・追加削除・手編集を拒否する。旧bundleからの生成は管理範囲を一括置換するが、管理外fileが混入していれば停止して報告する。

## CRUD抽出の範囲

全APIに`accesses`配列を要求する。空なら`no_access_reason`が必要。`unresolved_accesses`が空でなければ生成失敗。SQL正本はsource snapshotの範囲へ含める。呼出しはhandlerから到達する関数のAST上のCall行と一致し、SQL本文または所有先を含むSQL pathがそのcallへ実際に渡される範囲を扱う。SQL ASTでSELECT/JOIN/CTEの実table参照とINSERT/UPDATE/DELETE先を区別する。MERGE等は対応外として失敗させる。

非SQLのaccessは`symbol`（解決後call名）、`adapter`（対象service抽出器識別子）、`resource`、`action`（C/R/U/D）、`store`、`phase: runtime`、`source`を指定する。例: `storage.put_object`の呼出し行にオブジェクト保存adapterの抽出を結合する。構築時のCDK操作をAPIアクセスへ含めない。共通検査が対象serviceの意味を証明したとは扱わず、adapterはresource抽出・動的dispatch・網羅性を実装およびサービスfixtureで検証する。未対応をアクセスなしに分類しない。未解決の外部callは`accesses`か、source/symbol/reason/adapterを持つ`non_access_calls`による対象adapterの明示分類が必要である。動的callable、反射や代入経由のcallableは共通解析で失敗させる。

CSV・表・図・抽出根拠は同じCRUDモデルから生成する。SQLを直接所有しないAPIへ空SQLを作らない。保存先とリソース名はモデルに保持し、CSV表示では式として解釈される接頭辞を無害化する。

## 独自adapterから同じ検査を使う

`.dev-standard/design.json`の`surfaces.api`に既存の`openapi`、`operation_documents`、`markdown`、`generate`、`check`と次を設定する。

- `structure_model`: 再抽出した上記意味モデルのrepository相対path。
- `structure_root`: 当該group/API/帳票bundleのrepository相対path。
- `layout_config`: 下記API責務構成のconfig path。参照実装の追従が選択されたときだけ指定する。

`check_design.py`は章構成・繰返し節・階層・mapping・link・CRUD出力の集合を共通検査する。その後、対象adapterの非破壊再抽出/check commandでsnapshotと内容のdriftを検査する。構成適合と実装driftを別々の結果として出力する。章の一致は説明の意味的完全性やテスト成功を証明しない。

## API責務配置

```json
{
  "profile": "lazunex-v1",
  "python_root": "src",
  "shared": {"src/app/shared/auth": "複数APIで使う認可判定"},
  "operations": {
    "getItem": {
      "package": "src/app/operations/items/get_item",
      "handler": "get_item",
      "queries": {"src/app/operations/items/get_item/sql/read.sql": {"function": "read"}}
    }
  }
}
```

実行: `python <host-skill-path>/scripts/api_layout.py --root . --config api-layout.json --openapi openapi.json`。SQLGlotを使うCRUD生成は既存のpinned Python runtimeのdesignflow経由で実行する。

profileの6責務fileを検査し、OpenAPIとmethod/path/operation IDを照合する。package名とoperation IDの同名性は要求しない。prefixはconfigの`router_prefix`で明示し、実際の登録との一致を対象adapterで検証する。呼出し、annotation、decoratorの参照をimport aliasと再exportから解決する。未使用importやコメント、未呼出しの入れ子関数は実接続の証拠ではない。

handlerから業務関数・応答組立へ到達し、schemas・contract・samplesが使用されることを要求する。API間直接依存、共有からAPIへの逆依存、所有者不明の内部依存、全体共通query生成先を拒否する。SQL識別子には所有先pathを含め、同じbasenameを別APIで使用することは許可する。同一ownerで複数SQLを同じ生成symbolへ潰すことは拒否する。互換用`queries.py`は必須ではない。

これは静的に解決できるPython import・call・定数metadataの検査であり、runtimeのroute mounting、任意の動的import、computed SQL、反射、すべての業務意味の汎用検証ではない。解析できないbindingには対象adapterを用意し、その負例と実HTTP sample試験を含める。参照lazunex自身のmetadata-only contractも実接続を示すものではなく、そのまま適合と扱わない。KotoRelayの実行結果を導入先の合格証拠に流用しない。
