# Skills根拠資料一覧・整合性監査

- 確認日: 2026-07-23
- 対象: `distribution/manifest.json`に登録された18 Skills、各Skillの`references/`、`governance/standards/registry.json`
- 目的: Skillsが参照する研究・規格・公式ガイダンス・実装例を列挙し、主張、適用範囲、訂正、版、運用規則との整合を確認する

## 結論

主要な運用規則を反転させる矛盾は確認されなかった。次の食い違いまたは追跡性の不足を修正した。

1. `maintain-canonical-requirements`が「SWEBOK V4」と記しながら旧Wiki章へリンクしていたため、IEEE Computer SocietyのVersion 4.0aへ統一した。
2. Huang et al. (2017)の2025年訂正とGibson et al. (2019)の訂正を追記し、訂正の影響を明示した。前者は報告値の訂正後も主要結論を維持し、後者は表記・記号上の訂正である。
3. Cheng et al.はarXiv初版ではなくICLR 2026査読版を現行根拠として扱う。Shi et al.は版が更新されるarXiv研究として扱い、LLM judge一般への普遍的保証に使用しない。
4. `test-frontend-experience`のVisual Aesthetics of Websites InventoryのDOIを、別論文を指していた`10.1080/10447318.2010.535239`から原著の`10.1016/j.ijhcs.2010.05.006`へ修正した。
5. SUS、UEQ、美的ユーザビリティ効果を一次資料へ寄せ、主観尺度と行動・アクセシビリティ証拠を分離した。
6. ISO、W3C、NASA、SWEBOK等の規格・公式資料、Figma/OpenAI/Anthropic/web.dev等の実装・実務ガイダンス、リポジトリ固有方針を査読研究と区別した。
7. 日本語あいづち資料は有効な資料だったため、題名とDOIを付与して会話コーパス上の文脈依存性を明示した。

## 根拠区分

| 区分 | 意味 | 利用規則 |
|---|---|---|
| `R` | 査読済み研究または査読済み会議論文 | 対象、方法、効果範囲、限界を維持して運用規則へ写像する |
| `P` | versioned preprint | risk signalまたは検証仮説として使用し、単独で普遍的な義務・blocking gateを作らない |
| `N` | 規格、標準、公式仕様、公式assurance guidance | 適用版とscopeを固定し、準拠を表明する場合は対象条件を確認する |
| `G` | 公式実装資料、政府・業界・ベンダーの実務ガイダンス、設計例 | 実装候補・評価観点として使用し、経験的因果効果として扱わない |
| `L` | dev-standard固有の方針、schema、閾値、workflow | 外部研究の結論と偽らず、authorityと変更履歴をリポジトリ内で管理する |

共通ルール:

- `R`や`N`も、対象プロジェクトの永続要件を自動生成しない。要件化には利用者・consumer・法令・契約・採用標準等のauthorityが必要である。
- `P`や`G`だけを根拠にblocking gate、普遍的スタイル、診断、道徳判断を作らない。
- 研究結果は方向性ではなく、研究対象・比較条件・測定方法まで含めて適用する。
- 訂正、撤回、版更新、リンク先変更を保守時に確認する。
- 導入先の承認済み要件、固定版規格、repository conventionが一般的なガイダンスより優先する。ただし安全・法令・契約上の義務を上書きしない。

## 1. 対話・意味保持・トーン

