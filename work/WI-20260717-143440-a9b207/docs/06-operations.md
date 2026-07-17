# 運用設計・運用引継ぎ

## 運用対象とSLO

本変更はlibrary/reference repositoryであり、24時間稼働service、production environment、customer traffic、on-call、cloud resourceを追加しない。そのためavailability/latency/error-budget SLOは非適用。運用品質はCI再現性で定義し、PRとmainの必須検査が100% Passしなければreleaseしない。

## 監視・ログ・アラート

GitHub Actionsのtest result、spec/design drift、standards freshness、repository validator、auditを観測点とする。CLIは成功対象または具体errorとexit statusを返す。継続service log、APM、metric alert、log retentionはruntimeがないため非適用。

## Runbook・インシデント対応

| Event | Detection | Response | Recovery proof |
|---|---|---|---|
| canonical requirement drift | specflow/repo check failure | JSON正本またはgenerator defectを修正しview再生成 | specflow check Pass |
| design drift | designflow `--check` failure | sourceに従いbundle再生成しrequirement traceを再確認 | byte check Pass |
| stale standards source | standardsflow failure | official URLを再調査し、version/checklist changeを新しいgoverned deltaにする | freshness check Pass |
| dependency/API break | CI unit failure | pinned dependency compatibilityをreproduceしcodeまたはpinをauthorized update | full suite Pass |
| catalog/hash tamper | audit failure | Git historyから正当版を復元し原因調査 | audit Pass |

Escalation ownerはrepository maintainer、品質判断はPR reviewer、scope/requirement変更判断はrequesterである。24/365 response契約はない。

## バックアップ・復旧・DR

Git historyとremote repositoryがsource backupであり、generated viewsはcanonical/sourceから再生成する。Database/object storeはない。PR branchをclose/revertでき、mainへ直接pushしない。Region failover、RPO/RTO、data restore drillはcloud workloadがないため非適用。

## 容量・コスト・依存先

処理量はrepository file数に線形で、CI runnerの通常memory/disk範囲を前提とする。外部依存はGitHub Actions、Python 3.12、PyPIで取得するpin済み3 package、公式standard pageである。継続cloud費用、license purchase、reserved capacityはない。Source refreshはSWEBOK 180日、cloud guidance 90日を上限に再確認する。
