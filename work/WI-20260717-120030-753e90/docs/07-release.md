# リリース判定

## リリース対象

chat-first skill、root/lifecycle instruction、copy-only docs、manifest profile、validator/tests、work evidenceを新規PRに含める。

## 受入条件の充足

local CHAT-001〜007、CHAT-N1〜N4、26 tests、validator、catalog、auditを満たし、remote PR/CIを最終確認する。

## 未解決Issue・例外承認

なし。remote publication pending。

## デプロイ・ロールバック

feature branchとready PRを作成。mergeは対象外。rollbackはPR closeまたはrevert commit。

## 利用者・運用者への通知

PR bodyとREADMEで「copyして自然言語で相談」の利用方法、one authorization、automatic setupを通知する。

## Go / No-Go判断

local Go、remote PR/CI pending。
