// 永続要件の一次言語。JSONとMarkdownはこの仕様から生成する。
module requirements {
  type AcceptanceCriterion = { id: str, given: str, when_: str, expected: str }
  type Verification = { method: str, evidence: str }
  type Traces = { design: List[str], implementation: List[str], tests: List[str], standards: List[str] }
  type Requirement = {
    id: str,
    revision: int,
    status: str,
    kind: str,
    title: str,
    subject: str,
    actionName: str,
    objectName: str,
    rationale: str,
    sourceRefs: List[str],
    acceptanceCriteria: List[AcceptanceCriterion],
    verification: Verification,
    traces: Traces,
    lastChangedBy: str,
    retirementReason: str,
    supersededBy: str,
    scopeName: str,
    categoryName: str,
  }
  type Catalog = {
    schemaVersion: int,
    catalogRevision: int,
    product: str,
    updatedAt: str,
    requirements: List[Requirement],
  }
  type RequirementOperation = {
    kind: str,
    id: str,
    expectedRevision: int,
    replacement: Requirement,
  }
  type BatchFold = {
    requirements: List[Requirement],
    touchedIds: List[str],
    valid: bool,
  }
  // add / update / trace update / retireの版遷移を、実Catalog遷移へのrefinementとして検査する。
  type Lifecycle = {
    catalogRevision: int,
    itemRevision: int,
    itemPresent: bool,
    itemStatus: str,
    traceRevision: int,
    priorCatalogRevision: int,
    priorItemRevision: int,
    priorItemPresent: bool,
    priorItemStatus: str,
    priorTraceRevision: int,
    lastOperation: str,
  }

