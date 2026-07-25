# 開発契約

## 目的

自然言語の依頼から、必要な要件、実装、検証、Commit Comment、PRまでを最小十分な手順で完了します。手順や文書を増やすことではなく、利用者が得る結果と検証可能な証拠を優先します。

## 実行profile

| profile | 適用条件 | 追加する検証 |
|---|---|---|
| `direct` | 局所的、可逆、外部副作用なし | 対象test、build、lint、type、生成物drift |
| `assured` | 公開契約、DB、IaC、dependency、共有UI、generator、要件、governance、distribution | 関連するRisk-selected checkと必要時の独立review |
| `regulated` | 認証・認可、PII、データ損失、不可逆production、法令・契約統制、高額操作 | 明示承認、work item、phase gate、hash chain、監査 |

公開API変更は通常`assured`で扱い、公開APIであることだけを承認理由にしません。

## 変更フロー

1. 依頼、リポジトリ指示、権限境界を確認する。
2. 要件・設計・公開契約・data・IaC・dependency・securityへの影響を判定し、profileとcheckを選ぶ。
3. 永続要件が変わる場合だけ正本を更新する。
4. 実装し、変更範囲の決定的な検証から開始する。
5. as-built対象では実装から設計を生成し、driftを検査する。
6. selected check結果、Commit Comment、PRを作成し、現在HEADの外部CIを確認する。

未選択checkをN/Aとして保存しません。失敗や新しい影響が見つかった場合だけ、検証範囲やreviewを拡張します。

## このrepositoryの二層branch試行

`dev-standard`自身ではIssue #20に基づき、2回の通常releaseに限定して`main`と`dev`の二層branch契約を試行します。これはportableな開発標準ではなく、導入先repositoryの既定branch戦略を変更しません。machine-readableな正本は`.github/branch-policy.json`、長期判断の理由は[`ADR-0002`](../decisions/ADR-0002-two-layer-branch-history.md)です。導入時のphaseは`bootstrap`であり、外部GitHub設定と移行条件を満たすまで通常releaseを有効化しません。2回の試行中は`trial.phase`以外のmachine contractを変更できません。branch方向、marker、prefix、subject規約等の変更は試行を停止して別判断とします。

### 試行開始前のbootstrap

既存`dev`がcurrent `main`を祖先に持ち、両tip treeが一致し、まだbranch policyを含まない場合、初回導入PRは`dev`をbaseにできます。PR bodyへ`Branch-Policy-Bootstrap: true`と`Refs #20`を記録し、merge commitで統合します。統合後CIが成功したら、`Release-Type: bootstrap`、`Release-Review`、`Included-PRs`、必須4見出し、`Refs #20`を持つ`dev → main` PRを作成します。bootstrap releaseはIssueをcloseせず、2回の通常release試行にも数えません。`dev`が存在しない場合は導入PRを先に`main`へsquashし、そのcommitから`dev`を作成します。

導入直後は`.github/branch-policy.json`の`trial.phase`を`bootstrap`に保ち、通常の`dev → main` releaseを許可しません。次を完了してからtrialへ移行します。

1. `dev`が存在しない場合は導入時点の`main` commitから作成する。既存`dev`を使う場合は、初回導入前に`main → dev`をreconciliationし、両tip treeが一致することを確認する。
2. `main`と`dev`へ別々のrulesetを設定し、required checksを`integration`、`evidence`、`branch-policy`へ揃える。
3. squash messageの既定値をPR titleとdescriptionにし、削除・force push・rebase mergeを禁止する。
4. open PR #12を現在の`dev`へrebaseまたは再作成してretargetする。
5. branch graph回帰testが成功し、単一release operatorを明示する。
6. `.github/branch-policy.json`の`phase`を`trial`へ変更し、対応するactive review YAMLも同じcommitで更新するactivation PRを`main`へ作成する。PR bodyへ`Branch-Policy-Bootstrap: true`、`Trial-Activation: true`、全`Activation-Check`、`Refs #20`を記録する。
7. activation squash commitを`main → dev`へmerge commitで同期する。PR bodyは`Reconciliation-Type: bootstrap`と`Source-PR`を持ち、このreconciliationではactivation policyとそのactive review以外の新しい変更を混在させない。

