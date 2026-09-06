# dev-standard

AI開発agentが、対象repositoryの既存運用を壊さずに使える軽量なSkills集です。既定portable setは会話の入口と3本のガードレールだけを配布します。

## 1. durableな原子要件

永続要件の一次言語は[Quint](https://quint.sh/)です。`spec/requirements/requirements.qnt`を唯一の編集対象とし、型と不変条件を検査します。

## 2. 実装由来のas-built設計

現在の構造とinterfaceは実装artifactから決定的に生成します。生成文書を直接編集して実装との差を隠しません。

## 3. 変更に関係する検査だけ

変更と受入条件に対応するtest、lint、type check、build、generatorだけを選びます。CIがある場合は利用できますが、CIやmerge ruleの導入を要求しません。

## Quintから人向け文書まで

```text
requirements.qnt → requirements.json → REQUIREMENTS.md
skills.qnt       → skills.json       → FORMAL-SPECIFICATIONS.md
```

```bash
npm ci --ignore-scripts
python tools/quintflow.py generate
python tools/quintflow.py check
python tools/quintflow.py test
python tools/quintflow.py verify
```

`spec/skills/skills.qnt`は18 Skillのinventory、起動context、authority、副作用、依存関係を型付き契約として列挙します。形式モデルは、`repositoryBlocking`が3本柱だけであること、既定portable setが4 Skillだけであること、各Skillの7つのrepository policy fieldがfalseであることを検査します。`make verify`はこの参照repository自身についてunit testに加え、要件正本と配布templateを4 step、Skill契約を3 stepでApalache bounded model checkingします。検査結果とdigestは、モデル化したfield、探索範囲、byte対応の証拠であり、自然言語や外部repositoryの全状態を証明するものではありません。導入先で同じbounded検証を実行するかは任意であり、CIや同じcommandを要求する規則でもありません。

## 導入

まずdry-runし、差分を確認してから適用します。

```bash
python tools/install_reference.py --target ../target-repository --profile default
python tools/install_reference.py --target ../target-repository --profile default --apply
```

`default`が配布するSkillは次の4つです。

- `chat-first-development`
- `maintain-canonical-requirements`
- `generate-implementation-design`
- `inspect-quality-gates`

installerは導入先の`.github/`、branch、merge設定を追加も変更もしません。既存の`AGENTS.md`または`CLAUDE.md`は管理marker内だけを更新し、その他の記述を維持します。

最新モデル向けの構成判断と公式根拠は[フロンティアモデルと最小ハーネス](docs/reference/frontier-model-guidance.md)を参照してください。

詳細は[導入とSkills一覧](docs/guides/getting-started.md)、[形式仕様](docs/reference/FORMAL-SPECIFICATIONS.md)、[開発契約](docs/reference/development.md)を参照してください。

## 導入完了の条件

「Dev標準を入れて実装して」という依頼には、Skillの配置に加えて、実装由来のMarkdown設計の初回生成まで含まれます。API・data・infra・frontendの実装対象を棚卸しし、必要なgenerator/adapterを接続してください。生成器が未宣言であることを省略理由にしません。

[導入・復旧手順](.agents/skills/generate-implementation-design/references/adoption.md)に従い、必要な生成物を`.dev-standard/design.json`で明示し、`python <host-skill-path>/scripts/check_design.py --root .`または既存の同等検査を通常のverify入口で実行します。必要なMarkdownの欠落・空・drift・未対応は未完了です。実装がない領域は根拠を示して非該当とします。

完了報告には生成物へのpath、対象revision、生成・検査commandと結果を含めます。installer成功やアプリのtest成功だけでは導入完了になりません。CIとの接続は導入先の既存運用と権限に従います。

## 品質エビデンスの既定公開準備

製品要件だけで開発を始められるよう、新規開発・導入時はテスト一覧と個別結果、GWT画像、静的解析、実測coverage、検索可能な生成設計書をまとめる品質portalを初期成果に含めます。agentがframeworkに応じたadapterを実commandへ接続します。新規GitHub projectはPages公開用設定を準備し、既存projectは既存CI・公開先へ接続します。実公開には対象の権限を適用します。

[品質portalの導入契約](.agents/skills/inspect-quality-gates/references/evidence-portal.md)に共通JSON、同梱rendererとJUnit/Vitest変換、設計HTMLの接続、失敗を隠さない公開job、受入確認を定義しています。空templateや未接続adapterを導入完了としません。
