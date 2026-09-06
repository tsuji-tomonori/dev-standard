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
| `generate-implementation-design` | as-built-design | as-built設計 | blocking | 含む | `as-built-adoption-or-change` |
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
- manual digest: `fa3eb9831cca4a171bbabce33e3b2f843e65edbaedbb1e54948e6cad4641e369`
- payload digest: `9ad70d5f3a5dda494f0249985dfdea45c00bb217418a8be95476324f243dff99`
- interface digest: `2a288a121591cb1bd3c950bc18615d267d1edf0f28331f2157aa7296ef9ef856`

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
- manual digest: `765c6dd2bef4bef23a2e6ab691664e828ba5ce6b60c8d6416aa12d1f1c0f3e4b`
- payload digest: `ef45fe345793aaccce17c13d1658556d6af7e926c2bed273b26f5a0edfaf3e9d`
- interface digest: `3cd8efe2ae6065ac22af9c9bf7414b8636403dc0754994c260d7881f42eab195`

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
- 禁止事項: `do not infer approval from silence or unrelated history`, `do not self-mint or rewrite authority evidence`, `do not require a work item for ordinary external operations`, `do not freeze reversible implementation details`
- 依存Skill: なし
- 必須asset: `references/authorization-boundary.md`
- 要件trace: `REQ-PORTABLE-003`
- manual digest: `986d3bea3e4df940623100315b1a565a8de37fb36e36222076c569dfc04d52f1`
- payload digest: `fe706945e0261d253d3ab98aefcacc8b5905d2bc94e7ea4b243b6f376a0d3eed`
- interface digest: `38025d9d84a0db4183ca9f2d785e80fd3ffc4a239c0554567f99c6cae4129905`

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
- manual digest: `949651687839e31fde3609d337def4d3ad3927e7029087853db63f85f6ce4333`
- payload digest: `ac238a57de0efa49e9bf667ff5fb564ba14551d45f2062ed4ada2ce19afe8450`
- interface digest: `f2f0ae44b737d2fb39e6e5bfe2e771b3ed2430e6653f5d742e4d730eceee72d7`

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
- 義務: `verify-operation-sql-and-typed-query-generation`, `verify-japanese-explanations-at-generator-source`, `classify-durable-requirement-impact`, `complete-as-built-adoption-and-generation`, `run-only-selected-checks`, `bind-external-effects-to-authority`, `perform-pr-operation-only-when-requested`
- 禁止事項: `do not impose CI branch or merge policy`, `do not create per-change bureaucracy`, `do not create update comment or merge a PR unless requested`
- 依存Skill: `maintain-canonical-requirements`, `generate-implementation-design`, `inspect-quality-gates`
- 必須asset: `references/bootstrap-and-conversation.md`
- 要件trace: `REQ-DISC-005`, `REQ-PORTABLE-001`, `REQ-PORTABLE-003`, `REQ-ASBUILT-021`, `REQ-DESIGN-007`, `REQ-DOCS-002`
- manual digest: `d833a541c5a4faca6c782caa0bce2d8da772c0c7d93909551060dc18fd2ee8fd`
- payload digest: `e3f954a85f0d9c33a7c5ad846747f01ba02a42d0cbe7730386bf7e4c4ee6a3c0`
- interface digest: `fb458bd3bba0d3d1ee4cd64f42523207190dd082f61b7b93cebd0697654a470d`

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
- 禁止事項: `do not duplicate implementation-derived inventories`, `do not persist local design detail as ADR`, `do not mark unsupported required design complete`
- 依存Skill: なし
- 必須asset: `references/evidence-map.md`
- 要件trace: なし
- manual digest: `e8424b4f8afd3b16fb9f5bf47550da8d9a4403ba0ed03c570283588d95d0e006`
- payload digest: `3a6c7028166026088e59394ecd91218e663b05a032da8a2835f9da66893ad812`
- interface digest: `dbcd41c79681072af7015a3476e9a45f6f851dac7c1b6ec072d0abb47f46c99c`

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
- manual digest: `a101def52f60a99c54016e90898a32d917e5dd8667b09be5c8c2fafd9d4b0f4b`
- payload digest: `9e4bcabfece7a6685a9cb07399e6c8a10ee7a72c760dbbd1b20f91df671f4bb4`
- interface digest: `01653ab1c807a2841aa48a2eeea4a8da57eaf31227066664929c8dea2cfc4e1b`

