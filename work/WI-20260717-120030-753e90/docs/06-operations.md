# 運用設計・運用引継ぎ

## SLO・SLI・エラーバジェット

request-to-PR completion、user-run command 0、unexpected global/config write 0をquality targetとする。

## 監視・ログ・アラート

work evidence、test results、Git status、PR/CI checksをAIが監視する。command出力はdiagnosticでありuser taskにしない。

## Runbook・インシデント対応

setup failureはlocal環境再作成、runtime不足はlightweight fallback、publication failureはlocal commit保全とexact permission blockerを使う。

## バックアップ・復旧・DR

sourceとwork evidenceはGitで復旧。external database/stateはない。PR前はlocal branch、PR後はrevertでrollbackする。

## 容量・コスト・依存先

bounded model、必要なreviewだけ、repository-local dependency cacheでcostを抑える。
