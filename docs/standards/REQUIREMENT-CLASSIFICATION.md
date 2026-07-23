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

`nonfunctional`へ分類できることは、その具体を永続要件へ固定してよいことを意味しない。技術選択、architecture、tool、path、process、工程、成果物は、次のsolution specificity gateを通してから分類する。

## 3. Solution specificity gateの判定

上位要件は原則としてsolution-neutralにし、利用者またはconsumerが必要とする結果、外部から観測可能な振る舞い、quality of service、互換性、安全性、運用保証を記述する。具体的なframework、language、database、architecture style、tool、repository path、実装順、開発手法、工程、成果物は、その選択自体が権限ある永続制約である場合、または上位判断から下位scopeへ派生した義務である場合だけ要件化する。

「具体技術を書かない」という一律禁止ではない。候補に具体的なsolutionが含まれる場合は、次の順に判定する。

1. **Underlying obligation**: その具体を外すと失われる利用者結果、観測可能な振る舞い、quality of service、interoperability、法令・契約適合、安全性、運用保証は何か。
2. **Necessity**: exact choice自体が必要か、outcome、quality threshold、interface constraint、supported environment等へ戻せるか。
3. **Authority**: durableな利用者判断、consumer contract、public compatibility、法令・規制・安全義務、採用済み標準、repository policy、既存platform・hardware・protocol・migration・support境界、承認済みADRまたは親要件のどれに根拠を持つか。単なる例示、agentの提案、一般的best practiceはauthorityにしない。
4. **Lifetime and scope**: 今回の変更だけのinstructionか、将来も維持するobligationか。system、product、project、subsystem、teamのどこへ適用するか。
5. **Placement**: 次の表に従い、正本、ADR、生成設計、一時contextを分ける。

| 判定結果 | 置き場所 | 必須情報 |
|---|---|---|
| outcome、observable behavior、quality threshold、外部制約 | 要件正本 | source、acceptance、verification、適用scope |
| exact technologyまたはproject processが権限ある永続制約 | 要件正本 | `source_refs`、必要性を示す`rationale`、`scope` / `category`、verification |
| 可逆なimplementation choiceまたはsafe default | 実装 | repository conventionと検証に従い、追加質問や正本化をしない |
| 理由を将来も保持するarchitecture choice | ADR | decision、alternatives、rationale、consequences |
| 実装済みの現在構造 | `docs/design/generated/` | 実装から生成しdriftを検査する |
| 今回だけのtool、順序、path、作業方法 | current requestまたは`.devflow/run/` | 完了後に正本として残さない |
| 親要件または承認済みdecisionが下位scopeを拘束 | derived requirement | 親要件またはADR、下位scope、verificationへのtrace |

利用者が具体技術を名指ししても、それだけでdurable product requirementとは判定しない。今回の実装指示には従い得るが、将来も維持する義務かを分ける。反対に、既設機器、support contract、互換protocol、法令、安全性等がexact choiceを要求する場合は、technology constraintとして保持する。

solution-neutralityは、要件を凍結してarchitecture検討を遅らせる規則ではない。要件とarchitectureは反復的に再分析できる。ただし、architecture上の発見でunderlying obligationを更新することと、設計判断をstakeholder requirementとして偽装することを区別する。system全体ではADRである判断が、下位teamから見て拘束となる場合は、親decisionへtraceしたderived requirementとしてscopeを限定する。

## 4. Documentation requirementsの管理

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

## 5. 成果物への写像

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

## 6. この参照repositoryの境界

このrepositoryは導入先projectの稼働中workを保管する場所ではない。top-levelの`work/`へrepository固有の依頼、承認、phase記録、test reportを保存しない。

regulated runtimeの実装、template、schema、validatorは移植可能なsampleとして維持できる。実行中の`work/<id>/`は、regulated profileを選択した導入先repositoryで生成する。回帰fixtureが必要な場合は`tests/fixtures/`等へsyntheticであることを明示して置く。

## 7. 判定手順

1. 将来も守る義務か、今回だけの作業情報かを分ける。
2. named technology、architecture、tool、path、process、工程、成果物を含む場合は、underlying obligation、necessity、authority、lifetime、scope、placementを判定する。
3. 義務の対象を`product`または`project`へ分類する。
4. 能力・処理なら`functional`、品質・制約・成果物・プロセスなら`nonfunctional`へ分類する。
5. documentation requirementならAudienceからRetirement conditionまでを定義する。
6. exact choiceを永続化する場合はsource、rationale、scope、verificationを持たせ、derived requirementは親判断へtraceする。
7. 正本へadd / update / retireを適用し、文書はtraceされた実現手段として更新する。
8. Commit Commentへ要件影響、分類、solution specificityの判定理由を記録する。

## 8. 例

| 依頼 | 分類 | 扱い |
|---|---|---|
| OpenAPIからAPI referenceを生成しdriftを拒否する | `project / nonfunctional` | 生成、更新trigger、検証を要件化し、文書は生成表示にする |
| UIのhelp textで利用者へ操作方法を示す | `product / functional`または`product / nonfunctional` | 利用者が得る結果と品質に応じてproduct requirementへ置く |
| PRごとにtest logをMarkdownへ保存する | 原則として永続要件にしない | CIを正本とし、必要な検証契約だけを残す |
| 重大障害時に復旧runbookを最新化する | `project / nonfunctional` | audience、trigger、verification、retirementを要件化する |
| 今回の調査メモを残す | 一時情報 | `.devflow/run/`または会話に留め、完了後に削除する |
| 今回の変更をFastAPIで実装する | 原則として要件にしない | current-task instructionとして従い得るが、永続理由がなければ正本へ追加しない |
| support contract上Windows 11で動作する | `product / nonfunctional` | source、必要性、適用scope、verificationを持つtechnology constraintとして保持する |
| p95 latencyを200ms以内にする | `product / nonfunctional` | named technologyへ変換せずquality-of-service requirementとして保持する |
| architectがpipes-and-filtersを選ぶ | 原則ADR | system stakeholder requirementへ昇格させず、filter担当teamへは親decisionにtraceしたderived requirementとして扱える |
| Scrumと日次test reportを採用する | 根拠がなければ要件にしない | contract、policy、audit duty等がある場合だけ`project / nonfunctional`として保持する |
| productがFastAPI plugin互換を提供する | `product` requirement | product identityまたはconsumer interoperabilityに必要なinterface / constraintとして保持する |

## 9. Review checklistの確認

- product requirementとproject requirementを混同していない。
- named solutionを、利用者結果や権限あるconstraintなしに正本へ固定していない。
- exact technology、architecture、processを保持する場合、必要性、authority、lifetime、scope、verificationが分かる。
- reversible implementation choice、ADR、as-built design、current-task instruction、derived requirementを正しい成果物へ配置している。
- derived requirementが親要件またはdecisionへtraceされ、上位scopeへ過剰一般化されていない。
- functional behaviorとnonfunctional constraintを一つの原子的義務へ詰め込んでいない。
- 文書fileではなく、文書が満たす義務を正本化している。
- 文書のAudience、Authority、Update trigger、Verification、Retirement conditionが分かる。
- 生成表示、手書き標準、ADR、変更証跡のauthorityが重複していない。
- repository固有のlive work recordをsample artifactとして残していない。
