# 実装・テスト・報告

## 承認範囲で完了まで

要件サマリ確認は成果・scope・仮定を揃えるための一度の確認であり、可逆なcode変更へ追加の形式的な許可を要求するものではない。確認後は実装・検証・修正を自走し、途中のstatus質問や訂正は元の目的へ取り込む。

停止する新事実: 既定値が重要要件に違反、要件矛盾、必要なデータ/権限が得られない、公開/外部送信/破壊的操作への範囲拡張、予算/期限/安全等の重要制約下で実現不能、利用者が選ぶべき価値trade-off。判明した事実、変わる要件と成果を示し、その選択だけ質問する。内部構成・命名・可逆なlibrary choiceやtest失敗の通常修正は停止理由ではない。

Dev標準導入済みならdurable deltaは`$maintain-canonical-requirements`、実装由来設計は`$generate-implementation-design`、関係検査は`$inspect-quality-gates`へ渡す。frontendは必要な場合だけ既存frontend Skillを合成する。branch・merge・CI・commit形式・PR templateを追加しない。単独contextの空repositoryにはreadiness文書の最小正本方針を適用する。

## 検証

- 各受入条件をtestへtraceする。要件ID、受入条件ID、実test path/nodeまたはprobe、command、実結果（pass/fail/未実行と理由）を結ぶ。
- 正常系だけでなく該当する異常・空・境界・permission・再起動/保持・復旧を選ぶ。上限は直前・一致・超過、権限拒否はデータ不変も検証する。
- 実testを実行し失敗を調べ、実装を修正し該当checkを再実行する。閾値や期待結果を弱めず、mockだけで実I/F成功とは言わない。
- 低影響の可逆な内部変更に実装と同形のtestを増やさない。ただし承認済み受入条件の検証を省略しない。
- 環境や権限で検証できない部分は未検証として報告し、全要件達成と称さない。残存riskと実装済み/未達を分ける。
- 新しい依存・失敗・重要riskがある場合だけ範囲を広げる。対象owned mandatory checkがあるなら実行する。
- transcript、生ログ、利用者固有情報はcommit対象にしない。必要な一時証拠はgitignoreされた`.devflow/run/`へ。

## 完了報告

実装した挙動と起動方法を先に、以下を必要な長さで示す。未実行をpassと混同しない。

```text
実装: 対象、できること、主要artifact
起動: 必要環境 / 準備command / 起動command / ローカル確認方法
要件ID | 受入条件ID | test path/node | 実行command | 実結果
REQ-001 | AC-001 | tests/test_…::… | … | pass（実測値等）
既定値・仮定: 確認時に置いた値、変更があれば理由と確認
未達・未検証: 対象と理由（なければ「なし」）
残存risk: 根拠付きの実際の制約（なければ「なし」）
Dev標準使用時: 正本generate/check、生成設計pathとdrift check結果
```

利用者は対応表で各IDの受入が実際に検証されたかを読み、仮定で意図の差を、未検証で達成主張の限界を確認する。テスト成功は本番品質や完全性の一般保証ではない。
