# テスト結果

## 対象版

research-grounded adversarial validation branch local revision。

## 結果概要

| 種別 | 実行数 | Pass | Fail | Skip | 証跡 |
|---|---:|---:|---:|---:|---|
| Unit/contract | 28 | 28 | 0 | 0 | unittest discover |
| Repository validator | 1 | 1 | 0 | 0 | validate_repo |
| Skill validation | 1 | 1 | 0 | 0 | quick_validate |
| Compile/diff | 2 | 2 | 0 | 0 | compileall/diff check |
| Catalog/audit | 2 | 2 | 0 | 0 | make verify |

## 要求カバレッジ

ADV-001〜008、ADV-N1〜N4をresearch/source assertions、skill contract、catalog set equality、full regressionでcover。

## 未解決欠陥

自己敵対的検証で配布profile依存漏れを1件検出し、修正・regression test済み。open defectなし。

## 非機能・障害試験

unsafe boundary、single judge禁止、no-proof wording、benign utility、holdout/adaptive retestをstatic contractで確認した。

## 完了判定

local completion criteriaを満たす。remote PR/CIをrelease gateで確認する。
