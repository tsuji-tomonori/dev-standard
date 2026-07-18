<!-- specflow.pyによる自動生成。spec/requirements/requirements.jsonを編集すること。 -->
# dev-standard 要件一覧

- カタログ版: 3
- 更新日: 2026-07-18
- 正本: `spec/requirements/requirements.json`

| ID | 版 | 状態 | 種別 | 原子的な義務 | 検証方法 |
|---|---:|---|---|---|---|
| `REQ-DESIGN-001` | 2 | 有効 | 制約 | FastAPI実装フレームは、router.pyのオーケストレーションとfunctions.pyの具体処理に分けたoperationを**構成する** | 自動テスト |
| `REQ-DESIGN-002` | 2 | 有効 | 機能 | 設計生成器は、FastAPI routerの構文木から得たoperationシーケンス図を**導出する** | 自動テスト |
| `REQ-DESIGN-003` | 2 | 有効 | インターフェース | 設計生成器は、OpenAPI文書からのAPIとインターフェースの一覧を**導出する** | 自動テスト |
| `REQ-DESIGN-004` | 2 | 有効 | データ | 設計生成器は、生SQLからのquery objectとCRUD文書を**解析する** | 自動テスト |
| `REQ-DESIGN-005` | 2 | 有効 | 機能 | 設計生成器は、合成済みCloudFormationからのresourceとparameter一覧を**導出する** | 自動テスト |
| `REQ-DESIGN-006` | 2 | 有効 | 品質 | 設計フローは、実装成果物と自動生成された詳細設計の差分を**検出する** | 自動テスト |
| `REQ-DISC-001` | 2 | 有効 | 機能 | 開発エージェントは、適切な対話を通じたユーザーの意図する成果を**探り当てる** | 契約レビュー |
| `REQ-DISC-002` | 2 | 有効 | データ | 要件カタログは、正本要件IDごとの一つの原子的な義務を**維持する** | 自動テスト |
| `REQ-DISC-003` | 2 | 有効 | 機能 | 仕様管理フローは、版競合を検査した追加、更新、廃止操作を**適用する** | 自動テスト |
| `REQ-DISC-004` | 2 | 有効 | 機能 | 仕様管理フローは、正本カタログからの日本語の人間向け要件文書を**生成する** | 自動テスト |
| `REQ-DOCS-001` | 1 | 有効 | 品質 | 文書生成フローは、識別子と固有名詞を除いて日本語で統一された利用者向け文書を**提供する** | 自動検査 |
| `REQ-EXEC-001` | 1 | 有効 | 運用 | 開発実行基盤は、repository変更のscope、risk、confidence、予算、最小検証を**estimate** | 自動テスト |
| `REQ-EXEC-002` | 1 | 有効 | 品質 | 開発実行基盤は、検証失敗または新証拠に対応する一つの実行軸を**expand** | 自動テスト |
| `REQ-EXEC-003` | 1 | 有効 | 品質 | 開発実行基盤は、適正規模実行の予算、実績、拡張、停止結果を**measure** | 自動テストとbenchmark |
| `REQ-EXEC-004` | 1 | 有効 | 品質 | 標準検証基盤は、scope、成果物、risk、工程へ一致するチェック項目を**select** | 自動テスト |
| `REQ-FRAME-001` | 2 | 有効 | 制約 | リポジトリは、一時的な作業記録と永続的な製品要件を**分離する** | 自動検査 |
| `REQ-PORTABLE-001` | 2 | 有効 | 運用 | 移植可能なSkills集は、別リポジトリへのcopy-and-chat方式の導入を**実現する** | 自動テスト |
| `REQ-QUALITY-001` | 2 | 有効 | 運用 | 品質フレームは、SWEBOKとクラウド・AI公式資料の監査可能な出典台帳を**維持する** | 自動検査 |
| `REQ-QUALITY-002` | 2 | 有効 | 品質 | 品質フローは、適用可能な証拠ベースのチェックリストによる成果物検証を**検証する** | 自動監査 |
| `REQ-QUALITY-003` | 1 | 有効 | 品質 | チェックリスト生成フローは、一項目・一統制・一証跡で独立判定できるチェック項目を**維持する** | 自動テストと批判的レビュー |
| `REQ-WORKBOOK-001` | 1 | 有効 | 運用 | チェックリスト生成フローは、実データ範囲だけを集計し決定的に再現できるレビュー用ワークブックを**生成する** | 自動検査と描画確認 |

