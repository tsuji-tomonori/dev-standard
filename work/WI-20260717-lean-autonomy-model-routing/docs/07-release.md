# リリース判定

## リリース対象

- PR: https://github.com/tsuji-tomonori/dev-standard/pull/1
- branch: `agent/single-approval-autonomous-flow`
- remote head: `3872715d37309a57ee37b9be4792b781d08d1fdf`
- scope: single authorization flow、collaborative listening skill、lean prompt、terra routing、atomic checklist batch

## 受入条件の充足

- LA-001〜006、LAN-001〜004: local tests、validator、policy/config diffで充足
- LA-007: draft PR作成済み、Governance workflow run 29553424390 success
- local: 18/18 tests、catalog 1,740、repository validation、audit、skill validation success

## 未解決Issue・例外承認

未解決code issue、例外承認、stale authorizationなし。remote final evidence commit後に同workflowが再実行される。

## デプロイ・ロールバック

本変更のreleaseはPR merge。merge前はbranch update/PR close、merge後はrevert PR。force pushとbranch protection回避は禁止。

## 利用者・運用者への通知

PR bodyにbehavior、model routing、validation、work item、公式sourceを記載。最終check後にdraftをreadyへ変更する。

## Go / No-Go判断

**Go for ready review.** Localとinitial GitHub workflowはgreen。final evidence commitのGitHub workflow成功を確認してready化する。
