# AI駆動開発フロー

## 正本と生成方向

```text
自然言語の相談
   │  意図探索・発散/収束、Estimate（L1/L2/L3）
   ▼
work/<id>  ── execution-scope.json・要求断片・正本差分・初回承認・計画・証跡（非正本）
   │  版付き add / update / retire
   ▼
spec/requirements/requirements.json          ← 永続要件の唯一の正本
   │                                │
   │ 生成                           │ trace / 受入条件
   ▼                                ▼
docs/requirements/REQUIREMENTS.md      実装・テスト
                                      │
               ┌──────────────────────┼──────────────────────┐
               ▼                      ▼                      ▼
        router.py / OpenAPI          生SQL          CDK合成CFn
               │ AST                  │ AST                  │ 解析
               └──────────────────────┼──────────────────────┘
                                      ▼
                       docs/design/generated/*
                    シーケンス / IF / CRUD / resource
                                      │
                                      ▼
             SWEBOK・ベンダー公式資料の版管理されたチェックリスト
```

生成文書は読みやすい表示であり正本ではありません。生成ソースのdigestと再生成結果が一致しなければ失敗です。実装由来の設計が実装と一致しても、正本要件を満たすとは限らないため、受入テストと批判的レビューを別に行います。

## 初回承認まで

1. ユーザー原文、最大1回のmetadata-only probe、risk floorから`right-size-execution`がL1〜L3、confidence、soft budget、最小検証を`execution-scope.json`へ記録する。
2. ユーザー原文と解釈を`work/<id>/docs/00-request.md`へ保存する。
3. 現在の正本を読み、対話で目的・制約・例外・代替案を探索する。
4. 義務を原子化し、正本の基準版に対する`add`、`update`、`retire`差分を`docs/01-requirements.md`へ記録する。
5. `docs/01-traceability.md`へ正本IDと予定設計・実装・テスト・参照資料の対応を記録する。
6. `docs/01-execution-plan.md`へscopeの派生要約、全作業、権限境界、検証、rollback、停止条件、完了条件を記録する。
7. 結果を変える曖昧さだけを、融和的な一問で確認する。低リスクで可逆な詳細は既定値を明記する。
8. 差分と計画を一体として短く提示し、要求者の明示的な判断を一度だけ記録する。会話継続やAIの推測は承認にしない。

## 初回承認後

1. カタログ版と項目版を再確認し、正本差分を完全検証してから原子的に置換する。
2. 要件文書を生成し、バイト単位の一致を検査する。
3. アーキテクチャ、詳細設計、実装、テスト設計を正本IDへtraceする。
4. FastAPI/CDKでは実装成果物から詳細設計を生成し、ソースdigestと乖離を検査する。
5. profile内から`always_on + 成果物tag + risk tag + 現在工程`に合う項目を選び、selector版、入力、選択ID、digestを保存する。
6. 最小検証が失敗するか新証拠・予算超過がある場合だけ、scope→dependency→verification→review→capabilityの一軸を一段拡張する。
7. 欠陥を独立したoracle、反例、境界値、mutationで探し、承認範囲内の失敗を自動修正する。
8. 決定的成功後は追加探索を止め、効率reportを生成する。PRを作りCIを確認し、全工程が通れば`closed`にする。

定型的な設計選択、実装詳細、レビュー修正、テスト修正では追加承認を求めません。承認外の新要件、不可逆な外部操作、利用不能な権限だけを停止理由にします。

## 品質プロファイル

`CORE`はSWEBOKの主要ライフサイクルを扱います。クラウドベンダーを選ぶと`CLOUD-COMMON`に採用ベンダー固有の差分だけを加えます。

- `CORE`: SWEBOK主要KA
- `CLOUD-COMMON`: ベンダー共通のクラウド統制
- `AWS-DELTA` / `GCP-DELTA` / `AZURE-DELTA` / `OCI-DELTA`: 採用ベンダー固有差分
- `AI-CONDITIONAL`: ML・生成AI・エージェント固有観点

版、公式URL、適用範囲、前版との差分、確認日、再確認期限は`governance/standards/registry.json`で管理します。同じリスクを複数項目で扱うときは証跡を再利用できますが、各項目の適用判定は省略しません。
