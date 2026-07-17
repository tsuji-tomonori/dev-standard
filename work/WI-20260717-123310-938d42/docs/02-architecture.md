# アーキテクチャ

## コンテキストと境界

portable adversarial-validation skillを中心に、progressive research map、attack playbook、report template、repository Skills catalog、chat/release integrationで構成する。実攻撃環境はboundary外。

## コンポーネントと責務

| コンポーネント | 責務 | 所有データ | 依存先 | SLO |
|---|---|---|---|---|
| SKILL.md | trigger、workflow、decision/safety rules | validation contract | references | portable discovery |
| research basis | source-to-rule trace | citations/findings | primary sources | auditable rationale |
| playbook/report | risk-based executionとevidence schema | techniques/artifacts | target tests | reproducibility |
| Skills catalog | collection discovery/copy guidance | inventory table | manifest/filesystem | drift detection |

## データフローと信頼境界

target claimからthreat modelとindependent oracleを作り、attack portfolioをsafe environmentで実行する。findingはrepair/retest loopへ戻り、bounded conclusionだけをrelease evidenceに渡す。

## 可用性・性能・拡張性

static Markdown skillでruntime SLOなし。progressive disclosureで研究詳細は必要時だけloadする。portfolioはriskとbudgetでscaleする。

## 代替案とトレードオフ

security-only red teamではrequirements/code/testの反証を扱えないためsoftware techniquesを統合。all-techniques mandatoryはcost過大なためrisk selectionを採用。

## 失敗・縮退・復旧

oracle不明はmetamorphic/differential/human escalation。unsafe reproductionはsynthetic substitute。authority不足はexact blockerとして停止する。
