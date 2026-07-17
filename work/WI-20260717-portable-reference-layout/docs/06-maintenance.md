# 保守・変更・廃止計画

## 所有者と保守体制

repository ownerがmanifest、installer、guideを一体で保守する。skill/agent追加時はinventoryとprofile、validator/testを同一PRで更新する。

## 依存関係・脆弱性・更新方針

installerはPython標準libraryのみ。governance profileの`requirements.txt`はtargetで明示installする。official Codex path変更は公式manual確認後の別work itemで反映する。

## 互換性・移行方針

target側更新はdry-runでdriftを確認し、review後に`--apply --force`する。active target configは常にtarget ownerがmergeする。

## EOL・データ廃棄

配布asset削除はmanifestから外し、既導入先ではmanual removalとする。installerにdelete機能を持たせずtarget-owned dataを保護する。
