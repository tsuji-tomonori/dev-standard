# 運用設計

## 運用対象

常時稼働serviceではなく、GitHub repository、devflow CLI、repo-local skills、hooks、GitHub Actionsを運用対象とする。

## 通常操作

| Operation | Command or trigger | Expected result | Failure handling |
|---|---|---|---|
| work item作成 | `python tools/devflow.py init ...` | schema 2の全成果物を生成 | ID、profile、template errorを修正して再実行 |
| initial inspection | `inspect --phase requirements --ignore-approvals` | content/checklist blocker 0 | 文書または判定の原因を修正 |
| initial authorization | `authorize` | requirements digestへ一件記録 | 明示判断、current phase、digestを確認 |
| phase progression | `advance` | 全先行gate再検査後に次phase | 最初のinvalid gateを修正 |
| status | `status` | current gateとauthorization validity表示 | schema不一致ならmigrateまたは新item |
| repository audit | `audit` | chain/schema/preceding gates成功 | 改ざん・不足の原因を修正。履歴を直接編集しない |
| full validation | `make verify` | catalog/test/repo/audit成功 | failure別に修正して全再実行 |
| retrospective | Stop hookまたは`session-retrospective` | reportとpending proposal生成 | proposalを自動適用しない |

## 観測可能性

- `state.json`: phase、status、profiles、workflow schema
- `reports/latest-<phase>.json`: digest、documents、review count、blockers
- `events.jsonl`: creation、migration、check update、initial authorization、phase progression
- `approvals.jsonl`: requirements/requesterの一件の判断chain
- GitHub Actions: commitごとのcatalog、test、validator、audit結果
- PR checks: merge可否とfailure log

## incident categories

| Category | Detection | Response |
|---|---|---|
| stale authorization | APPROVAL_MISSING on requirements | requirements/plan変更を取り消す。無断再承認しない |
| legacy schema | workflow schema error | intake/requirementsならmigrate後にfresh authorization。後工程なら新item |
| preceding gate degradation | `preceding phase gate is no longer valid` | 指定phaseの成果物・check・evidenceを修復 |
| hash-chain tamper | audit/verify_chain error | 変更を停止し、Git履歴と正本から調査。JSONLを再生成しない |
| CI failure | GitHub Actions failure | logから原因を修正して同一branchへpush |
| branch protection blocker | merge不可 | ruleを迂回せず、成功PRを残して外部権限blockerを報告 |

## security and data

secret、個人data、本番log、raw transcriptをrepositoryへ保存しない。証跡は合成dataまたは公開URLを使う。approval/event recordは追記のみとし、誤りは新しいeventで訂正する。

## service levels

常時稼働SLO、RTO、RPO、on-callを設定しない。品質目標はcommand成功、audit整合、CI green、requirements traceabilityで判定する。

## rollback

merge前はfeature branchを修正する。merge後の重大回帰はrevert PRで打ち消し、同じ初回承認workflowとCIを通す。GitHub履歴をforce pushで消去しない。

## access

GitHub branch/repository権限はGitHub側で管理する。workflow permissionは`contents: read`を維持する。local agentは承認済みplan内のfeature branchとPRだけを変更する。
