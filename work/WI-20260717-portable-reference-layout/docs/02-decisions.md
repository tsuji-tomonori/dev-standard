# アーキテクチャ意思決定記録

| ADR | 決定 | 選択肢 | 根拠 | 影響 | 承認者 | 日付 |
|---|---|---|---|---|---|---|
| ADR-001 | skillsを`.agents/skills`、Codex agentsを`.codex/agents`に維持 | 独自directoryへ移動 | current Codex discovery standard | portable/Codex-specific境界が明確 | requester | 2026-07-17 |
| ADR-002 | manifest駆動、dry-run default installer | shell snippetのみ | copy contractを検証可能にする | Python 3が必要 | requester | 2026-07-17 |
| ADR-003 | target configはreference snippetから手動merge | config自動上書き/merge | target固有意味とownershipを保護 | 導入時に一度reviewが必要 | requester | 2026-07-17 |
| ADR-004 | Lean 4を導入せず曖昧なlean表記を除く | formal verification追加 | 本変更に定理証明対象がなく運用負荷が便益を上回る | 将来必要なら別work item | requester | 2026-07-17 |
