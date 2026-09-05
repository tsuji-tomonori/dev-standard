---
name: generate-implementation-design
description: Deterministically generate as-built design from implementation artifacts and check that generated documentation still matches the implementation.
---

# Generate Implementation Design

## Formal specification

`spec/skills/skills.qnt` の `skillContracts` にある `name: "generate-implementation-design"` を形式契約とする。

形式契約の`applicability`と`activationContexts`に該当しない場合は起動せず、artifactやblocking判定を作らないno-opとする。

実装から現在状態の設計を決定的に生成する。これは2本目のガードレールである。

変更artifactを扱う宣言済みgenerator contractがある場合だけ起動する。generator対象外のartifactはboundedな未生成surfaceとして返し、このSkillを理由に新しいgenerator、設計書、CIを要求しない。

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
- 実行例: `python tools/portable_python.py run <host-skill-path>/scripts/designflow.py -- fastapi --source-root <src> --openapi <openapi.json> --sql-root <sql> --requirements <requirements.json> --trace <trace.json> --test-root <tests> --out docs/design/generated/fastapi`

## AWS CDK

- synth後のCloudFormation templateからresource、parameter、template SHA-256を生成する。
- 作成または再編時は`references/cdk-contract.md`を読む。
- 実行例: `python tools/portable_python.py run <host-skill-path>/scripts/designflow.py -- cdk --template <template.yaml> --requirements <requirements.json> --trace <trace.json> --test-root <tests> --out docs/design/generated/cdk/<stack>`

## Pinned Python runtime

初回だけ`python tools/portable_python.py setup`でmanifestに固定されたisolated runtimeを準備する。対象repositoryの既存venvやglobal packageを変更せず、`designflow.py`と`qualityflow.py`は常に`python tools/portable_python.py run <host-skill-path>/scripts/{designflow,qualityflow}.py -- <args...>`で実行する。`<host-skill-path>`はinstaller receiptとhost adapterが配置した、このSkillのhost-native rootへ解決し、特定hostのdirectory名を本文へ固定しない。

## Verification

1. generationが成功する。
2. 同じ入力の2回目の出力がbyte一致する。
3. `--check`が既存生成物との差を検出する。
4. canonical requirements JSON、明示的なartifact trace JSON、test sourceを入力する。trace JSONの`applicable_requirement_ids`は、generatorが扱う変更surfaceに関係するactive requirementだけを明示する。
5. `applicable_requirement_ids`とrequirement→operation / resource→実在test nodeのmappingを集合として完全一致させる。未知ID、inactive ID、未mapping ID、宣言外の余剰mappingを拒否し、実装から要件充足を推測して新しいtraceを捏造しない。
6. generator対象外の変更surfaceは、path、理由、support statusを持つstructured `unsupported_surface`として返す。generator対象内で未対応構文を検出した場合はpath、function、line、node kindを持つbounded diagnosticでfail-closedにする。どちらも未生成surfaceへ完全性を主張しない。

`--check`はローカルでも対象repositoryが既に持つCIでも実行できる。このSkillはCI workflow、required check、branch protection、merge ruleを作成も要求もしない。生成設計は実装との一致を示すが、実装が要件を満たすことまでは証明しない。

<!-- BEGIN GENERATED QUINT CONTRACT -->
## Quint contract（自動生成）

このblockは`spec/skills/skills.qnt`から生成するviewです。直接編集しません。

- Skill: `generate-implementation-design`
- 役割: as-built-design
- 柱: design
- guardrail: yes
- repository blocking: yes
- 既定portable: yes
- 適用条件: when-a-declared-generator-supports-the-change
- 起動context: `supported-as-built-surface`
- 外部作用capability: no
- repository policy `ciWorkflow`: false
- repository policy `requiredCheck`: false
- repository policy `branchProtection`: false
- repository policy `ruleset`: false
- repository policy `mergeStrategy`: false
- repository policy `prTemplate`: false
- repository policy `commitFormat`: false
- 前提: a declared generator supports the changed surface and explicit trace JSON declares applicable_requirement_ids for that supported surface
- 事後条件: generated design is deterministic and isolated, matches implementation, and maps exactly the declared applicable active requirement set through operations or resources to existing test nodes
- Authority: implementation
- 副作用: repository-write
- 失敗状態: fail-on-drift
- 入力: `implementation`, `generator-contract`, `pinned-isolated-python-runtime`, `canonical-requirements-json`, `explicit-applicable-requirement-ids`, `explicit-artifact-trace`, `test-source`
- 出力: `generated-design`, `drift-result`, `exact-requirement-artifact-test-trace`, `structured-unsupported-surface-or-bounded-fail-closed-diagnostic`
- 義務: `run-with-pinned-isolated-runtime`, `generate-deterministic-as-built`, `verify-isolation-and-drift`, `match-explicit-applicable-active-set-exactly`, `reject-unknown-inactive-missing-or-excess-trace`
- 禁止事項: `do not modify the target repository virtual environment`, `do not edit generated design directly`, `do not infer requirement satisfaction from implementation`, `do not require a generator or CI for unsupported artifacts`
- 依存Skill: なし
- 必須asset: `assets/as-built-thresholds.json`, `references/cdk-contract.md`, `references/fastapi-contract.md`, `requirements.txt`, `scripts/designflow.py`, `scripts/qualityflow.py`
- 要件trace: `REQ-ASBUILT-001`, `REQ-ASBUILT-002`, `REQ-ASBUILT-003`, `REQ-ASBUILT-004`, `REQ-ASBUILT-005`, `REQ-ASBUILT-006`, `REQ-ASBUILT-007`, `REQ-ASBUILT-008`, `REQ-ASBUILT-009`, `REQ-ASBUILT-010`, `REQ-ASBUILT-011`, `REQ-ASBUILT-012`, `REQ-ASBUILT-013`, `REQ-ASBUILT-014`, `REQ-ASBUILT-015`, `REQ-ASBUILT-016`, `REQ-ASBUILT-018`, `REQ-ASBUILT-020`, `REQ-DESIGN-001`, `REQ-DESIGN-002`, `REQ-DESIGN-003`, `REQ-DESIGN-004`, `REQ-DESIGN-005`, `REQ-DESIGN-006`
- manual digest: `429d39048fee4fafa8f85558a3aa44178dd4cb2aeed73b941af1a0904569c208`
- payload digest: `972bf2d4303a151c201084447052731f0142c1c73de031a3451c31a9f0f20c68`
- interface digest: `2d53132a9471f1f73d6578654fd68cb4141b62c915e7d1ace402385808ef9f42`
<!-- END GENERATED QUINT CONTRACT -->
