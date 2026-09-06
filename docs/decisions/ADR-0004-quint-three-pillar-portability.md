# ADR-0004: Quintを一次言語としportable guardrailを3本柱へ限定する

- 状態: Accepted
- Date: 2026-08-27

## 背景

従来の固定実行分類とこのrepositoryのCIは、要件・設計・品質検査に加えて、review YAML、commit形式、branch topology、merge方式、required checkを一体の契約として扱っていた。これらは導入先ごとにauthorityが異なり、軽量な参照Skillsとしては過剰だった。また、JSON要件とSkill本文だけでは、モデル化した契約の構造矛盾、Skill inventoryの漏れ、生成viewのdriftを一つの検査経路で発見できなかった。

## 決定

1. 永続要件の唯一の編集対象を`spec/requirements/requirements.qnt`とする。
2. 要件JSONをQuintから生成し、人向けMarkdownをそのJSONから生成する。
3. 全Skillを`spec/skills/skills.qnt`の契約と1対1で対応させる。
4. portable blocking guardrailを次の3本だけにする。
   - durableな原子要件
   - 実装由来のas-built設計
   - 変更に関係する検査
5. 既定portable setは会話entry pointと3本柱の4 Skillだけにする。補助Skillは列挙された`activationContexts`に該当するときだけ起動し、4本目のblocking gateにしない。
6. すべてのportable Skillは、型付きの7つのrepository policy fieldをfalseとし、CI workflow、required check、branch protection、ruleset、merge方式、PR template、commit形式を要求しない。
7. このrepository自身のCIは単一の`verify` jobで形式仕様、unit test、repository整合性だけを検査する。workflow自体は配布しない。

## 検証

`tools/quintflow.py`はQuintのtypecheck、test、simulationに加え、要件正本と配布templateを4 step、Skill契約を3 stepでApalache bounded model checkingする。`make verify`とこのrepository自身の既存workflowはbounded model checkingを含む。形式不変条件はSkill coverage、3本柱、最小default portable set、repository policyのhost ownership、runner副作用境界、該当・非該当を含むworkflow orderを検査する。policy変更要求からhost-owned rejectionへ到達する遷移も実行する。installer isolation testは、既知のprotected pathを拒否し、導入先の既存`.github/`内容がbyte一致することを確認する。この検査構成はdev-standard自身の保守契約であり、導入先でのbounded検証は任意とし、portable manifestへworkflowやrequired checkとして配布しない。

## 結果

- JSONとMarkdownは派生viewになり、直接編集によるdriftを検出してauthority分裂のリスクを下げる。
- default配布は小さくなり、既存repositoryの運用判断を上書きしない。
- auxiliary Skillは必要時に選べるが、新しいportable blocking gateにはならない。
- ADR-0002の二層branch試行は終了し、現行policyではなく履歴として残す。

## 限界

形式検証はモデル化した契約と、要件正本・配布templateで4 step、Skill契約で3 stepまで探索した状態についての証拠であり、到達可能な全状態、自然言語の全意味、外部repository設定を絶対的に証明するものではない。Skill本文の独立review、digestによるbyte binding、派生生成drift、policy mutation test、installer isolation testを併用する。
