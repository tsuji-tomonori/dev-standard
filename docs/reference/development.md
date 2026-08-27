# 軽量な開発契約

利用者が得る結果を、対象repositoryの既存運用を維持したまま届けます。portableなガードレールは、要件、実装由来設計、関係する検査の3本だけです。

## Flow

1. 依頼、制約、受入条件を読み、結果を変える曖昧さだけを確認する。
2. durableな義務が変わる場合だけQuint要件正本を更新する。
3. 既存stackと規約に従って最小範囲を実装する。
4. 対象artifactに応じてas-built設計を生成する。
5. 変更に関係する決定的な検証だけを実行する。
6. 結果、検証範囲、残存riskを簡潔に報告する。

## Authority

| 情報 | Authority |
|---|---|
| durableな要件 | `spec/requirements/requirements.qnt` |
| 機械可読な要件view | 生成された`spec/requirements/requirements.json` |
| 人向け要件view | JSONから生成された`docs/requirements/REQUIREMENTS.md` |
| 実装済み構造 | 実装と`docs/design/generated/` |
| Skill契約 | `spec/skills/skills.qnt` |
| 長期判断の理由 | 必要な場合だけADR |

変更ごとの計画、implementation log、review YAML、test report、生ログを通常の成果物にしません。一時状態が本当に必要な場合だけ`.devflow/run/`を使います。

## Repository policy

branch、merge、PR、commit、CI/CDは対象repositoryのauthorityです。dev-standardはそれらを追加、変更、必須化しません。既存CIは利用できますが、CIがないこと自体を失敗とせず、ローカルの決定的検査を証拠として扱います。

外部書込み、削除、公開、merge、production、高額操作は明示された権限境界内だけで実行します。必要な能力とriskに応じて検査範囲を選び、成功後は無目的に工程を増やしません。
