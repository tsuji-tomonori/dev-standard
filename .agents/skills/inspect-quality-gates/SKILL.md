---
name: inspect-quality-gates
description: Select and run only the checks relevant to the current change, using local evidence or an existing project check without creating CI, merge rules, or review bureaucracy.
---

# Inspect Quality Gates

## Formal specification

`spec/skills/skills.qnt` の `skillContracts` にある `name: "inspect-quality-gates"` を形式契約とする。

形式契約の`applicability`と`activationContexts`に該当しない場合は起動せず、artifactやblocking判定を作らないno-opとする。

変更と受入条件に関係する検査だけを選び、結果を直接確認する。これは3本目のガードレールであり、別の統制層を追加しない。

## Inputs

- 変更差分と受入条件
- 対象repositoryが既に持つtest、lint、type check、build、generator
- 必要な場合だけ、既存のCI結果または人による確認結果

## Workflow

1. 変更した挙動、path、riskから、失敗を検出できる最小の検査を選ぶ。
2. 未選択の検査をN/Aとして列挙しない。
3. まず対象範囲のローカル検査を実行し、必要な場合だけ範囲を広げる。
4. blockingとするのは、受入条件、生成物の整合、機密情報、権限境界など、その変更に直接関係する失敗だけとする。
5. 既存CIがある場合は追加証拠として参照できる。CIがないこと自体を失敗にしない。
6. 結果は会話、既存のPR欄、または対象repositoryが既に採用するartifactへ簡潔に記録する。専用review YAMLを要求しない。

このSkillは検査と判定だけを行い、失敗を隠すためのsource、test、設定変更は行わない。失敗時は、該当check、直接証拠、影響範囲、最小の修正handoffを返し、別途権限を持つ実装Skillによる修正後に再実行する。選択したcommand自身が一時fileやbuild artifactを作る場合は、その対象repository内の通常の実行効果として明示する。

複数commandを機械実行する場合だけ、対象repositoryが既に所有するcommand registryとrepository-confined planを渡し、`python <host-skill-path>/scripts/inspect.py --root . --registry <target-owned-checks.json> --plan <selected-checks.json>`を使う。`<host-skill-path>`はinstaller receiptとhost adapterが配置した、このSkillのhost-native rootへ解決する。registryがない導入先へ新しいregistryを要求せず、関連checkを通常の対象repository手順で実行する。

registry entryは`command_id`、shell文字列ではない`command` argv、許可する`acceptance_ids` / `risk_tags`、宣言`effect`、`authority` / `authority_reference`、`output_roots`だけを持つ。effectは`read-only`、`repository-build-artifacts`、`target-declared-external`のいずれかとする。read-onlyはoutput rootなし、build artifactは一つ以上のrepository-relative output rootを宣言する。external effectは現在の明示authority referenceがなければ実行前に拒否する。

planはtop-levelにbounded `scope`、`residual_risks`、`no_applicable_reason`と選択済み`checks`だけを持つ。各checkは`command_id`、関連する`acceptance_ids` / `risk_tags`、任意のbounded `timeout_seconds`を持ち、argv、cwd、envを上書きしない。該当checkがなければ`checks: []`と具体的な`no_applicable_reason`を返すno-opとし、checkがある場合は理由をnullにする。

runnerは`.git`、`.devflow/run`、宣言済みoutput root以外の全tree digestを実行前後で比較し、source、config、ignored fileを含む予期しないmutationを拒否する。registryとplanのsnapshotは全command後にも再検証し、`--json-out`のCAS read preconditionへも結合する。commandが除外領域内のregistry / planを変更してもresultを発行しない。primary executableは固定system pathへ解決してFD pinし、実行前後のidentity hashを照合する。開始不能時は`cannot-start`とし、実行していないcommandにeffectやdriftがなかったとは主張しない。

