# 振り返り・改善

## 成果と計画差

software testingとAI red teamingを一つのfalsification workflowへ統合し、source-to-rule traceとSkills catalogを追加した。

## 有効だった統制

primary source優先、independent oracle、finite-budget wording、safe boundary、inventory set testが有効。

## 手戻り・ゲート失敗・見逃し

検索queryの一般語ではsoftware primary sourcesが十分出ず、technique別にqueryを分割した。また、GitHub連携で大容量JSONが切り詰められ、初回remote auditが失敗した。実装・テスト自体の手戻りはなし。

## 根本原因

adversarial validationの対象範囲がsoftware/AI両方に跨るため、単一queryでは検索rankingがAMLへ偏った。大容量JSONの失敗は、標準出力を介した転送上限を事前検査していなかったことが原因。

## 改善提案

| 対象skill/ルール | 変更案 | 根拠 | リスク | 承認状態 |
|---|---|---|---|---|
| research retrieval | domain別query setをreference保守手順へ追加 | initial search偏り | source selection固定化 | future proposal、未承認 |

## 次回確認方法

sourceリンク、required rule assertions、catalog equality、quick validation、PR CIを次回更新でも実行する。