  pure val requirementsSource: Catalog = {
    schemaVersion: 1,
    catalogRevision: 17,
    product: "dev-standard",
    updatedAt: "2026-09-06",
    requirements: [
      {
        id: "REQ-ASBUILT-001",
        revision: 1,
        status: "active",
        kind: "quality",
        title: "as-built生成の決定論性",
        subject: "as-built設計generator",
        actionName: "generate",
        objectName: "同一入力からバイト一致する設計出力",
        rationale: "差分によるdrift検知には非決定要素を除いた再現可能な出力が必要である。",
        sourceRefs: ["user:2026-07-21", "docs/standards/AS-BUILT-DESIGN.md"],
        acceptanceCriteria: [
          { id: "AC-ASBUILT-001-1", given: "同一revisionの宣言済み一次情報がある", when_: "generatorを複数回実行する", expected: "列挙順が固定され、時刻・乱数・環境依存pathを含まないバイト一致出力になる" }
        ],
        verification: { method: "自動テスト", evidence: "同一fixtureを複数回生成したbyte比較" },
        traces: {
          design: ["docs/standards/AS-BUILT-DESIGN.md"],
          implementation: ["governance/checks/catalog.yaml", ".agents/skills/generate-implementation-design/scripts/designflow.py"],
          tests: ["tests/test_review_contract.py", "tests/test_designflow.py"],
          standards: ["DEVSTD-AS-BUILT"],
        },
        lastChangedBy: "CHG-20260721-as-built-design",
        retirementReason: "",
        supersededBy: "",
        scopeName: "",
        categoryName: "",
      },
      {
        id: "REQ-ASBUILT-002",
        revision: 1,
        status: "active",
        kind: "quality",
        title: "generateとcheckの二相契約",
        subject: "as-built設計generator",
        actionName: "provide",
        objectName: "一つの生成logicを共有するgenerate modeとcheck mode",
        rationale: "生成と検査を別実装にすると両者の意味が乖離する。",
        sourceRefs: ["user:2026-07-21", "docs/standards/AS-BUILT-DESIGN.md"],
        acceptanceCriteria: [
          { id: "AC-ASBUILT-002-1", given: "宣言済み生成対象と既存生成物がある", when_: "check modeを実行する", expected: "生成logicを再利用して既存生成物と比較し、差分pathを列挙して非0終了する" }
        ],
        verification: { method: "自動テスト", evidence: "write modeとcheck modeの同一出力およびdrift終了code" },
        traces: {
          design: ["docs/standards/AS-BUILT-DESIGN.md"],
          implementation: ["governance/checks/catalog.yaml", ".agents/skills/generate-implementation-design/scripts/designflow.py"],
          tests: ["tests/test_review_contract.py", "tests/test_designflow.py"],
          standards: ["DEVSTD-AS-BUILT"],
        },
        lastChangedBy: "CHG-20260721-as-built-design",
        retirementReason: "",
        supersededBy: "",
        scopeName: "",
        categoryName: "",
      },
      {
        id: "REQ-ASBUILT-003",
        revision: 1,
        status: "active",
        kind: "constraint",
        title: "生成設計の隔離と識別",
        subject: "as-built生成物",
        actionName: "separate",
        objectName: "docs/design/generated/配下の直接編集禁止banner付き.gen.md設計",
        rationale: "専用path、命名、更新commandにより手書き設計との混在と直接編集を防げる。",
        sourceRefs: ["user:2026-07-21", "docs/standards/AS-BUILT-DESIGN.md"],
        acceptanceCriteria: [
          { id: "AC-ASBUILT-003-1", given: "Markdown形式のas-built設計を生成する", when_: "生成物の配置と先頭行を検査する", expected: "docs/design/generated/配下の.gen.mdでありgenerate/check commandを含む直接編集禁止bannerがあり、同じ現在状態の手書き設計が存在しない" }
        ],
        verification: { method: "repository検査", evidence: "生成path、file名、banner、重複設計scan" },
        traces: {
          design: ["docs/standards/AS-BUILT-DESIGN.md"],
          implementation: [".agents/skills/generate-implementation-design/SKILL.md", "governance/checks/catalog.yaml", ".agents/skills/generate-implementation-design/scripts/designflow.py"],
          tests: ["tests/test_review_contract.py", "tests/test_designflow.py"],
          standards: ["DEVSTD-AS-BUILT"],
        },
        lastChangedBy: "CHG-20260721-as-built-design",
        retirementReason: "",
        supersededBy: "",
        scopeName: "",
        categoryName: "",
      },
      {
        id: "REQ-ASBUILT-004",
        revision: 2,
        status: "active",
        kind: "functional",
        title: "API詳細設計の導出",
        subject: "as-built設計generator",
        actionName: "derive",
        objectName: "handler ASTとOpenAPIとsampleとSQLから得たAPI詳細設計",
        rationale: "APIのinterfaceと実行flowを同じ一次情報から導出すると実装との1対1対応を維持できる。",
        sourceRefs: ["user:2026-07-21", "docs/standards/AS-BUILT-DESIGN.md"],
        acceptanceCriteria: [
          { id: "AC-ASBUILT-004-1", given: "handler、framework OpenAPI、sample定数、生SQLがある", when_: "API設計を生成する", expected: "interface、sequence、全branchを保つcontrol-flow graph、処理step、error分岐、message、unit-test観点をhandler起点で生成する" }
        ],
        verification: { method: "自動テスト", evidence: "API fixtureからの生成内容assert" },
        traces: {
          design: ["docs/standards/AS-BUILT-DESIGN.md"],
          implementation: [".agents/skills/generate-implementation-design/SKILL.md", "governance/checks/catalog.yaml", ".agents/skills/generate-implementation-design/scripts/designflow.py"],
          tests: ["tests/test_review_contract.py", "tests/test_designflow.py"],
          standards: ["DEVSTD-AS-BUILT"],
        },
        lastChangedBy: "CHG-20260829-review-remediation",
        retirementReason: "",
        supersededBy: "",
        scopeName: "",
        categoryName: "",
      },
      {
        id: "REQ-ASBUILT-005",
        revision: 1,
        status: "active",
        kind: "functional",
        title: "API一覧の導出",
        subject: "as-built設計generator",
        actionName: "derive",
        objectName: "handler metadataから得た重複のないAPI一覧",
        rationale: "route metadataを正本にすると別管理のAPI台帳を不要にできる。",
        sourceRefs: ["user:2026-07-21", "docs/standards/AS-BUILT-DESIGN.md"],
        acceptanceCriteria: [
          { id: "AC-ASBUILT-005-1", given: "handler decoratorに設計metadataがある", when_: "API一覧を生成する", expected: "operation、API番号、権限、業務概要を重複なく列挙する" }
        ],
        verification: { method: "自動テスト", evidence: "metadata fixtureからのAPI一覧assert" },
        traces: {
          design: ["docs/standards/AS-BUILT-DESIGN.md"],
          implementation: [".agents/skills/generate-implementation-design/SKILL.md", "governance/checks/catalog.yaml", ".agents/skills/generate-implementation-design/scripts/designflow.py"],
          tests: ["tests/test_review_contract.py", "tests/test_designflow.py"],
          standards: ["DEVSTD-AS-BUILT"],
        },
        lastChangedBy: "CHG-20260721-as-built-design",
        retirementReason: "",
        supersededBy: "",
        scopeName: "",
        categoryName: "",
      },
      {
        id: "REQ-ASBUILT-006",
        revision: 2,
        status: "active",
        kind: "data",
        title: "CRUD関係の導出",
        subject: "as-built設計generator",
        actionName: "derive",
        objectName: "SQLと外部client呼出から得たtableおよび外部連携先のCRUD関係",
        rationale: "静的解析されたデータ操作をAPIへ接続するとCRUD図を手書きせず維持できる。",
        sourceRefs: ["user:2026-07-21", "docs/standards/AS-BUILT-DESIGN.md"],
        acceptanceCriteria: [
          { id: "AC-ASBUILT-006-1", given: "operationからSQLへの明示mappingと外部client呼出がある", when_: "CRUD設計を生成する", expected: "明示mappingだけからSELECTをR、INSERTをC、UPDATEをU、DELETEをDとしてtable×APIと外部連携先×APIを生成し、未mapping SQL、parse不能SQLおよびsupport外のMERGEを黙って推定せずstructured unsupportedとして扱う" }
        ],
        verification: { method: "自動テスト", evidence: "SQLおよびclient fixtureからのCRUD matrix assert" },
        traces: {
          design: ["docs/standards/AS-BUILT-DESIGN.md"],
          implementation: [".agents/skills/generate-implementation-design/SKILL.md", "governance/checks/catalog.yaml", ".agents/skills/generate-implementation-design/scripts/designflow.py"],
          tests: ["tests/test_review_contract.py", "tests/test_designflow.py"],
          standards: ["DEVSTD-AS-BUILT"],
        },
        lastChangedBy: "CHG-20260829-review-remediation",
        retirementReason: "",
        supersededBy: "",
        scopeName: "",
        categoryName: "",
      },
      {
        id: "REQ-ASBUILT-007",
        revision: 3,
        status: "active",
        kind: "data",
        title: "DB設計の導出",
        subject: "as-built設計generator",
        actionName: "derive",
        objectName: "正本DDLとSQLから得たtable定義とER関係と書込みAPI",
        rationale: "DDLとSQLを一次情報にするとDB設計の二重管理を避けられる。",
        sourceRefs: ["user:2026-07-21", "docs/standards/AS-BUILT-DESIGN.md"],
        acceptanceCriteria: [
          { id: "AC-ASBUILT-007-1", given: "repository内に正本DDLとendpoint別SQLがある", when_: "DB設計を生成する", expected: "table、column、constraint、column単位のforeign-key source/targetを含むER関係をDDLから生成し、columnへの書込みAPIをSQL解析から導出する" }
        ],
        verification: { method: "自動テスト", evidence: "DDLおよびSQL fixtureからのDB設計assert" },
        traces: {
          design: ["docs/standards/AS-BUILT-DESIGN.md"],
          implementation: ["governance/checks/catalog.yaml", ".agents/skills/generate-implementation-design/scripts/designflow.py"],
          tests: ["tests/test_review_contract.py", "tests/test_designflow.py"],
          standards: ["DEVSTD-AS-BUILT"],
        },
        lastChangedBy: "CHG-20260829-review-remediation",
        retirementReason: "",
        supersededBy: "",
        scopeName: "",
        categoryName: "",
      },
      {
        id: "REQ-ASBUILT-008",
        revision: 2,
        status: "active",
        kind: "functional",
        title: "E2E scenario設計の導出",
        subject: "as-built設計generator",
        actionName: "derive",
        objectName: "E2E testのGiven When Then構造から得たscenario設計",
        rationale: "test codeをscenarioの正本にすると実行可能な仕様と設計表示を一致させられる。",
        sourceRefs: ["user:2026-07-21", "docs/standards/AS-BUILT-DESIGN.md"],
        acceptanceCriteria: [
          { id: "AC-ASBUILT-008-1", given: "E2E testにGiven、When、Then sectionがある", when_: "scenario設計を生成する", expected: "前提、操作、期待状態をtest codeから順序どおり生成する" }
        ],
        verification: { method: "自動テスト", evidence: "E2E fixtureからのscenario出力assert" },
        traces: {
          design: ["docs/standards/AS-BUILT-DESIGN.md"],
          implementation: ["governance/checks/catalog.yaml", ".agents/skills/generate-implementation-design/scripts/designflow.py"],
          tests: ["tests/test_review_contract.py", "tests/test_designflow.py"],
          standards: ["DEVSTD-AS-BUILT"],
        },
        lastChangedBy: "CHG-20260802-skills-audit-remediation",
        retirementReason: "",
        supersededBy: "",
        scopeName: "",
        categoryName: "",
      },
      {
        id: "REQ-ASBUILT-009",
        revision: 4,
        status: "active",
        kind: "operational",
        title: "test evidence viewの対象所有集約",
        subject: "as-built設計generator",
        actionName: "derive",
        objectName: "対象repositoryが所有する結果JSONから得た参照限定test evidence view",
        rationale: "結果本文を複製せず、localまたは導入先が既に所有し選択したviewだけを使えばportable runtimeへ外部report基盤を強制しない。",
        sourceRefs: ["user:2026-07-21", "user:2026-08-27", "docs/standards/AS-BUILT-DESIGN.md"],
        acceptanceCriteria: [
          { id: "AC-ASBUILT-009-1", given: "対象repositoryが所有するtest結果JSONがある", when_: "test evidence viewを生成する", expected: "status、API response、DB結果、mock受信結果への参照だけを整形し、結果本文を保存せず、新しい外部report基盤を要求しない" }
        ],
        verification: { method: "契約テスト", evidence: "report fixtureとrepository非保存規則のassert" },
        traces: {
          design: ["docs/standards/AS-BUILT-DESIGN.md"],
          implementation: ["governance/checks/catalog.yaml", ".agents/skills/generate-implementation-design/scripts/designflow.py"],
          tests: ["tests/test_review_contract.py", "tests/test_designflow.py"],
          standards: ["DEVSTD-AS-BUILT"],
        },
        lastChangedBy: "CHG-20260827-quint-three-pillar-guardrails",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "nonfunctional",
      },
      {
        id: "REQ-ASBUILT-010",
        revision: 2,
        status: "active",
        kind: "functional",
        title: "generator tool設計の導出",
        subject: "as-built設計generator",
        actionName: "derive",
        objectName: "tool entrypoint ASTとdocstringから得たCLI仕様とflow",
        rationale: "generator自身を同じ方式で可視化すると抽出可能性をdogfoodingできる。",
        sourceRefs: ["user:2026-07-21", "docs/standards/AS-BUILT-DESIGN.md"],
        acceptanceCriteria: [
          { id: "AC-ASBUILT-010-1", given: "tool entrypointと呼出先関数にdocstringがある", when_: "tool設計を生成する", expected: "CLI argument、制御flow、関数責務をASTとdocstring先頭1行から生成する" }
        ],
        verification: { method: "自動テスト", evidence: "tool fixtureからのCLIおよびflow assert" },
        traces: {
          design: ["docs/standards/AS-BUILT-DESIGN.md"],
          implementation: ["governance/checks/catalog.yaml", ".agents/skills/generate-implementation-design/scripts/designflow.py"],
          tests: ["tests/test_review_contract.py", "tests/test_designflow.py"],
          standards: ["DEVSTD-AS-BUILT"],
        },
        lastChangedBy: "CHG-20260802-skills-audit-remediation",
        retirementReason: "",
        supersededBy: "",
        scopeName: "",
        categoryName: "",
      },
      {
        id: "REQ-ASBUILT-011",
        revision: 3,
        status: "active",
        kind: "data",
        title: "error case定義の生成",
        subject: "as-built設計generator",
        actionName: "generate",
        objectName: "API error分岐から得たcatalog全体で一意なID付きmachine-readable error case",
        rationale: "error分岐を機械可読にするとE2Eとの1対1 coverageを検査できる。",
        sourceRefs: ["user:2026-07-21", "docs/standards/AS-BUILT-DESIGN.md"],
        acceptanceCriteria: [
          { id: "AC-ASBUILT-011-1", given: "API handlerに正規化されたerror分岐がある", when_: "API設計を生成する", expected: "各error分岐へ安定IDを付けたmachine-readable定義を出力し、error IDの重複をoperation内だけでなく生成catalog全体で拒否する" }
        ],
        verification: { method: "自動テスト", evidence: "error branch fixtureからのcase ID出力assert" },
        traces: {
          design: ["docs/standards/AS-BUILT-DESIGN.md"],
          implementation: ["governance/checks/catalog.yaml", ".agents/skills/generate-implementation-design/scripts/designflow.py"],
          tests: ["tests/test_review_contract.py", "tests/test_designflow.py"],
          standards: ["DEVSTD-AS-BUILT"],
        },
        lastChangedBy: "CHG-20260829-review-remediation",
        retirementReason: "",
        supersededBy: "",
        scopeName: "",
        categoryName: "",
      },
      {
        id: "REQ-ASBUILT-012",
        revision: 2,
        status: "active",
        kind: "quality",
        title: "実装仕様sample三点整合",
        subject: "as-built整合check",
        actionName: "verify",
        objectName: "handler登録と設計metadataとerror sampleの三点整合",
        rationale: "実装、interface情報、設計掲載sampleの片落ちを静的に検出する必要がある。",
        sourceRefs: ["user:2026-07-21", "docs/standards/AS-BUILT-DESIGN.md"],
        acceptanceCriteria: [
          { id: "AC-ASBUILT-012-1", given: "API handler、OpenAPI metadata、error sampleがある", when_: "公開API変更の整合checkを実行する", expected: "handler登録漏れ、metadata欠落、error分岐に対応するsample不足を検出する" }
        ],
        verification: { method: "静的解析", evidence: "不整合fixtureを拒否するcheck結果" },
        traces: {
          design: ["docs/standards/AS-BUILT-DESIGN.md"],
          implementation: ["governance/checks/catalog.yaml", ".agents/skills/verify-against-engineering-standards/references/as-built-design-check-selection.md", ".agents/skills/generate-implementation-design/scripts/qualityflow.py"],
          tests: ["tests/test_review_contract.py", "tests/test_qualityflow.py"],
          standards: ["DEVSTD-AS-BUILT"],
        },
        lastChangedBy: "CHG-20260802-skills-audit-remediation",
        retirementReason: "",
        supersededBy: "",
        scopeName: "",
        categoryName: "",
      },
      {
        id: "REQ-ASBUILT-013",
        revision: 2,
        status: "active",
        kind: "quality",
        title: "sampleとtestの整合",
        subject: "as-built整合check",
        actionName: "verify",
        objectName: "設計掲載sampleと実response assertionの対応",
        rationale: "設計書に掲載する例をtest済みに限定すると表示と振る舞いの乖離を防げる。",
        sourceRefs: ["user:2026-07-21", "docs/standards/AS-BUILT-DESIGN.md"],
        acceptanceCriteria: [
          { id: "AC-ASBUILT-013-1", given: "正常または異常response sampleがある", when_: "sample整合checkを実行する", expected: "各sampleが対応testから参照され、実responseとのassertに使用されていることを検出する" }
        ],
        verification: { method: "AST静的解析", evidence: "未参照sampleと未assert sampleを拒否するcheck結果" },
        traces: {
          design: ["docs/standards/AS-BUILT-DESIGN.md"],
          implementation: ["governance/checks/catalog.yaml", ".agents/skills/verify-against-engineering-standards/references/as-built-design-check-selection.md", ".agents/skills/generate-implementation-design/scripts/qualityflow.py"],
          tests: ["tests/test_review_contract.py", "tests/test_qualityflow.py"],
          standards: ["DEVSTD-AS-BUILT"],
        },
        lastChangedBy: "CHG-20260802-skills-audit-remediation",
        retirementReason: "",
        supersededBy: "",
        scopeName: "",
        categoryName: "",
      },
      {
        id: "REQ-ASBUILT-014",
        revision: 3,
        status: "active",
        kind: "quality",
        title: "CRUDとE2E状態検証の整合",
        subject: "as-built整合check",
        actionName: "verify",
        objectName: "DBまたは外部変更effectを持つAPIとeffect別E2E状態assertの対応",
        rationale: "API responseだけでなく永続状態と外部状態を検証してデータ更新の回帰を検出する必要がある。",
        sourceRefs: ["user:2026-07-21", "user:2026-08-27", "docs/standards/AS-BUILT-DESIGN.md"],
        acceptanceCriteria: [
          { id: "AC-ASBUILT-014-1", given: "CRUD図でDBまたは外部変更effectを持つAPIがある", when_: "CRUD E2E整合checkを実行する", expected: "DB writeはDB状態、external writeは外部状態を個別にassertし、異常系も各effectの状態不変または理由付き許可変化をassertする" }
        ],
        verification: { method: "静的解析とE2E契約テスト", evidence: "状態assert欠落fixtureを拒否するcheck結果" },
        traces: {
          design: ["docs/standards/AS-BUILT-DESIGN.md"],
          implementation: ["governance/checks/catalog.yaml", ".agents/skills/verify-against-engineering-standards/references/as-built-design-check-selection.md", ".agents/skills/generate-implementation-design/scripts/qualityflow.py"],
          tests: ["tests/test_review_contract.py", "tests/test_qualityflow.py"],
          standards: ["DEVSTD-AS-BUILT"],
        },
        lastChangedBy: "CHG-20260827-quint-three-pillar-guardrails",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "nonfunctional",
      },
      {
        id: "REQ-ASBUILT-015",
        revision: 2,
        status: "active",
        kind: "quality",
        title: "解析可能なtest構造",
        subject: "導入先repositoryのtest",
        actionName: "structure",
        objectName: "AAAまたはGWTとdocstringと1 case 1関数を持つtest",
        rationale: "構造化されたtest codeをscenario設計とレビュー観点の一次情報にできる。",
        sourceRefs: ["user:2026-07-21", "docs/standards/AS-BUILT-DESIGN.md"],
        acceptanceCriteria: [
          { id: "AC-ASBUILT-015-1", given: "as-built標準を採用したtest codeがある", when_: "test構造checkを実行する", expected: "unit testのAAA、E2EのGWT、docstring、1 case 1関数を評価し、導入時はAdvisoryとして報告する" }
        ],
        verification: { method: "AST静的解析", evidence: "test構造fixtureとAdvisory結果" },
        traces: {
          design: ["docs/standards/AS-BUILT-DESIGN.md"],
          implementation: ["governance/checks/catalog.yaml", ".agents/skills/verify-against-engineering-standards/references/as-built-design-check-selection.md", ".agents/skills/generate-implementation-design/scripts/qualityflow.py"],
          tests: ["tests/test_review_contract.py", "tests/test_qualityflow.py"],
          standards: ["DEVSTD-AS-BUILT"],
        },
        lastChangedBy: "CHG-20260802-skills-audit-remediation",
        retirementReason: "",
        supersededBy: "",
        scopeName: "",
        categoryName: "",
      },
      {
        id: "REQ-ASBUILT-016",
        revision: 3,
        status: "active",
        kind: "quality",
        title: "unit test coverage目標",
        subject: "導入先repositoryのunit test",
        actionName: "measure",
        objectName: "C0命令網羅95%以上とC1分岐網羅90%以上のcoverage",
        rationale: "高い命令・分岐網羅を測定目標にしつつ、導入直後のfalse blockerを避けて効果を実測する。",
        sourceRefs: ["user:2026-07-21", "docs/standards/AS-BUILT-DESIGN.md"],
        acceptanceCriteria: [
          { id: "AC-ASBUILT-016-1", given: "as-built標準を採用したunit test suiteがある", when_: "coverageを測定する", expected: "C0 95%以上とC1 90%以上をAdvisoryとして評価し、実測に基づく昇格判断まで無条件blockingにしない" }
        ],
        verification: { method: "coverage toolとreview contract", evidence: "C0 C1測定結果への外部CI参照とAdvisory分類" },
        traces: {
          design: ["docs/standards/AS-BUILT-DESIGN.md"],
          implementation: ["governance/checks/catalog.yaml", ".agents/skills/generate-implementation-design/scripts/qualityflow.py"],
          tests: ["tests/test_review_contract.py", "tests/test_qualityflow.py"],
          standards: ["DEVSTD-AS-BUILT"],
        },
        lastChangedBy: "CHG-20260829-review-remediation",
        retirementReason: "",
        supersededBy: "",
        scopeName: "",
        categoryName: "",
      },
      {
        id: "REQ-ASBUILT-017",
        revision: 2,
        status: "active",
        kind: "constraint",
        title: "as-built check定義の単一正本",
        subject: "as-built規約",
        actionName: "maintain",
        objectName: "Rule IDからcatalog check IDへ接続された機械可読check定義",
        rationale: "Markdown tagとcatalogの二重定義を避けるとclass、trigger、enforcementを一か所で変更できる。",
        sourceRefs: ["user:2026-07-21", "docs/standards/AS-BUILT-DESIGN.md"],
        acceptanceCriteria: [
          { id: "AC-ASBUILT-017-1", given: "as-built標準に規範Rule IDがある", when_: "check mappingを検査する", expected: "check ID、class、timing、trigger、acceptance、enforcementがcatalogだけで定義され、標準が対応check IDを参照する" }
        ],
        verification: { method: "repository契約テスト", evidence: "標準Rule IDとcatalog IDの対応assert" },
        traces: {
          design: ["docs/standards/AS-BUILT-DESIGN.md"],
          implementation: ["governance/checks/catalog.yaml", "docs/standards/AS-BUILT-DESIGN.md"],
          tests: ["tests/test_review_contract.py"],
          standards: ["DEVSTD-AS-BUILT"],
        },
        lastChangedBy: "CHG-20260721-as-built-design",
        retirementReason: "",
        supersededBy: "",
        scopeName: "",
        categoryName: "",
      },
      {
        id: "REQ-ASBUILT-018",
        revision: 2,
        status: "active",
        kind: "operational",
        title: "抑制例外の可視化",
        subject: "as-built規約check",
        actionName: "generate",
        objectName: "理由付きRule ID抑制箇所の監査一覧",
        rationale: "例外を一覧化するとsilent suppressionと恒久化した例外を定期監査できる。",
        sourceRefs: ["user:2026-07-21", "docs/standards/AS-BUILT-DESIGN.md"],
        acceptanceCriteria: [
          { id: "AC-ASBUILT-018-1", given: "コードにignore Rule ID commentがある", when_: "抑制一覧を生成してGovernance Auditを実行する", expected: "全抑制path、Rule ID、理由を列挙し、理由欠落、孤児、反復を検出する" }
        ],
        verification: { method: "定期repository audit", evidence: "抑制inventoryとAUD-008結果" },
        traces: {
          design: ["docs/standards/AS-BUILT-DESIGN.md"],
          implementation: ["governance/checks/catalog.yaml", ".agents/skills/generate-implementation-design/scripts/qualityflow.py"],
          tests: ["tests/test_review_contract.py", "tests/test_qualityflow.py"],
          standards: ["DEVSTD-AS-BUILT"],
        },
        lastChangedBy: "CHG-20260802-skills-audit-remediation",
        retirementReason: "",
        supersededBy: "",
        scopeName: "",
        categoryName: "",
      },
      {
        id: "REQ-ASBUILT-019",
        revision: 4,
        status: "active",
        kind: "operational",
        title: "選択品質結果の単一軽量集約",
        subject: "inspect-quality-gates runner",
        actionName: "provide",
        objectName: "選択したtest・static analysis・規約check・coverageの結果と未検証範囲を示す一つのlocal summaryまたは対象所有view",
        rationale: "選択検査の実行runner自体へ結果集約を一本化すれば別report generatorを配布せず、CIを強制せずに証跡範囲と残存riskを追跡できる。",
        sourceRefs: ["user:2026-07-21", "user:2026-08-27", "docs/standards/AS-BUILT-DESIGN.md"],
        acceptanceCriteria: [
          { id: "AC-ASBUILT-019-1", given: "品質checkの集合から変更に関係するcheckを選択してinspect runnerで実行する", when_: "品質結果を報告する", expected: "選択したcheck、covered acceptance、対象scope、未検証範囲、残存risk、plan digestだけを一つのlocal summaryへ集約し、対象repositoryが既に所有するviewが選択された場合だけそこへ提示し、CI固有pathへ直接書かない" }
        ],
        verification: { method: "契約テスト", evidence: "inspect result fixture、repository-confined optional JSON、CI固有writeと別report generatorの不存在" },
        traces: {
          design: ["docs/standards/AS-BUILT-DESIGN.md"],
          implementation: [".agents/skills/inspect-quality-gates/scripts/inspect.py"],
          tests: ["tests/test_inspect_runner.py"],
          standards: ["DEVSTD-AS-BUILT"],
        },
        lastChangedBy: "CHG-20260829-review-remediation",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "nonfunctional",
      },
      {
        id: "REQ-ASBUILT-020",
        revision: 2,
        status: "active",
        kind: "quality",
        title: "適用対象要件・実装artifact・test nodeの追跡完全性",
        subject: "as-built設計generator",
        actionName: "validate",
        objectName: "schema version 2 trace JSONが適用対象として宣言したactive canonical requirement IDからartifactを経てportable pytest static nodeへ至る完全な明示trace",
        rationale: "generatorがsupportするsurfaceへ範囲を限定しつつ、宣言された適用対象集合、artifact metadata、lexical no-follow path、生成TEST_MANIFEST.gen.jsonを相互照合して欠落やaliasを許さない。",
        sourceRefs: ["user:2026-08-27", "docs/standards/AS-BUILT-DESIGN.md"],
        acceptanceCriteria: [
          { id: "AC-ASBUILT-020-1", given: "canonical requirements JSON、schema_version 2と必須applicable_requirement_idsを持つ明示trace JSON、artifact metadata、pytest test sourceがある", when_: "as-built設計とTEST_MANIFEST.gen.jsonを生成する", expected: "applicable_requirement_idsの未知・inactive・duplicate、適用対象の未mapping、対象外要件の余剰mapping、未知artifact、lexical aliasまたはsymlink path、存在しないportable pytest static node、duplicate link、metadataとtraceの片方向不一致を拒否し、宣言集合と完全一致するrequirement→artifact→test node viewと決定的manifestを生成する" }
        ],
        verification: { method: "自動テスト", evidence: "schema v2、applicable集合、lexical no-follow、portable pytest static node、TEST_MANIFEST.gen.jsonのpositive fixtureと各failure mutant" },
        traces: {
          design: ["docs/standards/AS-BUILT-DESIGN.md", ".agents/skills/generate-implementation-design/references/fastapi-contract.md", ".agents/skills/generate-implementation-design/references/cdk-contract.md"],
          implementation: [".agents/skills/generate-implementation-design/scripts/designflow.py"],
          tests: ["tests/test_designflow.py"],
          standards: ["DEVSTD-AS-BUILT"],
        },
        lastChangedBy: "CHG-20260829-review-remediation",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "nonfunctional",
      },
      {
        id: "REQ-ASBUILT-021",
        revision: 1,
        status: "active",
        kind: "quality",
        title: "導入時のas-built Markdown生成完了",
        subject: "Dev標準を導入する開発agent",
        actionName: "verify",
        objectName: "必要な実装領域のgenerator接続、Markdown生成、欠落とdrift検査",
        rationale: "既存generatorだけを起動条件にすると初回導入で生成が省略されるため、接続と生成物の完了確認を2本目の柱に含める。",
        sourceRefs: ["user:2026-09-06"],
        acceptanceCriteria: [
          { id: "AC-ASBUILT-021-1", given: "実装を伴う初回導入または設計に影響する変更がある", when_: "導入完了を判定する", expected: "API・data・infra・frontend等を棚卸しし、必要領域はgeneratorまたはadapterを接続して人向けMarkdownを生成する。実装のない領域だけを理由付きで非該当とし、未接続・未対応の必要領域を完了扱いにしない" },
          { id: "AC-ASBUILT-021-2", given: "導入先所有の生成契約と実装がある", when_: "通常の検証入口で設計検査を実行する", expected: "契約欠落・未分類・未完了・必要なMarkdown欠落/空・drift・checkによる書換えを非0終了で拒否する。CIは導入先運用に従い、CIがなくてもローカルで検証する" },
          { id: "AC-ASBUILT-021-3", given: "作業を再開または完了報告する", when_: "設計生成の証拠を確認する", expected: "実際の生成Markdown、対象revision、実行commandと結果、残存領域を確認する。install receiptや過去会話の完了報告を生成の証拠に代用しない" }
        ],
        verification: { method: "回帰テストと導入検査", evidence: "生成契約の未設定・Markdown欠落・drift・check書換え・正常例の実行結果とhost別配布検査" },
        traces: {
          design: [".agents/skills/generate-implementation-design/references/adoption.md"],
          implementation: [".agents/skills/generate-implementation-design/scripts/check_design.py", ".agents/skills/chat-first-development/SKILL.md", "distribution/snippets/AGENTS.governance.md"],
          tests: ["tests/test_design_adoption.py", "tests/test_portable_distribution.py"],
          standards: ["DEVSTD-AS-BUILT"],
        },
        lastChangedBy: "CHG-20260906-as-built-adoption",
        retirementReason: "",
        supersededBy: "",
        scopeName: "",
        categoryName: "",
      },
      {
        id: "REQ-DESIGN-007",
        revision: 1,
        status: "active",
        kind: "quality",
        title: "SQLのAPI別正本と型付きquery生成",
        subject: "SQLを使うAPIの導入・実装agent",
        actionName: "verify",
        objectName: "API別SQL正本、DDL/SQL AST由来の型付きquery生成と関連検査",
        rationale: "共通repositoryへのSQL集約や手書き型によってSQL配置・生成契約が省略される再発を防ぐ。",
        sourceRefs: ["user:2026-09-06"],
        acceptanceCriteria: [
          { id: "AC-DESIGN-007-1", given: "SQLを使うAPIを新規作成・再編またはDev標準へ導入する", when_: "実装完了を判定する", expected: "API別sql/NNN_name.sqlを正本としてDDL/SQL ASTから引数・結果行型とgenerated/queries.pyを生成する。functionsがDB port経由で呼び、業務判定とtransactionを管理する" },
          { id: "AC-DESIGN-007-2", given: "API別SQLと生成queryがある", when_: "関係する検査を選ぶ", expected: "SQL lint、配置・直書き・呼出境界、型生成の決定性と欠落/drift、関連DBテスト、query台帳・CRUD・table/ER Markdown生成を検証する。未接続の必要な検査を完了扱いにしない" },
          { id: "AC-DESIGN-007-3", given: "既存SQL配置を修正する", when_: "SQLを移す", expected: "parameter binding、NULL/行数/戻り型、transaction/rollbackと適用済みmigration本文・checksumを維持する。SQLを使わない実装にはSQL層を要求しない" }
        ],
        verification: { method: "回帰テストと導入検査・差分レビュー", evidence: "SQL配置・直書きSQL・生成物欠落・英語説明・日本語説明・機械用指示の検査結果と導入先の生成差分・型検査・DBテスト" },
        traces: {
          design: [".agents/skills/generate-implementation-design/references/sql-and-language.md"],
          implementation: [".agents/skills/generate-implementation-design/scripts/qualityflow.py", ".agents/skills/chat-first-development/SKILL.md", ".agents/skills/inspect-quality-gates/SKILL.md"],
          tests: ["tests/test_source_conventions.py"],
          standards: ["DEVSTD-AS-BUILT"],
        },
        lastChangedBy: "CHG-20260906-sql-japanese-comments",
        retirementReason: "",
        supersededBy: "",
        scopeName: "",
        categoryName: "",
      },
      {
        id: "REQ-DOCS-002",
        revision: 1,
        status: "active",
        kind: "quality",
        title: "説明コメントと生成ヘッダーの日本語",
        subject: "導入・実装agent",
        actionName: "verify",
        objectName: "利用者指定に従う日本語の説明コメントとdocstringと生成ヘッダー",
        rationale: "コメントの存在検査だけでは英語を検出できず、生成元が英語なら再生成で戻るため、言語指定と生成元修正を完了条件に含める。",
        sourceRefs: ["user:2026-09-06"],
        acceptanceCriteria: [
          { id: "AC-DOCS-002-1", given: "説明コメント・docstring・SQL説明・生成コードの説明を新規作成または変更する", when_: "説明言語を選ぶ", expected: "別言語の明示指示がなければ日本語にする。識別子・固有名詞・機械用指示・ライセンス原文・実行時文字列を誤って翻訳しない" },
          { id: "AC-DOCS-002-2", given: "生成物の説明が英語である", when_: "修正する", expected: "generator/templateを修正して再生成し、生成物を手修正したり生成directory全体を言語検査から除外したりしない" },
          { id: "AC-DOCS-002-3", given: "言語検査を実行する", when_: "完了を報告する", expected: "対象とcommandと結果を示す。Python/SQLの英語のみの説明は非0終了で検出し、日本語文字の存在を意味の品質保証に代用しない。他言語は対応parser/linterまたは差分レビューで補完する" }
        ],
        verification: { method: "回帰テストと導入検査・差分レビュー", evidence: "SQL配置・直書きSQL・生成物欠落・英語説明・日本語説明・機械用指示の検査結果と導入先の生成差分・型検査・DBテスト" },
        traces: {
          design: [".agents/skills/generate-implementation-design/references/sql-and-language.md"],
          implementation: [".agents/skills/generate-implementation-design/scripts/qualityflow.py", ".agents/skills/chat-first-development/SKILL.md", ".agents/skills/inspect-quality-gates/SKILL.md"],
          tests: ["tests/test_source_conventions.py"],
          standards: ["DEVSTD-AS-BUILT"],
        },
        lastChangedBy: "CHG-20260906-sql-japanese-comments",
        retirementReason: "",
        supersededBy: "",
        scopeName: "",
        categoryName: "",
      },
      {
        id: "REQ-DESIGN-001",
        revision: 3,
        status: "active",
        kind: "constraint",
        title: "FastAPI operation構成",
        subject: "FastAPI実装フレーム",
        actionName: "structure",
        objectName: "router.pyのオーケストレーションとfunctions.pyの具体処理に分けたoperation",
        rationale: "安定したoperation境界により、処理フローの導出と詳細設計の決定的な検査ができる。",
        sourceRefs: ["user:2026-07-17"],
        acceptanceCriteria: [
          { id: "AC-DESIGN-001-1", given: "FastAPI operationを実装している", when_: "ソース構成を検査する", expected: "router.pyが処理の流れを公開し、functions.pyが具体処理を持つ" }
        ],
        verification: { method: "自動テスト", evidence: "routerのAST契約テスト" },
        traces: {
          design: [".agents/skills/generate-implementation-design/references/fastapi-contract.md"],
          implementation: [".agents/skills/generate-implementation-design/SKILL.md"],
          tests: ["tests/test_designflow.py"],
          standards: ["SWEBOK-V4A"],
        },
        lastChangedBy: "WI-20260718-checklist-japanese-docs",
        retirementReason: "",
        supersededBy: "",
        scopeName: "",
        categoryName: "",
      },
      {
        id: "REQ-DESIGN-002",
        revision: 2,
        status: "active",
        kind: "functional",
        title: "routerからのシーケンス図導出",
        subject: "設計生成器",
        actionName: "derive",
        objectName: "FastAPI routerの構文木から得たoperationシーケンス図",
        rationale: "実装から導出したフロー文書はソースとの整合を維持できる。",
        sourceRefs: ["user:2026-07-17"],
        acceptanceCriteria: [
          { id: "AC-DESIGN-002-1", given: "router.pyに有効なroute関数がある", when_: "FastAPI設計生成器を実行する", expected: "生成Mermaidが実行時の呼出順を保ち、decoratorを除外する" }
        ],
        verification: { method: "自動テスト", evidence: "シーケンス出力のアサーション" },
        traces: {
          design: [".agents/skills/generate-implementation-design/references/fastapi-contract.md"],
          implementation: [".agents/skills/generate-implementation-design/scripts/designflow.py"],
          tests: ["tests/test_designflow.py"],
          standards: ["SWEBOK-V4A"],
        },
        lastChangedBy: "WI-20260718-checklist-japanese-docs",
        retirementReason: "",
        supersededBy: "",
        scopeName: "",
        categoryName: "",
      },
      {
        id: "REQ-DESIGN-003",
        revision: 2,
        status: "active",
        kind: "interface",
        title: "OpenAPIからのインターフェース設計導出",
        subject: "設計生成器",
        actionName: "derive",
        objectName: "OpenAPI文書からのAPIとインターフェースの一覧",
        rationale: "OpenAPIを実行可能なIF正本とすることで、手作業カタログの重複を避ける。",
        sourceRefs: ["user:2026-07-17", "OpenAPI Specification 3.1.1", "FastAPI OpenAPI documentation"],
        acceptanceCriteria: [
          { id: "AC-DESIGN-003-1", given: "アプリケーションが生成したOpenAPI文書がある", when_: "FastAPI設計生成器を実行する", expected: "operation IDを重複させずにAPI、request、response、schema文書を生成する" }
        ],
        verification: { method: "自動テスト", evidence: "OpenAPI fixtureの出力アサーション" },
        traces: {
          design: [".agents/skills/generate-implementation-design/references/fastapi-contract.md"],
          implementation: [".agents/skills/generate-implementation-design/scripts/designflow.py"],
          tests: ["tests/test_designflow.py"],
          standards: ["SWEBOK-V4A"],
        },
        lastChangedBy: "WI-20260718-checklist-japanese-docs",
        retirementReason: "",
        supersededBy: "",
        scopeName: "",
        categoryName: "",
      },
      {
        id: "REQ-DESIGN-004",
        revision: 2,
        status: "active",
        kind: "data",
        title: "SQLからのデータ設計導出",
        subject: "設計生成器",
        actionName: "parse",
        objectName: "生SQLからのquery objectとCRUD文書",
        rationale: "AST解析は構造的な証跡を作り、無効なSQLを推測せず拒否する。",
        sourceRefs: ["user:2026-07-17", "SQLGlot documentation"],
        acceptanceCriteria: [
          { id: "AC-DESIGN-004-1", given: "実行可能な生SQLファイルがある", when_: "FastAPI設計生成器を実行する", expected: "SQL構文木からquery objectとtable CRUD関係を生成する" }
        ],
        verification: { method: "自動テスト", evidence: "SQL AST fixtureとCRUD出力のアサーション" },
        traces: {
          design: [".agents/skills/generate-implementation-design/references/fastapi-contract.md"],
          implementation: [".agents/skills/generate-implementation-design/scripts/designflow.py"],
          tests: ["tests/test_designflow.py"],
          standards: ["SWEBOK-V4A"],
        },
        lastChangedBy: "WI-20260718-checklist-japanese-docs",
        retirementReason: "",
        supersededBy: "",
        scopeName: "",
        categoryName: "",
      },
      {
        id: "REQ-DESIGN-005",
        revision: 2,
        status: "active",
        kind: "functional",
        title: "CDKデプロイ設計の生成",
        subject: "設計生成器",
        actionName: "derive",
        objectName: "合成済みCloudFormationからのresourceとparameter一覧",
        rationale: "合成されたデプロイテンプレートが具体的なインフラストラクチャIFである。",
        sourceRefs: ["user:2026-07-17", "AWS CDK synth documentation", "CloudFormation template anatomy"],
        acceptanceCriteria: [
          { id: "AC-DESIGN-005-1", given: "AWS CDK stackがCloudFormation YAMLまたはJSONを合成している", when_: "CDK設計生成器を実行する", expected: "テンプレートからresourceとparameterの詳細文書を生成する" }
        ],
        verification: { method: "自動テスト", evidence: "CloudFormation fixtureの出力アサーション" },
        traces: {
          design: [".agents/skills/generate-implementation-design/references/cdk-contract.md"],
          implementation: [".agents/skills/generate-implementation-design/scripts/designflow.py"],
          tests: ["tests/test_designflow.py"],
          standards: ["AWS-WAF"],
        },
        lastChangedBy: "WI-20260718-checklist-japanese-docs",
        retirementReason: "",
        supersededBy: "",
        scopeName: "",
        categoryName: "",
      },
      {
        id: "REQ-DESIGN-006",
        revision: 3,
        status: "active",
        kind: "quality",
        title: "実装と設計の差分検出",
        subject: "設計フロー",
        actionName: "detect",
        objectName: "実装成果物と自動生成された詳細設計の差分",
        rationale: "digestと決定論的なバイト比較により実装と設計の1対1再現性を強制し、更新漏れの対象pathを特定する。",
        sourceRefs: ["user:2026-07-17", "user:2026-07-21", "docs/standards/AS-BUILT-DESIGN.md"],
        acceptanceCriteria: [
          { id: "AC-DESIGN-006-1", given: "宣言済みの自動生成設計がある", when_: "設計check modeを実行する", expected: "source SHA-256 manifestとクリーンな再生成結果がバイト単位で一致し、差分時は対象pathを列挙して非0終了する" }
        ],
        verification: { method: "自動テスト", evidence: "変更済みsourceを用いたdriftと差分pathの検出テスト" },
        traces: {
          design: [".agents/skills/generate-implementation-design/SKILL.md", "docs/standards/AS-BUILT-DESIGN.md"],
          implementation: [".agents/skills/generate-implementation-design/scripts/designflow.py", "governance/checks/catalog.yaml"],
          tests: ["tests/test_designflow.py", "tests/test_review_contract.py"],
          standards: ["SWEBOK-V4A", "DEVSTD-AS-BUILT"],
        },
        lastChangedBy: "CHG-20260721-as-built-design",
        retirementReason: "",
        supersededBy: "",
        scopeName: "",
        categoryName: "",
      },
      {
        id: "REQ-DISC-001",
        revision: 2,
        status: "active",
        kind: "functional",
        title: "研究に裏付けられた意図の探索",
        subject: "開発エージェント",
        actionName: "discover",
        objectName: "適切な対話を通じたユーザーの意図する成果",
        rationale: "言語化しきれていない要求を負担なく探り当てるには、心地よい傾聴と精密な言語化が必要である。",
        sourceRefs: ["user:2026-07-17", "Design Council Double Diamond", "calibrated listening research"],
        acceptanceCriteria: [
          { id: "AC-DISC-001-1", given: "ユーザーの要求が不完全または曖昧である", when_: "解釈差が成果を変える", expected: "推定した目的、制約、葛藤、最小限の重要質問を迎合せず提示する" }
        ],
        verification: { method: "契約レビュー", evidence: "Skill指示と研究根拠" },
        traces: {
          design: [".agents/skills/maintain-canonical-requirements/references/research-basis.md"],
          implementation: [".agents/skills/maintain-canonical-requirements/SKILL.md", ".agents/skills/calibrated-collaborative-listening/SKILL.md"],
          tests: ["tests/test_skills.py"],
          standards: ["SWEBOK-V4A"],
        },
        lastChangedBy: "WI-20260718-checklist-japanese-docs",
        retirementReason: "",
        supersededBy: "",
        scopeName: "",
        categoryName: "",
      },
      {
        id: "REQ-DISC-002",
        revision: 4,
        status: "active",
        kind: "data",
        title: "原子的な永続要件",
        subject: "要件カタログ",
        actionName: "maintain",
        objectName: "正本要件IDごとの一つの原子的な義務",
        rationale: "原子的な要件は独立した変更、検証、トレーサビリティを可能にする。",
        sourceRefs: ["user:2026-07-17", "SWEBOK Software Requirements"],
        acceptanceCriteria: [
          { id: "AC-DISC-002-1", given: "永続的な義務が受け入れられている", when_: "要件を永続化する", expected: "一つのID、主体、正規化action、対象、状態、受入条件、検証、traceを正本に持つ構造的完全性を機械検査し、一つの意味的義務だけを表す原子性は権限あるhuman semantic reviewで確認する" },
          { id: "AC-DISC-002-2", given: "要件にdesign、implementationまたはtests traceがある", when_: "catalogを検証する", expected: "同一category内のduplicate linkとrepository内でlexical no-followにより解決しないpathを拒否する" },
          { id: "AC-DISC-002-3", given: "active要件を実装前のrequirements phaseで確定する", when_: "catalogを検証してdownstreamへ引き渡す", expected: "現時点のsource、verification、既存traceを保持し、まだ存在しないimplementationまたはtests pathを要求せず、下流artifactが作成されたphaseでtraceを独立更新する" }
        ],
        verification: { method: "構造自動テストとhuman semantic review", evidence: "不完全な構造の拒否記録と、一つのIDが一つの意味的義務だけを表すreview記録" },
        traces: {
          design: [".agents/skills/maintain-canonical-requirements/assets/requirements.schema.json"],
          implementation: [".agents/skills/maintain-canonical-requirements/scripts/specflow.py"],
          tests: ["tests/test_specflow.py"],
          standards: ["SWEBOK-V4A"],
        },
        lastChangedBy: "CHG-20260829-review-remediation",
        retirementReason: "",
        supersededBy: "",
        scopeName: "",
        categoryName: "",
      },
      {
        id: "REQ-DISC-003",
        revision: 6,
        status: "active",
        kind: "functional",
        title: "安全な要件ライフサイクル変更",
        subject: "仕様管理フロー",
        actionName: "maintain",
        objectName: "版と同時更新安全性を保つQuint要件の追加、更新、廃止",
        rationale: "一次言語を一つに保ち、版更新、完全検証、廃止墓標、compare-and-swapにより更新消失と履歴消去を防ぐ。",
        sourceRefs: ["user:2026-07-17", "user:2026-08-27", "user:2026-08-29"],
        acceptanceCriteria: [
          { id: "AC-DISC-003-1", given: "新しいQuint要件を追加する", when_: "変更を確定する", expected: "catalogRevisionを一つ進め、対象をactiveかつrevision 1で追加する" },
          { id: "AC-DISC-003-2", given: "active要件の意味、分類またはverificationを変更する", when_: "updateを確定する", expected: "catalogRevisionと対象revisionをそれぞれ一つ進める" },
          { id: "AC-DISC-003-3", given: "正本だった要件の削除が要求される", when_: "変更を受け入れる", expected: "catalogRevisionと対象revisionをそれぞれ一つ進め、理由付きの廃止墓標として項目を残す" },
          { id: "AC-DISC-003-4", given: "生成開始後に別processが派生viewを変更する", when_: "要件JSONとMarkdownを公開する", expected: "開始時snapshotとの差を検出して全出力の上書きを拒否する" },
          { id: "AC-DISC-003-5", given: "Quint要件変更がある", when_: "派生viewを公開する", expected: "typecheckとcatalog不変条件検査を通した同一catalogからJSONとMarkdownを生成する" },
          { id: "AC-DISC-003-6", given: "catalogRevisionまたは対象revisionが開始時の期待値と異なる", when_: "add、update、trace updateまたはretireを試みる", expected: "staleなcompare-and-swapとしてcatalogを変更せず拒否する" },
          { id: "AC-DISC-003-7", given: "retired要件がある", when_: "update、trace updateまたは再retireを試みる", expected: "墓標を変更せず拒否する" },
          { id: "AC-DISC-003-8", given: "active要件のtrace集合を変更する", when_: "trace updateを確定する", expected: "独立したtrace操作としてcatalogRevisionと対象revisionをそれぞれ一つ進める" },
          { id: "AC-DISC-003-9", given: "activeまたはretired要件がある", when_: "retirement fieldsを検証する", expected: "activeのretirementReasonとsupersededByは空であり、retiredは理由を持ち、superseded chainはcatalog順で前進して循環せず、最終的にactive要件へ到達する" },
          { id: "AC-DISC-003-10", given: "一つのchangeに異なる要件への複数operationがある", when_: "atomic batchを確定する", expected: "catalogRevisionを一つだけ進め、各対象revisionを一つ進め、同一要件の二重touchまたはいずれかのstale CAS・不正値があればbatch全体を変更せず拒否する" }
        ],
        verification: { method: "Quint検証と自動テスト", evidence: "add、update、trace update、retireの版遷移、CAS競合、型、生成drift、廃止墓標の検査" },
        traces: {
          design: [".agents/skills/maintain-canonical-requirements/SKILL.md"],
          implementation: ["spec/requirements/requirements.qnt", "tools/quintflow.py", "tools/safe_io.py", ".agents/skills/maintain-canonical-requirements/scripts/specflow.py"],
          tests: ["tests/test_quintflow.py", "tests/test_specflow.py"],
          standards: ["SWEBOK-V4A", "QUINT-0.32"],
        },
        lastChangedBy: "CHG-20260829-review-remediation",
        retirementReason: "",
        supersededBy: "",
        scopeName: "project",
        categoryName: "nonfunctional",
      },
      {
        id: "REQ-DISC-004",
        revision: 5,
        status: "active",
        kind: "functional",
        title: "要件文書の自動生成",
        subject: "仕様管理フロー",
        actionName: "generate",
        objectName: "QuintからJSONを経由した日本語の人間向け要件文書",
        rationale: "生成ビューは競合する編集可能な正本を作らずに読者へ情報を提供する。",
        sourceRefs: ["user:2026-07-17", "user:2026-08-27", "user:2026-08-29"],
        acceptanceCriteria: [
          { id: "AC-DISC-004-1", given: "Quint正本が有効である", when_: "文書生成と差分検査を実行する", expected: "QuintからList順と空文字fieldを含む全fieldを保持したserialized JSONを生成し、そのserialized JSONを再parseした値だけから日本語文書をバイト一致で再現する" },
          { id: "AC-DISC-004-2", given: "QuintとJSONで各fieldに異なるgolden値、空optional値、順序の異なる複数要件がある", when_: "写像と逆写像を検査する", expected: "catalog、要件、受入条件、verification、全trace、分類、廃止情報の各fieldとList順が欠落や入替えなく往復し、Markdown意味へ対応する" }
        ],
        verification: { method: "自動テスト", evidence: "全field golden mapping、serialized JSON入力境界、Given When Then意味、生成文書の完全一致検査" },
        traces: {
          design: ["docs/requirements/REQUIREMENTS.md"],
          implementation: ["tools/quintflow.py", "tools/spec_mapping.py", "tools/render_requirements.py", ".agents/skills/maintain-canonical-requirements/scripts/specflow.py"],
          tests: ["tests/test_quintflow.py", "tests/test_specflow.py"],
          standards: ["SWEBOK-V4A", "QUINT-0.32"],
        },
        lastChangedBy: "CHG-20260829-review-remediation",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "functional",
      },
      {
        id: "REQ-DISC-005",
        revision: 3,
        status: "active",
        kind: "functional",
        title: "solution候補と永続要件の境界",
        subject: "要件管理Skill",
        actionName: "separate",
        objectName: "solution候補と権限ある永続要件",
        rationale: "結果や品質ではなく可逆な実装手段を正本へ固定すると設計裁量と変更容易性を失う一方、契約、法令、互換性、既存基盤、support境界または親判断に基づく正当な制約は保持する必要があるため。",
        sourceRefs: ["user:2026-07-24", "issue:25", "NASA Systems Engineering Handbook Appendix", "NASA SWE-050", "SWEBOK-V4A", "Nuseibeh:10.1109/2.910904", "Chen-Babar-Nuseibeh:10.1109/MS.2012.174"],
        acceptanceCriteria: [
          { id: "AC-DISC-005-1", given: "technology、architecture、tool、path、process、工程または成果物を名指しする要件候補がある", when_: "正本への反映可否を判定する", expected: "underlying outcome、necessity、authority、lifetime、scope、placementを判定し、可逆なsolution choiceを永続要件へ固定しない" },
          { id: "AC-DISC-005-2", given: "exact technology、architectureまたはproject process自体が権限ある永続制約である", when_: "永続要件として保持する", expected: "source_refs、必要性を示すrationale、scopeとcategory、verificationを記録する" },
          { id: "AC-DISC-005-3", given: "親要件または承認済みarchitecture decisionが下位scopeを拘束する", when_: "下位の永続義務として保持する", expected: "親要件またはdecision、下位scope、verificationへtraceしたderived requirementとして記録し、上位stakeholder requirementへ過剰一般化しない" }
        ],
        verification: { method: "自動テスト", evidence: "solution-only instruction、権限あるtechnology constraint、quality-of-service、ADR、derived requirement、product identityのpositive / negative contract test" },
        traces: {
          design: ["docs/standards/REQUIREMENT-CLASSIFICATION.md", "docs/guides/getting-started.md", ".agents/skills/maintain-canonical-requirements/references/research-basis.md"],
          implementation: [".agents/skills/maintain-canonical-requirements/SKILL.md", ".agents/skills/chat-first-development/SKILL.md", ".agents/skills/elicit-frontend-requirements/SKILL.md", ".agents/skills/maintain-canonical-requirements/assets/requirements.schema.json"],
          tests: ["tests/test_skills.py", "tests/test_specflow.py"],
          standards: ["SWEBOK-V4A"],
        },
        lastChangedBy: "user:2026-09-06",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "functional",
      },
      {
        id: "REQ-DOCS-003",
        revision: 1,
        status: "active",
        kind: "quality",
        title: "利用目的に基づく文書の最小保守",
        subject: "参照repositoryの文書保守",
        actionName: "maintain",
        objectName: "現行文書の利用者・目的・更新条件を明記し、変更と整合させ、不要文書と時点記録を分離すること",
        rationale: "使われない文書と重複した指示の維持負担を減らし、要件だけの依頼から対象projectへ3本柱を導入できる入口を保つ。",
        sourceRefs: ["user:2026-09-06"],
        acceptanceCriteria: [
          { id: "AC-DOCS-003-1", given: "文書を維持または追加する", when_: "文書索引を確認する", expected: "利用者・目的・更新条件が明示され、現行文書への参照が解決する" },
          { id: "AC-DOCS-003-2", given: "機能・Skill・配布の変更がある", when_: "保守Skillを実行する", expected: "関連する現行文書と正本・生成器を更新し、不要文書は呼出元ごと削除する。履歴は日付と更新対象外を表示し当時の内容を維持する" },
          { id: "AC-DOCS-003-3", given: "利用者が参照URLと開発要件を依頼する", when_: "既定導入を行う", expected: "対象projectの構成に合わせて要件初期化・設計生成・関連検査を実行し、文書保守のための追加Skill・承認工程・定型報告書を要求しない" }
        ],
        verification: { method: "自動検査と利用経路レビュー", evidence: "現行リンクと索引網羅の検査、既定4 Skillとhost配布の回帰検査、要件初期化・設計生成・検査経路の確認" },
        traces: {
          design: ["docs/README.md", "docs/guides/getting-started.md"],
          implementation: [".agents/skills/maintain-reference-repository/SKILL.md", ".agents/skills/chat-first-development/SKILL.md", "tools/audit_consistency.py"],
          tests: ["tests/test_audit_consistency.py", "tests/test_install_reference.py", "tests/test_design_adoption.py"],
          standards: [],
        },
        lastChangedBy: "user:2026-09-06",
        retirementReason: "",
        supersededBy: "",
        scopeName: "project",
        categoryName: "nonfunctional",
      },
      {
        id: "REQ-DOCS-001",
        revision: 1,
        status: "active",
        kind: "quality",
        title: "日本語の利用者向け文書",
        subject: "文書生成フロー",
        actionName: "provide",
        objectName: "識別子と固有名詞を除いて日本語で統一された利用者向け文書",
        rationale: "導入・運用・監査の文書言語を統一し、意味の取り違えと二重保守を防ぐ。",
        sourceRefs: ["user:2026-07-18"],
        acceptanceCriteria: [
          { id: "AC-DOCS-001-1", given: "利用者向けMarkdownまたは生成文書がある", when_: "リポジトリ検証を実行する", expected: "見出しと説明が日本語であり、生成物が日本語テンプレートから再現される" }
        ],
        verification: { method: "自動検査", evidence: "日本語文書検査と生成差分テスト" },
        traces: {
          design: ["docs/README.md"],
          implementation: [".agents/skills/maintain-canonical-requirements/scripts/specflow.py", ".agents/skills/verify-against-engineering-standards/scripts/standardsflow.py"],
          tests: ["tests/test_validate_repo.py", "tests/test_specflow.py", "tests/test_standardsflow.py"],
          standards: ["SWEBOK-V4A"],
        },
        lastChangedBy: "WI-20260718-checklist-japanese-docs",
        retirementReason: "",
        supersededBy: "",
        scopeName: "",
        categoryName: "",
      },
      {
        id: "REQ-EXEC-001",
        revision: 3,
        status: "active",
        kind: "operational",
        title: "多軸execution profileの推定",
        subject: "開発実行基盤",
        actionName: "estimate",
        objectName: "相互に独立した変更範囲、保証水準、計算資源および実行方式",
        rationale: "局所的だが重大な変更と、広範囲だが機械的な変更を単一レベルで混同しないため。",
        sourceRefs: ["user:2026-07-18", "user:2026-08-29", "arXiv:2607.13034", "arXiv:2407.01489"],
        acceptanceCriteria: [
          { id: "AC-EXEC-001-1", given: "repository変更依頼と決定的metadataがある", when_: "実装前profileを生成する", expected: "scope、assurance、compute、modeを直接根拠とともに独立記録し、同一入力とpolicyからtimestampを除く同一decision projectionを生成する" }
        ],
        verification: { method: "自動テスト", evidence: "多軸独立性、schema適合性および再現性の回帰テスト" },
        traces: {
          design: [".agents/skills/right-size-execution/references/execution-dimensions.md"],
          implementation: [".agents/skills/right-size-execution/scripts/executionflow.py", ".agents/skills/right-size-execution/assets/execution-policy.json", ".agents/skills/right-size-execution/assets/execution-profile.schema.json"],
          tests: ["tests/test_executionflow.py"],
          standards: ["SWEBOK-V4A"],
        },
        lastChangedBy: "user:2026-08-29",
        retirementReason: "",
        supersededBy: "",
        scopeName: "project",
        categoryName: "nonfunctional",
      },
      {
        id: "REQ-EXEC-002",
        revision: 3,
        status: "active",
        kind: "quality",
        title: "保証水準の下限制御",
        subject: "開発実行基盤",
        actionName: "enforce",
        objectName: "risk tag、成果物、外部副作用および不可逆性から導出したassurance下限",
        rationale: "重大性は探索範囲ではなく必要な保証の深さへ反映すべきである。",
        sourceRefs: ["user:2026-07-18", "user:2026-08-29", "SWEBOK-V4A"],
        acceptanceCriteria: [
          { id: "AC-EXEC-002-1", given: "risk tagと成果物tagがある", when_: "assuranceを推定または監査する", expected: "両集合のassurance floorの高い方を採用し、高riskだけでscopeを広げない" }
        ],
        verification: { method: "自動テスト", evidence: "artifact-only elevated、risk-wins critical、local-criticalの交差ケース" },
        traces: {
          design: [".agents/skills/right-size-execution/references/execution-dimensions.md"],
          implementation: [".agents/skills/right-size-execution/scripts/executionflow.py", ".agents/skills/right-size-execution/assets/execution-policy.json"],
          tests: ["tests/test_executionflow.py"],
          standards: ["SWEBOK-V4A"],
        },
        lastChangedBy: "user:2026-08-29",
        retirementReason: "",
        supersededBy: "",
        scopeName: "project",
        categoryName: "nonfunctional",
      },
      {
        id: "REQ-EXEC-003",
        revision: 3,
        status: "active",
        kind: "quality",
        title: "追加LLM呼出しを伴わない初期推定",
        subject: "開発実行基盤",
        actionName: "route",
        objectName: "通常のルート判断と決定的metadataによる初期Estimate",
        rationale: "Estimate自体が余分なLLMコストになり、単純な作業の利点を失うことを防ぐため。",
        sourceRefs: ["user:2026-07-18", "ACL:2024.naacl-long.389"],
        acceptanceCriteria: [
          { id: "AC-EXEC-003-1", given: "依頼文、path、manifestまたは依存metadataがある", when_: "初期profileを推定する", expected: "Estimate専用LLMを呼ばず、結果を変える不明点だけmetadata probeを最大一回実行して費用を記録する" }
        ],
        verification: { method: "自動テスト", evidence: "probe上限、再利用可能なprobe証拠およびEstimate overheadの検査" },
        traces: {
          design: [".agents/skills/right-size-execution/SKILL.md"],
          implementation: [".agents/skills/right-size-execution/scripts/executionflow.py"],
          tests: ["tests/test_executionflow.py"],
          standards: ["SWEBOK-V4A"],
        },
        lastChangedBy: "WI-20260718-right-size-execution-v2",
        retirementReason: "",
        supersededBy: "",
        scopeName: "",
        categoryName: "",
      },
      {
        id: "REQ-EXEC-004",
        revision: 2,
        status: "active",
        kind: "quality",
        title: "校正可能な確信度",
        subject: "開発実行基盤",
        actionName: "constrain",
        objectName: "実行制御へ入力するconfidenceの根拠とscore",
        rationale: "未校正のLLM自己申告値を閾値判定に使わず、観測特徴または実績で校正したrouterだけを使うため。",
        sourceRefs: ["user:2026-07-18", "arXiv:2406.18665"],
        acceptanceCriteria: [
          { id: "AC-EXEC-004-1", given: "校正済みrouterが未導入である", when_: "confidenceを記録する", expected: "deterministic feature evidenceとbandを記録しscoreをnullにする" }
        ],
        verification: { method: "自動テスト", evidence: "任意の自己申告scoreを拒否するschema・回帰テスト" },
        traces: {
          design: [".agents/skills/right-size-execution/references/execution-dimensions.md"],
          implementation: [".agents/skills/right-size-execution/assets/execution-profile.schema.json", ".agents/skills/right-size-execution/scripts/executionflow.py"],
          tests: ["tests/test_executionflow.py"],
          standards: ["SWEBOK-V4A"],
        },
        lastChangedBy: "WI-20260718-right-size-execution-v2",
        retirementReason: "",
        supersededBy: "",
        scopeName: "",
        categoryName: "",
      },
      {
        id: "REQ-EXEC-005",
        revision: 2,
        status: "active",
        kind: "quality",
        title: "最小十分な検証の導出",
        subject: "開発実行基盤",
        actionName: "derive",
        objectName: "scope、assurance、成果物、risk、受入条件および対象repositoryが明示したgateの完全一致するverification projection",
        rationale: "機能影響の広さと必要保証の深さを分離しながら、重大な検証漏れを防ぐため。",
        sourceRefs: ["user:2026-07-18", "user:2026-08-29", "SWEBOK-V4A"],
        acceptanceCriteria: [
          { id: "AC-EXEC-005-1", given: "schema適合profileと受入条件がある", when_: "検証集合を導出する", expected: "scope、assurance、成果物、risk、受入条件および対象repositoryが明示したgateの決定的和集合だけをblocking集合とし、追加diagnosticを別のadvisory集合へ分離する" }
        ],
        verification: { method: "自動テスト", evidence: "projection component、余分または不足checkの成功拒否、diagnostic非blocking" },
        traces: {
          design: [".agents/skills/right-size-execution/references/execution-dimensions.md"],
          implementation: [".agents/skills/right-size-execution/scripts/executionflow.py"],
          tests: ["tests/test_executionflow.py"],
          standards: ["SWEBOK-V4A"],
        },
        lastChangedBy: "user:2026-08-29",
        retirementReason: "",
        supersededBy: "",
        scopeName: "project",
        categoryName: "nonfunctional",
      },
      {
        id: "REQ-EXEC-006",
        revision: 2,
        status: "active",
        kind: "quality",
        title: "根拠付きの単軸Expand",
        subject: "開発実行基盤",
        actionName: "expand",
        objectName: "初期profileを覆す新証拠に対応する一つの実行軸",
        rationale: "推定誤りを回復しながら、無関係な軸の同時拡張と一律回数上限による回復阻害を防ぐため。",
        sourceRefs: ["user:2026-07-18", "user:2026-08-29", "arXiv:2607.13034"],
        acceptanceCriteria: [
          { id: "AC-EXEC-006-1", given: "許可理由と直接証拠がある", when_: "profileを拡張する", expected: "scope、assurance、verification、review、computeのうち一軸だけを変更し、stable failure identityの再登場をstagnationとして拒否し、各eventを前event digestへ連結する" }
        ],
        verification: { method: "自動テスト", evidence: "12回diagnosticのcount cap不存在、同identity別文言拒否、expansion chain tamperの回帰テスト" },
        traces: {
          design: [".agents/skills/right-size-execution/references/expansion-contract.md"],
          implementation: [".agents/skills/right-size-execution/scripts/executionflow.py"],
          tests: ["tests/test_executionflow.py"],
          standards: ["SWEBOK-V4A"],
        },
        lastChangedBy: "user:2026-08-29",
        retirementReason: "",
        supersededBy: "",
        scopeName: "project",
        categoryName: "nonfunctional",
      },
      {
        id: "REQ-EXEC-007",
        revision: 2,
        status: "active",
        kind: "quality",
        title: "成功後の停止",
        subject: "開発実行基盤",
        actionName: "stop",
        objectName: "成功条件、required verificationおよびassurance floor充足後の正のコスト活動",
        rationale: "成功後の念のための探索や能力引上げを防ぎ、必須確定処理だけを許可するため。",
        sourceRefs: ["user:2026-07-18", "user:2026-08-29", "arXiv:2607.13034"],
        acceptanceCriteria: [
          { id: "AC-EXEC-007-1", given: "選択projectionと完全一致するverificationがassurance-aligned modeで成功した", when_: "decisive successを記録する", expected: "projection、assurance、selector、全expansion chainを結ぶstop digestを作り、成功後expandを拒否またはpost-success活動として監査する" }
        ],
        verification: { method: "自動テスト", evidence: "検証の不足または余分を伴う成功拒否、stop digest tamper、成功後Expand拒否" },
        traces: {
          design: [".agents/skills/right-size-execution/references/stopping-contract.md"],
          implementation: [".agents/skills/right-size-execution/scripts/executionflow.py"],
          tests: ["tests/test_executionflow.py"],
          standards: ["SWEBOK-V4A"],
        },
        lastChangedBy: "user:2026-08-29",
        retirementReason: "",
        supersededBy: "",
        scopeName: "project",
        categoryName: "nonfunctional",
      },
      {
        id: "REQ-EXEC-008",
        revision: 2,
        status: "active",
        kind: "quality",
        title: "実行効率の計測",
        subject: "開発実行基盤",
        actionName: "measure",
        objectName: "明示選択時だけの推定、Estimate overhead、実績、Expand、品質および停止後活動の任意計測",
        rationale: "成功率と重大欠陥を制約にし、oracleなしの単一効率指標へ過適合しないため。",
        sourceRefs: ["user:2026-07-18", "user:2026-08-29", "arXiv:2607.13034"],
        acceptanceCriteria: [
          { id: "AC-EXEC-008-1", given: "利用者がtelemetry、benchmark、calibrationまたはauditを明示選択している", when_: "効率reportを確定する", expected: "tokenまたはproxy、時間、tool、read、probe、Expand、model、成功、escaped defectおよび停止後活動を保存し、oracleなしでACRRを表明せず、通常作業に永続台帳を要求しない" }
        ],
        verification: { method: "自動テストとbenchmark", evidence: "生指標、overrun、proxyおよびACRR境界の検査" },
        traces: {
          design: [".agents/skills/right-size-execution/references/measurement-contract.md"],
          implementation: [".agents/skills/right-size-execution/scripts/executionflow.py"],
          tests: ["tests/test_executionflow.py"],
          standards: ["SWEBOK-V4A"],
        },
        lastChangedBy: "user:2026-08-29",
        retirementReason: "",
        supersededBy: "",
        scopeName: "project",
        categoryName: "nonfunctional",
      },
      {
        id: "REQ-EXEC-009",
        revision: 3,
        status: "active",
        kind: "quality",
        title: "監査可能なチェック選択",
        subject: "標準検証基盤",
        actionName: "select",
        objectName: "version固定selectorによるチェック候補と選択漏れ監査sample",
        rationale: "未選択とN/Aを分離し、削減件数だけでなく重大controlの偽陰性を監査するため。",
        sourceRefs: ["user:2026-07-18", "user:2026-08-29", "SWEBOK-V4A"],
        acceptanceCriteria: [
          { id: "AC-EXEC-009-1", given: "execution profileとversion固定catalogがある", when_: "チェック候補を選択する", expected: "assurance、artifact、risk、phase、changed path、対象所有gateから選び、各selected IDの選択根拠、入力、選択digest、除外数、決定的監査sample、mandatory missを保存し、CASでcommitmentを維持する" }
        ],
        verification: { method: "自動テストとbenchmark", evidence: "選択根拠、curated mandatory controlの選択漏れゼロ、除外監査sample、CAS競合拒否" },
        traces: {
          design: [".agents/skills/right-size-execution/SKILL.md"],
          implementation: ["governance/checklist/catalog.json", ".agents/skills/right-size-execution/scripts/executionflow.py"],
          tests: ["tests/test_executionflow.py"],
          standards: ["SWEBOK-V4A"],
        },
        lastChangedBy: "CHG-20260829-review-remediation",
        retirementReason: "",
        supersededBy: "",
        scopeName: "project",
        categoryName: "nonfunctional",
      },
      {
        id: "REQ-EXEC-010",
        revision: 2,
        status: "active",
        kind: "constraint",
        title: "段階的な適用",
        subject: "実行効率制御",
        actionName: "stage",
        objectName: "repository blockerを増やさないtelemetry、shadow、soft routing、calibrationおよびadvisory診断の導入順序",
        rationale: "実行profileのschema、assurance、efficiency診断を第4のportable blockerへ昇格させず、未校正な効率規則が品質を損なうことを防ぐため。",
        sourceRefs: ["user:2026-07-18", "user:2026-08-27", "user:2026-08-29", "arXiv:2406.18665"],
        acceptanceCriteria: [
          { id: "AC-EXEC-010-1", given: "schema、assuranceまたはefficiencyの実行profile診断がある", when_: "shadowまたは通常modeで診断を報告する", expected: "diagnosticはrepository_blocking=falseのadvisory evidenceとなり、要件、as-built設計、選択check以外のportable blockerを作らない" }
        ],
        verification: { method: "自動テスト", evidence: "schema、assurance、efficiency診断がadvisoryかつrepository_blocking=falseとなる回帰テスト" },
        traces: {
          design: [".agents/skills/right-size-execution/references/measurement-contract.md"],
          implementation: [".agents/skills/right-size-execution/assets/execution-policy.json", ".agents/skills/right-size-execution/scripts/executionflow.py"],
          tests: ["tests/test_executionflow.py"],
          standards: ["SWEBOK-V4A"],
        },
        lastChangedBy: "user:2026-08-29",
        retirementReason: "",
        supersededBy: "",
        scopeName: "project",
        categoryName: "nonfunctional",
      },
      {
        id: "REQ-FRAME-001",
        revision: 3,
        status: "active",
        kind: "constraint",
        title: "workと正本の境界",
        subject: "リポジトリ",
        actionName: "separate",
        objectName: "一時的な作業記録と永続的な製品要件",
        rationale: "work itemは実行文脈であり、暗黙に製品仕様の正本へ変わってはならない。",
        sourceRefs: ["user:2026-07-17"],
        acceptanceCriteria: [
          { id: "AC-FRAME-001-1", given: "統制対象の要求が存在する", when_: "要求を記録する", expected: "workには要求断片、判断、計画、証跡だけが残り、永続要件は正本へ保存される" }
        ],
        verification: { method: "自動検査", evidence: "リポジトリ検証とSkill契約テスト" },
        traces: {
          design: ["docs/guides/getting-started.md"],
          implementation: [".agents/skills/maintain-canonical-requirements/SKILL.md"],
          tests: ["tests/test_specflow.py"],
          standards: ["SWEBOK-V4A"],
        },
        lastChangedBy: "CHG-20260802-skills-audit-remediation",
        retirementReason: "",
        supersededBy: "",
        scopeName: "",
        categoryName: "",
      },
      {
        id: "REQ-PORTABLE-001",
        revision: 5,
        status: "active",
        kind: "operational",
        title: "チャットだけで移植できる導入",
        subject: "移植可能なSkills集",
        actionName: "enable",
        objectName: "別リポジトリへのcopy-and-chat方式の導入",
        rationale: "本リポジトリは再利用可能な参照集であり、利用者が内部ツールを手動操作せずに使える必要がある。",
        sourceRefs: ["user:2026-07-17", "user:2026-08-27", "user:2026-08-29"],
        acceptanceCriteria: [
          { id: "AC-PORTABLE-001-1", given: "対象Skillsフォルダを別リポジトリへコピーしている", when_: "利用者が自然言語で開発要求を相談する", expected: "通常のチャットから導入、要件、設計、実装、テスト、依頼された公開までを自動実行する" },
          { id: "AC-PORTABLE-001-2", given: "空の対象repositoryとdefault、fullまたはdefaultにregulated addonを合成したprofileとCodexまたはClaude hostの組合せがある", when_: "profileを導入して配布closureをE2E検査する", expected: "base profileの各Skill形式契約、必須asset、runner、固定されたQuint依存が導入先だけで解決し、defaultとfullでは3本柱、default+regulatedでは3本柱と明示選択したregulated補助機能のgenerateとcheckをsource repositoryのfileなしで実行できる" }
        ],
        verification: { method: "自動E2Eテスト", evidence: "default、full、default+regulatedと両hostの空repository導入、参照closure、Quint generate/check、設計drift、selected check実行テスト" },
        traces: {
          design: ["docs/guides/getting-started.md", "docs/decisions/ADR-0003-canonical-host-asset-generation.md"],
          implementation: ["distribution/manifest.json", "distribution/host-adapters.json", ".agents/skills/chat-first-development/SKILL.md", "tools/install_reference.py", "tools/generate_host_assets.py", ".github/workflows/host-assets.yml"],
          tests: ["tests/test_install_reference.py", "tests/test_skills.py", "tests/test_generate_host_assets.py", "tests/test_profile_boundaries.py"],
          standards: ["SWEBOK-V4A"],
        },
        lastChangedBy: "CHG-20260829-review-remediation",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "functional",
      },
      {
        id: "REQ-PORTABLE-002",
        revision: 1,
        status: "active",
        kind: "constraint",
        title: "導入先repository policyの非強制",
        subject: "portable installerと既定profile",
        actionName: "preserve",
        objectName: "導入先のbranch、merge rule、CI workflowを追加も変更もしないこと",
        rationale: "3本柱は開発成果物の整合性を扱い、repository運用方針は導入先のauthorityへ委任する。",
        sourceRefs: ["user:2026-08-27", "https://quint.sh/docs/what-does-quint-do", "docs/decisions/ADR-0004-quint-three-pillar-portability.md"],
        acceptanceCriteria: [
          { id: "AC-PORTABLE-002-1", given: "独自のbranch ruleとCI workflowを持つ導入先がある", when_: "既定profileを適用する", expected: "既存設定がbyte一致し、新しいworkflow、ruleset、merge方式が追加されない" }
        ],
        verification: { method: "installer isolation test", evidence: "既存.github/workflowsとpolicy fixtureの適用前後byte比較" },
        traces: {
          design: ["docs/decisions/ADR-0004-quint-three-pillar-portability.md"],
          implementation: ["distribution/manifest.json", "tools/install_reference.py"],
          tests: ["tests/test_install_reference.py", "tests/test_profile_boundaries.py"],
          standards: ["QUINT-0.32"],
        },
        lastChangedBy: "CHG-20260827-quint-three-pillars",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "nonfunctional",
      },
      {
        id: "REQ-PORTABLE-003",
        revision: 2,
        status: "active",
        kind: "constraint",
        title: "外部操作の明示権限境界",
        subject: "portable Skillとruntime",
        actionName: "constrain",
        objectName: "外部または不可逆な操作を利用者が明示した依頼と必要な承認の範囲だけに限定すること",
        rationale: "copy-and-chatで導入したガードレールが、要件更新や検査を理由に未依頼の公開、deploy、merge、外部記録または高額操作へ権限を広げてはならない。",
        sourceRefs: ["user:2026-09-05", "user:2026-08-27", "user:2026-08-29", "AGENTS.md"],
        acceptanceCriteria: [
          { id: "AC-PORTABLE-003-1", given: "外部systemへの書込みまたは不可逆な操作が開発手順に現れる", when_: "portable Skillまたはruntimeが実行可否を判断する", expected: "利用者がその結果を明示的に依頼し、対象systemに必要な権限が確認できる場合だけ実行し、それ以外はrepository内の成果物またはhandoffに留める" },
          { id: "AC-PORTABLE-003-2", given: "同じ対象と外部作用への明示依頼・承認が会話または対象所有記録にあり、撤回・失効していない", when_: "後続の手順で同じ権限境界を確認する", expected: "既存承認を再利用し、形式的な再承認や別Skillの導入を要求しない。範囲拡張、失効、対象側の必須承認は省略しない" }
        ],
        verification: { method: "契約テストとmutation test", evidence: "未依頼外部操作の拒否、明示依頼と権限を伴う操作の許可、外部anchor handoff境界の検査" },
        traces: {
          design: ["AGENTS.md"],
          implementation: [".agents/skills/chat-first-development/SKILL.md", ".agents/skills/authorize-autonomous-execution/SKILL.md", "tools/install_reference.py"],
          tests: ["tests/test_skills.py", "tests/test_profile_boundaries.py", "tests/test_install_reference.py"],
          standards: [],
        },
        lastChangedBy: "user:2026-09-05",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "nonfunctional",
      },
      {
        id: "REQ-QUALITY-001",
        revision: 2,
        status: "active",
        kind: "operational",
        title: "版管理された出典台帳",
        subject: "品質フレーム",
        actionName: "maintain",
        objectName: "SWEBOKとクラウド・AI公式資料の監査可能な出典台帳",
        rationale: "正式名称、版、URL、参照範囲、差分、固定物ハッシュを保存することで、レビュー根拠を再現し更新を検知できる。",
        sourceRefs: ["user:2026-07-17", "SWEBOK V4", "AWS Well-Architected", "Azure Well-Architected", "Google Cloud Well-Architected", "OCI Best Practices"],
        acceptanceCriteria: [
          { id: "AC-QUALITY-001-1", given: "品質プロファイルを選択している", when_: "出典台帳を検証する", expected: "各資料が公式URL、版、参照日、更新間隔、適用範囲、変更確認日、前版との差分を持ち、固定参照物はSHA-256を持つ" },
          { id: "AC-QUALITY-001-2", given: "添付SWEBOKを参照する", when_: "版の同一性を検証する", expected: "v4.0aの正式名称、18KA対応、固定SHA-256が台帳と一致する" }
        ],
        verification: { method: "自動検査", evidence: "公式host、鮮度、範囲、差分、ハッシュのテスト" },
        traces: {
          design: ["docs/standards/SOURCES.md"],
          implementation: [".agents/skills/verify-against-engineering-standards/scripts/standardsflow.py", "governance/standards/registry.json"],
          tests: ["tests/test_standardsflow.py"],
          standards: ["SWEBOK-V4A", "AWS-WAF", "AWS-GENAI-LENS", "AWS-RAI-LENS", "AWS-ML-LENS", "AWS-AGENTIC-LENS", "AZURE-WAF", "AZURE-AI-WAF", "GCP-WAF", "GCP-AIML-WAF", "OCI-WAF"],
        },
        lastChangedBy: "WI-20260718-checklist-japanese-docs",
        retirementReason: "",
        supersededBy: "",
        scopeName: "",
        categoryName: "",
      },
      {
        id: "REQ-QUALITY-002",
        revision: 5,
        status: "active",
        kind: "quality",
        title: "変更範囲に対応する品質検査",
        subject: "品質フロー",
        actionName: "verify",
        objectName: "変更と受入条件に関係する検査だけによる成果物検証",
        rationale: "関係する失敗を直接証跡で検出しつつ、無関係な全件検査と専用記録の負担を避ける。",
        sourceRefs: ["user:2026-07-17", "user:2026-08-27", "user:2026-08-29", "SWEBOK V4", "cloud vendor official guidance"],
        acceptanceCriteria: [
          { id: "AC-QUALITY-002-1", given: "変更内容と受入条件が分かっている", when_: "品質検査を実行する", expected: "関係する最小のtest、lint、type check、buildまたはgeneratorだけを選び、PassまたはFailと直接証跡を簡潔に示す" },
          { id: "AC-QUALITY-002-2", given: "対象repositoryに該当する既存CIがない", when_: "選択した検査を実行する", expected: "ローカルcommandを使い、新しいCI workflow、required check、review YAMLを要求しない" }
        ],
        verification: { method: "契約テスト", evidence: "選択検査とrepository policy非強制のテスト" },
        traces: {
          design: [".agents/skills/inspect-quality-gates/SKILL.md", ".agents/skills/inspect-quality-gates/references/gate-rules.md"],
          implementation: [".agents/skills/inspect-quality-gates/scripts/inspect.py"],
          tests: ["tests/test_skills.py", "tests/test_review_contract.py", "tests/test_inspect_runner.py"],
          standards: ["SWEBOK-V4A", "AWS-WAF", "AWS-GENAI-LENS", "AWS-RAI-LENS", "AWS-ML-LENS", "AWS-AGENTIC-LENS", "AZURE-WAF", "AZURE-AI-WAF", "GCP-WAF", "GCP-AIML-WAF", "OCI-WAF"],
        },
        lastChangedBy: "CHG-20260829-review-remediation",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "nonfunctional",
      },
      {
        id: "REQ-QUALITY-003",
        revision: 3,
        status: "active",
        kind: "quality",
        title: "原子的なチェック統制",
        subject: "チェックリスト生成フロー",
        actionName: "maintain",
        objectName: "一項目・一統制・一証跡で独立判定できるチェック項目",
        rationale: "複数統制を一行へ詰め込むと部分実装を一意にPassまたはFailと判定できない。",
        sourceRefs: ["user:2026-07-18", "SWEBOK Software Quality"],
        acceptanceCriteria: [
          { id: "AC-QUALITY-003-1", given: "チェック項目を追加または更新する", when_: "ワークブックを生成・検証する", expected: "独立した合否条件を持つ統制へ分割され、既知の複合項目が再発しない" }
        ],
        verification: { method: "自動テストと批判的レビュー", evidence: "原子性回帰テストとチェック項目カタログ" },
        traces: {
          design: ["governance/reviews/README.md"],
          implementation: ["update_checklist.py", ".agents/skills/verify-against-engineering-standards/SKILL.md"],
          tests: ["tests/test_checklist.py"],
          standards: ["SWEBOK-V4A"],
        },
        lastChangedBy: "CHG-20260802-skills-audit-remediation",
        retirementReason: "",
        supersededBy: "",
        scopeName: "",
        categoryName: "",
      },
      {
        id: "REQ-QUALITY-004",
        revision: 2,
        status: "active",
        kind: "constraint",
        title: "3本柱だけのportable guardrail",
        subject: "portable blocking guardrail",
        actionName: "constrain",
        objectName: "要件正本、as-built生成、選択checkの3本柱だけを対象にすること",
        rationale: "導入時の摩擦とfalse blockerを抑え、repository固有の工程を強制しない。",
        sourceRefs: ["user:2026-08-27", "https://quint.sh/docs/what-does-quint-do", "docs/decisions/ADR-0004-quint-three-pillar-portability.md"],
        acceptanceCriteria: [
          { id: "AC-QUALITY-004-1", given: "全Skillの形式契約がある", when_: "Quint不変条件を検証する", expected: "blocking guardrailは3本柱のいずれかに属し、補助Skillはblockingにならない" },
          { id: "AC-QUALITY-004-2", given: "portable contractを検証する", when_: "merge ruleとCI requirementの属性を確認する", expected: "すべてfalseである" }
        ],
        verification: { method: "Quint invariant verification", evidence: "threePillarsOnlyとrepositoryPolicyIsHostOwnedの検証成功" },
        traces: {
          design: ["docs/decisions/ADR-0004-quint-three-pillar-portability.md"],
          implementation: ["spec/skills/skills.qnt", "distribution/manifest.json"],
          tests: ["tests/test_quintflow.py", "tests/test_profile_boundaries.py"],
          standards: ["QUINT-0.32"],
        },
        lastChangedBy: "user:2026-09-06",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "nonfunctional",
      },
      {
        id: "REQ-QUINT-001",
        revision: 3,
        status: "active",
        kind: "constraint",
        title: "Quint要件正本",
        subject: "永続要件",
        actionName: "maintain",
        objectName: "Quint仕様を唯一の編集対象としJSONを派生物として維持すること",
        rationale: "型検査と状態不変条件を要件記述の入口へ置き、手書きJSONの構造矛盾を防ぐ。",
        sourceRefs: ["user:2026-08-27", "user:2026-08-29", "https://quint.sh/docs/what-does-quint-do", "docs/decisions/ADR-0004-quint-three-pillar-portability.md"],
        acceptanceCriteria: [
          { id: "AC-QUINT-001-1", given: "永続要件の意味、分類、verificationまたはtraceを変更する", when_: "要件正本を更新する", expected: "Quint仕様と対象revisionが更新され、typecheckとcatalog invariant成功後に同じ内容のJSONが生成される" },
          { id: "AC-QUINT-001-2", given: "要件catalogとadd、update、trace update、retireの抽象遷移がある", when_: "bounded formal verificationを実行する", expected: "catalogWellFormedとlifecycleRefinesCatalogをrequirements.qntでもApalache検証し、失敗時は一時出力を破棄する前にbounded diagnosticを報告する" }
        ],
        verification: { method: "Quint typecheckと生成drift検査", evidence: "requirements.qntのtypecheck成功とrequirements.jsonのbyte一致" },
        traces: {
          design: ["docs/decisions/ADR-0004-quint-three-pillar-portability.md"],
          implementation: ["spec/requirements/requirements.qnt", "tools/quintflow.py"],
          tests: ["tests/test_quintflow.py", "tests/test_specflow.py"],
          standards: ["QUINT-0.32"],
        },
        lastChangedBy: "CHG-20260829-review-remediation",
        retirementReason: "",
        supersededBy: "",
        scopeName: "project",
        categoryName: "nonfunctional",
      },
      {
        id: "REQ-QUINT-002",
        revision: 3,
        status: "active",
        kind: "functional",
        title: "要件表示の二段生成",
        subject: "要件生成器",
        actionName: "generate",
        objectName: "Quintから全fieldとList順を保持するJSONを生成し、そのserialized JSONから人向けMarkdownを生成すること",
        rationale: "機械検証用表現と人向け表示の責務を分離しつつ、authorityを一本化する。",
        sourceRefs: ["user:2026-08-27", "user:2026-08-29", "https://quint.sh/docs/what-does-quint-do", "docs/decisions/ADR-0004-quint-three-pillar-portability.md"],
        acceptanceCriteria: [
          { id: "AC-QUINT-002-1", given: "同一のQuint要件仕様がある", when_: "生成を二回実行する", expected: "JSONとMarkdownがそれぞれバイト一致する" },
          { id: "AC-QUINT-002-2", given: "生成済みJSONを変更する", when_: "drift検査を実行する", expected: "Quint正本との差異として失敗する" },
          { id: "AC-QUINT-002-3", given: "全fieldに異なる値、空のretirement・classification field、順序の異なる複数要件を持つQuint fixtureがある", when_: "JSONとMarkdownを生成してJSONからQuint表現へ逆写像する", expected: "明示写像で全fieldとList順を保持して完全往復し、serialized JSONを再parseした値だけをMarkdownへ渡してGiven When Thenを含む意味を保持する" }
        ],
        verification: { method: "決定的生成とgolden mappingテスト", evidence: "全field oracle、serialized JSON境界、一時出力とcommitted JSON・Markdownのbyte比較" },
        traces: {
          design: ["docs/decisions/ADR-0004-quint-three-pillar-portability.md"],
          implementation: ["tools/quintflow.py", "tools/spec_mapping.py", "tools/render_requirements.py", ".agents/skills/maintain-canonical-requirements/scripts/specflow.py"],
          tests: ["tests/test_quintflow.py", "tests/test_specflow.py"],
          standards: ["QUINT-0.32"],
        },
        lastChangedBy: "CHG-20260829-review-remediation",
        retirementReason: "",
        supersededBy: "",
        scopeName: "product",
        categoryName: "functional",
      },
      {
        id: "REQ-QUINT-003",
        revision: 3,
        status: "active",
        kind: "quality",
        title: "全Skillの形式契約網羅",
        subject: "Skill形式仕様",
        actionName: "formalize",
        objectName: "すべてのSkillを一対一のQuint契約とactive要件の双方向traceへ対応付けること",
        rationale: "Skill追加時の形式仕様漏れ、削除後に残るstale契約、実装traceだけまたは自己申告requirement IDだけの片方向接続を機械検出する。",
        sourceRefs: ["user:2026-09-05", "user:2026-08-27", "user:2026-08-29", "https://quint.sh/docs/what-does-quint-do", "docs/decisions/ADR-0004-quint-three-pillar-portability.md"],
        acceptanceCriteria: [
          { id: "AC-QUINT-003-1", given: "Skill directoryとQuint契約catalogがある", when_: "形式契約検査を実行する", expected: "双方の名前集合が完全一致し、各SKILL.mdから契約へtraceできる" },
          { id: "AC-QUINT-003-2", given: "active要件がSkill pathをtraceするかSkill契約がrequirement IDを宣言する", when_: "trace整合検査を実行する", expected: "要件からSkill pathへの組とSkillからactive requirement IDへの組が完全一致し、未知またはretired IDを拒否する" },
          { id: "AC-QUINT-003-3", given: "Skillを実行時に読み込む", when_: "Quint契約のviewを生成する", expected: "入口には起動条件と実行境界と正本参照だけを表示し、詳細field・asset一覧・digestは生成catalogで保持する。簡略表示後も全field検査、digest照合、配布先drift検知を維持する" }
        ],
        verification: { method: "Quint testと双方向集合比較", evidence: "skills.qntのtest成功、Skill inventory、requirementIdsとactive要件Skill path traceの完全一致検査" },
        traces: {
          design: ["docs/decisions/ADR-0004-quint-three-pillar-portability.md"],
          implementation: ["spec/skills/skills.qnt", "tools/quintflow.py"],
          tests: ["tests/test_quintflow.py", "tests/test_skills.py"],
          standards: ["QUINT-0.32"],
        },
        lastChangedBy: "user:2026-09-05",
        retirementReason: "",
        supersededBy: "",
        scopeName: "project",
        categoryName: "nonfunctional",
      },
      {
        id: "REQ-REPO-001",
        revision: 3,
        status: "retired",
        kind: "constraint",
        title: "mainとdevの役割および統合方式",
        subject: "dev-standardのbranch運用",
        actionName: "enforce",
        objectName: "mainへのsquashとdevへのmerge commitを分離したbranch別統合契約",
        rationale: "利用者向けrelease履歴と到達可能なengineering履歴のauthorityを案件ごとのmerge判断に依存させないため。",
        sourceRefs: ["user:2026-07-24", "issue:#20", "docs/decisions/ADR-0002-two-layer-branch-history.md"],
        acceptanceCriteria: [
          { id: "AC-REPO-001-1", given: "trial phaseでmainまたはdevをbaseとするPull Requestがある", when_: "branch-policy checkを実行する", expected: "mainはrepositoryのdevまたはhotfixだけをsquashで受け入れ、devはtopic、main、またはhotfix競合を解消したreconcile branchだけをmerge commitで受け入れ、その他の方向を拒否する" },
          { id: "AC-REPO-001-2", given: "mainまたはdevへpushがある", when_: "push auditとGitHub rulesetを評価する", expected: "mainのlinear historyとdevの一回一merge commit更新を監査し、削除またはforce pushを許可しない" },
          { id: "AC-REPO-001-3", given: "branch policyがbootstrap phaseであり、dev、ruleset、required checks、PR移行、operator確認が完了している", when_: "trial phaseへ移行する", expected: "mainへのactivation PRでpolicyと対応するactive review YAMLだけを変更し、全Activation-Checkを一度ずつ記録した後、bootstrap reconciliationで同じpolicyとreviewをdevへ伝播する" },
          { id: "AC-REPO-001-4", given: "既存devがcurrent mainを祖先に持ち、両tip treeが一致し、まだbranch policyを含まない", when_: "二層branch契約をdev-firstでbootstrap導入する", expected: "Issue #20を参照する初回bootstrap PRだけをdevへmerge commitで統合し、同じtreeをRelease-Type bootstrapのdevからmainへのsquashで導入できるが、Issueをcloseせず2回の通常releaseへ数えない" }
        ],
        verification: { method: "CIとGitHub ruleset監査", evidence: "branch方向、merge parent、commit subject、protected branch設定のCI結果" },
        traces: {
          design: ["docs/decisions/ADR-0002-two-layer-branch-history.md", "docs/reference/development.md"],
          implementation: [],
          tests: [],
          standards: [],
        },
        lastChangedBy: "user:2026-08-29",
        retirementReason: "導入先へmerge方式やbranch構成を強制しない3本柱境界へ移行したため",
        supersededBy: "",
        scopeName: "project",
        categoryName: "nonfunctional",
      },
      {
        id: "REQ-REPO-002",
        revision: 3,
        status: "retired",
        kind: "operational",
        title: "release後の祖先関係とtreeを回復するreconciliation契約",
        subject: "release operatorとCI",
        actionName: "maintain",
        objectName: "release前後のancestor関係、tip tree条件、freezeを含むreconciliation transaction",
        rationale: "squashで記録されない祖先関係を回復し、既出file差分とconflictの再評価を防ぎながら詳細commitを保持するため。",
        sourceRefs: ["user:2026-07-24", "issue:#20", "Git FAQ: long-running squash merge", "docs/decisions/ADR-0002-two-layer-branch-history.md"],
        acceptanceCriteria: [
          { id: "AC-REPO-002-1", given: "devからmainへ通常releaseをsquash mergeした", when_: "release reconciliationを完了する", expected: "次のtopic統合前にmainをdevへmergeし、mainがdevの祖先であり両tip treeが一致する" },
          { id: "AC-REPO-002-2", given: "mainへhotfixをsquash mergeしdevに未release変更がある", when_: "hotfix reconciliationを完了する", expected: "conflict-freeならmainをdevへ直接mergeし、mainをdevの祖先にするが両tip treeの一致は要求しない" },
          { id: "AC-REPO-002-3", given: "通常releaseとreconciliationを2回行う", when_: "branch graph回帰testを実行する", expected: "前回release済みfile差分が次回release diffへ再出現せず、詳細commitはdevから到達可能なまま残る" },
          { id: "AC-REPO-002-4", given: "hotfix後のmainをdevへ直接mergeするとconflictする", when_: "hotfix conflict reconciliationを完了する", expected: "freeze中のdevからreconcile branchを作り、prior devとcurrent mainをparentに持つ解消mergeをdevへ統合し、outer merge treeとhotfix変更pathを保持してours相当の破棄を拒否する" }
        ],
        verification: { method: "branch graph回帰テストとCI", evidence: "一時Git repositoryのancestor、direct tree、three-dot diff、到達可能commitのassert" },
        traces: {
          design: ["docs/decisions/ADR-0002-two-layer-branch-history.md", "docs/reference/development.md"],
          implementation: [],
          tests: [],
          standards: [],
        },
        lastChangedBy: "user:2026-08-29",
        retirementReason: "repository固有のreconciliation契約を廃止し、GitHub標準設定へ委任したため",
        supersededBy: "",
        scopeName: "project",
        categoryName: "nonfunctional",
      },
      {
        id: "REQ-REPO-003",
        revision: 3,
        status: "retired",
        kind: "constraint",
        title: "試行範囲、非移植性、rollback",
        subject: "dev-standardの二層branch試行",
        actionName: "constrain",
        objectName: "2回のrelease cycleに限定しportable profileへ既定配布しない二層branch試行",
        rationale: "長寿命devは一般解ではなく、追加操作とGitHub上の非原子的なlock制約を受容できるrepositoryだけで評価すべきため。",
        sourceRefs: ["user:2026-07-24", "issue:#20", "docs/decisions/ADR-0002-two-layer-branch-history.md"],
        acceptanceCriteria: [
          { id: "AC-REPO-003-1", given: "二層branch契約のassetを配布profileへ追加しようとする", when_: "distribution contractを検査する", expected: "dev-standard固有のbranch policyとvalidatorをportable profileへ含めず、導入先の既定branch戦略を変更しない" },
          { id: "AC-REPO-003-2", given: "2回のrelease試行が完了していない、または昇格条件を満たさない", when_: "試行結果を判断する", expected: "恒久採用と一般化を行わず、必要時はdevへの新規統合を停止して同期済み状態で凍結する" },
          { id: "AC-REPO-003-3", given: "GitHub Actionsでmainとdevの状態を検査する", when_: "authority boundaryを確認する", expected: "required checkを原子的なcross-branch lockとは表明せず、単一operatorと明示freezeの限界を文書化する" },
          { id: "AC-REPO-003-4", given: "branch policyがbootstrap phaseである", when_: "二層branch試行を開始する", expected: "activation前に初回bootstrap導入以外のtopic mergeを拒否してbranch graph回帰testと外部GitHub設定を確認し、policyとactive reviewを両branchへ伝播した後の最初の小変更を1回目の管理されたdry runとして扱う" },
          { id: "AC-REPO-003-5", given: "二層branch試行を停止する", when_: "rollback transactionを完了する", expected: "policyと対応するactive review YAMLだけを変更するrollback hotfixをmainへsquashし、hotfix reconciliationでdevへ伝播した後にbootstrapで新規topic統合と通常releaseを停止する" },
          { id: "AC-REPO-003-6", given: "branch policyまたはreview validatorを変更するPull Requestまたはprotected branch pushがある", when_: "Governanceのevidenceまたはbranch-policy jobを実行する", expected: "利用可能な場合はPR baseまたはpush before側のvalidatorとdependencyで候補treeを検査し、候補validatorだけの自己緩和を当該判定へ使用しない" },
          { id: "AC-REPO-003-7", given: "Governance workflowを変更するPull Requestがある", when_: "CIの自己統制境界を評価する", expected: "workflow file自体をimmutableまたはtamper-proofとは表明せず、required checkのGitHub Actions由来sourceとworkflow差分を単一operatorが確認する" },
          { id: "AC-REPO-003-8", given: "既存の二層branch policyを変更するPull Requestまたはprotected branch pushがある", when_: "baseまたはbefore側policyと候補policyを比較する", expected: "2回の管理された試行中はtrial.phase以外のmachine contract変更を拒否し、契約変更は試行停止後の別判断として扱う" }
        ],
        verification: { method: "repository contract testと試行後review", evidence: "trial設定、base/before validator選択、workflow自己統制限界、distribution非包含、昇格条件とrollbackの契約テスト" },
        traces: {
          design: ["docs/decisions/ADR-0002-two-layer-branch-history.md"],
          implementation: [],
          tests: [],
          standards: [],
        },
        lastChangedBy: "user:2026-08-29",
        retirementReason: "二層branch試行を終了し、portable guardrailからrepository policyを除外したため",
        supersededBy: "",
        scopeName: "project",
        categoryName: "nonfunctional",
      },
      {
        id: "REQ-SKILL-001",
        revision: 1,
        status: "active",
        kind: "constraint",
        title: "right-size-executionのSkill境界",
        subject: "right-size-execution",
        actionName: "provide",
        objectName: "Estimate、ExecuteおよびExpandを一体化した再利用可能な実行制御契約",
        rationale: "Skill分割と既存工程責務の複製による選択・同期・contextコストを増やさないため。",
        sourceRefs: ["user:2026-07-18", "arXiv:2602.12670", "OpenAI:skills"],
        acceptanceCriteria: [
          { id: "AC-SKILL-001-1", given: "Skillを配布する", when_: "Skill構造を検査する", expected: "単一Skillが入力、出力、境界、判断規則、参照先、完了条件を持ち、要件管理、承認、標準合否、Git操作を複製しない" }
        ],
        verification: { method: "自動検査", evidence: "Skill構造と責務境界の契約テスト" },
        traces: {
          design: [".agents/skills/right-size-execution/SKILL.md"],
          implementation: [".agents/skills/right-size-execution/agents/openai.yaml"],
          tests: ["tests/test_skills.py"],
          standards: ["SWEBOK-V4A"],
        },
        lastChangedBy: "WI-20260718-right-size-execution-v2",
        retirementReason: "",
        supersededBy: "",
        scopeName: "",
        categoryName: "",
      },
      {
        id: "REQ-SKILL-002",
        revision: 1,
        status: "active",
        kind: "quality",
        title: "Skill制約のtrajectory検証",
        subject: "Skill検証基盤",
        actionName: "verify",
        objectName: "SKILL.mdの主要behavior constraintが代表trajectoryで実行された証拠",
        rationale: "テスト成功だけではSkill内の重要規則が実際に使われたことを保証できないため。",
        sourceRefs: ["user:2026-07-18", "arXiv:2606.20659"],
        acceptanceCriteria: [
          { id: "AC-SKILL-002-1", given: "機械可読なbehavior constraintがある", when_: "repository benchmarkを実行する", expected: "各constraintのconditionを発火させ、expected behaviorと実行証拠のcoverageを報告する" }
        ],
        verification: { method: "自動benchmark", evidence: "behavior constraint coverageと未実行constraint一覧" },
        traces: {
          design: [".agents/skills/right-size-execution/assets/behavior-constraints.json"],
          implementation: [".agents/skills/right-size-execution/scripts/executionflow.py"],
          tests: ["tests/test_executionflow.py"],
          standards: ["SWEBOK-V4A"],
        },
        lastChangedBy: "WI-20260718-right-size-execution-v2",
        retirementReason: "",
        supersededBy: "",
        scopeName: "",
        categoryName: "",
      },
      {
        id: "REQ-WORKBOOK-001",
        revision: 2,
        status: "active",
        kind: "operational",
        title: "再現可能で有界なワークブック",
        subject: "チェックリスト生成フロー",
        actionName: "generate",
        objectName: "実データ範囲だけを集計し決定的に再現できるレビュー用ワークブック",
        rationale: "Excel全行参照は読込時に過大なメモリを消費し、固定集計値は項目追加時に陳腐化する。",
        sourceRefs: ["user:2026-07-18"],
        acceptanceCriteria: [
          { id: "AC-WORKBOOK-001-1", given: "チェック項目の行数が変わる", when_: "ワークブックを再生成する", expected: "集計式が各シートの実データ最終行へ更新され、実数と一致し、全列参照を含まない" }
        ],
        verification: { method: "自動検査と描画確認", evidence: "数式範囲テスト、項目数照合、代表シートの描画結果" },
        traces: {
          design: ["docs/README.md"],
          implementation: ["update_checklist.py"],
          tests: ["tests/test_checklist.py"],
          standards: ["SWEBOK-V4A"],
        },
        lastChangedBy: "CHG-20260802-skills-audit-remediation",
        retirementReason: "",
        supersededBy: "",
        scopeName: "",
        categoryName: "",
      },
      {
        id: "REQ-ASBUILT-022",
        revision: 1,
        status: "active",
        kind: "quality",
        title: "APIの6帳票と要因別単体テストの完全対応",
        subject: "API設計generatorと導入完了検査",
        actionName: "generate",
        objectName: "全operationの詳細設計・interface・ログmessage・query・sequence・unit-test詳細",
        rationale: "ファイル存在や関数一覧だけではDB入出力・ログ・テスト要因が欠落しても完了になる。",
        sourceRefs: ["user:2026-09-06-api-six-documents", "https://github.com/tsuji-tomonori/rag-sample/tree/main/docs/spec/40.apis"],
        acceptanceCriteria: [
          { id: "AC-ASBUILT-022-1", given: "API実装とOpenAPIが存在する", when_: "生成と導入完了検査を実行する", expected: "全operationに6帳票があり、欠落・余剰operation・driftを拒否する" },
          { id: "AC-ASBUILT-022-2", given: "DBアクセス・ログを持つAPI", when_: "詳細設計・query・messagesを生成する", expected: "DB/tableの操作と入出力、SQL種別・概要・引数・戻り値・条件、ログlevel・本文・出力条件・項目が実装由来であり、未対応を非該当に偽装しない" },
          { id: "AC-ASBUILT-022-3", given: "認証・入力制約・分岐・例外から導出した必須要因と要素", when_: "unit-test詳細を生成する", expected: "具体的Given/When/Thenと期待ログ・DB状態を示し、全要因要素がケースと実在単体テストに対応する。欠落を拒否し、実行成功とassert妥当性は別途検証する" },
          { id: "AC-ASBUILT-022-4", given: "分岐と例外を持つAPI", when_: "interfaceとsequenceを生成する", expected: "Swagger互換OpenAPIと参照schemaを保持し、呼出元・API・DB等のMermaid図で実際の条件分岐・例外順序を示す。未対応構文はadapterで補完するまで未完了にする" }
        ],
        verification: { method: "自動テストとadapter内容レビュー", evidence: "6帳票生成、削除・source変更・要因欠落・test node欠落・operation追加の失敗fixture" },
        traces: {
          design: ["docs/standards/AS-BUILT-DESIGN.md", ".agents/skills/generate-implementation-design/references/api-documents.md"],
          implementation: [".agents/skills/generate-implementation-design/scripts/designflow.py", ".agents/skills/generate-implementation-design/scripts/check_design.py"],
          tests: ["tests/test_api_documents.py", "tests/test_design_adoption.py"],
          standards: ["DEVSTD-AS-BUILT"],
        },
        lastChangedBy: "CHG-20260906-api-six-documents",
        retirementReason: "",
        supersededBy: "",
        scopeName: "",
        categoryName: "",
      },
    ],
  }

