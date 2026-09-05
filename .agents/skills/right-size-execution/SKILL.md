---
name: right-size-execution
description: Select the smallest sufficient context, verification, review, and compute for a change, expanding only when evidence shows that another axis is needed.
---

# Right-size Execution

## Formal specification

`spec/skills/skills.qnt` の `skillContracts` にある `name: "right-size-execution"` を形式契約とする。

形式契約の`applicability`と`activationContexts`に該当しない場合は起動せず、artifactやblocking判定を作らないno-opとする。

成功条件と重大riskを満たす最小十分な経路を選ぶ。通常は会話内の短い判断に留め、専用artifact、telemetry、benchmark、calibration、audit台帳を作らない。

## Inputs and outputs

- 入力: 依頼、既知path、成果物tag、risk tag、受入条件、利用可能な証拠、対象repositoryが既に選んだgate
- 出力: `scope`、`assurance`、`compute`、`mode`の根拠付き選択と、選択された検証集合
- 任意出力: 明示的に計測または再開が必要な場合だけ、診断、実績、展開chain、停止digest

四軸を一つの段階へ畳み込まない。局所的だが重大な変更は`local + critical`、広範囲だが機械的な変更は`repository + standard`になり得る。値と決定特徴は[execution-dimensions.md](references/execution-dimensions.md)を参照する。

## Workflow

1. 通常ルートの依頼情報と決定的metadataから四軸を独立に推定する。結果を変える不明点だけmetadata probeを最大一回使う。
2. assurance下限はrisk tagと成果物tagの和集合から導出する。重大riskだけを理由にscopeを広げない。
3. confidenceは観測特徴による`low / medium / high`と根拠を記録し、校正済みrouterがない間はscoreを`null`にする。
4. blocking検証は、scope、assurance、成果物、risk、受入条件、対象repositoryが明示したgateの決定的な和集合と完全一致させる。追加探索は別の任意diagnosticとして扱う。
5. 初期判断を覆す新証拠がある場合だけ、一回の判断につき一軸を拡張する。同一のstable failure identityが戻った場合は回数ではなくstagnationとして止める。
6. 拡張は直前eventのdigestを含むchainにする。成功時は選択検証、assurance、selection、全拡張chainを結ぶ停止digestを作る。
7. stateまたは出力を明示的に保存するときは、観測したbyte digestを使うatomic compare-and-swapで競合を拒否する。
8. 成功条件と選択検証を満たしたら、確定処理以外の正のコスト活動を止める。

一時状態は再開が必要な場合だけ`.devflow/run/`へ置く。計測機能を明示的に使う場合のfield定義は[measurement-contract.md](references/measurement-contract.md)に限定し、通常依頼の前提にしない。

## Boundary

- CI、PR、branch、merge方式、commit形式の導入をprofile選択の結果にしない。
- 対象repositoryが既に選んだ検査は利用できるが、特定のhost、CI、branch保護、merge ruleがないことを不足としない。
- 全checkをN/A付きで列挙しない。
- shadow、schema、assurance、効率の診断はこの補助Skill自身を第四のrepository blockerにせず、`repository_blocking=false`で報告する。
- 外部書込み、削除、公開、merge、production、高額操作は明示権限の範囲だけ実行する。

## Completion

- 四軸と完全一致する検証projectionが実際のriskと成果物に対応する。
- 選択された検証に未解決の失敗が残っていないか、有界な失敗として報告される。
- 必要なauthority boundaryと残存riskが明確である。
- 成功後の無目的な追加作業がない。

<!-- BEGIN GENERATED QUINT CONTRACT -->
## Quint contract（自動生成）

このblockは`spec/skills/skills.qnt`から生成するviewです。直接編集しません。

- Skill: `right-size-execution`
- 役割: execution-sizing
- 柱: auxiliary
- guardrail: no
- repository blocking: no
- 既定portable: no
- 適用条件: when-execution-sizing-is-needed
- 起動context: `execution-sizing`
- 外部作用capability: no
- repository policy `ciWorkflow`: false
- repository policy `requiredCheck`: false
- repository policy `branchProtection`: false
- repository policy `ruleset`: false
- repository policy `mergeStrategy`: false
- repository policy `prTemplate`: false
- repository policy `commitFormat`: false
- 前提: execution context can provide sizing, adjustment, verification observation, and stopping evidence
- 事後条件: the selected or adjusted minimum profile has an exact verification projection, bounded diagnostics, and tamper-evident stopping evidence
- Authority: change-risk
- 副作用: repository-confined-temporary-write
- 失敗状態: report-bounded
- 入力: `execution-context`, `change-risk`, `artifacts`, `acceptance`, `target-owned-gates`, `available-evidence`
- 出力: `execution-profile`, `selected-verification`, `optional-diagnostics`, `stopping-evidence`
- 義務: `assess-independent-execution-axes`, `derive-exact-verification-projection`, `expand-one-evidence-backed-axis`, `stop-after-decisive-success`, `preserve-tamper-evident-state`
- 禁止事項: `do not infer repository policy from execution sizing`, `do not fabricate evidence or bypass a risk floor`, `do not continue unbounded exploration after success`
- 依存Skill: なし
- 必須asset: `assets/behavior-constraints.json`, `assets/benchmark-cases.json`, `assets/execution-policy.json`, `assets/execution-policy.schema.json`, `assets/execution-profile.schema.json`, `references/execution-dimensions.md`, `references/expansion-contract.md`, `references/measurement-contract.md`, `references/stopping-contract.md`, `scripts/executionflow.py`
- 要件trace: `REQ-EXEC-001`, `REQ-EXEC-002`, `REQ-EXEC-003`, `REQ-EXEC-004`, `REQ-EXEC-005`, `REQ-EXEC-006`, `REQ-EXEC-007`, `REQ-EXEC-008`, `REQ-EXEC-009`, `REQ-EXEC-010`, `REQ-SKILL-001`, `REQ-SKILL-002`
- manual digest: `c69584254c09ea7fe305d81281217534ed45524f683d205b5eb9b32dd92ac409`
- payload digest: `bf7266038bd097f19a95bbaf4c8a9b08130b42980920f2c87e106fdf0c90e803`
- interface digest: `c06abbf5b7ca484f5e2e33335928375624c069cb6d4a7393cda10acc52451211`
<!-- END GENERATED QUINT CONTRACT -->
