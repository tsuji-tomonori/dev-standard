# ADR-0001: as-built設計の正本・配置・適用範囲を分離する

- Status: Accepted
- Date: 2026-07-21

## 背景

as-built設計の汎用要件には、永続要件、実装・テスト規約、check定義、開発フローが混在していた。単一Markdownを`docs/requirements/`へ置くと要件の第二正本になり、独自のchecker tag体系は`governance/checks/catalog.yaml`と競合し、日付+slug計画書と全変更承認はdirect / assured / regulatedモデルと矛盾する。

## 決定

1. 永続義務は`spec/requirements/requirements.json`へ原子化し、人向け要件は`docs/requirements/REQUIREMENTS.md`から生成する。
2. 実装規約とテスト規約は`docs/standards/AS-BUILT-DESIGN.md`へ置く。
3. check ID、class、timing、trigger、acceptance、enforcementの正本は`governance/checks/catalog.yaml`だけとする。標準MarkdownはRule IDとcheck IDを結ぶ人向けビューとする。
4. 生成設計は`docs/design/generated/`へ置き、Markdownは`.gen.md`で終端し、直接編集禁止・generate/check commandを含むbannerを付ける。
5. 本標準は導入先向けのportable standardとし、追加時点ではdev-standard自身の既存`tools/`コードへレイアウト規約を遡及強制しない。
6. C0 95% / C1 90%、AAA/GWT、docstring、1 case 1関数、定量閾値はAdvisoryから開始する。実測で価値を確認したcheckだけをRisk-selectedまたはInvariantへ昇格する。
7. 公開API変更は`assured`とし、公開APIであることだけを承認triggerにしない。承認はauthority boundaryまたはregulated条件に結び付ける。
8. direct / assuredの再開用計画は`.devflow/run/`の一時状態とし、完了後に削除する。長期判断はADR、変更説明はCommit Comment、check結果はreview YAML、実行結果は外部CIへ保存する。

## 結果

- `docs/requirements/`は生成された`REQUIREMENTS.md`だけを保持する。
- as-built標準を採用したrepositoryはartifact triggerに応じてcheckを選択でき、全gateの無条件blockingを避けられる。
- 現在のdev-standard codebaseへ実装規約を適用する場合は、移行対象、互換性、閾値を定義する別変更が必要になる。
- Markdown規範とchecker実装の整合はcatalog mappingと設定一致checkで検査し、二つの機械可読正本を持たない。
