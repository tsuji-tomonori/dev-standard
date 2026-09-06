---
name: author-lifecycle-docs
description: Create retained lifecycle evidence only for a concrete legal, contractual, safety, production, audit, or user-specified documentation duty.
---

# Author Regulated Lifecycle Documents

形式契約: `spec/skills/skills.qnt`の`name: "author-lifecycle-docs"`（保守・監査時に参照）。

法令・契約・安全・production・監査または利用者指定による具体的な保持義務がある文書だけを作る。通常変更では要件正本、生成設計、必要なADR、既存の変更・検査記録で足りる。

対象projectの書式があればそれを使い、なければ必要内容に合う最小の構成を選ぶ。工程別templateの存在を作成理由にしない。文書ごとに利用者・目的・対象version・保持期間を明記し、根拠となる実装や検査への参照を示す。詳細設計・実装ログ・生のテスト結果を手書きで複製しない。

継続更新する利用手順・運用説明は更新条件を既存の文書索引へ記す。変更時点で固定する証拠は日付付きの履歴として分け、後から現在状態へ書き換えない。監査保持が不要な一時状態は `.devflow/run/` に置き、用済みになれば削除する。

成果は必要な文書とその根拠・保持規則に限る。保持理由のない文書、CI・branch・merge・commit形式の新たな規則を追加しない。

<!-- BEGIN GENERATED QUINT CONTRACT -->
## Quint contract（自動生成）

このblockは`spec/skills/skills.qnt`から自動生成し、直接編集しません。
詳細・要件trace・digestは`spec/skills/skills.json`の同名契約を、契約の保守・監査時だけ参照します。
repository policyは導入先が所有します。非該当ならartifactやblocking判定を作りません。

- Skill: `author-lifecycle-docs`
- 柱: auxiliary
- repository blocking: no
- 既定portable: no
- 適用条件: when-concrete-duty-exists
- 起動context: `concrete-regulated-duty`
- 外部作用capability: no
- Authority: concrete-duty-or-user
- 副作用: repository-write
- 失敗状態: no-op-unless-triggered
<!-- END GENERATED QUINT CONTRACT -->
