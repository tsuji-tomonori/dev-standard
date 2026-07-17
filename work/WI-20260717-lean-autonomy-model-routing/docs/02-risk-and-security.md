# リスク・セキュリティ設計

| Risk | Trigger | Control | Evidence |
|---|---|---|---|
| lean化で制約欠落 | authorization/evidence rule削除 | invariant tests、validator、full audit | tests/test_skills.py |
| lightweight model品質不足 | named check failure | effortを一段上げ、un-pinned rootで再判定 | AI policy routing table |
| agent fan-out cost | 不要なsubagents | max_threads 3、depth 1、bounded read-only delegation | config validator |
| instruction injection | untrusted docをdirective扱い | official docsはevidence、repository policyだけをdirectiveにする | AGENTS boundary |
| external write | PR/merge | initial plan内だけ実行、branch protectionを迂回しない | approvals/event chain |

秘密、個人data、training/RAG dataは追加しない。公式文書は短いparaphraseとURLのみを保存する。
