---
name: maintain-reference-repository
description: Preserve dev-standard portability when changing its formal specifications, skills, distribution, tests, or docs without exporting repository-specific policy.
---

# Maintain Reference Repository

形式契約: `spec/skills/skills.qnt`の`name: "maintain-reference-repository"`（保守・監査時に参照）。

`dev-standard`またはportable collectionを保守するforkの仕様、Skill、配布、検査、文書を変更するときに使う。導入先productの通常開発には使わない。

## Authorityと配布境界

- 永続要件は`spec/requirements/requirements.qnt`、Skill契約は`spec/skills/skills.qnt`を編集する。
- `python tools/quintflow.py generate`でJSONとMarkdownを生成する。生成viewを直接編集せず、同じ現在状態を複数の手書きfileで正本化しない。
- 既定portable setは`chat-first-development`と要件・実装由来設計・関係する検査の3本柱だけとする。
- 導入先のbranch、merge、CI workflow、required check、PR template、commit形式、既存の指示とownershipを維持する。参照repository固有のworkflow、履歴、review recordを配布しない。

## 変更と検証

変更した契約、Skill本文、manifest、installer、docs、testsを整合させる。本文は非自明な判断・実行境界・必要時に読む参照に絞り、常時読む指示へ全schema、digest、固定のモデル設定や一般的な手順を複製しない。

ローカル検査は変更に関係する範囲で行い、全体の契約変更には`make verify`を使う。SkillとQuint契約の1対1対応、生成drift、default set、依存assetの配布完結性、導入先設定の不変性を確認する。既存CIは追加証拠にする。

モデル更新時は公式ガイドと実際の失敗を根拠に指示を削減・修正する。文字量や静的testの成功だけでモデルの品質向上を断言せず、モデル固有の調整は対象環境で評価する。live work record、生ログ、利用者固有情報をportable assetへ含めない。

<!-- BEGIN GENERATED QUINT CONTRACT -->
## Quint contract（自動生成）

このblockは`spec/skills/skills.qnt`から自動生成し、直接編集しません。
詳細・要件trace・digestは`spec/skills/skills.json`の同名契約を、契約の保守・監査時だけ参照します。
repository policyは導入先が所有します。非該当ならartifactやblocking判定を作りません。

- Skill: `maintain-reference-repository`
- 柱: auxiliary
- repository blocking: no
- 既定portable: no
- 適用条件: when-reference-assets-change
- 起動context: `reference-maintenance`
- 外部作用capability: no
- Authority: reference-repository
- 副作用: repository-write
- 失敗状態: report-bounded
<!-- END GENERATED QUINT CONTRACT -->
