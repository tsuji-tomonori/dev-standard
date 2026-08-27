---
name: generate-implementation-design
description: Deterministically generate as-built design from implementation artifacts and check that generated documentation still matches the implementation.
---

# Generate Implementation Design

## Formal specification

`spec/skills/skills.qnt` の `skillContracts` にある `name: "generate-implementation-design"` を形式契約とする。

実装から現在状態の設計を決定的に生成する。これは2本目のガードレールである。

## Authority order

1. `spec/requirements/requirements.qnt`は意図した挙動を定義する。
2. 実装artifactは実装済み構造とinterfaceを定義する。
3. `docs/design/generated/`の生成設計は実装artifactを説明し、digestを持つ。
4. 不一致は欠陥であり、生成文書を直接編集して隠さない。

出力はgeneratorが完全所有するpathに限定し、symlink、directory置換、管理外pathへの出力を拒否する。

## FastAPI

- route AST、applicationが生成するOpenAPI、handler metadata、error branch、SQL ASTから設計を生成する。
- executable SQLを正規表現で推測せず、parseできないSQLを拒否する。
- 作成または再編時は`references/fastapi-contract.md`を読む。
- 実行例: `scripts/designflow.py fastapi --source-root <src> --openapi <openapi.json> --sql-root <sql> --out docs/design/generated/fastapi`

## AWS CDK

- synth後のCloudFormation templateからresource、parameter、template SHA-256を生成する。
- 作成または再編時は`references/cdk-contract.md`を読む。
- 実行例: `scripts/designflow.py cdk --template <template.yaml> --out docs/design/generated/cdk/<stack>`

## Verification

1. generationが成功する。
2. 同じ入力の2回目の出力がbyte一致する。
3. `--check`が既存生成物との差を検出する。
4. requirement IDがoperation、resource、testへtraceする。

`--check`はローカルでも対象repositoryが既に持つCIでも実行できる。このSkillはCI workflow、required check、branch protection、merge ruleを作成も要求もしない。生成設計は実装との一致を示すが、実装が要件を満たすことまでは証明しない。
