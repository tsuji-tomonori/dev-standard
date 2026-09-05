# 実行profileの四軸

実行規模を一つの段階値に畳み込まず、次を独立に決めます。

| 軸 | 値 | 判断対象 |
|---|---|---|
| scope | local / module / repository | 読取・変更・機能検証の広さ |
| assurance | standard / elevated / critical | 失敗影響に対して必要な保証の深さ |
| compute | economy / standard / capable と reasoning effort | 意味判断に必要な計算資源 |
| mode | direct-edit / agent / agent-with-review | 実行と独立reviewの構成 |

高リスクはscopeを広げる理由ではありません。認可の一行修正は`local + critical`、全体の機械的renameは`repository + standard`になり得ます。

## 決定特徴

- scope: 明示path、想定ファイル数、module・domain数、依存metadata、契約影響
- assurance: risk tag、成果物、外部副作用、不可逆性、データ分類
- compute: 機械的変更か意味判断か、制約間相互作用、失敗した試行の具体的証拠
- mode: assurance floor、独立reviewの必要性、作業の分割可能性

検証集合は`scopeの機能検証 ∪ assuranceの追加検証 ∪ 成果物固有検証 ∪ risk固有検証 ∪ 受入条件 ∪ 対象repositoryが明示したgate`として決定的に導出します。特定のhost、CI、branch、merge設定を暗黙のgateとして追加しません。追加探索はblocking集合へ混ぜず、任意diagnosticとして分離します。

confidenceはモデルの自己申告値ではありません。`deterministic-features-v1`が観測できた特徴をlow／medium／highへ分類し、校正済みrouterを導入するまでは`score=null`とします。

この四軸は初期profileを表します。実行中の拡張では、初期`mode`を`review`へ分解し、任意diagnosticを`verification`として独立に追跡するため、`scope`、`assurance`、`verification`、`review`、`compute`の五つを拡張controlとして扱います。scopeまたはassuranceの変更に伴う検証projectionの再導出は従属計算であり、別軸を暗黙に引き上げる判断ではありません。

## 計測runnerを使う場合の手順

計測・診断・厳密な実行profileを依頼された場合だけ適用する。

### Workflow

1. 通常ルートの依頼情報と決定的metadataから四軸を独立に推定する。結果を変える不明点だけmetadata probeを最大一回使う。
2. assurance下限はrisk tagと成果物tagの和集合から導出する。重大riskだけを理由にscopeを広げない。
3. confidenceは観測特徴による`low / medium / high`と根拠を記録し、校正済みrouterがない間はscoreを`null`にする。
4. blocking検証は、scope、assurance、成果物、risk、受入条件、対象repositoryが明示したgateの決定的な和集合と完全一致させる。追加探索は別の任意diagnosticとして扱う。
5. 初期判断を覆す新証拠がある場合だけ、一回の判断につき一軸を拡張する。同一のstable failure identityが戻った場合は回数ではなくstagnationとして止める。
6. 拡張は直前eventのdigestを含むchainにする。成功時は選択検証、assurance、selection、全拡張chainを結ぶ停止digestを作る。
7. stateまたは出力を明示的に保存するときは、観測したbyte digestを使うatomic compare-and-swapで競合を拒否する。
8. 成功条件と選択検証を満たしたら、確定処理以外の正のコスト活動を止める。

一時状態は再開が必要な場合だけ`.devflow/run/`へ置く。計測機能を明示的に使う場合のfield定義は[measurement-contract.md](measurement-contract.md)に限定し、通常依頼の前提にしない。


compute profileのtier・effort名は任意runner内の診断分類であり、特定の最新モデルへ同名の推論設定を強制するものではない。実際のモデル設定はhostが所有し、必要時に対象課題で評価する。
