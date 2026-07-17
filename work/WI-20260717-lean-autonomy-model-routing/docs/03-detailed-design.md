# 詳細設計

## Prompt layers

AGENTSはOutcome/Invariants/Efficient execution/Commands/Done/Publicationだけを持つ。govern skillはintakeからclosureまでの判断点を7段階で表す。reviewer promptは一つのreview outcome、evidence format、禁止境界だけを900文字以下で持つ。

## Model configuration

全custom reviewer: `model=gpt-5.6-terra`, `model_verbosity=low`, `sandbox_mode=read-only`。requirements/architecture/testはmedium、operations/improvementはlow、security/gate auditはhigh。global agentsはmax_threads 3、max_depth 1。

## Validation

`validate_repo.py`はAI policy存在・用語、thread/depth、agent model/effort/verbosity/prompt budgetを検査する。unit testも同じcontractを独立検証する。
