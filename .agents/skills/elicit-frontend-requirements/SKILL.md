---
name: elicit-frontend-requirements
description: Discover human-centred, testable frontend requirements without requiring design terminology. Persist only durable obligations and avoid permanent work items or per-change lifecycle documents.
---

# Elicit Frontend Requirements

## Formal specification

`spec/skills/skills.qnt` の `skillContracts` にある `name: "elicit-frontend-requirements"` を形式契約とする。

形式契約の`applicability`と`activationContexts`に該当しない場合は起動せず、artifactやblocking判定を作らないno-opとする。

利用者のtask、context、失敗影響、制約から、実装と検証に必要なfrontend要求を明らかにする。

## Composition

- ambiguityが結果を変える場合だけ`$calibrated-collaborative-listening`を使う。
- 永続的な義務だけを`$maintain-canonical-requirements`へ渡し、solution候補は共通のnecessity、authority、lifetime、scope、placement判定を通す。
- accessibility、法令、platform conventionが実質的に関係する場合だけ`$verify-against-engineering-standards`を使う。
- 高影響flow、排除risk、高額な作り直しriskでは必要時だけ`$adversarial-review`を使う。

`$author-lifecycle-docs`、恒久work item、変更ごとのrequirements documentを通常は使用しない。

## Workflow

1. 既存screen、navigation、terminology、component、token、supported environment、関連要件を調査する。
2. user problemと想定solutionを分離する。
3. people、role、task、frequency、urgency、error consequence、recoveryを確認する。
4. device、viewport、input、network、privacy、interruption等のcontextを確認する。
5. 回答がscope、interaction、priority、accessibility、risk、acceptanceを変える質問だけを行う。
6. observable outcomeとして要求を定義する。
7. applicableなloading、empty、partial、error、permission、success、recovery stateを確認する。
8. keyboard、zoom、reflow、localization、assistive technology等の必要範囲を確認する。
9. durable obligationを原子要件へ変換し、正本へadd / update / retireする。
10. designで決める仮説と、product requirementを区別する。
11. 要件影響、ID、理由を会話または対象repositoryが既に採用する変更記録へ残す。

一時的なinterview noteが必要な場合だけ`.devflow/run/<change-id>/frontend-notes.md`を使用し、正本適用後に削除する。

## Requirement quality

frontend requirementは次の場合に未完成である。

- user outcomeなしにsolutionだけを固定する
- intuitive、modern、simple等の未検証形容詞だけである
- applicableなfailure / empty / loading / permission / recoveryが欠ける
- mouse、vision、color perception、memory、language、device能力を根拠なく仮定する
- 独立義務を一つのIDに結合する
- acceptanceまたはverification方法がない
- user need、decision、sourceへのtraceがない

## Output

- 正本へ適用済みの永続要件add / update / retire、または変更不要という判定
- requirement IDとacceptance criteria
- designへ渡すcontext、constraint、priority
- requirement impactを含む簡潔な変更記録
- design / implementation / testへ渡すselected check

このSkillはcommit形式、CI workflow、required check、branch protection、merge ruleを作成も要求もしない。

独立した変更ごとのrequirements reportは作らない。

<!-- BEGIN GENERATED QUINT CONTRACT -->
## Quint contract（自動生成）

このblockは`spec/skills/skills.qnt`から生成するviewです。直接編集しません。

- Skill: `elicit-frontend-requirements`
- 役割: frontend-requirements
- 柱: auxiliary
- guardrail: no
- repository blocking: no
- 既定portable: no
- 適用条件: when-frontend-requirements-are-needed
- 起動context: `frontend-requirements`
- 外部作用capability: no
- repository policy `ciWorkflow`: false
- repository policy `requiredCheck`: false
- repository policy `branchProtection`: false
- repository policy `ruleset`: false
- repository policy `mergeStrategy`: false
- repository policy `prTemplate`: false
- repository policy `commitFormat`: false
- 前提: a frontend outcome is requested
- 事後条件: durable observable obligations are maintained in canonical requirements and design context is handed forward
- Authority: user-intent
- 副作用: repository-write
- 失敗状態: return-for-clarification
- 入力: `user-task`, `context`, `failure-impact`
- 出力: `canonical-requirement-delta`, `design-context`, `selected-check`
- 義務: `separate-user-problem-from-solution`, `maintain-durable-obligations`, `handoff-context-and-selected-checks`
- 禁止事項: `do not persist temporary interview notes`, `do not create per-change requirement reports`, `do not impose repository policy`
- 依存Skill: なし
- 必須asset: `references/evidence-map.md`
- 要件trace: `REQ-DISC-005`
- manual digest: `182dcaa3aa9c453416c979f33b4d7ddda3d3db66aeb530d519a4aaaa3ad8cc20`
- payload digest: `9e4bcabfece7a6685a9cb07399e6c8a10ee7a72c760dbbd1b20f91df671f4bb4`
- interface digest: `01653ab1c807a2841aa48a2eeea4a8da57eaf31227066664929c8dea2cfc4e1b`
<!-- END GENERATED QUINT CONTRACT -->
