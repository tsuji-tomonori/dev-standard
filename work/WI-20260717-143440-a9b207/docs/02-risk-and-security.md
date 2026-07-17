# リスク・セキュリティ設計

## 資産とデータ分類

| 資産 | 分類 | CIA要求 | 所有者 |
|---|---|---|---|
| canonical requirements catalog | repository internal/public specification | integrity high、availability via Git、confidentiality public前提 | product maintainer |
| generated design and manifests | derived public artifact | integrity high、availability regenerable、confidentiality public前提 | code maintainer |
| work authorization/evidence | project governance metadata | integrity high、availability via Git、secret/PII禁止 | requester/maintainer |
| standards registry/checklist | public reference metadata | integrity high、freshness required | quality maintainer |

## 脅威モデル

| 境界・フロー | 脅威または非該当根拠 | 統制 | 残余リスク |
|---|---|---|---|
| conversation -> requirement | 過度な同意、意味欠落、早すぎる収束 | calibrated formulation、semantic checksum、diverge/converge、path-changing questionのみ | 自然言語の意味を完全に形式化できない |
| change set -> canonical JSON | stale write、partial update、履歴消去、extra field | catalog/item revision、allowlist、candidate全体validation、fsync+replace、retire | 複数file transactionとしてgenerated viewに一時driftが残り得るがCIで検出 |
| source -> generated design | parser confusion、decorator誤混入、manual tamper | Python/SQL/YAML parser、runtime evaluation order、digest、byte comparison | dynamic dispatch内部のruntime flowは静的図に出ない |
| official web -> registry | unofficial summary、source陳腐化 | HTTPS official host allowlist、checked date、refresh interval | 期限内の急な改訂は次回checkまで遅延し得る |
| repository -> GitHub | secret/PII混入、main直接変更 | staged diff、secret禁止、branch PR、read-only CI permission | hosting側availability |

## プライバシー・法令・責任あるAI

個人情報、credential、production dump、raw transcriptをcommitしない。会話からは要求に必要な最小情報だけをwork recordへ要約する。AIは初回承認を推測せず、標準を理由に未承認scopeを拡張しない。runtime user service、個人data処理、model training、automated decisionは本変更に存在しないため、それら固有のprivacy/AI safety controlsは非適用である。

## リスク受容候補

未解決のCritical/High risk、期限付き例外、security exceptionはない。静的生成がdynamic runtime behaviorを完全には表さない制約は、生成設計を適合証明に使わず、正本traceとtestを別gateにすることで管理する。
