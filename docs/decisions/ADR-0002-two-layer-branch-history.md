# ADR-0002: mainのrelease履歴とdevのengineering履歴を二層で試行する

- 状態: Superseded by ADR-0004
- Date: 2026-07-24
- Issue: #20

> 2026-08-27に試行を終了した。branch topology、merge方式、required checkをガードレールとして強制せず、repository host側の設定へ委任する。以下は当時の判断を保存する履歴であり、現行policyではない。

## 背景

`main`へのsquash mergeは、利用者が参照する履歴をrelease単位の一commitへ整理できる。一方、topic PR内の意味あるcommit列は`main`の到達可能履歴へ残らない。このrepositoryでは、複数commitを持つPRを案件ごとにsquashまたはmerge commitで統合しており、release履歴とengineering履歴のauthorityが一定していなかった。

長寿命の`dev`を追加して`dev → main`をsquashするだけでは、squash commitは`dev`の祖先にならない。次の統合でmerge baseが進まず、既にreleaseしたfile差分やconflictが再評価され得る。反対に、すべてをmerge commitで`main`へ残すと、利用者向けに一変更・一release commitへ整理する目的を満たさない。

## 決定

### 試行範囲

二層branch契約を`dev-standard`自身だけで2回の通常release cycleに限定して試行する。恒久採用、他repositoryへの一般化、portable profileへの既定配布は試行結果を確認してから別途判断する。

machine-readableな正本は`.github/branch-policy.json`とし、`tools/branch_policy.py`、GitHub Actions、回帰test、文書を同じ契約へ整合させる。2回の管理された試行中は`trial.phase`以外のpolicy fieldを不変とし、base／before側policyと候補policyの差異を拒否する。branch方向、marker、prefix、subject規約等を変更する場合は本試行を停止し、別の判断として再設計する。

### 導入phaseと有効化

導入commitでは`trial.phase`を`bootstrap`とする。bootstrap中は通常topicと通常releaseを拒否するが、既存`dev`がcurrent `main`を祖先に持ち、両tip treeが一致し、まだbranch policyを含まない場合に限り、`Branch-Policy-Bootstrap: true`と`Refs #20`を持つ初回導入PRを`dev`へmerge commitで統合できる。その後、`Release-Type: bootstrap`、`Release-Review`、`Included-PRs`、必須4見出し、`Refs #20`を持つ`dev → main` PRで同じtreeをsquashする。このbootstrap releaseは2回の通常release試行には数えず、Issueをcloseしない。

`dev`が存在しないrepositoryでは、従来どおり導入PRを先に`main`へsquashし、そのcommitから`dev`を作成できる。いずれの経路でも、ruleset、required checks、squash message設定、open PR #12移行、tree一致を確認する前に`trial`へ移行しない。bootstrap中に`main`へ補正commitが入った場合は、`Reconciliation-Type: bootstrap`で`dev`へ同期する。

trialを有効化する前に、`.github/branch-policy.json`の`activation_requirements`をすべて確認する。有効化PRは`main`をbaseとし、次を満たす。

- 差分は`.github/branch-policy.json`の`phase: bootstrap`から`phase: trial`への変更と、その変更を評価するactive review YAMLだけとする。
- PR bodyと最終commitへ`Trial-Activation: true`と各`Activation-Check: <requirement>`を一度ずつ記録する。
- 利用可能な場合はbase側のbranch-policy validator、review validator、dependencyで候補treeを検査し、変更後validatorだけを弱めても当該PRの判定へ使わない。初回導入はbaseにvalidatorがないためcandidate版へfallbackする。

dev-firstで導入した場合はbootstrap releaseを`main`へsquashした直後に、`Reconciliation-Type: bootstrap`の`main → dev` PRでsquash commitをancestorへ戻す。続いて有効化commitを`main`へsquashした後も、同じreconciliation種別でpolicyとactive reviewをmerge commitとして伝播する。各reconciliationはmerge resultのtreeがsource `main`と一致する場合だけ許可する。最初の小さなtopic／regular release／reconciliationを1回目の管理されたdry runとして扱い、その後に2回目のrelease cycleを行う。

### branchの役割

- `main`はdefault branchとし、利用者へ公開可能なrelease履歴を保持する。通常releaseは`dev → main`、緊急修正は`hotfix/* → main`をsquash mergeする。linear historyを維持する。
- `dev`は未release変更の統合先とengineering commit historyの保持先とする。topic PR、conflict-freeな`main → dev` reconciliation、hotfix競合を解消した`reconcile/*` PRをmerge commitで統合する。
- topic branchは原則`dev`から分岐し、`dev`へPRを作る。中間commitはengineering historyであり、単独でrelease可能であることまでは保証しない。

