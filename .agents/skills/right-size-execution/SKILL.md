---
name: right-size-execution
description: Select the smallest sufficient context, verification, review, and compute for a change, expanding only when evidence shows that another axis is needed.
---

# Right-size Execution

## Formal specification

`spec/skills/skills.qnt` の `skillContracts` にある `name: "right-size-execution"` を形式契約とする。

成功条件と重大riskを満たす最小十分な経路を選ぶ。通常は内部判断に留め、専用artifactを要求しない。

## Profiles

- `direct`: 局所的、可逆、外部副作用なし
- `assured`: 複数module、公開contract、DB、IaC、dependency、共有UI、永続要件またはgeneratorへの影響
- `regulated`: security、sensitive data、data loss、不可逆production操作、法令・契約、高額操作、または利用者の明示指定

## Workflow

1. 変更成果物、risk、authority boundaryから最小profileを選ぶ。
2. 要件影響、設計影響、必要な検査を仮判定する。
3. 最小のcontext、tool、verificationで開始する。
4. 検査失敗、新しい依存、契約影響、証拠不足が判明した軸だけを拡張する。一回の判断では一軸だけを拡張する。
5. 成功条件を満たしたら無目的な追加探索を止める。

`direct`と`assured`では恒久的な計画、status log、review YAMLを作らない。再開用状態が必要な場合だけ`.devflow/run/`へ一時保存する。`regulated` artifactは具体的な法令・契約・監査上の必要がある場合だけ使う。

## Boundary

- CI、PR、branch、merge方式、commit形式の導入をprofile選択の結果にしない。
- 既存CIは利用できるが、CIがないことを不足としない。
- 全checkをN/A付きで列挙しない。
- 外部書込み、削除、公開、merge、production、高額操作は明示権限の範囲だけ実行する。

## Completion

- profileと検査範囲が実際のriskに対応する。
- blockingな失敗が残っていない。
- 必要なauthority boundaryと残存riskが明確である。
- 成功後の無目的な追加作業がない。
