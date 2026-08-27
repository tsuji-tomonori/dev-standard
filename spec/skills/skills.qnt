// 全portable Skillの形式契約と、3本柱を接続する最小状態機械。
module skills {
  type SkillContract = {
    name: str,
    role: str,
    pillar: str,
    guardrail: bool,
    blocking: bool,
    defaultProfile: bool,
    requiresCi: bool,
    requiresMergeRule: bool,
    authority: str,
    sideEffect: str,
    precondition: str,
    postcondition: str,
    inputs: List[str],
    outputs: List[str],
  }

  pure val skillContracts: List[SkillContract] = [
    {
      name: "adversarial-review",
      role: "independent-review",
      pillar: "auxiliary",
      guardrail: false,
      blocking: false,
      defaultProfile: false,
      requiresCi: false,
      requiresMergeRule: false,
      authority: "artifact-authority",
      sideEffect: "none",
      precondition: "falsifiable claims and an authority are available",
      postcondition: "counterexamples and bounded findings are reported",
      inputs: ["artifact", "authority", "review-scope"],
      outputs: ["findings", "residual-uncertainty"],
    },
    {
      name: "author-lifecycle-docs",
      role: "regulated-documentation",
      pillar: "auxiliary",
      guardrail: false,
      blocking: false,
      defaultProfile: false,
      requiresCi: false,
      requiresMergeRule: false,
      authority: "law-contract-or-user",
      sideEffect: "repository-write",
      precondition: "a concrete regulated retention duty exists",
      postcondition: "only required lifecycle evidence is retained",
      inputs: ["regulated-duty", "retention-rule"],
      outputs: ["regulated-evidence"],
    },
    {
      name: "authorize-autonomous-execution",
      role: "authority-boundary",
      pillar: "auxiliary",
      guardrail: false,
      blocking: false,
      defaultProfile: false,
      requiresCi: false,
      requiresMergeRule: false,
      authority: "explicit-user-authorization",
      sideEffect: "external-approval",
      precondition: "an external or irreversible authority boundary exists",
      postcondition: "authorization scope and stop conditions are explicit",
      inputs: ["requested-result", "external-effects", "rollback"],
      outputs: ["authorization-decision"],
    },
    {
      name: "calibrated-collaborative-listening",
      role: "intent-clarification",
      pillar: "auxiliary",
      guardrail: false,
      blocking: false,
      defaultProfile: false,
      requiresCi: false,
      requiresMergeRule: false,
      authority: "user-intent",
      sideEffect: "none",
      precondition: "multiple interpretations materially change the result",
      postcondition: "a correctable goal and decision are available",
      inputs: ["request", "constraints"],
      outputs: ["correctable-goal", "decision"],
    },
    {
      name: "chat-first-development",
      role: "orchestrator",
      pillar: "auxiliary",
      guardrail: false,
      blocking: false,
      defaultProfile: true,
      requiresCi: false,
      requiresMergeRule: false,
      authority: "user-and-target-repository",
      sideEffect: "repository-write",
      precondition: "a development outcome is requested",
      postcondition: "only applicable pillars have been completed",
      inputs: ["request", "target-repository-rules"],
      outputs: ["change", "verification-summary"],
    },
    {
      name: "design-frontend-experience",
      role: "frontend-design",
      pillar: "auxiliary",
      guardrail: false,
      blocking: false,
      defaultProfile: false,
      requiresCi: false,
      requiresMergeRule: false,
      authority: "approved-requirements",
      sideEffect: "repository-write",
      precondition: "frontend outcomes and constraints are known",
      postcondition: "minimum implementation decisions are explicit",
      inputs: ["requirements", "existing-design-system"],
      outputs: ["design-decisions", "verification-hooks"],
    },
    {
      name: "elicit-frontend-requirements",
      role: "frontend-requirements",
      pillar: "auxiliary",
      guardrail: false,
      blocking: false,
      defaultProfile: false,
      requiresCi: false,
      requiresMergeRule: false,
      authority: "user-intent",
      sideEffect: "repository-write",
      precondition: "a frontend outcome is requested",
      postcondition: "durable observable obligations are identified",
      inputs: ["user-task", "context", "failure-impact"],
      outputs: ["requirement-candidates", "design-context"],
    },
    {
      name: "generate-implementation-design",
      role: "as-built-design",
      pillar: "design",
      guardrail: true,
      blocking: true,
      defaultProfile: true,
      requiresCi: false,
      requiresMergeRule: false,
      authority: "implementation",
      sideEffect: "repository-write",
      precondition: "a declared generator supports the changed implementation",
      postcondition: "generated design is deterministic and matches implementation",
      inputs: ["implementation", "generator-contract"],
      outputs: ["generated-design", "drift-result"],
    },
    {
      name: "govern-development-request",
      role: "regulated-orchestration",
      pillar: "auxiliary",
      guardrail: false,
      blocking: false,
      defaultProfile: false,
      requiresCi: false,
      requiresMergeRule: false,
      authority: "law-contract-or-user",
      sideEffect: "repository-write",
      precondition: "a concrete regulated lifecycle duty exists",
      postcondition: "regulated evidence is complete within that duty",
      inputs: ["regulated-trigger", "authority-boundary"],
      outputs: ["regulated-record"],
    },
    {
      name: "implement-frontend-experience",
      role: "frontend-implementation",
      pillar: "auxiliary",
      guardrail: false,
      blocking: false,
      defaultProfile: false,
      requiresCi: false,
      requiresMergeRule: false,
      authority: "requirements-and-design",
      sideEffect: "repository-write",
      precondition: "frontend requirements and decisions are ready",
      postcondition: "the user task works in supported states",
      inputs: ["requirements", "design-decisions", "existing-frontend"],
      outputs: ["frontend-change", "tests"],
    },
    {
      name: "inspect-quality-gates",
      role: "selected-checks",
      pillar: "checks",
      guardrail: true,
      blocking: true,
      defaultProfile: true,
      requiresCi: false,
      requiresMergeRule: false,
      authority: "target-repository-and-selected-checks",
      sideEffect: "none",
      precondition: "changed artifacts and applicable risks are known",
      postcondition: "only selected checks have a verdict",
      inputs: ["change", "target-checks"],
      outputs: ["selected-check-results", "residual-risk"],
    },
    {
      name: "japanese-git-commit-gitmoji",
      role: "commit-message",
      pillar: "auxiliary",
      guardrail: false,
      blocking: false,
      defaultProfile: false,
      requiresCi: false,
      requiresMergeRule: false,
      authority: "target-repository-style",
      sideEffect: "none",
      precondition: "the target repository requests this commit style",
      postcondition: "a Japanese structured commit message is proposed",
      inputs: ["diff", "verification-summary"],
      outputs: ["commit-message"],
    },
    {
      name: "maintain-canonical-requirements",
      role: "canonical-requirements",
      pillar: "requirements",
      guardrail: true,
      blocking: true,
      defaultProfile: true,
      requiresCi: false,
      requiresMergeRule: false,
      authority: "quint-requirements",
      sideEffect: "repository-write",
      precondition: "a durable observable obligation changes",
      postcondition: "Quint source, derived JSON, and generated docs agree",
      inputs: ["durable-obligation", "source", "acceptance"],
      outputs: ["requirements-qnt", "requirements-json", "requirements-doc"],
    },
    {
      name: "maintain-reference-repository",
      role: "reference-maintenance",
      pillar: "auxiliary",
      guardrail: false,
      blocking: false,
      defaultProfile: false,
      requiresCi: false,
      requiresMergeRule: false,
      authority: "reference-repository",
      sideEffect: "repository-write",
      precondition: "dev-standard portable assets change",
      postcondition: "portable and repository-specific assets remain separated",
      inputs: ["reference-change", "distribution-boundary"],
      outputs: ["portable-assets", "compatibility-result"],
    },
    {
      name: "retrospect-and-improve",
      role: "retrospective",
      pillar: "auxiliary",
      guardrail: false,
      blocking: false,
      defaultProfile: false,
      requiresCi: false,
      requiresMergeRule: false,
      authority: "observed-defect",
      sideEffect: "repository-write",
      precondition: "an evidenced recurring defect or cost exists",
      postcondition: "a bounded evaluable improvement is proposed",
      inputs: ["defect-evidence", "impact"],
      outputs: ["improvement-candidate"],
    },
    {
      name: "right-size-execution",
      role: "execution-sizing",
      pillar: "auxiliary",
      guardrail: false,
      blocking: false,
      defaultProfile: false,
      requiresCi: false,
      requiresMergeRule: false,
      authority: "change-risk",
      sideEffect: "none",
      precondition: "verification depth is not already explicit",
      postcondition: "the smallest sufficient verification scope is selected",
      inputs: ["change-risk", "available-evidence"],
      outputs: ["verification-scope"],
    },
    {
      name: "test-frontend-experience",
      role: "frontend-testing",
      pillar: "auxiliary",
      guardrail: false,
      blocking: false,
      defaultProfile: false,
      requiresCi: false,
      requiresMergeRule: false,
      authority: "frontend-requirements",
      sideEffect: "none",
      precondition: "frontend requirements and implementation are available",
      postcondition: "claims are limited to executed test scope",
      inputs: ["requirements", "implementation", "supported-environment"],
      outputs: ["test-results", "residual-risk"],
    },
    {
      name: "verify-against-engineering-standards",
      role: "standards-lens",
      pillar: "auxiliary",
      guardrail: false,
      blocking: false,
      defaultProfile: false,
      requiresCi: false,
      requiresMergeRule: false,
      authority: "selected-official-standards",
      sideEffect: "none",
      precondition: "a relevant standard is selected for the change",
      postcondition: "only applicable controls have findings",
      inputs: ["change", "selected-standard"],
      outputs: ["standard-findings"],
    },
  ]

