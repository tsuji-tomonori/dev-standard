# AWS CDK実装・as-built設計標準

- 標準ID: `DEVSTD-AWS-CDK-AS-BUILT`
- 版: `2026-07-21`
- 基底標準: [`docs/standards/AS-BUILT-DESIGN.md`](AS-BUILT-DESIGN.md)
- 適用対象: AWS CDKを使用する導入先repository。原則はCloudFormationを出力する他のIaCへ写像できる
- 生成物path: `docs/design/generated/cdk/`
- 機械可読checkの正本: `governance/checks/catalog.yaml`
- 実行profileの正本: `right-size-execution`
- authority boundaryの正本: `authorize-autonomous-execution`

本標準は、AWS CDKによるインフラ実装から、実装と1対1で対応するas-built設計をコードから自動生成し、乖離をCIで機械的に検知するための要件を定める。あわせて、自動生成と安全なインフラ変更を成立させるため、実装規約とテスト規約を定める。

本書はアプリケーション層のas-built設計標準の姉妹編であり、同じ基本思想をIaC層へ適用する。コード例はCDKのPythonまたはTypeScriptを想定するが、原則はCloudFormationを出力する他のIaCにも適用できる。

## 1. 基本原則

| # | 原則 | 内容 | 主なcheck |
|---|---|---|---|
| C-1 | Single Source of TruthはCDKコード | 構成図、リソース一覧、IAM設計、パラメータ表を手で書かない。すべてrepository内の正本から派生させる。 | `FAST-006` |
| C-2 | 設計抽出の一次情報はsynthesized template | 設計生成はCDK sourceの解釈ではなく、`cdk synth`が出力したstackごとのCloudFormation templateを入力とする。synthは実装のdeploy時射影であり、L2/L3 constructに依存せず全resourceが確定形で現れる。 | `FAST-012`, `FAST-006` |
| C-3 | 決定論的synthと決定論的生成 | 同じsourceとcontextから常に同一templateを出力し、設計生成側も列挙をsortしてbyte一致させる。timestamp、乱数、実行環境依存値をtemplateまたは生成物へ含めない。 | `FAST-006`, `FAST-012` |
| C-4 | generate / checkの二相 | 設計生成toolは書込みmodeと、既存fileとの差分があれば非0終了するcheck modeを、同じ生成logicで提供する。CIではcheck modeを実行する。 | `FAST-006` |
| C-5 | 論理IDの安定性 | constructの移動やrenameによる論理ID変更はCloudFormation上の削除と再作成になり得る。特にstateful resourceの論理IDを規約とtestで保護する。 | `FAST-012` |
| C-6 | 生成物の機械的識別 | 自動生成物を`docs/design/generated/cdk/<stack>/`へ隔離し、Markdownを`.gen.md`で終端し、先頭へ自動生成・直接編集禁止・generate/check commandのbannerを付ける。 | `FAST-006` |
| C-7 | 差分の可視化がreview単位 | infrastructure変更ではCDK source差分だけでなく、synthesized templateの差分をreviewする。template差分にない変更はdeploy影響なしとして扱い、意図しないtemplate差分は欠陥として扱う。 | `IMP-009`, `FAST-012` |
| C-8 | policy準拠は合成時に機械検査 | security、tag、naming等の規約はAspectsやcdk-nag等で合成時に強制する。抑制は理由を必須とし、一覧を自動生成する。 | `FAST-012`, `AUD-008` |

## 2. 生成対象と一次情報

as-built設計として最低限、次の生成物を持つ。各生成物は一次情報を1か所に定め、それ以外の手書き情報を正本として参照しない。

