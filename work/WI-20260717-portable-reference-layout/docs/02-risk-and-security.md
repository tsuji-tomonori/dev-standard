# リスク・セキュリティ設計

## 資産とデータ分類

| 資産 | 分類 | CIA要求 | 所有者 |
|---|---|---|---|
| Reference assets | public source | integrity/high, availability/low, confidentiality/none | repository owner |
| Target repository files | target-owned | integrity/high | target maintainer |

## 脅威モデル

| 境界・フロー | 脅威または非該当根拠 | 統制 | 残余リスク |
|---|---|---|---|
| source -> installer | path traversal/symlink substitution | resolved source containment、symlink拒否 | repository checkout自体の侵害は対象外 |
| installer -> target | existing file overwrite | global preflight、default dry-run、explicit force | userがreview後forceを選ぶ可能性 |
| merge reference -> active config | incompatible manual merge | non-active filename、guideとcomments | maintainer判断の誤り |

## プライバシー・法令・責任あるAI

personal data、secret、外部APIを扱わない。AI reviewerは既存のread-only設定と最小能力model routingを維持する。配布物に新しい実行時network権限はない。

## リスク受容候補

残余リスクは通常のsource repository trustとmaintainerによるmanual mergeに限定され、追加例外承認は不要。
