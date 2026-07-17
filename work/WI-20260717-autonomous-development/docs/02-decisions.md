# 意思決定記録

- 記録日: 2026-07-17
- 要求判断: tsuji-tomonoriによる初回承認
- 設計判断: 承認済み要件と実行計画に基づきCodexが権限境界内で実施

## ADR-001 人の判断をrequirementsへ一回だけ集約する

- 状態: 採用
- 文脈: 工程ごとの承認待ちはAI開発の連続性を損なう。一方、品質ゲートまで削除すると無断変更を検出できない。
- 決定: requirementsの要件、初期トレーサビリティ、実行計画、checklist digestへrequesterの明示判断を一件だけ結び付ける。後続は機械検査のみとする。
- 帰結: 初回の計画完全性が重要になる。計画変更は承認失効として停止する。

## ADR-002 全先行工程をadvanceとauditで再検査する

- 状態: 採用
- 文脈: 現行実装はcurrent phaseだけを検査し、過去成果物の改変を後工程で見逃しうる。
- 決定: current phaseより前の全gateを現在のファイルとreview結果で再計算する。
- 帰結: 実行量は増えるが、このリポジトリ規模では許容でき、改ざん・劣化検知を優先する。

## ADR-003 旧work itemを自動移行しない

- 状態: 採用
- 文脈: 旧承認は複数工程モデルの成果物を対象とし、新しい実行計画を含まない。
- 決定: workflow schemaをstateへ記録し、旧itemは明示migrate後にfresh authorizationを要求する。
- 帰結: 旧itemに一手間必要だが、承認の意味を偽装しない。

## ADR-004 Fail例外の後続承認を廃止する

- 状態: 採用
- 文脈: 初回承認後にFail受容を人へ求めると単一承認原則を破る。
- 決定: schema 2ではFailを常にblockingとし、Passまたは具体的N/Aになるまで修正する。
- 帰結: リスク受容で進む案件は、初回計画に別要件として安全策を組み込む必要がある。

## ADR-005 改善候補を自動適用しない

- 状態: 採用
- 文脈: Stop hookによる恒久指示変更は、初回計画外の権限拡張になりうる。
- 決定: retrospectiveはpending proposalだけを生成する。計画外改善は次work itemで初回承認する。
- 帰結: 自動学習速度より、instruction poisoning耐性と権限の明確さを優先する。

## ADR-006 傾聴skillを意味構造化プロトコルとして実装する

- 状態: 採用
- 文脈: 共感定型文だけでは意図理解、核心化、短文化の再現性がない。
- 決定: atomic meaning ledger、relation map、practical question、intent candidates、core proposition、clarification decision、compression、semantic checksumの順で内部処理する。
- 帰結: SKILL.mdは実行規則を中心にし、詳細手順、自然な日本語、rubric、研究根拠をreferencesへ分離する。