| 生成物 | 一次情報 | 抽出方式 | Rule ID |
|---|---|---|---|
| resource catalog | synthesized templateの`Resources` | logical ID、type、主要property、所属stackをparseする | `CDK-DO-009` |
| parameter・環境差分表 | synthesized templateの`Parameters`と環境設定の正本file | parseして環境間diffをtableにする | `CDK-DO-010` |
| stack構成・依存関係図 | `cdk.out`のmanifestとtemplateの`Export` / `Fn::ImportValue` | parseし、Mermaidでstack間依存を描画する | `CDK-DO-011` |
| resource依存graph | templateの`Ref` / `Fn::GetAtt` / `DependsOn` | parseし、Mermaidで構成図を生成する | `CDK-DO-012` |
| IAM権限設計書 | templateの`AWS::IAM::*` resourceとinline policy | role×policy×resourceに加え、「このresourceへ書込み可能なrole」の逆引き表を生成する | `CDK-DO-013` |
| network設計書 | VPC、subnet、security group、route等のnetwork resource | SG許可をsource→destination→portのtableで生成する | `CDK-DO-014` |
| stateful resource台帳 | 該当resourceの`DeletionPolicy` / `UpdateReplacePolicy`、backup、encryption property | data保持、削除保護、backup、暗号化を一覧化し、保護なしresourceを機械抽出可能にする | `CDK-DO-015` |
| suppression一覧 | source中のcdk-nag suppression等 | rule ID、理由、箇所を静的解析して一覧化する | `CDK-DO-016` |
| cross-stack / external reference catalog | templateの`Outputs` / `Export`、SSM parameter、Secrets参照 | 他systemとのcontract pointを1表に集約する | `CDK-DO-017` |

### 2.1 生成規則

| Rule ID | Norm | 規則 | Check ID |
|---|---|---|---|
| `CDK-DO-001` | MUST | 同一source、lockfile、CDK context、account/region設定からbyte一致するsynthesized templateを生成する。 | `FAST-012` |
| `CDK-DONT-001` | MUST NOT | timestamp、乱数、current directory、absolute path、未固定の外部応答など、実行ごとに変化する値をtemplateへ含めない。 | `FAST-012` |
| `CDK-DO-002` | MUST | as-built設計の一次情報をsynthesized templateと`cdk.out` manifestに限定する。source ASTはsuppressionとescape hatch等、templateに残らない情報だけへ使用する。 | `FAST-006`, `FAST-012` |
| `CDK-DONT-002` | MUST NOT | resource catalog、構成図、IAM table、network table、parameter table、stateful台帳を手書きの現在状態として管理しない。 | `FAST-006` |
| `CDK-DO-003` | MUST | 全列挙を安定keyでsortし、同一入力からbyte一致する設計出力を生成する。 | `FAST-006` |
| `CDK-DO-004` | MUST | 一つの生成logicをgenerate modeとcheck modeで共有し、check modeは差分fileのrepository相対pathを列挙して非0終了する。 | `FAST-006` |
| `CDK-DO-005` | MUST | Markdown生成物を`docs/design/generated/cdk/<stack>/*.gen.md`へ置き、直接編集禁止とgenerate/check commandを含むbannerを先頭へ出力する。 | `FAST-006` |
| `CDK-DONT-003` | MUST NOT | 生成物を直接編集してsourceとのdriftを隠さない。 | `FAST-006` |
| `CDK-DO-006` | MUST | template resource、parameter、output、dependency、policy statement、network ruleを安定したlogical keyで識別する。 | `FAST-006` |
| `CDK-DO-007` | MUST | source suppression、escape hatch、明示physical nameなどtemplateだけでは理由を復元できない情報を、理由・rule ID・source位置付きで生成する。 | `AUD-008`, `FAST-021` |
| `CDK-DO-008` | MUST | manifestと全stack templateの入力digest、generator version、生成file一覧をmachine-readable manifestへ記録する。 | `FAST-006` |
| `CDK-DO-009` | MUST | 全stackの`Resources`からresource catalogを生成する。 | `FAST-006` |
| `CDK-DO-010` | MUST | 全対象環境の`Parameters`と型検証済み環境設定から環境差分表を生成する。 | `FAST-006`, `FAST-012` |
| `CDK-DO-011` | MUST | `cdk.out` manifestとexport/import関係からstack構成・依存関係図を生成する。 | `FAST-006` |
| `CDK-DO-012` | MUST | `Ref`、`Fn::GetAtt`、`DependsOn`からresource依存graphを生成する。 | `FAST-006` |
| `CDK-DO-013` | MUST | IAM resourceとpolicy statementからrole×action×resource表およびresource→書込み可能roleの逆引き表を生成する。 | `FAST-006`, `FAST-012` |
| `CDK-DO-014` | MUST | network resourceからVPC、subnet、route、security groupと通信許可表を生成する。 | `FAST-006`, `FAST-012` |
| `CDK-DO-015` | MUST | stateful resourceの保持、削除、置換、backup、暗号化propertyを台帳化し、保護欠落をquery可能にする。 | `FAST-006`, `FAST-012` |
| `CDK-DO-016` | MUST | cdk-nag等のsuppressionをrule ID、理由、source位置付きで一覧化する。 | `AUD-008` |
| `CDK-DO-017` | MUST | output/export、SSM、Secrets、cross-account principal等のexternal contract pointをcatalog化する。 | `FAST-006`, `REV-011` |

