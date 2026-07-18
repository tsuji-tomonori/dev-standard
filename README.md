# 移植可能なAI開発Skills・agents集

他のリポジトリへコピーし、自然言語で相談するだけで使えるAI開発Skills、Codex agents、統制実行基盤の参照コレクションです。このリポジトリ自身にも同じ仕組みを適用しています。

`$right-size-execution`が変更範囲、保証水準、計算資源、実行方式を独立に推定し、最小十分なcontext・tool・検証から開始します。高リスクは探索範囲ではなく保証水準へ反映し、新証拠があるときだけ一軸を拡張します。実行予算、実績、拡張理由、選択漏れ監査をwork itemへ保存し、成功後は探索を止めます。

## このリポジトリが担保する3本柱

### 1. 対話から原子的な永続要件を維持する

`$maintain-canonical-requirements`が、研究に基づく傾聴、言語化、発散と収束を用い、会話から本当に必要な結果を探ります。各要件を「一つの主体・一つの行為・一つの対象・独立した受入基準」に分け、追加・更新・廃止を版付き差分として適用します。

- 永続正本: [`spec/requirements/requirements.json`](spec/requirements/requirements.json)
- 人向け生成文書: [`docs/requirements/REQUIREMENTS.md`](docs/requirements/REQUIREMENTS.md)
- 会話断片・承認境界・計画・証跡: `work/<id>/`

`work/`は正本ではありません。要件の削除は履歴を消さず`retire`として残します。人向け文書は正本から自動生成し、直接編集と生成差分を検査します。

### 2. 実装と1対1の詳細設計を生成する

初期対象はFastAPIとAWS CDKです。`$generate-implementation-design`が実装成果物から決定的に詳細設計を生成し、ソースSHA-256とバイト差分で乖離を検出します。

| 実装ソース | 生成する詳細設計 |
|---|---|
| FastAPI `router.py`のAST | operationの処理フロー・Mermaidシーケンス図 |
| アプリケーションのOpenAPI | API一覧・request/response・schema一覧 |
| 生`.sql`のSQLGlot AST | query object一覧・table CRUD図 |
| CDKが合成したCloudFormation YAML/JSON | resource一覧・parameter詳細 |

FastAPIでは`router.py`に処理の流れ、`functions.py`に具体処理を置きます。生成設計は実装を説明しますが、要件適合を自動的に証明したことにはしません。正本要件、実装、生成設計、テストをtraceで接続します。

### 3. 世界標準と公式ベストプラクティスで検証する

`$verify-against-engineering-standards`がSWEBOK v4.0aと各クラウドベンダーの公式ガイダンスを、版、適用範囲、差分、確認日、再確認期限付きで管理します。これらは案件文脈に応じて適用する参照資料であり、完全準拠や一律適用を表明しません。

- 正本台帳: [`governance/standards/registry.json`](governance/standards/registry.json)
- 人向け生成一覧: [`docs/standards/SOURCES.md`](docs/standards/SOURCES.md)
- チェックリスト: `governance/checklist/catalog.json`と`checklist.xlsx`

各項目には、適用性、案件重要度と根拠、`Pass=直接証跡`、`N/A=範囲上の非該当理由`、`Fail=Issue・対応方針・期限`、レビュー担当、日付、再確認、履歴を記録します。古い資料を「最新」と扱わず、公式資料を定期的に再確認します。

## 使い方: フォルダをコピーして相談するだけ

1. このリポジトリの`.agents/skills`を対象リポジトリの`.agents/skills`へコピーします。
2. 対象リポジトリをAI開発エージェントで開きます。
3. 「検索を使いやすくしたい」「このAPIを追加したい」のように普段の言葉で相談します。

Skill名、Python、インストーラー、work item、テストコマンドを指定する必要はありません。AIが導入状態と既存リポジトリを確認し、必要な正本、台帳、リポジトリ内依存を自動準備します。要件差分と実行権限を一度だけ自然言語で承認した後は、設計、実装、テスト、PR作成、CI確認まで自走します。

厳密な工程チェックリスト、ハッシュ付き承認、工程監査も使う場合は、`.agents/skills`に加えて`governance`、`docs/templates`、`tools`、`checklist.xlsx`、`requirements.txt`を同じ相対パスへコピーします。コピープロファイルと自動導入の詳細は[移植ガイド](docs/INSTALLATION.md)、機械可読な対応関係は[distribution/manifest.json](distribution/manifest.json)を参照してください。

## 標準配置

| コレクション | コピー元 | コピー先 | 目的 |
|---|---|---|---|
| 移植用Skills | [`.agents/skills`](.agents/skills) | `<target>/.agents/skills` | 会話起点の要件・設計・検証フロー |
| 永続要件 | [`spec/requirements`](spec/requirements) | 対象側でSkillが自動初期化 | 対象製品固有の正本なので参照側の内容はコピーしない |
| Codex agents | [`.codex/agents`](.codex/agents) | `<target>/.codex/agents` | 任意の読取専用レビュー担当 |
| Codex hooks | [`.codex/hooks`](.codex/hooks) | 同じ相対パス | 任意のライフサイクル連携 |
| 統制実行基盤 | [`governance`](governance)、[`tools/devflow.py`](tools/devflow.py)、[`docs/templates`](docs/templates) | 同じ相対パス | 決定的ゲート、承認、監査 |
| 適正規模実行 | [`.agents/skills/right-size-execution`](.agents/skills/right-size-execution) | 同じ相対パス | 多軸profile、soft budget、単軸Expand、選択漏れ監査、benchmark |

対象固有の`AGENTS.md`と`.codex/config.toml`は上書きしません。AIが既存内容を維持し、必要部分だけをレビュー対象の変更として統合します。

## 一度だけの承認と自律境界

AIは、ユーザー原文、正本へのadd/update/retire差分、受入条件、trace、全作業、許可操作、外部副作用、停止条件、完了条件を一つのまとまりにします。人はこれを一度だけ承認します。その後の定型的な設計選択、実装、レビュー修正、テスト修正、PR作成、CI確認に追加承認を求めません。

承認は白紙委任ではありません。要件や外部副作用が承認境界を越える場合だけ、新しい差分として停止します。詳しくは[開発フロー](docs/FLOW.md)、[統制モデル](docs/GOVERNANCE.md)、[AI運用方針](docs/AI-OPERATING-POLICY.md)を参照してください。

## Skills一覧と検証

用途、起動条件、依存関係、コピー元は[Skills一覧](docs/SKILLS.md)に集約しています。

この参照実装自身は、要件正本、生成文書、出典の鮮度、カタログ、全単体テスト、リポジトリ構造、ハッシュチェーン監査をCIで検査します。AIが内部コマンドを実行するため、利用者へコマンド実行を求めません。
