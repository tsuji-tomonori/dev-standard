# コミットメッセージ契約

このリポジトリでは`Commit Comment`と呼びますが、Gitの正式名称はcommit messageです。変更ごとの別manifestや実装reportを作らず、最終コミットへ影響判定と検証契約を集約します。

## 形式

```text
<gitmoji> <type>(<scope>): <日本語の要約>

目的:
- <得られる結果>

変更内容:
- <主要変更>

要件影響:
- あり | なし
- 要件ID: <REQ IDs | none>
- 理由: <判定根拠>

設計影響:
- あり | なし
- 対象: <生成設計、ADR、公開契約、構成 | none>
- 生成設計: <path | 対象外>
- ADR: <ADR ID | 不要とした理由>

チェックリスト:
- governance/reviews/<change-id>.yaml

検証契約:
- GitHub Actions: <workflowまたはrequired check>
- ローカル: <必要時だけ>
- 結果の正本: GitHub Actions等

互換性・残存リスク:
- <互換性、移行、未検証範囲、既知制約>

Requirements: <REQ IDs | none>
Design-Impact: <none | generated | adr | contract | governance | mixed>
Review-Checklist: governance/reviews/<change-id>.yaml
Refs: <Issue / ADR。該当時だけ>
```

## 規則

- 1行目は一つの主目的を表す。
- 要件影響と設計影響は必ず判定し、`なし`でも理由を書く。
- 変更内容は意味単位に絞り、ファイル一覧や作業ログを貼らない。
- CIが完了する前にPassと書かず、実行されるworkflowまたはrequired checkを記載する。
- 生ログ、coverage全文、scanner出力を貼らない。
- squash mergeではPR全体の内容を最終squash commitへ統合する。
