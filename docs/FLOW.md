# AI駆動開発フロー

## 1. 二つの適用面

このrepositoryは、次を分けて扱う。

1. **参照collectionの保守**: Skills、agents、標準、governance、distribution、sample、documentationを更新する。`$maintain-reference-repository`を適用する。
2. **導入先projectの実行**: copyされたSkillsがproduct実装を進める。必要に応じて`direct`、`assured`、`regulated`を選択する。

参照collectionの保守記録を、導入先向けsampleの`work/`として保存しない。

## 2. 生成方向

```text
自然言語の相談
    │
    ├─ reference repository boundary
    ├─ product / project requirement
    ├─ functional / nonfunctional
    ├─ design impact
    ├─ authority / risk
    ▼
direct / assured / regulated
    │
    ├─ 必要時だけrequirements.jsonを更新
    ├─ 実装・test
    ├─ 実装からas-built設計を生成
    ├─ selected checkをreview YAMLへ保存
    ├─ 構造化Commit Comment
    ▼
PR・GitHub Actions・必要時のDeploy
```

この参照repositoryではtop-levelの`work/`を作らない。regulated runtimeの実行中work itemは導入先repositoryで生成する。

## 3. 変更開始前: Impact Check

次を判定する。

- 利用者が得る結果
- portable assetかrepository固有事情か
- product requirement / project requirement
- functional / nonfunctional
- documentation requirement
- design impact
- distribution / public contract
- DB / migration
- IaC / network
- dependency / lockfile
- authentication / authorization / PII
- external write / production / irreversible operation

この判定からprofileとselected checkを選ぶ。全checkを評価したり、未選択をN/Aへ変換したりしない。

## 4. 要件と文書

永続要件は`spec/requirements/requirements.json`へ置く。分類は[要件分類標準](standards/REQUIREMENT-CLASSIFICATION.md)に従う。

- product: 導入先へ提供する挙動、interface、品質、制約
- project: 開発、保守、review、配布、文書化、運用準備の義務
- functional: 能力、処理、変換、応答
- nonfunctional: 品質、閾値、制約、process、deliverable、operational guarantee

文書の存在、内容、鮮度、更新、配布、廃止は原則`project / nonfunctional`として扱う。文書fileは要件の実現手段または生成表示であり、要件正本ではない。

## 5. 実行プロファイル

### 直接実行（direct）

局所的、可逆、外部副作用なし。対象範囲のtest、build、lint、type、生成物driftだけを実行する。

### 保証付き実行（assured）

複数module、公開契約、DB、IaC、dependency、共有UI、generator、永続要件、governance、distribution。関連するRisk-selected checkを追加する。

### 規制・高保証実行（regulated）

authentication、authorization、PII、data loss、不可逆production操作、法令・契約統制、高額操作、高保証要求。導入先projectではwork item、明示承認、phase gate、hash chainを追加できる。

この参照repository自身ではliveなwork itemを保存しない。portable runtimeを検証する場合はsynthetic fixtureまたは一時directoryを使う。

## 6. 実装中: Fast Feedback Check

変更スライスごとに小さく検証する。

- syntax / build
- lint / type
- targeted test
- regression test
- generated drift
- secret scan
- 選択時だけcontract diff、SQL parse、migration、synth、UI interaction等
- reference repository boundary、manifest、portable profileのcontract test

CI結果の正本はGitHub Actions等とし、repositoryへ実行ログを保存しない。

## 7. PR作成前: Affected-scope Check

確認するもの:

- requirement impactと要件正本の差分
- product / project、functional / nonfunctionalの分類
- documentation requirementと文書lifecycle
- design impactと生成設計・ADR
- distribution profileとconsumer compatibility
- 受入条件とtest
- 不要な変更またはlive work recordの混入
- compatibility、migration、rollback
- selected check result
- blocking fail
- advisoryの扱い
- residual risk

結果を`governance/reviews/<change-id>.yaml`へ保存する。

## 8. コミットコメント

`docs/COMMIT-COMMENT.md`に従い、次をコミット本文へ記録する。

- 目的
- 変更内容
- 要件影響
- 設計影響
- review YAML path
- 検証契約
- 互換性・残存リスク

Change Manifest、Requirement Impact Result、Design Impact Resultを別ファイルとして作らない。

## 9. Merge前: Revision Integrity Check

- CIが現在HEADを対象としている
- required checkが成功している
- generated artifactが最新
- blocking failがない
- advisoryとresidual riskの扱いが明示されている
- squash後のCommit Commentに証跡が統合されている
- merge、release、deployがauthority boundary内
- top-levelの`work/`がない
- portable profileにrepository固有artifactが混入していない

HEAD変更で無効化された証拠だけを再確認する。過去工程を全て再実行しない。

## 10. Deploy後: Operational Check

production、migration、外部サービス、data変更がある場合だけ導入先で実施する。

- deploy status
- smoke test
- migration result
- 主要metric
- rollback / roll-forward

結果はdeployment service、monitoring、GitHub Actions等へ保持する。

## 11. 定期: Governance Audit

月次またはrelease単位で確認する。

- false blocker
- escaped defect
- selector miss
- Skill・hook競合
- 不要成果物
- repository固有work recordの再混入
- standard source freshness
- advisory滞留
- tool / context / reviewer cost

個々の変更へ毎回retrospectiveを強制しない。

## 12. 情報の保持

| 種類 | 保存先 | 更新規則 |
|---|---|---|
| 現在状態の正本 | requirements、code、test、generated design、ADR、project NFRに基づく運用文書 | 今後も維持 |
| 変更時点の証跡 | Commit Comment、review YAML、PR | 後から現在状態へ合わせて更新しない |
| automated result | GitHub Actions等 | 外部retention policy |
| 将来作業 | Issue | 完了まで維持 |
| 一時実行状態 | `.devflow/run/` | 完了後削除 |
| regulated live work | 導入先repositoryの`work/<id>/` | この参照repositoryへ保存しない |
