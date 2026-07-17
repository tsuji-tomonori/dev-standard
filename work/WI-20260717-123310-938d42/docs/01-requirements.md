# 要件定義

## 概要

敵対的検証を、対象の正しさを支持する確認ではなく、明示したclaimを反証するcounterexample探索として定義する。software testingとAI red teamingの研究知見を統合し、独立oracle、attack diversity、adaptive tests、utility control、reproducible artifactsを工程化する。

## ステークホルダー

| 役割 | 関心事 | 承認責任 |
|---|---|---|
| requester/repository owner | 根拠あるportable skillと一覧 | 要件・実行計画 |
| developer/evaluator | actionable counterexampleと再現手順 | finding修正 |
| affected user | safetyと通常機能の両立 | 受入判断 |

## 機能要件

| ID | 要件 | 優先度 | 受入基準 |
|---|---|---|---|
| ADV-001 | primary researchと公式taxonomyを調査する | Must | source、finding、skill ruleのresearch mapがある |
| ADV-002 | scope別のthreat modelを作る | Must | asset/claim、attacker goal/capability/knowledge/budget/lifecycleを明記 |
| ADV-003 | confirmationから独立したoracleを使う | Must | property、metamorphic、differential、referenceまたはhuman escalationを選ぶ |
| ADV-004 | 多様でadaptiveなattack portfolioを実行する | Must | boundary/mutation/fault/abuseとAI injection/multi-turnをscope選択 |
| ADV-005 | findingを再現可能にする | Must | input、environment、version、seed/budget、expected/actual、severityを記録 |
| ADV-006 | mitigation後にutilityとrobustnessを再検証する | Must | unchanged regression、holdout variant、benign controlを再実行 |
| ADV-007 | safety boundaryを守る | Must | test/local only、no real secret/harm/destructive production action |
| ADV-008 | Skills一覧を維持する | Must | name、purpose/trigger、dependencies、copy pathがinventoryと一致 |

## 非機能要件

| ID | 品質特性 | 測定方法 | 合格閾値 |
|---|---|---|---|
| ADV-N1 | Evidence quality | contract/validator | claimごとにdirect artifact |
| ADV-N2 | Reproducibility | report rubric | rerun可能なmetadata |
| ADV-N3 | Evaluator validity | position/independence checks | single biased judgeへの依存なし |
| ADV-N4 | Portability | skill validation | self-contained references、standard path |

## データ・法令・倫理要件

攻撃sampleは最小・redacted・authorizedに限定する。secret/PII/production evidenceをGitへ保存しない。AI evaluator biasとfalse confidenceを明示的riskとして扱う。

## リスクとトレードオフ

完全なattack coverageは不可能。absence of findingをproofにせず、budgetと未検証面を報告する。自動生成でscaleし、人/independent oracleで高severityを確認する。

## 対象外・N/A判断

penetration testing execution、malware/exploit作成、production red team、formal proof、第三者systemへのscanは対象外。
