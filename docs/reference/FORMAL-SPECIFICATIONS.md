<!-- tools/quintflow.pyによる自動生成。spec/skills/skills.qntを編集すること。 -->
# Skills形式仕様

全Skillの機械可読契約と、モデル化した3本柱の不変条件を人向けに表示した派生文書です。

- 正本: `spec/skills/skills.qnt`
- Quint: `0.32.0`
- Skill数: 18

| Skill | 役割 | 柱 | Guardrail | 既定portable | 起動context |
|---|---|---|---|---|---|
| `adversarial-review` | independent-review | 補助 | なし | 含めない | `explicit-review-request` |
| `author-lifecycle-docs` | regulated-documentation | 補助 | なし | 含めない | `concrete-regulated-duty` |
| `authorize-autonomous-execution` | authority-boundary | 補助 | なし | 含めない | `external-authority-boundary`, `concrete-regulated-duty` |
| `calibrated-collaborative-listening` | intent-clarification | 補助 | なし | 含めない | `material-ambiguity` |
| `chat-first-development` | orchestrator | 補助 | なし | 含む | `development-request` |
| `design-frontend-experience` | frontend-design | 補助 | なし | 含めない | `frontend-design` |
| `elicit-frontend-requirements` | frontend-requirements | 補助 | なし | 含めない | `frontend-requirements` |
| `generate-implementation-design` | as-built-design | as-built設計 | blocking | 含む | `supported-as-built-surface` |
| `govern-development-request` | regulated-orchestration | 補助 | なし | 含めない | `concrete-regulated-duty` |
| `implement-frontend-experience` | frontend-implementation | 補助 | なし | 含めない | `frontend-implementation` |
| `inspect-quality-gates` | selected-checks | 選択check | blocking | 含む | `selected-checks` |
| `japanese-git-commit-gitmoji` | commit-message | 補助 | なし | 含めない | `target-commit-style` |
| `maintain-canonical-requirements` | canonical-requirements | 要件正本 | blocking | 含む | `durable-requirement-change` |
| `maintain-reference-repository` | reference-maintenance | 補助 | なし | 含めない | `reference-maintenance` |
| `retrospect-and-improve` | retrospective | 補助 | なし | 含めない | `evidenced-systemic-failure` |
| `right-size-execution` | execution-sizing | 補助 | なし | 含めない | `execution-sizing` |
| `test-frontend-experience` | frontend-testing | 補助 | なし | 含めない | `frontend-testing` |
| `verify-against-engineering-standards` | standards-lens | 補助 | なし | 含めない | `relevant-standard` |

## 検証する不変条件

- 全Skill directoryと形式契約が1対1で対応する。
- blocking guardrailは要件正本、as-built設計、選択checkの3本柱だけに属する。
- portable契約はCI workflow、branch rule、merge方式、commit規約を要求しない。
- 既定portable setは入口Skillと3本柱の4 Skillだけである。
- 各柱は現在の変更へ非該当なら明示的にskipし、該当する柱の順序を飛び越えない。
- 各Skillの7つのrepository policy fieldはfalseで、導入先の所有権を維持する。
- `externalEffect` は外部作用が生じ得るrunner capabilityを追跡し、falseは未モデル化の外部作用が存在しないことまで保証しない。
- Skill本文、必須asset、interfaceのdigestが形式契約と一致する。

## 各Skillの契約

### adversarial-review

- 前提: falsifiable claims and an authority are available
- 事後条件: a bounded review report, including an explicit no-finding result when appropriate, is returned without mutating the artifact
- 適用条件: `when-explicitly-requested`
- 起動context: `explicit-review-request`
- Authority: `artifact-authority`
- 副作用: `none`
- 外部作用capability: `false`
- Guardrail / repository blocking / 既定portable: `false` / `false` / `false`
- Repository policy: `ciWorkflow=false`, `requiredCheck=false`, `branchProtection=false`, `ruleset=false`, `mergeStrategy=false`, `prTemplate=false`, `commitFormat=false`
- 失敗状態: `report-bounded`
- 入力: `artifact`, `authority`, `review-scope`
- 出力: `review-result`, `optional-findings`, `residual-uncertainty`, `conditional-repair-handoff`
- 義務: `reconstruct-independent-authority`, `seek-falsifying-evidence`, `allow-evidence-supported-no-finding-result`, `report-bounded-findings`
- 禁止事項: `do not mutate the reviewed artifact`, `do not claim proof from a finite review`, `do not invent requirements`
- 依存Skill: なし
- 必須asset: `references/challenge-playbook.md`, `references/report-template.md`, `references/research-basis.md`
- 要件trace: なし

