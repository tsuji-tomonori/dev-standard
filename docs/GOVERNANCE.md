# 統制・監査モデル

## 1. 情報の3分類

### 現在状態の正本

今後も最新状態を維持する。

- `spec/requirements/requirements.json`
- code、config、test
- `docs/design/generated/`
- ADR
- 恒久的な運用・保守文書

### 変更時点の証跡

その変更を説明・レビュー・監査するため固定し、現在状態へ合わせて後から書き換えない。

- Commit Comment
- `governance/reviews/<change-id>.yaml`
- PRとGit履歴
- regulated案件のapproval / event chain

### 一時実行状態

作業再開にだけ使い、完了後に削除する。

- `.devflow/run/`

通常変更で恒久的な`work/<id>/`を作らない。

## 2. 信頼境界

自然言語Skillは判断と作業方法を案内する。次は可能な限り決定的な仕組みへ置く。

- requirement schemaとrevision conflict
- generated artifact drift
- review result schema
- build、type、lint、test
- secret scan
- API contract diff
- migration / synth
- branch protectionとrequired check
- external operation permission

AIの自己申告だけをPass、承認、CI結果にしない。

## 3. Commit Comment

Commit Commentを次の変更時点証跡として使用する。

- Change Manifest
- Requirement Impact Result
- Design Impact Result
- implementation summary
- verification contract
- compatibility / residual risk

CIの実行結果は含めず、外部サービスのworkflowまたはrequired checkを参照する。

## 4. Review result

`governance/reviews/<change-id>.yaml`にはselected checkだけを保存する。

### Invariant

triggerに該当した場合はPass必須。

### Risk-selected

risk、artifact、path、profileから選択された場合だけblocking。

### Advisory

修正、Issue化、residual riskのいずれかへ収束できる。

### Periodic

個々のPRではなく定期監査で扱う。

未選択項目をN/Aにしない。N/Aは選択後に具体的な適用外事実が判明した場合だけ使用する。

## 5. Automated result

単体test、build、type、lint、coverage、security scan、deployment resultの正本はGitHub Actions、deployment service、monitoring service等とする。

repositoryへ次を保存しない。

- test log全文
- coverage report全文
- scanner生出力
- build log
- external service resultの複製

repositoryへ残すのは、test code、workflow定義、required check名、review resultからの参照である。

## 6. 承認

人の承認はauthority boundaryへ結び付ける。

承認対象:

- 永続要件の意味変更
- external write
- production operation
- deletion、publication、merge
- irreversible operation
- cost boundary
- secrets、PII、権限境界

可逆な実装手段、tool、trace path、test file、reviewer、実装順序を承認digestへ固定しない。

`direct`と通常の`assured`では初回承認を要求しない。`regulated`または外部副作用時だけ明示承認を使用する。

## 7. Regulated compatibility

既存の次の仕組みは`regulated`でのみ使用する。

- `work/<id>/`
- `tools/devflow.py`
- lifecycle phase
- approval hash chain
- event hash chain
- required lifecycle documents
- regulated release / audit

このruntimeをdirectまたはassuredへ自動適用しない。

## 8. Gate timing

- 変更開始前: Impact Check
- 実装中: Fast Feedback Check
- PR前: Affected-scope Check
- Merge前: Revision Integrity Check
- Deploy後: Operational Check
- 定期: Governance Audit

工程文書の存在ではなく、変更イベントとriskに応じた結果を確認する。

## 9. Failの扱い

- Invariant fail: 修正までblocking
- blocking Risk-selected fail: 修正までblocking
- Advisory: 修正、Issue、residual risk
- automated fail: 外部CIで失敗として扱う

その場で修正できる全Failへ一律にIssue、owner、due dateを要求しない。

## 10. 改ざんと履歴

Commit Comment、review YAML、PR、Git commitはGit履歴で追跡する。

regulated案件で強い改ざん検知が必要な場合だけhash chain、protected branch、signed commit、外部audit logを追加する。

## 11. 定期改善

改善はgate errorの回数だけから自動追加しない。次を確認する。

- 防ぎたい実際の品質欠陥
- 利用者影響
- 現行controlが防げなかった理由
- 新controlの予想コスト
- 適用trigger
- 既存controlで代替できない理由
- shadow評価
- 再評価日またはsunset条件

形式的な失敗からルールを無制限に増やさない。
