# アーキテクチャ設計

## Context and boundaries

入力はrequest、OpenAI公式model/prompt guide、Codex manual、既存repository controls。出力はlean instructions、custom agent config、AI operating policy、tests、PR。runtime API、model serving、billing、customer dataは境界外。

## Components and decisions

| Component | Responsibility | Decision |
|---|---|---|
| AGENTS/skills | outcome、invariants、authority、done | 手順重複を削りdecision rulesへ集約 |
| root agent | semantic judgment、implementation、final synthesis | model/effortをpinせず創造的裁量を保持 |
| custom reviewers | bounded read-only independent checks | terra + role effort + low verbosity |
| devflow/catalog | deterministic lifecycle checks | full catalog保持、current phaseだけcontext化 |
| validator/tests | configuration drift prevention | model、effort、prompt budget、routing policyを強制 |

## Quality scenarios

- routine reviewはterra/lowまたはmediumで完了し、必要時だけhigh/rootへ昇格する。
- prompt削減後もauthorization、evidence、N/A、Fail、audit invariantがtestで維持される。
- GitHub拒否時はlocal validationを失わずrelease blockerを一件で示す。

## Failure and rollback

unknown model、TOML error、900文字超prompt、thread過多はvalidator failure。quality regressionは該当prompt/config commitをrevertし、既存single authorization harnessは変更しない。
