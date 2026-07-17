# 運用設計・運用引継ぎ

## SLO・SLI・エラーバジェット

常時稼働serviceではない。操作成功率100%、unexpected overwrite 0を運用品質目標とする。

## 監視・ログ・アラート

CLI action/count、CI unit/validator/catalog/audit結果を観測する。失敗時は非zero exitと対象pathを出力する。

## Runbook・インシデント対応

まずdry-run、conflict内容とtarget diffを確認する。適用失敗時はwrite前preflightにより原則変更なし。適用後問題はtarget version controlでrevertする。

## バックアップ・復旧・DR

配布元はGit、導入先backupはtarget repositoryのversion controlに従う。外部stateやdatabaseはない。

## 容量・コスト・依存先

copy量はrepository asset sizeに比例し、外部API costはない。必要profileだけ選択して容量とcontext負荷を抑える。
