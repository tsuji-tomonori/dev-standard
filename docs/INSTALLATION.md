# Skills・agents導入ガイド

## 1. 推奨手順: コピーして開き、相談する

通常のrepositoryでは、次をコピーして自然言語で相談する。

- `.agents/skills/chat-first-development`
- `.agents/skills/right-size-execution`
- `.agents/skills/calibrated-collaborative-listening`
- `.agents/skills/maintain-canonical-requirements`
- `.agents/skills/generate-implementation-design`
- `.agents/skills/verify-against-engineering-standards`
- `.agents/skills/inspect-quality-gates`
- `.agents/skills/japanese-git-commit-gitmoji`
- `docs/standards/REQUIREMENT-CLASSIFICATION.md`
- 必要時だけfrontendまたはadversarial-review Skills

利用者がインストーラーを実行する必要はない。利用者にPython、installer、test、Git、governance commandを実行させず、AIがrepository内で必要な準備を行う。

`maintain-reference-repository`はこのsample / reference collection自身を保守するためのSkillであり、通常の導入先profileへ自動追加しない。

## 2. 既定成果物

対象repositoryには次の構造を使用する。

```text
spec/requirements/requirements.json                 # 要件影響時だけ初期化・更新
docs/requirements/REQUIREMENTS.md                   # 正本から生成
docs/standards/REQUIREMENT-CLASSIFICATION.md        # product/projectとdocumentation NFRの分類
docs/design/generated/                              # 対応実装から生成
docs/decisions/                                     # 条件付きADR
governance/reviews/                                 # selected check result
governance/standards/registry.json                  # versioned sources
.devflow/run/                                        # gitignoreされた一時状態
```

すべての変更では、構造化Commit Commentとreview resultを作る。CI結果はGitHub Actions等へ保持し、repositoryへtest reportや生ログをコピーしない。

文書の存在、内容、鮮度、更新、配布、廃止に関する義務は、原則としてsoftware projectのnonfunctional requirementとして要件正本へ置く。文書file自体を要件の第二正本にしない。

## 3. `work/`をコピーしない

この参照repositoryはliveな`work/<id>/`を配布しない。通常のdirect / assuredでは導入先にも恒久的な`work/<id>/`を作らない。

再開用状態が必要な場合だけ`.devflow/run/`を使用し、変更完了後に削除する。

regulatedを選択した導入先だけが、portable runtimeから自身の`work/<id>/`を生成する。参照repositoryの過去案件や承認記録をsampleとしてコピーしない。

## 4. 規制・高保証実行基盤

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

## 5. 実行プロファイル

| profile | 用途 | 追加内容 |
|---|---|---|
| `direct` | 局所的・可逆・外部副作用なし | targeted verification |
| `assured` | 公開契約、DB、IaC、dependency、共有UI、generator、永続要件 | Risk-selected checkとrelated verification |
| `regulated` | critical risk、不可逆production、法令・契約統制 | 導入先work item、承認、phase gate、hash chain、audit |

## 6. Skills配置

| 成果物 | コピー元 | コピー先 |
|---|---|---|
| repository Skill | `.agents/skills/<name>/` | `<target>/.agents/skills/<name>/` |
| Codex reviewer | `.codex/agents/<name>.toml` | 必要時だけ同じ相対path |
| hook | `.codex/hooks/` | regulatedまたは明示利用時だけ |
| requirements template | owning Skill assets | 対象固有の正本へ初期化 |
| requirement classification | `docs/standards/REQUIREMENT-CLASSIFICATION.md` | 同じ相対path |
| review result schema | `governance/reviews/` | 同じ相対path |
| standards registry | owning Skill assets | 対象固有台帳へ初期化 |

## 7. コミットコメント

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
- reference repository専用Skillをportable defaultへ混入させない。

この参照collection自身を更新するときは`maintain-reference-repository`を使用し、portable asset、project NFR、documentation、work境界、distribution、互換性を確認する。

## 9. 保守者向けinstaller

installerを使用する場合、既定profileは通常Skillsと要件分類標準だけを含める。`regulated`または`full`は明示指定時だけ利用する。

既存fileの内容が異なる場合は書込み前に停止し、対象repository所有fileを無断置換しない。
