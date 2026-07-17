# 要件定義

## 概要

対話の一時理解と永続仕様を分離し、正本からdocs・設計・検査証跡を再生成できるportable development frameworkを提供する。

## ステークホルダー

| 役割 | 関心事 | 承認責任 |
|---|---|---|
| requester | 3本柱の意味と永続境界 | 初回方針決定 |
| product stakeholder | 心地よい対話から意図を要件化 | 要件内容の決定 |
| developer/agent | 推測せず実装・テストできる設計 | なし |
| reviewer | versioned standardと直接証拠による判定 | なし |

## 機能要件

| ID | 要件 | 優先度 | 受入基準 |
|---|---|---|---|
| REQ-001 | `work/`を会話断片・delta・工程証跡に限定し、永続仕様の正本にしない | Must | root instructionsとflowで境界を明記 |
| REQ-002 | 永続要件を`spec/requirements/requirements.json`で管理する | Must | schema/validator/self-hosted catalogが存在 |
| REQ-003 | 各要件をsubject/action/objectからなる単一義務として構造化する | Must | 複合action、重複ID、欠落fieldをvalidatorが拒否 |
| REQ-004 | add/update/retireをbase revisionとitem revisionで競合検出し、temp+replaceで適用する | Must | success/conflict/retire testsが成功 |
| REQ-005 | active/retired要件、受入条件、traceをMarkdownへ自動生成し、手編集driftをcheckする | Must | generate/check testsが成功 |
| REQ-006 | 対話は傾聴、意味保存、発散・収束を研究根拠付きで要件deltaへ変換する | Must | Skill workflow/research mapに規則あり |
| REQ-007 | FastAPIはrouter.pyを処理フロー、functions.pyを具体処理とし、routerのflowからsequenceを生成する | Must | AST fixtureからsequence生成、違反を検出 |
| REQ-008 | FastAPI OpenAPIからAPI一覧とrequest/response IFを生成する | Must | OpenAPI fixtureのoperation/schemaがdocsに出る |
| REQ-009 | raw SQLをSQL ASTで解析し、CRUD matrixとquery objectsを生成する | Must | SQLGlot fixtureでread/write tableを識別 |
| REQ-010 | CDK synth後のCloudFormation YAMLからresource一覧とparameter詳細を生成する | Must | CFN fixtureのResources/Parametersがdocsに出る |
| REQ-011 | 全派生設計に生成元path/digestを記録し、`--check`で1対1対応とdriftを検査する | Must | manifest/digest tamper testが失敗を検出 |
| REQ-012 | SWEBOKとAWS/Azure/Google Cloud/OCI公式best practicesをversioned registryで管理する | Must | official URL、版、checked_at、refresh期限あり |
| REQ-013 | 適用checkを要件・設計・実装へtraceし、Passに直接証拠、N/Aに理由、Failにissueを要求する | Must | standards Skillとexisting gate contractが一致 |
| REQ-014 | Skills/profileをcopy後、利用者は自然言語だけで3本柱のflowを開始できる | Must | install testとREADME guidanceが成功 |

## 非機能要件

| ID | 品質特性 | 測定方法 | 合格閾値 |
|---|---|---|---|
| NFR-001 | 決定性 | 同一入力2回のbytes比較 | 完全一致 |
| NFR-002 | 原子性 | invalid/compound/concurrent delta tests | 部分更新なし |
| NFR-003 | 移植性 | temp repository install/generate | root外依存なし |
| NFR-004 | 鮮度 | registry freshness check | 期限超過sourceがCI失敗 |
| NFR-005 | 説明可能性 | generated docs/review evidence | source/digest/requirement/check IDを追跡可能 |

## データ・法令・倫理要件

秘密・個人情報・production dataを正本や生成docsへ入れない。`retire`は履歴保持のため物理削除ではなくtombstoneにする。

## リスクとトレードオフ

実装からdocsを生成すると実装誤りも文書化され得るため、正本要件とのtraceとstandard reviewを別gateとして維持する。

## 対象外・N/A判断

framework固有詳細はFastAPIとAWS CDKのみ。Azure/GCP/OCIはstandard verification profileの参照台帳まで。
