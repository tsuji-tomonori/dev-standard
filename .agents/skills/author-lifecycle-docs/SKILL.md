---
name: author-lifecycle-docs
description: Create work-item and phase documents only for regulated legal, contractual, safety, production, or audit evidence. Do not create lifecycle documents for ordinary direct or assured changes.
---

# Author Regulated Lifecycle Documents

## Formal specification

`spec/skills/skills.qnt` の `skillContracts` にある `name: "author-lifecycle-docs"` を形式契約とする。

このSkillは`regulated` profile専用である。

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
