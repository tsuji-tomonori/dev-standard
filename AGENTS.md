# Repository instructions

## Outcome

自然言語の依頼から、必要な要件、実装、test、as-built設計、レビュー、PR、CI確認までを完了する。結果と安全境界は明確にし、可逆な実装方法はAIに委ねる。

## Default workflow

feature、fix、refactor、design concern、incomplete ideaでは`$chat-first-development`を入口にする。

1. `$right-size-execution`で`direct`、`assured`、`regulated`を選ぶ。
2. 要件影響と設計影響を判定する。
3. 永続要件が変わる場合だけ`$maintain-canonical-requirements`を使う。
4. 変更固有のcheckだけを選択する。
5. 実装し、targeted verificationから開始する。
6. 対応対象では`$generate-implementation-design`でas-built設計を生成する。
7. `$inspect-quality-gates`でselected checkを確認する。
8. `governance/reviews/<change-id>.yaml`へreview結果を保存する。
9. `$japanese-git-commit-gitmoji`で構造化Commit Commentを作る。
10. PRを作成し、現在HEADのGitHub Actionsを確認する。

通常変更で恒久的な`work/<id>/`、変更ごとの実行計画、architecture文書、implementation log、test report、release report、retrospectiveを作らない。

## Required outputs

すべてのrepository変更で必須:

- 実際の成果物
- `docs/COMMIT-COMMENT.md`に従うCommit Comment
- selected check result: `governance/reviews/<change-id>.yaml`
- GitHub Actions等の外部CI結果

条件付きで維持:

- `spec/requirements/requirements.json`
- `docs/requirements/REQUIREMENTS.md`
- `docs/design/generated/`
- `docs/decisions/ADR-*.md`
- 恒久的な運用文書
- Issue

一時実行状態が必要な場合だけ`.devflow/run/`を使い、Git管理しない。

## Profile

### direct

局所的、可逆、外部副作用なし、critical riskなし。targeted test、build、lint、type、生成物driftを実行する。

### assured

複数module、公開契約、DB、IaC、dependency、共有UI、generator、永続要件、governance。変更固有のRisk-selected checkとrelated verificationを追加する。

### regulated

authentication、authorization、PII、confidential、data loss、irreversible production operation、法令・契約上の統制、高額操作、または明示的な高保証要求。

このprofileだけで次を使用する。

- `$govern-development-request`
- `$author-lifecycle-docs`
- `$authorize-autonomous-execution`
- work item
- hash chain
- phase gate
- regulated audit

## Requirements

永続要件の唯一の正本は`spec/requirements/requirements.json`である。

外部挙動、業務ルール、受入条件、非機能閾値、権限要求が変わる場合だけadd / update / retireを適用する。人向け要件は正本から生成し、直接編集しない。

要件影響はCommit Commentへ必ず`あり`または`なし`と理由を記録する。

## Design

FastAPI router、OpenAPI、SQL、CloudFormationその他の対応実装からas-built設計を生成し、source digestとdriftを検査する。

コードから生成可能な情報を手書き詳細設計として二重管理しない。将来の実装を制約し、コードだけでは理由が分からない判断だけADRにする。

設計影響はCommit Commentへ必ず`あり`または`なし`と理由を記録する。

## Checks

- `Invariant`: triggerに該当した場合はPass必須。
- `Risk-selected`: 変更riskから選択された場合だけblocking。
- `Advisory`: 修正、Issue化、residual riskのいずれかへ収束。
- `Periodic`: 個別PRではなく定期監査で扱う。

未選択項目をN/Aとして保存しない。CI結果、生ログ、coverage全文はGitへ複製しない。

check timing:

- 変更開始前: Impact Check
- 実装中: Fast Feedback Check
- PR前: Affected-scope Check
- Merge前: Revision Integrity Check
- Deploy後: Operational Check
- 定期: Governance Audit

## Commit Comment

形式は`docs/COMMIT-COMMENT.md`を正とする。

Commit CommentはChange Manifest、Requirement Impact Result、Design Impact Resultを代替し、次を必須とする。

- 目的
- 変更内容
- 要件影響
- 設計影響
- review result path
- 検証契約
- 互換性・残存リスク

CI結果は外部サービスを正本とし、まだ完了していないCIをPassと書かない。

## Safety boundaries

- secrets、PII、production dump、生CIログをGitへ含めない。
- 明示権限なしにproduction deploy、削除、公開、高額操作、mergeを行わない。
- 対象repository固有のbuild、test、ownership、commit規約を維持する。
- test、型、lint、security controlを弱めてgateを通さない。
- 必要な結論を裏付ける証拠が揃ったら探索を止める。

## Definition of done

- 要求された成果が実装されている。
- 要件影響と設計影響がCommit Commentに記録されている。
- 必要な正本と生成物が更新されている。
- selected check resultがreview YAMLにある。
- blocking checkがPassしている。
- advisoryの扱いが決まっている。
- 現在HEADの外部CIが成功している。
- CI結果や一時状態をrepositoryへ複製していない。
