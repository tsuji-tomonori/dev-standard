# コントリビューションガイド

## 参照repositoryとしての前提

このrepositoryは導入先productのlive projectではなく、移植可能なSkills、agents、標準、governance、installerのsample / reference collectionです。

変更前に[`maintain-reference-repository`](.agents/skills/maintain-reference-repository/SKILL.md)の視線を適用してください。top-levelの`work/`、実案件のapproval chain、変更ごとのimplementation logやtest reportは追加しません。

## 基本フロー

1. 依頼内容とrepositoryの指示を確認し、[docs/FLOW.md](docs/FLOW.md)に従って`direct`、`assured`、`regulated`を選択する。
2. product requirementとproject requirement、functionalとnonfunctionalを[要件分類標準](docs/standards/REQUIREMENT-CLASSIFICATION.md)に従って判定する。
3. 実際の成果物を更新する。外部挙動、業務ルール、受入条件、非機能閾値、権限要求、恒久的なproject constraintが変わる場合だけ`spec/requirements/requirements.json`を更新し、`docs/requirements/REQUIREMENTS.md`を再生成する。
4. documentation requirementは原則`project / nonfunctional`として扱い、audience、purpose、authority、update trigger、verification、maintenance rule、retirement conditionを定義する。文書file自体を要件正本にしない。
5. 実装から生成できる詳細設計は`docs/design/generated/`へ生成し、手書きで複製しない。コードから得られない長期判断だけを`docs/decisions/`へADRとして残す。
6. `governance/checks/catalog.yaml`から変更に必要なcheckだけを選び、結果を`governance/reviews/<change-id>.yaml`へ保存する。未選択checkをN/Aとして登録しない。
7. 変更範囲に応じたtest、build、lint、type check、生成物driftを実行し、Pull Request前に`make verify`でrepository契約を確認する。
8. 目的別にstageし、`.agents/skills/japanese-git-commit-gitmoji/SKILL.md`と[docs/COMMIT-COMMENT.md](docs/COMMIT-COMMENT.md)に従う日本語gitmoji Commit Commentを作成する。
9. Pull Requestには変更内容、理由・利用者影響、実行profile、review YAML path、要件・設計影響、検証契約、authority boundary、残存riskを記載する。CIの実結果はGitHub Actionsを正本とし、生ログをrepositoryへ複製しない。

## 実行プロファイル別の追加事項

### 直接実行

局所的で可逆、外部副作用のない変更に使用する。恒久的な`work/<id>/`、初回承認、lifecycle文書、phase gateを作成しない。依頼が具体的なら別計画書を作成せず、変更・検証・Commit Commentへ進む。

### 保証付き実行

複数module、公開API・event契約、DB、IaC、dependency、共有UI、generator、永続要件、governance、distributionへ影響する変更に使用する。変更固有のRisk-selected checkを追加するが、恒久的な`work/<id>/`と通常の初回承認は要求しない。公開API変更は`assured`として扱い、公開APIであることだけを承認理由にしない。

再開に必要な一時状態だけを、gitignoreされた`.devflow/run/`へ保存し、変更完了後に削除する。日付+slug計画書、固定template、段階status更新を必須にしない。

### 規制・高保証実行

authentication、authorization、PII、data loss、不可逆なproduction操作、法令・契約統制、高額操作、または明示的な高保証要求に該当する場合だけ使用する。

regulated runtimeのcode、schema、template、validatorはportable sampleとして変更できる。ただし、この参照repository自身のlive work itemはコミットしない。この場合に限り、導入先repositoryで`tools/devflow.py init`を実行して`work/<id>/`を生成する。導入先での動作を検証する必要がある場合は、一時directoryまたは`tests/fixtures/`のsynthetic dataを使用し、実案件の承認や証跡を模倣しない。

承認や証跡を捏造しないでください。公開repositoryへ秘密情報、個人データ、会話transcript、production証跡、CI生ログを追加しないでください。外部書込み、公開、merge、削除、production操作、高額操作は、依頼または明示承認で与えられたauthority boundary内だけで行ってください。
