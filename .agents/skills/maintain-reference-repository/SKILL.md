---
name: maintain-reference-repository
description: Preserve dev-standard portability when changing its formal specifications, skills, distribution, tests, or docs without exporting repository-specific policy.
---

# Maintain Reference Repository

## Formal specification

`spec/skills/skills.qnt` の `skillContracts` にある `name: "maintain-reference-repository"` を形式契約とする。

形式契約の`applicability`と`activationContexts`に該当しない場合は起動せず、artifactやblocking判定を作らないno-opとする。

`dev-standard`自身を更新するとき、導入先へ持ち出す3本柱と、このrepositoryだけの実行環境を分離する。

このSkillは`dev-standard`または同じportable collectionを保守するforkの仕様、Skill、distribution、検査、文書を変更するときだけ起動する。導入先product repositoryの通常開発には起動せず、導入先へこのrepository固有のrelease・branch・CI規則を持ち込まない。

## Authority

- 要件正本: `spec/requirements/requirements.qnt`
- 要件の機械view: `spec/requirements/requirements.json`
- 要件の人向けview: `docs/requirements/REQUIREMENTS.md`
- 全Skillの形式契約: `spec/skills/skills.qnt`
- Skill契約の機械view: `spec/skills/skills.json`
- 実装由来設計: `docs/design/generated/`
- 長期判断の理由: ADR

生成viewを直接編集せず、同じ現在状態を複数の手書きfileで正本化しない。

## Portable boundary

default portable setが配布するガードレールは次の3本だけとする。

1. durableな原子要件
2. 実装由来のas-built設計
3. 変更に関係する検査だけ

導入先へ適用するとき、installerとmanifestは次を追加も変更もしない。

- `.github/workflows/`等のCI設定とrequired check
- branch protection、ruleset、branch構成
- merge方式、merge先、release topology
- PR template、commit形式、変更ごとのreview YAML

対象repositoryの既存file、指示、ownership、build、security ruleを維持する。

## Workflow

1. 変更をportable collectionの変更として言い換える。
2. 永続要件が変わる場合は`requirements.qnt`を更新する。
3. Skillの契約が変わる場合は`skills.qnt`と該当`SKILL.md`を同時に更新する。
4. `python tools/quintflow.py generate`で派生viewを更新する。
5. manifest、installer、docs、testsを最小範囲で整合させる。
6. default portable setが3本柱と会話entry pointだけであることを確認する。
7. repository固有のworkflow、履歴、review record、live work item、生ログが配布されないことを確認する。
8. ローカル検査を通し、既存CIがある場合だけ追加証拠として確認する。

## Completion

- 18 SkillとQuint契約が1対1で対応する。
- default portable setは会話entry pointと3本柱だけを含む。
- どの配布構成も導入先のCI、branch、merge設定へ触れない。
- Quint、JSON、Markdownの生成driftがない。
- installer isolation testとrepository testが通る。
- live work record、生ログ、利用者固有情報がportable assetへ混入していない。

<!-- BEGIN GENERATED QUINT CONTRACT -->
## Quint contract（自動生成）

このblockは`spec/skills/skills.qnt`から生成するviewです。直接編集しません。

- Skill: `maintain-reference-repository`
- 役割: reference-maintenance
- 柱: auxiliary
- guardrail: no
- repository blocking: no
- 既定portable: no
- 適用条件: when-reference-assets-change
- 起動context: `reference-maintenance`
- 外部作用capability: no
- repository policy `ciWorkflow`: false
- repository policy `requiredCheck`: false
- repository policy `branchProtection`: false
- repository policy `ruleset`: false
- repository policy `mergeStrategy`: false
- repository policy `prTemplate`: false
- repository policy `commitFormat`: false
- 前提: dev-standard or its portable-collection fork changes portable assets
- 事後条件: portable and repository-specific assets remain separated
- Authority: reference-repository
- 副作用: repository-write
- 失敗状態: report-bounded
- 入力: `reference-change`, `distribution-boundary`
- 出力: `portable-assets`, `compatibility-result`
- 義務: `separate-portable-and-reference-only-assets`, `keep-default-portable-set-to-entry-and-three-pillars`, `verify-portable-dependency-closure`
- 禁止事項: `do not invoke for ordinary target-product changes`, `do not export reference-repository policy`, `do not edit generated views directly`
- 依存Skill: なし
- 必須asset: なし
- 要件trace: なし
- manual digest: `38c711380cc19a84d24c54033bf2a97dbaaaadd70621e6efaeb5f041cab4c367`
- payload digest: `a326bcc3756108c0dc1a8d07cb16a5bd85d63a7f4fb0aee45f7a5bed6b8656d4`
- interface digest: `4d1d390ff78d7538d4905e2af1e09699ada5bfdc594b4466ccc117ce6c09e68e`
<!-- END GENERATED QUINT CONTRACT -->
