<!-- tools/quintflow.pyによる自動生成。spec/skills/skills.qntを編集すること。 -->
# Skills形式仕様

全Skillの機械可読契約と3本柱の不変条件を、人向けに表示した派生文書です。

- 正本: `spec/skills/skills.qnt`
- Quint: `0.32.0`
- Skill数: 18

| Skill | 役割 | 柱 | Guardrail | 既定配布 |
|---|---|---|---|---|
| `adversarial-review` | independent-review | 補助 | なし | 含めない |
| `author-lifecycle-docs` | regulated-documentation | 補助 | なし | 含めない |
| `authorize-autonomous-execution` | authority-boundary | 補助 | なし | 含めない |
| `calibrated-collaborative-listening` | intent-clarification | 補助 | なし | 含めない |
| `chat-first-development` | orchestrator | 補助 | なし | 含む |
| `design-frontend-experience` | frontend-design | 補助 | なし | 含めない |
| `elicit-frontend-requirements` | frontend-requirements | 補助 | なし | 含めない |
| `generate-implementation-design` | as-built-design | as-built設計 | blocking | 含む |
| `govern-development-request` | regulated-orchestration | 補助 | なし | 含めない |
| `implement-frontend-experience` | frontend-implementation | 補助 | なし | 含めない |
| `inspect-quality-gates` | selected-checks | 選択check | blocking | 含む |
| `japanese-git-commit-gitmoji` | commit-message | 補助 | なし | 含めない |
| `maintain-canonical-requirements` | canonical-requirements | 要件正本 | blocking | 含む |
| `maintain-reference-repository` | reference-maintenance | 補助 | なし | 含めない |
| `retrospect-and-improve` | retrospective | 補助 | なし | 含めない |
| `right-size-execution` | execution-sizing | 補助 | なし | 含めない |
| `test-frontend-experience` | frontend-testing | 補助 | なし | 含めない |
| `verify-against-engineering-standards` | standards-lens | 補助 | なし | 含めない |

## 検証する不変条件

- 全Skill directoryと形式契約が一対一で対応する。
- blocking guardrailは要件正本、as-built設計、選択checkの3本柱だけに属する。
- portable契約はCI workflow、branch rule、merge方式を要求しない。
- 既定profileは入口Skillと3本柱の4 Skillだけである。
- 要件、設計、checkの順序を飛び越えた完了状態へ到達しない。

## 各Skillの契約

### adversarial-review

- 前提: falsifiable claims and an authority are available
- 事後条件: counterexamples and bounded findings are reported
- Authority: `artifact-authority`
- 副作用: `none`
- 入力: `artifact`, `authority`, `review-scope`
- 出力: `findings`, `residual-uncertainty`

### author-lifecycle-docs

- 前提: a concrete regulated retention duty exists
- 事後条件: only required lifecycle evidence is retained
- Authority: `law-contract-or-user`
- 副作用: `repository-write`
- 入力: `regulated-duty`, `retention-rule`
- 出力: `regulated-evidence`

### authorize-autonomous-execution

- 前提: an external or irreversible authority boundary exists
- 事後条件: authorization scope and stop conditions are explicit
- Authority: `explicit-user-authorization`
- 副作用: `external-approval`
- 入力: `requested-result`, `external-effects`, `rollback`
- 出力: `authorization-decision`

### calibrated-collaborative-listening

- 前提: multiple interpretations materially change the result
- 事後条件: a correctable goal and decision are available
- Authority: `user-intent`
- 副作用: `none`
- 入力: `request`, `constraints`
- 出力: `correctable-goal`, `decision`

### chat-first-development

- 前提: a development outcome is requested
- 事後条件: only applicable pillars have been completed
- Authority: `user-and-target-repository`
- 副作用: `repository-write`
- 入力: `request`, `target-repository-rules`
- 出力: `change`, `verification-summary`

### design-frontend-experience

- 前提: frontend outcomes and constraints are known
- 事後条件: minimum implementation decisions are explicit
- Authority: `approved-requirements`
- 副作用: `repository-write`
- 入力: `requirements`, `existing-design-system`
- 出力: `design-decisions`, `verification-hooks`

### elicit-frontend-requirements

- 前提: a frontend outcome is requested
- 事後条件: durable observable obligations are identified
- Authority: `user-intent`
- 副作用: `repository-write`
- 入力: `user-task`, `context`, `failure-impact`
- 出力: `requirement-candidates`, `design-context`

### generate-implementation-design

- 前提: a declared generator supports the changed implementation
- 事後条件: generated design is deterministic and matches implementation
- Authority: `implementation`
- 副作用: `repository-write`
- 入力: `implementation`, `generator-contract`
- 出力: `generated-design`, `drift-result`

### govern-development-request

- 前提: a concrete regulated lifecycle duty exists
- 事後条件: regulated evidence is complete within that duty
- Authority: `law-contract-or-user`
- 副作用: `repository-write`
- 入力: `regulated-trigger`, `authority-boundary`
- 出力: `regulated-record`

### implement-frontend-experience

- 前提: frontend requirements and decisions are ready
- 事後条件: the user task works in supported states
- Authority: `requirements-and-design`
- 副作用: `repository-write`
- 入力: `requirements`, `design-decisions`, `existing-frontend`
- 出力: `frontend-change`, `tests`

### inspect-quality-gates

- 前提: changed artifacts and applicable risks are known
- 事後条件: only selected checks have a verdict
- Authority: `target-repository-and-selected-checks`
- 副作用: `none`
- 入力: `change`, `target-checks`
- 出力: `selected-check-results`, `residual-risk`

### japanese-git-commit-gitmoji

- 前提: the target repository requests this commit style
- 事後条件: a Japanese structured commit message is proposed
- Authority: `target-repository-style`
- 副作用: `none`
- 入力: `diff`, `verification-summary`
- 出力: `commit-message`

### maintain-canonical-requirements

- 前提: a durable observable obligation changes
- 事後条件: Quint source, derived JSON, and generated docs agree
- Authority: `quint-requirements`
- 副作用: `repository-write`
- 入力: `durable-obligation`, `source`, `acceptance`
- 出力: `requirements-qnt`, `requirements-json`, `requirements-doc`

### maintain-reference-repository

- 前提: dev-standard portable assets change
- 事後条件: portable and repository-specific assets remain separated
- Authority: `reference-repository`
- 副作用: `repository-write`
- 入力: `reference-change`, `distribution-boundary`
- 出力: `portable-assets`, `compatibility-result`

### retrospect-and-improve

- 前提: an evidenced recurring defect or cost exists
- 事後条件: a bounded evaluable improvement is proposed
- Authority: `observed-defect`
- 副作用: `repository-write`
- 入力: `defect-evidence`, `impact`
- 出力: `improvement-candidate`

### right-size-execution

- 前提: verification depth is not already explicit
- 事後条件: the smallest sufficient verification scope is selected
- Authority: `change-risk`
- 副作用: `none`
- 入力: `change-risk`, `available-evidence`
- 出力: `verification-scope`

### test-frontend-experience

- 前提: frontend requirements and implementation are available
- 事後条件: claims are limited to executed test scope
- Authority: `frontend-requirements`
- 副作用: `none`
- 入力: `requirements`, `implementation`, `supported-environment`
- 出力: `test-results`, `residual-risk`

### verify-against-engineering-standards

- 前提: a relevant standard is selected for the change
- 事後条件: only applicable controls have findings
- Authority: `selected-official-standards`
- 副作用: `none`
- 入力: `change`, `selected-standard`
- 出力: `standard-findings`