### author-lifecycle-docs

- 前提: a concrete regulated retention duty exists
- 事後条件: only required lifecycle evidence is retained
- 適用条件: `when-concrete-duty-exists`
- 起動context: `concrete-regulated-duty`
- Authority: `concrete-duty-or-user`
- 副作用: `repository-write`
- 外部作用capability: `false`
- Guardrail / repository blocking / 既定portable: `false` / `false` / `false`
- Repository policy: `ciWorkflow=false`, `requiredCheck=false`, `branchProtection=false`, `ruleset=false`, `mergeStrategy=false`, `prTemplate=false`, `commitFormat=false`
- 失敗状態: `no-op-unless-triggered`
- 入力: `regulated-duty`, `retention-rule`
- 出力: `regulated-evidence`, `retention-disposition`
- 義務: `select-minimum-regulated-evidence`, `define-purpose-and-retention`, `separate-authority-evidence-and-temporary-state`
- 禁止事項: `do not create lifecycle documents for ordinary changes`, `do not retain raw logs or duplicated generated facts`, `do not impose repository policy`
- 依存Skill: なし
- 必須asset: `assets/template-map.json`, `references/document-rules.md`
- 要件trace: なし

### authorize-autonomous-execution

- 前提: an external or irreversible authority boundary exists
- 事後条件: authorization scope and stop conditions are explicit and backed by current authority-owned evidence
- 適用条件: `when-external-authority-boundary-exists`
- 起動context: `external-authority-boundary`, `concrete-regulated-duty`
- Authority: `explicit-user-authorization`
- 副作用: `none`
- 外部作用capability: `false`
- Guardrail / repository blocking / 既定portable: `false` / `false` / `false`
- Repository policy: `ciWorkflow=false`, `requiredCheck=false`, `branchProtection=false`, `ruleset=false`, `mergeStrategy=false`, `prTemplate=false`, `commitFormat=false`
- 失敗状態: `stop-at-authority-boundary`
- 入力: `requested-result`, `external-effects`, `rollback`, `current-explicit-authority-evidence`
- 出力: `authorization-decision`, `authority-evidence-reference`
- 義務: `bind-approval-to-result-and-effects`, `record-stop-and-rollback-boundary`, `reuse-current-approval-within-boundary`, `reject-self-issued-authorization`
- 禁止事項: `do not infer approval from silence or history`, `do not self-mint or rewrite authority evidence`, `do not require a work item for ordinary external operations`, `do not freeze reversible implementation details`
- 依存Skill: なし
- 必須asset: `references/authorization-boundary.md`
- 要件trace: `REQ-PORTABLE-003`

### calibrated-collaborative-listening

- 前提: multiple interpretations materially change the result
- 事後条件: a correctable goal and decision are available
- 適用条件: `when-ambiguity-changes-result`
- 起動context: `material-ambiguity`
- Authority: `user-intent`
- 副作用: `none`
- 外部作用capability: `false`
- Guardrail / repository blocking / 既定portable: `false` / `false` / `false`
- Repository policy: `ciWorkflow=false`, `requiredCheck=false`, `branchProtection=false`, `ruleset=false`, `mergeStrategy=false`, `prTemplate=false`, `commitFormat=false`
- 失敗状態: `return-for-clarification`
- 入力: `request`, `constraints`
- 出力: `correctable-goal`, `decision`
- 義務: `separate-evidence-from-inference`, `preserve-semantic-units`, `ask-only-consequential-questions`
- 禁止事項: `do not present inferred motives as facts`, `do not turn clarification into delay`, `do not remove conditions or uncertainty when compressing`
- 依存Skill: なし
- 必須asset: `references/evaluation-rubric.md`, `references/evidence-map.md`, `references/japanese-response-patterns.md`, `references/semantic-articulation-protocol.md`
- 要件trace: `REQ-DISC-001`

### chat-first-development

