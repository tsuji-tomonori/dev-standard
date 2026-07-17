# Portable AI Development Skills and Agents

他のrepositoryへ選択的に移植できるskills、Codex custom agents、governance runtimeのreference collectionです。このrepository自身も同じ配置を使うself-hosting exampleです。

## 使い方: copyして相談するだけ

1. 最小構成では、このrepositoryの`.agents/skills` folderを対象repositoryの`.agents/skills`へcopyします。
2. 対象repositoryをAI development agentで開きます。
3. 「検索が使いにくい」「この画面に絞り込みがほしい」のように、普段の言葉で相談します。

skill名、Python、installer、work item、test commandを指定する必要はありません。AIが導入状態を確認し、曖昧な相談を要件・受入条件・実行計画へまとめます。要件と権限境界を一度だけ自然言語で承認した後は、設計、実装、test、PR作成、CI確認までAIが進めます。

厳密なchecklist、hash付き承認、工程auditも使う場合は、`.agents`に加えて`governance`、`docs/templates`、`tools`、`checklist.xlsx`、`requirements.txt`を同じ相対pathへcopyします。依存準備と内部commandはAIが自動実行します。

## 配置と移植単位

| Collection | Source | Target | Notes |
|---|---|---|---|
| Portable skills | [`.agents/skills`](.agents/skills) | `<target>/.agents/skills` | current repository-scoped skill standard |
| Codex agents | [`.codex/agents`](.codex/agents) | `<target>/.codex/agents` | Codex project custom agents; standalone TOML |
| Codex hooks | [`.codex/hooks`](.codex/hooks) | same path | optional Codex integration |
| Governance runtime | [`governance`](governance), [`tools/devflow.py`](tools/devflow.py), [`docs/templates`](docs/templates), `checklist.xlsx`, `requirements.txt` | same paths | lifecycle skillsの依存runtime |

profile別のcopy対象、依存、config merge、更新方法は[移植ガイド](docs/INSTALLATION.md)、machine-readable mappingは[distribution/manifest.json](distribution/manifest.json)を参照してください。対象固有の`AGENTS.md`と`.codex/config.toml`は上書きせず、AIが既存内容を保ったまま必要部分をmergeします。

## Governance reference

governance profileはSWEBOK Guide V4.0の固定参照とクラウド／AIのWell-Architected観点を工程gateへ適用します。人が最初に要件と自律実行計画を一度だけ承認し、AIはその権限境界内で後続工程を最後まで進めます。

## 保証すること

- ユーザー要望の原文から要求、設計、実装、検証、運用、リリース、振り返りまで成果物を保持する
- 選択プロファイルに含まれるチェック項目を工程へ割り当て、適用／N/A、Pass／Fail、証跡を検査する
- N/Aに根拠、Passに到達可能な証跡、FailにIssueと期限付き例外承認を要求する
- 要件、トレーサビリティ、実行計画、レビュー結果のハッシュへ初回承認を結び付け、承認後の変更を自動失効させる
- 初回承認・工程イベントをハッシュチェーン付きJSONLで追跡する
- 後続工程では人の承認を求めず、全先行品質ゲートと初回承認の有効性を再検査して自律継続する
- セッション終了時に振り返りを生成し、再発したゲート失敗をskill改善候補へ変換する
- 計画外の改善候補は別work itemへ分離し、次の初回承認なしに恒久指示へ反映しない

## AIが内部で行うこと

AIはrepository状態と既存instructionを確認し、必要ならrepository-local environmentと依存を準備します。続いて要求原文、要件、traceability、自律実行計画を生成し、内容を短く提示して一度だけ実行可否を確認します。

承認後は、各工程の文書、check、証跡、testを満たしながら自動で状態を進めます。architecture以降に人の工程承認はありません。要件または実行計画が変わる場合だけ、元の権限境界が失効します。full runtimeをcopyしていない場合も、`chat-first-development`が軽量なwork recordを自動作成し、開発を止めません。

詳しい工程は[docs/FLOW.md](docs/FLOW.md)、統制モデルは[docs/GOVERNANCE.md](docs/GOVERNANCE.md)、AIへの恒久指示は[AGENTS.md](AGENTS.md)、自律境界・minimal prompt・model routingは[docs/AI-OPERATING-POLICY.md](docs/AI-OPERATING-POLICY.md)を参照してください。

## チェックリスト参照版

`checklist.xlsx`はSWEBOK Guide V4.0のローカル固定参照版に基づきます。参照PDFそのものは再配布せず、`.workspace/`をGit対象外にしています。オンライン版へ自動追従させず、参照版を変更する場合は別の承認付きwork itemとして扱ってください。

## 検証

AIが対象repository固有のbuild、test、lint、type checkと、このreferenceのcatalog整合、構造検査、hash chain auditを実行します。GitHub Actionsでも同じ検査を行います。
