# 要求受付

## メタデータ

- Work item: WI-20260717-123310-938d42
- タイトル: Research-grounded adversarial validation skill and skill catalog
- 作成日時: 2026-07-17T12:33:10Z
- 要求者: requester
- 対象プロファイル: CORE, AI-CONDITIONAL

## ユーザー原文

敵対的検証について関連研究を調べ、研究結果に従ったSkillsを作成する。Skills一覧を作成し、PRを作成する。

## 目的・期待する成果

関連研究に根差し、設計・実装・test・AI behaviorを反証志向で検証するportable skillを提供する。repository内の全Skillsを用途・trigger・依存・copy path付きで一覧化する。

## 対象範囲

一次研究/公式資料調査、research map、adversarial validation skill、playbook/report contract、Skills一覧、root/chat flow integration、validator/tests、PR。

## 対象外

実環境への攻撃、脆弱性悪用、production data、攻撃toolkitそのものの配布、PR merge。

## 制約・前提

検証はauthorized local/test environmentに限定し、反証の不在を安全証明と扱わない。再現性と通常機能のutilityを同時測定する。

## 受入条件

- [ ] primary/official sourcesとskill設計原則の対応が文書化される
- [ ] requirements/design/code/tests/AI agentsへ適用できるadversarial validation skillが作成される
- [ ] threat model、independent oracle、attack portfolio、artifact、repair/retestを必須化する
- [ ] 全Skillsの一覧がinventoryと一致する
- [ ] PRとCIが成功する

## 未解決質問

- なし。対象はdefensive validationであり、実攻撃は許可しない。
