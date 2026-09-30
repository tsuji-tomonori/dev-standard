---
name: elicit-to-delivery
description: Turn an underspecified new app or system request into confirmed, testable requirements, then complete implementation, tests, and reporting. Use when missing information materially changes the outcome; not for routine changes with sufficient requirements.
---

# Elicit to Delivery

形式契約: `spec/skills/skills.qnt`の`name: "elicit-to-delivery"`（保守・監査時に参照）。

新規アプリ・システムの「こんな感じ」という依頼から、利用者が訂正できる要件を確定し、承認範囲で実装・テスト・修正・報告まで完了する補助Skill。既定portable setや3本柱へblocking guardrailを追加しない。

## 対話から確認へ

1. **最初の応答を作る前に**[readiness-and-summary.md](references/readiness-and-summary.md)と[interview.md](references/interview.md)を必ず読む。対象repositoryの規則・既存要件から明示情報・推測・不足を分け、既存傾聴Skillの意味保存・訂正可能性を使う。UI固有の不足がある場合だけfrontend聞き取りSkillを合成する。
2. **利用者が要件サマリへ明示的に承認するまで、製品ファイル・テスト・scaffoldを作成・変更せず、依存導入もしない。**読み取り調査はできる。自分で「確定した」と宣言することは承認ではない。
3. 最初は目的と直近の具体例を開いて聞く（[ED-R06/R09](references/evidence-map.md)）。以後は未処置の**利用者が決める価値判断**だけを質問する。既定値禁止類型でも方針が分かった後の低リスクな実装細部は個別確認せず、サマリの既定値台帳（値・根拠・誤った場合の影響）へ置く。主要エンティティのCRUD・状態遷移も走査する。
4. 独立した低負担項目が複数残るときは**最大3問をまとめる**。依存する問い・価値衝突・矛盾修復は1問ずつ。未回答の値を一つ埋め込む「〜でしょうか／〜でよいですか」は使わず、開いた質問か偏りのない複数選択肢＋「それ以外」にする。小規模アプリは目的・例→重要類型→締め→サマリを概ね6〜8往復以内で進める目安とし、超えそうなら一括化・既定値化を再判断する（[ED-L05](references/evidence-map.md): 上限でも研究上の最適回数でもない）。
5. 停止規則: 10観点すべてに根拠付き処置があり、要件が原子的・整合的・実行可能・検証可能、未解決blockerが空なら、サマリ直前に「起きると困ること・やってはいけないこと」を開いた質問で1回聞く（ED-L04）。回答の不足を処置後、確認サマリに10観点の台帳を各1行で必ず出す: 確認済み（回答の短い引用）／既定値（値・根拠・誤った場合の影響）／非該当（理由）。空欄・未確認は不可。ID・受入条件・スコープ外・未解決事項（空）もまとめ、内容とローカル実装・テスト範囲を一度確認する。沈黙・時間経過を承認にしない。この同じ要件への明示承認が既にあれば再承認を求めない。

カバレッジ観点: 目的、利用者・権限、主要シナリオ、例外・空・境界、データ・保持、外部I/F、品質、制約、スコープ外、受入。停止判断の研究背景は[ED-R08](references/evidence-map.md)、具体的な開始条件はローカル方針ED-L01による。

## 確認から納品へ

**承認後、実装開始前に**[delivery-and-report.md](references/delivery-and-report.md)を必ず読む。durable obligationを対象正本へ反映し、実装・各受入条件のテスト・失敗修正を完了まで回す。Dev標準導入済みなら3本柱へhandoffし、空repositoryの扱いはreadiness参照に従う。

可逆な実装詳細には既存規約と確認済み既定値を使い、追加許可を要求しない。新事実が承認済み成果・重要制約・利用者の価値選択・権限を変える場合だけ該当作業を止め、影響と最小の質問を返す。独立作業は継続する。外部書込み・公開・merge・production・破壊的削除・高額操作は個別の明示権限に従う。

テスト・型・lint・security controlを弱めず、実行できない検査を成功扱いしない。実装、要件ID↔実test結果、仮定、未検証範囲・残存リスク、起動方法を報告する。モデル単体の完全実装能力をSkill配置や静的検査だけで保証しない。

保守時だけ[evidence-map.md](references/evidence-map.md)、評価時だけ[evaluation-rubric.md](references/evaluation-rubric.md)を読む。transcript・生ログはportable成果へ含めず、再開に必要な一時情報だけgitignoreされた`.devflow/run/`へ置く。

<!-- BEGIN GENERATED QUINT CONTRACT -->
## Quint contract（自動生成）

このblockは`spec/skills/skills.qnt`から自動生成し、直接編集しません。
詳細・要件trace・digestは`spec/skills/skills.json`の同名契約を、契約の保守・監査時だけ参照します。
repository policyは導入先が所有します。非該当ならartifactやblocking判定を作りません。

- Skill: `elicit-to-delivery`
- 柱: auxiliary
- repository blocking: no
- 既定portable: no
- 適用条件: when-new-system-request-has-material-gaps
- 起動context: `new-system-material-gaps`
- 外部作用capability: no
- Authority: user-and-target-repository
- 副作用: repository-write
- 失敗状態: return-for-clarification
<!-- END GENERATED QUINT CONTRACT -->
