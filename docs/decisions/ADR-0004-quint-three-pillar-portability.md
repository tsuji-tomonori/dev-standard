# ADR-0004: Quintを一次言語としportable guardrailを3本柱へ限定する

- 状態: Accepted
- Date: 2026-08-27

## 背景

従来の配布profileとこのrepositoryのCIは、要件・設計・品質検査に加えて、review YAML、commit形式、branch topology、merge方式、required checkを一体の契約として扱っていた。これらは導入先ごとにauthorityが異なり、軽量な参照Skillsとしては過剰だった。また、JSON要件とSkill本文だけでは、全体の矛盾、Skill inventoryの漏れ、生成viewのdriftを一つの形式モデルで検査できなかった。

## 決定

1. 永続要件の唯一の編集対象を`spec/requirements/requirements.qnt`とする。
2. 要件JSONをQuintから生成し、人向けMarkdownをそのJSONから生成する。
3. 全18 Skillを`spec/skills/skills.qnt`の契約と1対1で対応させる。
4. portable blocking guardrailを次の3本だけにする。
   - durableな原子要件
   - 実装由来のas-built設計
   - 変更に関係する検査
5. 既定profileは会話entry pointと3本柱の4 Skillだけにする。
6. すべてのportable Skillとprofileは、CI workflow、required check、branch protection、ruleset、merge方式を要求しない。
7. このrepository自身のCIは単一の`verify` jobで形式仕様、unit test、repository整合性だけを検査する。workflow自体は配布しない。

## 検証

`tools/quintflow.py`はQuintのtypecheck、test、simulation、bounded model checkingを実行する。形式不変条件はSkill coverage、3本柱、最小default profile、repository policyのhost ownership、workflow orderを検査する。installer isolation testは、導入先の既存`.github/`内容がbyte一致し、新しいworkflowを作らないことを確認する。

## 結果

- JSONとMarkdownは派生viewになり、直接編集によるauthority分裂を防ぐ。
- default配布は小さくなり、既存repositoryの運用判断を上書きしない。
- auxiliary Skillは必要時に選べるが、新しいportable blocking gateにはならない。
- ADR-0002の二層branch試行は終了し、現行policyではなく履歴として残す。

## 限界

形式検証はモデル化した契約についての保証であり、自然言語の全意味や外部repository設定を絶対的に証明するものではない。Skill本文との1対1 trace、派生生成drift、installer isolation testを併用する。
