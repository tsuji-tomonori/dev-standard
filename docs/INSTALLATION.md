# Skills・agents導入ガイド

## 推奨手順: コピーして開き、相談する

利用者がインストーラーを実行する必要はない。

1. `.agents/skills`を対象リポジトリの同じ相対パスへコピーする。
2. 対象リポジトリをAI開発エージェントで開く。
3. 実現したい結果を普段の言葉で相談する。

利用者にPython、インストーラー、初期設定、テスト、Git、ライフサイクルコマンドを実行させない。AIが対象を調査し、リポジトリ内の前提環境を作り、対象固有の要件正本と出典台帳を初期化し、内部コマンドを実行する。

Skillsをコピーしても、この参照リポジトリ固有の製品要件はコピーしない。初回利用時に`$maintain-canonical-requirements`が同梱の空テンプレートから対象固有の`spec/requirements/requirements.json`を作り、`docs/requirements/REQUIREMENTS.md`を生成する。`$verify-against-engineering-standards`も同様に、同梱の公式資料台帳から`governance/standards/registry.json`を初期化する。

決定的な統制フローをすべて使う場合は、相対パスを保って次もコピーする。

- 読取専用レビュー用の`.codex/agents`
- 方針、チェックリスト、出典台帳を持つ`governance`
- `docs/templates`
- `tools`
- `checklist.xlsx`
- `requirements.txt`

対象に`AGENTS.md`がなければ、`distribution/snippets/AGENTS.governance.md`を`AGENTS.md`としてコピーする。すでに存在する場合は上書きせず、AIが互換性を確認した区切り付きの節だけをレビュー対象の変更として追加する。`.codex/config.toml`も同様に保護する。

## 現行の標準配置

| 成果物 | このリポジトリのコピー元 | 対象リポジトリ | 規則 |
|---|---|---|---|
| 再利用可能なSkill | `.agents/skills/<name>/` | `<target>/.agents/skills/<name>/` | リポジトリ単位の移植用標準配置 |
| 永続要件 | Skill同梱テンプレート | `<target>/spec/requirements/requirements.json` | 対象固有、初回受付時に生成 |
| 生成要件文書 | 要件正本 | `<target>/docs/requirements/REQUIREMENTS.md` | 直接編集しない |
| 生成詳細設計 | ソース/OpenAPI/SQL/CFn | `<target>/docs/design/generated/` | ソースdigestと差分を検査 |
| 出典台帳 | Skill同梱台帳または統制プロファイル | `<target>/governance/standards/registry.json` | 公式資料、版、確認日、差分、更新間隔を保持 |
| Codexカスタムagent | `.codex/agents/<name>.toml` | 同じ相対パス | 任意のプロジェクト単位レビュー担当 |
| Codex hooks | `.codex/hooks/`、`.codex/hooks.json` | 同じ相対パス | 任意の信頼済みプロジェクト連携 |

リポジトリ用Skillsは`.agents/skills`へ置き、`.codex/skills`には置かない。個人用Skillsは`$HOME/.agents/skills`を利用できるが、このコレクションはグローバル領域へ書き込まない。

## コピープロファイル

| プロファイル | 用途 | コピー内容 |
|---|---|---|
| `requirements` | 対話、言語化、原子的な永続要件 | 要件正本管理と傾聴のSkills |
| `implementation-design` | FastAPI/CDKの実装由来設計 | 詳細設計生成Skill |
| `right-size-execution` | Estimate／Execute／Expandと効率計測だけを利用 | policy、schema、CLI、benchmarkを同梱した単一Skill |
| `standards-verification` | SWEBOK・クラウドのベストプラクティス検証 | 標準検証と批判的レビューのSkills |
| `development-framework` | 3つの品質保証をすべて利用 | 上記を支える6つのSkills |
| `chat-first` | 普通の相談から全工程を自動実行 | 開発フレームワークと会話起点の統括Skill |
| `adversarial-review` | 独立した批判的な正しさのレビュー | 批判的レビューSkill |
| `communication` | 傾聴だけを利用 | 傾聴Skill |
| `commit-style` | 日本語gitmojiコミットだけを利用 | コミット形式Skill |
| `skills` | すべての移植用Skills | `.agents/skills` |
| `agents` | 読取専用Codexレビュー担当を利用 | `.codex/agents` |
| `governance` | 決定的工程、チェック、承認、監査を利用 | Skills、agents、実行基盤、テンプレート、依存固定、統合用参照 |
| `codex-hooks` | ライフサイクルhookを利用 | hookスクリプトと宣言 |
| `full` | 完全な参照セットを利用 | 全Skills、agents、hooks、統制実行基盤 |

対応関係の正本は[`distribution/manifest.json`](../distribution/manifest.json)である。

## 依存関係と自動初期化

- 傾聴、要件正本、批判的レビュー、出典台帳の検証は、Python標準ライブラリまたは自然言語の指示だけを使う。
- `right-size-execution`はSkillフォルダ単体で動作し、`governance`と組み合わせるとtask固有のcheck選択をwork item初期化へ自動適用する。
- 実装設計は、自身の`requirements.txt`でPyYAMLとSQLGlotを固定する。AIが生成器を使う場合だけリポジトリ内環境へ準備する。
- 統制Skillsは`tools/devflow.py`、`checklist.xlsx`、ルートの`requirements.txt`も使う。
- Skillフォルダだけがある場合、会話起点Skillは軽量な`work/<id>`記録を使うが、永続カタログは`work/`外で維持する。

不足する自動化はAIの導入作業であり、利用者への質問ではない。導入時も対象所有ファイルの上書き、検査の弱体化、本番デプロイ、PRのマージ、明示権限のないグローバル設定変更は行わない。

## 保守者向け任意インストーラー

manifest駆動のインストーラーは保守者とCI向けであり、利用者の通常フローには含めない。既定は書込みを行わないプレビューである。

```bash
python3 tools/install_reference.py \
  --target /absolute/path/to/target-repository \
  --profile development-framework
```

レビュー済み計画を適用する場合:

```bash
python3 tools/install_reference.py \
  --target /absolute/path/to/target-repository \
  --profile development-framework \
  --apply
```

既存ファイルの内容が異なる場合、インストーラーは一件も書き込む前に停止する。`--force`は別途レビューした置換だけに使う。`/`、ホームディレクトリ、グローバルSkill領域を対象にしない。

## 更新と削除

新しいコレクションとの比較には、再コピーまたはインストーラーを使う。要件はカタログ全体の置換ではなく、版競合を検査したadd/update/retire差分で更新する。自動化が対象所有ファイルを削除しないよう、コピーしたSkillsの削除は手動で行う。永続要件は履歴を消さず廃止する。

## 公式の配置資料

- [Codex Skills](https://learn.chatgpt.com/docs/build-skills)
- [Codexカスタムagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Codexプロジェクト設定](https://learn.chatgpt.com/docs/config-file/config-basic)
