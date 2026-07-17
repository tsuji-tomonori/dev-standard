# アーキテクチャ

## コンテキストと境界

対象はportable development skills repositoryであり、runtime serviceやcloud workloadをdeployしない。利用者は普段の会話だけを入力し、development agentがrepository-local artifactを生成・検査・PR公開する。主要stakeholderは利用者（少ない操作と意図の保存）、product owner（正本要件の一貫性）、実装者（実装可能な詳細）、reviewer（独立証拠）、maintainer（移植性・更新性）である。

`work/<id>`は会話断片・承認delta・実行証跡、`spec/requirements/requirements.json`は永続要件の唯一の正本、`docs/requirements`と`docs/design/generated`は派生viewである。初回bootstrapは正本なしをcatalog revision 0として扱う。

## コンポーネントと責務

| コンポーネント | 責務 | 所有データ | 依存先 | 品質目標 |
|---|---|---|---|---|
| chat-first/listening Skills | 意図探索、発散・収束、初回承認package | 会話から得たrequest-local解釈 | Design Council/SWEBOK research | 意味を欠落させず必要最小限の質問 |
| canonical requirements Skill | atomic requirement、revision delta、generated view | `spec/requirements/requirements.json` | Python標準library | invalid candidateは書込前に100%拒否 |
| implementation design Skill | FastAPI/CDK artifact由来の詳細設計 | generated design bundleとdigest | PyYAML、SQLGlot | 同一入力はbyte-identical |
| standards verification Skill | official source版・鮮度・判定契約 | standards registry | SWEBOK/vendor公式page | stale sourceでcurrent claimを100%拒否 |
| governance runtime | authorization、check、phase、audit | `work/<id>` evidence/hash chain | checklist catalog | tamperまたはFailをadvance前に拒否 |
| distribution manifest | copy単位と標準path | profile mapping | installer | target外writeを拒否 |

## データフローと信頼境界

```text
User chat -> work delta -> one authorization -> canonical JSON
canonical JSON -> generated requirement Markdown
router/OpenAPI/SQL/CFn -> generated design + SHA-256 manifest
canonical/design/code/tests -> checklist verdict + reachable evidence
```

外部networkは公式資料のread-only確認とGitHub PR/CIに限定する。repositoryへ入るJSON/YAML/SQL/Pythonは非信頼入力としてparser/field allowlistで検証する。shell実行、cloud API、credential、production dataは本変更の経路に含めない。

## 可用性・性能・拡張性

online SLOは非適用。local generatorは対象file数に線形で、全操作をbatch処理する。schema versionとprofile mappingで後方互換を管理し、FastAPI/CDK以外は新しいauthorized requirementとしてadapterを追加する。生成失敗時は既存正本を維持し、CIがdriftをblockする。

## 代替案とトレードオフ

- `work/`を正本にする案: 会話単位で分断され、add/update/deleteの履歴と全体整合を維持できないため不採用。
- Markdownを正本にする案: 人には読みやすいが原子性・revision・機械検証が弱いため不採用。
- Python object/DBを正本にする案: portabilityと差分reviewを損なうため不採用。
- 実装と設計を別々に手編集する案: driftを構造的に生むため不採用。
- regex SQL解析案: dialect構文とnested queryを安全に識別できないため不採用。

## 失敗・縮退・復旧

stale revision、invalid schema、parse error、duplicate operation ID、missing `functions.py`、source digest drift、stale standards sourceはnonzeroで停止する。正本更新はcandidate全体をmemory上で検証し、temporary fileのfsync後にreplaceする。派生doc失敗時は正本から再生成できる。PR branchのrollbackはrevert/closeであり、main直接pushとdeployは行わない。
