# 文書の利用目的と更新対象

利用開始は[導入ガイド](guides/getting-started.md)へ進んでください。以下は文書の保守対象一覧です。機能変更に関係する行だけを確認し、不要になった文書は参照元・配布・生成・検査も含めて削除します。全件の読込みや、変更ごとの報告書作成は求めません。

## 継続して維持する文書

| 文書 | 利用者・目的 | 更新条件・更新元 |
|---|---|---|
| [README](../README.md) | 利用者・agentが3本柱と依頼方法を把握する | 利用目的・入口・導入完了条件が変わるとき |
| [AGENTS](../AGENTS.md) | この参照repositoryを変更するagentの入口 | 正本・保守方法・検証commandが変わるとき |
| この索引 | 保守者が更新対象・履歴を区別する | 文書の追加・削除・移動・用途変更時 |
| [導入ガイド](guides/getting-started.md) | 利用者・agentが配置から実装・初回生成・検査まで進める | installer・配布profile・対応能力・完了条件の変更時 |
| [要件分類標準](standards/REQUIREMENT-CLASSIFICATION.md) | 要件Skill利用者が永続義務と実装判断を区別する | 要件schema・分類・受入条件の変更時 |
| [as-built設計標準](standards/AS-BUILT-DESIGN.md) | 設計生成者が必要なfactと完全性を判断する | generator・adapter・生成帳票の契約変更時 |
| [AWS CDK設計標準](standards/AWS-CDK-AS-BUILT-DESIGN.md) | CDK利用時の生成者がcapabilityと適用範囲を判断する | CDK抽出・検査・対応能力の変更時だけ |
| [生成要件一覧](requirements/REQUIREMENTS.md) | 利用者・保守者が現在の要件を読む | `spec/requirements/requirements.qnt` → JSON → Markdown。`python tools/quintflow.py generate`で再生成 |
| [参照資料一覧](standards/SOURCES.md) | 標準照合の利用者が採用資料の版・適用範囲を確認する | standards Skillのregistryから再生成。下記の開発検査に従う |
| [設計の正本判断](decisions/ADR-0001-as-built-design-authority-and-scope.md) | 保守者が要件と実装由来設計の責務を確認する | 採用した正本・生成範囲を変更するとき |
| [host生成の判断](decisions/ADR-0003-canonical-host-asset-generation.md) | host保守者が複製を手編集しない理由を確認する | host adapter・生成物の管理方法を変えるとき |
| [3本柱と配布境界の判断](decisions/ADR-0004-quint-three-pillar-portability.md) | 保守者が強制範囲と形式検証の限界を確認する | 柱・配布境界・形式モデルを変えるとき |
| [各Skill](../.agents/skills/)の `SKILL.md`・`references/` | 該当Skillを実行するagentが固有の判断・操作を行う | 当該Skillの能力・入力・出力・失敗条件の変更時。必要な参照だけ読む |
| [reviewer](../.codex/agents/)・[配布snippet](../distribution/snippets/) | 選択されたhost・reviewerで入口と権限を保持する | host・reviewerの契約変更時。host別複製は再生成する |

手書き文書は利用目的と適用範囲を上表に集約します。生成物は手編集せず、正本・生成器を直します。Skill契約の詳細は `spec/skills/skills.qnt` と派生 `skills.json` に保持し、別の全件表示文書を重複管理しません。

## 更新しない履歴と一時情報

- `archive/YYYY-MM-DD-*.md`: 日付時点の監査・調査・廃止判断。本文を現在の仕様へ合わせず、当時のリンクや名称も履歴として扱います。現行の使用手順・合否の証拠として使いません。
- `governance/reviews/CHG-*.yaml`: 過去の変更時点の固定記録。新しい変更の定型成果物として増やさず、現在のpathへの更新も行いません。schema・validator・templateは明示的に選んだreview機能の保守対象です。
- `.devflow/run/`: 再開に必要な一時状態。Git管理せず、用済みになれば削除します。
- `.devflow/generated/`: host package等の再生成可能な出力。Git管理しません。

汎用の工程別文書テンプレートは配布しません。保持義務や利用者指定で必要な文書は、対象projectの書式・目的・保持期間に合わせて作成します。

## このrepositoryの開発検査

```bash
make setup
python tools/quintflow.py generate
python tools/quintflow.py check
python tools/audit_consistency.py
make verify
```

`make verify`は全体契約の変更時に使い、通常は変更に関係する検査だけを選びます。Quintによる型・不変条件、JSON/Markdownの生成差分、Skill本文・asset・interfaceのdigest、両hostの配布完結性と既存設定の保全を確認します。bounded検証の範囲は `tools/quintflow.py` が定義します。形式化していない自然言語の正しさや、全projectでの成功まで証明するものではありません。

標準registryを変えた場合は、standards Skillの `scripts/standardsflow.py generate` で `docs/standards/SOURCES.md` を再生成し、`check`で確認します。正本は `.agents/skills/verify-against-engineering-standards/assets/standards.registry.json` です。

指示設計は用途・必要な判断・検証方法に絞ります。[GPT-6公式ガイド](https://developers.openai.com/api/docs/guides/latest-model)が挙げる曖昧・矛盾した指示による不要停止に注意し、利用者の明示指示をSkillの一般ガイドより優先します。[Skills公式ガイド](https://learn.chatgpt.com/docs/build-skills)に沿って必要時に読み込む構成を保ちます。文字量の削減だけでモデルの成功率向上を主張しません。
