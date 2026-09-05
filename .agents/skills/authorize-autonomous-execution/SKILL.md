---
name: authorize-autonomous-execution
description: Record explicit authorization only for a concrete duty or real authority boundary such as external writes, production, deletion, publication, merge, or high cost. Do not authorize ordinary reversible code changes.
---

# Authorize Autonomous Execution

## Formal specification

`spec/skills/skills.qnt` の `skillContracts` にある `name: "authorize-autonomous-execution"` を形式契約とする。

形式契約の`applicability`と`activationContexts`に該当しない場合は起動せず、artifactやblocking判定を作らないno-opとする。

人の承認は、実装方法ではなくauthority boundaryへ結び付ける。

## 承認が必要な場合

- a concrete legal, contractual, safety, production, or audit duty that requires explicit approval
- production deployまたはproduction変更
- data deletionまたは不可逆migration
- 外部公開、通知、送信
- mergeを含むrepository外または共有状態の変更
- 高額な課金・resource作成
- secret、PII、権限境界を扱う操作
- 利用者が明示的に承認gateを要求

## 通常は承認不要

- 局所的で可逆なcode変更
- test追加・修正
- refactor
- 文書変更
- 生成設計の再生成
- lint、type、CI修正
- 承認済み結果を達成するための実装詳細変更
- trace path、test file名、使用tool、実装順序の変更

## 承認対象

- 達成する結果
- 永続要件の意味変更
- 許可する外部副作用
- 不可逆操作
- production対象
- cost boundary
- 明示的な禁止事項
- rollbackまたは停止条件

可逆な実装経路を承認digestへ固定しない。

## Workflow

1. 承認が必要なtriggerを具体的に示す。
2. 結果、要件差分、authority、外部副作用、不可逆性、rollback、停止条件を短く提示する。
3. 利用者から明示的なapprove / rejectを得る。
4. regulatedの場合は、承認主体または対象組織が事前作成したexact-schemaのtarget-owned authority evidenceを既存approval chainへ結合する。agentやrunnerが承認内容を作成、補完、書換えしない。
5. 通常の外部操作だけの場合はPR、Issue、または外部サービスの承認記録を正本とする。
6. 承認後は境界内の設計、実装、test、CI修正を追加承認なしで進める。

通常の外部操作にregulated work itemを要求しない。対象repositoryや外部serviceに既存の承認記録がない場合は、現在の会話にある明示依頼・承認と、実行直前に確認した対象・副作用・停止条件をauthority evidenceとする。ただしregulated runnerへ記録する場合、その会話をagentが証拠fileへ自己転記せず、承認主体または対象側が所有する事前存在fileを受け取る。

## 再承認条件

次が変わる場合だけ再承認する。

- 結果
- 永続要件の意味
- authority
- 外部副作用
- 不可逆性
- production対象
- cost boundary

内部設計、変更file、tool、reviewer、test方法、trace先の変更だけでは再承認しない。

## Boundaries

- silence、過去の一般的許可、AIの推測を承認にしない。
- 人に代わってapproveしない。
- agentまたはrunnerがauthority evidenceを自己発行・補完・書換えしない。
- 承認不要な通常変更を停止させない。
- 承認をgate failureの例外処理として使わない。
- 通常の外部操作を、work item作成のためだけに停止させない。

## Completion

- 承認triggerとauthority boundaryが明確である。
- 必要な場合だけ実在する人の判断がある。
- regulated recordでは事前存在するtarget-owned authority evidenceがresult、scope、effects、rollback、停止条件へ厳密に結合される。
- 可逆な実装判断が不必要に凍結されていない。
- 対象repositoryが採用する変更記録へ外部副作用と残存リスクが記録される。
- 承認を理由にCI workflow、required check、branch protection、merge ruleを追加または変更していない。

<!-- BEGIN GENERATED QUINT CONTRACT -->
## Quint contract（自動生成）

このblockは`spec/skills/skills.qnt`から生成するviewです。直接編集しません。

- Skill: `authorize-autonomous-execution`
- 役割: authority-boundary
- 柱: auxiliary
- guardrail: no
- repository blocking: no
- 既定portable: no
- 適用条件: when-external-authority-boundary-exists
- 起動context: `external-authority-boundary`, `concrete-regulated-duty`
- 外部作用capability: no
- repository policy `ciWorkflow`: false
- repository policy `requiredCheck`: false
- repository policy `branchProtection`: false
- repository policy `ruleset`: false
- repository policy `mergeStrategy`: false
- repository policy `prTemplate`: false
- repository policy `commitFormat`: false
- 前提: an external or irreversible authority boundary exists
- 事後条件: authorization scope and stop conditions are explicit and backed by current authority-owned evidence
- Authority: explicit-user-authorization
- 副作用: none
- 失敗状態: stop-at-authority-boundary
- 入力: `requested-result`, `external-effects`, `rollback`, `current-explicit-authority-evidence`
- 出力: `authorization-decision`, `authority-evidence-reference`
- 義務: `bind-approval-to-result-and-effects`, `record-stop-and-rollback-boundary`, `reuse-current-approval-within-boundary`, `reject-self-issued-authorization`
- 禁止事項: `do not infer approval from silence or history`, `do not self-mint or rewrite authority evidence`, `do not require a work item for ordinary external operations`, `do not freeze reversible implementation details`
- 依存Skill: なし
- 必須asset: `references/authorization-boundary.md`
- 要件trace: `REQ-PORTABLE-003`
- manual digest: `1bc98fd423c00945a2f617be9a66557de5a32798741b9ab959a5a0975a4cf4b0`
- payload digest: `c3fc07b73a6ca825409c8d13576b0e81faeb2f21062318ef8e9aa769ed98eabe`
- interface digest: `4c8aa415dd614335cecf8dbc4bc9fd924978275c4f1aac89f94f5ed66a948a46`
<!-- END GENERATED QUINT CONTRACT -->
