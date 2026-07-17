# 要求トレーサビリティ

| 要求ID | ユーザー要望 | 設計要素 | 実装 | テスト | 証跡 | 状態 |
|---|---|---|---|---|---|---|
| PORT-001 | 標準directory | source/destination contract | existing directories | validator | official manual | planned |
| PORT-002 | reference repo | README information architecture | README | content test | README | planned |
| PORT-003 | copy方法 | distribution manifest/guide | manifest, INSTALL.md | manifest test | temp install | planned |
| PORT-004 | 簡単で安全な移植 | dry-run installer | tools/install_reference.py | install tests | test report | planned |
| PORT-005 | 適切なagent構成 | standalone discovery | config mapping removal | TOML/config test | manual | planned |
| PORT-006 | lean用語削除 | terminology policy | current docs/tests/PR | rg/test | diff | planned |
| PORT-007 | quality維持 | regression gates | tests/validator | make verify/CI | PR check | planned |

## 未接続項目

- なし。planned targetはderived phaseで実結果へ接続する。
