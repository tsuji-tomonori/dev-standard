# 自律実行計画

## 承認対象

- Work item: WI-20260717-123310-938d42
- タイトル: Research-grounded adversarial validation skill and skill catalog
- 対象プロファイル: CORE, AI-CONDITIONAL
- 初回承認者: requester（本依頼）

この計画は、要件定義およびトレーサビリティと一体で初回承認する。承認後は、記載した権限境界内で追加の工程承認を求めず、完了まで自律実行する。

## 許可する操作

- research retrieval/analysis、repository docs/skills/tests/work evidence編集
- local validation、feature branch/PR/CI、PR metadata/comment更新

## 許可しない操作

- real target attack、production/destructive action、secret/PII保存、PR merge
- cited evidenceを超える効果保証、single evaluatorの無検証採用

## 作業分解

| ID | 作業 | 変更対象 | 検証 | 完了条件 |
|---|---|---|---|---|
| PLAN-001 | primary research synthesis | skill reference | source/rule trace | research map完成 |
| PLAN-002 | adversarial validation workflow | new skill/references | quick/contract validation | end-to-end method |
| PLAN-003 | Skills catalog | docs/SKILLS.md/manifest | inventory validator | 全skill掲載 |
| PLAN-004 | integration/regression | AGENTS/chat flow/tests | full verify/audit | existing behavior維持 |
| PLAN-005 | publication | work/GitHub | PR/CI | ready green PR/closed WI |

## 外部副作用

| 操作 | 対象 | 影響 | rollback |
|---|---|---|---|
| research web access | public primary sources | citation retrieval | local research map remains |
| GitHub branch/PR | repository | reviewable external state | PR close/revert |

## 既定の判断

| 判断点 | 追加確認せず採用する既定値 | 根拠 |
|---|---|---|
| attack depth | risk-based budget | exhaustive claimを避ける |
| evaluator | independent deterministic oracle優先、LLM judgeはbias check付き | reliability研究 |
| finding disclosure | minimal/redacted artifact | defensive useとsecret保護 |

## 検証計画

- source trace review、skill quick validation、contract/inventory tests、catalog、audit、GitHub Actions。

## 停止条件

- 権限境界外の不可逆操作または外部権限が不可欠になった場合は実行せず、ブロッカーとして記録する。
- primary sourceへ到達できず重要ruleを根拠付けできない、またはGitHub write権限不足の場合はblocker化する。

## 完了定義

- [ ] ADV-001〜008、ADV-N1〜N4がpass
- [ ] full tests、validator、audit、skill validation、CI success
- [ ] ready/mergeable PR、closed work item
