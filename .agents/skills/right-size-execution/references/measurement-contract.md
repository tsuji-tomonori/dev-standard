# Measurement contract

## Required raw metrics

- input/output tokens（取得可能な場合）
- wall-clock time
- tool calls、searches、subagents
- unique files、read bytes、read ranges
- duplicate read bytes
- capability escalations、Expand count/reason
- success/failure
- time-to-first-valid-patch

token telemetryがない場合も`read_bytes`、`read_ranges`、`tool_calls`は欠落させない。内容・secret・PIIは保存せず、path、range、byte、digestだけを記録する。

## Operational metric

`Execution Overrun Ratio = (actual_cost - estimated_budget) / estimated_budget`

一つのscalarへ集約して最適化しない。成功率、重大欠陥、各生指標、overrun、Expand理由を併記する。oracleがない実案件の値をACRRと呼ばない。

## Benchmark

repository benchmarkだけは人手で必要file、必要verification、合格testを定義し、`C_min`相当の境界を置ける。Current flow、Estimateなし、Expandなし、Full E3を比較し、削減率ではなく受入条件達成と生指標を先に確認する。
