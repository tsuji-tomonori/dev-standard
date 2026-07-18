# Expansion rules

## Triggers

次の新証拠がある場合だけExpandする。

- acceptanceまたはtargeted verificationが失敗した
- search hit、変更file、domainがestimateを超えた
- public IF、dependency、generated artifactへの影響が判明した
- requirement、design、implementationが矛盾した
- high-riskなのにconfidenceがpolicy閾値未満である
- 初期modelの具体的な能力不足が再現した

## Axis order

原則は`scope → dependencies → verification → review → capability`。一回につき一軸、一段だけ広げる。context不足をmodel引上げで代替しない。capabilityを選べるのは、必要contextとverificationが揃い、同じ原因による能力不足をevidenceで示せる場合だけである。

## Stop

最小の決定的verificationがPassしたら、必須final gate以外は停止する。失敗していない検証を繰り返さず、同じsearch、同じdigest・range、成功logを再読しない。
