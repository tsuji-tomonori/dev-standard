# 要求受付

## メタデータ

- Work item: WI-20260717-portable-reference-layout
- タイトル: Portable skills and agents reference layout
- 作成日時: 2026-07-17T11:40:23Z
- 要求者: requester
- 対象プロファイル: CORE, AI-CONDITIONAL

## ユーザー原文

leanという用語が難解または誤解を招くなら削除する。.agents/skillsと.codex/agentsを現在の標準に合わせ、このrepositoryを他repositoryへ移植しやすいskills/agents集として整理し、どこをどのようにcopyするか明記する。

## 目的・期待する成果

公式標準に沿うskills/agents reference repositoryへ整理し、他repositoryへの安全で簡単な移植方法を提供する。誤解を招く`lean`用語は現行文書・設定から除く。

## 対象範囲

`.agents/skills`、`.codex/agents`、Codex config、README、移植guide、distribution manifest、installer、validator、tests、PR更新。

## 対象外

historical work itemの改ざん、skills format変更、custom agent format変更、target repository既存fileの無断上書き、plugin packaging。

## 制約・前提

公式Codex manualをdirectory standardの正本とする。既存skills/agentsのbehaviorとsingle authorization controlsを維持する。

## 受入条件

- [ ] `.agents/skills`と`.codex/agents`の役割とcopy destinationが明記される
- [ ] selected profileをdry-run/applyできるinstallerとmanifestがtestされる
- [ ] current user-facing文書・validatorから曖昧な`lean`用語が除去される
- [ ] PRとGitHub Actionsが更新される

## 未解決質問

- なし。current standardに従い`.agents/skills`と`.codex/agents`を維持する。
