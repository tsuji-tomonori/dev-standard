# 要件定義

## 概要

repository一式またはdocumented copy setをtargetへcopyした後、利用者は自然言語で目的や困りごとを相談するだけとする。AIがpreflight、依存導入、work item初期化、要件整理、初回承認、設計、実装、test、PR、CI、closureを担う。

## ステークホルダー

| 役割 | 関心事 | 承認責任 |
|---|---|---|
| requester | command不要、曖昧な相談から完成まで | 要件・実行計画への一度の自然言語承認 |
| AI agent | 安全な自動導入と工程実行 | gate証跡と権限境界の遵守 |
| target maintainer | 既存構成の保護とreview可能なPR | merge判断 |

## 機能要件

| ID | 要件 | 優先度 | 受入基準 |
|---|---|---|---|
| CHAT-001 | 自然言語の開発相談でflowを自動開始する | Must | command名やskill名の指定なしでumbrella skillが発火する |
| CHAT-002 | AIが導入状態を自動preflight/bootstrapする | Must | runtime、依存、Git状態を確認し、安全な不足だけを内部で準備する |
| CHAT-003 | AIが曖昧な相談を要件・受入条件・実行計画へまとめる | Must | 必要最小限の対話後に一つの承認packageを提示する |
| CHAT-004 | 承認後に設計からPR/CI/closureまで自動実行する | Must | routine commandや工程承認を利用者へ求めない |
| CHAT-005 | copy-only導入経路を明記する | Must | copy setとcopy後の最初のchat例がREADME/guideにある |
| CHAT-006 | target固有fileを保護する | Must | active configや既存instructionのsilent overwriteを禁止する |
| CHAT-007 | 決定論的gateを維持する | Must | existing catalog、authorization digest、audit、testsが成功する |

## 非機能要件

| ID | 品質特性 | 測定方法 | 合格閾値 |
|---|---|---|---|
| CHAT-N1 | Usability | user-facing quick start | Python/shell commandを要求しない |
| CHAT-N2 | Autonomy | skill/instruction contract test | AI-owned stepsが明記される |
| CHAT-N3 | Safety | bootstrap boundary test/static validation | destructive/global/active-config overwriteなし |
| CHAT-N4 | Portability | copy map validation | sourceとtarget pathが明確で自己完結する |

## データ・法令・倫理要件

新しいpersonal data、secret、外部telemetryを扱わない。質問は実装結果や権限境界を変える不足情報に限定し、推測可能な可逆判断はAIが明示的に採用する。

## リスクとトレードオフ

内部Pythonを削除するとhash/gateの信頼性が落ちるため維持する。一方、利用者操作からは隠し、AIが実行・修復する。完全無承認ではなく、既存方針どおり要件と権限境界に一度だけ自然言語承認を得る。

## 対象外・N/A判断

GUI installer、global personal skill install、全AI製品共通package、production deploy/mergeは対象外。
