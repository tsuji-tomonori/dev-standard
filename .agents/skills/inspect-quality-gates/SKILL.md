---
name: inspect-quality-gates
description: Select and run only the checks relevant to the current change, using local evidence or an existing project check without creating CI, merge rules, or review bureaucracy.
---

# Inspect Quality Gates

## Formal specification

`spec/skills/skills.qnt` の `skillContracts` にある `name: "inspect-quality-gates"` を形式契約とする。

変更と受入条件に関係する検査だけを選び、結果を直接確認する。これは3本目のガードレールであり、別の統制層を追加しない。

## Inputs

- 変更差分と受入条件
- 対象repositoryが既に持つtest、lint、type check、build、generator
- 必要な場合だけ、既存のCI結果または人による確認結果

## Workflow

1. 変更した挙動、path、riskから、失敗を検出できる最小の検査を選ぶ。
2. 未選択の検査をN/Aとして列挙しない。
3. まず対象範囲のローカル検査を実行し、必要な場合だけ範囲を広げる。
4. blockingとするのは、受入条件、生成物の整合、機密情報、権限境界など、その変更に直接関係する失敗だけとする。
5. 既存CIがある場合は追加証拠として参照できる。CIがないこと自体を失敗にしない。
6. 結果は会話、既存のPR欄、または対象repositoryが既に採用するartifactへ簡潔に記録する。専用review YAMLを要求しない。

## Boundary

このSkillは次を作成、変更、要求しない。

- CI workflow、required check、status check
- branch protection、ruleset、merge方式、merge先
- PR template、変更ごとのreview YAML、test report、生ログ
- 3本柱以外のportable blocking gate

対象repositoryが既に持つ規則は尊重するが、それをportable契約として複製しない。

## Completion

- 変更と受入条件に対応する検査が選ばれている。
- 選んだblocking検査がPassする。
- 未検証範囲または残存riskがあれば明示されている。
- 証拠は実行範囲を超えて主張していない。
- CIやmerge設定を新たに要求していない。
