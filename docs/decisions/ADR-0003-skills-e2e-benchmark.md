# ADR-0003: Skills E2E benchmarkのauthority・oracle・実行tierを分離する

- Status: Accepted
- Date: 2026-07-24
- Related: Issue #22, ADR-0001

## 背景

`dev-standard`は、通常の自然言語依頼から永続要件、実装、実装由来設計、選択check、変更証跡までを一貫して扱う。個々のschema、generator、validatorのunit testだけでは、agentが適切なSkillを選び、必要な場合だけ質問し、複数authorityを混同せずに成果物を整合させられるかを検証できない。

Skillあり／なしの比較には、Skill本文の効果とcontext量の効果、実行環境の非決定性、oracle leakage、LLM judgeの主観性が交絡する。public pull requestで真のheld-out oracleを秘匿することもできない。

## 決定

1. Primary metricは、interaction、requirements、implementation、generated design、governance、safety / authorityのblocking Gateの論理積である`Strict E2E Pass`とする。診断scoreで重大欠陥を相殺しない。
2. `full-skills`、`no-skills`、`length-matched-control`を同一task・seed・model revision・prompt digest・tool schema・base ref・budgetでpaired実行する。報告するのは固定条件下の条件付き増分効果であり、Skill一般の普遍的因果効果ではない。
3. task、agent-visible input、controller-only oracle、base / gold / mutation fixture、result、run manifest、trajectory eventを別schemaで管理する。oracleとsimulated answerをagent workspaceへmountしない。
4. blocking判定はexecutable test、schema、AST / structured fact、digest、drift、annotated key conceptを優先する。LLM judgeは同義表現の診断補助に限定し、単独でGateを変更できない。
5. agent workspaceとtool executorの任意egressを禁止し、model provider / harness control planeはrun manifestのallowlistとして別に記録する。production deploy、外部write、merge、deleteをbenchmark taskから実行しない。
6. public PRでは公開conformance oracleだけを使用する。真のheld-out oracleはtrusted environment、private artifactまたは別checkoutからのみ投入し、fork PRへsecretを渡さない。
7. CIを分ける。schema・harness・gold/base/mutation discriminationはblocking、agent smokeは当初advisory、flake監視とutility推定はscheduled、held-out評価はtrusted manual / release workflowとする。
8. smokeの1 trajectory、flakeの3 trajectory、releaseの5 trajectoryを効果推定へ使用しない。utility runは事前固定したtask×seedのpaired observation、exact McNemar、Wilson interval、paired bootstrapを使用し、optional stoppingを禁止する。
9. trajectory、tool log、token、run result、utility reportはActions artifactへ置き、Gitにはschema、task、synthetic fixture、harness、公開conformance testだけを保持する。
10. agent benchmarkをblockingへ昇格する場合は、事前定義したflake率、provider failure率、再現率、費用、実行時間、annotation agreement、oracle leakageのGate別閾値をすべて満たす。

## 結果

- B01〜B08は小さいsynthetic repositoryとして常時再現できる。
- B06 / B07は実装由来fact、source digest、byte determinism、drift mutationを独立に検査する。
- B02 / B03はask / no-askをblockingにし、回答variantをcontroller側だけで供給する。
- public CIのscoreとtrusted held-out scoreを混同しない。
- benchmark定義のportable配布と、このrepository固有の受入matrix・review証跡を分離する。
