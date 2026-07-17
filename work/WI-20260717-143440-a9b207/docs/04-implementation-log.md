# 実装・構成管理記録

## 変更概要

3本柱を独立したportable Skillsとして追加し、このrepositoryへ自己適用した。`specflow.py`はstrict catalogとrevision付きoperation、`designflow.py`はFastAPI/OpenAPI/SQL/CFn由来の設計bundle、`standardsflow.py`はofficial source registryと鮮度を管理する。README、FLOW、AGENTS、templates、distribution profile、CIを同じauthority modelへ統合した。

## 要求・設計との対応

| 変更 | Canonical要求ID | 設計節 | 構成管理 | レビュー |
|---|---|---|---|---|
| canonical requirements Skill/schema/script/self spec | REQ-FRAME-001、REQ-DISC-001〜004 | 詳細設計 Data/Control | branch `agent/canonical-spec-design-quality-framework` | negative/round-trip tests |
| FastAPI/CDK design Skill/generator | REQ-DESIGN-001〜006 | 詳細設計 Interfaces/Control | same branch | AST/SQL/CFn fixtures |
| standards Skill/registry/generator | REQ-QUALITY-001〜002 | Architecture/Trust boundary | same branch | official host/freshness tests |
| copy profiles/docs/bootstrap | REQ-PORTABLE-001 | Migration/Compatibility | same branch | temp target install tests |
| CI/repository validator | 全active要件 | Observability | publication commits in PR | full suite and audit |

## セキュア実装・依存関係

PyYAML 6.0.2、SQLGlot 27.28.1、Ruff 0.12.4をpinし、design Skill内にも移植可能なparser dependency contractを置いた。YAMLはSafeLoader派生でunknown CFn tagをdataとして構築し、SQL/Pythonはparseのみで実行しない。JSON/change operationはexact field allowlist、official URLはHTTPS issuer host allowlistを使う。temp file名はOS生成、canonical replace前にfsyncする。

## 設計との差異

初期実装のrouter AST走査がdecoratorをruntime callへ含め、nested callをsource位置順に並べる可能性をadversarial reviewで検出した。function body限定のpost-order visitorへ修正し、runtime evaluation orderとdecorator除外をtest化した。さらに`functions.py`をmanifestへ含め、具体処理変更でもdriftを検出するよう設計を強化した。承認scope内であり要件拡張はない。

## 実行したローカル検査

- canonical catalog validationとgenerated requirements byte check
- standards registry official-host/freshness/generated-view check
- 40件から追加後の全unittest（spec/design/standards/install/governance/skill contract）
- Ruffのimport/error/static lint
- repository inventory/manifest/config validation
- governance catalog consistencyとtamper-evident audit
- staged diff、JSON syntax、Python syntax、generated drift inspection
