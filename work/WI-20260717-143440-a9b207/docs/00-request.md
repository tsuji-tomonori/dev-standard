# 要求受付

## メタデータ

- Work item: WI-20260717-143440-a9b207
- タイトル: 永続要件・実装由来設計・標準検証フレームを追加
- 作成日時: 2026-07-17T14:34:40Z
- 要求者: tsuji-tomonori
- 対象プロファイル: CORE, CLOUD-COMMON, AWS-DELTA

## ユーザー原文

workを対話断片と工程証跡に限定し、永続的な原子要件の正本と自動生成docsを設ける。FastAPIとCDKを対象に実装と1対1の詳細設計を生成し、router.pyからsequence、OpenAPIからIF/API、raw SQLのASTからCRUD/query objects、CloudFormation YAMLからresource/parameter docsを生成する。SWEBOKとクラウドベンダー公式best practicesのversioned checklistで要件・設計・実装を検証する。現状を点検し、3本柱へ再構成してPRを作る。

## 目的・期待する成果

本repositoryを、永続要件の発見・保守、実装と1対1の派生設計、国際標準・vendor best practicesによる品質検証の3本柱へ再構成する。

## 対象範囲

永続する機械可読要件正本、自動生成docs、FastAPI/CDK設計生成器、標準台帳と鮮度検査、3 Skills、配布profile、tests、PR。

## 対象外

FastAPI/CDK以外のframework固有生成、database実行、cloud deploy、既存checklist全項目の再執筆。

## 制約・前提

`work/`は会話断片・変更理由・工程証跡であり正本ではない。利用者はfolder copy後に自然言語で相談するだけとし、内部commandはAIが所有する。

## 受入条件

- [ ] `spec/requirements/requirements.json`が永続要件の唯一の正本になる
- [ ] 1要件1義務を構造検査し、add/update/retireをrevision競合付きで原子的に適用できる
- [ ] `docs/requirements`を正本から生成し、driftをCIで検出できる
- [ ] FastAPI router/OpenAPI/raw SQLとCDK CloudFormationから指定設計を生成できる
- [ ] source digestとtraceにより生成設計と実装の1対1対応を検査できる
- [ ] SWEBOK・AWS・Azure・Google Cloud・OCIの公式参照版と鮮度を台帳管理できる
- [ ] 3 Skillsとprofileをcopyすればチャットだけで運用できる
- [ ] local/remote CIが成功する

## 未解決質問

- なし。3本柱、初期framework範囲、生成元と生成物が明示済み。
