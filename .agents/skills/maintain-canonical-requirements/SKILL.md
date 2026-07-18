---
name: maintain-canonical-requirements
description: Discover, articulate, atomize, and persist durable product requirements through natural conversation. Use only when user-visible behavior, business rules, acceptance criteria, nonfunctional thresholds, authority, support, or operational guarantees change. Maintain spec/requirements/requirements.json as the authority, generate human-readable docs, and record the applied requirement impact in the Commit Comment without creating a permanent work item.
---

# Maintain Canonical Requirements

会話から、今後も維持する必要がある製品要求だけを正本へ反映する。

## Authority

- `spec/requirements/requirements.json`: 永続要件の唯一の正本
- `docs/requirements/REQUIREMENTS.md`: 人向けの生成表示。直接編集しない
- Commit Comment: その変更時点の要件影響と適用したID
- Git履歴: add / update / retire差分の履歴

`work/<id>/`、変更ごとの要件文書、適用後の差分コピーを正本として使用しない。

## 更新する条件

次のいずれかが変わる場合に使用する。

- 利用者向けの振る舞い
- 業務ルール
- 受入条件
- 非機能要求の閾値
- 認証・認可・privacy要求
- support対象
- 運用上の保証
- 明示的な禁止事項

通常は更新しない例:

- 外部挙動を変えないrefactor
- test追加
- lint・type修正
- 既存要件へ戻すbug fix
- 生成文書だけの再生成
- CI・Skill・開発補助の変更で製品要求が変わらない場合

ただしCommit Commentには`要件影響: なし`と理由を必ず記録する。

## Conversation workflow

1. ユーザーの目的、対象、制約、例外、受入条件を確認する。
2. 結果を変える曖昧さだけを一問で確認し、可逆な詳細は既定値を置く。
3. 一つの主体、一つの行為、一つの対象、一つの検証可能な義務へ原子化する。
4. 現在の正本と比較し、`add`、`update`、`retire`を作る。
5. base catalog revisionとitem revisionの競合を検査する。
6. 完全なcandidateを検証してから原子的に置換する。
7. 人向け文書を再生成し、byte driftを検査する。
8. requirement IDを実装、test、生成設計へ接続する。
9. Commit Commentの要件影響節へ、判定、ID、理由を記録する。

承認が必要なのは、要件の意味、外部副作用、権限境界、不可逆性が新しく変わる場合だけである。trace path、実装順序、使用tool、test file名の変更を要件承認の失効理由にしない。

## Atomicity

- 一つのrequirement IDに独立した複数義務を入れない。
- acceptance criteriaを必須とする。
- IDと履歴を維持する。
- 削除は`retire`とし、過去の正本を消さない。
- stale catalog revisionとpartial updateを拒否する。
- consequenceの大きいproduct choiceを黙って推測しない。

## Temporary proposal

承認前の差分を一時保存する必要がある場合だけ`.devflow/run/<change-id>/requirements-delta.json`を使用できる。この領域はGit管理せず、正本適用後に削除する。

## Completion

- 正本がschemaに適合する。
- add / update / retireが競合なく適用される。
- 人向け文書が正本から再生成される。
- requirement IDが実装・test・必要な生成設計へ到達できる。
- Commit Commentへ要件影響、ID、理由が記録される。
- 一時差分が正本として残っていない。