  // Lifecycle actions below mutate a real Catalog value.  The Lifecycle record
  // is only a refinement witness; it may not advance independently of catalog.
  pure val lifecycleRequirement: Requirement = {
    id: "REQ-LIFECYCLE-MODEL-001",
    revision: 1,
    status: "active",
    kind: "functional",
    title: "lifecycle fixture",
    subject: "requirements lifecycle model",
    actionName: "maintain",
    objectName: "a typed catalog requirement",
    rationale: "A concrete item makes lifecycle refinement non-vacuous.",
    sourceRefs: ["model:requirements-lifecycle"],
    acceptanceCriteria: [
      { id: "AC-LIFECYCLE-MODEL-001-1", given: "a current catalog", when_: "a CAS transition is accepted", expected: "catalog and item revisions advance together" }
    ],
    verification: { method: "Quint model", evidence: "catalog lifecycle transition tests" },
    traces: {
      design: ["spec/requirements/requirements.qnt"],
      implementation: [],
      tests: [],
      standards: ["QUINT-0.32"],
    },
    lastChangedBy: "model:add",
    retirementReason: "",
    supersededBy: "",
    scopeName: "project",
    categoryName: "nonfunctional",
  }

  pure val successionR1: Requirement = lifecycleRequirement
    .with("id", "REQ-SUCCESSION-R1")
    .with("acceptanceCriteria", [
      { id: "AC-SUCCESSION-R1", given: "R1 exists", when_: "R1 is superseded", expected: "the chain advances" }
    ])
    .with("status", "retired")
    .with("retirementReason", "superseded by R2")
    .with("supersededBy", "REQ-SUCCESSION-R2")
  pure val successionR2: Requirement = lifecycleRequirement
    .with("id", "REQ-SUCCESSION-R2")
    .with("acceptanceCriteria", [
      { id: "AC-SUCCESSION-R2", given: "R2 exists", when_: "R2 is superseded", expected: "the chain advances" }
    ])
    .with("status", "retired")
    .with("retirementReason", "superseded by R3")
    .with("supersededBy", "REQ-SUCCESSION-R3")
  pure val successionR3: Requirement = lifecycleRequirement
    .with("id", "REQ-SUCCESSION-R3")
    .with("acceptanceCriteria", [
      { id: "AC-SUCCESSION-R3", given: "R3 exists", when_: "the chain terminates", expected: "R3 is active" }
    ])
  pure val successionCycleR2: Requirement = successionR2
    .with("supersededBy", "REQ-SUCCESSION-R1")
  pure val successionRetiredTerminalR2: Requirement = successionR2
    .with("supersededBy", "")
  pure val successionCatalog: Catalog = {
    schemaVersion: 1,
    catalogRevision: 1,
    product: "succession-contract",
    updatedAt: "succession:fixture",
    requirements: [successionR1, successionR2, successionR3],
  }

