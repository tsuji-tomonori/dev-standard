# 要求トレーサビリティ

- Canonical source: `spec/requirements/requirements.json`
- Base catalog revision: 1
- この表は承認対象deltaの予定対応を示す。正本要件IDを再定義しない。

| 要求ID | ユーザー要望 | 設計要素 | 実装 | テスト | 証跡 | 状態 |
|---|---|---|---|---|---|---|
| REQ-QUALITY-001 | v4.0a、出典、差分を監査可能にする | 出典台帳スキーマ | `registry.json`、`standardsflow.py`、`update_checklist.py` | `test_standardsflow.py`、ワークブック検査 | 出典一覧、出典マスター | 予定 |
| REQ-QUALITY-002 | 実行結果を記録し品質ゲートで検証する | 実施結果スキーマ2 | `tools/devflow.py` | `test_devflow.py`、work監査 | `checklist-results.json`、events | 予定 |
| REQ-QUALITY-003 | 一項目・一統制・一証跡へ原子化する | 原子性規約 | `update_checklist.py`、検証Skill | 回帰テスト、ID検査 | チェック項目マスター | 予定 |
| REQ-DOCS-001 | docsを日本語に統一する | 日本語生成テンプレート | 文書、`specflow.py`、`standardsflow.py` | 文書言語検査、生成差分検査 | `docs/` | 予定 |
| REQ-WORKBOOK-001 | ワークブックを再現可能かつ軽量にする | 有界集計式 | `update_checklist.py` | 数式検査、読込・描画 | `checklist.xlsx` | 予定 |
| REQ-DISC-001〜004 | 対話で発見し原子的要件として維持する | 正本差分 | `requirements.json`、`specflow.py` | `test_specflow.py` | 要件一覧 | 予定 |
| REQ-FRAME-001、REQ-DESIGN-001〜006、REQ-PORTABLE-001 | 既存要件を意味を保って日本語化しv4.0aへ追随する | 日本語正本表現 | `requirements.json` | 正本スキーマ・生成差分 | 要件一覧 | 予定 |

## 未接続項目

- なし。詳細なファイルとテストは実装完了時に実績へ更新する。
