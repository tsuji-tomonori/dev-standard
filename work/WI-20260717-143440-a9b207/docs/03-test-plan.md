# テスト計画

## 品質リスク

重点riskは要件の複合化・lost update・history loss、generated view drift、AST call order誤認、SQL write target誤分類、CloudFormation custom tag parse failure、unofficial/stale standard source、profile copy漏れである。Critical riskはinvalid candidateが正本を書換えることと、stale guidanceをcurrentとしてPassすることである。

## テストレベルと責任

| レベル | 対象 | 技法 | 環境 | 実施者 |
|---|---|---|---|---|
| Unit | validator、renderer、AST helpers、freshness | positive/negative、boundary、exception | Python 3.12 repository-local | Codex |
| Integration | CLI generation/check、temp target install | filesystem fixture、round-trip、drift mutation | temporary directory | Codex |
| System | catalog、全tests、repository validator、audit | clean end-to-end command set | local + GitHub Actions | Codex/CI |
| Acceptance | 3本柱とcopy-and-chat documentation | requirement trace、artifact inspection | PR diff | requester review |

## 要求別テスト

| テストID | 要求ID | 条件 | 期待結果 | 自動化 |
|---|---|---|---|---|
| TEST-SPEC-001 | REQ-001〜006 | self-hosted catalogとgenerated doc | 14 atomic items、byte一致 | `tests/test_specflow.py` |
| TEST-SPEC-002 | REQ-003〜004 | composite action、stale revision、retire | invalid拒否、input不変、tombstone保持 | `tests/test_specflow.py` |
| TEST-DES-001 | REQ-007〜011 | router/functions/OpenAPI/SQL fixture | call順、IF、CRUD、digestが一致 | `tests/test_designflow.py` |
| TEST-DES-002 | REQ-007、011 | decorator、nested call、functions mutation | decorator除外、runtime順、drift拒否 | `tests/test_designflow.py` |
| TEST-CDK-001 | REQ-010〜011 | `!Ref`を含むCFn YAML | resource/parameter生成、check成功 | `tests/test_designflow.py` |
| TEST-STD-001 | REQ-012〜013 | official registry/as-of 2026-07-17 | fresh、generated view一致 | `tests/test_standardsflow.py` |
| TEST-STD-002 | REQ-012 | example.comまたは2027-07-17 | unofficial/staleを拒否 | `tests/test_standardsflow.py` |
| TEST-PORT-001 | REQ-014 | empty temp targetへprofiles copy | 3 Skillsとdependency pinが標準pathに存在 | `tests/test_install_reference.py` |
| TEST-GOV-001 | NFR-005 | full repository validation/audit | catalog、inventory、hash chainがPass | existing repository tests |

## セキュリティ・AI評価

arbitrary YAML constructorを実行しないこと、SQL/Pythonをparseのみとすること、official host allowlist、不正field rejection、target path escape rejectionを確認する。AI dialogue品質はlistening rubric、meaning preservation、non-sycophancy contract testで評価する。攻撃防御red-teamは本変更の敵対的reviewの意味ではなく、correctness defect探索のみを実施する。

## Entry・中断・再開・完了基準

Entryはauthorized requirements/plan、architecture docs、repository-local dependencyが揃うこと。parser dependency不在、test fixture破損、canonical driftでは中断し、dependency/fixture/sourceを修復後に全suiteから再開する。

完了は全unit/integration test Pass、catalog/spec/standards checks Pass、repository validator/audit Pass、未解決Critical/High defectなし、GitHub Actions greenである。skipは理由がない限り0、Failは0を要求する。時間や網羅率の数値を品質の代替にせず、要求別negative testを必須とする。
