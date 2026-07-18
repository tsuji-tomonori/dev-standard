# AI運用方針

## 1. 目的

AIには、達成結果、絶対条件、必要な証拠、authority boundary、停止条件を渡す。可逆な実装判断はAIへ委ね、人の介在は永続要件の意味変更、外部副作用、不可逆操作、regulated案件に限定する。

## 2. 指示の構成

- 同じ指示をAGENTS、hook、Skill、policyへ重複させない。
- 作業手順より、結果、禁止事項、選択規則、証拠契約を優先する。
- 全checklistや全標準をpromptへ複製しない。
- 例は製品要件または計測済み失敗に必要なものだけにする。
- repository固有の既存指示を維持する。

## 3. 必須成果物

repository変更では次を必須とする。

1. 実際の成果物
2. 構造化Commit Comment
3. selected check result YAML
4. external CI result

恒久的なwork item、変更ごとの計画・設計・実装・test・release reportは通常作らない。

## 4. Commit Comment

Commit Commentは次を代替する。

- Change Manifest
- Requirement Impact Result
- Design Impact Result
- implementation summary

必須節:

- 目的
- 変更内容
- 要件影響
- 設計影響
- チェックリスト
- 検証契約
- 互換性・残存リスク

まだ完了していないCIをPassと記載しない。

## 5. CI結果

単体test、build、lint、type、security scan、coverage、deploymentの結果はGitHub Actions等の外部サービスを正本とする。

repositoryへ生ログやreport全文を保存しない。Commit Commentとreview YAMLにはworkflow、required check、test code、生成物への参照だけを書く。

## 6. Profile

### direct

局所的、可逆、外部副作用なし。targeted verificationを行う。

### assured

公開契約、DB、IaC、dependency、共有UI、generator、永続要件、governance。変更固有のRisk-selected checkを追加する。

### regulated

authentication、authorization、PII、confidential、data loss、不可逆production操作、法令・契約統制、高額操作。work item、明示承認、hash chain、phase gateを追加する。

## 7. Check selection

- `Invariant`: trigger該当時はPass必須
- `Risk-selected`: 変更固有に選択された場合だけblocking
- `Advisory`: 修正、Issue、residual risk
- `Periodic`: 定期監査

未選択をN/Aへ変換しない。

## 8. 実行規模

- profile、scope、verification、review、computeを必要に応じて選ぶ。
- riskだけを理由に無関係な全repository scanを行わない。
- context、tool、reviewer、computeの予算はsoft limitにする。
- fixed file countやtool countをhard gateにしない。
- 検証失敗、新依存、契約影響、証拠不足に基づいて拡張する。
- 同じ新証拠から複数軸が直接必要なら、理由付きで同時拡張できる。
- 成功後はCommit Comment、review result、PR/CI確認以外の探索を止める。

## 9. Reviewerとsubagent

独立reviewerは次の場合だけ使用する。

- critical risk
- 高影響な公開契約
- oracleが不足する
- representative checkが失敗した
- 要求と実装の証拠が矛盾する

単純な棚卸しや局所修正へ常に複数agentを使用しない。

## 10. 承認

通常のdirect / assuredへ一律の初回承認を要求しない。

明示承認が必要:

- 永続要件の意味変更で利用者判断が必要
- external write
- production
- deletion、publication、merge
- irreversible operation
- cost boundary
- regulated

内部設計、tool、trace path、test方法の変更だけでは再承認しない。

## 11. Hooks

SessionStartはfull governanceを毎回再注入しない。active regulated workがある場合だけ、その状態とauthority boundaryを通知する。

Stop retrospectiveは次の場合だけ実行する。

- active regulated work
- escaped defect
- repeated user correction
- critical control miss
- rollback
- repeated CI repair

通常セッションの終了だけを理由にreportを増やさない。

## 12. 最小指示の回帰check

- [ ] 結果、成功条件、authority、証拠、停止条件がある。
- [ ] 同じ指示を複数層で重複していない。
- [ ] repository変更の必須成果物が4種類に限定されている。
- [ ] work itemとfull lifecycleがregulated限定である。
- [ ] related checkだけをcontextへ入れている。
- [ ] CI結果をrepositoryへ複製していない。
- [ ] 可逆な実装方法を過剰指定していない。
- [ ] 人が確認する情報がCommit Comment、review YAML、生成設計へ集約されている。
