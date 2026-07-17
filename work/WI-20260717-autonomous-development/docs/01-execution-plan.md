# 自律実行計画

## 承認によって許可される範囲

この計画への初回承認は、`tsuji-tomonori/dev-standard` に対する以下の作業を、追加の工程承認なしで完了まで実施する権限を与える。

- ローカルfeature branchの作成、リポジトリ内ファイルの追加・変更・必要な旧指示の削除
- ローカルテスト、validator、audit、差分検査の実行
- GitHub feature branchへのpush、PR作成、PR本文・状態の更新
- 必須CI成功後のsquash mergeとfeature branch削除
- このwork itemの成果物、チェック結果、証跡、イベント、完了状態の更新

許可はこのリポジトリと本work itemの受入条件に限定する。課金サービスの契約・起動、秘密情報の公開、本番環境変更、第三者へのメッセージ、リポジトリ外データの削除は含まない。

## 実行原則

1. 要件と本計画を初回承認後に凍結する。
2. 次の未完了工程を自律的に選び、品質ゲートを満たすまで修正する。
3. 低リスクかつ可逆な判断は、要件適合、既存規約、最小変更の順で既定値を選び、決定記録に残す。
4. テスト失敗、レビュー指摘、CI失敗は追加承認を求めず、原因を修正して再検証する。
5. 権限境界外の操作だけが必要になった場合、その操作は行わず、代替を尽くした後にブロッカーとして報告する。

## 作業分解

### 1. ベースラインと移行設計

- mainのcommit、現行policy、approval digest、advance、audit、hooks、skills、docs、testsをベースライン化する。
- 初回承認の正本、凍結対象、後続ゲートの検査順序、旧work itemの扱いを決定記録にする。
- 現行の工程別承認参照を全文検索し、変更対象一覧を確定する。

完了条件: 設計文書から、承認前、承認直後、後続工程、要件改変時、旧work item時の状態遷移を一意に説明できる。

### 2. 決定論的ハーネス

- `governance/policy.json` を、intakeは承認なし、requirementsはrequester一件、後続工程は承認なしへ変更する。
- `docs/01-execution-plan.md` をrequirementsの必須文書へ追加する。
- 新規work itemにworkflow schema/modeを記録する。
- 初回承認の有効性を後続`advance`と`audit`で必ず再検査する。
- 全先行工程の現行ゲートを後続`advance`と`audit`で検査する。
- 旧schemaのwork itemを自動承認済みとみなさず、明示エラーまたは安全な移行経路を提供する。

完了条件: AUT-001〜AUT-011の単体・統合テストが成功する。

### 3. 統制文書とrepo-local skills

- `AGENTS.md`、README、FLOW、GOVERNANCE、CONTRIBUTING、該当hooks/custom agentsを単一承認モデルへ揃える。
- `govern-development-request` を「計画作成→初回承認→自走→closed」へ変更する。
- `record-governance-approval` は初回承認専用へ改名または置換し、役割を明確化する。
- `author-lifecycle-docs` と `inspect-quality-gates` に、計画完全性、要件凍結、先行ゲート検査を追加する。
- repo-local `calibrated-collaborative-listening` を追加し、SKILL.md、意味構造化手順、日本語パターン、評価rubric、研究根拠mapを収録する。
- 要件・実行計画の作成時に、曖昧さが実行経路を変える場合だけ傾聴skillを使うようAGENTSへ接続する。

完了条件: AUT-012、LIS-001〜LIS-008、NFR-006〜NFR-007をvalidatorとrubricで満たす。

### 4. テストと回帰検証

- requirementsのみ承認が必要なケースを追加する。
- 承認後の全工程自走ケースを追加する。
- 要件・計画改変で後続進行とauditが失敗するケースを追加する。
- 先行工程劣化、改ざん、旧schema、欠落計画、未承認実装のケースを追加する。
- 既存の証跡、N/A、例外、hash chain、改善反映の回帰テストを維持する。
- `make verify`、skill validation、旧承認文言の全文検索を実行する。

