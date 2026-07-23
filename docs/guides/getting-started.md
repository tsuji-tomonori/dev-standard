# 導入とSkills一覧

## 導入方法

通常は対象リポジトリをAI開発agentで開き、次のように依頼します。

> dev-standardのdefault profileを導入し、既存の指示と構成を維持したまま統合して。

手動で確認する場合はdry-run後に適用します。

```bash
python tools/install_reference.py --target ../target-repository --profile default
python tools/install_reference.py --target ../target-repository --profile default --apply
```

`--profile`は複数指定できます。既存ファイルと内容が異なる場合は停止し、`--force`は差分を確認した後だけ使用します。

## 既定profile

`default`は自然言語の依頼から要件、実装、as-built設計、selected check、Commit Comment、PRまで進める最小構成です。認証・認可、PII、不可逆production操作などでは`regulated`を明示的に追加します。

配布内容の正本は[`distribution/manifest.json`](../../distribution/manifest.json)です。

## Skills一覧

| Skill | 用途 |
|---|---|
| `chat-first-development` | 通常依頼の入口とdelivery |
| `right-size-execution` | 実行profileと検証範囲の選択 |
| `calibrated-collaborative-listening` | 結果を変える曖昧さの確認 |
| `maintain-canonical-requirements` | 永続要件のadd・update・retire |
| `generate-implementation-design` | 実装由来のas-built設計生成 |
| `verify-against-engineering-standards` | 関連する標準checkの選択 |
| `inspect-quality-gates` | selected check結果の確認と保存 |
| `japanese-git-commit-gitmoji` | 日本語の構造化Commit Comment |
| `adversarial-review` | 高影響変更の独立反証review |
| `elicit-frontend-requirements` | UI要求の獲得 |
| `design-frontend-experience` | UI interaction設計 |
| `implement-frontend-experience` | UI実装 |
| `test-frontend-experience` | UI検証 |
| `govern-development-request` | regulated workの統制 |
| `author-lifecycle-docs` | regulated文書の作成 |
| `authorize-autonomous-execution` | 外部副作用と権限の承認 |
| `retrospect-and-improve` | 重大失敗時の改善 |
| `maintain-reference-repository` | この参照リポジトリ自身の保守 |

各Skillが利用する査読研究、規格、公式ガイダンス、実装例、ローカル方針の区分と確認結果は[Skills根拠資料一覧・整合性監査](../reference/skill-evidence-audit.md)を参照してください。

通常はSkill名を指定せず、実現したい結果を自然言語で依頼します。詳細な実行契約は[開発契約](../reference/development.md)を参照してください。
