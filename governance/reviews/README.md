# 過去のレビュー証跡

このdirectoryの`CHG-*.yaml`、schema、template、validatorは、2026年8月以前にこの参照repository自身が採用していたreview方式を再現するための履歴資料です。現行のportable guardrail、変更ごとの成果物、導入先repositoryのauthorityではありません。

## 現行方針

- 新しい変更に`governance/reviews/<change-id>.yaml`を作成しません。
- 旧固定実行分類や固定phaseを、現在の3本柱へ追加しません。補助機能は具体的な`activation context`がある場合だけ選択します。
- review YAML、Commit Comment、PR template、CI workflow、required check、branch protection、merge ruleを導入先へ要求しません。
- 選択した検査の結果は会話、ローカルsummary、または対象repositoryが既に所有する変更記録へ簡潔に返します。
- 法令・契約等が独立した保存義務を課す場合だけ、そのauthorityと保持範囲に従い`govern-development-request`等を明示的に選択します。

現行のblocking guardrailは、Quint要件正本、実装由来as-built設計、変更に関係する選択checkの3本だけです。過去のYAMLが同じcheck IDを参照していても、それによって現在の選択、証拠形式、merge条件は決まりません。

## 履歴の再現

過去のcommitを調査するときに限り、その時点のcatalog、schema、validator、commitを一緒にcheckoutして検証します。現在のcatalogへ合わせて古い`CHG-*.yaml`を書き換えません。`review-result.template.yaml`は新規作成用templateではなく、旧形式の説明用fixtureとして保持します。

```bash
python governance/reviews/validate.py --root . --commit <historical-commit>
```

installerと`distribution/manifest.json`は、このdirectoryをどの配布collectionにも含めません。