### generate-implementation-design

- 前提: adoption or implementation change requires an as-built inventory and generator connection, including first-time setup
- 事後条件: generated design is deterministic and isolated, matches implementation, and maps exactly the declared applicable active requirement set through operations or resources to existing test nodes
- 適用条件: `when-adopting-or-changing-implementation`
- 起動context: `as-built-adoption-or-change`
- Authority: `implementation`
- 副作用: `repository-write`
- 外部作用capability: `false`
- Guardrail / repository blocking / 既定portable: `true` / `true` / `true`
- Repository policy: `ciWorkflow=false`, `requiredCheck=false`, `branchProtection=false`, `ruleset=false`, `mergeStrategy=false`, `prTemplate=false`, `commitFormat=false`
- 失敗状態: `fail-on-missing-or-drift`
- 入力: `implementation`, `generator-contract`, `pinned-isolated-python-runtime`, `canonical-requirements-json`, `explicit-applicable-requirement-ids`, `explicit-artifact-trace`, `test-source`
- 出力: `generated-design`, `drift-result`, `exact-requirement-artifact-test-trace`, `structured-unsupported-surface-or-bounded-fail-closed-diagnostic`
- 義務: `verify-operation-sql-and-typed-query-generation`, `verify-japanese-explanations-at-generator-source`, `inventory-required-design-surfaces`, `connect-missing-generators`, `require-human-readable-markdown`, `reject-missing-design`, `run-with-pinned-isolated-runtime`, `generate-deterministic-as-built`, `verify-isolation-and-drift`, `match-explicit-applicable-active-set-exactly`, `reject-unknown-inactive-missing-or-excess-trace`
- 禁止事項: `do not modify the target repository virtual environment`, `do not edit generated design directly`, `do not infer requirement satisfaction from implementation`, `do not mark missing required design complete or impose CI policy`
- 依存Skill: なし
- 必須asset: `references/sql-and-language.md`, `assets/as-built-thresholds.json`, `references/adoption.md`, `scripts/check_design.py`, `references/cdk-contract.md`, `references/fastapi-contract.md`, `requirements.txt`, `scripts/designflow.py`, `scripts/qualityflow.py`
- 要件trace: `REQ-ASBUILT-001`, `REQ-ASBUILT-002`, `REQ-ASBUILT-003`, `REQ-ASBUILT-004`, `REQ-ASBUILT-005`, `REQ-ASBUILT-006`, `REQ-ASBUILT-007`, `REQ-ASBUILT-008`, `REQ-ASBUILT-009`, `REQ-ASBUILT-010`, `REQ-ASBUILT-011`, `REQ-ASBUILT-012`, `REQ-ASBUILT-013`, `REQ-ASBUILT-014`, `REQ-ASBUILT-015`, `REQ-ASBUILT-016`, `REQ-ASBUILT-018`, `REQ-ASBUILT-020`, `REQ-ASBUILT-021`, `REQ-DESIGN-001`, `REQ-DESIGN-002`, `REQ-DESIGN-003`, `REQ-DESIGN-004`, `REQ-DESIGN-005`, `REQ-DESIGN-006`, `REQ-DESIGN-007`, `REQ-DOCS-002`
- manual digest: `5129ffad0ba1f2037df03a771b80da3d0d6c4d58322f2cf567a177bd980219a5`
- payload digest: `39610f20062364120d6b19791f5bb749914a9afacdd6a4b7eb47398cc7db78de`
- interface digest: `2d53132a9471f1f73d6578654fd68cb4141b62c915e7d1ace402385808ef9f42`

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
- manual digest: `bf4f083149b4e0304fad22e317ed28bf8ad564a78066a1e3a4fe455f143a28fa`
- payload digest: `c5906a3efc5407865ee4b2d825332b46a61541613fb33253d573d9d8fe10e1ae`
- interface digest: `9bef3e4b8a30e1c39effdddb1f0101f892ce21ec8a2b468de3bf43f6af507d30`

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
- manual digest: `713ec708fe88eabdb3bf0408c0e1c1a4074b71c46df9b1cab8234799f26d2b1a`
- payload digest: `b6ac505f0c8ee8554d0ffc8d330739f636f4363265dd3d6ef23656a67236c911`
- interface digest: `d43aeb305cf1db96d64568e1d231ad529686b1ef3b92c86d8a2c4e0df7f2bb50`

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
- 義務: `verify-operation-sql-and-typed-query-generation`, `verify-japanese-explanations-at-generator-source`, `select-minimum-relevant-checks`, `validate-registry-command-and-declared-effect-when-runner-is-used`, `execute-selected-checks`, `report-process-effect-isolation-uncertainty-for-every-command`, `bound-verdict-to-observed-evidence`
- 禁止事項: `do not modify source to hide failures`, `do not claim external-effect absence process isolation or unselected coverage`, `do not execute a declared external effect without explicit authority`, `do not create CI or merge policy`
- 依存Skill: なし
- 必須asset: `references/gate-rules.md`, `references/runner-contract.md`, `scripts/inspect.py`
- 要件trace: `REQ-ASBUILT-019`, `REQ-QUALITY-002`, `REQ-DESIGN-007`, `REQ-DOCS-002`
- manual digest: `9a41d0b94433aedeef19a12e316d110dcc5dee70d2094dbe972decf191e14dbb`
- payload digest: `a474c9650ac451e4cebd1d40df9a5bad8acc631c962eced70c6b828f4de77408`
- interface digest: `073b20f8a4c4f30a38fac5fb4ae66a56ee7e97caf4cb96beeea189b26e391fd1`

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
- manual digest: `740237d898f1b183deb594df8e310e271abd2e82dd841037bd4a0c62b054e802`
- payload digest: `74dea666a7d9914d3c92f5bf16d74ae0b6ae1207a68d4da377e74541ed0ff08c`
- interface digest: `3cd81796135cb9dceb62bfdd67ea29d90f7114d9c2e9458e1d848abbbcc82423`

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
- manual digest: `384c51bbc94169ba05caa0c5c4dc60a864c0f471a10dd10467daa9ec543151e8`
- payload digest: `7f497d1fa2d81cfa91cbdab77b3aebb4e4d73bb88008579984370931661fcc43`
- interface digest: `b01e1f0024fed3697ccf71d93c9111cd47755cf531217ecbf61dfb66ec7b6a89`

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
- manual digest: `bc32c8ece88b4d744bc8395f421d2b3e06f3c6e751223815e69d185c706d27ca`
- payload digest: `a326bcc3756108c0dc1a8d07cb16a5bd85d63a7f4fb0aee45f7a5bed6b8656d4`
- interface digest: `3d060df2a991b7e9c891bcc86678132f72fdae5435b644b3c9a8c8b242f72f6c`

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
- manual digest: `0cb999de00126d6fcee37d346a91cd58c2ce3965552f3d394fbc34793052f428`
- payload digest: `8bddd1c183b216d2ff52bc8a016b430b202df65b8f7e1b1177fec4bbf7a1a629`
- interface digest: `b6e41b56a6ba2fe48c3ce901f0d83eac72ad651d9bea2224946efcdacd9eece3`

