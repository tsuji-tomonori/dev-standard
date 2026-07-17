# 要求受付

## メタデータ

- Work item: WI-20260717-120030-753e90
- タイトル: Chat-first zero-setup autonomous development
- 作成日時: 2026-07-17T12:00:30Z
- 要求者: requester
- 対象プロファイル: CORE, AI-CONDITIONAL

## ユーザー原文

フォルダをコピーし、自然言語で相談するだけで、AIが仕組みを自動導入し、要件整理、設計、実装、テスト、PR作成までフローに乗せる。利用者にPython commandを実行させない。

## 目的・期待する成果

利用者が開発用commandやgovernance内部構造を学ばず、自然言語の相談だけでAIが要求の言語化からPR作成までを一貫実行できる配布形態と操作契約を提供する。

## 対象範囲

root instructions、chat-first umbrella skill、copy-only導入guide、distribution manifest/snippet、validator、tests、README、既存lifecycle skillの内部実行規約、PR作成。

## 対象外

Python harnessの削除、初回の実行承認廃止、production操作、target固有configの無断上書き、PR merge。

## 制約・前提

PythonはAI内部の決定論的gateとして利用できるが、利用者へcommand実行を求めない。copy後にAIが不足依存・runtime・work itemを自動検出して準備する。

## 受入条件

- [ ] 利用者向けquick startが「copyして自然言語で相談」のみになる
- [ ] 通常の開発相談でchat-first skillが発火し、AIがbootstrapと全工程を内部実行する
- [ ] 初回承認だけは自然言語で取得し、以降はPR作成とCI確認まで自走する
- [ ] target固有fileを無断上書きせず、安全な自動導入と検証が行われる

## 未解決質問

- なし。既存single-authorization boundaryを維持し、操作面だけをchat-first化する。
