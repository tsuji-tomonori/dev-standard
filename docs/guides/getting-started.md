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

## 導入完了の条件

「Dev標準を入れて実装して」という依頼には、Skillの配置に加えて、実装由来のMarkdown設計の初回生成まで含まれます。API・data・infra・frontendの実装対象を棚卸しし、必要なgenerator/adapterを接続してください。生成器が未宣言であることを省略理由にしません。

[導入・復旧手順](../../.agents/skills/generate-implementation-design/references/adoption.md)に従い、必要な生成物を`.dev-standard/design.json`で明示し、`python <host-skill-path>/scripts/check_design.py --root .`または既存の同等検査を通常のverify入口で実行します。必要なMarkdownの欠落・空・drift・未対応は未完了です。実装がない領域は根拠を示して非該当とします。

完了報告には生成物へのpath、対象revision、生成・検査commandと結果を含めます。installer成功やアプリのtest成功だけでは導入完了になりません。CIとの接続は導入先の既存運用と権限に従います。

SQLを使うAPIでは[SQLと説明コメントの契約](../../.agents/skills/generate-implementation-design/references/sql-and-language.md)も適用します。API別SQLを正本に、DDL/SQLから型付き`generated/queries.py`を生成し、SQL lint・配置/呼出境界・生成差分・関連DBテストを完了させます。適用済みmigrationは書き換えません。説明コメント・docstring・生成ヘッダーは別言語の明示指示がなければ日本語とし、英語が残る生成物はテンプレートから直して再生成します。
