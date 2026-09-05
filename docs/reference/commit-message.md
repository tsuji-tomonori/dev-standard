# 日本語Gitmoji commit形式（任意）

この形式は、利用者または対象repositoryが明示的に選択した場合だけ使用します。dev-standardの既定profile、portable gate、merge条件ではありません。対象repositoryが別の形式を持つ場合はそちらを優先します。

```text
<gitmoji> <type>(<scope>): <日本語の要約>

目的:
- <達成する結果>

変更内容:
- <主要変更>

要件影響:
- <あり / なし、Quint要件ID、理由>

設計影響:
- <あり / なし、生成設計またはADR、理由>

検証:
- <実行したローカル検査、または既存CIへの参照>

互換性・残存リスク:
- <既知事項>
```

実行していない検査をPassと書かず、生ログを貼り付けません。review YAML、required check、特定CI、特定branchまたはmerge方式を必須項目にしません。
