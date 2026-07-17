# リリース判定

## リリース対象

README、移植guide、manifest、installer、merge snippets、config cleanup、validator/tests、work evidenceをPR #1へ追加する。

## 受入条件の充足

localではPORT-001〜007、PORT-N1〜N4を全て満たした。remote branch更新後にPR mergeabilityとGitHub Actions successを最終確認する。

## 未解決Issue・例外承認

なし。remote CI結果待ち。

## デプロイ・ロールバック

GitHub connectorで既存PR branchへ追加commitする。問題時は追加commitをrevertでき、PR merge前なのでproduction deploymentはない。

## 利用者・運用者への通知

PR title/body/commentとREADME/INSTALLATION.mdでdirectory、profile、copy/merge手順を通知する。

## Go / No-Go判断

remote CI成功後にGo。現時点はlocal Go / remote pending。