初回のbranch policy導入PRだけは、同期済みでpolicy未導入の`dev`へmergeできます。それ以外のbootstrap中topic PRと通常releaseはrequired checkで拒否します。dev-firstのbootstrap releaseを`main`へsquashした後、およびbootstrap中に`main`へ補正commitが入った場合は、`Reconciliation-Type: bootstrap`で`dev`へ同期し、両tip treeを一致させます。activationが`main`だけへ入り`dev`がbootstrapのまま残る状態でもtopic統合と通常releaseを開始しません。policyとactive reviewが両branchで一致し、`main`が`dev`の祖先になった後だけ試行を開始します。Governance workflowは利用可能な場合にPR baseまたはpush before側からbranch-policy validator、review validator、validator dependencyを取り出して候補treeを検査します。これにより、候補validatorだけを弱める変更は当該PRまたはpushの判定へ使われません。最初の導入PRではbaseにbranch-policy validatorがないためcandidate版へfallbackします。activation後の最初の小さなtopic変更を1回目のrelease dry runとし、`dry-run-completed`をactivation前提にはしません。

### branchの役割

- `main`
  - default branchを維持する。
  - 利用者へ公開可能なrelease履歴を保持する。
  - 通常releaseは`dev → main`、緊急修正は`hotfix/* → main`をsquash mergeする。
  - linear history、PR、required checksを必須とし、削除とforce pushを禁止する。
- `dev`
  - 未release変更の統合先と、意味あるengineering commit historyの保持先とする。
  - topic PR、conflict-freeな`main → dev` reconciliation、hotfix競合を解消した`reconcile/*` PRをmerge commitで統合する。
  - PRとrequired checksを必須とし、削除とforce pushを禁止する。
- topic branch
  - 原則`dev`から分岐し、`dev`へPRを作る。
  - `fixup!`、`squash!`、空疎なWIP subjectをmerge前に除去する。
  - `dev`へmerge後は削除できる。詳細commitは`dev`から到達可能なまま残る。
- reconciliation branch
  - 通常は作成しない。hotfixを`main → dev`へ直接mergeできない場合だけ、freeze中の`dev`から`reconcile/hotfix-*`を分岐する。
  - current `main`をmergeし、競合を明示解消した一つのmerge commitをheadにして`dev`へPRを作る。
  - outer mergeは解消済みhead treeをそのまま保持し、`ours` merge等でhotfixを破棄しない。


### 通常release transaction

releaseをsquashとreconciliationに分かれた一つのtransactionとして扱います。

1. release PRのbaseを`main`、headをrepositoryの`dev`そのものとする。
2. `git merge-base --is-ancestor origin/main origin/dev`でrelease前のancestor関係を確認する。
3. `dev`向けPRのmerge待ち、auto-merge、bot updateを停止し、単一のrelease operatorがfreezeを宣言する。
4. release PR bodyへ`Release-Type: regular`、`Release-Review: governance/reviews/CHG-....yaml`、`Included-PRs: #...`、少なくとも一つの`Closes #...`等を記録し、含まれるPR、要件・設計影響、互換性・rollback、残存リスクを必須4見出しへ集約する。
5. `dev → main`をsquash mergeする。
6. reconciliation前にremote最新tipを直接比較する。

```bash
git fetch origin main dev
git diff --quiet origin/main origin/dev
```

`git diff main...dev`ではなく両tip treeを直接比較します。不一致なら停止し、`ours` merge、force reset、force push、history rewriteで通過させません。

