# 要求トレーサビリティ

| 要求ID | ユーザー要望 | 設計要素 | 実装 | テスト | 証跡 | 状態 |
|---|---|---|---|---|---|---|
| CHAT-001 | 自然言語で開始 | umbrella skill trigger | chat-first SKILL.md | contract test | skill metadata | planned |
| CHAT-002 | 自動導入 | preflight/bootstrap contract | AGENTS/skill/reference | static test | docs | planned |
| CHAT-003 | 要件化 | conversational intake | umbrella/govern skills | contract test | examples | planned |
| CHAT-004 | 全工程自走 | lifecycle orchestration | AGENTS/skills | regression/audit | work evidence | planned |
| CHAT-005 | folder copy | copy-only quick start | README/INSTALLATION | content validation | guide | planned |
| CHAT-006 | target保護 | safe bootstrap boundary | reference policy | contract test | safety section | planned |
| CHAT-007 | gate維持 | deterministic internal harness | existing runtime | make verify/CI | reports | planned |

## 未接続項目

- なし。全要求は設計・実装・test targetへ接続済み。
