# 実装・構成管理記録

## 変更概要

`adversarial-validation`を`adversarial-review`へrenameし、security攻撃中心の内容を独立・反証的な欠陥探索レビューへ全面修正した。配布、一覧、chat-first、tests、validatorを同期した。

## 要求・設計との対応

| 変更 | 要求ID | 設計節 | コミット | レビュー |
|---|---|---|---|---|
| Skill/references rename and rewrite | REQ-001〜005 | detailed design | pending | contract tests |
| manifest/docs/tests update | REQ-006 | integration design | pending | install/repo tests |

## セキュア実装・依存関係

外部依存追加なし。security testingは対象外化。

## 設計との差異

なし。

## 実行したローカル検査

quick_validate成功。skill/install tests 17件成功。repository validator成功。旧名・security固有語彙のrg確認済み。
