---
name: author-lifecycle-docs
description: Create lifecycle evidence only when a concrete legal, contractual, safety, production, or audit retention duty requires it. Do not create lifecycle documents for ordinary changes.
---

# Author Regulated Lifecycle Documents

## Formal specification

`spec/skills/skills.qnt` の `skillContracts` にある `name: "author-lifecycle-docs"` を形式契約とする。

形式契約の`applicability`と`activationContexts`に該当しない場合は起動せず、artifactやblocking判定を作らないno-opとする。

このSkillは、具体的な法令、契約、安全性、production、監査上の保持義務が特定された場合だけ起動する。配布profile名や変更規模だけでは起動しない。

## 通常変更で作らないもの

- `docs/00-request.md`
- `docs/01-requirements.md`
- `docs/01-traceability.md`
- `docs/01-execution-plan.md`
- 変更ごとのarchitecture、design、test plan
- implementation log
- test report
- security review report
- operations / maintenance report
- release report
- retrospective

通常変更では次を使用する。

- 要件正本
- 実装由来生成設計
- 必要なADR
- Git diffと対象repositoryが既に採用する変更記録
- 実行したローカル検査、または既存CIへの参照

## Regulatedで作成する条件

文書ごとに、法令、契約、監査、不可逆production操作、安全性、復旧責任等の具体的な必要性がある場合だけ作成する。

単にtemplateが存在することを理由に作らない。

## Workflow

1. regulated起動根拠と必要な文書を列挙する。
2. 各文書の将来利用者、利用目的、保持期間を定義する。
3. 要件正本、authority boundary、外部副作用、rollback、停止条件を記載する。
4. コード、test、生成設計、既存CIから取得できる情報を手書きで複製しない。
5. 実行結果の生ログを貼り付けない。
6. 未確定事項は結果へ影響するものだけ解消し、それ以外は明示的なassumptionまたはresidual riskとする。
7. 対象repositoryが採用する変更記録から文書へ到達できるようにする。

## Document classes

### Current-state authority

今後も維持する必要がある場合だけ、製品の正本へ反映する。

### Immutable regulated evidence

変更時点で固定し、後から現在状態へ合わせて書き換えない。

### Temporary execution state

監査保持が不要なら`.devflow/run/`へ置き、完了後に削除する。

## Boundaries

- template tokenを埋めること自体を目的にしない。
- コードから生成可能な詳細設計を手書きしない。
- Git diffから再構成可能なimplementation logを作らない。
- test resultの生ログを複製しない。
- CI、branch、merge、commit形式を新たに要求しない。
- 将来利用者と保持理由がない文書をGitへ追加しない。

## Completion

- 各文書に明確な利用目的と保持規則がある。
- 正本、変更証跡、一時状態が混在していない。
- 重複文書がない。
- 検証証拠があり、生ログを保存していない。
- regulated案件で必要な証跡だけが残る。

<!-- BEGIN GENERATED QUINT CONTRACT -->
## Quint contract（自動生成）

このblockは`spec/skills/skills.qnt`から生成するviewです。直接編集しません。

- Skill: `author-lifecycle-docs`
- 役割: regulated-documentation
- 柱: auxiliary
- guardrail: no
- repository blocking: no
- 既定portable: no
- 適用条件: when-concrete-duty-exists
- 起動context: `concrete-regulated-duty`
- 外部作用capability: no
- repository policy `ciWorkflow`: false
- repository policy `requiredCheck`: false
- repository policy `branchProtection`: false
- repository policy `ruleset`: false
- repository policy `mergeStrategy`: false
- repository policy `prTemplate`: false
- repository policy `commitFormat`: false
- 前提: a concrete regulated retention duty exists
- 事後条件: only required lifecycle evidence is retained
- Authority: concrete-duty-or-user
- 副作用: repository-write
- 失敗状態: no-op-unless-triggered
- 入力: `regulated-duty`, `retention-rule`
- 出力: `regulated-evidence`, `retention-disposition`
- 義務: `select-minimum-regulated-evidence`, `define-purpose-and-retention`, `separate-authority-evidence-and-temporary-state`
- 禁止事項: `do not create lifecycle documents for ordinary changes`, `do not retain raw logs or duplicated generated facts`, `do not impose repository policy`
- 依存Skill: なし
- 必須asset: `assets/template-map.json`, `references/document-rules.md`
- 要件trace: なし
- manual digest: `ebb57e538bf756d35cf2c2422179972d8f35a2731b38c13b4e61ad8c865dc78c`
- payload digest: `ef45fe345793aaccce17c13d1658556d6af7e926c2bed273b26f5a0edfaf3e9d`
- interface digest: `3cd8efe2ae6065ac22af9c9bf7414b8636403dc0754994c260d7881f42eab195`
<!-- END GENERATED QUINT CONTRACT -->
