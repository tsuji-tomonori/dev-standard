---
name: right-size-execution
description: Select the smallest sufficient direct, assured, or regulated development profile and the necessary context, verification, review, and compute. Use before repository changes, checklist selection, reviewer escalation, and efficiency audits. Keep budgets soft, expand on evidence, and do not create permanent work artifacts for direct or assured changes.
---

# Right-size Execution

成功条件と重大リスクを満たす最小十分な経路を選ぶ。

## 出力

通常は内部判断として次を保持し、PR前にreview YAMLへ必要部分だけ確定する。

- `profile`: direct / assured / regulated
- 変更成果物とrisk tag
- selected check ID
- required verification
- authority boundary
- expansion理由

`direct`と`assured`では恒久的なexecution profileファイルを作らない。再開用状態が必要な場合だけ`.devflow/run/`へ保存し、完了後に削除する。

`regulated`では既存の`work/<id>/execution-profile.json`を使用できる。

## Profile selection

### direct

- 局所的
- 可逆
- 外部副作用なし
- critical riskなし
- 公開契約、DB、IaC、依存への重大影響なし

### assured

- 複数module
- 公開API・event
- DB・migration
- IaC・network
- dependency・lockfile
- 共有UI・重要flow
- 永続要件、generator、governance

### regulated

- security、authentication、authorization
- permissions、data loss
- confidential、PII
- irreversible production operation
- 法令・契約上の統制
- 高額外部操作
- 利用者が明示的に高保証工程を要求

高リスクはまずverificationとreviewを強める。影響範囲の証拠がない限り、repository全体へscopeを広げない。

## Workflow

1. 要求、changed path、repository metadataからprofileを選ぶ。
2. 要件影響、設計影響、authority impactを仮判定する。
3. `governance/checks/catalog.yaml`のtrigger、timing、classからcheck IDを選ぶ。
4. 最小のcontext、tool、verificationで開始する。
5. 検証失敗、新しい依存、契約影響、証拠不足が判明した場合だけ拡張する。
6. 複数軸が同じ新証拠から直接必要になった場合は、理由を一つ記録して同時拡張できる。
7. 成功条件を満たしたら、Commit Comment、review YAML、PR/CI確認以外の探索を停止する。
8. PR前に実際のprofile、selected check、残存リスクをreview YAMLへ確定する。

## Soft budget

context、tool call、search、reviewer、computeの予算は観測用のsoft limitとする。

- 固定上限をhard gateにしない。
- repository規模、monorepo、生成コード、間接依存を考慮する。
- 同一digestの無目的な反復は警告する。
- 変更後確認、再生成後確認、文脈回復のための再読は禁止しない。
- 情報不足を強いmodelだけで補おうとしない。

## Expansion

許可理由の例:

- verification-failed
- impact-surface-exceeded
- dependency-discovered
- contract-impact-discovered
- assurance-insufficient
- requirements-conflict
- evidence-insufficient
- compute-insufficient
- independent-review-required

原則として必要な軸だけを広げる。一律の回数上限は設けない。

## Check selection

- ID、class、timing、trigger、合格条件は`governance/checks/catalog.yaml`だけを正本とする。
- 全checklistをpromptへ入れない。
- `trigger`、changed path、risk、profileから選択する。
- 未選択をN/Aへ変換しない。
- `Invariant`はtrigger該当時に必須。
- `Risk-selected`は選択された場合だけblocking。
- `Advisory`は修正、Issue、残存リスクへ収束させる。

## Completion

- profileが実際の変更と一致する。
- 要件影響と設計影響がCommit Commentへ記録される。
- selected checkがreview YAMLへ記録される。
- required verificationがGitHub Actions等で実行される。
- blocking failが残っていない。
- 成功後の無目的な追加探索がない。
