---
name: test-frontend-experience
description: Verify frontend tasks, states, accessibility, responsiveness, visual invariants, and performance by risk without imposing CI, merge policy, or per-change reports.
---

# Test Frontend Experience

形式契約: `spec/skills/skills.qnt`の`name: "test-frontend-experience"`（保守・監査時に参照）。

実装が、対象の人に対象contextでtaskを完了させるかを確認する。render成功やscanner成功だけを品質Passにしない。

## Authority order

1. canonical requirementとacceptanceが期待する利用者向け結果を定義する。
2. approved design decision / ADRが、要件を満たすための意図したinteractionと制約を定義する。
3. implementationとgenerated as-built designが、実際に存在する構造を示す。
4. 実行したtest evidenceが、宣言した範囲のverdictを決める。

下位のartifactで上位authorityとの不一致を正当化しない。不一致はbounded findingと修正handoffとして返す。

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

変更、受入条件、riskに該当する層だけを選択する。全次元の実行やN/A列挙を既定にせず、非該当の層はrunner入力にもblocking判定にも含めない。

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
11. failは、違反したauthority、最小再現、修正先、再実行するtestを含むhandoffとして返す。呼出元に既存の実装依頼があれば、その権限内で修正して再検証できる。別Skillの導入や再承認は不要である。

test commandがnetwork、browser service、external environment等へeffectを持ち得る場合は、その宣言effect、target、現在の明示authority、残存riskを実行前に確認して結果へ残す。test runnerがprocess isolationやexternal effect不在を証明したとは主張しない。

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

このSkillは検証専用であり、production source、要件、design decisionを修正しない。test fixtureやbaselineの更新も、期待結果を定義するauthorityで正当化され、別途変更が依頼された場合だけ実装側へhandoffする。

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

<!-- BEGIN GENERATED QUINT CONTRACT -->
## Quint contract（自動生成）

このblockは`spec/skills/skills.qnt`から自動生成し、直接編集しません。
詳細・要件trace・digestは`spec/skills/skills.json`の同名契約を、契約の保守・監査時だけ参照します。
repository policyは導入先が所有します。非該当ならartifactやblocking判定を作りません。

- Skill: `test-frontend-experience`
- 柱: auxiliary
- repository blocking: no
- 既定portable: no
- 適用条件: when-frontend-testing-is-requested
- 起動context: `frontend-testing`
- 外部作用capability: yes
- Authority: frontend-requirements-and-approved-design
- 副作用: target-command-effects
- 失敗状態: report-bounded
<!-- END GENERATED QUINT CONTRACT -->
