# Regulated work item contract

具体的な法令、契約、監査、安全性、不可逆production操作、data-loss、高額操作等の義務がある場合だけ、`work/<ID>/regulated/`へ次を置く。

- `state.json`: schema version、ID、duty kind / concrete reference / obligation、authority boundary、retention、現在status、authorization digest、最終event digest。
- `events.jsonl`: sequence、previous digest、event payload、digestを持つlocal hash chain。
- `anchor.json`: close時の最終digestと、外部anchorが必要かを示すlocal record。

追加の文書は`$author-lifecycle-docs`が具体的な利用目的と保持義務を確認した場合だけ作る。全checklist、phase template、execution plan、生ログ、CI結果を一律に複製しない。

## State transition

1. `init`: `law / contract / safety / production / audit / user-mandated`のduty kind、具体的referenceとobligation、authority boundaryから`active`を作る。authentication、PII等のrisk labelだけはobligationとして受理しない。
2. `authorize`: `--authority-evidence <repository-relative.json>`だけを受け取り、承認主体または対象組織が事前作成したauthority identity、approval reference、authorized scope、result、effects、rollback、stop conditions、expiry、nonceをpathとcanonical digestへ結合し、`authorized`を作る。個別scalar引数から承認を組み立てない。
3. `verify`: 実行済みselected verificationのbounded summaryと観測scope / result / effectsを承認境界へ照合し、Passなら`verified`、Failなら`blocked`にする。
4. `close`: strict replay上の直前状態が`verified`で、現行authorizationとPass verificationがある場合だけ`closed`にし、local anchorを固定する。外部からauthorization digestを入力しない。
5. `check`: file identity、schema、event sequence、hash chainをstrict prefix replayし、再構築stateと保存state / anchorの完全一致を検査する。

authority evidenceはexact schema v1のJSON objectで、fieldは`schema_version`、`evidence_kind`、`work_id`、`authority_boundary`、`authority_identity`、`approval_reference`、`authorized_scope`、`result_boundary`、`effects`、`rollback`、`stop_conditions`、`expires_at`、`nonce`だけとする。`schema_version`は`1`、`evidence_kind`は`target-owned-authorization`である。pathはrepository-relativeな`.json`で、`.devflow/`または`work/<ID>/regulated/`配下を拒否する。

runnerはauthority evidenceを作成・変更しない。authorize時にno-followで読んで正規化し、canonical SHA-256を算出する。verify、close、checkでも現在fileを再読し、eventへ結合したpath、内容、digestとの不一致、削除、差替えを拒否する。authorize / verify / closeではevidence snapshotをCASのread preconditionへ加え、同じpinned rootとlockの内側でpublication直前と全output後に再照合し、途中driftならtransition全体をrollbackする。これによりagentやrunner-owned stateから承認を自己発行できない。

各transitionはrepository-local lock、no-follow read、compare-and-swap publicationを使用する。symlink、途中変更、壊れたchain、status飛越し、state / authorization / anchor改ざんを拒否する。

外部append-only recordが必要な場合も、このrunnerは書き込まない。`close`が返す`external_anchor_handoff`を、対象組織が所有する別のauthorized processへ渡す。
