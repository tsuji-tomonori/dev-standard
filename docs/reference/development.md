# 開発契約

## 目的

自然言語の依頼から、必要な要件、実装、検証、Commit Comment、PRまでを最小十分な手順で完了します。手順や文書を増やすことではなく、利用者が得る結果と検証可能な証拠を優先します。

## 実行profile

| profile | 適用条件 | 追加する検証 |
|---|---|---|
| `direct` | 局所的、可逆、外部副作用なし | 対象test、build、lint、type、生成物drift |
| `assured` | 公開契約、DB、IaC、dependency、共有UI、generator、要件、governance、distribution | 関連するRisk-selected checkと必要時の独立review |
| `regulated` | 認証・認可、PII、データ損失、不可逆production、法令・契約統制、高額操作 | 明示承認、work item、phase gate、hash chain、監査 |

公開API変更は通常`assured`で扱い、公開APIであることだけを承認理由にしません。

## 変更フロー

1. 依頼、リポジトリ指示、権限境界を確認する。
2. 要件・設計・公開契約・data・IaC・dependency・securityへの影響を判定し、profileとcheckを選ぶ。
3. 永続要件が変わる場合だけ正本を更新する。
4. 実装し、変更範囲の決定的な検証から開始する。
5. as-built対象では実装から設計を生成し、driftを検査する。
6. selected check結果、Commit Comment、PRを作成し、現在HEADの外部CIを確認する。

未選択checkをN/Aとして保存しません。失敗や新しい影響が見つかった場合だけ、検証範囲やreviewを拡張します。

## 正本と証拠

| 情報 | 正本 |
|---|---|
| 永続要件 | `spec/requirements/requirements.json` |
| 人向け要件 | `docs/requirements/REQUIREMENTS.md`（生成） |
| 実装由来設計 | `docs/design/generated/`（生成） |
| 長期判断の理由 | `docs/decisions/` |
| check定義 | `governance/checks/catalog.yaml` |
| 変更時点のreview判断 | `governance/reviews/<change-id>.yaml` |
| 変更概要と影響判定 | Git commit message |
| test・build・scan結果 | GitHub Actions等の外部サービス |
| 将来作業 | Issue |

変更ごとの計画、implementation log、test report、CI生ログを重複保存しません。一時実行状態が必要な場合だけ`.devflow/run/`を使用し、Git管理しません。

## 要件と設計

要件分類は[要件分類標準](../standards/REQUIREMENT-CLASSIFICATION.md)を正とします。外部挙動、業務ルール、受入条件、非機能制約、権限、恒久的なproject義務が変わる場合だけ要件正本を更新します。

具体的なtechnology、architecture、tool、path、process、工程、成果物が依頼に含まれるだけでは要件影響ありとしません。underlying outcome、quality threshold、exact choiceの必要性とauthority、lifetime、scopeを判定し、可逆な実装選択は実装、長期判断はADR、実装済み構造は生成設計、下位拘束は親判断へtraceしたderived requirementへ置きます。

コードや宣言から生成できる情報を手書き設計として複製しません。as-built生成・実装・test規約は[as-built設計標準](../standards/AS-BUILT-DESIGN.md)を参照し、コードだけでは理由が分からない長期判断だけをADRにします。

## Review結果

`governance/reviews/<change-id>.yaml`には選択されたcheckだけを保存します。

- `Invariant`: trigger該当時はPass必須
- `Risk-selected`: 選択された場合だけblocking
- `Advisory`: 修正、Issue、残存リスクへ収束
- `Periodic`: 個々のPRではなく定期監査

形式と検証方法は[`governance/reviews/README.md`](../../governance/reviews/README.md)を参照してください。

## 権限と安全性

外部書込み、削除、公開、merge、production、高額操作、不可逆操作は、依頼または明示承認で与えられた範囲だけ実行します。secrets、PII、production dump、会話transcript、外部CIの生ログをコミットしません。

モデル名は文書へ固定せず、taskに必要な能力、コスト、read-only境界、検証可能性から選びます。AIの自己申告だけをPass、承認、CI結果にしません。
