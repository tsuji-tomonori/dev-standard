# AI駆動開発フロー

```text
ユーザー要望
    │ 原文保存
    ▼
要求受付 ── requester承認
    ▼
要件定義 ── requester + product-owner承認
    ▼
アーキテクチャ／リスク ── architect + security-owner承認
    ▼
詳細設計／テスト設計 ── architect + qa-owner承認
    ▼
実装／構成管理 ── 自動検査
    ▼
検証／品質保証 ── qa-owner + security-owner承認
    ▼
運用／保守準備 ── operations-owner承認
    ▼
リリース判定 ── requester + release-owner承認
    ▼
振り返り／改善 ── governance-owner承認
    ▼
完了
```

## 各工程で行うこと

1. `state.json`の`current_phase`を確認する。
2. `governance/policy.json`に定義された必須文書を更新する。
3. `review/checklist-results.json`の当該工程項目をすべて評価する。
4. 工程に対応するread-only custom agentへ独立レビューを委譲する。
5. `inspect`を実行し、文書・適用判定・証跡・例外の不足を解消する。
6. 人間の責任者が`approve`で判断を記録する。
7. `advance`で次工程へ進む。

## プロファイル

`CORE`は常に選択されます。クラウドベンダープロファイルを選ぶと`CLOUD-COMMON`も自動選択されます。

- `CORE`: SWEBOK主要ライフサイクルKA
- `CLOUD-COMMON`: ベンダー共通クラウド統制
- `AWS-DELTA` / `GCP-DELTA` / `AZURE-DELTA` / `OCI-DELTA`: 採用ベンダー固有差分
- `AI-CONDITIONAL`: 従来型ML、生成AI、エージェントAI

同じ根本リスクを複数シートで扱う場合、証跡とIssue IDは再利用できます。ただし、ベンダー固有差分を共通統制で評価済みとする場合も、N/A根拠に評価済みIDを明記します。

## AIエージェントの境界

AIは、質問の抽出、文書草案、チェック項目の候補判定、証跡収集、独立レビュー、ゲート実行を行えます。人間の役割名での承認、リスク受容、Go判断は行えません。承認コマンドは、ユーザーが明示的に判断を示した後だけ実行します。
