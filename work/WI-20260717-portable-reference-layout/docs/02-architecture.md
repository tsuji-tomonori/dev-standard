# アーキテクチャ

## コンテキストと境界

本repositoryを配布元、任意のrepositoryを導入先とする。portable skill、Codex固有agent、任意hook、governance runtimeを独立したprofileとして扱う。対象固有設定は信頼境界外として自動mergeしない。

## コンポーネントと責務

| コンポーネント | 責務 | 所有データ | 依存先 | SLO |
|---|---|---|---|---|
| Source collections | skill/agent/runtimeの正本 | versioned files | Git | repository availability |
| Distribution manifest | profile別source/destination contract | JSON mapping | source collections | schema validation |
| Safe installer | plan、conflict検出、明示適用 | copy plan | manifest, filesystem | atomic preflight |
| Merge references | target固有設定への統合候補 | Markdown/TOML snippets | maintainer review | not auto-activated |

## データフローと信頼境界

installerはmanifestを読み、sourceをrepository root内へ限定し、target配下のdestinationへ展開する。全conflictをwrite前に検出する。targetの`AGENTS.md`と`.codex/config.toml`には触れず、非activeなreference fileを出力する。

## 可用性・性能・拡張性

静的file copyのため常時稼働SLOはない。profile追加はmanifest entryで拡張でき、重複destinationはplan時に排除する。

## 代替案とトレードオフ

shell copyのみでは依存と衝突を検証できないため、manual手順に加えPython標準library installerを採用した。config自動mergeは便利だがtarget意味を壊すため不採用とした。

## 失敗・縮退・復旧

missing/symlink source、path escape、unknown profile、既存差分をfail closedとする。default dry-runで復旧不要とし、適用後のrollbackはtarget側version controlで行う。
