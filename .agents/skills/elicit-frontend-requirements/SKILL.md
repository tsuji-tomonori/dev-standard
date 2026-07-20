---
name: elicit-frontend-requirements
description: Discover human-centred, testable frontend requirements from users who may not know design terminology. Persist only durable obligations in the canonical requirements, use temporary notes only in .devflow/run when necessary, and record requirement impact in the Commit Comment. Do not require a permanent work item or per-change lifecycle documents.
---

# Elicit Frontend Requirements

利用者のtask、context、失敗影響、制約から、実装と検証に必要なfrontend要求を明らかにする。

## Composition

- ambiguityが結果を変える場合だけ`$calibrated-collaborative-listening`を使う。
- 永続的な義務だけを`$maintain-canonical-requirements`へ渡す。
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
11. 要件影響、ID、理由をCommit Commentへ記録する。

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

- 永続要件のadd / update / retire
- requirement IDとacceptance criteria
- designへ渡すcontext、constraint、priority
- requirement impactを含むCommit Comment
- 必要なselected check

独立した変更ごとのrequirements reportは作らない。
