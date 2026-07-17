# アーキテクチャ

## コンテキストと境界

Standalone Skill folderを正本とし、chat-first、manifest、Skills catalog、validator/testsを派生統合点とする。runtimeや外部サービスは変更しない。

## コンポーネントと責務

| コンポーネント | 責務 | 所有データ | 依存先 | SLO |
|---|---|---|---|---|
| SKILL.md | トリガー、姿勢、手順、判定規則 | なし | references | N/A |
| references | 研究根拠、challenge matrix、report schema | なし | primary sources | N/A |
| distribution/docs | 移植・発見性 | manifest | Skill folder | N/A |
| tests/validator | 名称・意味・inventoryの回帰防止 | assertions | repository files | N/A |

## データフローと信頼境界

ユーザー意図→Skill contract→references→配布・一覧→tests。機密・外部データなし。

## 可用性・性能・拡張性

静的Markdown/YAML/JSONのみ。性能・可用性SLOは非該当。

## 代替案とトレードオフ

旧名維持は互換的だがsecurity意味との混同が継続するため不採用。`adversarial-review`へ変更する。

## 失敗・縮退・復旧

参照漏れはcatalog equality、manifest profile、install test、rgで検出し、commit revertで復旧する。
