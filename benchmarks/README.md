# Skills E2Eベンチマーク

このdirectoryは、自然言語依頼から対話、永続要件、実装、生成設計、governance証跡、authority boundaryまでを一つのtrajectoryとして評価するportable benchmarkです。

## 評価原則

- Primary metricは六つのblocking Gateの論理積である`Strict E2E Pass`です。重み付き点数で重大欠陥を相殺しません。
- `full-skills`、`no-skills`、`length-matched-control`を同じtask、model revision、tool schema、base ref、seed、budgetでpaired実行します。
- 結果は固定したmodel・harness・task・prompt・tool条件下の**条件付き増分効果**としてのみ解釈します。
- executable test、schema、AST fact、digest、drift、structured oracleをblocking判定に使用し、LLM judgeは同義表現の診断補助に限定します。
- public PRでは公開conformance oracleだけを使用します。held-out oracleはtrusted environment、private artifactまたは別checkoutからのみ投入します。
- live trajectory、tool log、run result、utility reportはGitHub Actions artifactへ保存し、Gitへコミットしません。

## 実行

```bash
python -m benchmarks.harness.certify --root .
python -m unittest discover -s tests -v
```

外部agent adapterはJSON配列のargvとして指定し、shell文字列を受け付けません。agent workspaceのegressを禁止するsandboxと、model provider / harness control planeの許可範囲は別に記録します。

## 構成

- `schemas/`: task、oracle、result、run manifest、trajectory、acceptance matrixの契約
- `tasks/`: agent-visible task定義
- `oracles/`: controller-only oracle。agent workspaceへcopyしない
- `fixtures/`: synthetic base / gold / mutation repository state
- `harness/`: workspace隔離、実行、採点、統計、認定
- `repository/acceptance-matrix.json`: Issue #22と研究レビューの受入条件に対する証拠

Task追加時はbaseが指定GateでFailし、goldが全GateをPassし、最低一つの典型的mutationが指定GateでFailすることを認定します。
