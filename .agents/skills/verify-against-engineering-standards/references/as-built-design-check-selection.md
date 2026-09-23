# as-built設計check選択

導入先が採用するas-built要件と、変更対象のsurfaceに関係するcheckを選ぶ。要件の正本は`spec/requirements/requirements.qnt`、実行commandの所有者は導入先repositoryである。dev-standard固有の検査catalogや旧言語固有Rule IDを導入先へ要求しない。

| 変更 | 選択する証拠 |
|---|---|
| adapter契約、参照tools棚卸し | schema、全件集合、要件mapping、採用判断と実接続先 |
| 実装または生成command | 2回生成のbyte一致、`--check`による設計drift |
| APIや保存先の処理 | 導入先の責務・制御flow・型・CRUD・例外経路の静的検査 |
| 帳票profileや生成物 | 章・順序・階層・索引・リンク・旧生成物 |
| test、品質portal | 実行結果、未検証範囲、階層表示とCSV取得 |

[adapter契約](../../generate-implementation-design/references/adapter-contract.md)と[APIの6帳票契約](../../generate-implementation-design/references/api-documents.md)を参照する。構成適合、設計drift、実行テスト、未検証範囲は別に報告する。

選択条件と除外は会話または導入先の既存記録へ必要な分だけ残す。ローカルcommandを実行し、既存CIがあれば同じcheckを再利用できる。CI workflow、required check、review YAML、branch protection、merge ruleをこの標準のために追加または要求しない。外部作用は導入先の既存権限に従う。
