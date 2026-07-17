# 実装・構成管理記録

## 変更概要

adversarial-validation skill、research basis、attack playbook、report template、UI metadataを追加。Skills catalogとinventory validatorを追加し、AGENTS/chat-first/README/INSTALLATION/manifest/testsへ統合した。

## 要求・設計との対応

| 変更 | 要求ID | 設計節 | コミット | レビュー |
|---|---|---|---|---|
| adversarial skill/references | ADV-001〜007 | architecture/workflow | current branch | quick/contract validation |
| Skills catalog | ADV-008 | ADR-004 | current branch | set equality validator |
| integration/tests | ADV-N1〜N4 | decision/safety rules | current branch | full regression |

## セキュア実装・依存関係

runtime dependencyなし。attack execution codeやexploit artifactは含めず、defensive methodとsafe boundariesだけを配布する。

## 設計との差異

自己敵対的検証でchat-first skillから新skillへの参照に対し、chat-first配布profileの依存漏れを検出した。profile、guide、catalog、install testを修正した。source selectionはsoftware property/metamorphic/mutationとAI red-team/agent/judge/taxonomyをbalanceした。

## 実行したローカル検査

28 tests、repository validator、skill quick validation、compile、diff checkをsuccess。