  pure val batchRequirement1: Requirement = lifecycleRequirement
    .with("id", "REQ-BATCH-1")
    .with("acceptanceCriteria", [
      { id: "AC-BATCH-1", given: "batch source", when_: "item one changes", expected: "revision advances once" }
    ])
  pure val batchRequirement2: Requirement = lifecycleRequirement
    .with("id", "REQ-BATCH-2")
    .with("acceptanceCriteria", [
      { id: "AC-BATCH-2", given: "batch source", when_: "item two changes", expected: "revision advances once" }
    ])
  pure val batchRequirement3: Requirement = lifecycleRequirement
    .with("id", "REQ-BATCH-3")
    .with("acceptanceCriteria", [
      { id: "AC-BATCH-3", given: "batch source", when_: "item three changes", expected: "revision advances once" }
    ])
  pure val batchBefore: Catalog = {
    schemaVersion: 1,
    catalogRevision: 5,
    product: "batch-contract",
    updatedAt: "batch:before",
    requirements: [batchRequirement1, batchRequirement2, batchRequirement3],
  }
  pure val batchAfterTwo: Catalog = batchBefore
    .with("catalogRevision", 6)
    .with("updatedAt", "batch:two")
    .with("requirements", [
      batchRequirement1
        .with("revision", 2)
        .with("title", "batch item one updated")
        .with("lastChangedBy", "batch:change"),
      batchRequirement2
        .with("revision", 2)
        .with("traces", batchRequirement2.traces.with("tests", ["tests/batch-two.py"]))
        .with("lastChangedBy", "batch:change"),
      batchRequirement3,
    ])
  pure val batchAfterThree: Catalog = batchBefore
    .with("catalogRevision", 6)
    .with("updatedAt", "batch:three")
    .with("requirements", [
      batchAfterTwo.requirements.nth(0),
      batchAfterTwo.requirements.nth(1),
      batchRequirement3
        .with("revision", 2)
        .with("status", "retired")
        .with("retirementReason", "batch retirement")
        .with("lastChangedBy", "batch:change"),
    ])
  pure val batchStaleAfter: Catalog = batchAfterTwo.with("requirements", [
    batchRequirement1,
    batchAfterTwo.requirements.nth(1),
    batchRequirement3,
  ])
  pure val batchPartialAfterStale: Catalog = batchBefore
    .with("catalogRevision", 6)
    .with("updatedAt", "batch:stale-after-valid")
    .with("requirements", [
      batchAfterTwo.requirements.nth(0),
      batchRequirement2,
      batchRequirement3,
    ])
  pure val batchInvalidAfter: Catalog = batchAfterTwo.with("requirements", [
    batchAfterTwo.requirements.nth(0).with("title", ""),
    batchAfterTwo.requirements.nth(1),
    batchRequirement3,
  ])
  pure val batchUpdateOperation: RequirementOperation = {
    kind: "update",
    id: "REQ-BATCH-1",
    expectedRevision: 1,
    replacement: batchAfterTwo.requirements.nth(0),
  }
  pure val batchTraceOperation: RequirementOperation = {
    kind: "trace",
    id: "REQ-BATCH-2",
    expectedRevision: 1,
    replacement: batchAfterTwo.requirements.nth(1),
  }
  pure val batchRetireOperation: RequirementOperation = {
    kind: "retire",
    id: "REQ-BATCH-3",
    expectedRevision: 1,
    replacement: batchAfterThree.requirements.nth(2),
  }
  pure val batchStaleOperation: RequirementOperation = batchUpdateOperation
    .with("expectedRevision", 0)
  pure val batchStaleTraceOperation: RequirementOperation = batchTraceOperation
    .with("expectedRevision", 0)
  pure val batchInvalidOperation: RequirementOperation = batchUpdateOperation
    .with("replacement", batchInvalidAfter.requirements.nth(0))
  pure val batchResurrectionOperation: RequirementOperation = {
    kind: "update",
    id: "REQ-BATCH-3",
    expectedRevision: 2,
    replacement: batchAfterThree.requirements.nth(2)
      .with("revision", 3)
      .with("status", "active")
      .with("retirementReason", "")
      .with("lastChangedBy", "batch:change"),
  }
  pure val batchResurrectedAfter: Catalog = batchAfterThree
    .with("catalogRevision", 7)
    .with("updatedAt", "batch:resurrection")
    .with("requirements", batchAfterThree.requirements.replaceAt(
      2,
      batchResurrectionOperation.replacement
    ))