## 3. 整合性gate

実装と設計、実装と実環境の1対1対応を、人の注意ではなくCIと定期監査で担保する。

| Rule ID | Norm | gate | 合格条件 | Check ID |
|---|---|---|---|---|
| `CDK-DO-018` | MUST | 設計drift検知 | CDKまたは入力設定の変更後に全generatorのcheck modeを実行し、未再生成fileがあれば差分pathを出して失敗する。 | `FAST-006` |
| `CDK-DO-019` | MUST | template snapshot | 全stackにsynthesized templateのsnapshot testがあり、意図しないlogical ID、resource、property変化を検出する。snapshot更新は差分説明と同じreview単位にする。 | `FAST-012` |
| `CDK-DO-020` | MUST | 破壊的変更判定 | template差分からreplacementとdeletionを機械抽出し、stateful resourceが該当する場合は、明示的な移行・許可宣言なしに失敗する。 | `FAST-012` |
| `CDK-DO-021` | MUST | policy準拠 | cdk-nag等を合成時に実行し、encryption、public access block、least privilege、deletion protection、必須tag違反を失敗させる。suppressionは理由を必須にする。 | `FAST-012`, `AUD-008` |
| `CDK-DO-022` | MUST | deploy前diff | deploy対象環境に対する`cdk diff`または同等のchange setを取得し、CI artifactとして現在HEADへ関連付ける。生logをrepositoryへ複製しない。 | `FAST-012`, `FAST-023` |
| `CDK-DO-023` | MUST | 実環境drift監査 | CloudFormation drift detectionを定期実行し、手作業変更を検出して是正する。個々のPRのblocking gateにはしない。 | periodic IaC audit |
| `CDK-DO-024` | MUST | 直列quality command | format・lint・type・規約→synth→policy→snapshot/assertion→設計check→破壊的変更判定をtask runnerの1 commandへ束ねる。 | `FAST-006`, `FAST-012`, `FAST-023` |
| `CDK-DONT-004` | MUST NOT | snapshotのみの品質判定 | snapshot一致だけをsecurity、data protection、intended behaviorの証拠として扱わない。 | `FAST-012` |
| `CDK-DONT-005` | MUST NOT | PRごとの実環境drift | CloudFormation drift detectionを全PRで実行しない。定期監査または明示risk選択に限定する。 | periodic IaC audit |

CIの標準順序は次のとおりとする。

```text
format / lint / type / convention
  -> cdk synth
  -> policy compliance
  -> snapshot and fine-grained assertions
  -> generated design --check
  -> destructive-change classification
```

## 4. 実装規約

### 4.1 layoutと責務分離

| Rule ID | Norm | 規則 | Check ID |
|---|---|---|---|
| `CDK-DO-025` | MUST | app entrypointは環境設定の読込みとstack instantiationだけを行う。 | `FAST-021` |
| `CDK-DONT-006` | MUST NOT | app entrypointへresource定義、business rule、条件分岐、値の組立てを記述しない。 | `FAST-021` |
| `CDK-DO-026` | MUST | stack classはconstructの組立てと接続だけを行い、stackを読めば構成要素と接続が追跡できるようにする。 | `FAST-021` |
| `CDK-DO-027` | MUST | constructを1責務に分け、入力を型とfield説明を持つproperty typeで受ける。 | `FAST-021` |
| `CDK-DONT-007` | MUST NOT | constructから環境変数を直接読み、または深いcontext pathを暗黙参照しない。 | `FAST-021` |
| `CDK-DO-028` | MUST | `app`、`stacks/`、`constructs/`、`config/`のlayoutを規約checkerで強制する。 | `FAST-021` |

