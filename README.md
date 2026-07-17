# Governed AI Development

SWEBOK Guide V4.0を固定参照し、クラウド／AIのWell-Architected観点を加えたチェックリストを、AI駆動開発の工程ゲートとして実行するためのリポジトリです。

Codexの`AGENTS.md`、repo-local skills、custom agents、lifecycle hooksと、決定論的なPythonハーネスを組み合わせます。人が最初に要件と自律実行計画を一度だけ承認し、AIはその権限境界内で後続工程を最後まで進めます。

## 保証すること

- ユーザー要望の原文から要求、設計、実装、検証、運用、リリース、振り返りまで成果物を保持する
- 選択プロファイルに含まれるチェック項目を工程へ割り当て、適用／N/A、Pass／Fail、証跡を検査する
- N/Aに根拠、Passに到達可能な証跡、FailにIssueと期限付き例外承認を要求する
- 要件、トレーサビリティ、実行計画、レビュー結果のハッシュへ初回承認を結び付け、承認後の変更を自動失効させる
- 初回承認・工程イベントをハッシュチェーン付きJSONLで追跡する
- 後続工程では人の承認を求めず、全先行品質ゲートと初回承認の有効性を再検査して自律継続する
- セッション終了時に振り返りを生成し、再発したゲート失敗をskill改善候補へ変換する
- 計画外の改善候補は別work itemへ分離し、次の初回承認なしに恒久指示へ反映しない

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

要求原文を保存した後、要件、トレーサビリティ、自律実行計画を完成させます。内容検査が通ったら、要求者が一度だけ実行可否を判断します。AIエージェント自身を承認者にしてはいけません。

```bash
.venv/bin/python tools/devflow.py authorize \
  --work-item <ID> \
  --decision approved \
  --approver "owner@example.com" \
  --comment "要件、実行計画、権限境界、完了条件を確認"

.venv/bin/python tools/devflow.py advance --work-item <ID> --actor "owner@example.com"
```

承認後は、各工程の文書、チェック、証跡、テストを満たして`advance`を続けます。architecture以降に人の工程承認はありません。要件または実行計画が変わると初回承認が失効し、後続工程は停止します。

詳しい工程は[docs/FLOW.md](docs/FLOW.md)、統制モデルは[docs/GOVERNANCE.md](docs/GOVERNANCE.md)、AIへの恒久指示は[AGENTS.md](AGENTS.md)、自律境界・lean prompt・model routingは[docs/AI-OPERATING-POLICY.md](docs/AI-OPERATING-POLICY.md)を参照してください。

## チェックリスト参照版

`checklist.xlsx`はSWEBOK Guide V4.0のローカル固定参照版に基づきます。参照PDFそのものは再配布せず、`.workspace/`をGit対象外にしています。オンライン版へ自動追従させず、参照版を変更する場合は別の承認付きwork itemとして扱ってください。

## 検証

```bash
make verify
```

GitHub Actionsでも同じカタログ整合、テスト、リポジトリ構造、ハッシュチェーン監査を実行します。
