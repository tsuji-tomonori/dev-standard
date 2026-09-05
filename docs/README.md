# 文書索引

## 利用者向け

- [導入とSkills一覧](guides/getting-started.md)
- [開発契約](reference/development.md)
- [Quint形式仕様](reference/FORMAL-SPECIFICATIONS.md)
- [Skills根拠資料一覧・整合性監査](reference/skill-evidence-audit.md)
- [Quint・3本柱・portable policyの判断](decisions/ADR-0004-quint-three-pillar-portability.md)
- [終了した二層branch試行](decisions/ADR-0002-two-layer-branch-history.md)

## 正本と生成物

- [要件分類標準](standards/REQUIREMENT-CLASSIFICATION.md)
- [as-built設計標準](standards/AS-BUILT-DESIGN.md)
- [AWS CDK実装・as-built設計標準](standards/AWS-CDK-AS-BUILT-DESIGN.md)
- [参照資料一覧](standards/SOURCES.md)
- [生成要件一覧](requirements/REQUIREMENTS.md)

要件正本は`spec/requirements/requirements.qnt`、全Skillの形式契約は`spec/skills/skills.qnt`である。JSONと本索引から参照するMarkdownは派生viewとして生成する。

`templates/`は具体的な法令・契約・安全・本番運用・監査・利用者指定の義務に必要な場合だけ使用します。ADRは長期判断が必要な場合だけ`decisions/`へ追加します。
