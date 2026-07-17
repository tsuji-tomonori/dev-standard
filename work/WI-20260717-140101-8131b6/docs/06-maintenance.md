# 保守・変更・廃止計画

## 所有者と保守体制

repository owner。研究追加時はsource-to-rule mapとcontract testを同時更新する。

## 依存関係・脆弱性・更新方針

外部package依存なし。リンク切れと研究の再解釈を保守対象とする。

## 互換性・移行方針

folder copy契約を維持。renameは未マージPR内で完結する。

## EOL・データ廃棄

廃止時はfolder、manifest、catalog、tests、参照を同一変更で削除する。データ廃棄なし。
