---
name: retrospect-and-improve
description: Analyze an evidenced escaped defect, incident, rollback, or recurring cost into one bounded improvement candidate. Do not trigger from routine completion, a periodic review alone, or one transient check failure.
---

# Retrospect and Improve

形式契約: `spec/skills/skills.qnt`の`name: "retrospect-and-improve"`（保守・監査時に参照）。

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

このblockは`spec/skills/skills.qnt`から自動生成し、直接編集しません。
詳細・要件trace・digestは`spec/skills/skills.json`の同名契約を、契約の保守・監査時だけ参照します。
repository policyは導入先が所有します。非該当ならartifactやblocking判定を作りません。

- Skill: `retrospect-and-improve`
- 柱: auxiliary
- repository blocking: no
- 既定portable: no
- 適用条件: when-evidenced-systemic-trigger-exists
- 起動context: `evidenced-systemic-failure`
- 外部作用capability: no
- Authority: observed-defect
- 副作用: repository-confined-temporary-write
- 失敗状態: no-op-unless-triggered
<!-- END GENERATED QUINT CONTRACT -->