### 通常release transaction

1. release前に`main`が`dev`の祖先であることを確認する。
2. `dev`へのmerge、auto-merge、bot updateをfreezeし、単一のrelease operatorだけが操作する。
3. release PRへ`Release-Type: regular`、`Release-Review: governance/reviews/CHG-....yaml`、`Included-PRs: #...`と必須4見出しを記録し、`dev → main`をsquash mergeする。
4. remote最新tipを直接比較し、`git diff --quiet origin/main origin/dev`が成功することを確認する。
5. `main → dev`をmerge commitでreconciliationする。機能変更やreview更新を混在させない。
6. `main`が`dev`の祖先であり、両tip treeが一致することを確認してfreezeを解除する。

通常releaseでtreeが一致しない場合は停止する。`ours` merge、force reset、force push、history rewriteで不一致を隠さない。

hotfix PRでは`Release-Type: hotfix`、`Release-Review`、`Included-PRs`とIssue closing keywordを記録する。hotfixでは`dev`に未release変更が存在し得るため、reconciliation後に`main`が`dev`の祖先であることは要求するが、両tip treeの一致は要求しない。

conflict-freeな場合は`main → dev`を直接mergeする。conflictする場合はfreeze中の`dev`から`reconcile/hotfix-*`を分岐し、current `main`をsecond parentとしてmergeして競合を解消する。そのheadから`dev`へmerge commitで統合し、outer merge resultが解消済みhead treeを保持することを検査する。hotfixが変更したpathについて、prior `dev`またはhotfix前のblobをそのまま残す`ours`相当の解消は、祖先関係だけを回復して修正を捨てるため拒否する。

### 試行停止のrollback transaction

trialを停止するときは`main`からhotfix branchを作り、phaseを`bootstrap`へ戻すpolicyと対応するactive review YAMLだけを変更する。PR bodyと最終squash commitへ`Trial-Rollback: true`とhotfix release markerを記録し、`main`へsquashした後に`Reconciliation-Type: hotfix`で`dev`へ伝播する。

rollback reconciliation後はbootstrap policyがtopic mergeと通常releaseを拒否する。未release変更が`dev`に残る場合もhistory rewriteせず凍結し、再開時はactivation requirementsを再確認する。

### 履歴とdiffの意味

reconciliationは祖先関係とtreeを回復するが、squash前の詳細commitを`main`の祖先へ変換しない。詳細commitを`dev`から到達可能に保つ以上、次回release PRのcommit一覧や`git log main..dev`には過去releaseの詳細commitが残り得る。これは本モデルの正常な性質である。

受入条件は「過去commitが一覧から消えること」ではなく、次の二点とする。

- 過去release済みのfile差分が次回の`git diff main...dev`へ再出現しない。
- 過去の詳細commitは`dev`から到達可能なまま保持される。

cleanなrelease PRのcommit一覧も必要な場合、`dev`を直接headにせず、各releaseで`main`から生成する別release branchへ変更する必要がある。それは本試行の対象外とする。

### 証跡のauthority

- topic最終commitは変更単位のCommit Commentとreview YAML参照を保持する。
- topic内の中間commitは意味あるengineering historyを保持する。
- `dev`上のtopic merge commitはtopology markerとする。
- release PR bodyは、含まれるPR、要件・設計影響、互換性、rollback、残存riskを集約する事前release manifestとする。
- release review YAMLはrelease時に選択したcheck結果を保持する。
- `main`上のsquash commitはrelease manifestの永続的な索引とする。
- reconciliation merge commitは祖先関係を回復するtopology markerとし、新しい正本を持たない。

### GitHub上の限界

最終squash commitはmerge操作時に作成され、messageを編集できる。そのcommit object自体を通常のPR required checkで事前検証することはできない。release PR bodyとrelease reviewを事前authorityとし、`main` push時のCommit Comment検査を事後auditとして扱う。

`pull_request` workflowはPRのmerge refに含まれる候補workflowから実行され得る。base／before側validatorを選択してもworkflow file自体はimmutableにならず、個人repositoryではorganization rulesetのrequired workflowをauthorityにできない。required status checksは可能な場合にGitHub Actionsをexpected sourceへ固定し、workflow変更は単一operatorが差分とcheck sourceを明示確認する。この試行はCIをtamper-proofとは表明しない。

required checkは各event時点のsnapshotであり、`main`と`dev`を跨ぐ原子的なrelease lockでもない。試行中は単一operatorと明示freezeをauthorityとする。複数operatorへ拡張する場合はGitHub Appまたはbotによるlockを別変更で実装する。

