# コントリビューションガイド

## 基本フロー

1. 依頼内容とrepositoryの指示を確認し、[docs/FLOW.md](docs/FLOW.md)に従って`direct`、`assured`、`regulated`を選択する。
2. 実際の成果物を更新する。永続要件が変わる場合だけ`spec/requirements/requirements.json`を更新し、対応対象の実装からas-built設計を生成する。
3. `governance/checks/catalog.yaml`から変更に必要なcheckだけを選び、結果を`governance/reviews/<change-id>.yaml`へ保存する。未選択checkをN/Aとして登録しない。
4. 変更範囲に応じたtest、build、lint、type check、生成物driftを実行し、Pull Request前に`make verify`でrepository契約を確認する。
5. 目的別にstageし、`.agents/skills/japanese-git-commit-gitmoji/SKILL.md`と[docs/COMMIT-COMMENT.md](docs/COMMIT-COMMENT.md)に従う日本語gitmoji Commit Commentを作成する。
6. Pull Requestには変更内容、理由・利用者影響、実行profile、review YAML path、検証契約、残存riskを記載する。CIの実結果はGitHub Actionsを正本とし、生ログをrepositoryへ複製しない。

## 実行プロファイル別の追加事項

### 直接実行

局所的で可逆、外部副作用のない変更に使用する。恒久的な`work/<id>/`、初回承認、lifecycle文書、phase gateを作成しない。

### 保証付き実行

複数module、公開契約、DB、IaC、dependency、共有UI、generator、永続要件、governanceへ影響する変更に使用する。変更固有のRisk-selected checkを追加するが、恒久的な`work/<id>/`と通常の初回承認は要求しない。

### 規制・高保証実行

authentication、authorization、PII、data loss、不可逆なproduction操作、法令・契約統制、高額操作、または明示的な高保証要求に該当する場合だけ使用する。この場合に限り、`tools/devflow.py init`でwork itemを作成し、必要なlifecycle文書、一度だけの明示承認、hash chain、phase gate、regulated auditを追加する。

承認や証跡を捏造しないでください。公開repositoryへ秘密情報、個人データ、会話transcript、production証跡、CI生ログを追加しないでください。外部書込み、公開、merge、削除、production操作は、依頼または明示承認で与えられたauthority boundary内だけで行ってください。
