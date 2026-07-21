## 変更内容

<!-- 何を変更したかを、意味単位で簡潔に記載してください。 -->

## 理由・利用者影響

<!-- なぜ必要か、利用者または開発者にどのような影響があるかを記載してください。 -->

## 変更証跡

- 実行profile: `direct` / `assured` / `regulated`
- 選択理由:
- Review YAML: `governance/reviews/<change-id>.yaml`
- Requirements: `REQ-...` / `none`
- Design-Impact: `none` / `generated` / `adr` / `contract` / `governance` / `mixed`
- 生成設計 / ADR:

- [ ] Commit Commentに目的、変更内容、要件影響、設計影響、review YAML path、検証契約、残存riskを記載した
- [ ] 選択したcheckだけをreview YAMLへ保存し、未選択checkをN/Aとして登録していない
- [ ] CIの生ログやtest reportをrepositoryへ複製していない

## 選択checkと検証

- 変更範囲のtargeted check:
- repository検証: `make verify`
- 外部CI: GitHub Actionsの現在HEAD結果を参照

未選択checkをN/Aとして列挙しない。CI logとtest report本文を貼り付けない。

## Authority boundary

- 外部書込み・production・削除・公開・merge・高額操作: あり / なし
- 必要な承認と記録:

公開API変更だけでは承認を必須にしない。

## 残存リスク・例外

<!-- advisory、未検証環境、互換性、rollback、Issue化した事項を記載してください。 -->

## Regulatedの場合のみ

<!-- direct / assuredでは記入不要です。 -->

- Work item:
- Current/final phase:
- 明示承認の記録:
- [ ] 必要なlifecycle文書、hash chain、phase gate、regulated auditが現在の変更と整合している
