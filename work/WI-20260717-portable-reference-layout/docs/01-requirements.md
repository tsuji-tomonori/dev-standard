# 要件定義

## 概要

本repositoryをself-hosting reference collectionとして整理する。portable skillは`.agents/skills`、Codex-specific custom agentは`.codex/agents`に置き、copy単位、依存、検証をmachine-readable manifestとguideで提供する。

## ステークホルダー

| 役割 | 関心事 | 承認責任 |
|---|---|---|
| requester/repository owner | 標準準拠、移植容易性、誤解のない用語 | 本要件と実行計画 |
| destination repository maintainer | 上書きなしの導入、必要componentだけ選択 | target側適用判断 |

## 機能要件

| ID | 要件 | 優先度 | 受入基準 |
|---|---|---|---|
| PORT-001 | current標準のdirectoryを維持する | Must | skills=`.agents/skills/<name>/SKILL.md`、agents=`.codex/agents/<name>.toml` |
| PORT-002 | repository用途をreference collectionとして明記する | Must | README冒頭にinventory、portable/Codex-specific区分がある |
| PORT-003 | copy元・copy先・依存・適用範囲を明記する | Must | installation guideとmanifestが一致する |
| PORT-004 | selected componentを安全にcopyできる | Must | installerはdefault dry-run、`--apply`でcopy、衝突時fail、`--force`だけ上書き |
| PORT-005 | custom agent登録の重複を除く | Must | standalone `.codex/agents`自動検出を使い、configに個別mappingを持たない |
| PORT-006 | 曖昧なlean prompt用語をcurrent surfaceから除く | Must | current docs/tests/validator/PRで`minimal prompt`または`outcome-first`を使用 |
| PORT-007 | 既存behaviorとquality gateを維持する | Must | full tests、validator、catalog、audit、GitHub Actions成功 |

## 非機能要件

| ID | 品質特性 | 測定方法 | 合格閾値 |
|---|---|---|---|
| PORT-N1 | Portability | temp targetへのinstall test | selected filesがexpected destinationへ一致copy |
| PORT-N2 | Safety | conflict/force test | defaultで既存fileを上書きしない |
| PORT-N3 | Discoverability | manifest/README validator | 全skill/agentがmanifest inventoryに存在 |
| PORT-N4 | Maintainability | standard pathsをconstant/test化 | path driftでtest failure |

## データ・法令・倫理要件

新しいsecret、個人data、network credentialを扱わない。installerは指定target以下だけにwriteし、symlink sourceやpath traversalを許可しない。

## リスクとトレードオフ

- config全体copyはtarget固有設定を壊すため行わず、必要snippetをguideで示す。
- governance skillsはruntime files依存があるため、standalone skillとprofileを分離する。
- historical work evidenceの`lean`表記は承認記録保全のため変更しない。

## 対象外・N/A判断

plugin packaging、global `$HOME/.agents/skills` installation、Windows専用shell installer、target config自動mergeは対象外。
