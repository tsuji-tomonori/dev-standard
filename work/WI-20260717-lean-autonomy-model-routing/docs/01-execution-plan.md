# 自律実行計画

## 承認対象

- Work item: WI-20260717-lean-autonomy-model-routing
- タイトル: Lean promptと低コストmodel routing
- 対象プロファイル: CORE, AI-CONDITIONAL
- 初回承認者: requester（本依頼で明示承認済み）

本計画は要件・traceabilityと一体で承認する。以降、記載した範囲で追加工程承認を求めず完了まで自律実行する。

## 許可する操作

- repository instruction、skills、Codex config/custom agents、docs、validator、tests、work evidenceの編集
- OpenAI公式文書とCodex manualのread-only取得
- local validation、commit、GitHub branch push、draft PR、CI修正、ready化、merge可能性確認

## 許可しない操作

- secret取得・公開、branch protection回避、mainへの直接write、force push、未承認の課金API実行
- root agentの一律軽量model固定、安全・権限・証跡gateの削除
- checklistの未検証bulk pass、公式価格やavailabilityの推測

## 作業分解

| ID | 作業 | 変更対象 | 検証 | 完了条件 |
|---|---|---|---|---|
| PLAN-1 | 公式指針を抽出 | official docs/manual | source照合 | model/prompt原則が特定済み |
| PLAN-2 | promptをoutcome-first化 | AGENTS、governance skills、custom agents | diff/test | 不変条件を保ち重複削減 |
| PLAN-3 | model routing設定 | config、agent TOML、AI policy | TOML/validator/test | terraと役割別effortが強制 |
| PLAN-4 | checklist分離と回帰check追加 | AI policy、validator、tests | full verify | catalog品質を保ちprompt量を増やさない |
| PLAN-5 | lifecycle evidence完成 | work item docs/checks | phase inspect/audit | release以外の全gate成功 |
| PLAN-6 | GitHub公開 | feature branch、PR | GitHub checks | PR URLとgreen checkを記録 |

## 外部副作用

| 操作 | 対象 | 影響 | rollback |
|---|---|---|---|
| branch push | tsuji-tomonori/dev-standard | remote branch作成 | branchを残してPR close、または権限者が削除 |
| PR作成 | main向けdraft PR | review/CI開始 | PR close |
| merge | main | repository既定変更 | revert PR |

## 既定の判断

| 判断点 | 追加確認せず採用する既定値 | 根拠 |
|---|---|---|
| root model | pinしない | taskに応じた能力選択と独創性を保持 |
| reviewer model | gpt-5.6-terra | Codex manualのlower-cost recommendation |
| effort | routine low、analysis medium、security/audit high | 必要最小限でqualityを段階化 |
| parallelism | max_threads 3、depth 1、必要時のみdelegate | subagent token costを制限 |
| verbosity | reviewer low、rootは固定しない | summaryは短く、final completenessはrootが保持 |

## 検証計画

- 17件以上のunit tests、TOML parse、prompt budget/model routing assertions
- repository validator、catalog 1,740件整合、compile、secret scan、diff check、work-item audit
- GitHub Actionsのrequired checks

## 停止条件

- GitHub App書込権限が再度拒否され、認証済み代替もない場合はrelease blockerにする。
- 公式docsとCodex manualで利用可能modelが矛盾する場合はCodex manualをproject configの正本とし、差異を明記する。
- 要件境界外の不可逆・課金・secret操作が必要なら実行しない。

## 完了定義

- [ ] LA-001〜007とLAN-001〜004が証跡付きで充足
- [ ] 全phase gate、full verification、GitHub checksが成功
- [ ] PRを作成し、release evidenceを記録
- [ ] retrospectiveを完了しwork itemがclosed
