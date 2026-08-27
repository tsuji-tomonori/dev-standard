---
name: japanese-git-commit-gitmoji
description: Create a concise Japanese Gitmoji Conventional Commit message when the user or target repository has selected that commit style.
---

# Japanese Git Commit with Gitmoji

## Formal specification

`spec/skills/skills.qnt` の `skillContracts` にある `name: "japanese-git-commit-gitmoji"` を形式契約とする。

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
