---
name: design-frontend-experience
description: Define minimum interaction, information, accessibility, responsive, and visual decisions before frontend implementation. Persist only long-lived decisions; do not require per-change design or test-plan documents.
---

# Design Frontend Experience

形式契約: `spec/skills/skills.qnt`の`name: "design-frontend-experience"`（保守・監査時に参照）。

approved requirementsを、実装者がproduct behaviorを発明せずに実装できる最小限のdesign decisionへ変換する。

## Inputs

- user request
- canonical requirement IDとacceptance criteria
- elicitationから渡されたdesign context、constraint、priority
- 既存frontend、design system、component、token、route、test
- architecture / ADR
- supported environment
- selected check

problem、user、context、outcomeが不足する場合だけ`$elicit-frontend-requirements`へ戻す。

## Design order

1. primary taskとcompletion path
2. information hierarchyとnavigation
3. contentとterminology
4. state transitionとerror recovery
5. responsive / input modality
6. semantic structure、focus、keyboard
7. visual direction
8. reusable token / component decision

## 必ず決めるもの

変更に該当する範囲だけを決める。

- taskとinformation priority
- 重要なstateとtransition
- destructive actionとrecovery
- permission / privacy boundary
- responsive rule
- keyboard / focus / semantic behavior
- content rule
- existing design systemからの意図的な差異
- acceptanceを検証するhook

## 手書きしないもの

次は実装、type、Storybook、test、route、component、token usageから生成する。

- component inventory
- props / event一覧
- route graph
- state coverage一覧
- ARIA role / accessible name inventory
- token usage
- API call mapping
- test mapping

変更ごとの`docs/03-detailed-design.md`、`docs/03-test-plan.md`を通常は作らない。

## Alternative

結果を大きく左右するdesign choiceでは、2つ以上の実質的なalternativeを比較できる。

比較軸:

- requirement fit
- task completion
- accessibility
- consistency
- implementation cost
- migration
- risk

色だけが異なるdecorative alternativeは作らない。

## ADR

次を満たす判断だけADRへ残す。

- 将来の実装を制約する
- codeだけでは理由が分からない
- 有力なalternativeがある
- 変更costが高い
- 複数team / featureへ影響する

local component detailやcodeから自明な構造はADRにしない。

## Output

- implementationに必要なdecisionとconstraint
- 必要時のprototypeまたはreference
- 必要時のADR
- implementationへ渡すacceptance / verification hook
- implementation / testへ渡すselected check handoff
- 対象repositoryが採用する変更記録のdesign impact判定
- 必要なselected check

一時的な比較noteが必要な場合だけ`.devflow/run/<change-id>/frontend-design-notes.md`へ置き、decision確定後に削除する。

## Implementation readiness

次の場合は未準備である。

- primary taskまたはinformation priorityが不明
- critical state、error、permission、recoveryをimplementerへ丸投げする
- responsive behaviorが画像だけで、ruleがない
- keyboard、focus、semantic behaviorが必要なのに未定義
- existing design systemとの差異に理由がない
- acceptanceまたはverification hookがない

## Completion

- requirementごとに必要なdesign decisionがある。
- codeから生成可能な情報を手書きで複製していない。
- 長期判断だけADRへ残る。
- design impactが対象repositoryの既存方式で追跡できる。
- このSkillのためにCI workflow、required check、branch protection、merge rule、commit形式を追加または変更していない。
- Dev標準の導入・実装では必要なfrontend設計を生成・検査する入口を用意し、未接続なら設計Skillの導入手順でadapterを補う。設計相談だけの場合は未実装のfactを生成せず、実装時の接続へ引き継ぐ。

<!-- BEGIN GENERATED QUINT CONTRACT -->
## Quint contract（自動生成）

このblockは`spec/skills/skills.qnt`から自動生成し、直接編集しません。
詳細・要件trace・digestは`spec/skills/skills.json`の同名契約を、契約の保守・監査時だけ参照します。
repository policyは導入先が所有します。非該当ならartifactやblocking判定を作りません。

- Skill: `design-frontend-experience`
- 柱: auxiliary
- repository blocking: no
- 既定portable: no
- 適用条件: when-frontend-design-is-needed
- 起動context: `frontend-design`
- 外部作用capability: no
- Authority: approved-requirements
- 副作用: repository-write
- 失敗状態: return-to-requirements
<!-- END GENERATED QUINT CONTRACT -->
