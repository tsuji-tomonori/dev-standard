# 導入と開発のガイド

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

## 必要時だけ追加する機能

UIの要求・設計・実装・検証には `frontend`、具体的な証跡保持義務には `regulated`、関連標準の照合には `standards-verification` 等のprofileを選べます。全Skill一覧と配布内容の正本は [manifest](../../distribution/manifest.json)、実行手順は[各Skill](../../.agents/skills/)です。`full`は全機能が必要な場合だけ使います。

Skillの機械可読な起動条件・authority・依存関係は `spec/skills/skills.qnt` で検査し、詳細は同名の `skills.json` に生成します。保守・監査時に必要な契約だけ参照してください。

## 導入完了の条件

「Dev標準を入れて実装して」という依頼には、Skillの配置に加えて、実装由来のMarkdown設計の初回生成まで含まれます。API・data・infra・frontendの実装対象を棚卸しし、必要なgenerator/adapterを接続してください。生成器が未宣言であることを省略理由にしません。

[導入・復旧手順](../../.agents/skills/generate-implementation-design/references/adoption.md)に従い、必要な生成物を`.dev-standard/design.json`で明示し、`python <host-skill-path>/scripts/check_design.py --root .`または既存の同等検査を通常のverify入口で実行します。必要なMarkdownの欠落・空・drift・未対応は未完了です。実装がない領域は根拠を示して非該当とします。

完了報告には生成物へのpath、対象revision、生成・検査commandと結果を含めます。installer成功やアプリのtest成功だけでは導入完了になりません。CIとの接続は導入先の既存運用と権限に従います。

SQLを使うAPIでは[SQLと説明コメントの契約](../../.agents/skills/generate-implementation-design/references/sql-and-language.md)も適用します。API別SQLを正本に、DDL/SQLから型付き`generated/queries.py`を生成し、SQL lint・配置/呼出境界・生成差分・関連DBテストを完了させます。適用済みmigrationは書き換えません。説明コメント・docstring・生成ヘッダーは別言語の明示指示がなければ日本語とし、英語が残る生成物はテンプレートから直して再生成します。

## 変更時の文書更新

永続要件はQuint正本、実装済み構造は生成設計へ反映します。手書きの利用手順・運用説明は利用者や操作が変わった場合だけ更新し、導入先の既存索引に利用目的・更新条件を記します。変更ごとの計画書・実装ログ・テスト報告書を増やしません。作業の一時状態は `.devflow/run/`、保持が必要な過去の結果は日付付きの履歴へ分けます。

導入先の要件・言語・framework・既存verify入口を調べ、3本柱をその構成へ接続します。Quintの初期化は `maintain-canonical-requirements`、API/data/infra/frontendの生成と適用外の根拠は設計Skillに従います。既存の指示や有効な承認を再利用し、承認不足の外部操作がある場合も独立して進められる準備は完了します。
