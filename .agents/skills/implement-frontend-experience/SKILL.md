---
name: implement-frontend-experience
description: Implement approved frontend requirements and decisions in production code, preserve complete states, semantics, focus, responsive behavior, and design-system intent, then generate as-built design and record selected review evidence. Do not maintain a per-change implementation log.
---

# Implement Frontend Experience

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
10. implementationからroute、component、state、token、API、test mapping等のas-built設計を生成する。
11. selected check resultをreview YAMLへ記録する。
12. `$japanese-git-commit-gitmoji`へ、要件影響、設計影響、review path、検証契約、残存リスクを渡す。

## Evidence

次を直接証拠として使用する。

- Git diff
- codeとtype
- test code
- Storybookまたはcomponent example
- generated as-built design
- GitHub Actions required check
- review YAML
- ADR

`docs/04-implementation-log.md`を作らない。CI結果や生logをGitへ保存しない。

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
- as-built設計が生成されていない

## Completion

- user taskがapplicable stateとsupported contextで動く。
- requirementとdecisionがcode / testへ到達できる。
- as-built設計が実装と一致する。
- selected blocking checkがPassする。
- CI結果は外部サービスにある。
- Commit Commentへdesign impactとverification contractが記録される。
