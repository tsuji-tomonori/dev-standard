# アーキテクチャ意思決定記録

| ADR | 決定 | 選択肢 | 根拠 | 影響 | 承認者 | 日付 |
|---|---|---|---|---|---|---|
| ADR-001 | Skill名を`adversarial-review`へ変更 | 旧名維持、別Skill追加 | security検証との混同を構造的に避ける | 既存PR内参照を一括更新 | tsuji-tomonori | 2026-07-17 |
| ADR-002 | 誤りは作業仮説、結論は証拠依存 | 常に欠陥判定、通常レビュー | 批判性とfalse positive抑制を両立 | 独立oracleと最小証拠を必須化 | tsuji-tomonori | 2026-07-17 |
