<!-- standardsflow.pyによる自動生成。governance/standards/registry.jsonを編集すること。 -->
# 参照資料一覧

この一覧は品質検証で参照する知識体系・公式ガイダンスの版と適用範囲を固定する。各資料は案件条件に応じて適用性を判断する参照情報であり、一律適用や完全準拠を表明しない。

| ID | 発行元 | 資料 | 版・公開日 | 適用範囲 | 参照日 | 変更確認日 | 更新間隔 | プロファイル | 固定参照物SHA-256 |
|---|---|---|---|---|---|---|---:|---|---|
| `SWEBOK-V4A` | IEEE Computer Society | [Guide to the Software Engineering Body of Knowledge, Version 4.0a](https://www.computer.org/education/bodies-of-knowledge/software-engineering) | 4.0a / 2025-09 | 18 Knowledge Areaを対応付ける。KA 1〜10・12・13を直接参照、KA 11・14・15を部分整合、KA 16〜18を前提知識として理由付き対象外とする。 | 2026-07-18 | 2026-07-18 | 180日 | CORE | `b3cb8028fecb9607f757504c861947fa3bf423087ea8bf08c58020f0ba3596dc` |
| `AWS-WAF` | Amazon Web Services | [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/2025-02-25/framework/welcome.html) | 2025-02-25 | AWSおよびクラウド共通の設計判断、リスク、柱間トレードオフ。 | 2026-07-18 | 2026-07-18 | 90日 | CLOUD-COMMON, AWS-DELTA | — |
| `AWS-GENAI-LENS` | Amazon Web Services | [AWS Well-Architected Generative AI Lens](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/generative-ai-lens.html) | 2025-11-19 | 基盤モデル、生成AI、RAG、プロンプト、生成AIライフサイクルを持つAWSワークロード。 | 2026-07-18 | 2026-07-18 | 90日 | AI-CONDITIONAL, AWS-DELTA | — |
| `AWS-RAI-LENS` | Amazon Web Services | [AWS Well-Architected Responsible AI Lens](https://docs.aws.amazon.com/wellarchitected/latest/responsible-ai-lens/responsible-ai-lens.html) | 2025-11-19 | 特定AIユースケースの便益・リスク、責任あるAIの判断。法令準拠チェックリストとしては使用しない。 | 2026-07-18 | 2026-07-18 | 90日 | AI-CONDITIONAL, AWS-DELTA | — |
| `AWS-ML-LENS` | Amazon Web Services | [AWS Well-Architected Machine Learning Lens](https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/machine-learning-lens.html) | 2025-11-19 | 教師あり・教師なし学習、予測、分類、回帰等を含む従来型MLライフサイクル。 | 2026-07-18 | 2026-07-18 | 90日 | AI-CONDITIONAL, AWS-DELTA | — |
| `AWS-AGENTIC-LENS` | Amazon Web Services | [AWS Well-Architected Agentic AI Lens](https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentic-ai-lens.html) | 2026-06-10 | 自律的ツール利用、メモリ、反復推論、複数エージェント、現実世界への作用を持つエージェントAI。 | 2026-07-18 | 2026-07-18 | 60日 | AI-CONDITIONAL, AWS-DELTA | — |
| `AZURE-WAF` | Microsoft | [Azure Well-Architected Framework](https://learn.microsoft.com/en-us/azure/well-architected/) | 継続更新 | Azureおよびクラウド共通の柱、設計原則、ワークロード固有のトレードオフ。 | 2026-07-18 | 2026-07-18 | 90日 | CLOUD-COMMON, AZURE-DELTA | — |
| `AZURE-AI-WAF` | Microsoft | [AI Workload Documentation - Azure Well-Architected Framework](https://learn.microsoft.com/en-us/azure/well-architected/ai/) | 継続更新 | 非決定的挙動、データ、モデル、AIアプリケーション、AI運用を含むAzure AIワークロード。 | 2026-07-18 | 2026-07-18 | 90日 | AI-CONDITIONAL, AZURE-DELTA | — |
| `GCP-WAF` | Google Cloud | [Google Cloud Well-Architected Framework](https://docs.cloud.google.com/docs/get-started/well-architected-framework) | 継続更新 | Google Cloudおよびクラウド共通の設計原則、柱、運用上のトレードオフ。 | 2026-07-18 | 2026-07-18 | 90日 | CLOUD-COMMON, GCP-DELTA | — |
| `GCP-AIML-WAF` | Google Cloud | [Google Cloud Well-Architected Framework: AI and ML perspective](https://cloud.google.com/architecture/framework/perspectives/ai-ml) | 継続更新 | Google Cloud上のAI/MLデータ、モデル、運用、責任あるAIの設計観点。 | 2026-07-18 | 2026-07-18 | 90日 | AI-CONDITIONAL, GCP-DELTA | — |
| `OCI-WAF` | Oracle | [Best practices framework for Oracle Cloud Infrastructure](https://docs.oracle.com/en/solutions/oci-best-practices/) | F29550-09 / 2025-05 | OCIおよびクラウド共通の設計原則とベンダー固有差分。 | 2026-07-18 | 2026-07-18 | 90日 | CLOUD-COMMON, OCI-DELTA | — |
| `DEVSTD-AS-BUILT` | dev-standard maintainers | [as-built設計標準](https://github.com/tsuji-tomonori/dev-standard/blob/main/docs/standards/AS-BUILT-DESIGN.md) | 2026-07-21 | 実装由来設計の決定論的生成、専用path、整合check、解析可能な実装・test規約、profile連携。導入時はAdvisoryから評価する。 | 2026-07-21 | 2026-07-21 | 180日 | CORE | `f35016e6dcfa0ea52225a68e2659f07f29c65333e5a5aa6778caee7a1533b05f` |

## 前版との差分・変更確認

- `SWEBOK-V4A`: v4.0から2025年9月の軽微改訂版v4.0aへ更新。完全準拠ではなく、対象範囲を明示した参照・整合として扱う。
- `AWS-WAF`: 基準日付きURLを維持し、案件のSLO、RTO/RPO、データ分類、規制、コスト制約に応じて適用する方針を明示。
- `AWS-GENAI-LENS`: 公開日2025年11月19日の現行Lensを登録し、従来型MLとエージェントAIから用途を分離。
- `AWS-RAI-LENS`: 2025年11月19日公開のLensを追加。各考慮事項を案件固有に適用し、一律要件・保証表明にしない。
- `AWS-ML-LENS`: 2025年11月19日公開の独立Lensを追加し、Generative AI Lensとの適用境界を明示。
- `AWS-AGENTIC-LENS`: 2026年6月10日公開のLensを追加。境界付き自律性、追跡可能性、リスク比例の人間監督、実行予算を反映。
- `AZURE-WAF`: 継続更新型資料として変更確認日を固定し、採用ベンダー差分だけをCloud Commonへ追加する。
- `AZURE-AI-WAF`: Azure AI Workload資料を独立出典として登録し、一般WAFとの重複は差分プロファイルで扱う。
- `GCP-WAF`: 継続更新型資料として変更確認日を固定し、Cloud CommonとGCP固有差分の重複規則を適用。
- `GCP-AIML-WAF`: AI/ML perspectiveを一般WAFから分離し、AI-CONDITIONALとGCP差分に対応付け。
- `OCI-WAF`: 文書版F29550-09を維持し、Cloud Common評価後にOCI固有差分だけを追加する。
- `DEVSTD-AS-BUILT`: 利用者提供の汎用要件を要件正本、標準、check catalog、既存Skillへ分配し、3本柱モデルとauthority boundaryへ整合した初版。