- 前提: a development outcome is requested
- 事後条件: the requested outcome and only applicable pillars are complete, and every external effect remains within explicit authority
- 適用条件: `when-development-is-requested`
- 起動context: `development-request`
- Authority: `user-and-target-repository`
- 副作用: `repository-and-authorized-external-write`
- 外部作用capability: `true`
- Guardrail / repository blocking / 既定portable: `false` / `false` / `true`
- Repository policy: `ciWorkflow=false`, `requiredCheck=false`, `branchProtection=false`, `ruleset=false`, `mergeStrategy=false`, `prTemplate=false`, `commitFormat=false`
- 失敗状態: `report-bounded`
- 入力: `request`, `target-repository-rules`, `authority-boundary`
- 出力: `change`, `verification-summary`, `external-operation-result`
- 義務: `classify-durable-requirement-impact`, `generate-supported-as-built-design`, `run-only-selected-checks`, `bind-external-effects-to-authority`, `perform-pr-operation-only-when-requested`
- 禁止事項: `do not impose CI branch or merge policy`, `do not create per-change bureaucracy`, `do not create update comment or merge a PR unless requested`
- 依存Skill: `maintain-canonical-requirements`, `generate-implementation-design`, `inspect-quality-gates`
- 必須asset: `references/bootstrap-and-conversation.md`
- 要件trace: `REQ-DISC-005`, `REQ-PORTABLE-001`, `REQ-PORTABLE-003`

### design-frontend-experience

- 前提: frontend outcomes and constraints are known
- 事後条件: minimum implementation decisions and selected-check handoff are explicit
- 適用条件: `when-frontend-design-is-needed`
- 起動context: `frontend-design`
- Authority: `approved-requirements`
- 副作用: `repository-write`
- 外部作用capability: `false`
- Guardrail / repository blocking / 既定portable: `false` / `false` / `false`
- Repository policy: `ciWorkflow=false`, `requiredCheck=false`, `branchProtection=false`, `ruleset=false`, `mergeStrategy=false`, `prTemplate=false`, `commitFormat=false`
- 失敗状態: `return-to-requirements`
- 入力: `requirements`, `design-context`, `existing-design-system`, `selected-check`
- 出力: `design-decisions`, `verification-hooks`, `selected-check-handoff`
- 義務: `derive-minimum-implementation-decisions`, `cover-applicable-interaction-states`, `handoff-verification-hooks`
- 禁止事項: `do not duplicate implementation-derived inventories`, `do not persist local design detail as ADR`, `do not require a generator for unsupported artifacts`
- 依存Skill: なし
- 必須asset: `references/evidence-map.md`
- 要件trace: なし

### elicit-frontend-requirements

- 前提: a frontend outcome is requested
- 事後条件: durable observable obligations are maintained in canonical requirements and design context is handed forward
- 適用条件: `when-frontend-requirements-are-needed`
- 起動context: `frontend-requirements`
- Authority: `user-intent`
- 副作用: `repository-write`
- 外部作用capability: `false`
- Guardrail / repository blocking / 既定portable: `false` / `false` / `false`
- Repository policy: `ciWorkflow=false`, `requiredCheck=false`, `branchProtection=false`, `ruleset=false`, `mergeStrategy=false`, `prTemplate=false`, `commitFormat=false`
- 失敗状態: `return-for-clarification`
- 入力: `user-task`, `context`, `failure-impact`
- 出力: `canonical-requirement-delta`, `design-context`, `selected-check`
- 義務: `separate-user-problem-from-solution`, `maintain-durable-obligations`, `handoff-context-and-selected-checks`
- 禁止事項: `do not persist temporary interview notes`, `do not create per-change requirement reports`, `do not impose repository policy`
- 依存Skill: なし
- 必須asset: `references/evidence-map.md`
- 要件trace: `REQ-DISC-005`

### generate-implementation-design

