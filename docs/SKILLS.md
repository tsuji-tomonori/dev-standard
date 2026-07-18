# Skills一覧

必要なフォルダを`<target>/.agents/skills/<name>/`へコピーする。`SKILL.md`のmetadataが自動起動条件を定めるため、通常はSkill名を指定せず、問題を自然言語で相談すればよい。

| Skill | 目的・起動条件 | 依存関係 | コピー元 |
|---|---|---|---|
| `adversarial-review` | 欠陥がある前提で要件、設計、実装、テスト、文書の正しさを批判的に検証する | 単体利用可 | `.agents/skills/adversarial-review` |
| `author-lifecycle-docs` | 要求ごとの工程文書、正本差分、計画、トレーサビリティを保守する | 統制実行基盤一式 | `.agents/skills/author-lifecycle-docs` |
| `authorize-autonomous-execution` | 要件差分と実行計画に対する要求者の一度だけの明示承認を記録する | 統制実行基盤一式 | `.agents/skills/authorize-autonomous-execution` |
| `calibrated-collaborative-listening` | 迎合、上から目線、意味の欠落を避けながら曖昧な意図を推定し、穏やかに確認する | 単体利用可 | `.agents/skills/calibrated-collaborative-listening` |
| `chat-first-development` | 普通の相談を、導入、要件、設計、実装、テスト、PR、CIまでの自動フローへ載せる | 開発フレームワーク。統制実行基盤一式を推奨 | `.agents/skills/chat-first-development` |
| `generate-implementation-design` | FastAPIのシーケンス/OpenAPI/SQL設計とCDKのCloudFormation設計を生成し、差分を検査する | 同梱のPyYAML/SQLGlot依存固定 | `.agents/skills/generate-implementation-design` |
| `govern-development-request` | 一度だけの承認で統制されたライフサイクル全体を進行する | 統制実行基盤一式 | `.agents/skills/govern-development-request` |
| `inspect-quality-gates` | 決定的な工程ゲートと証跡契約を検査する | 統制実行基盤一式 | `.agents/skills/inspect-quality-gates` |
| `japanese-git-commit-gitmoji` | リポジトリ規約に従う日本語gitmojiコミットを作る | 単体利用可 | `.agents/skills/japanese-git-commit-gitmoji` |
| `maintain-canonical-requirements` | 意図を探り、原子的なadd/update/retire要件をwork item外へ永続化する | 傾聴Skillを推奨。schemaとscriptを同梱 | `.agents/skills/maintain-canonical-requirements` |
| `retrospect-and-improve` | 振り返りと、承認対象にできる改善提案を生成する | 統制実行基盤一式 | `.agents/skills/retrospect-and-improve` |
| `right-size-execution` | scope、assurance、compute、modeを独立に推定し、新証拠に基づく単軸Expand、成功後停止、選択漏れと効率を監査する | 単体利用可。work item・標準選択には統制実行基盤を推奨 | `.agents/skills/right-size-execution` |
| `verify-against-engineering-standards` | 版管理されたSWEBOK・クラウド公式資料と証拠ベースのチェックリストで成果物を検証する | 出典台帳。批判的レビューSkillを推奨 | `.agents/skills/verify-against-engineering-standards` |

## 組合せ

- 原子的要件: `maintain-canonical-requirements` + `calibrated-collaborative-listening`
- 実装由来設計: `generate-implementation-design`
- 標準検証: `verify-against-engineering-standards` + `adversarial-review`
- 適正規模実行: `right-size-execution`（Skillフォルダ内にpolicy、schema、CLI、benchmarkを同梱）
- 3本柱のフレームワーク: 上記を支える6つのSkills（`development-framework`）
- 会話だけで進む開発: 3本柱 + `chat-first-development`（`chat-first`）
- 統制ライフサイクル一式: 全Skills + [導入ガイド](INSTALLATION.md)の実行基盤

Codexのカスタムレビューagentsは`.codex/agents`に分離している。Skillsはこれらのagentsがなくても移植・実行できる。
