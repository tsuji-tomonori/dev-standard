# 要求受付

## メタデータ

- Work item: WI-20260717-lean-autonomy-model-routing
- タイトル: Lean promptと低コストmodel routing
- 作成日時: 2026-07-17T03:41:16Z
- 要求者: requester
- 対象プロファイル: CORE, AI-CONDITIONAL

## ユーザー原文

https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.6#prompting-best-practices をもとに、人の介在を最小化し、指示過多でAIの独創性を減らさず、適切なチェックリストを維持し、必要最小限の安価で軽量なモデルを使う設定へ変更してPRを作成する。承認済み。

## 目的・期待する成果

OpenAI公式GPT-5.6指針に合わせてpromptとmodel routingを簡素・低cost化し、初回承認後の自律実行と決定論的品質統制を両立したPRを作成する。

## 対象範囲

AGENTS、governance skills、Codex custom agents/config、AI運用方針、validator、tests、work item evidence、GitHub PR。

## 対象外

OpenAI API application実装、課金実測、model training/RAG、cloud runtime、root modelの一律pin、branch protection変更。

## 制約・前提

公式文書を正本とする。安全・権限・証跡をcost削減の対象にしない。既存single authorizationと1,740-item catalogを維持する。

## 受入条件

- [ ] outcome-first prompt、terra reviewer routing、役割別effort、prompt/checklist分離がtestで検証される
- [ ] full verificationとGitHub checksが成功し、PR URLが記録される

## 未解決質問

- なし。model availabilityの差異はCodex manualをproject configの正本として扱う。
