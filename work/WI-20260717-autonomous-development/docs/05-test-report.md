# テスト結果

## 対象

- Branch: local feature branch based on main `9ac8bb3`
- Date: 2026-07-17
- Python: current Codex runtime、GitHub Actions target Python 3.12
- Requirements: AUT-001〜AUT-012、LIS-001〜LIS-008、NFR-001〜NFR-008

## 結果概要

| Test suite | Result | Evidence |
|---|---|---|
| Python compileall | Pass | tools、tests、hooks、skill scriptにsyntax errorなし |
| unittest | Pass | 15 tests、failure 0、error 0、skip 0 |
| catalog check | Pass | 1740 items、source hash一致 |
| repository validator | Pass | policy、skills、agents、hooks、templates整合 |
| devflow audit | Pass | chain、schema、全先行gate整合 |
| listening skill quick validation | Pass | frontmatter、name、structure有効 |
| authorization skill quick validation | Pass | frontmatter、name、structure有効 |
| `make verify PYTHON=python3` | Pass | catalog、unittest、repo validation、audit成功 |

## requirement verification

| Requirement | Test or inspection | Result |
|---|---|---|
| AUT-001〜AUT-004 | init、authorization digest、plan mutation tests | Pass |
| AUT-005〜AUT-007 | no-later-approval、preceding gate recheck、Fail blocking | Pass |
| AUT-008〜AUT-010 | AGENTS/FLOW/plan/skill contract tests、current work item progression | Pass |
| AUT-011 | legacy status rejection and explicit migration test | Pass |
| AUT-012 | repo validator and removed-workflow text test | Pass |
| LIS-001〜LIS-008 | skill contract tests、14-case rubric evidence | Pass |
| NFR-001〜NFR-005 | unittest、audit、validator、migration and tamper tests | Pass |
| NFR-006〜NFR-007 | quick validation、27/28 rubric、critical failure 0 | Pass |
| NFR-008 | local make verify | Pass; GitHub Actions is release-gate evidence |

## failure-path coverage

- 初回承認前: `APPROVAL_MISSING`
- execution plan改変: digest不一致でauthorization失効
- requirements改変: 後続advanceがpreceding gate invalidで停止
- legacy state: current commandを拒否し、明示migrationを要求
- missing evidence: `CHECK_EVIDENCE`
- rationaleなしN/A: `CHECK_NA_RATIONALE`
- Fail with exception: `CHECK_FAIL_BLOCKING`
- tampered chain: `GovernanceError`
- 別phaseでのauthorize: `GovernanceError`

## environment note

このCodex runtimeで`python3 -m venv`が生成したPython symlinkはsandbox固有pathへ向き、`.venv/bin/python`を実行できなかった。依存自体はinstall済みであり、Makefileのdocumented override `PYTHON=python3`を使って同一commandを実行した。repository codeの失敗ではなく、system Pythonによる全検証は成功した。GitHub Actionsは独立したPython 3.12環境で再実行する。

## 未処理結果

失敗、skip、accepted Failはない。GitHub Actionsとmerge後main検証はrelease工程で追記せず、PR/check URLをrelease文書へ記録する。