## REQ-DESIGN-001: FastAPI operation構成

FastAPI実装フレームは、router.pyのオーケストレーションとfunctions.pyの具体処理に分けたoperationを**構成する**。

根拠: 安定したoperation境界により、処理フローの導出と詳細設計の決定的な検査ができる。

受入条件:
- `AC-DESIGN-001-1` 前提: FastAPI operationを実装している。条件: ソース構成を検査する。期待結果: router.pyが処理の流れを公開し、functions.pyが具体処理を持つ。

要求源: user:2026-07-17
検証証跡: routerのAST契約テスト
トレース: 設計=.agents/skills/generate-implementation-design/references/fastapi-contract.md; 実装=.agents/skills/generate-implementation-design/SKILL.md; テスト=tests/test_designflow.py; 参照資料=SWEBOK-V4A

## REQ-DESIGN-002: routerからのシーケンス図導出

設計生成器は、FastAPI routerの構文木から得たoperationシーケンス図を**導出する**。

根拠: 実装から導出したフロー文書はソースとの整合を維持できる。

受入条件:
- `AC-DESIGN-002-1` 前提: router.pyに有効なroute関数がある。条件: FastAPI設計生成器を実行する。期待結果: 生成Mermaidが実行時の呼出順を保ち、decoratorを除外する。

要求源: user:2026-07-17
検証証跡: シーケンス出力のアサーション
トレース: 設計=.agents/skills/generate-implementation-design/references/fastapi-contract.md; 実装=.agents/skills/generate-implementation-design/scripts/designflow.py; テスト=tests/test_designflow.py; 参照資料=SWEBOK-V4A

## REQ-DESIGN-003: OpenAPIからのインターフェース設計導出

設計生成器は、OpenAPI文書からのAPIとインターフェースの一覧を**導出する**。

根拠: OpenAPIを実行可能なIF正本とすることで、手作業カタログの重複を避ける。

受入条件:
- `AC-DESIGN-003-1` 前提: アプリケーションが生成したOpenAPI文書がある。条件: FastAPI設計生成器を実行する。期待結果: operation IDを重複させずにAPI、request、response、schema文書を生成する。

要求源: user:2026-07-17, OpenAPI Specification 3.1.1, FastAPI OpenAPI documentation
検証証跡: OpenAPI fixtureの出力アサーション
トレース: 設計=.agents/skills/generate-implementation-design/references/fastapi-contract.md; 実装=.agents/skills/generate-implementation-design/scripts/designflow.py; テスト=tests/test_designflow.py; 参照資料=SWEBOK-V4A

## REQ-DESIGN-004: SQLからのデータ設計導出

設計生成器は、生SQLからのquery objectとCRUD文書を**解析する**。

根拠: AST解析は構造的な証跡を作り、無効なSQLを推測せず拒否する。

受入条件:
- `AC-DESIGN-004-1` 前提: 実行可能な生SQLファイルがある。条件: FastAPI設計生成器を実行する。期待結果: SQL構文木からquery objectとtable CRUD関係を生成する。

要求源: user:2026-07-17, SQLGlot documentation
検証証跡: SQL AST fixtureとCRUD出力のアサーション
トレース: 設計=.agents/skills/generate-implementation-design/references/fastapi-contract.md; 実装=.agents/skills/generate-implementation-design/scripts/designflow.py; テスト=tests/test_designflow.py; 参照資料=SWEBOK-V4A

## REQ-DESIGN-005: CDKデプロイ設計の生成

設計生成器は、合成済みCloudFormationからのresourceとparameter一覧を**導出する**。

根拠: 合成されたデプロイテンプレートが具体的なインフラストラクチャIFである。