### 4.2 環境設定

| Rule ID | Norm | 規則 | Check ID |
|---|---|---|---|
| `CDK-DO-029` | MUST | dev、stg、prod等の差分値を`config/`配下のmachine-readableかつ型検証済みfileへ集約する。 | `FAST-021`, `FAST-022` |
| `CDK-DONT-008` | MUST NOT | 環境固有値をconstruct、stack、appへ直書きまたは散在させない。 | `FAST-021` |
| `CDK-DO-030` | MUST | account IDとregionを設定正本から注入し、env-agnostic synthを許可する場合は理由を設定に明示する。 | `FAST-012`, `FAST-021` |
| `CDK-DO-031` | MUST | 環境によるresource構成差はstackの有無またはstack compositionへ持ち上げる。 | `FAST-021` |
| `CDK-DONT-009` | MUST NOT | construct内部の環境名ifでresource構成を変えない。 | `FAST-021` |

### 4.3 論理IDとresource保護

| Rule ID | Norm | 規則 | Check ID |
|---|---|---|---|
| `CDK-DO-032` | MUST | construct treeの移動・rename時は、logical ID維持または明示的な移行をsnapshotとtemplate diffで確認する。 | `FAST-012` |
| `CDK-DO-033` | MUST | DB、storage、queue、log等の全stateful resourceへRemovalPolicyを明示し、productionは`RETAIN`を既定にする。 | `FAST-012` |
| `CDK-DONT-010` | MUST NOT | stateful resourceのRemovalPolicyをframework defaultへ委ねない。 | `FAST-012` |
| `CDK-DO-034` | MUST | stateful resourceのreplacementを伴うproperty変更へ移行手順、rollback、承認対象を宣言する。 | `FAST-012` |

### 4.4 IAMと権限

| Rule ID | Norm | 規則 | Check ID |
|---|---|---|---|
| `CDK-DO-035` | MUST | L2の`grant*` methodで表現できる権限はgrantを使用する。 | `FAST-012`, `FAST-021` |
| `CDK-DONT-011` | MUST NOT | grantで表現できるpolicy statementをinlineで手書きしない。 | `FAST-012`, `FAST-021` |
| `CDK-DONT-012` | MUST NOT | 理由付きsuppressionなしにwildcard resourceまたはwildcard actionを使用しない。 | `FAST-012`, `AUD-008` |
| `CDK-DO-036` | MUST | cross-accountまたはexternal principalへの許可をexternal reference catalogへ現れる形で宣言する。 | `FAST-006`, `FAST-012`, `REV-011` |

### 4.5 抽象化levelとescape hatch

| Rule ID | Norm | 規則 | Check ID |
|---|---|---|---|
| `CDK-DO-037` | MUST | L2 constructを既定とし、L1直書きや`addOverride`等へ理由とticket/ADR参照を持つ識別commentを付ける。 | `FAST-021`, `AUD-008` |
| `CDK-DONT-013` | MUST NOT | 理由と参照を持たないescape hatchを使用しない。 | `FAST-021`, `AUD-008` |
| `CDK-DO-038` | MUST | third-party construct追加時にmaintenance状況、transitive dependency、権限要求をRisk-selected checkで確認する。 | `FAST-008`, `FAST-012` |

### 4.6 namingとtag

| Rule ID | Norm | 規則 | Check ID |
|---|---|---|---|
| `CDK-DO-039` | MUST | system、environment、owner、cost allocation等の必須tagをstackまたはAspectで一括付与し、漏れを合成時検査で失敗させる。 | `FAST-012` |
| `CDK-DONT-014` | MUST NOT | 必須tagをresourceごとに手書きしない。 | `FAST-012`, `FAST-021` |
| `CDK-DO-040` | MUST | physical nameの明示指定へ理由を付け、全指定箇所を一覧生成する。 | `FAST-006`, `AUD-008` |
| `CDK-DONT-015` | MUST NOT | 理由なしにphysical nameを固定しない。 | `FAST-012`, `AUD-008` |

### 4.7 定量閾値

閾値は標準文書とmachine-readable設定の両方へ保持し、値の一致を機械検査する。引下げは許可し、引上げはCommit CommentまたはADRへ理由を記録する。

