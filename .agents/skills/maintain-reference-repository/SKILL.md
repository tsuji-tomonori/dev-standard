---
name: maintain-reference-repository
description: Preserve dev-standard as a portable reference and sample repository when changing its skills, agents, standards, governance, distribution, tests, or documentation. Use for changes to this repository itself. Separate reusable product behavior from project nonfunctional obligations, prevent repository-specific work records from becoming samples, and keep authority, distribution, compatibility, and evidence boundaries explicit.
---

# Maintain Reference Repository

このrepository自身を更新するとき、導入先projectの実作業と、移植可能な参照資産を混同しない。

## Repository identity

`dev-standard`は、Skills、agents、generator、schema、check catalog、installer、標準文書のsample / reference collectionである。導入先productの稼働中projectではない。

次をrepository固有の恒久成果物として残さない。

- liveな`work/<id>/`
- 実依頼のapproval chainやphase記録
- 変更ごとのexecution plan、implementation log、test report、release report、retrospective
- GitHub Actionsや外部serviceの生結果
- 会話transcript、利用者固有情報、production evidence

regulated runtimeのcode、template、schema、validatorはsampleとして維持できる。実行中のwork itemは導入先repositoryで生成する。synthetic fixtureが必要な場合は`tests/fixtures/`等へ置き、実案件と誤認できない名前と内容にする。

## Apply this Skill

次のいずれかを変更するときに使用する。

- `.agents/skills/`または`.codex/agents/`
- `distribution/manifest.json`またはinstaller
- `governance/`、check catalog、review contract
- `spec/requirements/`または要件生成logic
- `docs/`、README、CONTRIBUTING、AGENTS
- sample、fixture、template、profile、repository layout

導入先productの通常実装では起動しない。portableな`default`、`chat-first`、`development-framework` profileへこのSkillを自動追加しない。

## Required lenses

### 1. Portability

- repository名、現在のPR、個人、組織、実環境へ不必要に依存していないか。
- copyされたartifactが導入先だけで意味を持つか。
- sample値とproduction値を区別できるか。
- target repositoryの`AGENTS.md`、ownership、build、security ruleを上書きしないか。

### 2. Requirement classification

`docs/standards/REQUIREMENT-CLASSIFICATION.md`に従い、まず`product` / `project`を分け、次に`functional` / `nonfunctional`を分ける。

- Skillやtoolの外部挙動・品質はproduct requirementとして扱う。
- 開発、保守、review、配布、文書化の義務はproject requirementとして扱う。
- documentation requirementは原則`project / nonfunctional`とする。
- 利用者へ表示するhelp、message、帳票等、その内容自体がproduct behaviorならproduct requirementとして扱う。

今回だけの作業手順をproject requirementへ昇格させない。

### 3. Authority

- 永続要件: `spec/requirements/requirements.json`
- 人向け要件: 正本から生成した`docs/requirements/REQUIREMENTS.md`
- 実装由来設計: `docs/design/generated/`
- 長期判断の理由: ADR
- check定義: `governance/checks/catalog.yaml`
- 変更証跡: Commit Comment、review YAML、PR、外部CI

同じ現在状態を複数の手書きfileで正本化しない。

### 4. Documentation as project NFR

恒久文書を追加または更新する場合、対応するproject NFRについて次を確認する。

1. audience
2. purpose
3. authority
4. update trigger
5. verification
6. maintenance rule
7. retirement condition

文書が必要なのではなく、読者が達成すべき結果と維持すべき品質が必要である。要件正本へ義務を置き、文書pathはtraceにする。

### 5. Distribution boundary

- 新しいportable assetをどのprofileへ含めるかを明示する。
- repository-maintenance専用assetをdefault profileへ混入させない。
- manifest、installer test、Skills一覧を同時に更新する。
- repository固有のreview YAML、work record、CI resultを配布しない。
- profile追加は既存profileのcopy結果を破壊しない。

### 6. Self-hosting

このrepository自身が定義する規則を変更する場合、規則、実装、sample、test、説明を一つの変更で整合させる。ただし、変更ごとの重複文書を増やして自己証明しない。

## Workflow

1. 依頼をportable collectionの変更として言い換える。
2. product / projectとfunctional / nonfunctionalを判定する。
3. 永続要件の意味が変わる場合だけ`$maintain-canonical-requirements`を使う。
4. 必要なartifactだけを更新し、liveな`work/`を作らない。
5. Skill、standard、manifest、installer、test、root instructionの影響を確認する。
6. repository固有の値、履歴、証跡がportable artifactへ混入していないかreviewする。
7. selected check、Commit Comment、PR、現在HEADのCIで変更を確定する。

## Meta review questions

- この差分は導入先へ持ち出せる規則か、このrepositoryだけの一時事情か。
- 永続要件と変更証跡を混同していないか。
- documentの存在ではなく、project NFRを定義しているか。
- `work/`、log、report、approvalをsampleとして残していないか。
- default profileへrepository-maintenance専用Skillを混入させていないか。
- distribution manifestと実際のfile treeが一致しているか。
- 既存consumerに互換性破壊がある場合、migrationまたはversioningが明示されているか。
- 新しい規則が防ぐ具体的な欠陥と、追加costが釣り合っているか。

## Completion

- top-levelの`work/`が存在しない。
- liveなrepository固有work recordが他pathへ移動していない。
- documentation requirementの分類とauthorityが明示されている。
- `docs/SKILLS.md`と`distribution/manifest.json`がSkill treeと整合する。
- portable profileにこのrepository専用Skillが暗黙追加されていない。
- contract testがwork境界、分類、distributionを検証する。
- Commit Commentとreview YAMLが現在の差分を説明する。
