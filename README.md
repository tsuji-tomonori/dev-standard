# dev-standard

AI開発agentが、対象repositoryの既存運用を壊さずに使える軽量なSkills集です。既定profileは会話の入口と3本のガードレールだけを配布します。

## 1. durableな原子要件

永続要件の一次言語は[Quint](https://quint.sh/)です。`spec/requirements/requirements.qnt`を唯一の編集対象とし、型と不変条件を検査します。

## 2. 実装由来のas-built設計

現在の構造とinterfaceは実装artifactから決定的に生成します。生成文書を直接編集して実装との差を隠しません。

## 3. 変更に関係する検査だけ

変更と受入条件に対応するtest、lint、type check、build、generatorだけを選びます。CIがある場合は利用できますが、CIやmerge ruleの導入を要求しません。

## Quintから人向け文書まで

```text
requirements.qnt → requirements.json → REQUIREMENTS.md
skills.qnt       → skills.json       → FORMAL-SPECIFICATIONS.md
```

```bash
npm ci --ignore-scripts
python tools/quintflow.py generate
python tools/quintflow.py check
python tools/quintflow.py test
```

全18 Skillは`spec/skills/skills.qnt`の形式契約と1対1で対応します。形式モデルは、既定profileが4 Skillだけであること、portable blocking guardrailが3本だけであること、すべてのSkillがCIとmerge ruleを要求しないことを検査します。

## 導入

まずdry-runし、差分を確認してから適用します。

```bash
python tools/install_reference.py --target ../target-repository --profile default
python tools/install_reference.py --target ../target-repository --profile default --apply
```

`default`が配布するSkillは次の4つです。

- `chat-first-development`
- `maintain-canonical-requirements`
- `generate-implementation-design`
- `inspect-quality-gates`

installerは導入先の`.github/`、branch、merge設定を追加も変更もしません。既存の`AGENTS.md`または`CLAUDE.md`は管理marker内だけを更新し、その他の記述を維持します。

詳細は[導入とSkills一覧](docs/guides/getting-started.md)、[形式仕様](docs/reference/FORMAL-SPECIFICATIONS.md)、[開発契約](docs/reference/development.md)を参照してください。
