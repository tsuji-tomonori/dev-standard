---
name: maintain-reference-repository
description: Maintain dev-standard skills, distribution, and current documentation together when their behavior or usage changes, while preserving the three pillars and target repository policy.
---

# Maintain Reference Repository

形式契約: `spec/skills/skills.qnt`の`name: "maintain-reference-repository"`（保守・監査時に参照）。

`dev-standard`またはportable collectionを保守するforkを変更するときに使う。導入先productの通常開発には使わない。利用者の明示指示をこのSkillの一般ガイドより優先し、有効な承認を再確認しない。

## 正本と配布

永続要件は `spec/requirements/requirements.qnt`、Skill契約は `spec/skills/skills.qnt` を編集する。本文・必須asset・interfaceを変えた契約のdigestを実体から更新し、`python tools/quintflow.py generate`でJSON・Markdownを再生成する。生成viewを手編集しない。

既定は `chat-first-development` と3本柱の4 Skill。導入先のbranch、merge、CI、commit形式、既存指示は導入先が所有する。参照repository固有のworkflow・履歴を配布しない。

## 変更に伴う文書保守

[文書索引](../../../docs/README.md)の目的・更新条件から、差分に関係する文書だけを選ぶ。

- 変更した入力・出力・実行command・対応能力・失敗条件を、実装、Skill、配布manifest、利用ガイドで照合する。command例は実際のCLIと確認する。
- 同じ内容の手書き複製は統合する。不要な文書・templateは実行・配布の呼出元を調べ、不要な呼出元・生成処理・存在だけを要求する検査も一緒に削除する。動作上の検査は維持する。
- 残す手書き文書の利用者・目的・更新条件を索引へ反映する。索引以外に同じ文書台帳を作らず、機能無関係の文書を毎回更新しない。
- 時点の監査・廃止判断は日付付き `docs/archive/` へ分離し、更新対象外・対象日を表示する。履歴を現行仕様へ書き換えない。再開用情報は `.devflow/run/` だけに置く。
- 生成物は正本から再生成し、現在文書のリンク・要件trace・利用手順を検査する。過去の合格記録を今回の検証結果として扱わない。

## 検証と完了

変更に関係する最小の検査を選び、全体契約の変更には `make verify` を使う。Skillと契約の1対1対応、生成差分、既定4 Skill、配布依存の完結性、導入先設定の保全を確認する。

結果は変更理由・実測した検証・残件を簡潔に報告する。文書保守だけの承認工程や変更ごとの報告書は追加しない。モデル固有の設定は固定せず、観測した失敗と公式資料から指示を削減・修正する。文字数削減をモデル品質の向上と断言しない。

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
