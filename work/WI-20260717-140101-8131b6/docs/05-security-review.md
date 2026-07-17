# セキュリティ・責任あるAIレビュー結果

## 対象と方法

文書・配布定義のrename。新規runtime、入力、権限、外部通信なし。

## 脅威・脆弱性検証

非該当。Skillはsecurity攻撃検証を別要件なしに開始しないと明記。

## データ・プライバシー検証

データ処理なし。

## AI固有評価

AI reviewerのfalse positive、confirmation bias、人格批判を、独立oracle、証拠要件、誤りは作業仮説という規則で抑制。

## 残余リスク・例外

残余リスクは利用者が`adversarial`をsecurity意味に再解釈すること。descriptionと名称、forbidden-term testで低減。
