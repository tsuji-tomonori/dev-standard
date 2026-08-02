# ADR-0003: AI coding agent向けassetを単一正本から生成する

- 状態: 採用
- Date: 2026-08-02
- Issue: #50

## 背景

repositoryのSkillとreviewerはCodex向け配置を正本としていた。Claude Code等のhost向け配置を人が複製すると、本文、参照、モデル選択、実行権限、更新時期が分岐する。一方、hostが読み込むdirectoryとmetadataは同一ではないため、正本をそのまま全hostに配置することもできない。

## 決定

`.agents/skills/`と`.codex/agents/`をrepositoryの単一正本とし、`distribution/host-adapters.json`の変換契約に従って`tools/generate_host_assets.py`がhost別packageを生成する。

- Codex packageは`.agents/skills/`と`.codex/agents/`を保持する。
- Claude Code packageは`.claude/skills/`と`.claude/agents/`を生成する。OpenAI固有metadataは配布せず、reviewerはモデル名を固定しないMarkdownへ変換する。
- `AGENTS.md`または`CLAUDE.md`への統合はinstallerがmanaged marker内だけを更新し、導入先の既存指示を保持する。
- `.github/workflows/host-assets.yml`は両hostを毎回再生成し、完成packageをGitHub Actions artifactとして公開する。
- `.devflow/generated/hosts/`、`.claude/skills/`、`.claude/agents/`はGit管理しない。pre-commitとCIの`check`は、これらの生成pathがtrackedになった場合や、同じ入力からbyte一致しない場合を失敗させる。

host固有assetの直接修正は行わない。変更は正本またはadapterに入れ、Actionsが再生成する。

## 却下した選択肢

### hostごとのSkillをすべてtrackする

即時利用できるが、同じ契約の重複と人手の同期を必要とし、今回解消するdriftを再発させるため却下した。

### 実行時に正本directoryへ直接生成する

未管理ファイルや人の変更を上書きする境界が不明確になるため却下した。生成先は専用pathへ限定する。

### symlinkでhost間を共有する

metadata差分を表現できず、archive、Windows、外部toolでの取り扱いも一貫しないため却下した。

## 結果

- Skill本文とreviewer契約は一箇所でreviewできる。
- host追加はadapterと変換testの追加として扱える。
- 利用者はActions artifactまたはinstallerから導入し、repositoryは展開後の複製を保持しない。
- 生成物をcommitする変更はlocal hookとGitHub Actionsの両方で失敗する。hookを回避してもPRは合格できない。

## 参照

- Codex Skills: https://learn.chatgpt.com/docs/build-skills
- Claude Code Skills: https://code.claude.com/docs/en/skills
- Claude Code subagents: https://code.claude.com/docs/en/sub-agents
