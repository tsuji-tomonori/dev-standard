# レビュー結果

このディレクトリには、変更ごとに**選択されたチェック結果だけ**を保存する。

## 目的

- PRレビュー時に、何を確認し、何を確認しなかったかを短時間で把握できるようにする。
- blocking check、advisory、N/A判断、残存リスクをGit履歴へ残す。
- CIログやテストレポートをリポジトリへ複製しない。

## ファイル名

```text
governance/reviews/<change-id>.yaml
```

例:

```text
governance/reviews/CHG-20260718-artifact-governance.yaml
```

`change-id`はPR番号に依存させず、ブランチ作成時またはレビュー開始時に確定する。

## 保存するもの

- profile: `direct` / `assured` / `regulated`
- review対象branchまたはPR
- 選択されたcheck ID
- check class: `Invariant` / `Risk-selected` / `Advisory`
- result: `pass` / `fail` / `na`
- 到達可能な証拠参照
- N/A・手動判断・advisoryの短い根拠
- 残存リスク

## 保存しないもの

- 未選択check
- 全カタログのN/A
- 単体テスト件数やテストログ全文
- coverage report全文
- build log
- scannerの生出力
- GitHub Actionsと同じ結果のコピー

CI結果はGitHub Actionsなどの外部サービスを正本とする。レビュー結果にはworkflow名、required check名、テストコード、生成物、Issue等への参照だけを記載する。

## 結果の意味

### pass

選択されたcheckを直接裏付ける証拠がある。

### fail

- `Invariant`またはblockingに選択された`Risk-selected`はmerge前に解消する。
- `Advisory`は、修正、Issue化、残存リスクとしての明示のいずれかを選ぶ。

### na

selectorで選択された後、具体的な事実により適用外と判明した場合だけ使用する。未選択をN/Aとして登録しない。

## メンテナンス

このファイルは変更時点の証跡であり、将来の現在状態へ合わせて更新しない。誤りを訂正する場合は新しいコミットで履歴を残す。
