---
name: govern-development-request
description: Run a local hash-chained authorization and verification record only when a concrete legal, contractual, safety, production, audit, or explicitly requested lifecycle duty requires it.
---

# Govern Development Request

## Formal specification

`spec/skills/skills.qnt` の `skillContracts` にある `name: "govern-development-request"` を形式契約とする。

形式契約の`applicability`と`activationContexts`に該当しない場合は起動せず、artifactやblocking判定を作らないno-opとする。

このSkillは、具体的な法令、契約、安全性、不可逆production、監査上の義務、または利用者が明示したlifecycle dutyが存在する場合だけ起動する。配布profile、変更規模、technology、security labelだけでは起動しない。

通常のfeature、fix、refactor、文書変更、局所UI変更には使用せず、`$chat-first-development`の軽量な3本柱で処理する。

## 起動条件

次のsignalに加えて、authority、必要な証跡、保持期間、停止条件を定める具体的義務が確認できた場合だけ使用する。

- authentication、authorization、permissions、tenant isolationに関する具体的な統制義務
- confidential情報、PII、data lossに関する具体的な法令・契約・安全義務
- 明示されたirreversible production operation
- 法令、契約、監査上の工程統制
- 明示された高額な外部操作
- 利用者が具体的な証跡と保持範囲を伴うgoverned lifecycleを指定

上記のtechnologyやriskが存在するだけで義務が特定できない場合は起動せず、必要ならauthorityを確認する。

## Regulated outputs

- `work/<id>/regulated/`の義務限定実行記録
- authority boundary
- 一度だけの明示承認
- hash chained approval / event log
- dutyに関係するselected checkのbounded result
- dutyが要求する最小のrelease / audit evidence
- 法令または契約が外部anchorを要求する場合のdigestと参照先handoff

製品要求の正本は引き続き`spec/requirements/requirements.qnt`とし、work itemを製品正本にしない。

## Workflow

1. concrete duty、authority boundary、必要証跡、保持規則、外部anchor要否を特定する。
2. `scripts/regulatedflow.py init`でlocal recordを`active`として作る。
3. 承認主体または対象組織が事前作成したtarget-owned authority evidence JSONを取得する。agentやrunnerが承認内容を作成・補完せず、`authorize`でそのpath、canonical digest、result、scope、effects、rollback、stop conditionsを結合して`authorized`へ遷移する。
4. 承認範囲内で設計、実装、関係するcheckを実行する。追加lifecycle文書が具体的義務に必要な場合だけ`$author-lifecycle-docs`を使う。
5. bounded summary、安全なevidence reference、観測scope / result / effectを`verify`へ渡す。Passだけが`verified`へ進み、Failは`blocked`にする。
6. 実行したローカル検査、既存CI、deployment serviceの結果を必要に応じて参照し、生ログをGitへ複製しない。
7. strict event replayを`check`し、保存stateとの完全一致、authorizationの有効性、直前Pass verificationを確認する。
8. `close`でlocal anchorを固定し、必要な外部anchorはauthorized processへのhandoffとして返す。

法令または契約がreplay-resistantな外部append-only記録を要求する場合、このSkillは最終digestと必要な参照を、対象組織が所有するauthorized audit processへ渡すhandoffとして出力する。このSkill自身は外部recordへ書き込まない。外部記録操作は、別途明示された依頼と権限の下でtarget-owned processが行う。

## Local runner

repository rootから、次の5 commandだけを`init → authorize → verify → close`の順で使用し、任意時点で`check`する。`<host-skill-path>`はinstaller receiptとhost adapterが配置した、このSkillのhost-native rootへ解決し、特定hostのdirectory名を本文へ固定しない。

- `python <host-skill-path>/scripts/regulatedflow.py --root . init --id <id> --duty-kind <law|contract|safety|production|audit|user-mandated> --duty-reference <concrete-reference> --obligation <bounded-obligation> --authority <boundary> --retention <rule> [--external-anchor-required]`
- `python <host-skill-path>/scripts/regulatedflow.py --root . authorize --id <id> --authority-evidence <target-owned-repository-relative.json>`
- `python <host-skill-path>/scripts/regulatedflow.py --root . verify --id <id> --result <pass|fail> --summary <bounded-summary> --observed-scope <scope> --observed-result <result> --observed-effect <effect> --evidence-ref <safe-reference>`（Passでは1件以上必須）
- `python <host-skill-path>/scripts/regulatedflow.py --root . close --id <id>`
- `python <host-skill-path>/scripts/regulatedflow.py --root . check --id <id>`