- 前提: a declared generator supports the changed surface and explicit trace JSON declares applicable_requirement_ids for that supported surface
- 事後条件: generated design is deterministic and isolated, matches implementation, and maps exactly the declared applicable active requirement set through operations or resources to existing test nodes
- 適用条件: `when-a-declared-generator-supports-the-change`
- 起動context: `supported-as-built-surface`
- Authority: `implementation`
- 副作用: `repository-write`
- 外部作用capability: `false`
- Guardrail / repository blocking / 既定portable: `true` / `true` / `true`
- Repository policy: `ciWorkflow=false`, `requiredCheck=false`, `branchProtection=false`, `ruleset=false`, `mergeStrategy=false`, `prTemplate=false`, `commitFormat=false`
- 失敗状態: `fail-on-drift`
- 入力: `implementation`, `generator-contract`, `pinned-isolated-python-runtime`, `canonical-requirements-json`, `explicit-applicable-requirement-ids`, `explicit-artifact-trace`, `test-source`
- 出力: `generated-design`, `drift-result`, `exact-requirement-artifact-test-trace`, `structured-unsupported-surface-or-bounded-fail-closed-diagnostic`
- 義務: `run-with-pinned-isolated-runtime`, `generate-deterministic-as-built`, `verify-isolation-and-drift`, `match-explicit-applicable-active-set-exactly`, `reject-unknown-inactive-missing-or-excess-trace`
- 禁止事項: `do not modify the target repository virtual environment`, `do not edit generated design directly`, `do not infer requirement satisfaction from implementation`, `do not require a generator or CI for unsupported artifacts`
- 依存Skill: なし
- 必須asset: `assets/as-built-thresholds.json`, `references/cdk-contract.md`, `references/fastapi-contract.md`, `requirements.txt`, `scripts/designflow.py`, `scripts/qualityflow.py`
- 要件trace: `REQ-ASBUILT-001`, `REQ-ASBUILT-002`, `REQ-ASBUILT-003`, `REQ-ASBUILT-004`, `REQ-ASBUILT-005`, `REQ-ASBUILT-006`, `REQ-ASBUILT-007`, `REQ-ASBUILT-008`, `REQ-ASBUILT-009`, `REQ-ASBUILT-010`, `REQ-ASBUILT-011`, `REQ-ASBUILT-012`, `REQ-ASBUILT-013`, `REQ-ASBUILT-014`, `REQ-ASBUILT-015`, `REQ-ASBUILT-016`, `REQ-ASBUILT-018`, `REQ-ASBUILT-020`, `REQ-DESIGN-001`, `REQ-DESIGN-002`, `REQ-DESIGN-003`, `REQ-DESIGN-004`, `REQ-DESIGN-005`, `REQ-DESIGN-006`

### govern-development-request

- 前提: a concrete regulated lifecycle duty exists
- 事後条件: regulated evidence strictly binds unchanged pre-existing target-owned authority evidence within that duty and any required external anchor is returned as a handoff
- 適用条件: `when-concrete-duty-exists`
- 起動context: `concrete-regulated-duty`
- Authority: `concrete-duty-or-user`
- 副作用: `repository-write`
- 外部作用capability: `false`
- Guardrail / repository blocking / 既定portable: `false` / `false` / `false`
- Repository policy: `ciWorkflow=false`, `requiredCheck=false`, `branchProtection=false`, `ruleset=false`, `mergeStrategy=false`, `prTemplate=false`, `commitFormat=false`
- 失敗状態: `stop-at-authority-boundary`
- 入力: `concrete-duty-kind`, `concrete-duty-reference`, `bounded-obligation`, `authority-boundary`, `retention-rule`, `pre-existing-target-owned-authority-evidence`
- 出力: `strict-replay-regulated-record`, `local-anchor`, `external-anchor-handoff`
- 義務: `bind-regulated-work-to-concrete-duty`, `consume-and-bind-pre-existing-target-owned-authority-evidence`, `bind-authorization-to-authority-result-effects-rollback-and-stop`, `strictly-replay-init-authorize-verify-close`, `handoff-required-external-anchor`
- 禁止事項: `do not activate from a technology or risk label alone`, `do not apply lifecycle evidence to ordinary work`, `do not self-mint or rewrite authority evidence`, `do not write external audit records`, `do not retain secrets PII or raw production logs`
- 依存Skill: なし
- 必須asset: `references/work-item-contract.md`, `scripts/regulatedflow.py`, `scripts/start.py`
- 要件trace: なし

### implement-frontend-experience

- 前提: frontend requirements and decisions are ready
- 事後条件: the user task works in supported states and implementation evidence is handed to testing
- 適用条件: `when-frontend-implementation-is-requested`
- 起動context: `frontend-implementation`
- Authority: `requirements-and-design`
- 副作用: `repository-write`
- 外部作用capability: `false`
- Guardrail / repository blocking / 既定portable: `false` / `false` / `false`
- Repository policy: `ciWorkflow=false`, `requiredCheck=false`, `branchProtection=false`, `ruleset=false`, `mergeStrategy=false`, `prTemplate=false`, `commitFormat=false`
- 失敗状態: `return-to-design`
- 入力: `requirements`, `design-decisions`, `existing-frontend`, `selected-check`
- 出力: `frontend-change`, `tests`, `as-built-design`, `selected-check-result`
- 義務: `implement-complete-user-task-states`, `preserve-semantics-and-supported-context`, `handoff-as-built-and-check-evidence`
- 禁止事項: `do not invent product requirements during implementation`, `do not weaken type test or accessibility constraints`, `do not force an unsupported generator`
- 依存Skill: なし
- 必須asset: `references/evidence-map.md`
- 要件trace: なし

