---
name: right-size-execution
description: Select the smallest sufficient context, verification, review, and compute for a change, expanding only when evidence shows that another axis is needed.
---

# Right-size Execution

形式契約: `spec/skills/skills.qnt`の`name: "right-size-execution"`（保守・監査時に参照）。

成功条件と重大riskを満たす最小十分な経路を選ぶ。通常は会話内の短い判断に留め、専用artifact、telemetry、benchmark、calibration、audit台帳を作らない。

## 通常の選択

変更範囲、risk、受入条件、既存の必須検査から最小十分な経路を選び、成功したら終える。新しい証拠で必要になった範囲だけ広げる。通常依頼では会話内の判断で足り、四軸の記録、probe回数、拡張chain、停止digestを要求しない。

実行profileの機械計測・診断を明示的に選んだ場合だけ[execution-dimensions.md](references/execution-dimensions.md)のrunner手順を使用する。その場合は四軸、検証projection、改ざん検知可能な状態、停止証拠の契約を満たす。

## Boundary

- CI、PR、branch、merge方式、commit形式の導入をprofile選択の結果にしない。
- 対象repositoryが既に選んだ検査は利用できるが、特定のhost、CI、branch保護、merge ruleがないことを不足としない。
- 全checkをN/A付きで列挙しない。
- shadow、schema、assurance、効率の診断はこの補助Skill自身を第四のrepository blockerにせず、`repository_blocking=false`で報告する。
- 外部書込み、削除、公開、merge、production、高額操作は明示権限の範囲だけ実行する。

## Completion

- 選択した検証が実際のriskと成果物に対応する。計測runner使用時は四軸のprojectionと一致する。
- 選択された検証に未解決の失敗が残っていないか、有界な失敗として報告される。
- 必要なauthority boundaryと残存riskが明確である。
- 成功後の無目的な追加作業がない。

<!-- BEGIN GENERATED QUINT CONTRACT -->
## Quint contract（自動生成）

このblockは`spec/skills/skills.qnt`から自動生成し、直接編集しません。
詳細・要件trace・digestは`spec/skills/skills.json`の同名契約を、契約の保守・監査時だけ参照します。
repository policyは導入先が所有します。非該当ならartifactやblocking判定を作りません。

- Skill: `right-size-execution`
- 柱: auxiliary
- repository blocking: no
- 既定portable: no
- 適用条件: when-execution-sizing-is-needed
- 起動context: `execution-sizing`
- 外部作用capability: no
- Authority: change-risk
- 副作用: repository-confined-temporary-write
- 失敗状態: report-bounded
<!-- END GENERATED QUINT CONTRACT -->
