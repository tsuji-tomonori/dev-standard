# 振り返り・改善

## 成果と計画差

ユーザーの短い訂正から、security red teamingと批判的レビューの語義差をSkill名・trigger・workflowへ反映した。

## 有効だった統制

ユーザー原文を正本化し、旧security語彙をnegative assertionで検査したこと。

## 手戻り・ゲート失敗・見逃し

初版が`adversarial`をsecurity文脈へ過度に寄せ、ユーザーの「正しさを疑うレビュー」という核心を外した。

## 根本原因

用語の一般的な技術用法を優先し、ユーザーが置いた文脈上の意味を要件として十分に固定しなかった。

## 改善提案

| 対象skill/ルール | 変更案 | 根拠 | リスク | 承認状態 |
|---|---|---|---|---|
| calibrated listening | 多義語は対象・目的・非対象の三点で固定する | 今回の語義ずれ | 質問過多 | future proposal、未承認 |

## 次回確認方法

trigger description、forbidden security vocabulary、perspective/independent evidence assertionsを再実行する。
