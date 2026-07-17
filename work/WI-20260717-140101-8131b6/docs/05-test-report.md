# テスト結果

## 対象版

working tree、`adversarial-review` semantic correction。

## 結果概要

| 種別 | 実行数 | Pass | Fail | Skip | 証跡 |
|---|---:|---:|---:|---:|---|
| Skill quick validation | 1 | 1 | 0 | 0 | command output |
| Full unit tests | 28 | 28 | 0 | 0 | make verify output |
| Repository validator | 1 | 1 | 0 | 0 | command output |
| Catalog/audit | 2 | 2 | 0 | 0 | 1,740 checks / audit OK |
| GitHub Actions Governance | 1 | 1 | 0 | 0 | run 29586744518 |

## 要求カバレッジ

REQ-001〜006をcontract、source、target、inventory、install assertionsでカバー。

## 未解決欠陥

なし。

## 非機能・障害試験

runtime変更なし。全体`make verify`とremote CIが成功した。

## 完了判定

Pass。local full verification、Skill validation、remote CI成功。
