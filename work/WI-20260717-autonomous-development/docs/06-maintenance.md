# 保守設計

## 保守方針

policy、harness、skills、templates、docs、testsを一つのrepositoryで同期保守する。仕様変更は必ず新work itemの要求原文、requirements、traceability、execution planへ記録し、一度だけ初回承認を得る。

## 変更種類

| 種類 | 例 | 必須対応 |
|---|---|---|
| corrective | digest判定、migration、gate進行のbug | 再現testを先に追加し、全verify |
| adaptive | Codex hooks、GitHub Actions、Python version変更 | compatibility requirementとCI環境を更新 |
| perfective | skillの簡潔性、validator、diagnostic改善 | measurable acceptanceと回帰testを追加 |
| preventive | recurring blockerの予防rule | pending proposalを新work itemへ変換 |

## skill maintenance

- SKILL.mdは500行未満とし、中核workflowだけを置く。
- 詳細手順、評価、研究根拠は一階層のreferencesへ分離する。
- trigger descriptionと`agents/openai.yaml`を同期する。
- skill-creator `quick_validate.py`とrepo validatorを実行する。
- 傾聴skillは14-case rubricでcritical failure 0、合計22/28以上を維持する。
- 研究追加は既存ruleとの対応をevidence mapへ記録し、長い論文本文を収録しない。

## workflow maintenance

- policy schemaを変更するときはstate migration、legacy rejection、fresh authorization testを同時に更新する。
- requirements authorizationへ新しい文書を束縛するときはdigest mutation testを追加する。
- 後続phaseに`required_approvals`を追加しないことをrepo validatorで強制する。
- Failをexceptionで通す経路を追加しない。
- automatic durable improvement applyを再導入しない。

## dependency maintenance

新規依存は、必要性、license、security、version pin、CI compatibilityを別work itemで評価する。現在は`openpyxl==3.1.5`を既存のまま維持する。Python/GitHub Actions version更新時はmain CIとlocal commandを照合する。

## lifecycle and deprecation

`approve` aliasは互換入口として残すが、documentationの正規commandは`authorize`とする。aliasを削除する場合は利用状況、migration notice、breaking-change testを新work itemで扱う。

## knowledge transfer

READMEは利用開始、FLOWは状態遷移、GOVERNANCEはtrust boundary、AGENTSはAIの恒久指示、work item docsは変更理由と証跡を担当する。新規参画者はこの順で読む。

## maintenance completion

変更後はcatalog check、unittest、repo validator、skill validator、audit、GitHub Actionsを全て成功させる。失敗またはstale authorizationを残して完了扱いにしない。
