---
name: right-size-execution
description: Choose and audit the smallest sufficient execution profile for repository work by estimating scope, assurance, compute, and execution mode independently; execute within soft budgets; expand one evidence-backed axis at a time; and stop after decisive success. Use before governed implementation, checklist selection, model or reviewer escalation, and execution-efficiency audits. Keep Estimate, Execute, and Expand in one state machine.
---

# Right-size Execution

成功条件と重大リスクを満たす最小十分な経路を選びます。要件管理、初回承認、個別チェックの合否、Git／PR／CI操作、技術規約は既存Skillへ委ねます。

## 入出力

- 入力: 開発要求、明示path、成果物・risk tag、依存metadata、受入条件
- 正本出力: `work/<id>/execution-profile.json`
- 派生出力: 実行計画要約、selector manifest、`reports/execution-efficiency.json`
- Policy／Schema: `assets/execution-policy.json`、`assets/execution-profile.schema.json`

## Workflow

1. `references/execution-dimensions.md`を必要なときだけ読み、通常のルート判断と決定的metadataから`scope`、`assurance`、`compute`、`mode`を独立に推定します。Estimate専用LLM呼出しは行いません。結果が変わる不明点だけmetadata probeを最大1回行い、結果を再利用します。
2. repository変更なら初回承認前に`execution-profile.json`を生成します。調査・回答だけなら永続profileは作りません。
3. required verificationとsoft budget内で実行します。検索はpath・line・短い断片から始め、同一digest・rangeを再読しません。
4. 新証拠が初期profileを覆した場合だけ`references/expansion-contract.md`に従い、一回につき一軸を拡張します。一律のExpand回数上限は設けません。
5. `references/stopping-contract.md`の成功条件を満たしたら確定処理以外を停止します。
6. 実績を確定し、selectorの選択漏れ監査とprofile auditを実行します。rolloutがshadowの間、効率判断は警告、assurance floor違反と不正schemaはblockingです。

## 効率規則

- チェックリスト全量をpromptへ入れず、selector版、入力特徴、選択・除外ID数、digest、除外監査sampleを保存します。
- `not-selected`と、実際に評価した`not-applicable`を混同しません。
- 成功ログは機械判定と要約だけ、失敗ログは因果的箇所だけを保持します。
- token telemetryがなければbyte、range、tool callを必須proxyにします。
- 強いmodelは情報不足を解決しません。`compute-insufficient`の証拠がある場合だけcomputeを引き上げます。

## 完了検査

- profile schemaとpolicy revisionが一致する
- 高リスクがscopeではなくassurance floorへ反映される
- confidence scoreは校正済みrouterがない限りnullである
- required verificationとassurance floorを満たす
- Expandが新証拠に基づく単軸変更である
- selector manifestと選択漏れ監査がある
- 成功後の正のコスト活動がない

詳細な計測は`references/measurement-contract.md`を参照します。ACRRは`C_min` oracleを持つbenchmark限定とし、論文の削減率を実運用目標へ転用しません。
