---
name: verify-against-engineering-standards
description: Verify only official standards relevant to a change, preserving canonical requirements and reporting bounded evidence without imposing CI or merge policy.
---

# Verify Against Engineering Standards

## Formal specification

`spec/skills/skills.qnt` の `skillContracts` にある `name: "verify-against-engineering-standards"` を形式契約とする。

SWEBOK、cloud Well-Architected、security、accessibility等を、正本要件を上書きしない独立した品質レンズとして使用する。このSkillは任意の補助Skillであり、portable blocking gateではない。

## Selection

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

## Completion

- 現在の変更に関係するcontrolだけが選択される。
- verdictが直接証拠と実行範囲に対応する。
- advisoryと残存riskの扱いが明示される。
- 要件正本と対象repositoryの既存policyを上書きしていない。
