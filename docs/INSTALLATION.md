# Skills・agents導入ガイド

## 1. 推奨導入

通常のrepositoryでは、次をコピーして自然言語で相談する。

- `.agents/skills/chat-first-development`
- `.agents/skills/right-size-execution`
- `.agents/skills/calibrated-collaborative-listening`
- `.agents/skills/maintain-canonical-requirements`
- `.agents/skills/generate-implementation-design`
- `.agents/skills/verify-against-engineering-standards`
- `.agents/skills/inspect-quality-gates`
- `.agents/skills/japanese-git-commit-gitmoji`
- 必要時だけfrontendまたはadversarial-review Skills

利用者にPython、installer、test、Git、governance commandを実行させない。AIがrepository内で必要な準備を行う。

## 2. 既定成果物

対象repositoryには次の構造を使用する。

```text
spec/requirements/requirements.json      # 要件影響時だけ初期化・更新
docs/requirements/REQUIREMENTS.md        # 正本から生成
docs/design/generated/                    # 対応実装から生成
docs/decisions/                           # 条件付きADR
governance/reviews/                       # selected check result
governance/standards/registry.json        # versioned sources
.devflow/run/                              # gitignoreされた一時状態
```

すべての変更では、構造化Commit Commentとreview resultを作る。CI結果はGitHub Actions等へ保持し、repositoryへtest reportや生ログをコピーしない。

## 3. `work/`をコピーしない

通常のdirect / assuredでは恒久的な`work/<id>/`を使用しない。

再開用状態が必要な場合だけ`.devflow/run/`を使用し、変更完了後に削除する。

## 4. Regulated runtime

次の場合だけfull runtimeを追加する。

- authentication / authorization
- PII / confidential
- data loss
- irreversible production operation
- 法令・契約上の工程統制
- 高額外部操作
- 明示的な高保証要求

コピー対象:

- regulated専用Skills
- `.codex/agents`
- `governance/policy.json`
- `governance/checklist/catalog.json`
- `docs/templates`
- `tools/devflow.py`
- `checklist.xlsx`
- regulated用依存
- 必要時だけ`.codex/hooks`

既存の`AGENTS.md`と`.codex/config.toml`を上書きせず、互換性を確認した区切り付き節だけを追加する。

## 5. Profile

| profile | 用途 | 追加内容 |
|---|---|---|
| `direct` | 局所的・可逆・外部副作用なし | targeted verification |
| `assured` | 公開契約、DB、IaC、dependency、共有UI、generator、永続要件 | Risk-selected checkとrelated verification |
| `regulated` | critical risk、不可逆production、法令・契約統制 | work item、承認、phase gate、hash chain、audit |

## 6. Skills配置

| 成果物 | コピー元 | コピー先 |
|---|---|---|
| repository Skill | `.agents/skills/<name>/` | `<target>/.agents/skills/<name>/` |
| Codex reviewer | `.codex/agents/<name>.toml` | 必要時だけ同じ相対path |
| hook | `.codex/hooks/` | regulatedまたは明示利用時だけ |
| requirements template | owning Skill assets | 対象固有の正本へ初期化 |
| review result schema | `governance/reviews/` | 同じ相対path |
| standards registry | owning Skill assets | 対象固有台帳へ初期化 |

## 7. Commit Comment

対象repositoryのcommit規約を優先しつつ、本文へ次を追加する。

- 目的
- 変更内容
- 要件影響
- 設計影響
- review result path
- 検証契約
- 互換性・残存リスク

詳細は`docs/COMMIT-COMMENT.md`を参照する。

## 8. 更新

Skillsを更新する場合も、対象repository固有の指示と所有fileを維持する。

- 全Skillsを無条件に上書きしない。
- regulated runtimeを通常repositoryへ自動追加しない。
- requirement catalogを全置換しない。
- review resultの過去fileを現在状態へ合わせて書き換えない。
- 一時実行状態をGitへ追加しない。

## 9. 保守者向けinstaller

installerを使用する場合、既定profileは通常Skillsだけを含める。`regulated`または`full`は明示指定時だけ利用する。

既存fileの内容が異なる場合は書込み前に停止し、対象repository所有fileを無断置換しない。
