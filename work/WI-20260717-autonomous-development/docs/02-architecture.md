# アーキテクチャ

## 目的

初回のrequirements authorizationを唯一の人による工程判断とし、後続工程では決定論的な品質ゲートだけを使って`closed`まで進行する。

## 構成

| 構成要素 | 責務 | 信頼境界 |
|---|---|---|
| `governance/policy.json` | workflow schema、工程順、初回承認工程・役割、必須文書を宣言 | policy変更自体は承認済みwork itemでのみ行う |
| `tools/devflow.py` | work item生成、digest、承認記録、チェック、進行、監査を決定論的に実行 | 自然言語エージェントの自己申告を信用しない |
| `work/<ID>` | 要件、計画、派生成果物、チェック、証跡、イベントを保持 | 初回承認後のrequirements成果物は凍結 |
| `.agents/skills` | AIの作業手順、傾聴、文書作成、検査、振り返りを指示 | 合否や承認の正本にはしない |
| `.codex/hooks` | 開始時の状態注入と終了時の振り返り候補生成 | 恒久ルールを自動適用しない |
| Git/GitHub | 差分、CI、PR、mergeを追跡 | feature branchと保護ルールを境界にする |

## 状態遷移

1. `init`はworkflow schema 2のwork itemと全テンプレートを生成する。
2. intakeは要求原文の内容検査だけで進行する。
3. requirementsは要件、初期トレーサビリティ、実行計画、97件のrequirements checklistを検査する。
4. `authorize`はrequirements digestへrequesterの明示判断を一件記録する。
5. architecture以降の`advance`は、全先行工程を現在の成果物で再計算してから現工程を検査する。
6. requirements成果物またはrequirements checklistが変わるとdigestが変わり、承認レコードが一致しなくなる。
7. retrospective gate成功後に`closed`へ進む。

## 初回承認モデル

- policy上のauthorizationは`requirements/requester`だけである。
- requirements以外の`required_approvals`は空配列である。
- 承認レコードは既存のhash chain付き`approvals.jsonl`を利用し、イベント名を`initial-authorization-recorded`とする。
- `approve`は互換aliasとして残すが、schema 2ではrequirements/requester以外を拒否する。
- 旧work itemは`workflow_schema_version`がないため、`status`、`advance`、`audit`で停止する。`migrate`はschemaだけを更新し、旧承認を再利用しない。

## 自走と停止

エージェントは承認済み計画内の設計選択、実装、文書、レビュー修正、テスト修正、CI修正を自律継続する。計画外の課金、本番変更、秘密情報公開、データ削除、第三者連絡、権限不足によるmergeだけを停止条件とする。

## skill構成

- `authorize-autonomous-execution`: 一件の明示承認を完全な権限境界へ結び付ける。
- `govern-development-request`: 初回承認後に全工程を自走する。
- `author-lifecycle-docs`: 承認前に実行計画を完全化し、承認後は派生文書を更新する。
- `inspect-quality-gates`: 初回承認と全先行工程を検査する。
- `calibrated-collaborative-listening`: 事実・意図仮説・不明点を分離し、結果を変える曖昧さだけ確認する。
- `retrospect-and-improve`: 改善候補を生成するが自動適用せず、計画外変更を次work itemへ分離する。

## 品質属性

- 正確性: unittestでdigest、移行、先行ゲート、Failのblockingを検証する。
- 監査性: approvals/eventsのhash chainと全先行ゲートをauditする。
- 保守性: policyを宣言源とし、authorization判定をhelperへ集約する。
- 安全性: 人の初回承認を推測せず、権限境界外の操作を実行しない。
- 可搬性: Python標準ライブラリ中心のCLIとして既存実行環境を維持する。

## 代替案

各工程の人承認を残す案は対話負荷が高く、ユーザー目的に反する。全ゲートを自動化する案は品質保証を弱める。採用案は、人の判断を一回の完全な権限境界へ集約し、機械検査を全工程で維持する。
