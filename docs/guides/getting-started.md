# 導入とSkills一覧

## 導入方法

対象repositoryで、既存の指示と構成を維持したまま`default` profileを統合します。

```bash
python tools/install_reference.py --target ../target-repository --profile default
python tools/install_reference.py --target ../target-repository --profile default --apply
python tools/install_reference.py --target ../target-repository --profile default --host claude-code --apply
```

最初のcommandはdry-runです。既存fileと内容が異なる場合は停止し、`--force`は差分を確認した後だけ使用します。Codexは`AGENTS.md`、Claude Codeは`CLAUDE.md`の管理marker内だけを更新します。

## 既定profile

`default`と`chat-first`は次の4 Skillだけです。

| Skill | 役割 |
|---|---|
| `chat-first-development` | 自然言語依頼の入口 |
| `maintain-canonical-requirements` | Quintによるdurableな原子要件 |
| `generate-implementation-design` | 実装由来のas-built設計 |
| `inspect-quality-gates` | 変更に関係する検査だけを選択 |

導入先のCI workflow、required check、branch protection、ruleset、merge方式、PR template、commit形式は追加も変更もしません。CIがないrepositoryではローカル検査を使います。

## 全Skills

| Skill | 用途 |
|---|---|
| `adversarial-review` | 反証可能な主張の独立review |
| `author-lifecycle-docs` | 明示的なregulated証拠の文書化 |
| `authorize-autonomous-execution` | 外部副作用と権限境界の確認 |
| `calibrated-collaborative-listening` | 結果を変える曖昧さの確認 |
| `chat-first-development` | 通常依頼の入口 |
| `design-frontend-experience` | UI interaction設計 |
| `elicit-frontend-requirements` | UI要求の獲得 |
| `generate-implementation-design` | 実装由来設計の生成 |
| `govern-development-request` | 明示的なregulated work |
| `implement-frontend-experience` | UI実装 |
| `inspect-quality-gates` | 関係する検査の選択 |
| `japanese-git-commit-gitmoji` | opt-inの日本語commit形式 |
| `maintain-canonical-requirements` | Quint要件のadd・update・retire |
| `maintain-reference-repository` | この参照repositoryの保守 |
| `retrospect-and-improve` | 重大失敗時の改善 |
| `right-size-execution` | 実行範囲の調整 |
| `test-frontend-experience` | UI検証 |
| `verify-against-engineering-standards` | 関連標準の任意review |

全Skillのmachine-readableな役割、事前条件、事後条件、authority、side effectは[`spec/skills/skills.qnt`](../../spec/skills/skills.qnt)で形式化され、[形式仕様](../reference/FORMAL-SPECIFICATIONS.md)へ生成されます。配布内容の正本は[`distribution/manifest.json`](../../distribution/manifest.json)です。
