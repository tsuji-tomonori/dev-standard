# Skills一覧

必要なフォルダを`<target>/.agents/skills/<name>/`へコピーする。`SKILL.md`のmetadataが自動起動条件を定めるため、通常はSkill名を指定せず、問題を自然言語で相談すればよい。

| Skill | 目的・起動条件 | 依存関係 | コピー元 |
|---|---|---|---|
| `adversarial-review` | 欠陥がある前提で要件、設計、実装、テスト、文書の正しさを批判的に検証する | 単体利用可 | `.agents/skills/adversarial-review` |
| `author-lifecycle-docs` | 要求ごとの工程文書、正本差分、計画、トレーサビリティを保守する | 統制実行基盤一式 | `.agents/skills/author-lifecycle-docs` |
| `authorize-autonomous-execution` | 要件差分と実行計画に対する要求者の一度だけの明示承認を記録する | 統制実行基盤一式 | `.agents/skills/authorize-autonomous-execution` |
| `calibrated-collaborative-listening` | 迎合、上から目線、意味の欠落を避けながら曖昧な意図を推定し、穏やかに確認する | 単体利用可 | `.agents/skills/calibrated-collaborative-listening` |
| `chat-first-development` | 普通の相談を、導入、要件、設計、実装、テスト、PR、CIまでの自動フローへ載せる | 開発フレームワーク。統制実行基盤一式を推奨 | `.agents/skills/chat-first-development` |
| `design-frontend-experience` | 承認済み要件から情報設計、操作、状態、レスポンシブ、アクセシビリティ、視覚、トークン、コンポーネントを実装可能な詳細設計へ落とす | UI要求獲得Skill、工程文書Skill、既存デザインシステムを推奨 | `.agents/skills/design-frontend-experience` |
| `elicit-frontend-requirements` | デザイン用語を知らない要求者から、人間中心で検証可能なフロントエンド要件を獲得する | 傾聴Skillと要件正本化Skillを必須利用 | `.agents/skills/elicit-frontend-requirements` |
| `generate-implementation-design` | FastAPIのシーケンス/OpenAPI/SQL設計とCDKのCloudFormation設計を生成し、差分を検査する | 同梱のPyYAML/SQLGlot依存固定 | `.agents/skills/generate-implementation-design` |
| `govern-development-request` | 一度だけの承認で統制されたライフサイクル全体を進行する | 統制実行基盤一式 | `.agents/skills/govern-development-request` |
| `implement-frontend-experience` | 要件と詳細設計から、状態・意味・フォーカス・レスポンシブ規則を失わず本番フロントエンドへ実装する | UI設計Skill、工程文書Skill、対象リポジトリのテスト基盤 | `.agents/skills/implement-frontend-experience` |
| `inspect-quality-gates` | 決定的な工程ゲートと証跡契約を検査する | 統制実行基盤一式 | `.agents/skills/inspect-quality-gates` |
| `japanese-git-commit-gitmoji` | リポジトリ規約に従う日本語gitmojiコミットを作る | 単体利用可 | `.agents/skills/japanese-git-commit-gitmoji` |
| `maintain-canonical-requirements` | 意図を探り、原子的なadd/update/retire要件をwork item外へ永続化する | 傾聴Skillを推奨。schemaとscriptを同梱 | `.agents/skills/maintain-canonical-requirements` |
| `retrospect-and-improve` | 振り返りと、承認対象にできる改善提案を生成する | 統制実行基盤一式 | `.agents/skills/retrospect-and-improve` |
| `right-size-execution` | scope、assurance、compute、modeを独立に推定し、新証拠に基づく単軸Expand、成功後停止、選択漏れと効率を監査する | 単体利用可。work item・標準選択には統制実行基盤を推奨 | `.agents/skills/right-size-execution` |
| `test-frontend-experience` | 要件・設計・実装に対し、機能、状態、アクセシビリティ、ユーザビリティ、視覚、レスポンシブ、性能を証拠付きで検証する | UI実装Skill、標準検証Skill、批判的レビューSkillを推奨 | `.agents/skills/test-frontend-experience` |
| `verify-against-engineering-standards` | 版管理されたSWEBOK・クラウド公式資料と証拠ベースのチェックリストで成果物を検証する | 出典台帳。批判的レビューSkillを推奨 | `.agents/skills/verify-against-engineering-standards` |

## 組合せ

- 原子的要件: `maintain-canonical-requirements` + `calibrated-collaborative-listening`
- フロントエンド要求獲得: `elicit-frontend-requirements` + `calibrated-collaborative-listening` + `maintain-canonical-requirements`
- フロントエンド全工程: `elicit-frontend-requirements` → `design-frontend-experience` → `implement-frontend-experience` → `test-frontend-experience`
- 実装由来設計: `generate-implementation-design`
- 標準検証: `verify-against-engineering-standards` + `adversarial-review`
- 適正規模実行: `right-size-execution`（Skillフォルダ内にpolicy、schema、CLI、benchmarkを同梱）
- 3本柱のフレームワーク: 上記を支える6つのSkills（`development-framework`）
- 会話だけで進む開発: 3本柱 + `chat-first-development`（`chat-first`）
- 統制ライフサイクル一式: 全Skills + [導入ガイド](INSTALLATION.md)の実行基盤

フロントエンド全工程では、要求者へ色・余白・コンポーネント名などの設計判断を直接委ねない。要求獲得で利用状況、作業、失敗影響、制約、価値の優先順位を明らかにし、設計以降で専門的判断へ変換する。

Codexのカスタムレビューagentsは`.codex/agents`に分離している。Skillsはこれらのagentsがなくても移植・実行できる。
