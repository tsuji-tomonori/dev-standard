# 詳細設計

## インターフェース

frontmatter名/descriptionを自動trigger契約とし、bodyはprepare→workflow→decision rules→boundaries。referencesはresearch-basis、challenge-playbook、report-template。

## データモデル

manifest inventory/profile、docs table、test expected setは`adversarial-review`で一致させる。

## 制御・状態・例外

レビューはclaim extraction→independent derivation→perspective passes→counterexample→evidence verdict→repair/retest。根拠不足は欠陥断定せずunresolved question。

## 認証・認可・入力検証

runtime入力なし。権限変更なし。security red teamingを別要件なしに開始しない。

## 観測可能性

再現可能なclaim/evidence/statusをreport templateへ残す。

## 移行・互換性

未マージPR内のrenameのため移行shimなし。全repository参照を同時更新する。