受入条件:
- `AC-DESIGN-005-1` 前提: AWS CDK stackがCloudFormation YAMLまたはJSONを合成している。条件: CDK設計生成器を実行する。期待結果: テンプレートからresourceとparameterの詳細文書を生成する。

要求源: user:2026-07-17, AWS CDK synth documentation, CloudFormation template anatomy
検証証跡: CloudFormation fixtureの出力アサーション
トレース: 設計=.agents/skills/generate-implementation-design/references/cdk-contract.md; 実装=.agents/skills/generate-implementation-design/scripts/designflow.py; テスト=tests/test_designflow.py; 参照資料=AWS-WAF

## REQ-DESIGN-006: 実装と設計の差分検出

設計フローは、実装成果物と自動生成された詳細設計の差分を**検出する**。

根拠: digestとバイト比較により実装と設計の1対1再現性を強制する。

受入条件:
- `AC-DESIGN-006-1` 前提: 自動生成された詳細設計がある。条件: 設計差分検査を実行する。期待結果: ソースSHA-256 manifestが存在し、クリーンな再生成結果がバイト単位で一致する。

要求源: user:2026-07-17
検証証跡: 変更済みソースを用いた差分検出テスト
トレース: 設計=.agents/skills/generate-implementation-design/SKILL.md; 実装=.agents/skills/generate-implementation-design/scripts/designflow.py; テスト=tests/test_designflow.py; 参照資料=SWEBOK-V4A

## REQ-DISC-001: 研究に裏付けられた意図の探索

開発エージェントは、適切な対話を通じたユーザーの意図する成果を**探り当てる**。

根拠: 言語化しきれていない要求を負担なく探り当てるには、心地よい傾聴と精密な言語化が必要である。

受入条件:
- `AC-DISC-001-1` 前提: ユーザーの要求が不完全または曖昧である。条件: 解釈差が成果を変える。期待結果: 推定した目的、制約、葛藤、最小限の重要質問を迎合せず提示する。

要求源: user:2026-07-17, Design Council Double Diamond, calibrated listening research
検証証跡: Skill指示と研究根拠
トレース: 設計=.agents/skills/maintain-canonical-requirements/references/research-basis.md; 実装=.agents/skills/maintain-canonical-requirements/SKILL.md,.agents/skills/calibrated-collaborative-listening/SKILL.md; テスト=tests/test_skills.py; 参照資料=SWEBOK-V4A

## REQ-DISC-002: 原子的な永続要件

要件カタログは、正本要件IDごとの一つの原子的な義務を**維持する**。

根拠: 原子的な要件は独立した変更、検証、トレーサビリティを可能にする。

受入条件:
- `AC-DISC-002-1` 前提: 永続的な義務が受け入れられている。条件: 要件を永続化する。期待結果: 一つのID、主体、正規化action、対象、状態、受入条件、検証、traceを正本に持つ。

要求源: user:2026-07-17, SWEBOK Software Requirements
検証証跡: 複合または不完全な義務をスキーマ検証が拒否する記録
トレース: 設計=.agents/skills/maintain-canonical-requirements/assets/requirements.schema.json; 実装=.agents/skills/maintain-canonical-requirements/scripts/specflow.py; テスト=tests/test_specflow.py; 参照資料=SWEBOK-V4A

## REQ-DISC-003: 安全な要件ライフサイクル変更

仕様管理フローは、版競合を検査した追加、更新、廃止操作を**適用する**。

根拠: 楽観的同時実行制御と廃止墓標により、更新消失と履歴消去を防ぐ。

受入条件:
- `AC-DISC-003-1` 前提: 変更セットが現行カタログ版と項目版を指定している。条件: 追加、更新、廃止を適用する。期待結果: 完全な候補を検証してから正本を原子的に置換する。
- `AC-DISC-003-2` 前提: 正本だった要件の削除が要求される。条件: 変更を受け入れる。期待結果: 理由付きの廃止墓標として項目を残す。

要求源: user:2026-07-17
検証証跡: 版競合と廃止操作のテスト
トレース: 設計=.agents/skills/maintain-canonical-requirements/SKILL.md; 実装=.agents/skills/maintain-canonical-requirements/scripts/specflow.py; テスト=tests/test_specflow.py; 参照資料=SWEBOK-V4A

