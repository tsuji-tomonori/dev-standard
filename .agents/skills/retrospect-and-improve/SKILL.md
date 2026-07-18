---
name: retrospect-and-improve
description: Analyze evidence-backed process failures only after regulated work, escaped defects, repeated user corrections, critical control misses, rollback, repeated CI repair, or periodic governance audit. Do not generate a retrospective for every ordinary session or change.
---

# Retrospect and Improve

実際の品質欠陥、利用者影響、反復した非効率から、検証可能な改善候補を作る。

## 起動条件

- active regulated workの終了
- escaped defect
- repeated user correction
- critical control miss
- rollbackまたはincident
- 同一原因のCI再修正
- false blockerの反復
- periodic governance audit

通常セッションの終了、単一のtemplate未入力、形式的なgate errorだけを理由に起動しない。

## 入力

- defect / incident
- user correction
- review YAML
- GitHub Actions / deployment / monitoring結果
- selector miss
- false blocker
- tool / context / reviewer cost
- advisory滞留

生の会話全文、secret、PII、production dumpを保存しない。

## Workflow

1. 防ぎたい実際の成果上の欠陥を特定する。
2. 利用者、security、operation、costへの影響を確認する。
3. 一回限りのnoiseと反復するsystemic failureを分ける。
4. 現行rule、Skill、tool、test、selectorが防げなかった理由を確認する。
5. 新rule以外の代替を先に検討する。
6. 改善案ごとに適用trigger、予想cost、評価方法、rollback、再評価日を定義する。
7. まずshadowまたはAdvisoryとして評価する。
8. 実測で価値が確認された場合だけInvariantまたはblockingへ昇格する。

## 改善候補に必須の内容

- problem
- user / system impact
- evidence
- root cause hypothesis
- proposed change
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
- CIで強制できるものをpromptだけへ追加しない。
- 現在の変更と無関係な改善を同じPRへ混ぜない。

## Completion

- 実際の欠陥または反復costに基づく。
- 新ruleの適用triggerが限定される。
- 既存ruleで代替できない理由がある。
- shadow評価と再評価条件がある。
- 不要なrule増殖を避けている。
