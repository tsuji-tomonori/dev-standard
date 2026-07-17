# 要求トレーサビリティ

| 要求ID | ユーザー要望 | 設計要素 | 実装 | テスト | 証跡 | 状態 |
|---|---|---|---|---|---|---|
| LA-001 | 指示過多を避ける | outcome-first prompt contract | AGENTS、govern skill、reviewer prompts | skill contract tests | test report、diff | planned |
| LA-002 | 人の介在を最小化 | single authorization invariant | existing policy/harnessを保持 | devflow tests | audit | planned |
| LA-003 | AIの独創性を減らさない | root unpinned、decision rules | config、AI operating policy | config/policy tests | validator | planned |
| LA-004 | 安価で軽量なmodel | role-based routing | custom agent TOML | model routing test | official docs、validator | planned |
| LA-005 | 適切なchecklist | validation contract分離 | AI policy、existing catalog/harness | catalog/audit | 1,740-item catalog | planned |
| LA-006 | 公式linkに基づく設定 | source-backed policy | AI operating policy | required-term test | official URLs | planned |
| LA-007 | PR作成 | publication flow | GitHub branch/PR | GitHub checks | PR URL | planned |

## 未接続項目

なし。実装・test・evidence欄は承認時点の予定targetであり、derived phase文書へ実結果を記録する。
