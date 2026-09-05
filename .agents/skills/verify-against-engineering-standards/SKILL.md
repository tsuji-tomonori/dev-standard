---
name: verify-against-engineering-standards
description: Verify only official standards relevant to a change, preserving canonical requirements and reporting bounded evidence without imposing CI or merge policy.
---

# Verify Against Engineering Standards

形式契約: `spec/skills/skills.qnt`の`name: "verify-against-engineering-standards"`（保守・監査時に参照）。

SWEBOK、cloud Well-Architected、security、accessibility等を、正本要件を上書きしない独立した品質レンズとして使用する。このSkillは任意の補助Skillであり、portable blocking gateではない。

## Authority order

1. canonical requirementと対象repositoryの既存policyが、満たすべきproduct / project obligationを定義する。
2. versionと鮮度を記録した公式標準が、選択controlの内容を定義する。
3. repository artifactと実行した検査がverdictの直接証拠となる。

外部標準を理由に正本要件を黙って追加・上書きせず、新しいdurable obligationが必要なら要件変更候補としてhandoffする。

## Selection

- 既定registryはSkill自身の`assets/standards.registry.json`であり、導入先へ`governance/standards/registry.json`の作成を要求しない。対象repositoryが明示的に所有する別registryがある場合だけ`--registry`で選択する。
- changed path、artifact、risk、requirement / design impactから関係するcontrolだけを選ぶ。
- 未選択controlをN/Aとして保存しない。
- 外部標準の鮮度は、期限到達、対象標準の変更、公式更新の証拠、法令・契約上の必要がある場合だけ確認する。
- as-built関連は`references/as-built-design-check-selection.md`から対象artifactのcontrolだけを選ぶ。

## Verdict

- `Pass`: test、generator、repository path、公式資料等の直接証拠がある。
- `N/A`: 選択後に具体的な適用外事実が判明した場合だけ理由を示す。
- `Advisory`: 修正、Issue、または残存riskとして扱うが、単独で変更を停止しない。
- `Fail`: 正本要件または選択したblocking条件に反する場合は修正する。

## Boundary

- checklistだけから完全準拠、認証、網羅性を主張しない。
- CI workflow、required check、branch protection、merge ruleを作成も要求もしない。
- 対象repositoryが既に持つCIは証拠として参照できるが、ローカルの決定的検査も同等に扱う。
- 専用review YAML、全catalog結果、生ログを要求しない。

`scripts/standardsflow.py validate`と`check`はread-onlyである。`generate`だけが明示的なrepository writeであり、`--root`内の`--out`へ決定的な一覧を生成する。absolute escape、`..`、symlink traversal、repository外pathを拒否する。通常のstandard reviewではgeneratorを実行せず、文書生成が依頼された場合だけ使用する。

## Completion

- 現在の変更に関係するcontrolだけが選択される。
- verdictが直接証拠と実行範囲に対応する。
- advisoryと残存riskの扱いが明示される。
- 要件正本と対象repositoryの既存policyを上書きしていない。

<!-- BEGIN GENERATED QUINT CONTRACT -->
## Quint contract（自動生成）

このblockは`spec/skills/skills.qnt`から自動生成し、直接編集しません。
詳細・要件trace・digestは`spec/skills/skills.json`の同名契約を、契約の保守・監査時だけ参照します。
repository policyは導入先が所有します。非該当ならartifactやblocking判定を作りません。

- Skill: `verify-against-engineering-standards`
- 柱: auxiliary
- repository blocking: no
- 既定portable: no
- 適用条件: when-a-relevant-standard-is-selected
- 起動context: `relevant-standard`
- 外部作用capability: no
- Authority: canonical-requirements-target-policy-and-selected-official-standards
- 副作用: repository-write
- 失敗状態: report-bounded
<!-- END GENERATED QUINT CONTRACT -->
