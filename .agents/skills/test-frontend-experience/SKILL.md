---
name: test-frontend-experience
description: Verify frontend tasks, states, accessibility, responsiveness, visual invariants, and performance by risk without imposing CI, merge policy, or per-change reports.
---

# Test Frontend Experience

## Formal specification

`spec/skills/skills.qnt` の `skillContracts` にある `name: "test-frontend-experience"` を形式契約とする。

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
9. automated resultをローカル出力または対象repositoryの既存CIで確認する。
10. selected manual check、N/A、Advisory、residual riskだけを会話または既存の変更記録へ簡潔に残す。
11. failを修正し、影響するtestを再実行する。

## Repositoryに保存するもの

- test code
- test data
- generated as-built design
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

実行したcommand、test path、対象範囲を直接証拠とする。既存CIがある場合は追加証拠として参照できる。

### Manual / expert

判断が必要なselected checkだけを簡潔に記録する。

### Fail

- Invariant / blocking Risk-selectedは修正する。
- Advisoryは修正、Issue、residual riskへ収束させる。

## Completion

- applicable requirementがtestまたは根拠ある非該当へ対応する。
- critical taskとfailure pathが確認される。
- automated resultとhuman judgmentが区別される。
- claimが実行範囲を超えない。
- blocking checkがPassする。
- 検証結果が対象差分と実行範囲に対応する。
- selected manual resultとresidual riskが必要な場合だけ記録される。
- このSkillのためにCI workflow、required check、branch protection、merge ruleを追加または変更していない。
