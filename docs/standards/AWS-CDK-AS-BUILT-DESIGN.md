# 旧AWS CDK as-built標準からの移行

- 旧標準ID: `DEVSTD-AWS-CDK-AS-BUILT`
- 版: `2026-09-23`
- 状態: [言語非依存のas-built設計標準](AS-BUILT-DESIGN.md)へ統合

このpathと標準IDは過去の参照のために残す。旧CDK固有Rule IDおよびbundled generatorの規範は廃止し、永続義務は`spec/requirements/requirements.qnt`のadapter契約へ再定義した。

インフラを持つ導入先は、実装artifactから生成するadapterを自身のrepositoryに実装し、schema version 2の`.dev-standard/design.json`へ生成command、`--check` command、出力root、適用要件IDを宣言する。解析方法と実行環境は導入先が所有する。

`aws-cdk-implementation-design` profileは`implementation-design`と同じ言語非依存assetを配布する互換aliasである。旧`designflow.py cdk`利用者は[導入・復旧手順](../../.agents/skills/generate-implementation-design/references/adoption.md)に従ってadapterへ移行する。旧生成器と専用runtimeは、移行検証後に導入先で確認して除去する。deployや公開、既存CI・merge規則の変更は移行に含まれない。
