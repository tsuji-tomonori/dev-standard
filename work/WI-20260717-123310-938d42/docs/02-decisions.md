# アーキテクチャ意思決定記録

| ADR | 決定 | 選択肢 | 根拠 | 影響 | 承認者 | 日付 |
|---|---|---|---|---|---|---|
| ADR-001 | falsification-first portable skill | generic security checklist | confirmation biasを避けscope横断 | counterexample探索cost | requester | 2026-07-17 |
| ADR-002 | research mapをskill referenceに保持 | READMEへ長文埋込 | source/rule traceとprogressive disclosure | source更新保守 | requester | 2026-07-17 |
| ADR-003 | independent oracleとjudge bias checksを必須化 | single LLM judge | position bias/false confidence研究 | extra evaluation | requester | 2026-07-17 |
| ADR-004 | Skills catalogをfilesystemと自動照合 | manual listのみ | driftをCI検知 | skill追加時更新必須 | requester | 2026-07-17 |
