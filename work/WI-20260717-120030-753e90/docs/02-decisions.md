# アーキテクチャ意思決定記録

| ADR | 決定 | 選択肢 | 根拠 | 影響 | 承認者 | 日付 |
|---|---|---|---|---|---|---|
| ADR-001 | umbrella `chat-first-development` skillを追加 | 既存skill名を利用者が指定 | ordinary requestで確実に発火 | skillが一つ増える | requester | 2026-07-17 |
| ADR-002 | user commandを禁止しAI内部でbootstrap | manual installer/README command | chat onlyの操作面 | agentにsetup責任 | requester | 2026-07-17 |
| ADR-003 | full runtime優先、欠落時lightweight fallback | runtime必須で停止 | folder一つでも開発継続 | lightweightは厳密性低下 | requester | 2026-07-17 |
| ADR-004 | initial authorizationは自然言語で維持 | 完全無承認 | authority boundaryを保護 | 一度だけ対話が必要 | requester | 2026-07-17 |
