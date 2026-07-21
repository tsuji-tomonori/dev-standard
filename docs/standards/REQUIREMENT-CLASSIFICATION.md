# 要件分類標準

## 1. 目的

この標準は、移植可能なSkills・agents・統制部品を扱う際に、永続要件をSWEBOKに沿って分類し、成果物と変更証跡を混同しないための判断規則を定める。

要件の唯一の正本は`spec/requirements/requirements.json`である。この文書は分類方法を説明する人向け標準であり、個々の要件の第二正本ではない。

参照資料は`governance/standards/registry.json`の`SWEBOK-V4A`を使用する。SWEBOKのSoftware Requirementsでは、software product requirementsとsoftware project requirements、functional requirementsとnonfunctional requirements、technology constraintsとquality-of-service constraintsを区別する。本repositoryでは、その区別を次の二段階判定へ適用する。

## 2. 二段階分類

### 2.1 Scope: product / projectの判定

| Scope | 対象 | 例 |
|---|---|---|
| `product` | 導入先へ提供するsoftware、Skill、agent、generator、schema、CLI等の外部挙動または品質 | 自然言語からSkillを起動できる、同一入力から同一生成物を得る、公開schemaを維持する |
| `project` | 開発・保守・レビュー・配布・文書化の進め方、成果物、証跡、更新責任 | 文書を所定の条件で更新する、review YAMLを検証する、配布profileの互換性を確認する |

「このrepositoryで作業した」という事実はproject requirementではない。今後も繰り返し守る義務だけをproject requirementとして正本化する。

### 2.2 Category: functional / nonfunctionalの判定

| Category | 判定 | 例 |
|---|---|---|
| `functional` | 主体が実行する能力、処理、変換、応答を規定する | 要件差分をadd / update / retireとして適用する、manifestからprofileを導入する |
| `nonfunctional` | 品質、制約、閾値、技術選択、プロセス、成果物、運用保証を規定する | 決定論性、互換性、security、文書の鮮度、直接編集禁止、証跡の保持境界 |

`scope`と`category`は独立に判定する。たとえば、generatorの決定論性は`product / nonfunctional`、文書更新ルールは`project / nonfunctional`である。

## 3. Documentation requirementsの管理

文書の存在、内容、品質、更新、配布、廃止に関する義務は、原則として`project / nonfunctional`として管理する。

例外は、その文書または文言自体が利用者へ提供するproduct behaviorである場合である。アプリケーション内のhelp、利用者へ表示するerror message、契約上の帳票内容等は`product`側へ分類する。

永続的なdocumentation requirementは、少なくとも次を受入条件または検証情報として持つ。

1. **Audience**: 誰が読むか。
2. **Purpose**: 読者が何を判断または実行できる必要があるか。
3. **Authority**: 何を正本とし、文書が正本・生成表示・説明資料のどれか。
4. **Update trigger**: どの変更で更新するか。
5. **Verification**: 内容、link、生成drift、freshness等をどう検証するか。
6. **Maintenance rule**: owner、再確認条件、互換性、更新方法。
7. **Retirement condition**: いつ削除またはsupersedeできるか。

Markdown fileの存在自体を要件にしない。満たすべき義務を正本へ記録し、文書pathは`traces.design`または`traces.implementation`から接続する。

## 4. 成果物への写像

| 情報 | 置き場所 | 扱い |
|---|---|---|
| 永続的なproduct / project requirement | `spec/requirements/requirements.json` | add / update / retireで現在状態を維持する |
| 人向け要件表示 | `docs/requirements/REQUIREMENTS.md` | 正本から生成し直接編集しない |
| documentation requirementを実現する文書 | `docs/`、README、runbook等 | 対応するproject NFRのtriggerで更新する |
| 実装由来の現在状態 | `docs/design/generated/` | 実装から生成しdriftを検査する |
| 長期判断の理由 | `docs/decisions/` | ADRとしてstatusを管理する |
| 変更時点の証跡 | Commit Comment、review YAML、PR、CI | documentation requirementの正本へ昇格させない |
| 再開用状態 | `.devflow/run/` | Git管理せず完了後に削除する |

変更ごとの計画書、implementation log、test report、release report、retrospectiveを、工程が存在するという理由だけで作らない。利用者、法令、契約、安全、運用上の永続義務があり、project NFRとして検証可能な場合だけ恒久文書を作る。

## 5. この参照repositoryの境界

このrepositoryは導入先projectの稼働中workを保管する場所ではない。top-levelの`work/`へrepository固有の依頼、承認、phase記録、test reportを保存しない。

regulated runtimeの実装、template、schema、validatorは移植可能なsampleとして維持できる。実行中の`work/<id>/`は、regulated profileを選択した導入先repositoryで生成する。回帰fixtureが必要な場合は`tests/fixtures/`等へsyntheticであることを明示して置く。

## 6. 判定手順

1. 将来も守る義務か、今回だけの作業情報かを分ける。
2. 義務の対象を`product`または`project`へ分類する。
3. 能力・処理なら`functional`、品質・制約・成果物・プロセスなら`nonfunctional`へ分類する。
4. documentation requirementならAudienceからRetirement conditionまでを定義する。
5. 正本へadd / update / retireを適用し、文書はtraceされた実現手段として更新する。
6. Commit Commentへ要件影響と分類理由を記録する。

## 7. 例

| 依頼 | 分類 | 扱い |
|---|---|---|
| OpenAPIからAPI referenceを生成しdriftを拒否する | `project / nonfunctional` | 生成、更新trigger、検証を要件化し、文書は生成表示にする |
| UIのhelp textで利用者へ操作方法を示す | `product / functional`または`product / nonfunctional` | 利用者が得る結果と品質に応じてproduct requirementへ置く |
| PRごとにtest logをMarkdownへ保存する | 原則として永続要件にしない | CIを正本とし、必要な検証契約だけを残す |
| 重大障害時に復旧runbookを最新化する | `project / nonfunctional` | audience、trigger、verification、retirementを要件化する |
| 今回の調査メモを残す | 一時情報 | `.devflow/run/`または会話に留め、完了後に削除する |

## 8. Review checklistの確認

- product requirementとproject requirementを混同していない。
- functional behaviorとnonfunctional constraintを一つの原子的義務へ詰め込んでいない。
- 文書fileではなく、文書が満たす義務を正本化している。
- 文書のAudience、Authority、Update trigger、Verification、Retirement conditionが分かる。
- 生成表示、手書き標準、ADR、変更証跡のauthorityが重複していない。
- repository固有のlive work recordをsample artifactとして残していない。