## REQ-DISC-004: 要件文書の自動生成

仕様管理フローは、正本カタログからの日本語の人間向け要件文書を**生成する**。

根拠: 生成ビューは競合する編集可能な正本を作らずに読者へ情報を提供する。

受入条件:
- `AC-DISC-004-1` 前提: 正本カタログが有効である。条件: 文書生成と差分検査を実行する。期待結果: 日本語の要件文書を再現でき、正本とバイト単位で一致する。

要求源: user:2026-07-17
検証証跡: 生成文書の完全一致検査
トレース: 設計=docs/requirements/REQUIREMENTS.md; 実装=.agents/skills/maintain-canonical-requirements/scripts/specflow.py; テスト=tests/test_specflow.py; 参照資料=SWEBOK-V4A

## REQ-DOCS-001: 日本語の利用者向け文書

文書生成フローは、識別子と固有名詞を除いて日本語で統一された利用者向け文書を**提供する**。

根拠: 導入・運用・監査の文書言語を統一し、意味の取り違えと二重保守を防ぐ。

受入条件:
- `AC-DOCS-001-1` 前提: 利用者向けMarkdownまたは生成文書がある。条件: リポジトリ検証を実行する。期待結果: 見出しと説明が日本語であり、生成物が日本語テンプレートから再現される。

要求源: user:2026-07-18
検証証跡: 日本語文書検査と生成差分テスト
トレース: 設計=docs/README.md; 実装=.agents/skills/maintain-canonical-requirements/scripts/specflow.py,.agents/skills/verify-against-engineering-standards/scripts/standardsflow.py; テスト=tests/test_validate_repo.py,tests/test_specflow.py,tests/test_standardsflow.py; 参照資料=SWEBOK-V4A

## REQ-EXEC-001: 適正規模の初期推定

開発実行基盤は、repository変更のscope、risk、confidence、予算、最小検証を**estimate**。

根拠: 成功条件と重大リスクを満たす最小十分な経路を作業前に固定し、単純な変更の過剰探索と重大変更の過小評価を避ける。

受入条件:
- `AC-EXEC-001-1` 前提: 自然言語のrepository変更依頼がある。条件: 実装前のscopeを推定する。期待結果: L1からL3、risk、confidence、soft budget、最小検証をschema検証済み台帳へ記録し、高リスク変更をL3にする。

要求源: user:2026-07-18, arXiv:2607.13034
検証証跡: scope分類、risk floor、schemaの回帰テスト
トレース: 設計=.agents/skills/right-size-execution/references/scope-levels.md; 実装=.agents/skills/right-size-execution/scripts/scopeflow.py,.agents/skills/right-size-execution/assets/execution-policy.json; テスト=tests/test_scopeflow.py; 参照資料=SWEBOK-V4A

## REQ-EXEC-002: 根拠付きの段階的拡張

開発実行基盤は、検証失敗または新証拠に対応する一つの実行軸を**expand**。

根拠: 推定誤りを回復しつつ、無関係なcontext、review、model能力を同時に増やすコストを防ぐ。

受入条件:
- `AC-EXEC-002-1` 前提: 検証失敗またはscope推定を覆す証拠がある。条件: 実行経路を拡張する。期待結果: 許可された理由、直接証拠、actorを記録し、一回につき一軸を一段だけ拡張する。

要求源: user:2026-07-18, arXiv:2607.13034
検証証跡: 拡張理由、一軸制約、回数上限、能力引上げ前提の回帰テスト
トレース: 設計=.agents/skills/right-size-execution/references/expansion-rules.md; 実装=.agents/skills/right-size-execution/scripts/scopeflow.py; テスト=tests/test_scopeflow.py; 参照資料=SWEBOK-V4A

## REQ-EXEC-003: 実行効率の生指標計測

開発実行基盤は、適正規模実行の予算、実績、拡張、停止結果を**measure**。

根拠: oracleなしの単一指標を最適化せず、成功率と重大欠陥を保ちながら冗長性を改善するには、生指標と理由の再現可能な台帳が必要である。

