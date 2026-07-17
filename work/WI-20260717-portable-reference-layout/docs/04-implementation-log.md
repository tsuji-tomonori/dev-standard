# 実装・構成管理記録

## 変更概要

standard directoryを維持しつつconfig重複を削除した。manifest、safe installer、移植guide、merge reference snippets、validator、testsを追加し、current surfaceの曖昧なlean表記をminimal promptへ変更した。

## 要求・設計との対応

| 変更 | 要求ID | 設計節 | コミット | レビュー |
|---|---|---|---|---|
| directory/config整理 | PORT-001/005 | ADR-001 | current PR commit | automated validation |
| manifest/installer/guide | PORT-002/003/004 | architecture/data flow | current PR commit | 5 installer tests |
| terminology/quality contract | PORT-006/007 | ADR-004 | current PR commit | full verify |

## セキュア実装・依存関係

runtime dependency追加なし。installerは標準libraryのみを使用し、source/destination containment、symlink拒否、write前conflict検出を実装した。

## 設計との差異

当初guideだけだったconfig mergeを、導入先に安全に残るnon-active reference snippetへ拡張した。承認済みscope内の安全性改善である。

## 実行したローカル検査

23 unit tests、repository validator、JSON parse、compileall、catalog check、audit、`make verify PYTHON=python3`を実行し全て成功した。
