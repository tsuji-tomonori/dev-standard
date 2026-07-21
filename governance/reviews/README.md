# レビュー結果

このディレクトリには、変更ごとに**選択されたチェック結果だけ**を保存する。

check ID、class、timing、trigger、合格条件の正本は`governance/checks/catalog.yaml`である。Excelはこの正本から生成する人向け一覧とし、ID判定には使用しない。

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
- reviewを含むcommitを表す`source_ref: self`
- 使用したcatalogのversionとSHA-256 digest
- 完了したtimingと構造化されたimpact flag
- 選択されたcheck ID
- check class: `Invariant` / `Risk-selected` / `Advisory` / `Periodic`
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

`python governance/reviews/validate.py --root . --commit HEAD`は、現在のCommit Commentが`Review-Checklist`で指す**active reviewだけ**を完全検証する。schema、catalog version/digest、ID/class、blocking fail、Advisory処理、直接証拠、必須checkの選択漏れ、Commit Commentを確認する。

active reviewの`source_ref: self`は、review YAML自身を含むcommitを意味する。`commit:self`も同じcommitへ解決されるため、`HEAD`の移動で過去証拠の意味が変わらない。active reviewはcatalog digestと現行catalogの一致を検査する。

過去の`CHG-*.yaml`は変更時点の不変証拠であり、現行catalog、現在tree、現在HEADへ再束縛しない。過去証拠を再検証する場合は、そのcommitとcatalog digestをcheckoutして行う。

`completed_timings`と`impact_flags`からcatalogのtriggerを評価し、完了済みtimingの必須checkが`selected_checks`から省略された場合はFailとする。秘密情報検査のPassは、secret scan stepのあるworkflow証拠で直接裏付ける。

`as_built_adoption`はas-built標準を導入または拡張する変更で使用し、coverage、test構造、解析可能な実装規約、外部report集約をAdvisoryとして選択する。`e2e_change`はSQLを変えずE2E scenarioまたは状態assertだけを変更する場合に使用する。`quality_threshold_change`は定量閾値またはlinter delegation設定を変更する場合に使用し、標準・設定・委譲先の一致checkをRisk-selectedとして選択する。

`CHG-*.yaml`はこのリポジトリ固有の変更証跡であり、インストーラーは導入先へコピーしない。配布対象はcatalog、schema、validator、README、templateだけである。

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