受入条件:
- `AC-EXEC-003-1` 前提: repository作業を実行している。条件: 効率reportを確定する。期待結果: token取得可否にかかわらずtool、search、file、byte、range、重複、時間、Expand、成功、成功後探索を記録し、ACRRをoracleなしで表明しない。

要求源: user:2026-07-18, arXiv:2607.13034
検証証跡: efficiency report、overrun、成功後停止の回帰テスト
トレース: 設計=.agents/skills/right-size-execution/references/measurement-contract.md; 実装=.agents/skills/right-size-execution/scripts/scopeflow.py; テスト=tests/test_scopeflow.py; 参照資料=SWEBOK-V4A

## REQ-EXEC-004: タスク固有の標準チェック選択

標準検証基盤は、scope、成果物、risk、工程へ一致するチェック項目を**select**。

根拠: プロファイル全量をpromptと実施記録へ登録せず、選択入力と結果を保存することで実行効率と監査可能性を両立する。

受入条件:
- `AC-EXEC-004-1` 前提: schema検証済みscopeとversion固定catalogがある。条件: 標準チェックを選択する。期待結果: always-on、成果物tag、risk tag、工程、scope levelから候補を決め、selector版、入力特徴、選択ID、digestを保存する。

要求源: user:2026-07-18, arXiv:2607.13034
検証証跡: 同一入力の選択再現性とwork item初期化テスト
トレース: 設計=.agents/skills/right-size-execution/SKILL.md; 実装=tools/devflow.py,governance/checklist/catalog.json; テスト=tests/test_scopeflow.py,tests/test_devflow.py; 参照資料=SWEBOK-V4A

## REQ-FRAME-001: workと正本の境界

リポジトリは、一時的な作業記録と永続的な製品要件を**分離する**。

根拠: work itemは実行文脈であり、暗黙に製品仕様の正本へ変わってはならない。

受入条件:
- `AC-FRAME-001-1` 前提: 統制対象の要求が存在する。条件: 要求を記録する。期待結果: workには要求断片、判断、計画、証跡だけが残り、永続要件は正本へ保存される。

要求源: user:2026-07-17
検証証跡: リポジトリ検証とSkill契約テスト
トレース: 設計=docs/FLOW.md; 実装=.agents/skills/maintain-canonical-requirements/SKILL.md; テスト=tests/test_specflow.py; 参照資料=SWEBOK-V4A

## REQ-PORTABLE-001: チャットだけで移植できる導入

移植可能なSkills集は、別リポジトリへのcopy-and-chat方式の導入を**実現する**。

根拠: 本リポジトリは再利用可能な参照集であり、利用者が内部ツールを手動操作せずに使える必要がある。

受入条件:
- `AC-PORTABLE-001-1` 前提: 対象Skillsフォルダを別リポジトリへコピーしている。条件: 利用者が自然言語で開発要求を相談する。期待結果: 通常のチャットから導入、要件、設計、実装、テスト、公開までを自動実行する。

要求源: user:2026-07-17
検証証跡: プロファイル導入とSkill検出テスト
トレース: 設計=docs/INSTALLATION.md; 実装=distribution/manifest.json,.agents/skills/chat-first-development/SKILL.md; テスト=tests/test_install_reference.py,tests/test_skills.py; 参照資料=SWEBOK-V4A

## REQ-QUALITY-001: 版管理された出典台帳

品質フレームは、SWEBOKとクラウド・AI公式資料の監査可能な出典台帳を**維持する**。

根拠: 正式名称、版、URL、参照範囲、差分、固定物ハッシュを保存することで、レビュー根拠を再現し更新を検知できる。

受入条件:
- `AC-QUALITY-001-1` 前提: 品質プロファイルを選択している。条件: 出典台帳を検証する。期待結果: 各資料が公式URL、版、参照日、更新間隔、適用範囲、変更確認日、前版との差分を持ち、固定参照物はSHA-256を持つ。
- `AC-QUALITY-001-2` 前提: 添付SWEBOKを参照する。条件: 版の同一性を検証する。期待結果: v4.0aの正式名称、18KA対応、固定SHA-256が台帳と一致する。

