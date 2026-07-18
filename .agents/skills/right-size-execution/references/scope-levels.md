# Scope levels

| level | 判定 | 初期context | 初期verification |
|---|---|---|---|
| L1 Local | 対象ファイル・関数が明示された局所変更。契約変更なし | 対象range、近傍定義、直接test | targeted test、syntax、affected lint |
| L2 Bounded | 同一moduleの複数fileまたは直接dependency変更 | 検索hit、public IF、直接dependency、関連test | module test、type check、related lint |
| L3 Systemic | 複数domain、public contract、横断変更、高risk | canonical requirements、design、dependency graph、関連standard | full gate、integration、CI、defect-seeking review |

## L3 risk floor

次は見かけ上1 fileでもL3とする。

- authentication、authorization、security、secret
- database schema、migration、data deletion／loss
- public API、event、external contract
- IaC、network、permission、deploy
- dependency、lockfile、runtime upgrade
- durable requirement、governance、checklist、generator
- confidential information、PII、external side effect
- rollbackが困難または不可逆な変更

Levelは作業量ではなく、正しく完了するために必要な観測・検証範囲を表す。
