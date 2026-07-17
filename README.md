# Portable AI Development Skills and Agents

他のrepositoryへcopyして、自然言語で相談するだけで使えるAI開発skills・Codex agents・governance runtimeのreference collectionです。このrepository自身も同じ仕組みを自己適用しています。

## このrepositoryが担保する3本柱

### 1. 対話から原子的な永続要件を維持する

`$maintain-canonical-requirements`が、研究に基づく傾聴・言語化・発散と収束を使い、会話から本当に必要な結果を探します。各要件を「一つの主体・一つの行為・一つの対象・独立した受入基準」に分け、追加・更新・廃止をrevision付きdeltaとして適用します。

- 永続正本: [`spec/requirements/requirements.json`](spec/requirements/requirements.json)
- 人向け生成文書: [`docs/requirements/REQUIREMENTS.md`](docs/requirements/REQUIREMENTS.md)
- 会話断片・承認境界・計画・証跡: `work/<id>/`

`work/`は正本ではありません。要件の削除は履歴を消さず`retire`として残します。人向け文書は正本から自動生成し、直接編集と生成差分を検査します。

### 2. 実装と1対1の詳細設計を生成する

初期対象はFastAPIとAWS CDKです。`$generate-implementation-design`が、実装artifactから決定論的に詳細設計を生成し、source SHA-256とbyte差分でdriftを検出します。

| 実装source | 生成する詳細設計 |
|---|---|
| FastAPI `router.py` AST | operation flow・Mermaid sequence diagram |
| applicationのOpenAPI | API一覧・request/response・schema一覧 |
| raw `.sql`のSQLGlot AST | query object一覧・table CRUD図 |
| CDKがsynthしたCloudFormation YAML/JSON | resource一覧・parameter詳細 |

FastAPIでは`router.py`に処理の流れ、`functions.py`に具体処理を置きます。生成設計は実装を説明しますが、要件適合を勝手に証明したことにはしません。正本要件、実装、生成設計、testをtraceで接続します。

### 3. 世界標準と公式best practiceで検証する

`$verify-against-engineering-standards`がSWEBOKと各cloud vendorの公式guidanceを、版・確認日・再確認期限付きで管理します。

- 正本registry: [`governance/standards/registry.json`](governance/standards/registry.json)
- 人向け生成一覧: [`docs/standards/SOURCES.md`](docs/standards/SOURCES.md)
- checklist: `governance/checklist/catalog.json`と`checklist.xlsx`

各checkは`Pass=直接証跡`、`N/A=適用不能となるscope根拠`、`Fail=Issueと再test方法`で判定します。古いsourceを「最新」と扱わず、公式sourceの再確認を要求します。

## 使い方: folderをcopyして相談するだけ

1. このrepositoryの`.agents/skills`を対象repositoryの`.agents/skills`へcopyします。
2. 対象repositoryをAI development agentで開きます。
3. 「検索を使いやすくしたい」「このAPIを追加したい」のように普段の言葉で相談します。

skill名、Python、installer、work item、test commandを指定する必要はありません。AIが導入状態と既存repositoryを確認し、必要な正本・registry・repository-local dependencyを自動準備します。要件deltaと実行権限を一度だけ自然言語で承認した後は、設計、実装、test、PR作成、CI確認まで自走します。

厳密なphase checklist、hash付き承認、工程auditも使う場合は、`.agents/skills`に加えて`governance`、`docs/templates`、`tools`、`checklist.xlsx`、`requirements.txt`を同じ相対pathへcopyします。copy profileと自動導入の詳細は[移植ガイド](docs/INSTALLATION.md)、machine-readable mappingは[distribution/manifest.json](distribution/manifest.json)を参照してください。

## 標準配置

| Collection | Source | Target | Purpose |
|---|---|---|---|
| Portable skills | [`.agents/skills`](.agents/skills) | `<target>/.agents/skills` | chat-firstの要件・設計・検証workflow |
| Durable requirements | [`spec/requirements`](spec/requirements) | targetでskillが自動bootstrap | target product固有の正本なのでreferenceの内容はcopyしない |
| Codex agents | [`.codex/agents`](.codex/agents) | `<target>/.codex/agents` | optional read-only reviewer |
| Codex hooks | [`.codex/hooks`](.codex/hooks) | same path | optional lifecycle integration |
| Governance runtime | [`governance`](governance), [`tools/devflow.py`](tools/devflow.py), [`docs/templates`](docs/templates) | same paths | deterministic gate・authorization・audit |

対象固有の`AGENTS.md`と`.codex/config.toml`は上書きしません。AIが既存内容を保ち、必要な部分だけをreview対象の変更としてmergeします。

## 一度だけの承認と自律境界

AIは、ユーザー原文、正本へのadd/update/retire delta、受入条件、trace、全作業、許可操作、外部副作用、停止条件、完了条件を一つのpackageにまとめます。人がこれを一度だけ承認します。その後のroutineな設計選択、実装、review修正、test修正、PR作成、CI確認に追加承認は求めません。

承認は白紙委任ではありません。要件や外部副作用が承認境界を越える場合だけ、新しいdeltaとして止めます。詳しくは[開発フロー](docs/FLOW.md)、[統制モデル](docs/GOVERNANCE.md)、[AI operating policy](docs/AI-OPERATING-POLICY.md)を参照してください。

## Skills一覧と検証

用途、trigger、依存、copy元は[Skills一覧](docs/SKILLS.md)に集約しています。

このreference自身はcanonical requirements、generated docs、standards freshness、catalog、全unit test、repository structure、hash-chain auditをCIで検査します。AIが内部commandを所有するため、利用者にcommand実行を求めません。
