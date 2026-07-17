# 詳細設計

## インターフェース

CLI: `install_reference.py --target PATH --profile NAME [--profile NAME...] [--apply] [--force]`。defaultはplan表示のみ。manifestはprofileごとの`source`/`destination` mappingを保持する。

## データモデル

manifestは`schema_version`、`standard_paths`、skill/agent `inventory`、`profiles`から成る。copy itemはresolved sourceとtarget-relative destinationのimmutable pairである。

## 制御・状態・例外

全mappingを展開し、destination重複とconflictを確認してからcopyする。unknown profile、invalid manifest、unsafe pathは`InstallError`とexit 2。identical fileはunchangedとして扱う。

## 認証・認可・入力検証

認証は不要。sourceはrepository root内、destinationは明示target内に限定し、root/home targetとsymlink sourceを拒否する。上書きは`--force`でのみ許可する。

## 観測可能性

各itemを`WOULD_COPY`、`COPY`、`UNCHANGED`、`CONFLICT`で表示し、最後にcountを出力する。CIはunit test、validator、catalog、auditで監視する。

## 移行・互換性

既存配置は変更しない。旧configのcustom agent mappingだけを除去し、standalone TOML discoveryへ移行する。installerはtargetのactive configを変更しないため後方互換性を保つ。
