# 移植可能なAI開発Skills・agents集

他のrepositoryへコピーし、自然言語で相談するだけで使えるAI開発Skills、Codex agents、条件付き統制基盤の参照コレクションです。

## このrepositoryが担保する3本柱

### 1. 対話から原子的な永続要件を維持する

`$maintain-canonical-requirements`が、会話から今後も維持すべき製品要求だけを抽出し、`add`、`update`、`retire`として正本へ適用します。

- 正本: [`spec/requirements/requirements.json`](spec/requirements/requirements.json)
- 人向け生成表示: [`docs/requirements/REQUIREMENTS.md`](docs/requirements/REQUIREMENTS.md)

外部挙動、業務ルール、受入条件、非機能閾値、権限要求が変わらない場合、要件正本を更新しません。ただし要件影響の判定と理由はCommit Commentへ残します。

### 2. 実装と1対1のas-built設計を生成する

`$generate-implementation-design`が実装成果物から詳細設計を生成し、source digestとdriftを検査します。

| 実装ソース | 生成する設計 |
|---|---|
| FastAPI `router.py` AST | operation flow・Mermaid sequence |
| application OpenAPI | API・request / response・schema |
| raw SQL AST | query object・table CRUD |
| CDK synthesized CloudFormation | resource・parameter |

コードから生成できる情報を手書き設計として二重管理しません。コードだけでは理由が分からず、将来を制約する判断だけADRにします。

### 3. 必要なチェックだけを、適切な時点で行う

`$verify-against-engineering-standards`と`$inspect-quality-gates`が、変更riskとartifactに応じたcheckだけを選択します。

- `Invariant`: trigger該当時はPass必須
- `Risk-selected`: 選択された場合だけblocking
- `Advisory`: 修正、Issue、残存リスクへ収束
- `Periodic`: 個々のPRではなく定期監査

check timing:

1. 変更開始前: Impact Check
2. 実装中: Fast Feedback Check
3. PR前: Affected-scope Check
4. Merge前: Revision Integrity Check
5. Deploy後: Operational Check
6. 定期: Governance Audit

## 必ず残すもの

すべてのrepository変更で次を残します。

1. 実際の成果物
2. 構造化Commit Comment
3. `governance/reviews/<change-id>.yaml`のselected check result
4. GitHub Actions等の外部CI結果

Commit CommentはChange Manifest、Requirement Impact Result、Design Impact Resultを代替します。CIの生ログやtest reportはrepositoryへ複製しません。

詳細:

- [成果物とチェックのライフサイクル](docs/ARTIFACTS-AND-CHECKS.md)
- [Commit Comment契約](docs/COMMIT-COMMENT.md)
- [レビュー結果](governance/reviews/README.md)

## `work/`の扱い

通常の`direct`と`assured`では恒久的な`work/<id>/`を作りません。

再開用の一時状態が必要な場合だけ、gitignoreされた`.devflow/run/`を使用し、変更完了後に削除します。

既存のwork item、初回承認、hash chain、phase gateは`regulated`専用です。

## 実行プロファイル

### 直接実行（direct）

局所的、可逆、外部副作用なし。targeted test、build、lint、type check、生成物driftを実行します。

### 保証付き実行（assured）

複数module、公開API、DB、IaC、dependency、共有UI、generator、永続要件、governance。変更固有のRisk-selected checkを追加します。

### 規制・高保証実行（regulated）

authentication、authorization、PII、confidential、data loss、不可逆なproduction操作、法令・契約上の統制、高額操作、または明示的な高保証要求。

この場合だけ、次を追加します。

- work item
- 一度だけの明示承認
- lifecycle document
- hash chain
- phase gate
- regulated audit

## 使い方

1. 必要なSkillsを対象repositoryの`.agents/skills`へコピーします。
2. repositoryをAI開発agentで開きます。
3. 実現したい結果を普段の言葉で相談します。

利用者がSkill名、work item、Python、test commandを指定する必要はありません。AIがprofileと必要checkを選び、実装、test、Commit Comment、PR、CI確認を行います。

## 標準配置

| 成果物 | 配置 | 役割 |
|---|---|---|
| Skills | `.agents/skills/<name>/` | 会話、要件、設計生成、review、commit |
| 永続要件 | `spec/requirements/requirements.json` | 現在状態の正本 |
| 人向け要件 | `docs/requirements/REQUIREMENTS.md` | 正本から生成 |
| as-built設計 | `docs/design/generated/` | 実装から生成 |
| ADR | `docs/decisions/` | 条件付きの長期判断 |
| review result | `governance/reviews/` | 変更時点のselected check証跡 |
| standards registry | `governance/standards/registry.json` | 公式資料の版と再確認期限 |
| 一時実行状態 | `.devflow/run/` | Git管理外、完了後削除 |
| regulated runtime | `governance/`, `tools/devflow.py`, `work/` | regulated profile限定 |

対象固有の`AGENTS.md`と`.codex/config.toml`は上書きしません。既存規則を維持し、必要部分だけを統合します。

## Skills一覧

用途、起動条件、依存関係は[Skills一覧](docs/SKILLS.md)を参照してください。