要求源: user:2026-07-17, SWEBOK V4, AWS Well-Architected, Azure Well-Architected, Google Cloud Well-Architected, OCI Best Practices
検証証跡: 公式host、鮮度、範囲、差分、ハッシュのテスト
トレース: 設計=docs/standards/SOURCES.md; 実装=.agents/skills/verify-against-engineering-standards/scripts/standardsflow.py,governance/standards/registry.json; テスト=tests/test_standardsflow.py; 参照資料=SWEBOK-V4A,AWS-WAF,AWS-GENAI-LENS,AWS-RAI-LENS,AWS-ML-LENS,AWS-AGENTIC-LENS,AZURE-WAF,AZURE-AI-WAF,GCP-WAF,GCP-AIML-WAF,OCI-WAF

## REQ-QUALITY-002: 証跡に裏付けられた標準検証

品質フローは、適用可能な証拠ベースのチェックリストによる成果物検証を**検証する**。

根拠: 適用判断から再確認までの完全な実施記録により、観点集を監査可能な品質ゲートへ変える。

受入条件:
- `AC-QUALITY-002-1` 前提: 要件、設計、実装、テストをレビューする。条件: 品質ゲートを評価する。期待結果: 各選択項目が案件重要度と根拠、Passと直接証跡、N/Aと範囲理由、またはFailとIssue、対応方針、期限、レビュアー、日付を記録する。
- `AC-QUALITY-002-2` 前提: 以前の判定がFailである。条件: 是正後にPassへ変更する。期待結果: 旧Failを履歴に残し、到達可能な証跡、再確認者、再確認日を含むPassの再確認記録を持つ。

要求源: user:2026-07-17, SWEBOK V4, cloud vendor official guidance
検証証跡: 品質ゲート監査と実施結果スキーマのテスト
トレース: 設計=.agents/skills/verify-against-engineering-standards/SKILL.md; 実装=tools/devflow.py; テスト=tests/test_devflow.py,tests/test_standardsflow.py; 参照資料=SWEBOK-V4A,AWS-WAF,AWS-GENAI-LENS,AWS-RAI-LENS,AWS-ML-LENS,AWS-AGENTIC-LENS,AZURE-WAF,AZURE-AI-WAF,GCP-WAF,GCP-AIML-WAF,OCI-WAF

## REQ-QUALITY-003: 原子的なチェック統制

チェックリスト生成フローは、一項目・一統制・一証跡で独立判定できるチェック項目を**維持する**。

根拠: 複数統制を一行へ詰め込むと部分実装を一意にPassまたはFailと判定できない。

受入条件:
- `AC-QUALITY-003-1` 前提: チェック項目を追加または更新する。条件: ワークブックを生成・検証する。期待結果: 独立した合否条件を持つ統制へ分割され、既知の複合項目が再発しない。

要求源: user:2026-07-18, SWEBOK Software Quality
検証証跡: 原子性回帰テストとチェック項目カタログ
トレース: 設計=docs/GOVERNANCE.md; 実装=update_checklist.py,.agents/skills/verify-against-engineering-standards/SKILL.md; テスト=tests/test_checklist.py; 参照資料=SWEBOK-V4A

## REQ-WORKBOOK-001: 再現可能で有界なワークブック

チェックリスト生成フローは、実データ範囲だけを集計し決定的に再現できるレビュー用ワークブックを**生成する**。

根拠: Excel全行参照は読込時に過大なメモリを消費し、固定集計値は項目追加時に陳腐化する。

受入条件:
- `AC-WORKBOOK-001-1` 前提: チェック項目の行数が変わる。条件: ワークブックを再生成する。期待結果: 集計式が各シートの実データ最終行へ更新され、実数と一致し、全列参照を含まない。

要求源: user:2026-07-18
検証証跡: 数式範囲テスト、項目数照合、代表シートの描画結果
トレース: 設計=docs/GOVERNANCE.md; 実装=update_checklist.py; テスト=tests/test_checklist.py; 参照資料=SWEBOK-V4A
