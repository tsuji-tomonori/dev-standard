---
name: verify-against-engineering-standards
description: Verify only official standards relevant to a change, preserving canonical requirements and reporting bounded evidence without imposing CI or merge policy.
---

# Verify Against Engineering Standards

## Formal specification

`spec/skills/skills.qnt` の `skillContracts` にある `name: "verify-against-engineering-standards"` を形式契約とする。

形式契約の`applicability`と`activationContexts`に該当しない場合は起動せず、artifactやblocking判定を作らないno-opとする。

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

このblockは`spec/skills/skills.qnt`から生成するviewです。直接編集しません。

- Skill: `verify-against-engineering-standards`
- 役割: standards-lens
- 柱: auxiliary
- guardrail: no
- repository blocking: no
- 既定portable: no
- 適用条件: when-a-relevant-standard-is-selected
- 起動context: `relevant-standard`
- 外部作用capability: no
- repository policy `ciWorkflow`: false
- repository policy `requiredCheck`: false
- repository policy `branchProtection`: false
- repository policy `ruleset`: false
- repository policy `mergeStrategy`: false
- repository policy `prTemplate`: false
- repository policy `commitFormat`: false
- 前提: a relevant standard is selected for the change
- 事後条件: only applicable controls have evidence-bounded findings without overriding canonical authority, and any requested generated source document stays repository-confined
- Authority: canonical-requirements-target-policy-and-selected-official-standards
- 副作用: repository-write
- 失敗状態: report-bounded
- 入力: `change`, `requirements`, `target-policy`, `skill-default-standards-registry`, `source-context`, `optional-repository-output`
- 出力: `selected-standards`, `selected-controls`, `standard-findings`, `residual-risk`, `requirement-handoff`, `generated-sources-doc-when-requested`
- 義務: `select-only-relevant-official-controls`, `preserve-standard-version-and-freshness`, `derive-verdict-from-direct-evidence`, `confine-generated-output-to-target-repository`
- 禁止事項: `do not override canonical requirements with external standards`, `do not claim certification or exhaustive compliance`, `do not write outside the target repository or create CI or merge policy`
- 依存Skill: なし
- 必須asset: `assets/standards.registry.json`, `references/as-built-design-check-selection.md`, `references/source-policy.md`, `scripts/standardsflow.py`
- 要件trace: `REQ-ASBUILT-012`, `REQ-ASBUILT-013`, `REQ-ASBUILT-014`, `REQ-ASBUILT-015`, `REQ-DOCS-001`, `REQ-QUALITY-001`, `REQ-QUALITY-003`
- manual digest: `c8af30668eff4b9a6f011eb7045ce7186d8946b5cc4747b984b916ad306ad90e`
- payload digest: `1ee8c37168749ce8fb21781a9b4fcf2a794fc7d9216a8ea8c3f9f08391f18f4e`
- interface digest: `4849946704e4fff8bf109eb0ad4eff8513f9e717cd21e00f79893f68cdb9cd89`
<!-- END GENERATED QUINT CONTRACT -->
