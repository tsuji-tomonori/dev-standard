# 統制・監査モデル

## 信頼境界

自然言語のskillとagentは作業方法を指示します。合否判定、ハッシュ、承認チェーン、状態遷移は`tools/devflow.py`が決定論的に実行します。AIの自己申告をゲート証跡にしません。

## 成果物に結び付く承認

ゲートダイジェストは、次の正規化データからSHA-256で計算します。

- work item IDと工程
- 必須文書のパスとSHA-256
- 当該工程の全チェック結果

承認レコードはこのダイジェストを保持します。文書や判定が変わるとダイジェストも変わり、旧承認は現行ゲートに一致しなくなります。

## 改ざん検知

`approvals.jsonl`と`events.jsonl`は、各レコードに前レコードのハッシュを含むチェーンです。途中の編集、削除、並べ替えは`audit`で検出されます。これは改ざんを防止する署名ではなく、リポジトリ内の不整合を検出する仕組みです。高保証用途では、署名付きコミット、保護ブランチ、外部監査ログを追加してください。

## チェック結果

- `undecided`: ゲート失敗
- `not-applicable`: 具体的なN/A根拠が必要
- `applicable + pass`: reviewer、reviewed_at、到達可能な証跡が必要
- `applicable + fail`: Issue IDと期限付き例外承認が必要
- 案件Criticalの例外: security-owner、release-owner、governance-ownerのいずれかが必要

## 自動振り返りとskill改善

Stop hookはアクティブwork itemのゲートを読み、作業ツリーとブロッカーを`reports/retrospectives/`へ保存します。同じブロッカーコードが複数セッションで再発すると改善候補を生成します。

改善候補は自動では恒久ルールになりません。

1. `improvement-list --status pending`で候補を確認する。
2. governance-ownerが`improvement-approve`を実行する。
3. Stop hookまたは`improvement-apply`が対象skillの`references/learned-rules.md`へ追記する。
4. 次回の同種作業でルールが有効か確認する。

この分離により、セッションごとの学習を自動化しつつ、悪意あるプロンプトや一度限りの失敗が恒久指示へ昇格することを防ぎます。
