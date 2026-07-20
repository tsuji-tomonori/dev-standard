---
name: govern-development-request
description: Run the full work-item, authorization, hash-chain, phase-gate, release, and audit lifecycle only for regulated changes: authentication, authorization, confidential or personal data, data loss, irreversible production operations, legal or contractual controls, high-cost external actions, or an explicitly requested high-assurance workflow. Do not use for ordinary direct or assured repository changes.
---

# Govern Development Request

このSkillは`regulated` profile専用である。

通常のfeature、fix、refactor、文書変更、局所UI変更には使用しない。これらは`$chat-first-development`のdirectまたはassured workflowで処理する。

## 起動条件

次のいずれかに該当する場合だけ使用する。

- authenticationまたはauthorization
- permissions、tenant isolation
- confidential情報、PII
- data lossの可能性
- irreversible production operation
- 法令、契約、監査上の工程統制
- 高額な外部操作
- 利用者が明示的にfull governed lifecycleを指定

## Regulated outputs

- `work/<id>/`のregulated実行記録
- 完全なexecution profile
- authority boundary
- 一度だけの明示承認
- hash chained approval / event log
- selected regulated checklist result
- release / audit evidence

製品要求の正本は引き続き`spec/requirements/requirements.json`とし、work itemを製品正本にしない。

## Workflow

1. regulated起動条件と、軽量profileでは不十分な理由を記録する。
2. `$right-size-execution`でregulated profile、scope、verification、reviewを確定する。
3. work itemを作成し、要求、要件差分、authority boundary、不可逆操作、rollback、停止条件を記録する。
4. `$author-lifecycle-docs`でregulated案件に必要な文書だけを作成する。
5. `$authorize-autonomous-execution`で一度だけ明示承認を取得する。
6. 承認範囲内で設計、実装、検証、PR、CI修正を自律実行する。
7. selected regulated checkを`tools/devflow.py`で検査する。
8. external CIとdeployment serviceの結果を参照し、生ログをGitへ複製しない。
9. Commit Commentへ要件影響、設計影響、review path、検証契約、残存リスクを統合する。
10. release、audit、closureを行う。

## Boundaries

- direct / assuredへこのworkflowを自動適用しない。
- 手順、tool、trace pathの可逆な変更だけで再承認を求めない。
- 結果、authority、外部副作用、不可逆性が承認境界を越える場合だけ停止する。
- gateを通すためにcheck、test、型、security controlを弱めない。
- raw production evidence、secret、PII、CIログをGitへ保存しない。

## Completion

- regulated起動根拠がある。
- authority boundaryと承認が現行である。
- regulated blocking checkがPassする。
- external CIが現在HEADを対象として成功する。
- Commit Commentとreview resultに最終証跡が残る。
- work itemは規制・監査上必要な期間だけ保持される。
