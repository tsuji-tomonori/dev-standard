---
name: chat-first-development
description: Complete development requests through a lightweight three-pillar flow: durable requirements, implementation-derived design, and only the checks relevant to the change.
---

# Chat-first Development

## Formal specification

`spec/skills/skills.qnt` の `skillContracts` にある `name: "chat-first-development"` を形式契約とする。

形式契約の`applicability`と`activationContexts`に該当しない場合は起動せず、artifactやblocking判定を作らないno-opとする。

自然言語の依頼を入口に、対象repositoryの規則を維持したまま成果を完成させる。portableなguardrailは次の3本柱だけである。

1. 永続的な外部義務が変わる場合だけ、Quint要件正本を更新する。
2. 対象generatorがある場合だけ、実装からas-built設計を生成してdriftを確認する。
3. 変更に関係するcheckだけを選び、最小十分な検証を行う。

## Workflow

1. 依頼、対象repositoryの`AGENTS.md`等、変更対象、権限境界を確認する。
2. 利用者向け挙動、受入条件、恒久制約が変わるかを判定する。
3. 変わる場合だけ`$maintain-canonical-requirements`を使う。変わらない場合は要件artifactを作らない。
4. 実装または文書を変更する。
5. 宣言済みgeneratorが変更対象を扱う場合だけ`$generate-implementation-design`を使う。
6. `$inspect-quality-gates`で対象test、build、lint、type、drift等から関連するものだけを実行する。
7. 実際の変更、検証結果、未検証範囲を利用者へ返す。

失敗、新しい依存、公開契約への影響が見つかった場合だけ、その根拠に対応する範囲を広げる。成功条件を満たしたら停止する。

## Repository policy boundary

このSkillは次を要求、作成、変更しない。

- branch構成、branch protection、ruleset
- merge方式、merge先、review人数
- CI/CD workflow、required check、status check
- Commit Commentの書式
- PR template、review YAML、変更ごとの計画書やtest report

PRの作成・更新・comment・review・mergeやCI設定の修正は、それぞれが現在の依頼に明示されている場合だけ行い、対象repositoryに既にある規則と権限へ従う。code変更の依頼だけからPR操作を推測しない。CIがないrepositoryではローカル検証を正当な証拠として扱い、このSkillを理由にCIを導入しない。

## Requirement impact

外部挙動、業務ルール、受入条件、非機能閾値、権限要求、恒久的なproject義務が変わる場合だけ要件影響ありとする。

framework、language、database、tool、path、process、成果物が依頼に含まれるだけでは永続要件にしない。underlying outcome、exact choiceの必要性とauthority、lifetime、scopeを判定し、可逆な実装選択は実装、長期判断はADR、実装済み構造は生成設計へ置く。

## Design impact

実装から導出できる現在構造は生成設計へ置く。コードから分からない長期判断だけをADR候補とする。generatorが存在しない対象へ、新しいgeneratorや設計書をこのSkillだけの都合で要求しない。

## Check selection

- 変更した受入条件へ対応するtest
- 対象repositoryが既に定めるbuild、lint、type、security check
- 変更対象generatorのdrift check
- 公開契約、migration、IaC等へ直接関係する互換性check

未選択checkをN/Aとして記録せず、repository全体のchecklistを一律実行しない。

## Authority boundaries

- secrets、PII、production dumpを保存しない。
- 外部書込み、公開、merge、削除、production操作、高額・不可逆操作は、依頼または明示承認の範囲だけで行う。
- gateを通す目的でtest、型、lint、security controlを弱めない。
- 対象repositoryのownership、build、security、commit、release規則を上書きしない。

repository内の可逆な実装は依頼された成果の範囲で進められる。外部または共有状態を変える操作は、利用者の明示依頼と必要な承認が現在も有効な場合だけ実行し、対象、効果、停止条件を越えない。通常の外部操作だけを理由にregulated work itemを作らない。

## Completion

- 依頼された成果が実装または文書へ反映されている。
- 該当する3本柱だけが適用されている。
- selected checkにblocking failureが残っていない、または失敗と未完了範囲が明示されている。
- branch、merge、CI方針を新しく強制していない。
- 実行した外部操作がある場合は、明示依頼・承認範囲と実結果が対応している。
- PR操作がある場合は、その種類が現在の依頼に含まれている。

<!-- BEGIN GENERATED QUINT CONTRACT -->
## Quint contract（自動生成）

このblockは`spec/skills/skills.qnt`から生成するviewです。直接編集しません。

- Skill: `chat-first-development`
- 役割: orchestrator
- 柱: auxiliary
- guardrail: no
- repository blocking: no
- 既定portable: yes
- 適用条件: when-development-is-requested
- 起動context: `development-request`
- 外部作用capability: yes
- repository policy `ciWorkflow`: false
- repository policy `requiredCheck`: false
- repository policy `branchProtection`: false
- repository policy `ruleset`: false
- repository policy `mergeStrategy`: false
- repository policy `prTemplate`: false
- repository policy `commitFormat`: false
- 前提: a development outcome is requested
- 事後条件: the requested outcome and only applicable pillars are complete, and every external effect remains within explicit authority
- Authority: user-and-target-repository
- 副作用: repository-and-authorized-external-write
- 失敗状態: report-bounded
- 入力: `request`, `target-repository-rules`, `authority-boundary`
- 出力: `change`, `verification-summary`, `external-operation-result`
- 義務: `classify-durable-requirement-impact`, `generate-supported-as-built-design`, `run-only-selected-checks`, `bind-external-effects-to-authority`, `perform-pr-operation-only-when-requested`
- 禁止事項: `do not impose CI branch or merge policy`, `do not create per-change bureaucracy`, `do not create update comment or merge a PR unless requested`
- 依存Skill: `maintain-canonical-requirements`, `generate-implementation-design`, `inspect-quality-gates`
- 必須asset: `references/bootstrap-and-conversation.md`
- 要件trace: `REQ-DISC-005`, `REQ-PORTABLE-001`, `REQ-PORTABLE-003`
- manual digest: `0708a9c422d1b68fc7c0a451d3b385858c32cfd5cf63743472c7e8427dd34ede`
- payload digest: `23e2400ebf4e7aad2ff46da62f6a61ad8b0899c21a60ded4d246706395f6ff2c`
- interface digest: `fb458bd3bba0d3d1ee4cd64f42523207190dd082f61b7b93cebd0697654a470d`
<!-- END GENERATED QUINT CONTRACT -->
