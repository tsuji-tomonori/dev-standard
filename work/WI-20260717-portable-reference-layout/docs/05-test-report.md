# テスト結果

## 対象版

PR branchのportable reference layout実装（2026-07-17 local verified revision）。

## 結果概要

| 種別 | 実行数 | Pass | Fail | Skip | 証跡 |
|---|---:|---:|---:|---:|---|
| Python unit | 23 | 23 | 0 | 0 | `python3 -m unittest discover -s tests -v` |
| Repository validator | 1 | 1 | 0 | 0 | `python3 tools/validate_repo.py` |
| Catalog/audit | 2 | 2 | 0 | 0 | `make verify PYTHON=python3` |
| Compile/JSON | 2 | 2 | 0 | 0 | `compileall`, `json.tool` |

## 要求カバレッジ

PORT-001〜007とPORT-N1〜N4をvalidator、installer tests、contract tests、full verifyでcoverした。GitHub Actions結果はrelease文書へ記録する。

## 未解決欠陥

なし。

## 非機能・障害試験

conflict、explicit force、dry-run no-write、target active config preservation、manifest inventory driftを自動検証し全て成功した。

## 完了判定

local completion criteriaを満たした。remote CI成功をrelease gateとする。