| ID | 区分 | 資料 | 使用Skill | 確認した利用方法・限界 | 判定 |
|---|---|---|---|---|---|
| C-01 | R | Weger et al. (2014), [The Relative Effectiveness of Active Listening in Initial Interactions](https://doi.org/10.1080/10904018.2013.813234) | `calibrated-collaborative-listening` | active listeningは初対面会話で「理解された感覚」を高めた。助言との差が全指標で一貫したとは扱わない。 | 限定を明記 |
| C-02 | R | Kluger et al. (2024), [A Meta-analytic Systematic Review and Theory of the Effects of Perceived Listening on Work Outcomes](https://doi.org/10.1007/s10869-023-09897-5) | 同上 | perceived listeningと関係・仕事結果の関連を支持するが、異質性、自己報告、因果制約を維持する。 | 整合 |
| C-03 | R | Clark & Brennan (1991), [Grounding in Communication](https://doi.org/10.1037/10096-006) | 同上 | common groundを共同更新する理論。任意の推測を事実化する根拠ではない。 | 整合 |
| C-04 | R | Eyal, Steffel, & Epley (2018), [Perspective Mistaking](https://doi.org/10.1037/pspa0000115) | 同上 | perspective-gettingが特定課題でperspective-takingより正確だった。直接確認が常に可能・安全とは仮定しない。 | 限定を明記 |
| C-05 | R | Huang et al. (2017), [It Doesn't Hurt to Ask: Question-Asking Increases Liking](https://doi.org/10.1037/pspi0000097) | 同上 | follow-up questionはgetting-acquainted chatとspeed-datingでresponsiveness/likingに関係した。無差別な質問増加へ一般化しない。 | 補正 |
| C-06 | R | APA (2025), [Correction to Huang et al. (2017)](https://doi.org/10.1037/pspi0000491) | 同上 | 報告上の誤りを訂正。主要結論は維持されるため、規則は反転せず訂正と文脈限界を記録する。 | 追加 |
| C-07 | R | Kintsch & van Dijk (1978), [Toward a Model of Text Comprehension and Production](https://doi.org/10.1037/0033-295X.85.5.363) | 同上 | propositionとmacrostructureの理論をcore抽出へ限定利用する。 | 整合 |
| C-08 | R | Roberts (2012), [Information Structure in Discourse](https://doi.org/10.3765/sp.5.6) | 同上 | question under discussionを関連性判断へ使用する理論的枠組み。 | 整合 |
| C-09 | R | Reyna (2012), [A New Intuitionism](https://pmc.ncbi.nlm.nih.gov/articles/PMC4268540/) | 同上 | gist/verbatimの区別から精度保持を導く。逐語保持を常に要求する根拠ではない。 | 整合 |
| C-10 | R | Nenkova & Passonneau (2004), [Evaluating Content Selection in Summarization](https://aclanthology.org/N04-1019/) | 同上 | weighted semantic unitsを要約の意味保持評価へ転用する。 | 整合 |
| C-11 | R | Liu et al. (2023), [Revisiting the Gold Standard: Grounding Summarization Evaluation with Robust Human Evaluation](https://doi.org/10.18653/v1/2023.acl-long.228) | 同上 | atomic content unitsをcompleteness検査の補助にする。単一自動評価を真値としない。 | 整合 |
| C-12 | R | Gibson et al. (2019), [How Efficiency Shapes Human Language](https://doi.org/10.1016/j.tics.2019.02.003) | 同上 | signal costと情報保持のtrade-offを圧縮原則へ使用する。 | 補正 |
| C-13 | R | Elsevier (2019), [Correction to Gibson et al.](https://doi.org/10.1016/j.tics.2019.09.005) | 同上 | spelling/notationの訂正で、利用中の概念的結論は変わらない。 | 追加 |
| C-14 | R | 宮田ほか (2024), [日本語文簡易化コーパスの構築と分析](https://doi.org/10.5715/jnlp.31.590) | 同上 |日本語簡易化で流暢さと意味保持を別に確認する。 | 整合 |
| C-15 | R | Steindl et al. (2015), [Understanding Psychological Reactance](https://doi.org/10.1027/2151-2604/a000222) | 同上 | controlling languageがreactanceを生み得るという境界を支える。個人反応の診断には使わない。 | 整合 |
| C-16 | R | Yu, Berg, & Zlatev (2021), [Emotional Acknowledgment](https://doi.org/10.1016/j.obhdp.2021.02.002) | 同上 |感情承認とtrustの研究を、正確なvalenceに限定して使用する。 | 整合 |
| C-17 | R | Pérez-Almendros et al. (2020), [Don't Patronize Me!](https://aclanthology.org/2020.coling-main.518/) | 同上 | patronizing languageのdataset/category研究。分類語彙として使用し、因果的有害性の証明とは扱わない。 | 限定を明記 |
| C-18 | R | Cheng et al. (ICLR 2026), [ELEPHANT: Measuring and Understanding Social Sycophancy in LLMs](https://www.microsoft.com/en-us/research/publication/elephant-measuring-and-understanding-social-sycophancy-in-llms/) | 同上 | emotional validation、moral endorsement、indirectness、frame acceptanceを分離する。特定benchmarkの率を全会話へ一般化しない。 | 査読状態を更新 |
| C-19 | R | 国立国語研究所 (2025), [「そうなんですね」の使用の拡大と「そうですか」との違いについて](https://doi.org/10.15084/0002000455) | 同上 | 日本語あいづちの機能が形式だけで決まらないことを会話コーパスから確認する。普遍的な共感token一覧にはしない。 | 題名・DOI追加 |

## 2. 要件・レビュー・反証

| ID | 区分 | 資料 | 使用Skill | 確認した利用方法・限界 | 判定 |
|---|---|---|---|---|---|
| RQ-01 | G | Design Council, [Framework for Innovation](https://www.designcouncil.org.uk/our-resources/framework-for-innovation/) | `maintain-canonical-requirements`, frontend Skills | divergence/convergenceを探索順序へ使用する公式framework。工程を一律固定する規格ではない。 | 整合 |
| RQ-02 | N | IEEE Computer Society, [SWEBOK Guide Version 4.0a](https://www.computer.org/education/bodies-of-knowledge/software-engineering) | `maintain-canonical-requirements`, `verify-against-engineering-standards` | requirements lifecycleと知識領域を参照する。完全準拠を主張せずregistryのscopeに従う。 | 旧Wikiリンクを修正 |
| RQ-03 | N | NASA SWEHB, [Software Requirements](https://swehb.nasa.gov/display/SWEHBVD/4.1+-+Software+Requirements) | `maintain-canonical-requirements` | traceable、verifiable、unambiguous、change controlをrequirements contractへ使用する。 | 整合 |
| RQ-04 | R | Basili et al. (1996), [The Empirical Investigation of Perspective-Based Reading](https://doi.org/10.1007/BF00368702) | `maintain-canonical-requirements`, `adversarial-review` | user/designer/tester等の異なるscenarioで欠陥探索する。各perspectiveが必ず同数の欠陥を見つけるとは扱わない。 | 整合 |
| AR-01 | R | Claessen & Hughes (2000), [QuickCheck](https://doi.org/10.1145/357766.351266) | `adversarial-review` | executable property、generated input、counterexample reductionをproperty-based testingへ使用する。 | 整合 |
| AR-02 | R | Chen et al. (2018), [Metamorphic Testing: A Review of Challenges and Opportunities](https://doi.org/10.1145/3143561) | 同上 | oracleが難しい場合のmetamorphic relationへ使用する。relation自体の妥当性検証が必要。 | 整合 |
| AR-03 | R | Jia & Harman (2011), [Mutation Testing Survey](https://doi.org/10.1109/TSE.2010.62) | 同上 | test adequacy評価へ限定し、equivalent mutantをfailureに数えない。 | 整合 |
| AR-04 | R | Parnas & Weiss (1987), [Active Design Reviews](https://doi.org/10.1016/0164-1212(87)90025-2) | 同上 | 明確な専門性、観点、質問、positive assertionをreview設計へ使用する。 | 整合 |
| AR-05 | R | Laitenberger et al. (2001), [Checklist and Perspective-Based Reading of Code Documents](https://doi.org/10.1109/32.922713) | 同上 | 3 industrial studiesでのunique defect/cost結果を、無指向checklistよりscenario passを優先する根拠にする。全artifactへの優越を保証しない。 | 限定を明記 |
| AR-06 | N | NASA (2015), [Assuring NASA's Safety and Mission Critical Software](https://ntrs.nasa.gov/citations/20160000215) | 同上 | IV&Vのobjective examinationとindependenceを高影響reviewへ使用する。NASA certificationを表明しない。 | 区分を修正 |
| AR-07 | P | Shi et al., [Judging the Judges: Position Bias in LLM-as-a-Judge](https://arxiv.org/abs/2406.07791) | 同上 | judge/task依存のposition biasをrisk signalとし、order swap、repeat、rubric、human escalationを採用する。特定modelの恒久的bias値は固定しない。 | preprint境界を追加 |

## 3. Frontend・HCI・アクセシビリティ

| ID | 区分 | 資料 | 使用Skill | 確認した利用方法・限界 | 判定 |
|---|---|---|---|---|---|
| FE-01 | N | ISO, [ISO 9241-210:2019](https://www.iso.org/standard/77520.html) | `elicit-frontend-requirements`, `design-frontend-experience` | human-centred designをlifecycleとcontextへ適用する。短いagent interviewをuser researchの代替としない。 | 整合 |
| FE-02 | N | ISO, [ISO 9241-11:2018](https://www.iso.org/standard/63500.html) | `elicit-frontend-requirements`, `test-frontend-experience` | usabilityをspecified context of useのoutcomeとして扱う。 | 整合 |
| FE-03 | N | W3C WAI, [WCAG 2 Overview](https://www.w3.org/WAI/standards-guidelines/wcag/) | `elicit-frontend-requirements` | accessibility要件をintakeから扱う。overview自体をconformance reportにしない。 | 整合 |
| FE-04 | N | W3C, [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | design/implement/test frontend Skills | applicable success criteriaをconcrete states/evidenceへ写像する。 | 整合 |
| FE-05 | G | W3C WAI, [Involving Users in Web Accessibility](https://www.w3.org/WAI/test-evaluate/involving-users/) | elicit/test frontend Skills | disabled peopleとの評価とstandards inspectionを相補的に扱う。 | 整合 |
| FE-06 | G | W3C WAI, [Evaluating Web Accessibility](https://www.w3.org/WAI/test-evaluate/) | `test-frontend-experience` | tool、method、human judgmentを組み合わせる。 | 整合 |
| FE-07 | G | W3C WAI, [Easy Checks](https://www.w3.org/WAI/test-evaluate/preliminary/) | 同上 | preliminary checkを完全評価と同一視しない。 | 整合 |
| FE-08 | G | W3C WAI, [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/) | design/implement/test frontend Skills | native HTML優先、custom widgetのsemantic/keyboard contractへ使用する。APG exampleをconformance保証としない。 | 整合 |
| FE-09 | N | WHATWG, [HTML Living Standard](https://html.spec.whatwg.org/) | `implement-frontend-experience` | native elementの定義済みsemantics/behaviorを実装authorityとして使用する。 | 整合 |
| FE-10 | G | GOV.UK Service Manual, [User research](https://www.gov.uk/service-manual/user-research) | `elicit-frontend-requirements` | users、tasks、constraints、problem fitを調べる実務guidance。 | 整合 |
| FE-11 | G | GOV.UK Design System, [Accessibility](https://design-system.service.gov.uk/accessibility/) | `design-frontend-experience` | accessible component利用だけでservice全体のaccessibilityを証明しない。 | 整合 |
| FE-12 | G | Figma, [MCP Server Guide](https://github.com/figma/mcp-server-guide) | design/implement frontend Skills | component、variable、annotation、Code Connect等をdesign-to-code contextの実装例として使用する。 | 区分を明記 |
| FE-13 | G | Figma, [figma-generate-design skill](https://github.com/figma/mcp-server-guide/blob/main/skills/figma-generate-design/SKILL.md) | `design-frontend-experience` | published primitiveからincrementalにcomposeするworkflow例。経験的普遍則ではない。 | 区分を明記 |
| FE-14 | G | Figma, [figma-implement-design skill](https://github.com/figma/mcp-server-guide/blob/main/skills/figma-implement-design/SKILL.md) | `implement-frontend-experience` | context/screenshot/asset/validationを含むworkflow例。repository conventionへ翻訳する。 | 区分を明記 |
| FE-15 | G | OpenAI, [frontend-skill](https://github.com/openai/skills/blob/main/skills/.curated/frontend-skill/SKILL.md) | design/implement frontend Skills | visual thesis、hierarchy、restraint等のcraft guidance。user task、accessibility、product consistencyより優先しない。 | 区分を明記 |
| FE-16 | G | Anthropic, [frontend-design skill](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md) | design/implement frontend Skills | deliberate directionとcontext-specific refinementのworkflow例。普遍的なstyle prescriptionではない。 | 区分を明記 |
| FE-17 | G | web.dev, [Responsive Web Design Basics](https://web.dev/articles/responsive-web-design-basics) | `implement-frontend-experience` | flexible content、viewport、layout-driven breakpointの実装guidance。 | 整合 |
| FE-18 | G | web.dev, [Core Web Vitals](https://web.dev/articles/vitals) | implement/test frontend Skills | runtime metricをcontext付きで測定する。単一lab runを全利用者の経験としない。 | 整合 |
| FE-19 | R | Brooke (1996), [SUS—A Quick and Dirty Usability Scale](https://www.researchgate.net/publication/319394819_SUS_--_a_quick_and_dirty_usability_scale) | `test-frontend-experience` | 10-item global subjective assessment。task successやaccessibilityの直接測定ではない。 | 一次資料へ変更 |
| FE-20 | R | Laugwitz, Held, & Schrepp (2008), [Construction and Evaluation of a User Experience Questionnaire](https://doi.org/10.1007/978-3-540-89350-9_6) | 同上 | UEQのsubjective dimensionsとanalysisを承認済み評価質問へ限定する。 | 一次資料へ変更 |
| FE-21 | R | Moshagen & Thielsch (2010), [Facets of Visual Aesthetics](https://doi.org/10.1016/j.ijhcs.2010.05.006) | 同上 | VisAWIによるvisual aesthetics constructをusability/accessibilityと分離する。 | DOI修正 |
| FE-22 | R | Tractinsky, Katz, & Ikar (2000), [What Is Beautiful Is Usable](https://doi.org/10.1016/S0953-5438(00)00031-X) | 同上 | 特定実験でperceived aestheticsとperceived usabilityが関連した。魅力が常に欠陥を隠すとは一般化しないため、行動証拠を独立確認する。 | 二次解説から一次研究へ変更 |

## 4. 実装・設計生成の公式資料

| ID | 区分 | 資料 | 使用Skill | 確認した利用方法・限界 | 判定 |
|---|---|---|---|---|---|
| IM-01 | G | FastAPI, [Extending OpenAPI](https://fastapi.tiangolo.com/how-to/extending-openapi/) | `generate-implementation-design` | application OpenAPIの取得・拡張方法。local router layeringやargument数は`L`方針である。 | 区分を明記 |
| IM-02 | N | OpenAPI Initiative, [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) | 同上 | OpenAPI documentのsyntax/semantics authority。 | 整合 |
| IM-03 | G | SQLGlot, [AST documentation](https://sqlglot.com/sqlglot.html) | 同上 | raw SQL解析のtool authority。解析可能性が意味的正しさを保証するとは扱わない。 | 整合 |
| IM-04 | G | AWS CDK, [Synthesis](https://docs.aws.amazon.com/cdk/v2/guide/configure-synth.html) | 同上 | `cdk synth`からCloudFormation templateを生成する公式手順。 | 整合 |
| IM-05 | N | AWS CloudFormation, [Template Anatomy](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-anatomy.html) | 同上 | synthesized templateのsection authority。 | 整合 |

`router.py`/`functions.py`分離、3引数目安、direct return、`/health`配置、generated path、digest、drift、coverage閾値等は外部資料の直接結論ではなく`L`区分のportable contractである。

## 5. Engineering standards registryの確認

次の資料は`verify-against-engineering-standards`が`governance/standards/registry.json`を通じて参照する。版、確認日、更新間隔、適用profile、scopeはregistryと生成物`docs/standards/SOURCES.md`をauthorityとする。

| ID | 区分 | 資料 | 主な適用範囲 | 判定 |
|---|---|---|---|---|
| ST-01 | N | [SWEBOK Guide Version 4.0a](https://www.computer.org/education/bodies-of-knowledge/software-engineering) | Software engineering knowledge areas | 現行版と整合 |
| ST-02 | G | [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/2025-02-25/framework/welcome.html) | AWS/cloud common | scope付きで整合 |
| ST-03 | G | [AWS Generative AI Lens](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/generative-ai-lens.html) | Generative AI/RAG | scope付きで整合 |
| ST-04 | G | [AWS Responsible AI Lens](https://docs.aws.amazon.com/wellarchitected/latest/responsible-ai-lens/responsible-ai-lens.html) | Responsible AI consideration | 法令checklistにしない境界と整合 |
| ST-05 | G | [AWS Machine Learning Lens](https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/machine-learning-lens.html) | Traditional ML lifecycle | scope付きで整合 |
| ST-06 | G | [AWS Agentic AI Lens](https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentic-ai-lens.html) | Agentic AI | registryの現行URLをauthorityとする |
| ST-07 | G | [Azure Well-Architected Framework](https://learn.microsoft.com/en-us/azure/well-architected/) | Azure/cloud common | 継続更新資料として整合 |
| ST-08 | G | [Azure AI Workload Documentation](https://learn.microsoft.com/en-us/azure/well-architected/ai/) | Azure AI | scope付きで整合 |
| ST-09 | G | [Google Cloud Well-Architected Framework](https://docs.cloud.google.com/docs/get-started/well-architected-framework) | GCP/cloud common | 継続更新資料として整合 |
| ST-10 | G | [Google Cloud AI and ML Perspective](https://cloud.google.com/architecture/framework/perspectives/ai-ml) | GCP AI/ML | scope付きで整合 |
| ST-11 | G | [OCI Best Practices Framework](https://docs.oracle.com/en/solutions/oci-best-practices/) | OCI/cloud common | F29550-09と整合 |
| ST-12 | L | [`AS-BUILT-DESIGN.md`](../standards/AS-BUILT-DESIGN.md) | dev-standard as-built contract | local authorityとして適切 |

注: ST-06の実際のURL・版はregistryを正とする。監査文書のリンクは説明用であり、standard selectionは必ずregistry経由で行う。

## 6. Commit conventionの確認

| ID | 区分 | 資料 | 使用Skill | 確認した利用方法・限界 | 判定 |
|---|---|---|---|---|---|
| CM-01 | G | [gitmoji Specification](https://gitmoji.dev/specification) | `japanese-git-commit-gitmoji` | intention emoji、optional scope、brief messageのconvention。 | 整合 |
| CM-02 | N | [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) | 同上 | `type(scope): description`、`!`、`BREAKING CHANGE`、footerのsyntax。 | 整合 |
| CM-03 | L | [`docs/reference/commit-message.md`](commit-message.md) | 同上 | 日本語要約、影響節、review path、検証契約、risk、trailersはdev-standard固有extension。 | 区分を明記 |

## 7. 外部研究に直接依存しないSkills

次のSkillsは、主にrepository-local authority、権限境界、schema、catalog、workflow、導入先conventionから動作する。外部研究の裏付けがあると主張しない。

- `chat-first-development`
- `right-size-execution`
- `inspect-quality-gates`
- `govern-development-request`
- `author-lifecycle-docs`
- `authorize-autonomous-execution`
- `retrospect-and-improve`
- `maintain-reference-repository`

`verify-against-engineering-standards`は研究を直接埋め込まず、versioned registryをselection authorityにする。`generate-implementation-design`は公式仕様・tool documentationをimplementation authorityとして使う。

## 8. Skill間の整合性

| 観点 | 結果 |
|---|---|
| 会話から要件への接続 | `calibrated-collaborative-listening`のtentative inferenceと`maintain-canonical-requirements`のatomic delta/change controlは矛盾しない。前者は意味形成、後者は永続化authorityを担当する。 |
| 質問量 | follow-up question研究は「質問を増やす」一般則ではない。Skillの「path-changing questionだけを一問ずつ」と整合する。 |
| 感情承認と反証 | acknowledgementとmoral endorsement/frame acceptanceを分離するため、`calibrated-collaborative-listening`と`adversarial-review`は補完関係にある。 |
| HCDとdelivery | frontend4 Skillsはelicitation、design、implementation、testを分離しつつ、ISO/WCAGのcontext/lifecycleを継続して扱う。短いintakeや自動checkだけでqualityを証明しない。 |
| design guidanceとrequirements | Figma/OpenAI/Anthropic等は`G`であり、approved requirement、accessibility、repository conventionより下位に置く。 |
| 自動評価 | LLM judge、visual diff、automated accessibility、questionnaire、performance metricはいずれもbounded evidenceとして扱い、単独oracleにしない。 |
| engineering standards | versioned registryが適用資料を選び、一般WAFやlocal standardを一律準拠として扱わない。 |
| local policy | JSON shape、revision protocol、review schema、commit extensions、閾値、file layoutは`L`として明示し、研究結果と混同しない。 |

## 9. 保守手順

根拠を追加・更新するときは、次を満たす。

1. title、author/issuer、year/version、stable URLまたはDOI、source classを記録する。
2. 原著・公式資料を優先し、二次解説だけで運用規則を作らない。
3. correction、retraction、expression of concern、後続版を確認する。
4. finding usedとoperational ruleの間に、対象・比較・測定・限界を残す。
5. `P`や`G`を`R`や`N`として表現しない。
6. external evidenceとlocal deterministic controlを分ける。
7. 既存Skillの規則を反転・強化する場合は、要件影響、compatibility、必要なtestを独立に評価する。
8. standard/guidanceをgateへ使う場合は`governance/standards/registry.json`へ版とscopeを登録する。
