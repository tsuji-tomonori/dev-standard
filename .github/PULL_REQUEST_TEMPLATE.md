## 変更内容

<!-- 何を変更したかを、意味単位で簡潔に記載してください。 -->

## 理由・利用者影響

<!-- なぜ必要か、利用者または開発者にどのような影響があるかを記載してください。 -->

## branch契約

- PR種別: `topic` / `release` / `reconciliation` / `hotfix` / `bootstrap`
- base / head:

<!-- bootstrap／activation PRだけでcommentを外す:
Branch-Policy-Bootstrap: true
Refs #20

activation時だけ追加し、policyとactive review YAMLだけを変更して全項目を一度ずつ列挙する:
Trial-Activation: true
Activation-Check: dev-created-from-current-main
Activation-Check: main-and-dev-rulesets-configured
Activation-Check: required-checks-configured
Activation-Check: squash-message-title-and-description
Activation-Check: open-pr-12-migrated
Activation-Check: dev-tree-equals-main-before-activation
Activation-Check: branch-graph-regression-passed
Activation-Check: single-release-operator-confirmed
-->

<!-- release／hotfix PRだけでcommentを外し、直近reconciliationより後のreviewを指定する:
Release-Type: regular | hotfix
Release-Review: governance/reviews/CHG-....yaml
Included-PRs: #...
Closes #...

rollback hotfixだけ追加する。policyとactive review YAML以外を混在させない:
Trial-Rollback: true
-->

<!-- reconciliation PRだけでcommentを外す:
Reconciliation-Type: bootstrap | release | hotfix
Source-PR: #...

hotfixがmain -> devでconflictする場合だけ、freeze中のdevからreconcile/hotfix-*を分岐し、
current mainをmergeして競合解消したheadからdevへPRを作る。oursでhotfixを捨てない。
-->

## 含まれるPR

<!-- release PRだけ記入。topic PRでは対象IssueをRefs #...で参照する。 -->

## 要件・設計影響

<!-- release PRでは含まれる変更全体を集約する。 -->

## 互換性・rollback

<!-- release PRでは互換性、migration、rollback方法を集約する。 -->

## 残存リスク

<!-- advisory、未検証環境、既知制約を記載する。 -->

## 変更証跡

- 実行profile: `direct` / `assured` / `regulated`
- 選択理由:
- Review YAML: `governance/reviews/<change-id>.yaml`
- Requirements: `REQ-...` / `none`
- Design-Impact: `none` / `generated` / `adr` / `contract` / `governance` / `mixed`
- 生成設計 / ADR:

- [ ] Commit Commentに目的、変更内容、要件影響、設計影響、review YAML path、検証契約、残存riskを記載した
- [ ] 選択したcheckだけをreview YAMLへ保存し、未選択checkをN/Aとして登録していない
- [ ] CIの生ログやtest reportをrepositoryへ複製していない
- [ ] PR head evidenceとsynthetic merge resultの両方を検査する

## 選択checkと検証

- 変更範囲のtargeted check:
- repository検証: `make verify`
- 外部CI: GitHub Actionsの現在HEAD結果を参照

未選択checkをN/Aとして列挙しない。CI logとtest report本文を貼り付けない。

## 権限境界

- 外部書込み・production・削除・公開・merge・高額操作: あり / なし
- 必要な承認と記録:

公開API変更だけでは承認を必須にしない。required checkを`main`と`dev`を跨ぐ原子的なrelease lockとは扱わない。

## Regulatedの場合のみ

<!-- direct / assuredでは記入不要です。 -->

- 作業項目:
- 現在または最終phase:
- 明示承認の記録:
- [ ] 必要なlifecycle文書、hash chain、phase gate、regulated auditが現在の変更と整合している
