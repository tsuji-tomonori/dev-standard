# 統制・監査モデル

## 信頼境界

自然言語のSkillとagentは作業方法を指示します。合否判定、ハッシュ、初回承認、状態遷移は`tools/devflow.py`が決定的に実行します。AIの自己申告をゲート証跡や人の承認にしません。

実行制御の正本は`work/<id>/execution-profile.json`です。`right-size-execution`がscope、assurance、compute、mode、観測特徴に基づくconfidence、soft budget、required verification、Expand、実績、選択結果をschemaとpolicyに基づいて記録します。これは製品要件の正本ではなく、そのwork itemの実行制御台帳です。

永続要件の正本は`spec/requirements/requirements.json`です。`work/<id>/docs/01-requirements.md`は、その時点の会話から得た変更差分と承認境界であり、正本ではありません。承認後に版付き差分を正本へ適用し、`docs/requirements/REQUIREMENTS.md`を生成します。削除は履歴を残す`retire`です。

## 初回承認に結び付く成果物

要件ゲートのダイジェストは次の正規化データからSHA-256で計算します。

- work item IDと要件工程
- 要件定義、トレーサビリティ、自律実行計画のパスとSHA-256
- 要件工程の全チェック結果

要求者の初回承認はこのダイジェストを保持します。いずれかの文書または判定が変わると承認は失効します。後続の`advance`と`audit`は、初回承認と全先行工程を毎回再検査します。

初回承認は後続作業を自由に拡張する白紙委任ではありません。実行できるのは、承認済み計画に列挙した対象、操作、外部副作用、完了条件の範囲だけです。

要件定義には正本の基準版とadd/update/retire差分を含めます。正本への適用後、差分と生成結果の対応を証跡に残します。新しい要件変更は新しいwork itemと初回承認を必要としますが、承認済み差分の適用、設計、実装、検証には追加承認を求めません。

## 後続品質ゲート

アーキテクチャ以降の工程は、人の承認ではなく次の機械検査で進行を制御します。

- 必須文書の存在、実質内容、未入力token
- 各チェック項目の適用判定、案件重要度と根拠、Pass/Fail、証跡、レビュー担当、日時
- N/Aの具体的根拠、レビュー担当、日時
- FailのIssue、対応方針、是正期限。Failは後続承認で受容せず、原因を修正するまで停止する
- Fail是正後の旧判定履歴、再確認証跡、再確認者、再確認日
- 現在の初回承認
- 全先行工程の現行ダイジェスト
- profile schema、assurance floor、単軸Expandの直接証拠、予算超過、compute引上げ、選択漏れ、決定的成功後の活動

失敗を追加承認へ転嫁しません。承認済み範囲内で原因を解消します。

適正規模ポリシーはshadow modeから開始し、構造破損、改ざん、assurance floor違反だけをblockingとします。scope過不足、overrun、成功後活動、selector偽陰性は警告と計測にし、校正データとリポジトリ固有benchmarkが揃った後だけ限定blockingへ昇格します。

## チェック選択の監査

カタログ項目は`always_on`、`artifact_tags`、`risk_tags`、`assurance_levels`、`phase`を持ちます。work item初期化時にassurance、変更成果物、risk、工程、changed pathから候補を決め、selector版、入力特徴、選択ID、除外数、選択digest、除外監査sample、mandatory missを保存します。未選択は`not-selected`として扱い、実際に評価した`not-applicable`へ一括変換しません。

## 改ざん検知

`approvals.jsonl`と`events.jsonl`は、各レコードに前レコードのハッシュを含むチェーンです。途中の編集、削除、並べ替えは`audit`で検出されます。これは署名ではないため、高保証用途では署名付きコミット、保護ブランチ、外部監査ログを追加してください。

## 旧work itemの移行

workflow schemaを持たない旧work itemは停止します。`migrate`はschemaを明示更新しますが、旧承認を新しい初回承認として再利用しません。新しい実行計画を完成させたうえで、要件ゲートへ新しい初回承認を記録します。

## 自動振り返りとskill改善

停止hookはアクティブwork itemのゲート、作業ツリー、停止理由を`reports/retrospectives/`へ保存します。同じ停止理由が複数セッションで再発すると改善候補を生成します。

改善候補は自動的に恒久ルールへ昇格させません。現在の承認済み実行計画に明記された変更だけを現在のwork itemで適用できます。計画外の改善は別work itemへ分離し、その要件と実行計画に一度だけ初回承認を得ます。
