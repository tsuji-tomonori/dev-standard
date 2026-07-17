# 要件定義

## 概要

OpenAI公式GPT-5.6 prompt guidanceとCodex manualに基づき、repository instructionをoutcome-firstへ簡素化し、人の介在とtoken/costを減らしながら、決定論的checklist gateと品質証跡を維持する。

## ステークホルダー

| 役割 | 関心事 | 承認責任 |
|---|---|---|
| requester/repository owner | 自律性、品質、cost、PR | 本要件と実行計画の初回承認 |
| Codex root agent | 実装経路の裁量、明確な停止条件 | 承認なし。計画内実行責任 |
| read-only reviewers | 独立品質検査、低cost | 承認なし。所見のみ |

## 機能要件

| ID | 要件 | 優先度 | 受入基準 |
|---|---|---|---|
| LA-001 | AGENTSとgovernance skillをoutcome-firstに簡素化する | Must | outcome、成功条件、権限境界、証跡、停止条件を残し、重複手順を削減 |
| LA-002 | 初回承認後は計画内の設計・実装・検証・PRを追加確認なしで継続する | Must |既存single authorization testとpolicy validationが成功 |
| LA-003 | root agentの実装上の創造的裁量を保持する | Must | root model/effortを固定せず、手順ではなく判断基準を記述 |
| LA-004 | reviewerを最小costのCodex対応modelへ設定する | Must | 全custom reviewerが`gpt-5.6-terra`、役割別`low`/`medium`/`high`、low verbosity |
| LA-005 | checklist品質をprompt量から分離する | Must | 1,740-item catalogを維持し、current phaseだけを読むpolicyとfull auditを保持 |
| LA-006 | 公式指針、model routing、回帰checklistを文書化する | Must | `docs/AI-OPERATING-POLICY.md`に公式sourceとlean regression checklistがある |
| LA-007 | GitHubへbranchを公開しPRを作成する | Must | PR URL、差分、GitHub checksをrelease evidenceへ記録 |

## 非機能要件

| ID | 品質特性 | 測定方法 | 合格閾値 |
|---|---|---|---|
| LAN-001 | prompt efficiency | custom agent instruction長と重複確認 | 各developer instructions 900文字以下、同一ruleの不要反復なし |
| LAN-002 | cost control | config/model test | reviewersはterra、max threads 3以下、depth 1、max/xhigh/proを既定不使用 |
| LAN-003 | quality preservation | unit/repository/audit verification | 全test、validator、catalog、audit成功 |
| LAN-004 | traceability | 要求から実装・test・evidenceへの対応 | LA-001〜007が未接続0 |

## データ・法令・倫理要件

新しい個人data、secret、外部customer data、training/RAG dataを扱わない。公式公開文書の要約だけをrepositoryへ記録し、長文転載をしない。低cost化は安全・権限・証跡を弱める理由にしない。

## リスクとトレードオフ

- prompt削減で重要制約を落とすriskはvalidatorとregression checklistで防ぐ。
- 軽量modelでsecurity/audit品質が低下するriskはreasoning `high`と、named check failure時のun-pinned root再判定で防ぐ。
- subagent削減はwall-clock短縮機会を失うが、token/costとcontext pollutionを抑える。
- GitHub App権限が反映されない場合はrelease blockerとして残し、迂回しない。

## 対象外・N/A判断

OpenAI API呼出実装、billing実測、model training、RAG、production serving、cloud infrastructure、価格表固定、root modelの強制pinは対象外。
