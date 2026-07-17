# 詳細設計

## インターフェース

skill metadataはfeature、fix、refactor、design concern、failing behavior、incomplete ideaをtriggerに含む。bodyはpreflight、intake、authorization、delivery、safetyの順である。

## データモデル

full modeは既存work item schema。lightweight modeはrequest、requirements/plan、design/risk、implementation、test/security、release/retrospectiveのMarkdown set。

## 制御・状態・例外

runtime detectionでmode選択。setupはlocal repair、missing runtimeはfallback、missing external writeはpublication blocker。routine decisionはagent default、consequential ambiguityのみ質問する。

## 認証・認可・入力検証

repository instruction/configをreadしてから変更し、global/home write、silent overwrite、merge/deployを禁止する。authorization decisionは明示natural languageのみ。

## 観測可能性

progress update、work evidence、test output、PR/CI statusを保持する。利用者にはcommandでなくoutcomeとblockerを通知する。

## 移行・互換性

既存full flowとPython runtimeは互換維持。chat-first profileはumbrella/listeningだけをcopyでき、full profileは自動的に新skillを含む。