  pure val allowedPillars = Set("requirements", "design", "checks", "auxiliary")
  pure val guardrailPillars = Set("requirements", "design", "checks")
  pure val defaultSkills = Set(
    "chat-first-development",
    "maintain-canonical-requirements",
    "generate-implementation-design",
    "inspect-quality-gates"
  )

  pure def pairwiseUnique(contracts: List[SkillContract]): bool =
    contracts.indices().forall(i =>
      contracts.indices().forall(j => i == j or contracts.nth(i).name != contracts.nth(j).name)
    )

  pure def contractsAreComplete(contracts: List[SkillContract]): bool = all {
    contracts.length() == 18,
    pairwiseUnique(contracts),
    contracts.indices().forall(i => all {
      contracts.nth(i).name != "",
      contracts.nth(i).precondition != "",
      contracts.nth(i).postcondition != "",
      contracts.nth(i).inputs.length() > 0,
      contracts.nth(i).outputs.length() > 0,
      allowedPillars.contains(contracts.nth(i).pillar),
    }),
  }

  pure def threePillarsOnly(contracts: List[SkillContract]): bool =
    contracts.indices().forall(i => all {
      contracts.nth(i).guardrail.implies(guardrailPillars.contains(contracts.nth(i).pillar)),
      contracts.nth(i).blocking.iff(contracts.nth(i).guardrail),
    })

