# Skills一覧

通常はSkill名を指定せず、実現したい結果を自然言語で相談する。`$chat-first-development`がprofileと必要Skillを選ぶ。

このrepository自身のSkill、agent、標準、governance、distribution、documentationを変更するときだけ、`$maintain-reference-repository`を先に適用する。

## 既定で利用できるSkills

| Skill | 目的・起動条件 |
|---|---|
| `chat-first-development` | ordinary requestをdirect / assured / regulatedへ振り分け、実装、review、Commit Comment、PR、CIまで進める |
| `right-size-execution` | profile、scope、verification、review、computeを最小十分に選ぶ |
| `calibrated-collaborative-listening` | 結果を変える曖昧さだけを穏やかに確認する |
| `maintain-canonical-requirements` | 永続要件をproduct / project、functional / nonfunctionalへ分類し、add / update / retireを正本へ適用する |
| `generate-implementation-design` | 実装からas-built設計を生成しdriftを検査する |
| `verify-against-engineering-standards` | 関連する標準controlだけをInvariant / Risk-selected / Advisory / Periodicとして選ぶ |
| `inspect-quality-gates` | 変更イベントごとにselected checkを確認しreview YAMLへ保存する |
| `japanese-git-commit-gitmoji` | Change Manifestと要件・設計影響を代替する構造化Commit Commentを作る |
| `adversarial-review` | critical、高影響、oracle不足、検証失敗時に独立して反証を探す |

## この参照repository専用Skill

| Skill | 目的・起動条件 |
|---|---|
| `maintain-reference-repository` | dev-standard自身を更新するとき、portable asset、project NFR、documentation、work境界、distribution、互換性をmeta reviewする |

このSkillは導入先の通常開発では起動せず、portableな`default`、`chat-first`、`development-framework` profileへ自動追加しない。明示的な`reference-repository-maintenance`、`skills`、`full` profileを選んだ場合だけcopy対象になり得る。

## フロントエンドSkills

| Skill | 目的・起動条件 |
|---|---|
| `elicit-frontend-requirements` | 利用者、task、context、失敗影響からtest可能なUI要求を獲得する |
| `design-frontend-experience` | 実装前に必要なinteraction decisionとconstraintを定義する。生成可能なas-built情報を手書きで複製しない |
| `implement-frontend-experience` | 要件とdecisionを実装し、complete state、semantics、responsive behaviorを保持する |
| `test-frontend-experience` | task、state、accessibility、responsive、performanceを変更riskに応じて検証する |

Frontend Skillsも通常は恒久work itemや変更ごとの工程文書を要求しない。長期判断はADR、実装構造は生成設計、review判断はreview YAMLへ集約する。

## Regulated専用Skills

次は`regulated` profileでのみ使用する。

| Skill | 目的 |
|---|---|
| `govern-development-request` | 導入先でfull work-item、承認、phase gate、release、auditを進める |
| `author-lifecycle-docs` | 法令・契約・安全・監査上必要なregulated文書だけを作る |
| `authorize-autonomous-execution` | authority、external effect、不可逆操作へ明示承認を結び付ける |
| `retrospect-and-improve` | regulated、重大失敗、反復欠陥時に改善候補を作る |

これらをdirectまたは通常assuredへ自動適用しない。この参照repositoryにはliveな`work/`を保存しない。

## 成果物

すべてのrepository変更:

- 実際の成果物
- 構造化Commit Comment
- `governance/reviews/<change-id>.yaml`
- external CI result

条件付き:

- 永続要件正本
- 人向け生成要件
- project NFRにより必要なdocumentation
- 実装由来as-built設計
- ADR
- 恒久的運用文書
- Issue

詳細は[要件分類標準](standards/REQUIREMENT-CLASSIFICATION.md)、[成果物とチェックのライフサイクル](ARTIFACTS-AND-CHECKS.md)、[Commit Comment契約](COMMIT-COMMENT.md)を参照する。

## 推奨組合せ

- 通常開発: `chat-first-development`
- 要件変更: `maintain-canonical-requirements` + `calibrated-collaborative-listening`
- 実装由来設計: `generate-implementation-design`
- 標準review: `verify-against-engineering-standards` + 必要時`adversarial-review`
- Commit Comment: `japanese-git-commit-gitmoji`
- regulated: `govern-development-request` + regulated専用Skills
- この参照repositoryの保守: `maintain-reference-repository` + 必要な既存Skills
