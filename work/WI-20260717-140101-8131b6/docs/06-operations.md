# 運用設計・運用引継ぎ

## SLO・SLI・エラーバジェット

静的referenceのため非該当。

## 監視・ログ・アラート

CIのcatalog、tests、validator、auditを監視点とする。

## Runbook・インシデント対応

CI失敗時は該当assertionとrename漏れを確認し、直前commitをrevert可能。

## バックアップ・復旧・DR

永続データなし。Git履歴が復旧手段。

## 容量・コスト・依存先

追加runtime費用・依存先なし。