  pure def repositoryPolicyIsHostOwned(contracts: List[SkillContract]): bool =
    contracts.indices().forall(i => all {
      not(contracts.nth(i).requiresCi),
      not(contracts.nth(i).requiresMergeRule),
    })

  pure def defaultProfileIsMinimal(contracts: List[SkillContract]): bool = all {
    contracts.indices().filter(i => contracts.nth(i).defaultProfile).size() == 4,
    contracts.indices().forall(i =>
      contracts.nth(i).defaultProfile.iff(defaultSkills.contains(contracts.nth(i).name))
    ),
  }

  var contracts: List[SkillContract]
  var phase: str
  var requirementsAligned: bool
  var designAligned: bool
  var checksPassed: bool
  var ciPolicyTouched: bool
  var mergePolicyTouched: bool

  action init = all {
    contracts' = skillContracts,
    phase' = "intake",
    requirementsAligned' = false,
    designAligned' = false,
    checksPassed' = false,
    ciPolicyTouched' = false,
    mergePolicyTouched' = false,
  }

  action alignRequirements = all {
    phase == "intake",
    contracts' = contracts,
    phase' = "design",
    requirementsAligned' = true,
    designAligned' = designAligned,
    checksPassed' = checksPassed,
    ciPolicyTouched' = ciPolicyTouched,
    mergePolicyTouched' = mergePolicyTouched,
  }

  action alignDesign = all {
    phase == "design",
    requirementsAligned,
    contracts' = contracts,
    phase' = "checks",
    requirementsAligned' = requirementsAligned,
    designAligned' = true,
    checksPassed' = checksPassed,
    ciPolicyTouched' = ciPolicyTouched,
    mergePolicyTouched' = mergePolicyTouched,
  }

  action runSelectedChecks = all {
    phase == "checks",
    requirementsAligned,
    designAligned,
    contracts' = contracts,
    phase' = "done",
    requirementsAligned' = requirementsAligned,
    designAligned' = designAligned,
    checksPassed' = true,
    ciPolicyTouched' = ciPolicyTouched,
    mergePolicyTouched' = mergePolicyTouched,
  }

  action step = any {
    alignRequirements,
    alignDesign,
    runSelectedChecks,
  }

  val formalContractsHold = all {
    contractsAreComplete(contracts),
    threePillarsOnly(contracts),
    repositoryPolicyIsHostOwned(contracts),
    defaultProfileIsMinimal(contracts),
  }

  val workflowOrderIsConsistent = all {
    (phase == "design").implies(requirementsAligned),
    (phase == "checks").implies(requirementsAligned and designAligned),
    (phase == "done").implies(requirementsAligned and designAligned and checksPassed),
  }

  val portablePolicyIsUntouched = not(ciPolicyTouched) and not(mergePolicyTouched)
  val allInvariants = formalContractsHold and workflowOrderIsConsistent and portablePolicyIsUntouched

  run formalContractTest = {
    init.then(all {
      assert(formalContractsHold),
      contracts' = contracts,
      phase' = phase,
      requirementsAligned' = requirementsAligned,
      designAligned' = designAligned,
      checksPassed' = checksPassed,
      ciPolicyTouched' = ciPolicyTouched,
      mergePolicyTouched' = mergePolicyTouched,
    })
  }

  run orderedWorkflowTest = {
    init
      .then(alignRequirements)
      .then(alignDesign)
      .then(runSelectedChecks)
      .then(all {
        assert(allInvariants),
        contracts' = contracts,
        phase' = phase,
        requirementsAligned' = requirementsAligned,
        designAligned' = designAligned,
        checksPassed' = checksPassed,
        ciPolicyTouched' = ciPolicyTouched,
        mergePolicyTouched' = mergePolicyTouched,
      })
  }
}
