# 保守・変更・廃止計画

## 所有者と保守体制

repository ownerがskill/research map/playbook/report/catalog/validatorを一体保守する。

## 依存関係・脆弱性・更新方針

code dependencyなし。NIST taxonomy、agent attack/evaluator research更新時はsource/rule mapをreviewする。

## 互換性・移行方針

standard `.agents/skills` layoutを維持。skill追加/削除時はmanifestとdocs/SKILLS.mdを同一PRで更新する。

## EOL・データ廃棄

folder removalでdisable可能。historical reports/source citationsは改ざんせず、superseding versionを追加する。
