# セキュリティレビュー

変更はlocal text/configで、新しいnetwork tool、secret、dependency、production data、privileged actionを追加しない。review agentsはread-onlyをvalidatorで強制。authorization、安全境界、Pass evidence、N/A rationale、blocking Failはlean化後も明示され既存testが成功する。

Residual riskはlightweight reviewerのsemantic miss。named validation failure時だけeffort/root judgmentへ昇格し、cost最適化をgate bypassに使わない。