### right-size-execution

- 前提: execution sizing is needed; exact profile and stopping evidence apply only when measured execution is selected
- 事後条件: minimum sufficient checks are selected; measured execution additionally has an exact verification projection, bounded diagnostics, and tamper-evident stopping evidence
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
- manual digest: `f5d3ddb338b6fea71326b34c8cc9468d3df92a175b1b2ff88755478a5d494c3a`
- payload digest: `4c1b2d00f7d4597070f1d8bd6c8d032f3712e64ccaa8b08f86a32afd02bb3ea5`
- interface digest: `0da8298df4216322130c6c5eed94f9b98fa68557b8e2a24378f84e572a1b20a8`

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
- manual digest: `0df812138601c4432c5d650acb027955b5146aa75dd76413b175188f63619a6e`
- payload digest: `ae93336d0c22d3524dc0615c389b1cec418b953875d59fb7ffd1f943abb2d0a6`
- interface digest: `75a61d820c9f0f7aeca8315708801ba28ce17a3850b1372b6ec45f9962c9c6d4`

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
- manual digest: `e9dca0bd1c9c450fe0aba6cffa4621b85037ab06e32ebbd7058b7ab7b98398f9`
- payload digest: `43e8ae228716003160d8796993fb6387c9f3310ec98e9017cf3f50dd4da5cd16`
- interface digest: `4849946704e4fff8bf109eb0ad4eff8513f9e717cd21e00f79893f68cdb9cd89`