## 却下した選択肢

### mainだけへsquash mergeする

release履歴は簡潔だが、named branchから到達可能な詳細commitを保持できないため却下した。

### mainへmerge commitする

engineering historyは保持できるが、一変更・一release commitという利用者向け履歴の目的を満たさないため、現時点では採用しない。

### 長寿命devをreconciliationなしで使う

merge baseが進まず、既出差分とconflictを再評価するため却下した。

### releaseごとにmainからrelease branchを作る

release PRのcommit一覧を新しい変更だけへ限定できるが、branch生成とpatch選択の追加実装が必要である。2層試行でcommit一覧の累積が許容できないと判明した場合の代替案とする。

### trunk-based developmentへ統一する

一般的には単純で統合頻度を高く保てる。一方、本試行の「mainのsquash release履歴」と「named branch上の詳細commit保持」を同時に評価できないため、比較対象として残す。

## 結果

- branch方向、merge方式、freeze、reconciliation、hotfix変更の保持、証跡authorityが機械検査対象になる。
- PRのintegration resultとtopic head evidenceを別jobで検査する。既存rulesetの`verify` contextを切れ目なく移行するため、3 jobを集約する互換`verify` jobを残す。
- `main`と`dev`のGitHub ruleset設定はrepository外部の運用設定として適用し、trial有効化前に確認する。
- policyとvalidatorの変更は利用可能なbase／before側validatorで検査し、phase遷移はmainのactivation／rollback commitとmainからdevへのreconciliationでだけ伝播する。workflow file自体の自己統制限界は単一operatorの明示reviewで補う。
- PR #12は試行開始前に依存関係を確認し、`dev`基準へrebaseまたはretargetする。
- release操作は増える。push auditで検出した失敗はhistory rewriteせず、freezeを維持してrevertまたはforward fixする。

## 恒久採用条件

2回の通常releaseとreconciliationを完了し、次をすべて確認した場合だけ恒久採用を再判断する。

- 2回目のrelease diffへ1回目のrelease済みfile差分が再出現しない。
- 詳細commitが`dev`から到達可能である。
- reconciliation後の祖先関係とtree一致が自動検査される。
- freeze違反、手動history修復、未管理conflictが発生しない。
- release PRの累積commit表示、追加CI時間、操作costを受容できる。

条件を満たさない場合はrollback transactionでphaseを`bootstrap`へ戻し、最終`main`を`dev`へreconciliationして新規topic統合と通常releaseを停止する。既存historyはrewriteしない。


## 参照と適用境界

この決定は、Gitの履歴・diff・ancestor semanticsとGitHubのruleset／workflow仕様を公式資料で確認した上で、このrepository固有の目的へ適用したlocal policyである。参照資料は、長寿命`dev`を普遍的に推奨する根拠ではなく、採用した仕組みの技術的挙動とplatform限界を検証するために使用する。

- Git FAQ: long-running branch間でsquash mergeを反復した場合のmerge-base問題と通常mergeの推奨
  - https://git-scm.com/docs/gitfaq
- `git merge`: `--squash`がmerge commitと`MERGE_HEAD`を作らないこと
  - https://git-scm.com/docs/git-merge
- `git diff`: two-dot／three-dotとmerge-base基準の差分
  - https://git-scm.com/docs/git-diff
- `git merge-base`: `--is-ancestor`による祖先関係の検査
  - https://git-scm.com/docs/git-merge-base
- GitHub rulesets: branch deletion、force push、linear history、required status checks、merge method等の規則
  - https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
- GitHub Actions security: `pull_request`／`pull_request_target`の実行境界とuntrusted codeの扱い
  - https://docs.github.com/en/actions/reference/security/secure-use
- GitHub required workflows: organization／enterpriseで管理するworkflow authorityの適用範囲
  - https://docs.github.com/en/enterprise-cloud@latest/actions/how-tos/write-workflows/manage-workflow-runs/require-workflows
- GitHub Flow、DORA trunk-based development、GitLab Flow: 単純な主線と短命branchを重視する一般的な比較対象
  - https://docs.github.com/en/get-started/using-github/github-flow
  - https://dora.dev/capabilities/trunk-based-development/
  - https://about.gitlab.com/topics/version-control/what-is-gitlab-flow/

継続更新されるGitHub文書はtrial activation前と恒久採用判断時に再確認する。Git／GitHubの仕様変更、ruleset capability、workflow authorityの変更が本決定の前提を変える場合は、trialを停止して本ADRとbranch policyを再評価する。
