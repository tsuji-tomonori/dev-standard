# リリース判定

## リリース対象

Branch `agent/canonical-spec-design-quality-framework`から作成するGitHub PR。対象は3 portable Skills、self-hosted canonical requirements、official standards registry、generated docs、distribution profiles、templates、tests、CI、reference documentationである。Cloud deploy、package publish、DB migration、main直接pushは対象外。

## 受入条件の充足

- 1: `work/`とcanonical catalogを分離し、14 atomic requirementsをrevision 1として永続化した。
- 2: FastAPI router/functions/OpenAPI/raw SQLとCDK synth CFnからdigest付き設計を生成するframeworkとfixturesを実装した。
- 3: SWEBOK/AWS/Azure/GCP/OCIのofficial source版・check日・refresh期限とevidence verdict contractを実装した。
- Portability: `requirements`、`implementation-design`、`standards-verification`、`development-framework`、`chat-first` profilesをmanifest/test/docsへ追加した。
- Quality: 42 unittest、2 generated checks、repository/catalog/auditがlocal Passした。

## 未解決Issue・例外承認

未解決Issue、Fail、skip、risk exception、期限付きwaiverは0件。CIが失敗した場合はGo判定を撤回し、同branchで修正して全checkを再実行する。

## デプロイ・ロールバック

Deployはない。PR merge後のrepository changeだけがreleaseであり、このwork itemはmerge権限を含まない。RollbackはPR close、merge前branch修正、merge後のrevert PRで行う。Canonical schema/dataを戻す場合も履歴を消すresetではなくforward migrationまたはrevert commitを使う。

## 利用者・運用者への通知

PR本文に正本path、copy profile、generated artifact、dependency、検証結果、scope limitation（FastAPI/CDK）を記載する。README、INSTALLATION、SKILLS、FLOWが利用者向けrelease noteを兼ねる。

## Go / No-Go判断

Local gateはGo。Remote GitHub Actions successとPR diffのsecret-free確認を最終Go条件とする。PR作成後にwork itemのrelease/retrospectiveを監査し、main mergeはrequester判断に残す。
