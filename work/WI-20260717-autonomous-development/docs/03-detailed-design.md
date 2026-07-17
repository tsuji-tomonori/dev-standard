# 詳細設計

- 版: 1.0
- 記録日: 2026-07-17
- 対象読者: Python実装者、repo-local skill保守者、reviewer、監査担当
- 対象: policy schema 2、devflow CLI、hooks、validator、統制skill、傾聴skill
- 対象外: Web/API、DB、UI、クラウド資源、AIモデル・学習・推論基盤
- 参照: `docs/01-requirements.md`、`docs/01-execution-plan.md`、`docs/02-architecture.md`、`docs/02-decisions.md`

## policy schema 2

`governance/policy.json`へ`authorization`を追加する。値は`phase=requirements`、`role=requester`とする。requirementsの必須文書はrequirements、traceability、execution-planの3件とし、他工程の`required_approvals`は空配列にする。

## state

新規work itemの`state.json`へ`workflow_schema_version`を保存する。現在policyと一致しないstateは、`status`、`advance`、`audit`でエラーにする。`migrate`だけが旧stateをschema 2へ更新できる。migration eventは移行前後のschemaと`prior_authorizations_reused=false`を記録する。

## helper設計

| 関数 | 入力 | 出力・例外 | 責務 |
|---|---|---|---|
| `require_current_workflow` | state | schema不一致で`GovernanceError` | 旧itemの暗黙利用を防ぐ |
| `authorization_definition` | policy | phaseとrole | 単一承認設定を検証する |
| `preceding_phase_reports` | work/state/results/phase | 先行gate report配列 | 現在ファイルで過去工程を再検査する |
| `cmd_migrate` | work item/actor | state更新とevent | 明示移行し旧承認を再利用しない |
| `cmd_approve` | decision/approver/comment | hash chain record | requirements/requesterだけを記録する |
| `cmd_advance` | work item/actor | 次phase | 全先行gate、現gateの順に検査する |
| `cmd_audit` | repository | failure一覧 | chain、schema、全先行gateを監査する |

## authorize CLI

`authorize`は`cmd_approve`を呼び出す正規commandとする。roleとphaseはpolicyから取得し、利用者入力を不要にする。`approve`は互換aliasとして残すが、schema 2では別phase/roleを拒否する。

承認recordは次を持つ。

- timestamp
- work_item
- phase=`requirements`
- gate_digest
- decision
- approver
- role=`requester`
- comment
- prev_hash / record_hash

## gate進行

`cmd_advance`は次の順で処理する。

1. workflow schema検査
2. current phaseより前の全phaseを`include_approvals=true`で再計算
3. 最初の失敗reportを書き出して停止
4. current gateを再計算
5. 成功時だけstateを次phaseへ原子的に更新
6. phase-advanced eventを追記

requirements gateだけが初回承認を要求するため、architecture以降の再検査でauthorizationの有効性も確認できる。

## Fail処理

schema 2では`verdict=fail`を常に`CHECK_FAIL_BLOCKING`にする。Issue IDは原因追跡用に要求するが、exception recordが存在してもgateを通さない。`cmd_set_check`は新しいhuman exceptionの登録を拒否する。

## retrospective

Stop hookはreportとpending improvement proposalだけを生成する。`improvement-approve`と`improvement-apply`をCLIから削除し、skillへの自動追記を廃止する。計画外改善は次work itemのrequirementsへ移す。

## skill詳細

`calibrated-collaborative-listening`はprogressive disclosureを使う。

- `SKILL.md`: trigger、visible loop、核心化、確認判断、非迎合、圧縮、tone boundary、完了条件
- `semantic-articulation-protocol.md`: atomic ledgerからsemantic checksumまでの内部手順
- `japanese-response-patterns.md`: 自然な校正、差分指摘、事実訂正、短文化例
- `evaluation-rubric.md`: 14次元、critical failure、14ケース、合格閾値
- `evidence-map.md`: 公開研究への対応

## validator

repo validatorは、期待skill一覧に新しい二skillを含める。policyのauthorizationがrequirements/requesterであること、他phaseに承認がないこと、execution-plan templateがrequirementsへ束縛されることを検査する。

## エラーと原子性

JSON stateは既存`atomic_write_json`を利用する。events/approvalsはappend-only hash chainを維持する。schema、policy、必須plan、承認roleの不整合は具体的な`GovernanceError`で停止し、部分的にphaseを進めない。
