# 保守・変更・廃止計画

## 所有者と保守体制

repository ownerがumbrella skill、bootstrap reference、README/guide、manifest、testsを一体で保守する。

## 依存関係・脆弱性・更新方針

新dependencyなし。Codex skill discovery変更時はofficial docsを確認し、trigger metadataとcopy pathを同一work itemで更新する。

## 互換性・移行方針

chat-first skillはstandalone fallbackを維持する。full runtime schema変更時はumbrella orchestrationとcontract testsを更新する。

## EOL・データ廃棄

skill廃止時はmanifest/inventory/docsから除去する。既導入先はfolder削除で無効化でき、user dataの自動削除はしない。
