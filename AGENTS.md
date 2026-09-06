# Repository instructions

`dev-standard`は、他のrepositoryへ軽量な開発ガードレールを配布する参照repositoryです。このrepositoryを変更するときは、最初に`$maintain-reference-repository`を適用してください。

## 3本柱

portableなblocking guardrailは次だけです。

1. `$maintain-canonical-requirements`: durableで原子的な要件をQuint正本へ保つ
2. `$generate-implementation-design`: 実装由来のas-built設計を決定的に生成する
3. `$inspect-quality-gates`: 変更に関係する検査だけを実行する

通常依頼の入口は`$chat-first-development`です。その他のSkillは明示的な必要がある場合だけ使う補助機能であり、4つの既定Skillへ新しいportable gateを追加しません。

## Authority

- 要件正本: `spec/requirements/requirements.qnt`
- 要件の派生JSON: `spec/requirements/requirements.json`
- 要件の人向け表示: `docs/requirements/REQUIREMENTS.md`
- Skill形式契約: `spec/skills/skills.qnt`
- Skill契約の派生JSON: `spec/skills/skills.json`

派生JSONとMarkdownは直接編集しません。`python tools/quintflow.py generate`で生成し、`python tools/quintflow.py check`でdriftを検査します。

## Portability boundary

installerとdistribution profileは、導入先の次の状態を維持します。

- branch構成、branch protection、ruleset
- merge方式、merge先、release手順
- CI/CD workflow、required check、status check
- commit形式、PR template、既存のrepository指示

このrepository自身のGitHub Actionsは参照repositoryを検査するためだけに存在し、導入先へ配布しません。PR作成やCI確認が依頼された場合は、GitHub上の現在設定に従います。

## 文書保守

`docs/README.md`が継続更新する文書の目的・更新条件の索引です。変更した機能に関係する文書だけを `maintain-reference-repository` で更新します。不要な文書は呼出元とともに削除し、時点の記録は日付付き `docs/archive/` へ分離します。利用者の明示指示をSkillの一般ガイドより優先します。

## Verification

変更に関係する最小のローカル検査を実行してください。repository全体の契約を変更する場合は`make verify`を使用します。外部CIは追加証拠であり、portable contractの前提ではありません。

再開に必要な一時状態だけを`.devflow/run/`へ置き、恒久的なwork recordとしてcommitしません。

明示権限なしにproduction deploy、削除、公開、merge、高額操作を行わないでください。secret、PII、production dump、生ログ、会話transcriptをcommitしません。
