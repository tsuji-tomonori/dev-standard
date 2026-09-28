# 参照適合の完了条件（manifest v3）

Quint正本の`REQ-ASBUILT-036`を実行へ接続する契約。文書の見出し・所有・driftと、導入先の意味検査を区別する。新規API導入と参照追従更新では通常の`check_design.py`を使う。旧v2を明示して診断する`--legacy-layout-only`は移行前の読み取り用であり、実装完了の証拠ではない。v3ではこの迂回を拒否する。APIを持たない既存v2の構成検査は維持する。

## 主参照を保持する

利用者がlazunexを正と指定した場合は固定版lazunexを主参照にする。`api.profile.reference`、conformance profile、mapping、`target-adoption` inventoryのrepository/SHAを一致させる。KotoRelayなどの補助参照は追加できるが、主参照を置換できない。配布lazunex profileでは全52 toolsのpath/blob集合も照合する。

[配布profile](../assets/lazunex-conformance-v1.json)は正本要件IDの適用集合であり、要件本文の別正本ではない。67件を個別に扱う。`REQ-ASBUILT-015/016`は引き続きAdvisoryである。SQL・外部I/O・E2E・公開portal等の適用外は導入先の明示要件・理由と、その不在を検査する正負例を持つ。未実装や未対応を適用外にしない。

## Manifest

既存v2の各項目を保持し、`schema_version: 3`と次を追加する。commandはshell文字列ではなくargvで、`{report}`を独立した引数としてちょうど1回含める。

```json
{
  "conformance": {
    "profile": ".agents/skills/generate-implementation-design/assets/lazunex-conformance-v1.json",
    "mapping": ".dev-standard/reference-conformance.json",
    "check": ["python", "tools/project/check_conformance.py", "--report", "{report}"]
  }
}
```

`check_conformance.py`は導入先で実装する。名前は例であり、言語・配置を固定しない。生成器を呼ぶだけのno-opや定数passのreportを実装しない。所有・型・sample・順序・例外/ログ・factor/collector対応・source全件発見の検査と、意図的に壊した負例を実行する。必須ルールが未実装なら完了を拒否する。

## 要件mapping

mappingは`schema_version: 1`、`reference: {repository, revision}`、`rules`を持つ。各ruleは以下の5項目を持つ。

| 項目 | 意味 |
|---|---|
| `id` | profile中の正確な参照要件ID。全件を重複なく写像する |
| `status` | `required` / `advisory` / `not-applicable`。未対応は完了できない |
| `requirement_id` | 導入先Quint派生JSON中のactive要件ID。capabilityの適用集合にも含める |
| `acceptance_id` | その要件の実在する受入条件ID。各参照要件で異なる受入条件へ対応させる |
| `reason` | 適応・適用外の具体的な根拠。単に「実装済み」「同等」と書かない |

一つの`TECH-DESIGN`に複数の受入条件を置くことは可能だが、独立した67の義務を一つの受入条件へ潰すことはできない。参照要件を全て導入先へ同名コピーする必要はない。mappingの適用外判断自体もreview対象であり、共通検査器が業務上の妥当性を判断するわけではない。

## 新規実行report

共通検査器は作業用コピーで、既存の帳票とは別の新規一時pathを`{report}`へ渡してcommandを1回実行する。`DEV_STANDARD_SOURCE_DIGEST`に、共通側で計算した宣言source・適合入力・manifestのSHA-256を渡す。終了code、新規reportの存在、digest、要件集合、collector IDとsource位置、正例/負例の結果を照合する。commandがrepositoryを書き換えた場合も拒否する。reportは次の形で出力する。

```json
{
  "schema_version": 1,
  "source_digest": "実行時に受け取ったDEV_STANDARD_SOURCE_DIGEST",
  "tests": [
    {"id": "tests/sample::valid_pair", "kind": "positive", "status": "pass", "path": "tests/sample.py", "line": 10},
    {"id": "tests/sample::placeholder_rejected", "kind": "negative", "status": "pass", "path": "tests/sample.py", "line": 20}
  ],
  "rules": [
    {"id": "REQ-ASBUILT-012", "status": "pass", "test_ids": ["tests/sample::valid_pair", "tests/sample::placeholder_rejected"], "reason": ""}
  ]
}
```

これは1要件だけを説明する抜粋である。実reportはprofile全件を含める。testのstatusは`pass/fail/error/skipped/not-run`。必須要件には実行済みでpassのpositiveとnegativeの両方を必要とし、参照した全testが実collectorの正確な検証単位であることを導入先が保証する。parametrize後の別caseを同じ関数名へ潰さない。testと検査commandのsourceもcapabilityの`sources`へ含める。未知ID・重複・孤児test・範囲外のsource行・宣言source外のtestを拒否する。

適用外はrule statusを`not-applicable`とし、mappingと同じreason、適用範囲の不在を確認するpositiveと、対象を追加すると不在判定が失敗するnegativeの実行結果を含める。単に`test_ids: []`とはしない。Advisoryの`fail/not-run`は理由付きで別欄へ出し、必須検査の成功・失敗へ混ぜない。

## 帳票内容の負例

少なくとも次の差分が適切な検査を失敗させるよう、導入先の実装・parser・collectorで確認する。

| 変更 | 期待する拒否・差分 |
|---|---|
| sampleを「OpenAPI参照」だけにする／sampleのassert参照を除く | 内容不足・未対応sampleを拒否 |
| BodyとPathを持つAPIでPathを落とす／参照schemaの項目を削る | 入力全体と展開型の欠落を拒否 |
| endpointへquery呼出し、入れ子helper、別名経由のAPI依存を追加 | 所有・責務境界の違反を拒否 |
| SQLの投影・束縛・NULLを変える | 型または生成driftを検出 |
| callbackの呼出順、条件、early return、DBのretryを変える | sequenceが変わる。解析不能なら明示失敗 |
| 例外のstatus、loggerのID/level/項目型を変える | 例外→応答→運用ログの対応不一致を拒否 |
| collectorのcaseやassertを削除する／同名に潰す | 実在・要因/要素・期待効果の対応漏れを拒否 |
| 未登録API・未知provider method・別sourceのhelperを追加 | 全source照合で未対応を検出。空配列へ隠さない |
| CRUD列・未使用資源・group CSVを落とす | 行列母集合・同一モデル照合で拒否 |

共通検査器はPython/TypeScript/SQL等の意味解析器ではない。trusted commandの虚偽実装を暗号学的に防止する仕組みでもない。digestは宣言された入力を束縛するが、未宣言sourceを自動発見する証明ではない。実解析、全sourceの独立発見、assertの妥当性は導入先で実装・review・mutation testする。共通契約だけで「SlotKeeperの業務テストが通った」「AWSで動いた」とは報告しない。