### inspect-quality-gates

- 前提: changed artifacts, applicable risks, target-owned checks, declared command effects, and any required external authority are known
- 事後条件: selected blockers pass or a bounded failure is reported with declared command effects and a process-effect-not-isolated residual for every command, without claiming unselected coverage or isolation
- 適用条件: `when-change-relevant-checks-exist`
- 起動context: `selected-checks`
- Authority: `target-repository-and-selected-checks`
- 副作用: `target-command-effects`
- 外部作用capability: `true`
- Guardrail / repository blocking / 既定portable: `true` / `true` / `true`
- Repository policy: `ciWorkflow=false`, `requiredCheck=false`, `branchProtection=false`, `ruleset=false`, `mergeStrategy=false`, `prTemplate=false`, `commitFormat=false`
- 失敗状態: `report-bounded`
- 入力: `change`, `acceptance`, `target-owned-checks`, `optional-target-owned-command-registry`, `declared-command-effects`, `external-authority-if-applicable`
- 出力: `selected-check-results`, `declared-effect-report`, `residual-risk`, `repair-handoff`
- 義務: `select-minimum-relevant-checks`, `validate-registry-command-and-declared-effect-when-runner-is-used`, `execute-selected-checks`, `report-process-effect-isolation-uncertainty-for-every-command`, `bound-verdict-to-observed-evidence`
- 禁止事項: `do not modify source to hide failures`, `do not claim external-effect absence process isolation or unselected coverage`, `do not execute a declared external effect without explicit authority`, `do not create CI or merge policy`
- 依存Skill: なし
- 必須asset: `references/gate-rules.md`, `scripts/inspect.py`
- 要件trace: `REQ-ASBUILT-019`, `REQ-QUALITY-002`

### japanese-git-commit-gitmoji

- 前提: the user explicitly requests this style or the target repository already selects it
- 事後条件: a Japanese structured commit message is proposed
- 適用条件: `when-user-or-target-selects-style`
- 起動context: `target-commit-style`
- Authority: `explicit-user-or-target-repository-style`
- 副作用: `none`
- 外部作用capability: `false`
- Guardrail / repository blocking / 既定portable: `false` / `false` / `false`
- Repository policy: `ciWorkflow=false`, `requiredCheck=false`, `branchProtection=false`, `ruleset=false`, `mergeStrategy=false`, `prTemplate=false`, `commitFormat=false`
- 失敗状態: `no-op-unless-selected`
- 入力: `diff`, `verification-summary`
- 出力: `commit-message`
- 義務: `derive-message-from-actual-diff`, `report-verification-truthfully`, `prefer-target-repository-style`
- 禁止事項: `do not make this style a portable gate`, `do not report unexecuted checks as passing`, `do not require a particular merge method`
- 依存Skill: なし
- 必須asset: なし
- 要件trace: なし

### maintain-canonical-requirements

- 前提: a requirements authority is initialized or a durable observable obligation changes
- 事後条件: Quint source, verification, derived JSON, and generated docs agree, while only already-existing downstream artifacts require current traces and future trace work is handed downstream
- 適用条件: `when-durable-obligation-changes-or-authority-is-initialized`
- 起動context: `durable-requirement-change`
- Authority: `quint-requirements`
- 副作用: `repository-write`
- 外部作用capability: `false`
- Guardrail / repository blocking / 既定portable: `true` / `true` / `true`
- Repository policy: `ciWorkflow=false`, `requiredCheck=false`, `branchProtection=false`, `ruleset=false`, `mergeStrategy=false`, `prTemplate=false`, `commitFormat=false`
- 失敗状態: `fail-on-invalid-catalog`
- 入力: `initialization-or-delta`, `source`, `acceptance`
- 出力: `requirements-qnt`, `requirements-json`, `requirements-doc`, `existing-requirement-trace`, `downstream-trace-handoff`
- 義務: `maintain-quint-as-sole-requirements-authority`, `atomize-and-classify-durable-obligations`, `generate-json-then-human-documentation`, `handoff-future-downstream-trace-without-blocking-requirement-update`
- 禁止事項: `do not edit generated requirement views`, `do not persist reversible implementation choices as requirements`, `do not require CI branch or merge policy`
- 依存Skill: なし
- 必須asset: `assets/documentation-project-nfr.example.json`, `assets/requirements.schema.json`, `assets/requirements.template.qnt`, `references/research-basis.md`, `scripts/specflow.py`
- 要件trace: `REQ-DISC-001`, `REQ-DISC-002`, `REQ-DISC-003`, `REQ-DISC-004`, `REQ-DISC-005`, `REQ-DOCS-001`, `REQ-FRAME-001`, `REQ-QUINT-002`

