# リリース判定

## リリース対象

branch `agent/single-approval-autonomous-flow` の次のlocal commitsを対象とする。

- `fc49ce6` 初回承認後の自律実行flow
- `a2c1778` 協働的傾聴と言語化skill
- `d3ecdaa` work itemと検証証跡

baseは`main`の`9ac8bb3`である。

## 受入条件の充足

- 初回要求、要件、traceability、execution planに対するrequester authorizationは有効。
- 先行phaseの全gateは通過済み。
- `make verify PYTHON=python3`はcatalog 1,740件、unit tests 15件、repository validator、全work item auditを成功。
- secret pattern scanと`git diff --check`は問題なし。
- 新規2 skillsはskill-creator quick validationを成功。
- 傾聴skillの静的・sample評価は27/28、critical failure 0。

## 未解決Issue・例外承認

実装・検証上の未解決issueと例外承認はない。GitHub連携アプリによるbranch作成だけが外部blockerである。

- operation: `github_create_branch`
- result: HTTP 403 `Resource not accessible by integration`
- required capability: repository contents write / branch ref creation
- prohibited workaround: main直接更新、branch protection回避、authorization tokenの推測または露出

## デプロイ・ロールバック

予定手順はfeature branch push、draft PR、GitHub Actions、ready化、squash mergeである。現環境では連携アプリの書込権限不足により未実行。local commitsはGit bundleへ固め、権限のある環境で同じbranchへpush可能にする。

rollbackはmerge前ならbranch更新、merge後ならrevert PRとし、force pushは使わない。

## 利用者・運用者への通知

本release文書と最終応答で、local completion、検証結果、GitHub publication blocker、bundle pathを通知する。GitHub上のPR URLはbranch作成前に拒否されたため存在しない。

## Go / No-Go判断

**No-Go for GitHub release / Go for local handoff.**

コード品質と正本整合はrelease可能水準だが、remote branch、PR、required CI、mergeの実在を確認できないためrelease gateは閉じない。追加承認ではなく、GitHub App権限の付与または権限のある環境からのbundle pushが解除条件である。
