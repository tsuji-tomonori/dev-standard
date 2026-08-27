# as-built設計check選択

`docs/standards/AS-BUILT-DESIGN.md`を具体的なartifact・code scopeへ採用した場合だけ、変更対象に対応するcheckを選ぶ。AWS CDKについては`docs/standards/AWS-CDK-AS-BUILT-DESIGN.md`を併用する。未採用repositoryの無関係な変更へ一律適用しない。

| Artifact / change | 選択候補 | 目的 |
|---|---|---|
| as-built標準contract | `FAST-024` | 要件、標準、generator、distribution、traceの整合 |
| generator入力または生成物 | `FAST-006` | generate/checkの決定論性とbyte一致 |
| API handler、OpenAPI、error sample | `FAST-016`, `FAST-017` | interfaceとsampleの整合 |
| SQL CRUD、E2E assertion | `FAST-018` | CRUDとE2E stateの対応 |
| CDK source、context、stack | `IMP-009`, `FAST-012` | synth、replacement、IAM、network、policy |
| coverage、test構造、実装規約 | `FAST-019`〜`FAST-021` | 採用scopeの実測。初回はAdvisory |
| 閾値またはdelegation設定 | `FAST-022` | 文書とmachine-readable設定の一致 |
| 品質結果とtest evidence | `FAST-023` | 実行範囲に対応する簡潔な結果 |
| suppression inventory | `AUD-008` | 理由、重複、失効、孤児の定期確認 |

選択条件、採用scope、除外は、会話または対象repositoryが既に採用する変更記録へ必要な分だけ残す。ローカルcommandを既定とし、既存CIがある場合だけ同じcheckを再利用する。

MUST / SHOULDは採用済みscope内の規範強度、Risk-selected / Advisory / Periodicは検査選択の性質であり、branchやmergeのenforcement stateではない。CI workflow、required check、review YAML、branch protection、merge ruleをこの標準のために追加または要求しない。

deploy、resource削除、production変更、課金操作等の外部副作用だけをauthority boundaryとして扱う。synth、test、設計生成は対象repositoryの既存環境で実行する。