### maintain-reference-repository

- 前提: dev-standard or its portable-collection fork changes portable assets
- 事後条件: portable and repository-specific assets remain separated
- 適用条件: `when-reference-assets-change`
- 起動context: `reference-maintenance`
- Authority: `reference-repository`
- 副作用: `repository-write`
- 外部作用capability: `false`
- Guardrail / repository blocking / 既定portable: `false` / `false` / `false`
- Repository policy: `ciWorkflow=false`, `requiredCheck=false`, `branchProtection=false`, `ruleset=false`, `mergeStrategy=false`, `prTemplate=false`, `commitFormat=false`
- 失敗状態: `report-bounded`
- 入力: `reference-change`, `distribution-boundary`
- 出力: `portable-assets`, `compatibility-result`
- 義務: `separate-portable-and-reference-only-assets`, `keep-default-portable-set-to-entry-and-three-pillars`, `verify-portable-dependency-closure`
- 禁止事項: `do not invoke for ordinary target-product changes`, `do not export reference-repository policy`, `do not edit generated views directly`
- 依存Skill: なし
- 必須asset: なし
- 要件trace: なし

### retrospect-and-improve

- 前提: an evidenced escaped defect, incident, rollback, or recurring cost exists
- 事後条件: a bounded evaluable improvement is proposed but not automatically applied
- 適用条件: `when-evidenced-systemic-trigger-exists`
- 起動context: `evidenced-systemic-failure`
- Authority: `observed-defect`
- 副作用: `repository-confined-temporary-write`
- 外部作用capability: `false`
- Guardrail / repository blocking / 既定portable: `false` / `false` / `false`
- Repository policy: `ciWorkflow=false`, `requiredCheck=false`, `branchProtection=false`, `ruleset=false`, `mergeStrategy=false`, `prTemplate=false`, `commitFormat=false`
- 失敗状態: `no-op-unless-triggered`
- 入力: `defect-incident-rollback-or-recurring-cost-evidence`, `impact`
- 出力: `bounded-candidate-or-not-triggered`, `optional-temporary-json-result`
- 義務: `require-evidenced-systemic-trigger`, `compare-lighter-alternatives`, `define-evaluation-rollback-and-sunset`
- 禁止事項: `do not trigger from one transient check failure`, `do not auto-promote a proposal to a blocking rule`, `do not mix unrelated improvement into the active change`
- 依存Skill: なし
- 必須asset: `references/improvement-policy.md`, `scripts/retrospect.py`
- 要件trace: なし

### right-size-execution

- 前提: execution context can provide sizing, adjustment, verification observation, and stopping evidence
- 事後条件: the selected or adjusted minimum profile has an exact verification projection, bounded diagnostics, and tamper-evident stopping evidence
- 適用条件: `when-execution-sizing-is-needed`
- 起動context: `execution-sizing`
- Authority: `change-risk`
- 副作用: `repository-confined-temporary-write`
- 外部作用capability: `false`
- Guardrail / repository blocking / 既定portable: `false` / `false` / `false`
- Repository policy: `ciWorkflow=false`, `requiredCheck=false`, `branchProtection=false`, `ruleset=false`, `mergeStrategy=false`, `prTemplate=false`, `commitFormat=false`
- 失敗状態: `report-bounded`
- 入力: `execution-context`, `change-risk`, `artifacts`, `acceptance`, `target-owned-gates`, `available-evidence`
- 出力: `execution-profile`, `selected-verification`, `optional-diagnostics`, `stopping-evidence`
- 義務: `assess-independent-execution-axes`, `derive-exact-verification-projection`, `expand-one-evidence-backed-axis`, `stop-after-decisive-success`, `preserve-tamper-evident-state`
- 禁止事項: `do not infer repository policy from execution sizing`, `do not fabricate evidence or bypass a risk floor`, `do not continue unbounded exploration after success`
- 依存Skill: なし
- 必須asset: `assets/behavior-constraints.json`, `assets/benchmark-cases.json`, `assets/execution-policy.json`, `assets/execution-policy.schema.json`, `assets/execution-profile.schema.json`, `references/execution-dimensions.md`, `references/expansion-contract.md`, `references/measurement-contract.md`, `references/stopping-contract.md`, `scripts/executionflow.py`
- 要件trace: `REQ-EXEC-001`, `REQ-EXEC-002`, `REQ-EXEC-003`, `REQ-EXEC-004`, `REQ-EXEC-005`, `REQ-EXEC-006`, `REQ-EXEC-007`, `REQ-EXEC-008`, `REQ-EXEC-009`, `REQ-EXEC-010`, `REQ-SKILL-001`, `REQ-SKILL-002`

