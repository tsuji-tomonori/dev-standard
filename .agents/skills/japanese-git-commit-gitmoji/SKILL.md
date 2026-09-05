---
name: japanese-git-commit-gitmoji
description: Create a concise Japanese Gitmoji Conventional Commit message when the user or target repository has selected that commit style.
---

# Japanese Git Commit with Gitmoji

## Formal specification

`spec/skills/skills.qnt` の `skillContracts` にある `name: "japanese-git-commit-gitmoji"` を形式契約とする。

形式契約の`applicability`と`activationContexts`に該当しない場合は起動せず、artifactやblocking判定を作らないno-opとする。

利用者または対象repositoryがこの形式を選択している場合だけ使用する。portable default、commit gate、merge条件にはしない。

## Format

```text
<gitmoji> <type>(<scope>): <日本語の要約>

目的:
- <達成する結果>

変更内容:
- <主要変更>

要件影響:
- <あり / なし、ID、理由>

設計影響:
- <あり / なし、対象、理由>

検証:
- <実行したローカル検査、または既存CIへの参照>

互換性・残存リスク:
- <既知事項>
```

代表typeは`feat`、`fix`、`refactor`、`docs`、`test`、`build`、`ci`、`chore`、`revert`、`release`とする。破壊的変更では`!`または`BREAKING CHANGE:`を使用する。

## Rules

- staged diffまたは対象差分から、一つの主目的を選ぶ。
- 実行していない検査をPassと書かない。
- 生ログ、coverage全文、scanner全文を貼り付けない。
- review YAML、required check、特定CI、特定merge方式を必須項目にしない。
- 対象repositoryが別形式を採用している場合は、その形式を優先する。

## Completion

- 1行目が一つの主目的を表す。
- 要件・設計への影響と検証範囲が誤解なく読める。
- 互換性と残存riskを隠していない。

<!-- BEGIN GENERATED QUINT CONTRACT -->
## Quint contract（自動生成）

このblockは`spec/skills/skills.qnt`から生成するviewです。直接編集しません。

- Skill: `japanese-git-commit-gitmoji`
- 役割: commit-message
- 柱: auxiliary
- guardrail: no
- repository blocking: no
- 既定portable: no
- 適用条件: when-user-or-target-selects-style
- 起動context: `target-commit-style`
- 外部作用capability: no
- repository policy `ciWorkflow`: false
- repository policy `requiredCheck`: false
- repository policy `branchProtection`: false
- repository policy `ruleset`: false
- repository policy `mergeStrategy`: false
- repository policy `prTemplate`: false
- repository policy `commitFormat`: false
- 前提: the user explicitly requests this style or the target repository already selects it
- 事後条件: a Japanese structured commit message is proposed
- Authority: explicit-user-or-target-repository-style
- 副作用: none
- 失敗状態: no-op-unless-selected
- 入力: `diff`, `verification-summary`
- 出力: `commit-message`
- 義務: `derive-message-from-actual-diff`, `report-verification-truthfully`, `prefer-target-repository-style`
- 禁止事項: `do not make this style a portable gate`, `do not report unexecuted checks as passing`, `do not require a particular merge method`
- 依存Skill: なし
- 必須asset: なし
- 要件trace: なし
- manual digest: `30135076a592066597be1518d0b2fce03690b729e6069c32ef767e46139cf454`
- payload digest: `74dea666a7d9914d3c92f5bf16d74ae0b6ae1207a68d4da377e74541ed0ff08c`
- interface digest: `3cd81796135cb9dceb62bfdd67ea29d90f7114d9c2e9458e1d848abbbcc82423`
<!-- END GENERATED QUINT CONTRACT -->