7. `main → dev`のreconciliation PRを作成し、PR bodyへ次を記録する。

```text
Reconciliation-Type: release
Source-PR: #<release PR number>
```

8. merge commitで統合し、次を確認してからfreezeを解除する。

```bash
git merge-base --is-ancestor origin/main origin/dev
git diff --quiet origin/main origin/dev
```

reconciliationには新しい機能変更、review YAML更新、文書修正を混在させません。

### hotfixのreconciliation

`hotfix/*`は`main`から分岐し、PR bodyへ`Release-Type: hotfix`、`Release-Review`、`Included-PRs`、少なくとも一つのIssue closing keywordと必須4見出しを記録して`main`へsquash mergeします。conflictがなければ、その直後に`main → dev`をmerge commitでreconciliationし、PR bodyへ次を記録します。

```text
Reconciliation-Type: hotfix
Source-PR: #<hotfix PR number>
```

hotfix時は`dev`に未release変更が存在し得るため、`main`が`dev`の祖先になることは要求しますが、両tip treeの一致は要求しません。

`main → dev`がconflictする場合は、protected `main`へ解消commitを追加しません。freeze中の`dev`から`reconcile/hotfix-*`を分岐し、current `main`をmergeして競合を解消します。reconciliation branchのheadは、first parentがfreeze直前の`dev`、second parentがcurrent `main`である一つのmerge commitとします。そのbranchから`dev`へPRを作り、同じ`Reconciliation-Type: hotfix`と`Source-PR`を記録します。CIはsynthetic outer mergeが解消済みhead treeを保持すること、current `main`が結果の祖先になること、hotfixで変更されたpathを`ours`等で捨てていないことを検査します。競合pathでprior `dev`またはhotfix前のblobをそのまま採用した場合は、hotfixを統合した証拠にならないため拒否します。

### trial停止とrollback

2回の試行を完了できない、運用costが便益を上回る、またはfreeze・topology invariantを維持できない場合は、次のtransactionで`bootstrap`へ戻します。

1. `main`から`hotfix/*`を分岐し、`.github/branch-policy.json`のphaseを`bootstrap`へ戻し、対応するactive review YAMLだけを更新する。
2. PR bodyと最終squash commitへ`Trial-Rollback: true`、`Release-Type: hotfix`、`Release-Review`、`Included-PRs`を記録する。
3. `main`へsquash mergeした後、`Reconciliation-Type: hotfix`の`main → dev` PRで同じpolicyとreviewを伝播する。競合する場合は前節の`reconcile/hotfix-*`経路を使用する。
4. reconciliation後はbootstrap policyによりtopic mergeと通常releaseを停止し、`dev`を同期済みまたは未release変更を保持した凍結状態として扱う。

rollbackへ機能変更や別の文書変更を混在させません。既存historyをrewriteせず、再開する場合はactivation requirementsを改めて満たします。

### 履歴とdiffの読み方

reconciliationは祖先関係とtreeを回復しますが、squash前の詳細commitを`main`の祖先へ変換しません。詳細commitを`dev`から到達可能に保つ以上、次回release PRのcommit一覧や`git log main..dev`には過去releaseの詳細commitが残り得ます。

試行の受入条件は、過去commitを一覧から消すことではありません。次を検査します。

- 前回release済みのfile差分が次回の`git diff main...dev`へ再出現しない。
- 詳細commitが`dev`から到達可能なまま残る。

cleanなrelease PR commit一覧も必要になった場合は、`main`からreleaseごとに生成する別branch方式を再検討します。

### CIとGitHub設定

`Governance` workflowは次を分離します。

- `integration`: Pull Requestではsynthetic merge refをcheckoutし、baseへ統合した結果をtestする。
- `evidence`: PR headをcheckoutし、topic最終commitのCommit Commentとreview YAML、またはrelease reviewを検査する。
- `branch-policy`: base/head許可行列、ancestor、tip tree、merge parent、commit subject、hotfix変更がreconciliationで保持されたことを検査する。

