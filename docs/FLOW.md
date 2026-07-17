# AI駆動開発フロー

## Authorityと生成方向

```text
自然言語の相談
   │  意図探索・発散/収束
   ▼
work/<id>  ── 要求断片・正本delta・初回承認・計画・証跡（非正本）
   │  revision付き add / update / retire
   ▼
spec/requirements/requirements.json          ← 永続要件の唯一の正本
   │                                │
   │ generate                       │ trace / acceptance
   ▼                                ▼
docs/requirements/REQUIREMENTS.md      実装・test
                                      │
               ┌──────────────────────┼──────────────────────┐
               ▼                      ▼                      ▼
        router.py / OpenAPI          raw SQL        CDK synth CFn
               │ AST                  │ AST                  │ parse
               └──────────────────────┼──────────────────────┘
                                      ▼
                       docs/design/generated/*
                    sequence / IF / CRUD / resource
                                      │
                                      ▼
             SWEBOK・vendor公式sourceのversioned checklist
```

生成文書は読みやすいviewであり正本ではありません。生成sourceのdigestと再生成結果が一致しなければ失敗です。実装由来の設計が実装と一致しても、正本要件を満たすとは限らないため、受入testとadversarial reviewを別に行います。

## 初回承認まで

1. ユーザー原文と解釈を`work/<id>/docs/00-request.md`へ保存する。
2. 現在の正本を読み、対話で目的・制約・例外・代替案を探索する。
3. obligationを原子化し、正本のbase revisionに対する`add`、`update`、`retire` deltaを`docs/01-requirements.md`へ記録する。
4. `docs/01-traceability.md`へ正本IDと予定設計・実装・test・standardの対応を記録する。
5. `docs/01-execution-plan.md`へ全作業、対象、許可操作、外部副作用、既定判断、検証、rollback、停止条件、完了条件を列挙する。
6. 結果を変える曖昧さだけを、融和的な一問で確認する。低riskで可逆な詳細は既定値を明記する。
7. deltaと計画を一体として短く提示し、要求者の明示的な判断を一度だけ記録する。会話継続やAIの推測は承認にしない。

## 初回承認後

1. catalog/item revisionを再確認し、正本deltaを完全検証してから原子的に置換する。
2. requirements viewを生成し、byte-currentを検査する。
3. architecture、詳細設計、実装、test設計を正本IDへtraceする。
4. FastAPI/CDKではimplementation artifactから詳細設計を生成し、source digestとdriftを検査する。
5. 適用するSWEBOK/cloud profileを選び、source freshnessと全checkを証跡付きで評価する。
6. defectを独立oracle、反例、境界値、mutationで探し、承認scope内の失敗を自動修正する。
7. PRを作りCIを確認し、release/retrospectiveを含む全phaseが通れば`closed`にする。

routineな設計選択、実装詳細、review修正、test修正では追加承認を求めません。承認外の新要件、不可逆な外部操作、利用不能な権限だけをblockerにします。

## 品質profile

`CORE`はSWEBOK主要ライフサイクルを扱います。cloud vendorを選ぶと`CLOUD-COMMON`に実vendorのdeltaだけを加えます。

- `CORE`: SWEBOK主要KA
- `CLOUD-COMMON`: vendor共通cloud統制
- `AWS-DELTA` / `GCP-DELTA` / `AZURE-DELTA` / `OCI-DELTA`: 実vendor差分
- `AI-CONDITIONAL`: ML・生成AI・agent固有観点

version、公式URL、確認日、再確認期限は`governance/standards/registry.json`で管理します。同じriskを複数checkで扱うときは証跡を再利用できますが、各checkの適用判定は省略しません。