| 指標 | 標準値 |
|---|---:|
| 1 stackあたりCloudFormation resource数 | 200 |
| construct 1 classのlogical line | 150 |
| stack classのlogical line | 200 |
| property typeのfield数 | 10 |
| control nest深さ | 2 |
| escape hatch箇所数 / stack | 5 |

| Rule ID | Norm | 規則 | Check ID |
|---|---|---|---|
| `CDK-DO-041` | MUST | 採用した閾値をmachine-readable設定へ保存し、標準値との一致を検査する。 | `FAST-022` |
| `CDK-DONT-016` | MUST NOT | 理由記録なしに標準閾値を引き上げない。 | `FAST-022` |

## 5. 規約の機械化

基底標準と同じMUST / SHOULD語彙、曖昧語禁止、Rule ID、check mapping、suppression inventoryを適用する。CDK固有Rule IDは`CDK-DO-NNN`または`CDK-DONT-NNN`とする。

| Rule ID | Norm | 規則 | Check ID |
|---|---|---|---|
| `CDK-DO-042` | MUST | cdk-nag等の既存ruleで表現できる規則を既存rule setへ委譲する。 | `FAST-022` |
| `CDK-DO-043` | MUST | 採用rule set、自作checker、標準Rule IDのmappingをmachine-readableに保持し、片落ちを検出する。 | `FAST-022` |
| `CDK-DO-044` | MUST | 規約検査をAspect等でsynth pipelineへ組み込み、「synthが成功すること」とblocking policy準拠を接続する。 | `FAST-012` |
| `CDK-DO-045` | SHOULD | Aspectで表現できない規則だけをsynthesized template後段のcheckerで検査する。 | `FAST-012` |
| `CDK-DONT-017` | MUST NOT | reviewerの注意だけに依存するsecurity、tag、naming、RemovalPolicy規則を残さない。 | `FAST-012` |
| `CDK-DO-046` | MUST | suppressionへrule IDと理由を付け、一覧生成と月次監査へ接続する。 | `AUD-008` |

## 6. テスト規約

### 6.1 スナップショットtest

| Rule ID | Norm | 規則 | Check ID |
|---|---|---|---|
| `CDK-DO-047` | MUST | 全stackにsynthesized templateのsnapshot testを持つ。 | `FAST-012` |
| `CDK-DO-048` | MUST | snapshot更新時にlogical ID、resource、replacement、permission、network差分の説明をCommit Commentへ記録する。 | `FAST-012`, `REV-002` |
| `CDK-DONT-018` | MUST NOT | snapshot一致だけを品質passにしない。 | `FAST-012` |

### 6.2 個別property assertion

最低限、次をsnapshotと独立にassertする。

- stateful resourceのencryptionが有効である
- storageとDBのpublic accessが遮断される
- `RemovalPolicy` / `DeletionPolicy`が環境別期待値と一致する
- 許可済みsuppressionを除きIAM policyにwildcardがない
- 必須tagが付与される

| Rule ID | Norm | 規則 | Check ID |
|---|---|---|---|
| `CDK-DO-049` | MUST | securityとdata protection propertyをfine-grained assertionで検証する。 | `FAST-012` |
| `CDK-DO-050` | MUST | 全test関数へ前提と期待結果を1文で表すdocstringを付ける。 | `FAST-020` |
| `CDK-DO-051` | MUST | test本文へAAA section commentを置き、1 caseを1 test関数で表す。 | `FAST-020` |
| `CDK-DO-052` | MUST | `config/`正本の全環境でsynth成功と環境固有期待値を検証する。 | `FAST-012` |

### 6.3 deploy検証

| Rule ID | Norm | 規則 | Check ID |
|---|---|---|---|
| `CDK-DO-053` | MUST | 新規stack、IAM、network、custom resource、provisioning order依存変更では実accountへのintegration testをRisk-selectedで選択する。 | `FAST-012` |
| `CDK-DO-054` | MUST | deploy検証結果を外部CI/report基盤へ集約し、repositoryへ生logまたはtest reportを複製しない。 | `FAST-023` |
| `CDK-DO-055` | MUST | 検証用stackを破棄可能にし、検証環境では`RemovalPolicy.DESTROY`と自動cleanupを使用する。 | `FAST-012` |
| `CDK-DONT-019` | MUST NOT | 実AWS accountへのdeploy testを全変更の無条件gateにしない。 | `FAST-012` |

