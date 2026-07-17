# 保守設計

- OpenAI model guideまたはCodex manualの更新時にmodel availabilityとroutingを再評価する。
- prompt instructionは実測failureを根拠に一群ずつ変更し、同じrepresentative testsを再実行する。
- model/effortを上げる前にmissing success criterion、tool route、verification loopを確認する。
- checklist catalogはpromptから独立してversion管理し、profile/phase選択とfull auditを維持する。
- prompt budget 900、max_threads 3、depth 1の変更は新しいgoverned work itemで扱う。
