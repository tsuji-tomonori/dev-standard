---
name: implement-frontend-experience
description: Implement approved frontend requirements in production code with complete states, semantics, focus, responsiveness, and design-system intent. Generate as-built design and selected evidence; do not create implementation logs.
---

# Implement Frontend Experience

形式契約: `spec/skills/skills.qnt`の`name: "implement-frontend-experience"`（保守・監査時に参照）。

要件と最小限のdesign decisionを、既存stackとdesign systemに適合するproduction codeへ変換する。

## Inputs

- user request
- canonical requirements
- approved design decision / ADR
- existing frontendとdesign system
- test infrastructure
- selected check

behavior、state、content、responsive、accessibility contractが不足する場合だけ`$design-frontend-experience`へ戻す。

## Workflow

1. framework、route、state、data fetching、form、validation、i18n、test、build conventionを調査する。
2. native semantics、existing token / component、feature pattern、design-system extension、local primitiveの順で再利用する。
3. 一つのuser taskと関連stateを完了するvertical sliceで実装する。
4. semantic structureとinteractionを先に実装し、visual stylingを適用する。
5. applicableなdefault、loading、empty、partial、stale、offline、validation、system error、permission、success、undo、retryを実装する。
6. keyboard、focus、pointer、touch、accessible name、status announcement、reduced motionを必要範囲で実装する。
7. long content、localization、zoom、reflow、supported viewportでresponsive ruleを確認する。
8. stable design roleにはsemantic tokenを使い、local numberごとにtokenを増やさない。
9. targeted type、build、lint、component / unit / browser testを小さいsliceごとに実行する。
10. Dev標準の導入・実装では、route、component、state、token、API、test mapping等の必要なas-built設計を生成し、driftを確認する。generator未接続なら設計Skillの導入手順でadapterを補い、未生成の必要領域を残して完了にしない。frontend Skillだけを単独で利用する場合は、対象projectが採用した設計契約に従う。
11. selected check resultを会話または対象repositoryが既に採用する変更記録へ簡潔に残す。
12. 利用者または対象repositoryが指定した場合だけ、既存のcommit形式へ要件影響、設計影響、検証範囲、残存リスクを渡す。

## Evidence

次を直接証拠として使用する。

- Git diff
- codeとtype
- test code
- Storybookまたはcomponent example
- generated as-built design
- 実行したローカル検査、または既存CIへの参照
- ADR

`docs/04-implementation-log.md`を作らない。CI結果や生logをGitへ保存しない。このSkillのためにCI workflow、required check、branch protection、merge ruleを追加または変更しない。

## Boundaries

- coding中にproduct requirementを黙って追加しない。
- design defectを見つけた場合はdecisionまたはADRを更新する。
- 新しいproduct obligationが必要なら要件正本へ戻す。
- existing componentを理解せず複製しない。
- screenshotだけに最適化しない。
- type、lint、test、accessibility constraintを弱めない。
- generic element + ARIAでnative controlを不必要に再実装しない。

## Code review readiness

次の場合は未準備である。

- applicable requirementにcodeまたは明示的な非該当理由がない
- happy pathしかない
- keyboard / focusが偶然のbrowser behaviorに依存する
- existing token / componentを重複実装する
- responsive behaviorがrepresentative contentで失敗する
- approved decisionとの差異が未解決
- testがCSS詳細だけを確認し、user-visible outcomeを検証しない
- 採用した設計契約で必要なas-built設計が生成されていない

## Completion

- user taskがapplicable stateとsupported contextで動く。
- requirementとdecisionがcode / testへ到達できる。
- 宣言済みgeneratorの対象ではas-built設計が実装と一致し、対象外では未生成surfaceが明示される。
- selected blocking checkがPassする。
- 実行した検査の範囲と結果が明確である。
- design impactと検証範囲が対象repositoryの既存方式で追跡できる。
- test Skillへfrontend change、test、as-built結果、selected check resultが渡される。

<!-- BEGIN GENERATED QUINT CONTRACT -->
## Quint contract（自動生成）

このblockは`spec/skills/skills.qnt`から自動生成し、直接編集しません。
詳細・要件trace・digestは`spec/skills/skills.json`の同名契約を、契約の保守・監査時だけ参照します。
repository policyは導入先が所有します。非該当ならartifactやblocking判定を作りません。

- Skill: `implement-frontend-experience`
- 柱: auxiliary
- repository blocking: no
- 既定portable: no
- 適用条件: when-frontend-implementation-is-requested
- 起動context: `frontend-implementation`
- 外部作用capability: no
- Authority: requirements-and-design
- 副作用: repository-write
- 失敗状態: return-to-design
<!-- END GENERATED QUINT CONTRACT -->
