---
name: authorize-autonomous-execution
description: Record explicit human authorization only for regulated work or when external writes, production operations, deletion, publication, merge, high cost, or other difficult-to-reverse actions require a real authority boundary. Do not require initial authorization for ordinary direct or assured code changes.
---

# Authorize Autonomous Execution

人の承認は、実装方法ではなくauthority boundaryへ結び付ける。

## 承認が必要な場合

- regulated profile
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
4. regulatedの場合は既存のapproval chainへ記録する。
5. 通常の外部操作だけの場合はPR、Issue、または外部サービスの承認記録を正本とする。
6. 承認後は境界内の設計、実装、test、CI修正を追加承認なしで進める。

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
- 承認不要な通常変更を停止させない。
- 承認をgate failureの例外処理として使わない。

## Completion

- 承認triggerとauthority boundaryが明確である。
- 必要な場合だけ実在する人の判断がある。
- 可逆な実装判断が不必要に凍結されていない。
- Commit Commentへ外部副作用と残存リスクが記録される。
