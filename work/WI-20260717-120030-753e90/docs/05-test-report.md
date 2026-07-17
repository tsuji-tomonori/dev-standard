# テスト結果

## 対象版

chat-first implementation branch local revision。

## 結果概要

| 種別 | 実行数 | Pass | Fail | Skip | 証跡 |
|---|---:|---:|---:|---:|---|
| Python unit | 26 | 26 | 0 | 0 | unittest discover |
| Repository validator | 1 | 1 | 0 | 0 | validate_repo |
| Compile/diff | 2 | 2 | 0 | 0 | compileall、diff check |
| Catalog/audit | 2 | 2 | 0 | 0 | full verify |

## 要求カバレッジ

CHAT-001〜007とCHAT-N1〜N4をskill/root contract、chat-first install profile、validator、existing regressionでcoverする。

## 未解決欠陥

なし。

## 非機能・障害試験

full runtime missing fallback、target instruction preservation、repository-local setup、no user commandsをstatic contractで検証した。

## 完了判定

local completion criteriaを満たす。remote PR/CIはrelease gateで確認する。
