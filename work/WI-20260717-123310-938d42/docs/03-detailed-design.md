# 詳細設計

## インターフェース

skill triggerはadversarial review、red teaming、robustness、counterexample、mutation/fuzz/prompt injectionとhigh-risk release/mitigation。referencesはresearch、playbook、reportの3つ。

## データモデル

claim、threat model、oracle、campaign case、artifact metadata、finding、repair/retest、bounded conclusionをlogical recordとする。Skills catalogはdirectory nameをprimary keyとする。

## 制御・状態・例外

baseline→portfolio→independent evaluation→classification→repair→unchanged/benign/holdout retest。one high-impact reproducible counterexampleでclaim fail、no findingはbounded statement。

## 認証・認可・入力検証

authorized local/test isolation、synthetic data、no destructive/production/third-party/persistence/exploit disclosure。authority拡張なし。

## 観測可能性

environment/version、seed/generator、budget、expected/actual、minimal reproducer、logs、tested/untested surfaceをreport templateで記録する。

## 移行・互換性

standalone profileでskill folderだけcopy可能。full skills profileにも自動包含。existing skill names/pathは変更しない。