authority evidenceはexact schema v1のJSON objectとし、`schema_version: 1`、`evidence_kind: "target-owned-authorization"`、`work_id`、`authority_boundary`、`authority_identity`、`approval_reference`、`authorized_scope`、`result_boundary`、`effects`、`rollback`、`stop_conditions`、`expires_at`、`nonce`だけを持つ。repository-relativeな`.json`で、`.devflow/`と`work/<id>/regulated/`の外に事前存在しなければならない。runnerはこれを作成・更新せず、authorize、verify、close、checkの各読込みで同じcanonical内容とdigestを要求する。

runnerはhost-nativeなsibling scriptと`tools/safe_io.py`をno-followで固定読込みし、repository-local lockとCASで`work/<id>/regulated/{state.json,events.jsonl,anchor.json}`を遷移させる。authority evidenceのsnapshotも各authorize / verify / close publicationのread preconditionへ含め、同じpinned rootとlockの内側でpublication直前と全output後に再照合する。途中差替え・削除時はtransition全体をrollbackする。全eventをstrict prefix replayしてstateと完全一致させ、保存stateのstatus、authorization、digest改ざんを拒否する。source、CI設定、外部serviceは変更しない。

## Boundaries

- concrete dutyのない通常変更へこのworkflowを自動適用しない。
- agent、runner、runner-owned stateがauthority evidenceを自己発行、補完、書換えしない。
- 手順、tool、trace pathの可逆な変更だけで再承認を求めない。
- 結果、authority、外部副作用、不可逆性が承認境界を越える場合だけ停止する。
- gateを通すためにcheck、test、型、security controlを弱めない。
- raw production evidence、secret、PII、CIログをGitへ保存しない。
- CI workflow、required check、branch protection、merge ruleをこのSkillのために追加または変更しない。
- 外部append-only recordへ直接書き込まない。

## Completion

- concrete dutyと保持根拠がある。
- authority boundaryと承認が現行である。
- target-owned authority evidenceが事前存在し、eventへ結合した内容から変わっていない。
- dutyに関係するselected checkがPassする。
- 実行範囲に対応する検証が成功する。
- 対象repositoryが採用する変更記録に最終証跡が残る。
- 外部anchor義務がある場合は、最終digestと参照先handoffが返される。
- work itemは規制・監査上必要な期間だけ保持される。

<!-- BEGIN GENERATED QUINT CONTRACT -->
## Quint contract（自動生成）

このblockは`spec/skills/skills.qnt`から生成するviewです。直接編集しません。

- Skill: `govern-development-request`
- 役割: regulated-orchestration
- 柱: auxiliary
- guardrail: no
- repository blocking: no
- 既定portable: no
- 適用条件: when-concrete-duty-exists
- 起動context: `concrete-regulated-duty`
- 外部作用capability: no
- repository policy `ciWorkflow`: false
- repository policy `requiredCheck`: false
- repository policy `branchProtection`: false
- repository policy `ruleset`: false
- repository policy `mergeStrategy`: false
- repository policy `prTemplate`: false
- repository policy `commitFormat`: false
- 前提: a concrete regulated lifecycle duty exists
- 事後条件: regulated evidence strictly binds unchanged pre-existing target-owned authority evidence within that duty and any required external anchor is returned as a handoff
- Authority: concrete-duty-or-user
- 副作用: repository-write
- 失敗状態: stop-at-authority-boundary
- 入力: `concrete-duty-kind`, `concrete-duty-reference`, `bounded-obligation`, `authority-boundary`, `retention-rule`, `pre-existing-target-owned-authority-evidence`
- 出力: `strict-replay-regulated-record`, `local-anchor`, `external-anchor-handoff`
- 義務: `bind-regulated-work-to-concrete-duty`, `consume-and-bind-pre-existing-target-owned-authority-evidence`, `bind-authorization-to-authority-result-effects-rollback-and-stop`, `strictly-replay-init-authorize-verify-close`, `handoff-required-external-anchor`
- 禁止事項: `do not activate from a technology or risk label alone`, `do not apply lifecycle evidence to ordinary work`, `do not self-mint or rewrite authority evidence`, `do not write external audit records`, `do not retain secrets PII or raw production logs`
- 依存Skill: なし
- 必須asset: `references/work-item-contract.md`, `scripts/regulatedflow.py`, `scripts/start.py`
- 要件trace: なし
- manual digest: `8f45357d0b44a87af2bb87661679c6f8c80377ab1dad0982ba79b71d78957210`
- payload digest: `c5906a3efc5407865ee4b2d825332b46a61541613fb33253d573d9d8fe10e1ae`
- interface digest: `9bef3e4b8a30e1c39effdddb1f0101f892ce21ec8a2b468de3bf43f6af507d30`
<!-- END GENERATED QUINT CONTRACT -->
