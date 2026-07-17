# リスク・セキュリティ設計

## 資産とデータ分類

| 資産 | 分類 | CIA要求 | 所有者 |
|---|---|---|---|
| target claims/code/tests | repository data | integrity high | repository owner |
| attack artifacts | potentially sensitive | confidentiality/integrity high | validator |
| research mapping | public sources | integrity high | skill maintainer |

## 脅威モデル

| 境界・フロー | 脅威または非該当根拠 | 統制 | 残余リスク |
|---|---|---|---|
| evaluator -> finding | judge bias/confirmation | independence、order swap、repeat、human/deterministic escalation | imperfect oracle |
| test -> target | destructive/unauthorized action | local/test only、synthetic canary、hard stop | environment misclassification |
| artifact -> Git | exploit/secret disclosure | minimal/redacted evidence | reduced debugging detail |
| mitigation -> utility | overblocking | benign baseline/control and holdout retest | incomplete usage sample |

## プライバシー・法令・責任あるAI

real secret/PII/third-party/production attackを禁止。research citationはpublic metadataのみ。absence of findingをsecurity proofとしない。

## リスク受容候補

finite attack budgetとuntested surfaceを明記することで残余不確実性を受容。High finding acceptanceはskill外のgoverned decision。