  var catalog: Catalog
  var lifecycle: Lifecycle

  action init = all {
    catalog' = requirementsSource,
    lifecycle' = {
      catalogRevision: requirementsSource.catalogRevision,
      itemRevision: 0,
      itemPresent: false,
      itemStatus: "missing",
      traceRevision: 0,
      priorCatalogRevision: requirementsSource.catalogRevision,
      priorItemRevision: 0,
      priorItemPresent: false,
      priorItemStatus: "missing",
      priorTraceRevision: 0,
      lastOperation: "init",
    },
  }

  action addRequirementAt(expectedCatalogRevision: int): bool = all {
    expectedCatalogRevision == catalog.catalogRevision,
    lifecycle.catalogRevision == expectedCatalogRevision,
    not(lifecycle.itemPresent),
    catalog.requirements.indices().forall(i =>
      catalog.requirements.nth(i).id != lifecycleRequirement.id
    ),
    catalog' = catalog
      .with("catalogRevision", catalog.catalogRevision + 1)
      .with("requirements", catalog.requirements.append(lifecycleRequirement)),
    lifecycle' = {
      catalogRevision: lifecycle.catalogRevision + 1,
      itemRevision: 1,
      itemPresent: true,
      itemStatus: "active",
      traceRevision: 0,
      priorCatalogRevision: lifecycle.catalogRevision,
      priorItemRevision: lifecycle.itemRevision,
      priorItemPresent: lifecycle.itemPresent,
      priorItemStatus: lifecycle.itemStatus,
      priorTraceRevision: lifecycle.traceRevision,
      lastOperation: "add",
    },
  }

  action addRequirement = addRequirementAt(lifecycle.catalogRevision)

  def updateRequirementIsAllowed(expectedCatalogRevision: int, expectedItemRevision: int): bool =
    all {
      lifecycle.itemPresent,
      lifecycle.itemStatus == "active",
      expectedCatalogRevision == catalog.catalogRevision,
      expectedCatalogRevision == lifecycle.catalogRevision,
      expectedItemRevision == lifecycle.itemRevision,
      catalog.requirements.nth(catalog.requirements.length() - 1).id == lifecycleRequirement.id,
      catalog.requirements.nth(catalog.requirements.length() - 1).revision == expectedItemRevision,
      catalog.requirements.nth(catalog.requirements.length() - 1).status == "active",
      catalog.requirements.nth(catalog.requirements.length() - 1).title != "lifecycle fixture updated",
    }

  action updateRequirementAt(expectedCatalogRevision: int, expectedItemRevision: int): bool = all {
    updateRequirementIsAllowed(expectedCatalogRevision, expectedItemRevision),
    catalog' = catalog
      .with("catalogRevision", catalog.catalogRevision + 1)
      .with(
        "requirements",
        catalog.requirements.replaceAt(
          catalog.requirements.length() - 1,
          catalog.requirements.nth(catalog.requirements.length() - 1)
            .with("revision", expectedItemRevision + 1)
            .with("title", "lifecycle fixture updated")
            .with("lastChangedBy", "model:update")
        )
      ),
    lifecycle' = {
      catalogRevision: lifecycle.catalogRevision + 1,
      itemRevision: lifecycle.itemRevision + 1,
      itemPresent: true,
      itemStatus: "active",
      traceRevision: lifecycle.traceRevision,
      priorCatalogRevision: lifecycle.catalogRevision,
      priorItemRevision: lifecycle.itemRevision,
      priorItemPresent: lifecycle.itemPresent,
      priorItemStatus: lifecycle.itemStatus,
      priorTraceRevision: lifecycle.traceRevision,
      lastOperation: "update",
    },
  }

  action updateRequirement = updateRequirementAt(lifecycle.catalogRevision, lifecycle.itemRevision)

  def traceUpdateIsAllowed(expectedCatalogRevision: int, expectedItemRevision: int): bool =
    all {
      lifecycle.itemPresent,
      lifecycle.itemStatus == "active",
      lifecycle.traceRevision == 0,
      expectedCatalogRevision == catalog.catalogRevision,
      expectedCatalogRevision == lifecycle.catalogRevision,
      expectedItemRevision == lifecycle.itemRevision,
      catalog.requirements.nth(catalog.requirements.length() - 1).id == lifecycleRequirement.id,
      catalog.requirements.nth(catalog.requirements.length() - 1).revision == expectedItemRevision,
      catalog.requirements.nth(catalog.requirements.length() - 1).status == "active",
    }

  action updateRequirementTraceAt(expectedCatalogRevision: int, expectedItemRevision: int): bool = all {
    traceUpdateIsAllowed(expectedCatalogRevision, expectedItemRevision),
    catalog' = catalog
      .with("catalogRevision", catalog.catalogRevision + 1)
      .with(
        "requirements",
        catalog.requirements.replaceAt(
          catalog.requirements.length() - 1,
          catalog.requirements.nth(catalog.requirements.length() - 1)
            .with("revision", expectedItemRevision + 1)
            .with(
              "traces",
              catalog.requirements.nth(catalog.requirements.length() - 1).traces.with(
                "tests",
                catalog.requirements.nth(catalog.requirements.length() - 1).traces.tests
                  .append("tests/model-trace-update.py")
              )
            )
            .with("lastChangedBy", "model:trace-update")
        )
      ),
    lifecycle' = {
      catalogRevision: lifecycle.catalogRevision + 1,
      itemRevision: lifecycle.itemRevision + 1,
      itemPresent: true,
      itemStatus: "active",
      traceRevision: lifecycle.traceRevision + 1,
      priorCatalogRevision: lifecycle.catalogRevision,
      priorItemRevision: lifecycle.itemRevision,
      priorItemPresent: lifecycle.itemPresent,
      priorItemStatus: lifecycle.itemStatus,
      priorTraceRevision: lifecycle.traceRevision,
      lastOperation: "trace-update",
    },
  }

  action updateRequirementTrace =
    updateRequirementTraceAt(lifecycle.catalogRevision, lifecycle.itemRevision)

  def retirementIsAllowed(expectedCatalogRevision: int, expectedItemRevision: int): bool =
    all {
      lifecycle.itemPresent,
      lifecycle.itemStatus == "active",
      expectedCatalogRevision == catalog.catalogRevision,
      expectedCatalogRevision == lifecycle.catalogRevision,
      expectedItemRevision == lifecycle.itemRevision,
      catalog.requirements.nth(catalog.requirements.length() - 1).id == lifecycleRequirement.id,
      catalog.requirements.nth(catalog.requirements.length() - 1).revision == expectedItemRevision,
      catalog.requirements.nth(catalog.requirements.length() - 1).status == "active",
    }

  action retireRequirementAt(expectedCatalogRevision: int, expectedItemRevision: int): bool = all {
    retirementIsAllowed(expectedCatalogRevision, expectedItemRevision),
    catalog' = catalog
      .with("catalogRevision", catalog.catalogRevision + 1)
      .with(
        "requirements",
        catalog.requirements.replaceAt(
          catalog.requirements.length() - 1,
          catalog.requirements.nth(catalog.requirements.length() - 1)
            .with("revision", expectedItemRevision + 1)
            .with("status", "retired")
            .with("retirementReason", "model retirement")
            .with("lastChangedBy", "model:retire")
        )
      ),
    lifecycle' = {
      catalogRevision: lifecycle.catalogRevision + 1,
      itemRevision: lifecycle.itemRevision + 1,
      itemPresent: true,
      itemStatus: "retired",
      traceRevision: lifecycle.traceRevision,
      priorCatalogRevision: lifecycle.catalogRevision,
      priorItemRevision: lifecycle.itemRevision,
      priorItemPresent: lifecycle.itemPresent,
      priorItemStatus: lifecycle.itemStatus,
      priorTraceRevision: lifecycle.traceRevision,
      lastOperation: "retire",
    },
  }

  action retireRequirement = retireRequirementAt(lifecycle.catalogRevision, lifecycle.itemRevision)

  action lifecycleStutter = all {
    catalog' = catalog,
    lifecycle' = {
      catalogRevision: lifecycle.catalogRevision,
      itemRevision: lifecycle.itemRevision,
      itemPresent: lifecycle.itemPresent,
      itemStatus: lifecycle.itemStatus,
      traceRevision: lifecycle.traceRevision,
      priorCatalogRevision: lifecycle.catalogRevision,
      priorItemRevision: lifecycle.itemRevision,
      priorItemPresent: lifecycle.itemPresent,
      priorItemStatus: lifecycle.itemStatus,
      priorTraceRevision: lifecycle.traceRevision,
      lastOperation: "none",
    },
  }

  // Negative-model action: if only the witness counter moved, refinement must
  // detect that no corresponding Catalog transition occurred.
  action counterOnlyMutation = all {
    catalog' = catalog,
    lifecycle' = lifecycle.with("catalogRevision", lifecycle.catalogRevision + 1),
  }

  action step = any {
    addRequirement,
    updateRequirement,
    updateRequirementTrace,
    retireRequirement,
    lifecycleStutter,
  }

  pure val allowedStatuses = Set("active", "retired")
  pure val allowedKinds = Set("functional", "quality", "constraint", "interface", "data", "operational")
  pure val allowedScopes = Set("product", "project")
  pure val allowedCategories = Set("functional", "nonfunctional")
  pure val allowedActions = Set(
    "constrain", "derive", "detect", "discover", "enable", "enforce", "estimate",
    "expand", "formalize", "generate", "maintain", "measure", "parse", "preserve",
    "provide", "route", "select", "separate", "stage", "stop", "structure", "validate", "verify"
  )

  pure def stringsAreUnique(values: List[str]): bool = values.indices().forall(i =>
    values.indices().forall(j => i == j or values.nth(i) != values.nth(j))
  )

  pure def stringsAreNonempty(values: List[str]): bool =
    values.indices().forall(i => values.nth(i) != "")

  pure def requirementIdsAreUniqueIn(requirements: List[Requirement]): bool =
    requirements.indices().forall(i =>
      requirements.indices().forall(j =>
        i == j or requirements.nth(i).id != requirements.nth(j).id
      )
    )

  val requirementIdsAreUnique = requirementIdsAreUniqueIn(catalog.requirements)

  // 構造的完全性は機械検査する。1 IDが意味的に1義務だけを表すかは、
  // 自然言語を解釈できる権限あるhuman semantic reviewの責務である。
  pure def requirementsAreStructurallyCompleteIn(requirements: List[Requirement]): bool =
    requirements.indices().forall(i => all {
      requirements.nth(i).id != "",
      requirements.nth(i).revision >= 1,
      requirements.nth(i).title != "",
      requirements.nth(i).subject != "",
      requirements.nth(i).actionName != "",
      requirements.nth(i).objectName != "",
      requirements.nth(i).rationale != "",
      requirements.nth(i).lastChangedBy != "",
      requirements.nth(i).sourceRefs.length() > 0,
      stringsAreNonempty(requirements.nth(i).sourceRefs),
      stringsAreUnique(requirements.nth(i).sourceRefs),
      requirements.nth(i).acceptanceCriteria.length() > 0,
      requirements.nth(i).verification.method != "",
      requirements.nth(i).verification.evidence != "",
    })

  val requirementsAreStructurallyComplete =
    requirementsAreStructurallyCompleteIn(catalog.requirements)

  pure def requirementsAreTypedIn(requirements: List[Requirement]): bool =
    requirements.indices().forall(i => all {
      allowedStatuses.contains(requirements.nth(i).status),
      allowedKinds.contains(requirements.nth(i).kind),
      allowedActions.contains(requirements.nth(i).actionName),
      (requirements.nth(i).scopeName == "").or(allowedScopes.contains(requirements.nth(i).scopeName)),
      (requirements.nth(i).categoryName == "").or(allowedCategories.contains(requirements.nth(i).categoryName)),
    })

  val requirementsAreTyped = requirementsAreTypedIn(catalog.requirements)

  pure def acceptanceCriteriaAreCompleteIn(requirements: List[Requirement]): bool =
    requirements.indices().forall(i =>
      requirements.nth(i).acceptanceCriteria.indices().forall(j => all {
        requirements.nth(i).acceptanceCriteria.nth(j).id != "",
        requirements.nth(i).acceptanceCriteria.nth(j).given != "",
        requirements.nth(i).acceptanceCriteria.nth(j).when_ != "",
        requirements.nth(i).acceptanceCriteria.nth(j).expected != "",
      })
    )

  val acceptanceCriteriaAreComplete =
    acceptanceCriteriaAreCompleteIn(catalog.requirements)

  pure def acceptanceCriterionIdsAreUniqueIn(requirements: List[Requirement]): bool =
    requirements.indices().forall(i =>
      requirements.indices().forall(j =>
        requirements.nth(i).acceptanceCriteria.indices().forall(x =>
          requirements.nth(j).acceptanceCriteria.indices().forall(y =>
          (i == j and x == y) or
            requirements.nth(i).acceptanceCriteria.nth(x).id !=
              requirements.nth(j).acceptanceCriteria.nth(y).id
          )
        )
      )
    )

  val acceptanceCriterionIdsAreUnique =
    acceptanceCriterionIdsAreUniqueIn(catalog.requirements)

  pure def traceLinksAreUniqueIn(requirements: List[Requirement]): bool =
    requirements.indices().forall(i => all {
      stringsAreNonempty(requirements.nth(i).traces.design),
      stringsAreNonempty(requirements.nth(i).traces.implementation),
      stringsAreNonempty(requirements.nth(i).traces.tests),
      stringsAreNonempty(requirements.nth(i).traces.standards),
      stringsAreUnique(requirements.nth(i).traces.design),
      stringsAreUnique(requirements.nth(i).traces.implementation),
      stringsAreUnique(requirements.nth(i).traces.tests),
      stringsAreUnique(requirements.nth(i).traces.standards),
    })

  val traceLinksAreUnique = traceLinksAreUniqueIn(catalog.requirements)

  pure def classificationIsPairedIn(requirements: List[Requirement]): bool =
    requirements.indices().forall(i =>
      (requirements.nth(i).scopeName == "") iff
      (requirements.nth(i).categoryName == "")
    )

  val classificationIsPaired = classificationIsPairedIn(catalog.requirements)

  pure def retirementFieldsAreConsistentIn(requirements: List[Requirement]): bool =
    requirements.indices().forall(i => all {
    (requirements.nth(i).status == "active").implies(all {
      requirements.nth(i).retirementReason == "",
      requirements.nth(i).supersededBy == "",
    }),
    (requirements.nth(i).status == "retired").implies(
      requirements.nth(i).retirementReason != ""
    ),
    (requirements.nth(i).supersededBy != "").implies(all {
      requirements.nth(i).status == "retired",
      requirements.nth(i).supersededBy != requirements.nth(i).id,
    }),
  })

  val retirementFieldsAreConsistent =
    retirementFieldsAreConsistentIn(catalog.requirements)

  pure def supersessionChainsAreValid(requirements: List[Requirement]): bool =
    requirements.indices().forall(i =>
      (requirements.nth(i).supersededBy != "").implies(
        requirements.indices().exists(j => all {
          j > i,
          requirements.nth(j).id == requirements.nth(i).supersededBy,
          requirements.nth(j).id != requirements.nth(i).id,
          (requirements.nth(j).status == "active").or(all {
            requirements.nth(j).status == "retired",
            requirements.nth(j).supersededBy != "",
          }),
        })
      )
    )

  pure def catalogHeaderIsValid(source: Catalog): bool = all {
    source.schemaVersion == 1,
    source.catalogRevision >= 1,
    source.product != "",
    source.updatedAt != "",
    source.requirements.length() > 0,
  }

  // Pure catalog component of catalogWellFormed. Lifecycle witness refinement
  // remains a state invariant below and is intentionally not fabricated for a
  // caller-supplied batch result.
  pure def catalogDataWellFormed(source: Catalog): bool = all {
    catalogHeaderIsValid(source),
    requirementIdsAreUniqueIn(source.requirements),
    requirementsAreStructurallyCompleteIn(source.requirements),
    requirementsAreTypedIn(source.requirements),
    acceptanceCriteriaAreCompleteIn(source.requirements),
    acceptanceCriterionIdsAreUniqueIn(source.requirements),
    traceLinksAreUniqueIn(source.requirements),
    classificationIsPairedIn(source.requirements),
    retirementFieldsAreConsistentIn(source.requirements),
    supersessionChainsAreValid(source.requirements),
  }

  pure def stringsContain(values: List[str], value: str): bool =
    values.indices().exists(i => values.nth(i) == value)

  pure def requirementExists(requirements: List[Requirement], id: str): bool =
    requirements.indices().exists(i => requirements.nth(i).id == id)

  pure def requirementById(requirements: List[Requirement], id: str): Requirement =
    requirements.select(requirement => requirement.id == id).head()

  pure def replaceRequirement(
    requirements: List[Requirement],
    id: str,
    replacement: Requirement,
  ): List[Requirement] =
    range(0, requirements.length()).foldl(requirements, (result, index) =>
      if (result.nth(index).id == id)
        result.replaceAt(index, replacement)
      else
        result
    )

  pure def updateReplacementIsValid(
    current: Requirement,
    replacement: Requirement,
    changeId: str,
  ): bool = all {
    current.status == "active",
    replacement == current
      .with("revision", current.revision + 1)
      .with("kind", replacement.kind)
      .with("title", replacement.title)
      .with("subject", replacement.subject)
      .with("actionName", replacement.actionName)
      .with("objectName", replacement.objectName)
      .with("rationale", replacement.rationale)
      .with("sourceRefs", replacement.sourceRefs)
      .with("acceptanceCriteria", replacement.acceptanceCriteria)
      .with("verification", replacement.verification)
      .with("scopeName", replacement.scopeName)
      .with("categoryName", replacement.categoryName)
      .with("lastChangedBy", changeId),
    replacement
      .with("revision", current.revision)
      .with("lastChangedBy", current.lastChangedBy) != current,
  }

  pure def traceReplacementIsValid(
    current: Requirement,
    replacement: Requirement,
    changeId: str,
  ): bool = all {
    current.status == "active",
    replacement.traces != current.traces,
    replacement == current
      .with("revision", current.revision + 1)
      .with("traces", replacement.traces)
      .with("lastChangedBy", changeId),
  }

  pure def retirementReplacementIsValid(
    current: Requirement,
    replacement: Requirement,
    changeId: str,
  ): bool = all {
    current.status == "active",
    replacement.retirementReason != "",
    replacement == current
      .with("revision", current.revision + 1)
      .with("status", "retired")
      .with("retirementReason", replacement.retirementReason)
      .with("supersededBy", replacement.supersededBy)
      .with("lastChangedBy", changeId),
  }

  pure def batchOperationIsAllowed(
    accumulator: BatchFold,
    operation: RequirementOperation,
    changeId: str,
  ): bool =
    if (not(accumulator.valid)) false
    else if (stringsContain(accumulator.touchedIds, operation.id)) false
    else if (operation.kind == "add") all {
      not(requirementExists(accumulator.requirements, operation.id)),
      operation.expectedRevision == 0,
      operation.id == operation.replacement.id,
      operation.replacement.revision == 1,
      operation.replacement.status == "active",
      operation.replacement.retirementReason == "",
      operation.replacement.supersededBy == "",
      operation.replacement.lastChangedBy == changeId,
    }
    else if (not(requirementExists(accumulator.requirements, operation.id))) false
    else if (
      operation.expectedRevision !=
        requirementById(accumulator.requirements, operation.id).revision
    ) false
    else if (operation.kind == "update") updateReplacementIsValid(
      requirementById(accumulator.requirements, operation.id),
      operation.replacement,
      changeId
    )
    else if (operation.kind == "trace") traceReplacementIsValid(
      requirementById(accumulator.requirements, operation.id),
      operation.replacement,
      changeId
    )
    else if (operation.kind == "retire") retirementReplacementIsValid(
      requirementById(accumulator.requirements, operation.id),
      operation.replacement,
      changeId
    )
    else false

  pure def applyBatchOperation(
    accumulator: BatchFold,
    operation: RequirementOperation,
    changeId: str,
  ): BatchFold =
    if (batchOperationIsAllowed(accumulator, operation, changeId)) {
      requirements:
        if (operation.kind == "add")
          accumulator.requirements.append(operation.replacement)
        else
          replaceRequirement(accumulator.requirements, operation.id, operation.replacement),
      touchedIds: accumulator.touchedIds.append(operation.id),
      valid: true,
    } else accumulator.with("valid", false)

  pure def initialBatchFold(before: Catalog): BatchFold = {
    requirements: before.requirements,
    touchedIds: [],
    valid: true,
  }

  pure def foldBatchOperations(
    before: Catalog,
    operations: List[RequirementOperation],
    changeId: str,
  ): BatchFold = operations.foldl(
    initialBatchFold(before),
    (accumulator, operation) => applyBatchOperation(accumulator, operation, changeId)
  )

  pure def batchCandidate(
    before: Catalog,
    operations: List[RequirementOperation],
    changedAt: str,
    changeId: str,
  ): Catalog = before
    .with("catalogRevision", before.catalogRevision + 1)
    .with("updatedAt", changedAt)
    .with("requirements", foldBatchOperations(before, operations, changeId).requirements)

  pure def batchWouldBeAccepted(
    before: Catalog,
    expectedCatalogRevision: int,
    operations: List[RequirementOperation],
    changedAt: str,
    changeId: str,
  ): bool = all {
    expectedCatalogRevision == before.catalogRevision,
    operations.length() > 0,
    changedAt != "",
    changeId != "",
    foldBatchOperations(before, operations, changeId).valid,
    catalogDataWellFormed(batchCandidate(before, operations, changedAt, changeId)),
  }

  // This relation models the same arbitrary-length operation fold and CAS
  // boundary as specflow.apply_change. No operation may resurrect a retired
  // item, and any stale or invalid member makes the entire batch stutter.
  pure def atomicBatchTransitionIsValid(
    before: Catalog,
    after: Catalog,
    expectedCatalogRevision: int,
    operations: List[RequirementOperation],
    changedAt: str,
    changeId: str,
    outcome: str,
  ): bool = all {
    Set("accepted", "rejected").contains(outcome),
    catalogDataWellFormed(before),
    (outcome == "accepted") iff batchWouldBeAccepted(
      before, expectedCatalogRevision, operations, changedAt, changeId
    ),
    (outcome == "accepted").implies(
      after == batchCandidate(before, operations, changedAt, changeId)
    ),
    (outcome == "rejected").implies(after == before),
  }

  val lifecycleRefinesCatalog = all {
    lifecycle.catalogRevision == catalog.catalogRevision,
    lifecycle.itemPresent iff
      catalog.requirements.indices().exists(i =>
        catalog.requirements.nth(i).id == lifecycleRequirement.id
      ),
    lifecycle.itemPresent.implies(all {
      catalog.requirements.nth(catalog.requirements.length() - 1).id == lifecycleRequirement.id,
      catalog.requirements.nth(catalog.requirements.length() - 1).revision == lifecycle.itemRevision,
      catalog.requirements.nth(catalog.requirements.length() - 1).status == lifecycle.itemStatus,
      (lifecycle.traceRevision == 0).implies(
        catalog.requirements.nth(catalog.requirements.length() - 1).traces.tests ==
          lifecycleRequirement.traces.tests
      ),
      (lifecycle.traceRevision == 1).implies(
        catalog.requirements.nth(catalog.requirements.length() - 1).traces.tests ==
          lifecycleRequirement.traces.tests.append("tests/model-trace-update.py")
      ),
    }),
  }

  val lifecycleRevisionTransitionIsSound = all {
    Set("init", "add", "update", "trace-update", "retire", "none").contains(lifecycle.lastOperation),
    (lifecycle.lastOperation == "init").implies(all {
      lifecycle.catalogRevision == requirementsSource.catalogRevision,
      lifecycle.itemRevision == 0,
      not(lifecycle.itemPresent),
    }),
    (lifecycle.lastOperation == "add").implies(all {
      not(lifecycle.priorItemPresent),
      lifecycle.itemPresent,
      lifecycle.itemStatus == "active",
      lifecycle.catalogRevision == lifecycle.priorCatalogRevision + 1,
      lifecycle.itemRevision == 1,
    }),
    (lifecycle.lastOperation == "update").implies(all {
      lifecycle.priorItemPresent,
      lifecycle.priorItemStatus == "active",
      lifecycle.itemStatus == "active",
      lifecycle.catalogRevision == lifecycle.priorCatalogRevision + 1,
      lifecycle.itemRevision == lifecycle.priorItemRevision + 1,
      lifecycle.traceRevision == lifecycle.priorTraceRevision,
    }),
    (lifecycle.lastOperation == "trace-update").implies(all {
      lifecycle.priorItemPresent,
      lifecycle.priorItemStatus == "active",
      lifecycle.itemStatus == "active",
      lifecycle.catalogRevision == lifecycle.priorCatalogRevision + 1,
      lifecycle.itemRevision == lifecycle.priorItemRevision + 1,
      lifecycle.traceRevision == lifecycle.priorTraceRevision + 1,
    }),
    (lifecycle.lastOperation == "retire").implies(all {
      lifecycle.priorItemPresent,
      lifecycle.priorItemStatus == "active",
      lifecycle.itemPresent,
      lifecycle.itemStatus == "retired",
      lifecycle.catalogRevision == lifecycle.priorCatalogRevision + 1,
      lifecycle.itemRevision == lifecycle.priorItemRevision + 1,
      lifecycle.traceRevision == lifecycle.priorTraceRevision,
    }),
    (lifecycle.lastOperation == "none").implies(all {
      lifecycle.catalogRevision == lifecycle.priorCatalogRevision,
      lifecycle.itemRevision == lifecycle.priorItemRevision,
      lifecycle.itemPresent == lifecycle.priorItemPresent,
      lifecycle.itemStatus == lifecycle.priorItemStatus,
      lifecycle.traceRevision == lifecycle.priorTraceRevision,
    }),
  }

  val catalogWellFormed = all {
    catalogDataWellFormed(catalog),
    lifecycleRevisionTransitionIsSound,
    lifecycleRefinesCatalog,
  }

  run catalogContractTest = {
    init.then(all {
      assert(catalogWellFormed),
      catalog' = catalog,
      lifecycle' = lifecycle,
    })
  }

  run catalogAndSupersessionMutationRejectionTest = {
    init.then(all {
      assert(not(catalogHeaderIsValid(catalog.with("requirements", [])))),
      assert(catalogDataWellFormed(successionCatalog)),
      assert(supersessionChainsAreValid([successionR1, successionR2, successionR3])),
      assert(not(catalogDataWellFormed(successionCatalog.with("requirements", [successionR1])))),
      assert(not(catalogDataWellFormed(successionCatalog.with("requirements", [successionR1, successionRetiredTerminalR2])))),
      assert(not(catalogDataWellFormed(successionCatalog.with("requirements", [successionR1, successionCycleR2])))),
      assert(not(supersessionChainsAreValid([successionR1]))),
      assert(not(supersessionChainsAreValid([successionR1, successionRetiredTerminalR2]))),
      assert(not(supersessionChainsAreValid([successionR1, successionCycleR2]))),
      catalog' = catalog,
      lifecycle' = lifecycle,
    })
  }

  run atomicBatchTransitionContractTest = {
    init.then(all {
      assert(atomicBatchTransitionIsValid(batchBefore, batchAfterTwo, 5, [batchUpdateOperation, batchTraceOperation], "batch:two", "batch:change", "accepted")),
      assert(atomicBatchTransitionIsValid(batchBefore, batchAfterThree, 5, [batchUpdateOperation, batchTraceOperation, batchRetireOperation], "batch:three", "batch:change", "accepted")),
      assert(atomicBatchTransitionIsValid(batchBefore, batchBefore, 4, [batchUpdateOperation], "batch:stale-catalog", "batch:change", "rejected")),
      assert(atomicBatchTransitionIsValid(batchBefore, batchBefore, 5, [batchStaleOperation], "batch:stale-item", "batch:change", "rejected")),
      assert(atomicBatchTransitionIsValid(batchBefore, batchBefore, 5, [batchUpdateOperation, batchStaleTraceOperation], "batch:stale-after-valid", "batch:change", "rejected")),
      assert(not(atomicBatchTransitionIsValid(batchBefore, batchPartialAfterStale, 5, [batchUpdateOperation, batchStaleTraceOperation], "batch:stale-after-valid", "batch:change", "accepted"))),
      assert(atomicBatchTransitionIsValid(batchBefore, batchBefore, 5, [batchUpdateOperation, batchUpdateOperation], "batch:duplicate", "batch:change", "rejected")),
      assert(atomicBatchTransitionIsValid(batchBefore, batchBefore, 5, [batchInvalidOperation], "batch:invalid", "batch:change", "rejected")),
      assert(not(atomicBatchTransitionIsValid(batchBefore, batchInvalidAfter, 5, [batchInvalidOperation], "batch:invalid", "batch:change", "accepted"))),
      assert(catalogDataWellFormed(batchResurrectedAfter)),
      assert(atomicBatchTransitionIsValid(batchAfterThree, batchAfterThree, 6, [batchResurrectionOperation], "batch:resurrection", "batch:change", "rejected")),
      assert(not(atomicBatchTransitionIsValid(batchAfterThree, batchResurrectedAfter, 6, [batchResurrectionOperation], "batch:resurrection", "batch:change", "accepted"))),
      catalog' = catalog,
      lifecycle' = lifecycle,
    })
  }

  run lifecycleTransitionContractTest = {
    init
      .then(addRequirement)
      .then(updateRequirement)
      .then(updateRequirementTrace)
      .then(retireRequirement)
      .then(all {
        assert(lifecycleRevisionTransitionIsSound),
        assert(lifecycleRefinesCatalog),
        assert(catalogWellFormed),
        catalog' = catalog,
        lifecycle' = lifecycle,
      })
  }

  run lifecycleCasAndRetiredUpdateRejectionTest = {
    init
      .then(addRequirement)
      .then(all {
        assert(not(updateRequirementIsAllowed(catalog.catalogRevision - 1, lifecycle.itemRevision))),
        assert(not(updateRequirementIsAllowed(catalog.catalogRevision, lifecycle.itemRevision - 1))),
        catalog' = catalog,
        lifecycle' = lifecycle,
      })
      .then(retireRequirement)
      .then(all {
        assert(not(updateRequirementIsAllowed(catalog.catalogRevision, lifecycle.itemRevision))),
        assert(not(traceUpdateIsAllowed(catalog.catalogRevision, lifecycle.itemRevision))),
        assert(not(retirementIsAllowed(catalog.catalogRevision, lifecycle.itemRevision))),
        catalog' = catalog,
        lifecycle' = lifecycle,
      })
  }

  run refinementRejectsCounterOnlyMutationTest = {
    init
      .then(counterOnlyMutation)
      .then(all {
        assert(not(lifecycleRefinesCatalog)),
        catalog' = catalog,
        lifecycle' = lifecycle,
      })
  }
}
