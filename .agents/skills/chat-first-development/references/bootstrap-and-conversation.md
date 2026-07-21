# 開発開始と対話の契約

## AIが行う事前確認

開発依頼の開始時に、次を利用者へ作業指示として転送せず実施する。

1. repository rootと適用される指示を確認し、Git状態を調べ、無関係な変更を保護する。
2. `tools/devflow.py`、`governance/policy.json`、`docs/templates`、check catalogの有無から利用可能なruntimeを把握する。
3. 要件影響、設計影響、authority、riskを判定し、`direct`、`assured`、`regulated`のいずれかを選ぶ。
4. 利用可能なtest、build、lint、type check、生成物drift、GitHub連携、公開境界を確認する。
5. 必要になった時点でだけrepository-local環境を作り、固定された依存をlocalへ導入する。安全に修復できるsetup driftは利用者へ転送しない。
6. 外部機能の不足は、成果達成に実際に必要となった時点でだけblockerとして扱う。

AIが安全にsetupを修復できる場合、利用者へfileのコピーやinstallation commandの実行を求めて作業を停止しない。

## 通常変更の記録

`direct`と`assured`では、恒久的な`work/<id>/`を作成しない。すべてのrepository変更で残すものは次の4つである。

1. 実際のコード、設定、test、要件、生成設計、ADR等の成果物
2. `docs/COMMIT-COMMENT.md`に従う構造化Commit Comment
3. 選択checkだけを記録した`governance/reviews/<change-id>.yaml`
4. GitHub Actions等の外部サービスにあるCI結果

再開に必要な一時状態だけを、gitignoreされた`.devflow/run/`へ置き、変更完了後に削除する。

通常変更では、変更ごとのrequest、requirements写し、execution plan、architecture、implementation log、test report、security report、release report、retrospectiveを作成しない。永続要件は`spec/requirements/requirements.json`だけへ反映し、実装から生成できる設計は手書きで複製しない。

## Regulatedの記録

次のいずれかに該当する場合だけ、`work/<id>/`を作成または再開し、regulated runtimeを使用する。

- authentication、authorization、PII、confidential dataを扱う
- data lossまたは不可逆なproduction操作のriskがある
- 法令、契約、監査上の統制が必要である
- 高額操作または明示的な高保証要求がある

この場合に限り、必要なlifecycle文書、一度だけの明示承認、hash chain、phase gate、regulated auditを追加する。templateが存在することだけを理由に文書を作らない。

## 対話の順序

1. 利用者が得たい結果を一、二文で確認する。
2. 選択肢によって結果が大きく変わる事実だけを質問する。可逆な事項は明示した前提で進める。
3. `direct`または`assured`では、通常の初回承認を要求せず、必要なimpact判定とselected checkを示して実行する。
4. 外部書込み、公開、merge、削除、production操作、不可逆操作、cost boundary等に明示権限が必要な場合は、そのauthority boundaryだけを確認する。
5. `regulated`では、結果、要件差分、authority、外部副作用、rollback、停止条件をまとめた一つの承認packageを提示し、明確な自然言語の承認を一度だけ得る。
6. 実行中は節目を共有するが、commandやroutineな実装判断を利用者へ転送しない。

## 完了の順序

関連する設計、実装、test、静的検査、security確認、文書、Git commit、remote branch、PR、CIを完了する。CIの生ログをrepositoryへ複製しない。明示的な権限なしにmergeしない。

`direct`と`assured`では、成果物、Commit Comment、review YAML、外部CIが現在HEADと整合した時点で完了する。`regulated`では、それらに加えて必要なregulated evidenceを最新にした後だけwork recordを閉じる。
