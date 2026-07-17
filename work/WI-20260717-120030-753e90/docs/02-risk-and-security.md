# リスク・セキュリティ設計

## 資産とデータ分類

| 資産 | 分類 | CIA要求 | 所有者 |
|---|---|---|---|
| target source/config | target-owned | integrity high | target maintainer |
| authorization/work evidence | repository data | integrity high | requester/agent |
| GitHub branch/PR | external state | integrity high | repository owner |

## 脅威モデル

| 境界・フロー | 脅威または非該当根拠 | 統制 | 残余リスク |
|---|---|---|---|
| chat -> scope | vague intent causes wrong change | calibrated clarification、single authorization | requester misunderstanding |
| bootstrap -> repository | global/active config overwrite | repository-local only、preserve/merge rule | incompatible target tooling |
| fallback | reduced deterministic assurance | full runtime preferred、explicit evidence | fewer machine gates |
| publication | unintended merge/deploy | PR only、no merge/production | external permission failure |

## プライバシー・法令・責任あるAI

secret、personal data、telemetryを追加しない。AIは承認を推測せず、質問量削減とauthority boundaryを両立する。

## リスク受容候補

lightweight fallbackのassurance低下は、full runtime未copyでも作業停止しないための限定tradeoffとして受容する。PR/test evidenceは省略しない。
