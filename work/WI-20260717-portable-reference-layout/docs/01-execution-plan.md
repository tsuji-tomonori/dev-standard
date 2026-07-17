# 自律実行計画

## 承認対象

- Work item: WI-20260717-portable-reference-layout
- タイトル: Portable skills and agents reference layout
- Profiles: CORE, AI-CONDITIONAL
- 初回承認者: requester（本変更依頼）

## 許可する操作

- repository docs/config/tools/tests/manifest/work evidenceの編集
- current PR branch更新、GitHub Actions確認、PR title/body/comment更新
- temp directoryでinstallerを検証

## 許可しない操作

- historical authorization artifactsの意味変更
- target repository既存fileのdefault上書き、home directory/global install
- current official pathから独自非標準pathへの移動

## 作業分解

| ID | 作業 | Target | Validation | Done |
|---|---|---|---|---|
| P1 | official directory standard確定 | Codex manual | source citation | paths決定 |
| P2 | reference information architecture | README, INSTALL.md | content/links | copy map明示 |
| P3 | manifestとinstaller | distribution, tools | temp/conflict tests | safe copy可能 |
| P4 | config重複除去 | .codex/config.toml | TOML/validator | standalone discovery |
| P5 | terminology修正 | current docs/tests/validator/PR | rg/test | lean ambiguityなし |
| P6 | lifecycle/PR evidence | work, GitHub | full verify/CI | closed/green |

## 外部副作用

PR #1のbranch、title、body、commentを更新する。rollbackは追加commitのrevertまたはPR close。

## 既定の判断

- `.agents/skills`をportable skill正本、`.codex/agents`をCodex agent正本として維持する。
- configはcopyせずsnippet提示。installerはdry-run default、explicit `--apply`、collision fail。
- standalone profileはlistening/commit skills、governance profileはruntime依存を含める。

## 検証計画

unit tests、temp install equality、collision/force、manifest inventory、TOML、18+ existing tests、catalog、validator、audit、GitHub Actions。

## 停止条件

official manualがpathを確定できない、またはPR write permissionが失われた場合のみblocker化する。

## 完了定義

- [ ] PORT-001〜007、PORT-N1〜N4が証跡付きで成功
- [ ] PR #1がupdated、mergeable、GitHub Actions success
- [ ] work item closed
