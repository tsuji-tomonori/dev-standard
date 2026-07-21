# as-built設計check選択

`docs/standards/AS-BUILT-DESIGN.md`を採用済み、または同標準のgenerator・API・SQL・test・threshold契約を変更する場合に使用する。AWS CDKの導入・変更では、追加で`docs/standards/AWS-CDK-AS-BUILT-DESIGN.md`を参照する。未採用repositoryの無関係な変更へ一律適用しない。

| Artifact / change | 選択するcheck | Class | 選択条件 |
|---|---|---|---|
| 宣言済みgenerator入力または生成物 | `FAST-006` | Invariant | `generated_change: true`。同一生成logicのgenerate/check、決定論性、差分pathを確認する。 |
| API handler、OpenAPI、設計metadata、error sample | `FAST-016` | Risk-selected | `public_api_change: true`で三点整合が影響を受ける。 |
| API sampleまたはresponse assertion | `FAST-017` | Risk-selected | `public_api_change: true`で設計掲載sampleが変わる。 |
| SQL CRUD、E2E state assertion、error coverage | `FAST-018` | Risk-selected | `sql_change: true`または`e2e_change: true`でCRUD/E2E対応が変わる。 |
| CDK source、context、環境設定、stack構成 | `IMP-009`, `FAST-012` | Risk-selected | `iac_change: true`。synth、template差分、replacement、IAM、network、policyを確認する。 |
| generated CDK designまたは入力 | `FAST-006` | Invariant | `generated_change: true`。`docs/design/generated/cdk/`のgenerate/checkとbyte一致を確認する。 |
| as-built規約の導入・拡張 | `FAST-019` | Advisory | `as_built_adoption: true`。C0 95% / C1 90%を測定し、導入時はblockingにしない。 |
| as-built規約の導入・拡張 | `FAST-020` | Advisory | `as_built_adoption: true`。AAA/GWT、docstring、1 case 1関数を評価する。 |
| as-built規約の導入・拡張 | `FAST-021` | Advisory | `as_built_adoption: true`。解析可能なlayout、layer、SQL、log、tool、CDK construct構造を評価する。 |
| 定量閾値またはlinter/checker delegation設定 | `FAST-022` | Risk-selected | `quality_threshold_change: true`。標準値、machine-readable設定、委譲設定を一致させる。 |
| 品質結果、`cdk diff`、deploy test evidence | `FAST-023` | Advisory | `as_built_adoption: true`。結果を外部workflowまたはreport viewへ集約し、repositoryへの複製を避ける。 |
| suppression inventory | `AUD-008` | Periodic | `monthly_cycle: true`。抑制理由、重複、失効、孤児を監査する。 |

公開API変更は`assured`であり、`FAST-009`と必要な`FAST-016`/`FAST-017`を選ぶ。CDKのsynth影響変更も`assured`であり、`IMP-009`と`FAST-012`を選ぶ。公開APIまたはIaCであることだけを承認理由にせず、deploy、削除、production、課金等のauthority boundaryで承認を得る。

Advisoryをblockingへ昇格する場合は`retrospect-and-improve`に従い、escaped defectまたは反復cost、適用trigger、評価結果、予想cost、rollback、再評価日を記録する。
