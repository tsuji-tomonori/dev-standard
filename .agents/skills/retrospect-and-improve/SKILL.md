---
name: retrospect-and-improve
description: Analyze an evidenced escaped defect, incident, rollback, or recurring cost into one bounded improvement candidate. Do not trigger from routine completion, a periodic review alone, or one transient check failure.
---

# Retrospect and Improve

## Formal specification

`spec/skills/skills.qnt` の `skillContracts` にある `name: "retrospect-and-improve"` を形式契約とする。

形式契約の`applicability`と`activationContexts`に該当しない場合は起動せず、artifactやblocking判定を作らないno-opとする。

実際のescaped defect、incident、rollback、または複数観測で確認した反復costから、検証可能な改善候補を一つだけ作る。

## 起動条件

- escaped defect
- incident
- rollback
- 同一原因を持つverification再修正、false blocker、tool / context / reviewer costが複数回観測された場合

具体的義務を持つ作業の終了、periodic audit、利用者訂正、critical missという分類だけでは起動しない。それらから実際のdefect、incident、rollback、または反復costの直接証拠が得られた場合だけ起動する。通常セッションの終了、単一のtemplate未入力、形式的なgate errorだけを理由に起動しない。

## 入力

- escaped defect / incident / rollbackの直接証拠
- 対象repositoryが既に採用するreviewまたは変更記録
- ローカル検査、既存automation、deployment / monitoring結果
- 同一原因のselector miss / false blocker / tool / context / reviewer costについて複数の観測

生の会話全文、secret、PII、production dumpを保存しない。

## Workflow

1. 防ぎたい実際の成果上の欠陥を特定する。
2. 利用者、security、operation、costへの影響を確認する。
3. 一回限りのnoiseと反復するsystemic failureを分ける。
4. 現行rule、Skill、tool、test、selectorが防げなかった理由を確認する。
5. 削除、統合、既存test修正、selector修正など、新ruleより軽い代替を最低一つ比較する。
6. 一つのSkillの一つの予防可能な挙動へscopeを限定し、適用trigger、予想cost、測定可能な評価、実行可能なrollback、再評価またはsunset日を定義する。
7. まずshadowまたはAdvisoryとして評価する。
8. 実測で価値が確認された場合だけInvariantまたはblockingへ昇格する。

候補を機械検査する場合は、`references/improvement-policy.md`に沿う`schema_version: 2`のbounded JSONを`--input`へ渡し、`python <host-skill-path>/scripts/retrospect.py --root . --input <candidate-input.json>`を実行する。`<host-skill-path>`はinstaller receiptとhost adapterが配置した、このSkillのhost-native rootへ解決する。runnerはtriggerと反復証拠を検査し、通常sessionや単一の一時的failed checkには`not_triggered`を返す。候補はstdoutへのbounded `auto_apply: false`結果であり、rule、source、repository設定を変更しない。明示的な`--json-out`を使う場合も新規pathを`.devflow/run/`内へ限定する。

runner inputは`trigger`、direct evidenceを持つ`consequence`、一つのSkill / behaviorを持つ`target`、`problem`、一つ以上の`alternatives`、bounded operation / control / authority deltaを持つ`proposal`、全てfalseの`safety_claims`、`expected`、数値baseline / targetを持つ`evaluation`、実行可能な`rollback`、ISO dateを持つ`sunset`だけを正確に受理する。

## 改善候補に必須の内容

- problem
- user / system impact
- evidence
- root cause hypothesis
- proposed change
- lighter alternative and comparison
- scope / trigger
- expected benefit
- expected cost
- evaluation
- rollback
- review or sunset date

## Boundaries

- gate error回数だけからruleを追加しない。
- 形式的な文書不足を品質欠陥と同一視しない。
- instructionを追加する前に、既存instructionの削除・統合を検討する。
- 決定的なlocal automationまたは対象repositoryの既存checkで検証できるものをpromptだけへ追加しない。
- 現在の変更と無関係な改善を同じPRへ混ぜない。
- authorityを拡大し、checkを弱め、failureを隠し、authorizationを迂回する候補を作らない。
- 全repositoryや全Skillをscopeにせず、一つのSkillの一つの挙動へ限定する。
- `never`、`none`等の実行不能なrollbackや、測定不能な評価を受理しない。

## Completion

- 実際の欠陥または反復costに基づく。
- 新ruleの適用triggerが限定される。
- 既存ruleで代替できない理由がある。
- 一つ以上の軽い代替との比較がある。
- shadow評価と再評価条件がある。
- 実行可能なrollbackとsunsetがある。
- 不要なrule増殖を避けている。

<!-- BEGIN GENERATED QUINT CONTRACT -->
## Quint contract（自動生成）

このblockは`spec/skills/skills.qnt`から生成するviewです。直接編集しません。

- Skill: `retrospect-and-improve`
- 役割: retrospective
- 柱: auxiliary
- guardrail: no
- repository blocking: no
- 既定portable: no
- 適用条件: when-evidenced-systemic-trigger-exists
- 起動context: `evidenced-systemic-failure`
- 外部作用capability: no
- repository policy `ciWorkflow`: false
- repository policy `requiredCheck`: false
- repository policy `branchProtection`: false
- repository policy `ruleset`: false
- repository policy `mergeStrategy`: false
- repository policy `prTemplate`: false
- repository policy `commitFormat`: false
- 前提: an evidenced escaped defect, incident, rollback, or recurring cost exists
- 事後条件: a bounded evaluable improvement is proposed but not automatically applied
- Authority: observed-defect
- 副作用: repository-confined-temporary-write
- 失敗状態: no-op-unless-triggered
- 入力: `defect-incident-rollback-or-recurring-cost-evidence`, `impact`
- 出力: `bounded-candidate-or-not-triggered`, `optional-temporary-json-result`
- 義務: `require-evidenced-systemic-trigger`, `compare-lighter-alternatives`, `define-evaluation-rollback-and-sunset`
- 禁止事項: `do not trigger from one transient check failure`, `do not auto-promote a proposal to a blocking rule`, `do not mix unrelated improvement into the active change`
- 依存Skill: なし
- 必須asset: `references/improvement-policy.md`, `scripts/retrospect.py`
- 要件trace: なし
- manual digest: `d1b329800294b8ea06b8534e4ac958314dd1bd850e5fad0d2428474b5a00bb00`
- payload digest: `8bddd1c183b216d2ff52bc8a016b430b202df65b8f7e1b1177fec4bbf7a1a629`
- interface digest: `b6e41b56a6ba2fe48c3ce901f0d83eac72ad651d9bea2224946efcdacd9eece3`
<!-- END GENERATED QUINT CONTRACT -->
