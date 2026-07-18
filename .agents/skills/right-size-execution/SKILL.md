---
name: right-size-execution
description: Estimate and enforce the smallest sufficient execution scope for repository work, then expand one justified axis only after verification failure, new dependency evidence, or a measured budget overrun. Use before governed implementation, when selecting context, tools, model tier, validation, reviewers, or standards checks, and when auditing execution efficiency. Treat Estimate, Execute, and Expand as one state machine; do not split them into separate skills.
---

# Right-size Execution

最小コストではなく、成功条件と重大リスクを満たす最小十分な実行経路を選ぶ。Estimate／Execute／Expandを一つの状態機械として扱い、判断・計測・監査は`scripts/scopeflow.py`の決定的な出力へ委ねる。

## Workflow

1. `references/scope-levels.md`と`assets/execution-policy.json`を読む。自然言語依頼、明示された成果物、契約変更、risk tagから初期operating pointを一度だけ推定する。曖昧なときのmetadata-only probeは最大1回とし、結果を再利用する。
2. repository変更なら、初回承認パッケージを作る前に`execution-scope.json`を生成する。回答・調査だけなら永続台帳は作らず、同じ停止規則だけを適用する。
3. 初期コンテキスト、tool/model budget、最小の決定的検証内でExecuteする。検索はpath・line・短い断片から始め、必要範囲だけを読む。同一digestの同一rangeを再読しない。
4. 検証失敗、新しい依存・契約影響、予算超過、高リスクかつ低confidence、具体的な能力不足のいずれかが観測されたときだけExpandする。`references/expansion-rules.md`に従い、一回につき一軸を一段だけ広げ、evidenceと理由を記録する。
5. 最小の決定的検証がPassしたら成功を記録し、必須最終ゲートだけを実行して停止する。成功後の「念のため」の検索、全量ログ読取、追加reviewをしない。
6. `finalize`で`reports/execution-efficiency.json`を生成し、`audit --mode soft`で過小分類、未説明overrun、無根拠な能力引上げ、成功後探索を報告する。blocking化はrepository benchmarkと実績に基づく別の承認済み変更まで行わない。

## State contract

- 正本: `work/<id>/execution-scope.json`
- 派生要約: `docs/01-execution-plan.md`
- 実績: `work/<id>/reports/execution-efficiency.json`
- Schema: `assets/execution-scope.schema.json`
- Policy: `assets/execution-policy.json`
- 計測定義: `references/measurement-contract.md`

予算はsoft limitである。超過は作業を停止させず、対応するExpand eventまたは「追加範囲が不要」という決定的証拠を要求する。policyのモデルtierは能力帯であり、具体的モデル名をSkillへ固定しない。

## Efficiency rules

- 成功した決定的コマンドはexit code、要約、digestだけを保持する。
- 失敗ログは最初の因果的エラーと周辺行だけを取り込む。
- 生成物は本文全量ではなくdigestと差分で検査する。
- checklist全量をpromptへ入れず、selectorの版、入力特徴、選択ID、digestを保存する。
- subagentへ親contextを全量転送しない。独立判断が必要な範囲だけを渡す。
- token telemetryが取れない環境ではread bytes、read ranges、tool callsを必須proxyとする。

## Correctness boundary

高リスク変更をファイル数だけでL1/L2へ落とさない。security、data loss、DB schema、migration、public API/event、IaC、network、permission、dependency/lock、durable requirement、governance、generator、PII、external side effect、rollback困難な変更はL3を下限とする。

ACRRは正確な`C_min` oracleを持つbenchmarkでのみ使える。実案件ではExecution Overrun Ratioと各生指標、成功率、重大欠陥を併記し、論文の削減率を目標値として転用しない。
