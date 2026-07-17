# アーキテクチャ

## コンテキストと境界

利用者、chat-first umbrella skill、full governance runtime、target repository、GitHubを境界とする。利用者interfaceは自然言語だけ。skillはruntime有無をpreflightし、fullまたはlightweight flowを選択する。

## コンポーネントと責務

| コンポーネント | 責務 | 所有データ | 依存先 | SLO |
|---|---|---|---|---|
| chat-first skill | intent intake、bootstrap、lifecycle orchestration | conversational/work evidence | repository tools | request-to-PR completion |
| full runtime | hash、checklist、phase gate | work state | local Python | deterministic audit |
| lightweight record | runtimeなしの工程証跡 | Markdown work record | repository filesystem | non-blocking fallback |
| GitHub publication | branch、PR、CI | remote refs/checks | GitHub connector | reviewable result |

## データフローと信頼境界

自然言語requestをskillがrequirementsへ変換し、一度のauthorization後にrepositoryへwriteする。full runtimeがあれば内部command、なければMarkdown evidenceを使う。外部writeはPR branchに限定する。

## 可用性・性能・拡張性

常時serviceはなく、requestごとのagent session。skill metadataで広い開発intentを発火させ、progressive referenceでcontext量を抑える。

## 代替案とトレードオフ

Python完全削除はgate integrityを失うため不採用。installer必須もchat-firstに反するため不採用。full runtimeを優先しつつstandalone skill fallbackを採用する。

## 失敗・縮退・復旧

setup失敗はrepository-local範囲で修復する。runtime不足はlightweightへ縮退。GitHub権限不足だけはlocal completionを保全して具体的blockerにする。
