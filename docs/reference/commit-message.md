# コミットメッセージ契約

このリポジトリでは`Commit Comment`と呼びますが、Gitの正式名称はcommit messageです。変更ごとの別manifestや実装reportを作らず、最終コミットへ影響判定と検証契約を集約します。

## 形式

```text
<gitmoji> <type>(<scope>): <日本語の要約>

目的:
- <得られる結果>

変更内容:
- <主要変更>

要件影響:
- あり | なし
- 要件ID: <REQ IDs | none>
- 理由: <判定根拠>

設計影響:
- あり | なし
- 対象: <生成設計、ADR、公開契約、構成 | none>
- 生成設計: <path | 対象外>
- ADR: <ADR ID | 不要とした理由>

チェックリスト:
- governance/reviews/<change-id>.yaml

検証契約:
- GitHub Actions: <workflowまたはrequired check>
- ローカル: <必要時だけ>
- 結果の正本: GitHub Actions等

互換性・残存リスク:
- <互換性、移行、未検証範囲、既知制約>

Requirements: <REQ IDs | none>
Design-Impact: <none | generated | adr | contract | governance | mixed>
Review-Checklist: governance/reviews/<change-id>.yaml
Refs: <Issue / ADR。該当時だけ>
```

## 規則

- 1行目は一つの主目的を表す。
- 要件影響と設計影響は必ず判定し、`なし`でも理由を書く。
- 変更内容は意味単位に絞り、ファイル一覧や作業ログを貼らない。
- CIが完了する前にPassと書かず、実行されるworkflowまたはrequired checkを記載する。
- 生ログ、coverage全文、scanner出力を貼らない。
- `fixup!`、`squash!`、WIP、tmp等の一時subjectをprotected branchへ残さない。
- 通常topic commitのsubjectはGitmoji、Conventional Commit、日本語要約を使用する。

## 二層branchでのauthority

| 対象 | 保持する情報 |
|---|---|
| topic PRの最終head commit | 上記の完全なCommit Commentとreview YAML参照 |
| topic PR内の中間commit | Gitmoji、Conventional Commit、日本語要約によるengineering history |
| `dev`上のtopic merge commit | PR統合を示すtopology marker。新しい正本を持たない |
| release PR body | 含まれるPR、要件・設計影響、互換性・rollback、残存riskを集約した事前manifest |
| release review YAML | releaseで選択したcheck結果 |
| `main`上のsquash commit | release manifestの永続的な索引として完全なCommit Commentを保持する |
| reconciliation merge commit | ancestor関係を回復するtopology marker。機能変更を混在させない |

`dev`向けtopic PRではIssueを利用者へ提供済みと扱わないため`Refs #...`を使用します。Issueをcloseするのは通常`main`へのrelease PRです。

## release PRの必須情報

release PR bodyには次のmarkerと見出しを含めます。

```text
Release-Type: regular | hotfix
Release-Review: governance/reviews/CHG-....yaml
Included-PRs: #101, #102
Closes #201

## 含まれるPR

## 要件・設計影響

## 互換性・rollback

## 残存リスク
```

通常releaseでは`Release-Type: regular`、hotfixでは`Release-Type: hotfix`を使用します。`Included-PRs`と「含まれるPR」見出しには少なくとも一つのPR番号を含め、release PRと最終squash commitは少なくとも一つのIssueを`Closes`、`Fixes`、`Resolves`等でcloseします。release reviewは直近reconciliationより後に作成または更新し、過去releaseのreviewを誤流用しません。release reviewの`impact_flags.squash`は`true`とし、squash releaseを評価するreviewであることをvalidatorが検査します。最終squash commitには同じmarker、必須4見出し、Issue closing keywordに加えて同じpathの`Review-Checklist`を残し、push auditとreconciliationがrelease manifestを検証できるようにします。

reconciliation PR bodyには次を含めます。

```text
Reconciliation-Type: bootstrap | release | hotfix
Source-PR: #<mainへ統合したPR>
```

`bootstrap`はbootstrap中の`main`補正または`phase: bootstrap`から`phase: trial`への有効化commitを`dev`へ伝播するときに使用します。通常releaseとhotfixではそれぞれ`release`、`hotfix`を使用します。hotfixが`main → dev`でconflictする場合だけ、freeze中の`dev`から`reconcile/hotfix-*`を分岐し、current `main`をmergeして明示解消したheadから`dev`へPRを作ります。解消済みtreeをouter mergeで変えず、`ours`相当でhotfixを破棄しません。

導入／activation PRには次のmarkerを使用します。activation時はpolicyと対応するactive review YAMLだけを変更し、policyに列挙された全`Activation-Check`を一度ずつ記載して最終squash commitにも保持します。

```text
Branch-Policy-Bootstrap: true
Trial-Activation: true
Activation-Check: <activation requirement>
Refs #20
```

trialを停止するrollback hotfixではpolicyと対応するactive review YAMLだけを変更し、`Trial-Rollback: true`をrelease PR bodyと最終squash commitへ記録します。続く`Reconciliation-Type: hotfix`で`dev`へ伝播するまでrollback完了と扱いません。

最終squash commitはmerge時に作成されるため、PR required checkだけでcommit objectを事前保証できません。release PR bodyとrelease reviewを事前authorityとし、`main` push時のCommit Comment検査を事後auditとして扱います。
