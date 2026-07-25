# コントリビューションガイド

## 変更前

このリポジトリを変更するときは[`maintain-reference-repository`](../.agents/skills/maintain-reference-repository/SKILL.md)を適用し、移植可能な資産とリポジトリ固有の一時情報を分けます。

開発契約は[`docs/reference/development.md`](../docs/reference/development.md)、Commit Comment形式は[`docs/reference/commit-message.md`](../docs/reference/commit-message.md)を参照してください。

## 基本フロー

1. `direct`、`assured`、`regulated`を選び、要件・設計・配布・互換性・authority boundaryへの影響を判定する。
2. 必要な成果物だけを変更する。永続要件が変わる場合だけ正本を更新する。
3. `governance/checks/catalog.yaml`から関連checkだけを選ぶ。
4. 変更範囲のtest、build、lint、type、生成物driftを実行する。
5. `governance/reviews/<change-id>.yaml`へselected check結果を保存する。
6. `make verify`を実行し、構造化Commit Commentでコミットする。
7. `.github/branch-policy.json`に従うbaseへPRを作成し、現在HEADのGitHub Actionsを確認する。

公開API変更は通常`assured`で扱います。認証・認可、PII、データ損失、不可逆production操作、法令・契約統制、高額操作では`regulated`を使用します。

## branch試行

Issue #20のbranch policyは導入直後に`bootstrap` phaseで開始します。同期済みでpolicy未導入の既存`dev`には、`Branch-Policy-Bootstrap: true`と`Refs #20`を持つ初回導入PRだけをmergeできます。その後、`Release-Type: bootstrap`の`dev → main` PRで同じtreeをsquashし、`Reconciliation-Type: bootstrap`で`dev`へ戻します。このbootstrap releaseはIssueをcloseせず、2回の通常releaseへ数えません。それ以外のbootstrap中topic PRと通常releaseはmergeできません。

`dev`、ruleset、required checks、squash message、PR #12移行、tree一致、回帰test、単一operatorを確認したactivation PRでだけ`trial`へ移行します。activation PRはpolicyのphaseと対応するactive review YAMLだけを変更し、全`Activation-Check`を記録します。activation後は`Reconciliation-Type: bootstrap`で`main`のpolicyとreviewを`dev`へ伝播します。`main`へ補正が入った場合も同じreconciliation種別で`dev`へ同期します。

`trial` phaseでは次のフローを使用します。

- 最初の小さなtopic変更を1回目のrelease dry runとする。
- 通常topicは`dev`から分岐し、`dev`へPRを作る。
- `dev`へのtopic統合はmerge commitを使用する。
- 通常releaseはrepositoryの`dev`から`main`へのPRだけを許可し、squash mergeする。
- 通常release直後は`dev`へのmergeをfreezeしたまま`main → dev`をmerge commitでreconciliationする。
- hotfixは`main`から`hotfix/*`を分岐し、`main`へのsquash後に`main → dev`をreconciliationする。conflict時だけfreeze中の`dev`から`reconcile/hotfix-*`を作り、current `main`をmergeして明示解消したheadから`dev`へ統合する。`ours`等でhotfixを破棄しない。
- 試行停止時はpolicyとactive reviewだけを変更する`Trial-Rollback: true` hotfixを用い、hotfix reconciliation後にbootstrapで凍結する。
- topic PRでは`Refs #...`を使用し、Issueをcloseするのは利用者へ提供する`main`へのrelease PRとする。

release PRには`Release-Type`、`Release-Review`、`Included-PRs`、Issue closing keywordと、含まれるPR、要件・設計影響、互換性・rollback、残存リスクを記載します。reconciliation PRには`Reconciliation-Type`と`Source-PR`を記載し、機能変更を混在させません。

reconciliation後も詳細commitは`dev`から到達可能であるため、次回release PRのcommit一覧へ過去commitが残り得ます。確認対象は、既出file差分が再出現しないこと、ancestor関係、通常release後のtip tree一致です。

Governance workflowを変更するPRでは、base側validatorが選択されること、required checkのsourceがGitHub Actionsであること、workflow差分がcheckを無効化していないことを単一operatorが確認します。base側validatorの選択だけでworkflow fileがtamper-proofになるとは扱いません。

## 境界

- 既存consumerのpathや配布profileを変える場合は、migrationまたは互換性を明示する。
- repository固有のbranch policyをportableなdistribution profileへ追加しない。
- 未選択checkをN/Aとして登録しない。
- CIの生ログやtest reportをコミットしない。
- secrets、PII、production evidenceをコミットしない。
- 明示権限なしにproduction deploy、削除、公開、merge、高額操作を行わない。
