# Governed AI Development

SWEBOK Guide V4.0を固定参照し、クラウド／AIのWell-Architected観点を加えたチェックリストを、AI駆動開発の工程ゲートとして実行するためのリポジトリです。

Codexの`AGENTS.md`、repo-local skills、custom agents、lifecycle hooksと、決定論的なPythonハーネスを組み合わせます。AIは文書作成とレビューを支援しますが、ユーザーや各責任者の承認を代行しません。

## 保証すること

- ユーザー要望の原文から要求、設計、実装、検証、運用、リリース、振り返りまで成果物を保持する
- 選択プロファイルに含まれるチェック項目を工程へ割り当て、適用／N/A、Pass／Fail、証跡を検査する
- N/Aに根拠、Passに到達可能な証跡、FailにIssueと期限付き例外承認を要求する
- 成果物とレビュー結果のハッシュへ承認を結び付け、承認後の変更を自動失効させる
- 承認・工程イベントをハッシュチェーン付きJSONLで追跡する
- セッション終了時に振り返りを生成し、再発したゲート失敗をskill改善候補へ変換する
- governance-ownerが承認した改善だけを、次のStop hookでskillへ自動反映する

## セットアップ

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python tools/devflow.py catalog --check
.venv/bin/python -m unittest discover -s tests -v
```

Codexで利用する場合は、このリポジトリをtrusted projectとして開き、`/hooks`で`.codex/hooks.json`の内容を確認して信頼してください。skillsは`.agents/skills`、custom agentsは`.codex/agents`から自動検出されます。

## 最初のwork item

```bash
.venv/bin/python tools/devflow.py init \
  --title "ユーザー検索APIを追加" \
  --request "氏名とメールアドレスでユーザーを検索できるAPIがほしい" \
  --profile CORE \
  --profile AWS-DELTA \
  --actor "requester@example.com"
```

出力されたIDを使って、生成された`work/<ID>/docs/`を埋めます。未記入トークンが一つでも残るとゲートは失敗します。

```bash
.venv/bin/python tools/devflow.py inspect --work-item <ID>
```

チェック結果は`work/<ID>/review/checklist-results.json`へ記録します。1件ずつ記録する場合:

```bash
.venv/bin/python tools/devflow.py set-check \
  --work-item <ID> \
  --item REQ-001 \
  --applicability applicable \
  --verdict pass \
  --severity High \
  --reviewer "requirements-reviewer" \
  --evidence "docs/01-requirements.md"
```

ゲート内容が揃った後、実在する責任者が判断を記録します。AIエージェント自身を承認者にしてはいけません。

```bash
.venv/bin/python tools/devflow.py approve \
  --work-item <ID> \
  --decision approved \
  --approver "owner@example.com" \
  --role requester \
  --comment "要求原文、目的、受入条件を確認"

.venv/bin/python tools/devflow.py advance --work-item <ID> --actor "owner@example.com"
```

詳しい工程は[docs/FLOW.md](docs/FLOW.md)、統制モデルは[docs/GOVERNANCE.md](docs/GOVERNANCE.md)、AIへの恒久指示は[AGENTS.md](AGENTS.md)を参照してください。

## チェックリスト参照版

`checklist.xlsx`はSWEBOK Guide V4.0のローカル固定参照版に基づきます。参照PDFそのものは再配布せず、`.workspace/`をGit対象外にしています。オンライン版へ自動追従させず、参照版を変更する場合は別の承認付きwork itemとして扱ってください。

## 検証

```bash
make verify
```

GitHub Actionsでも同じカタログ整合、テスト、リポジトリ構造、ハッシュチェーン監査を実行します。
