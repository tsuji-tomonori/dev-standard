module requirements_mapping {
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

  pure val fixture: Catalog = {
    schemaVersion: 1,
    catalogRevision: 9,
    product: "mapping-fixture",
    updatedAt: "2026-08-29",
    requirements: [
      {
        id: "REQ-Z-001",
        revision: 7,
        status: "active",
        kind: "functional",
        title: "title-REQ-Z-001",
        subject: "subject-REQ-Z-001",
        actionName: "generate",
        objectName: "object-REQ-Z-001",
        rationale: "rationale-REQ-Z-001",
        sourceRefs: ["source-b-REQ-Z-001", "source-a-REQ-Z-001"],
        acceptanceCriteria: [
          { id: "AC-REQ-Z-001-2", given: "given-2", when_: "when-2", expected: "then-2" },
          { id: "AC-REQ-Z-001-1", given: "given-1", when_: "when-1", expected: "then-1" }
        ],
        verification: { method: "method-REQ-Z-001", evidence: "evidence-REQ-Z-001" },
        traces: {
          design: ["design-b-REQ-Z-001", "design-a-REQ-Z-001"],
          implementation: ["implementation-b-REQ-Z-001", "implementation-a-REQ-Z-001"],
          tests: ["tests-b-REQ-Z-001", "tests-a-REQ-Z-001"],
          standards: ["standard-b-REQ-Z-001", "standard-a-REQ-Z-001"],
        },
        lastChangedBy: "change-REQ-Z-001",
        retirementReason: "",
        supersededBy: "",
        scopeName: "",
        categoryName: "",
      },
      {
        id: "REQ-A-001",
        revision: 7,
        status: "retired",
        kind: "functional",
        title: "title-REQ-A-001",
        subject: "subject-REQ-A-001",
        actionName: "generate",
        objectName: "object-REQ-A-001",
        rationale: "rationale-REQ-A-001",
        sourceRefs: ["source-b-REQ-A-001", "source-a-REQ-A-001"],
        acceptanceCriteria: [
          { id: "AC-REQ-A-001-2", given: "given-2", when_: "when-2", expected: "then-2" },
          { id: "AC-REQ-A-001-1", given: "given-1", when_: "when-1", expected: "then-1" }
        ],
        verification: { method: "method-REQ-A-001", evidence: "evidence-REQ-A-001" },
        traces: {
          design: ["design-b-REQ-A-001", "design-a-REQ-A-001"],
          implementation: ["implementation-b-REQ-A-001", "implementation-a-REQ-A-001"],
          tests: ["tests-b-REQ-A-001", "tests-a-REQ-A-001"],
          standards: ["standard-b-REQ-A-001", "standard-a-REQ-A-001"],
        },
        lastChangedBy: "change-REQ-A-001",
        retirementReason: "retired-REQ-A-001",
        supersededBy: "",
        scopeName: "project",
        categoryName: "nonfunctional",
      }
    ],
  }

  var catalog: Catalog
  action init = catalog' = fixture
  action step = catalog' = catalog
}
