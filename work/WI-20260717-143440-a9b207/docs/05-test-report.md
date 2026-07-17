# テスト結果

## 対象版

Branch `agent/canonical-spec-design-quality-framework`のPR候補。Python 3.12、openpyxl 3.1.5、PyYAML 6.0.2、SQLGlot 27.28.1、Ruff 0.12.4。Canonical catalog revision 1、standards registry checked 2026-07-17。

## 結果概要

| 種別 | 実行数 | Pass | Fail | Skip | 証跡 |
|---|---:|---:|---:|---:|---|
| Python unittest | 42 | 42 | 0 | 0 | `python3 -m unittest discover -s tests -v` |
| Canonical/generated checks | 2 | 2 | 0 | 0 | specflow check、standardsflow check |
| Static lint | 1 | 1 | 0 | 0 | `ruff check .` |
| Repository/catalog/audit | 3 | 3 | 0 | 0 | catalog check、validate_repo、devflow audit |
| Negative defect probes | 9 | 9 | 0 | 0 | composite/stale/drift/parser/source expiry tests |

## 要求カバレッジ

- REQ-FRAME-001、REQ-DISC-001〜004: canonical self-host、composite action/object rejection、revision conflict、retire tombstone、generated view equality。
- REQ-DESIGN-001〜006: router/functions presence、decorator exclusion、nested evaluation order、OpenAPI operation/schema、SQL CRUD、CFn `!Ref`、source mutation drift。
- REQ-QUALITY-001〜002: registry/asset equality、official host allowlist、expiry rejection、existing evidence gate tests。
- REQ-PORTABLE-001: chat-first/development-framework/full profilesをempty temporary targetへcopyし、standard pathとtarget config preservationを確認。

## 未解決欠陥

未解決defect、skip、期限付き例外は0件。Generated designはdynamic dispatch内部のbehaviorを記述しないという既知制約があるが、仕様どおり静的flowに限定し、要件適合は別testで判定する。

## 非機能・障害試験

同一inputのbyte比較、stale catalog/item revision、invalid composite obligation、missing direct response call、functions source mutation、unofficial host、freshness expiry、target install conflictを試験した。runtime load/performance、network failure、cloud failoverはdeployable serviceを作らないため非適用である。

## 完了判定

local verificationはPass。GitHub Actions successをreleaseの最終条件とし、CI failureは同じbranchで原因修正して再実行する。