stdoutへraw outputを含まないbounded JSONを返し、明示した`--json-out`以外へsummaryを書かない。runner自身はGitHub APIや外部serviceを呼ばないが、任意のtarget commandが持つprocess外effectを隔離も完全検知もできない。このためeffect宣言がlocalであっても全commandへ`process-effect-not-isolated:<command_id>` residualを付ける。global resultは`process_effect_isolation_provided: false`と`process_effect_detection_provided: false`、各command resultは`process_effect_isolated: false`と`process_effect_detection: "not-provided"`を返し、宣言effect、authority、acceptance / riskとの関連、未検証範囲を伝播する。tree差分から判定できるのはrepository mutationであり、process外effectを検知したとは表現しない。

## Boundary

このSkillは次を作成、変更、要求しない。

- CI workflow、required check、status check
- branch protection、ruleset、merge方式、merge先
- PR template、変更ごとのreview YAML、test report、生ログ
- 3本柱以外のportable blocking gate

対象repositoryが既に持つ規則は尊重するが、それをportable契約として複製しない。

## Completion

- 変更と受入条件に対応する検査が選ばれている。
- 非該当の場合は具体的なno-op理由があり、blocking failureを作っていない。
- 選んだblocking検査がPassする。
- 未検証範囲または残存riskがあれば明示されている。
- 証拠は実行範囲を超えて主張していない。
- CIやmerge設定を新たに要求していない。
- target commandの宣言effectとauthorityを報告し、全commandについてprocess isolationやexternal-effect不在を過大主張していない。

<!-- BEGIN GENERATED QUINT CONTRACT -->
## Quint contract（自動生成）

このblockは`spec/skills/skills.qnt`から生成するviewです。直接編集しません。

- Skill: `inspect-quality-gates`
- 役割: selected-checks
- 柱: checks
- guardrail: yes
- repository blocking: yes
- 既定portable: yes
- 適用条件: when-change-relevant-checks-exist
- 起動context: `selected-checks`
- 外部作用capability: yes
- repository policy `ciWorkflow`: false
- repository policy `requiredCheck`: false
- repository policy `branchProtection`: false
- repository policy `ruleset`: false
- repository policy `mergeStrategy`: false
- repository policy `prTemplate`: false
- repository policy `commitFormat`: false
- 前提: changed artifacts, applicable risks, target-owned checks, declared command effects, and any required external authority are known
- 事後条件: selected blockers pass or a bounded failure is reported with declared command effects and a process-effect-not-isolated residual for every command, without claiming unselected coverage or isolation
- Authority: target-repository-and-selected-checks
- 副作用: target-command-effects
- 失敗状態: report-bounded
- 入力: `change`, `acceptance`, `target-owned-checks`, `optional-target-owned-command-registry`, `declared-command-effects`, `external-authority-if-applicable`
- 出力: `selected-check-results`, `declared-effect-report`, `residual-risk`, `repair-handoff`
- 義務: `select-minimum-relevant-checks`, `validate-registry-command-and-declared-effect-when-runner-is-used`, `execute-selected-checks`, `report-process-effect-isolation-uncertainty-for-every-command`, `bound-verdict-to-observed-evidence`
- 禁止事項: `do not modify source to hide failures`, `do not claim external-effect absence process isolation or unselected coverage`, `do not execute a declared external effect without explicit authority`, `do not create CI or merge policy`
- 依存Skill: なし
- 必須asset: `references/gate-rules.md`, `scripts/inspect.py`
- 要件trace: `REQ-ASBUILT-019`, `REQ-QUALITY-002`
- manual digest: `c1c6fe623b543c243f7661cba7d384dda773d9ace416d380e1e248fe039857f8`
- payload digest: `c8b9782e79e3b5e8cc46c4f4459e06b8fe19854f2365ed8fe73f07562d82a4ab`
- interface digest: `dd6b82dde5da4e1f6860fa7cb229cdaec7009d68b9b998d277844b174692994c`
<!-- END GENERATED QUINT CONTRACT -->
