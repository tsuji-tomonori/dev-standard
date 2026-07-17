# 運用設計

運用対象はrepository config、skills、validator、GitHub Actions。常時稼働serviceではない。

- routine reviewはterra low/medium、security/auditはhigh。
- quality failure時だけreasoningを一段上げる。max/xhigh/proや追加agentはdefaultにしない。
- model slugまたはconfig schema変更時はvalidator/testとofficial sourceを同じPRで更新する。
- `make verify`とGitHub checksをrelease gateとし、failureはbranch内で修正する。
- merge後のregressionはrevert PR。force pushとbranch protection回避は禁止。
