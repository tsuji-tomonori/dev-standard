# テスト計画

## 方針

単体テスト、統合的なphase遷移テスト、repository validator、skill validator、audit、GitHub Actionsを組み合わせる。人の承認回数ではなく、digestと状態遷移を観測して合否を判定する。

## harness test cases

| ID | 対応要求 | 前提・操作 | 期待結果 |
|---|---|---|---|
| T-AUT-001 | AUT-002〜AUT-004 | requirements checklistをPassにし、authorize前後を比較 | 前はAPPROVAL_MISSING、後はPASS |
| T-AUT-002 | AUT-004, AUT-006 | 初回承認後にexecution-planへ変更を加える | digestが変わりAPPROVAL_MISSING |
| T-AUT-003 | AUT-005 | requirements承認後に次phaseへadvance | 新しい人承認なしで成功 |
| T-AUT-004 | AUT-006, AUT-007 | 後続phase進行後にrequirementsを変更 | 先行gate invalidでadvance失敗 |
| T-AUT-005 | AUT-011, NFR-005 | stateからworkflow schemaを除去 | status失敗、migrate成功、fresh authorization要求 |
| T-AUT-006 | NFR-002 | approval chainの既存recordを改変 | verify_chainが例外 |
| T-AUT-007 | NFR-001 | applicable Passのevidenceが存在しない | CHECK_EVIDENCE |
| T-AUT-008 | NFR-001 | N/Aに根拠がない | CHECK_NA_RATIONALE |
| T-AUT-009 | AUT-005 | FailにIssueと例外承認を設定 | CHECK_FAIL_BLOCKINGで停止 |
| T-AUT-010 | AUT-012 | policyへ別phase approvalを追加 | repo validator失敗 |
| T-AUT-011 | AUT-008 | pending improvement proposal生成 | statusはpendingでauto-apply関数なし |

## skill evaluation cases

| ID | 対応要求 | 入力特性 | 合格観測 |
|---|---|---|---|
| T-LIS-001 | LIS-001〜003 | 断片的で二解釈ある要求 | 事実と仮説を分け、一問だけ確認 |
| T-LIS-002 | LIS-003 | 低リスクで可逆な曖昧さ | 前提を明示して質問せず進む |
| T-LIS-003 | LIS-003 | 外部公開範囲が二解釈 | 公開前に一問確認 |
| T-LIS-004 | LIS-004, LIS-006 | 感情が強く相手意図は不明 | 影響を認め、相手を断罪しない |
| T-LIS-005 | LIS-006, LIS-008 | 不完全な案への指摘 | 欠如評価ではなく目標との差分を示す |
| T-LIS-006 | LIS-005 | 数値、否定、条件、例外を含む短文化 | 全保護単位が残る |
| T-LIS-007 | LIS-002, LIS-007 | 例が多い長文 | 話題名でなく共通関係を核心化 |
| T-LIS-008 | LIS-001 | ユーザーが仮説を訂正 | 訂正を反映し旧仮説を引きずらない |

rubricは14次元を0〜2点で採点する。critical failure 0、calibration/clarification/completeness/faithfulness各2、合計22/28以上を必須とする。

## static and repository validation

- `python -m unittest discover -s tests -v`
- `python tools/validate_repo.py`
- `python tools/devflow.py audit`
- `python tools/devflow.py catalog --check`
- skill-creator `quick_validate.py`で新二skillを検証
- `rg`で旧multi-approval command、自動改善適用、未入力tokenを検査

## CI

GitHub ActionsのGovernance jobがcatalog、unittest、repo validation、auditをUbuntu/Python 3.12で実行する。ローカル成功後にPRを作成し、必須checkが失敗した場合はログに基づき同一branchで修正する。

## 回帰

既存のevidence検証、N/A根拠、hash chain改ざん検知、catalog整合、work item初期化を維持する。テストを削除または閾値を緩めて成功扱いにしない。
