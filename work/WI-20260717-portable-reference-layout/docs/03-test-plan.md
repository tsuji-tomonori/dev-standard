# テスト計画

## 品質リスク

誤配置、silent overwrite、target config破壊、manifest drift、既存governance regressionを主要riskとする。

## テストレベルと責任

| レベル | 対象 | 技法 | 環境 | 実施者 |
|---|---|---|---|---|
| Unit | installer/manifest | positive/negative/force | temp directory | automation |
| Contract | directory/config/terminology | validator/static assertions | repository | automation |
| Regression | governance runtime/skills | unittest/catalog/audit | repository | automation |
| Integration | PR checks | GitHub Actions | GitHub | automation |

## 要求別テスト

| テストID | 要求ID | 条件 | 期待結果 | 自動化 |
|---|---|---|---|---|
| TEST-001 | PORT-001/005 | validatorでinventory/configを検査 | standard path、mapping重複なし | yes |
| TEST-002 | PORT-003/004 | dry-run/applyをtemp targetで実行 | expected pathへ一致copy | yes |
| TEST-003 | PORT-N2 | differing target fileを用意 | forceなしfail、forceあり明示更新 | yes |
| TEST-004 | PORT-N2 | existing AGENTS/configでfull apply | active file不変、reference file追加 | yes |
| TEST-005 | PORT-006/007 | full verifyとcurrent surface検索 | regressionなし、曖昧表記なし | yes |

## セキュリティ・AI評価

新AI推論機能はない。custom reviewersのread-only sandbox、bounded model設定、single-authorization契約をexisting contract testで確認する。

## 完了基準

全unit test、repository validator、catalog check、audit、compile、GitHub Actionsがsuccessし、未解決High issueがないこと。
