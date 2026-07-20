---
name: design-frontend-experience
description: Define the minimum interaction, information, accessibility, responsive, and visual decisions needed before frontend implementation. Persist long-lived non-obvious decisions as ADRs, generate as-built structure from implementation, and record design impact in the Commit Comment. Do not require per-change detailed-design or test-plan documents.
---

# Design Frontend Experience

approved requirementsを、実装者がproduct behaviorを発明せずに実装できる最小限のdesign decisionへ変換する。

## Inputs

- user request
- canonical requirement IDとacceptance criteria
- 既存frontend、design system、component、token、route、test
- architecture / ADR
- supported environment

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
- Commit Commentのdesign impact判定
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
- design impactがCommit Commentへ記録される。
- 実装後にas-built設計を生成できる。
