---
name: test-frontend-experience
description: Verify frontend tasks, states, accessibility, responsiveness, visual invariants, and performance according to change risk. Keep automated results in external CI, record selected manual and review decisions in governance/reviews/<change-id>.yaml, and do not create a per-change test report.
---

# Test Frontend Experience

実装が、対象の人に対象contextでtaskを完了させるかを確認する。render成功やscanner成功だけを品質Passにしない。

## Inputs

- user request
- canonical requirementとacceptance
- design decision / ADR
- implementation
- generated as-built design
- supported environment
- selected check

expected outcome、user、context、acceptanceが未定義なら`$elicit-frontend-requirements`へ戻す。failureがmissing design decisionに起因する場合は`$design-frontend-experience`へ戻す。

## Test layers

変更に該当する層だけを選択する。

- static / build: type、lint、markup、token、build
- unit: state transition、validation、logic
- component: semantics、accessible name、keyboard、focus、state
- integration / E2E: complete task、route、data、permission、error、retry
- visual / responsive: invariant、theme、zoom、reflow、content pressure
- accessibility: automated rule + keyboard / focus + 必要なassistive technology
- usability: expert walkthrough、必要時だけrepresentative participant
- performance: loading、responsiveness、layout stability、resource budget

一つの層がPassしたことを理由に、変更risk上必要な別層を省略しない。

## Workflow

1. requirement、task、precondition、environment、action、expected outcome、evidence methodをtestへ落とす。
2. harm、frequency、irreversibility、complexity、change surface、uncertaintyで優先する。
3. happy pathに加え、applicableなloading、empty、partial、stale、offline、validation、system error、conflict、permission、undo、retry、recoveryを確認する。
4. rendered semantics、keyboard、focus、dynamic statusを確認する。
5. contrast、color以外の伝達、zoom、reflow、localization、reduced motionを必要範囲で確認する。
6. automated accessibility resultはtool coverage内の結果として扱い、単独で全体Passにしない。
7. task completion、error prevention / recovery、system status理解を確認する。
8. supported browser、device、locale、theme、inputの宣言範囲内だけを主張する。
9. automated resultをGitHub Actions等へ保持する。
10. selected manual check、N/A、Advisory、residual riskだけをreview YAMLへ記録する。
11. failを修正し、影響するtestを再実行する。

## Repositoryに保存するもの

- test code
- test data
- CI workflow
- generated as-built design
- selected check result YAML
- 必要なscreenshot baselineまたはvisual reference

## Repositoryに保存しないもの

- 変更ごとの`docs/05-test-report.md`
- test log全文
- coverage report全文
- scanner生出力
- browser run log
- GitHub Actions resultの複製

## Verdict

### Automated

外部CIのrequired checkを正本とする。review YAMLにはworkflow名、check名、test pathを参照する。

### Manual / expert

判断が必要なselected checkだけをreview YAMLへ記録する。

### Fail

- Invariant / blocking Risk-selectedは修正する。
- Advisoryは修正、Issue、residual riskへ収束させる。

## Completion

- applicable requirementがtestまたは根拠ある非該当へ対応する。
- critical taskとfailure pathが確認される。
- automated resultとhuman judgmentが区別される。
- claimが実行範囲を超えない。
- blocking checkがPassする。
- external CIが現在HEADを対象としている。
- review YAMLにselected manual resultとresidual riskがある。
- Commit Commentに検証契約がある。
