# リリース判定

## リリース対象

chat-first skill、root/lifecycle instruction、copy-only docs、manifest profile、validator/tests、work evidenceを[PR #2](https://github.com/tsuji-tomonori/dev-standard/pull/2)に含めた。initial remote headは`03ebc8fc425740bbfb93d0b983fc17b493eba751`。

## 受入条件の充足

CHAT-001〜007、CHAT-N1〜N4、26 tests、skill validation、validator、catalog、auditを満たした。GitHub Actions Governance run 29579216204はsuccess。

## 未解決Issue・例外承認

なし。failed check、stale authorization、例外承認なし。

## デプロイ・ロールバック

feature branchとready PRを作成した。mergeは対象外。rollbackはPR closeまたはrevert commit。

## 利用者・運用者への通知

PR bodyとREADMEで「copyして自然言語で相談」の利用方法、one authorization、automatic setupを通知した。

## Go / No-Go判断

**Go for review.** local/remote gateはgreen。最終証跡commit後のCI成功を確認する。