### test-frontend-experience

- 前提: frontend requirements, approved design, implementation, and selected checks are available
- 事後条件: tests selected only for applicable dimensions pass or a bounded repair handoff is returned, and claims stay within executed scope
- 適用条件: `when-frontend-testing-is-requested`
- 起動context: `frontend-testing`
- Authority: `frontend-requirements-and-approved-design`
- 副作用: `target-command-effects`
- 外部作用capability: `true`
- Guardrail / repository blocking / 既定portable: `false` / `false` / `false`
- Repository policy: `ciWorkflow=false`, `requiredCheck=false`, `branchProtection=false`, `ruleset=false`, `mergeStrategy=false`, `prTemplate=false`, `commitFormat=false`
- 失敗状態: `report-bounded`
- 入力: `requirements`, `design-decisions`, `implementation`, `as-built-design`, `supported-environment`, `selected-check`, `declared-test-command-effects`, `external-authority-if-applicable`
- 出力: `test-results`, `selected-check-result`, `declared-effect-report`, `residual-risk`, `repair-handoff`
- 義務: `derive-tests-from-authority-order`, `select-only-applicable-test-dimensions`, `exercise-applicable-task-and-failure-states`, `bind-declared-external-effects-to-authority`, `bound-verdict-to-supported-environment`
- 禁止事項: `do not mutate production artifacts while reviewing`, `do not let implementation override requirements`, `do not claim process isolation or unexecuted coverage`
- 依存Skill: なし
- 必須asset: `references/evidence-map.md`
- 要件trace: なし

### verify-against-engineering-standards

- 前提: a relevant standard is selected for the change
- 事後条件: only applicable controls have evidence-bounded findings without overriding canonical authority, and any requested generated source document stays repository-confined
- 適用条件: `when-a-relevant-standard-is-selected`
- 起動context: `relevant-standard`
- Authority: `canonical-requirements-target-policy-and-selected-official-standards`
- 副作用: `repository-write`
- 外部作用capability: `false`
- Guardrail / repository blocking / 既定portable: `false` / `false` / `false`
- Repository policy: `ciWorkflow=false`, `requiredCheck=false`, `branchProtection=false`, `ruleset=false`, `mergeStrategy=false`, `prTemplate=false`, `commitFormat=false`
- 失敗状態: `report-bounded`
- 入力: `change`, `requirements`, `target-policy`, `skill-default-standards-registry`, `source-context`, `optional-repository-output`
- 出力: `selected-standards`, `selected-controls`, `standard-findings`, `residual-risk`, `requirement-handoff`, `generated-sources-doc-when-requested`
- 義務: `select-only-relevant-official-controls`, `preserve-standard-version-and-freshness`, `derive-verdict-from-direct-evidence`, `confine-generated-output-to-target-repository`
- 禁止事項: `do not override canonical requirements with external standards`, `do not claim certification or exhaustive compliance`, `do not write outside the target repository or create CI or merge policy`
- 依存Skill: なし
- 必須asset: `assets/standards.registry.json`, `references/as-built-design-check-selection.md`, `references/source-policy.md`, `scripts/standardsflow.py`
- 要件trace: `REQ-ASBUILT-012`, `REQ-ASBUILT-013`, `REQ-ASBUILT-014`, `REQ-ASBUILT-015`, `REQ-DOCS-001`, `REQ-QUALITY-001`, `REQ-QUALITY-003`
