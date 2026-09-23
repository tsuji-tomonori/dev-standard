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

Dev標準は言語非依存のガードレールと、導入先adapterが満たす実装要件を配布します。静的解析・as-built生成の実装は導入先repositoryで作成します。「Dev標準を入れて実装して」という依頼には、実装surfaceの棚卸し、adapter接続、必要なMarkdown設計の初回生成と検査まで含まれます。

[導入・復旧手順](../../.agents/skills/generate-implementation-design/references/adoption.md)に従い、固定revisionの参照tools全件を比較して用途・要件対応・採用区分・理由・実接続先を記録します。[lazunexの52ファイル棚卸し](../../.agents/skills/generate-implementation-design/assets/reference-tools/lazunex-096e1e5.json)を基に、導入先の言語と構造へadapt・extendします。別の参照実装も同じschemaで評価できます。

schema version 2の`.dev-standard/design.json`へcapabilityごとの生成command、`--check` command、出力root、要件ID、帳票構成profile、棚卸し参照を宣言します。[adapter契約](../../.agents/skills/generate-implementation-design/references/adapter-contract.md)の検査器は作業コピーで2回生成のbyte一致とdriftを確認し、[APIの6帳票](../../.agents/skills/generate-implementation-design/references/api-documents.md)の章・順序・階層・索引、旧生成物、リンク、CRUDモデルの整合を検査します。

```bash
python <host-skill-path>/scripts/check_design.py --root .
```

`<host-skill-path>`はinstallerが配置したSkillのhost-native rootです。言語固有の解析・型検査・実行テストはmanifestへ接続した導入先commandが担います。実装がない領域だけを根拠付きで非該当とし、未接続・未対応・未生成を成功扱いにしません。完了報告は構成適合、設計drift、実行テスト、未検証範囲を分け、生成物path、対象revision、commandと結果を示します。

旧`designflow.py`・`qualityflow.py`・`portable_python.py`は配布しません。既存利用者はadapterとmanifestを接続してから旧assetと専用runtimeを確認除去してください。installerは既存fileを自動削除しません。`aws-cdk-implementation-design`は汎用`implementation-design`の互換aliasです。CIとの接続は導入先の既存運用に従います。

## 品質エビデンスの既定公開準備

製品要件だけで開発を始められるよう、新規開発・導入時はテスト一覧と個別結果、GWT画像、静的解析、実測coverage、検索可能な生成設計書をまとめる品質portalを初期成果に含めます。agentがframeworkに応じたadapterを実commandへ接続します。新規GitHub projectはPages公開用設定を準備し、既存projectは既存CI・公開先へ接続します。実公開には対象の権限を適用します。

[品質portalの導入契約](../../.agents/skills/inspect-quality-gates/references/evidence-portal.md)に共通JSON、同梱rendererとJUnit/Vitest変換、設計HTMLの接続、失敗を隠さない公開job、受入確認を定義しています。空templateや未接続adapterを導入完了としません。