## 7. 開発flow

IaC変更は既存のdirect / assured / regulated profileに従い、独自の承認・計画書制度を追加しない。

| Rule ID | Norm | 規則 | 接続先 |
|---|---|---|---|
| `CDK-DO-056` | MUST | synthへ影響するIaC変更を`assured`とする。comment等、synthへ影響しない変更だけを`direct`にできる。authentication、authorization、PII保管、不可逆なproduction操作は`regulated`とする。 | `right-size-execution` |
| `CDK-DO-057` | MUST | deploy、resource削除、課金影響の大きい作成など、実在するauthority boundaryだけで承認を得る。 | `authorize-autonomous-execution` |
| `CDK-DONT-020` | MUST NOT | synth、test、設計生成、PR作成を、deploy承認の未取得だけを理由に停止しない。 | `authorize-autonomous-execution` |
| `CDK-DO-058` | MUST | format/lint/type、synth、policy、test、設計再生成、破壊的変更判定を品質commandとして実行する。 | `FAST-006`, `FAST-012` |
| `CDK-DO-059` | MUST | 変更内容、template差分要約、破壊的変更の有無、残存riskをCommit Commentへ、selected checkをreview YAMLへ記録する。`cdk diff`生logは外部CIへ残す。 | `REV-002`, `REV-007`, `FAST-023` |
| `CDK-DO-060` | MUST | 再開用一時memoを`.devflow/run/`へ置き、長期判断をADRへ収束させる。 | `chat-first-development` |
| `CDK-DONT-021` | MUST NOT | directまたはassured変更へ恒久work item、独自計画書、独自phase gateを要求しない。 | `chat-first-development` |

## 8. 導入時の受入基準

- [ ] 全as-built設計が`docs/design/generated/cdk/`配下にあり、同じ現在状態を複製する手書き構成図・resource表が存在しない
- [ ] 全generatorがgenerate modeとcheck modeを同じlogicで提供し、CIでcheck modeを実行する
- [ ] CDK sourceだけを変更して設計書を再生成しない場合にCIが失敗し、差分pathを表示する
- [ ] 全stackにsnapshot testがあり、更新はtemplate差分説明と同じreview単位で行う
- [ ] stateful resourceのreplacement・deletionを機械検出し、移行・許可宣言なしに通さない
- [ ] encryption、public access block、least privilege、deletion protection、必須tagを合成時に検査する
- [ ] suppression、escape hatch、physical name指定を理由付きで一覧生成する
- [ ] 環境差分を`config/`正本へ集約し、全環境の差分表とsynth testを持つ
- [ ] CloudFormation drift detectionを定期監査として定義し、全PRの無条件gateにしない
- [ ] deploy等のauthority boundaryだけに承認を結び付け、synth・test・設計生成・PR作成へ独自承認を追加しない

## 9. check選択

導入先で本標準を採用または変更する場合、少なくとも次を選択する。CDK固有checkerの詳細は導入先catalogへ追加してよいが、既存checkと意味を重複させない。

| Change | Check | Class | 選択条件 |
|---|---|---|---|
| CDK source、context、環境設定、stack構成 | `IMP-009` | Risk-selected | `iac_change: true` |
| synth、snapshot、replacement、IAM、network、policy | `FAST-012` | Risk-selected | `iac_change: true` |
| generated CDK designまたは入力 | `FAST-006` | Invariant | `generated_change: true` |
| layout、config、escape hatch規約 | `FAST-021` | Advisory | `as_built_adoption: true` |
| 定量閾値またはchecker delegation | `FAST-022` | Risk-selected | `quality_threshold_change: true` |
| CI artifact、`cdk diff`、deploy test evidence | `FAST-023` | Advisory | `as_built_adoption: true` |
| suppression inventory | `AUD-008` | Periodic | `monthly_cycle: true` |
| external contract変更 | `REV-011` | Risk-selected | `public_contract_change: true` |

本標準の追加時点では、未実装のCDK generatorやcheckerを実装済みとは扱わない。導入先は受入基準に必要なtoolingとtestを実装し、証拠を得たcheckだけをpassとして記録する。
