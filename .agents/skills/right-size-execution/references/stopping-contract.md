# 停止契約

成功条件、required verification、assurance floorを満たした時点で、必須の確定処理以外を停止します。

成功後に許可する操作:

- 実績reportとdigestの確定
- 明示的に選ばれたauditの確定
- 対象repositoryが選んだremote check結果の記録
- 別途権限がある確定処理

成功後に禁止する操作:

- 念のための追加検索や全ファイル走査
- 全量ログ読取
- 根拠のない追加reviewまたはcompute引上げ
- 同一digest・同一rangeの再読

状態機械は成功後の正のコスト活動を`post_success_activity`として残し、shadow modeでは警告します。停止digestは検証projection、assurance、selector manifest、全拡張chainを結びます。
