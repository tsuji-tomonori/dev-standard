---
name: authorize-autonomous-execution
description: Record explicit authorization only for a concrete duty or real authority boundary such as external writes, production, deletion, publication, merge, or high cost. Do not authorize ordinary reversible code changes.
---

# Authorize Autonomous Execution

形式契約: `spec/skills/skills.qnt`の`name: "authorize-autonomous-execution"`（保守・監査時に参照）。

外部書込み、公開・送信、merge、production、削除、高額操作、または具体的な法令・契約・監査上の承認義務について、依頼された結果と権限境界を確認する。通常の可逆なcode・文書変更や検査を承認待ちにしない。

## 判断

1. 対象、結果、外部副作用、不可逆性、cost、rollback、停止条件を、現在の明示依頼・承認と照合する。
2. 有効な承認が同じ境界を覆う場合はそのまま進める。会話の前のturnにある承認も、撤回・失効・対象変更がなければ有効である。
3. 不足する承認がある場合だけ、独立した準備を終えてから具体的な操作と不足根拠を提示し、権限を持つ利用者の判断を得る。
4. 結果・要件の意味・authority・外部作用・production対象・cost等が承認範囲を越える場合だけ再承認する。内部設計、file名、tool、test方法の変更では取り直さない。

沈黙、別案件の一般的許可、AIの推測を承認にせず、人に代わってapproveしない。承認をtest failureや実行環境の制限を回避する手段にしない。

## 証拠

通常の外部操作では、既存のPR・外部serviceの承認記録、または現在の会話にある明示依頼・承認を使用する。work itemや証拠fileを作るためだけに停止しない。

具体的なregulated dutyがある場合だけ[authorization-boundary.md](references/authorization-boundary.md)を読む。regulated runnerは、承認主体または対象組織が事前に所有するexact-schemaのauthority evidenceを変更せず結合する。agentやrunnerが証拠を自己発行・補完・書換えしたり、会話を証拠fileへ自己転記したりしない。

完了時は承認範囲と実際の操作を対応付ける。CI workflow、required check、branch protection、merge ruleを新しく要求しない。

<!-- BEGIN GENERATED QUINT CONTRACT -->
## Quint contract（自動生成）

このblockは`spec/skills/skills.qnt`から自動生成し、直接編集しません。
詳細・要件trace・digestは`spec/skills/skills.json`の同名契約を、契約の保守・監査時だけ参照します。
repository policyは導入先が所有します。非該当ならartifactやblocking判定を作りません。

- Skill: `authorize-autonomous-execution`
- 柱: auxiliary
- repository blocking: no
- 既定portable: no
- 適用条件: when-external-authority-boundary-exists
- 起動context: `external-authority-boundary`, `concrete-regulated-duty`
- 外部作用capability: no
- Authority: explicit-user-authorization
- 副作用: none
- 失敗状態: stop-at-authority-boundary
<!-- END GENERATED QUINT CONTRACT -->
