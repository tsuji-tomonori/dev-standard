# dev-standard開発参照集

他のリポジトリへ移植して使う、AI開発用のSkills・agents・標準・検証部品の参照集です。

## 提供するもの

- **要件管理**: 会話から永続要件だけを`spec/requirements/requirements.json`へ反映する
- **as-built設計**: 実装から詳細設計を生成し、生成元とのdriftを検査する
- **変更検証**: 変更リスクに応じたcheckだけを選び、PRとCIまで進める

通常の依頼は`chat-first-development`が`direct`、`assured`、`regulated`へ振り分けます。利用者がSkill名や内部コマンドを指定する必要はありません。

## 導入

対象リポジトリをAI開発agentで開き、次のように依頼します。

> dev-standardのdefault profileをこのリポジトリへ導入して、既存ルールと競合しないように統合して。

手動で確認する場合は、まずdry-runを実行します。

```bash
python tools/install_reference.py --target ../target-repository --profile default
python tools/install_reference.py --target ../target-repository --profile default --apply
```

既存の`AGENTS.md`や`.codex/config.toml`は自動上書きせず、必要な規則だけを統合します。

## 主な配置

| 配置 | 内容 |
|---|---|
| `.agents/skills/` | 移植可能なSkills |
| `.codex/agents/` | read-only reviewer等のCodex agents |
| `spec/requirements/` | 永続要件の正本 |
| `docs/standards/` | 人向け標準 |
| `governance/checks/` | check定義の正本 |
| `governance/reviews/` | 変更ごとのselected check結果 |
| `distribution/manifest.json` | 配布profile |

## 文書

- [導入とSkills一覧](docs/guides/getting-started.md)
- [開発契約](docs/reference/development.md)
- [コミットメッセージ契約](docs/reference/commit-message.md)
- [要件分類標準](docs/standards/REQUIREMENT-CLASSIFICATION.md)
- [as-built設計標準](docs/standards/AS-BUILT-DESIGN.md)
- [文書索引](docs/README.md)
