# アーキテクチャ意思決定記録

| ADR | 決定 | 比較した選択肢 | 根拠 | 影響 | 決定者 | 日付 |
|---|---|---|---|---|---|---|
| ADR-001 | 永続要件正本を`spec/requirements/requirements.json`に置く | work Markdown、DB、JSON | portable、strict、diff可能、標準libraryで処理可能 | generated Markdownは直接編集禁止 | requester authorization | 2026-07-17 |
| ADR-002 | 削除を`retire` tombstoneにする | physical delete | stable ID、判断履歴、traceを保持 | catalogは縮小しない | requester authorization | 2026-07-17 |
| ADR-003 | catalog/item revisionを両方検査する | last-write-wins、catalog revisionのみ | 同時変更と対象itemのlost updateを防ぐ | conflictは再baseが必要 | Codex within plan | 2026-07-17 |
| ADR-004 | FastAPI flowをrouter ASTから生成する | prose、runtime trace | source control下で決定的、decoratorをflowから除外可能 | hidden runtime behaviorは対象外 | requester authorization | 2026-07-17 |
| ADR-005 | SQLGlot ASTでraw SQLを解析する | regex、ORM metadata | parse errorを拒否しCRUD target/readを構造判定 | dialect追加は将来delta | requester authorization | 2026-07-17 |
| ADR-006 | CDK sourceではなくsynth済みCFnを設計入力にする | construct AST、cloud describe API | deployment contractに最も近くofflineで再現可能 | synth自体はtarget build責務 | requester authorization | 2026-07-17 |
| ADR-007 | official source registryへ鮮度期限を持たせる | latest URLのみ、固定snapshotのみ | 再現性とcurrent claimを両立 | 期限後は再調査が必要 | requester authorization | 2026-07-17 |
| ADR-008 | Skills folderだけでlightweight bootstrapを可能にする | installer必須、global install | copy-and-chat要求とtarget isolationを満たす | full auditにはruntime追加copyが必要 | requester authorization | 2026-07-17 |
