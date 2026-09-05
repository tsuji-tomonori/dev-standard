---
name: implement-frontend-experience
description: Implement approved frontend requirements in production code with complete states, semantics, focus, responsiveness, and design-system intent. Generate as-built design and selected evidence; do not create implementation logs.
---

# Implement Frontend Experience

## Formal specification

`spec/skills/skills.qnt` の `skillContracts` にある `name: "implement-frontend-experience"` を形式契約とする。

形式契約の`applicability`と`activationContexts`に該当しない場合は起動せず、artifactやblocking判定を作らないno-opとする。

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
10. 宣言済みgeneratorが変更artifactを扱う場合だけ、implementationからroute、component、state、token、API、test mapping等のas-built設計を生成し、driftを確認する。対象外なら未生成surfaceを明示し、このSkillだけのためにgeneratorを追加しない。
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
- 宣言済みgeneratorが変更artifactを扱うのに、as-built設計が生成されていない

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

このblockは`spec/skills/skills.qnt`から生成するviewです。直接編集しません。

- Skill: `implement-frontend-experience`
- 役割: frontend-implementation
- 柱: auxiliary
- guardrail: no
- repository blocking: no
- 既定portable: no
- 適用条件: when-frontend-implementation-is-requested
- 起動context: `frontend-implementation`
- 外部作用capability: no
- repository policy `ciWorkflow`: false
- repository policy `requiredCheck`: false
- repository policy `branchProtection`: false
- repository policy `ruleset`: false
- repository policy `mergeStrategy`: false
- repository policy `prTemplate`: false
- repository policy `commitFormat`: false
- 前提: frontend requirements and decisions are ready
- 事後条件: the user task works in supported states and implementation evidence is handed to testing
- Authority: requirements-and-design
- 副作用: repository-write
- 失敗状態: return-to-design
- 入力: `requirements`, `design-decisions`, `existing-frontend`, `selected-check`
- 出力: `frontend-change`, `tests`, `as-built-design`, `selected-check-result`
- 義務: `implement-complete-user-task-states`, `preserve-semantics-and-supported-context`, `handoff-as-built-and-check-evidence`
- 禁止事項: `do not invent product requirements during implementation`, `do not weaken type test or accessibility constraints`, `do not force an unsupported generator`
- 依存Skill: なし
- 必須asset: `references/evidence-map.md`
- 要件trace: なし
- manual digest: `594ea2760c6b4f0ddcc897dee65fac87a05219f2c1bc13a70c2c86bf48d572d1`
- payload digest: `b6ac505f0c8ee8554d0ffc8d330739f636f4363265dd3d6ef23656a67236c911`
- interface digest: `d43aeb305cf1db96d64568e1d231ad529686b1ef3b92c86d8a2c4e0df7f2bb50`
<!-- END GENERATED QUINT CONTRACT -->
