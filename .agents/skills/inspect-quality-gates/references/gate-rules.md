# Selected check rules

検査順序と実行場所は対象repositoryへ委任し、このSkillは変更と受入条件に関係する最小の検査だけを選ぶ。

## 選択

- changed path、挙動、risk、生成対象から、失敗を検出できる検査を選ぶ。
- 未選択の検査をN/Aとして列挙しない。
- まずtargeted test、lint、type check、build、generator check等のローカルcommandを使う。
- 既存CIがある場合は同じcommandの追加証拠として参照できる。

## Verdict

- Passは実行command、対象範囲、直接証拠を持つ。
- N/Aは選択後に判明した具体的な適用外理由を持つ。
- blocking Failは修正し、影響する検査だけを再実行する。
- Advisoryは修正、Issue、残存riskのいずれかへ収束させる。

## Boundary

固定phase、専用review YAML、work item、CI workflow、required check、branch protection、merge ruleをこのSkillのために追加または要求しない。結果は会話または対象repositoryが既に採用する変更記録へ簡潔に残す。
