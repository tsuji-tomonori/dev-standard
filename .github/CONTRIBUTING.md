# Contributing

変更は、対象と受入条件に対応する最小範囲にしてください。

1. durableな要件が変わる場合は`spec/requirements/requirements.qnt`を更新する。
2. Skill契約が変わる場合は`spec/skills/skills.qnt`と対応する`SKILL.md`を更新する。
3. `python tools/quintflow.py generate`でJSONとMarkdownを再生成する。
4. 変更に関係する検査を実行する。repository全体の契約を変える場合は`make verify`を使う。
5. GitHubの現在のrepository設定に従ってPull Requestを作成する。

特定のbranch構成、merge方式、commit形式はこの文書では定義しません。workflow、branch policy、生ログ、repository固有のreview recordをportable profileへ追加しないでください。