完了条件: ローカル必須検証が全成功し、警告または失敗を未処理で残さない。

### 5. GitHub反映と完了

- 変更を目的別の日本語gitmoji commitへ分割する。
- feature branchをpushし、要件、設計判断、変更概要、テスト、リスクを含むPRを作成する。
- CI失敗はログを確認し、権限境界内で修正、再pushする。
- 必須check成功後、squash mergeし、リモートfeature branchを削除する。
- main上のmerge結果とCIを確認し、work itemをclosedにして監査結果を残す。

完了条件: merge済みPR、成功した必須check、監査成功、closed状態を確認できる。

## 変更予定領域

| 領域 | 予定対象 |
|---|---|
| policy/harness | `governance/policy.json`, `tools/devflow.py` |
| templates/work item | `docs/templates/01-execution-plan.md`, work item documents/state/review/evidence |
| repo instructions | `AGENTS.md`, `README.md`, `docs/FLOW.md`, `docs/GOVERNANCE.md`, `CONTRIBUTING.md` |
| hooks/agents | `.codex/hooks/*`, `.codex/agents/*` の承認関連箇所 |
| governance skills | `.agents/skills/govern-development-request`, `author-lifecycle-docs`, `inspect-quality-gates`, 初回承認skill |
| listening skill | `.agents/skills/calibrated-collaborative-listening/**` |
| tests/validation | `tests/test_devflow.py`, `tools/validate_repo.py`、必要な追加テスト |

## 既定の判断

| 判断点 | 承認後の既定値 |
|---|---|
| 実装方式が複数ある | 公開API差分と変更量が最小で、テスト可能性が高い方式 |
| 文書とコードが矛盾する | 承認済み要件と実行計画を正とし、派生文書とコードを修正 |
| 低リスクな名称・配置 | 既存命名規約とskill-creator規約に合わせる |
| テスト失敗 | 原因を修正して再実行。テスト削除や閾値緩和で通さない |
| CI失敗 | ログを確認し、同一branchで修正を継続 |
| PR差分に追加改善を発見 | 受入条件に必要なら実施。無関係なら別候補として記録し本PRへ混ぜない |
| merge方式 | 必須check成功後にsquash merge |
| 既存個人skill | 内容を参照しrepo-local版を整備。差分が不要なら個人skillを無意味に更新しない |

## 検証コマンド

- `python -m unittest discover -s tests -v`
- `python tools/validate_repo.py`
- `python tools/devflow.py audit`
- `make verify`
- skill-creatorの`quick_validate.py`によるrepo-local skill検証
- `rg`による旧工程別承認指示、未入力token、要求ID、変更対象の検査
- GitHub Actions必須checkの確認

## rollback

- merge前: feature branch内で修正し、mainへ影響させない。
- merge後に重大回帰が判明: merge commitを打ち消す専用revert PRを作成し、同じ必須検証を通す。
- 承認・イベントの履歴は直接編集しない。誤記録は追記イベントで訂正する。

## 停止条件

次の場合だけ、未許可操作を実行せずブロッカーとして終了する。

- mainへのpush/PR/merge権限がない。
- branch protectionが必須の第三者レビューを要求し、自動的に満たせない。
- 受入条件達成に、計画外の課金、本番変更、秘密情報公開、データ削除、第三者連絡が不可欠になる。
- GitHubまたはCIの外部障害が継続し、再試行と代替検証で完了を証明できない。

通常の設計選択、実装詳細、テスト修正、CI修正、文書整合は停止理由にしない。

## 完了定義

- 28要求が検証済みでトレーサビリティが閉じている。
- 全選択チェック項目に適用判定、根拠、判定、証跡がある。
- 全工程の現行品質ゲートと初回承認が有効である。
- ローカル検証とGitHub Actionsが成功している。
- PRがsquash mergeされ、mainの状態を再確認している。
- work itemが`closed`で、auditが成功している。