`main`と`dev`には別々のGitHub rulesetを設定し、`.github/branch-policy.json`のmerge方式、required checks、linear history、削除・force push制限へ合わせます。導入前の`verify` checkをrequiredにしている設定から安全に移行できるよう、workflowは3 jobを集約する互換`verify` contextも維持しますが、trial rulesetでrequiredにする正本は`integration`、`evidence`、`branch-policy`です。source branch名の許可行列はrulesetだけへ依存せず、`branch-policy` required checkで検査します。required status checksは可能な場合にGitHub Actionsをexpected sourceとして設定します。

`pull_request` workflow自体はPRのmerge refに含まれる候補workflowから実行され得ます。base／before側validatorの選択はvalidatorの自己緩和を防ぎますが、workflow fileそのものをimmutableまたはtamper-proofにはしません。この個人repositoryではorganization rulesetのrequired workflowをauthorityにできないため、Governance workflowを変更するPRは単一operatorが差分とcheck sourceを明示確認します。required checkはevent時点のsnapshotであり、`main`と`dev`を跨ぐ原子的なlockでもありません。試行中は単一operatorと明示freezeをauthorityとします。最終squash commitのmessageはmerge時に作られるため、release PR bodyを事前authority、`main` push検査を事後auditとして扱います。

## 正本と証拠

| 情報 | 正本 |
|---|---|
| 永続要件 | `spec/requirements/requirements.json` |
| 人向け要件 | `docs/requirements/REQUIREMENTS.md`（生成） |
| 実装由来設計 | `docs/design/generated/`（生成） |
| 長期判断の理由 | `docs/decisions/` |
| check定義 | `governance/checks/catalog.yaml` |
| 変更時点のreview判断 | `governance/reviews/<change-id>.yaml` |
| 変更概要と影響判定 | Git commit message |
| test・build・scan結果 | GitHub Actions等の外部サービス |
| 将来作業 | Issue |

変更ごとの計画、implementation log、test report、CI生ログを重複保存しません。一時実行状態が必要な場合だけ`.devflow/run/`を使用し、Git管理しません。

## 要件と設計

要件分類は[要件分類標準](../standards/REQUIREMENT-CLASSIFICATION.md)を正とします。外部挙動、業務ルール、受入条件、非機能制約、権限、恒久的なproject義務が変わる場合だけ要件正本を更新します。

具体的なtechnology、architecture、tool、path、process、工程、成果物が依頼に含まれるだけでは要件影響ありとしません。underlying outcome、quality threshold、exact choiceの必要性とauthority、lifetime、scopeを判定し、可逆な実装選択は実装、長期判断はADR、実装済み構造は生成設計、下位拘束は親判断へtraceしたderived requirementへ置きます。

コードや宣言から生成できる情報を手書き設計として複製しません。as-built生成・実装・test規約は[as-built設計標準](../standards/AS-BUILT-DESIGN.md)を参照し、コードだけでは理由が分からない長期判断だけをADRにします。

## Review結果

`governance/reviews/<change-id>.yaml`には選択されたcheckだけを保存します。

- `Invariant`: trigger該当時はPass必須
- `Risk-selected`: 選択された場合だけblocking
- `Advisory`: 修正、Issue、残存リスクへ収束
- `Periodic`: 個々のPRではなく定期監査

形式と検証方法は[`governance/reviews/README.md`](../../governance/reviews/README.md)を参照してください。

## 権限と安全性

外部書込み、削除、公開、merge、production、高額操作、不可逆操作は、依頼または明示承認で与えられた範囲だけ実行します。secrets、PII、production dump、会話transcript、外部CIの生ログをコミットしません。

モデル名は文書へ固定せず、taskに必要な能力、コスト、read-only境界、検証可能性から選びます。AIの自己申告だけをPass、承認、CI結果にしません。
