# リポジトリ指示

## 目的

このリポジトリは、他のリポジトリへ移植するSkills、agents、標準、schema、generator、check、templateの参照集である。このリポジトリ自身を変更するときは、最初に`$maintain-reference-repository`を適用する。

## 既定フロー

feature、fix、refactor、設計相談は`$chat-first-development`を入口にする。

1. `$right-size-execution`で`direct`、`assured`、`regulated`を選ぶ。
2. 要件、設計、配布、互換性、権限への影響を判定する。
3. 永続要件が変わる場合だけ`$maintain-canonical-requirements`を使う。
4. 変更に必要なcheckだけを選び、実装と対象検証を行う。
5. 対応実装では`$generate-implementation-design`でas-built設計を生成する。
6. `governance/reviews/<change-id>.yaml`へselected check結果を保存する。
7. `$japanese-git-commit-gitmoji`でCommit Commentを作り、`.github/branch-policy.json`に従うbaseへPRを作成し、現在HEADのCI結果を確認する。

詳細は`docs/reference/development.md`を参照する。

## 二層branch試行

このrepository自身はIssue #20の2 release試行として、`main`を利用者向けrelease履歴、`dev`を未release統合先とengineering historyに使用する。導入直後は`bootstrap` phaseであり、`.github/branch-policy.json`のactivation requirementsと外部GitHub設定を満たすまで`dev → main` releaseを開始しない。activation PRはpolicy phaseと対応するactive reviewだけを変更し、全`Activation-Check`を記録し、`Reconciliation-Type: bootstrap`で`dev`へ伝播する。bootstrap中はtopic mergeと通常releaseを拒否し、`main`への補正は同じreconciliation種別で同期する。

`trial` phaseでは通常topicを`dev`から分岐して`dev`へmerge commitで統合し、通常releaseは`dev → main`をsquashした直後に`main → dev`をmerge commitでreconciliationする。

- 最初の小さな変更を1回目のrelease dry runとする。
- `main`または`dev`への削除・force pushを行わない。
- release中は単一operatorが`dev`をfreezeし、reconciliation完了後にだけ解除する。
- 通常release後は`main`が`dev`の祖先であり、両tip treeが一致することを確認する。
- hotfix後はancestor回復を必須とするが、未release変更があるためtree一致は要求しない。
- hotfixが`main → dev`でconflictする場合だけ、freeze中の`dev`から`reconcile/hotfix-*`を作り、current `main`をmergeして明示解消したheadから`dev`へ統合する。outer mergeは解消済みtreeを保持し、`ours`等でhotfixを捨てない。
- 詳細commitは次回release PRのcommit一覧へ残り得る。受入条件は既出file差分が再出現しないことと、詳細commitが`dev`から到達可能なことである。
- topic PRでは`Refs #...`、利用者へ提供する`main`へのrelease PRでIssueをcloseする。
- 試行停止時はpolicyとactive reviewだけを変更する`Trial-Rollback: true` hotfixを`main → dev`までreconciliationし、bootstrapへ戻して新規topic統合を停止する。
- Governance workflow変更ではbase側validator、GitHub Actions由来check、required jobの維持を明示確認し、workflow file自体をtamper-proofとは扱わない。
- 2回の試行中は`.github/branch-policy.json`の`trial.phase`以外を変更しない。契約変更はtrialを停止して別判断とする。
- このbranch戦略をportable Skillやdistribution profileへ既定配布しない。

## 正本

- 永続要件: `spec/requirements/requirements.json`
- 人向け要件: `docs/requirements/REQUIREMENTS.md`（生成物）
- 要件分類: `docs/standards/REQUIREMENT-CLASSIFICATION.md`
- as-built設計標準: `docs/standards/AS-BUILT-DESIGN.md`
- 生成設計: `docs/design/generated/`
- 長期判断: `docs/decisions/`
- check定義: `governance/checks/catalog.yaml`
- review結果: `governance/reviews/<change-id>.yaml`
- Commit Comment形式: `docs/reference/commit-message.md`
- repository固有branch契約: `.github/branch-policy.json`
- 二層branch判断: `docs/decisions/ADR-0002-two-layer-branch-history.md`

同じ現在状態を複数の手書き文書へ複製しない。

## 実行プロファイル

- `direct`: 局所的、可逆、外部副作用なし。対象test、build、lint、type、driftを実行する。
- `assured`: 公開契約、DB、IaC、dependency、共有UI、generator、要件、governance、distributionに影響する。関連するRisk-selected checkを追加する。
- `regulated`: 認証・認可、PII、データ損失、不可逆production操作、法令・契約統制、高額操作、明示的な高保証要求に使用する。

## 記録と境界

すべての変更で、実際の成果物、Commit Comment、review YAML、外部CI結果を残す。CIの生ログやreport全文をGitへ複製しない。

通常変更で恒久的な`work/<id>/`、実行計画、implementation log、test reportを作らない。一時状態が必要な場合だけgitignoreされた`.devflow/run/`を使い、完了後に削除する。

- secrets、PII、production dump、会話transcriptをコミットしない。
- 明示権限なしにproduction deploy、削除、公開、merge、高額操作を行わない。
- 対象リポジトリ固有のbuild、test、ownership、security、commit規約を維持する。
- gateを通すためにtest、型、lint、security controlを弱めない。
- モデル名を文書へ固定せず、必要能力、コスト、read-only境界から選ぶ。
