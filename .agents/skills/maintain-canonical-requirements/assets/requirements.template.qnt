// 永続要件の一次言語。product固有の要件を追加し、JSONとMarkdownをここから生成する。
module requirements {
  type AcceptanceCriterion = { id: str, given: str, when_: str, expected: str }
  type Verification = { method: str, evidence: str }
  type Traces = {
    design: List[str],
    implementation: List[str],
    tests: List[str],
    standards: List[str],
  }
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

  pure val requirementsSource: Catalog = {
    schemaVersion: 1,
    catalogRevision: 0,
    product: "replace-with-product-name",
    updatedAt: "1970-01-01",
    requirements: [],
  }

  var catalog: Catalog

  action init = catalog' = requirementsSource
  action step = catalog' = catalog

  val requirementIdsAreUnique = catalog.requirements.indices().forall(i =>
    catalog.requirements.indices().forall(j =>
      i == j or catalog.requirements.nth(i).id != catalog.requirements.nth(j).id
    )
  )

  val requirementsAreAtomicAndVerifiable = catalog.requirements.indices().forall(i => all {
    catalog.requirements.nth(i).id != "",
    catalog.requirements.nth(i).revision >= 1,
    catalog.requirements.nth(i).subject != "",
    catalog.requirements.nth(i).actionName != "",
    catalog.requirements.nth(i).objectName != "",
    catalog.requirements.nth(i).sourceRefs.length() > 0,
    catalog.requirements.nth(i).acceptanceCriteria.length() > 0,
    catalog.requirements.nth(i).verification.method != "",
    catalog.requirements.nth(i).verification.evidence != "",
  })

  val classificationIsPaired = catalog.requirements.indices().forall(i =>
    (catalog.requirements.nth(i).scopeName == "") iff
    (catalog.requirements.nth(i).categoryName == "")
  )

  val retirementIsExplicit = catalog.requirements.indices().forall(i =>
    (catalog.requirements.nth(i).status == "retired").implies(
      catalog.requirements.nth(i).retirementReason != ""
    )
  )

  val catalogWellFormed = all {
    catalog.schemaVersion == 1,
    catalog.catalogRevision >= 0,
    requirementIdsAreUnique,
    requirementsAreAtomicAndVerifiable,
    classificationIsPaired,
    retirementIsExplicit,
  }

  run catalogContractTest = {
    init.then(all {
      assert(catalogWellFormed),
      catalog' = catalog,
    })
  }
}
