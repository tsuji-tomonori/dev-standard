# コントリビューションガイド

1. `tools/devflow.py init`でwork itemを作成する。
2. 要件、トレーサビリティ、自律実行計画を作成し、要求者の初回承認を一度だけ記録する。
3. [docs/FLOW.md](docs/FLOW.md)の品質ゲートを、追加の工程承認なしで順番に通す。
4. `make verify`を実行する。
5. 目的別にstageし、`.agents/skills/japanese-git-commit-gitmoji/SKILL.md`に従う日本語gitmojiコミットを作成する。
6. Pull Requestにwork item ID、初回承認、ゲート状態、検証結果を記載する。

初回承認や証跡を捏造しないでください。承認後は実行計画の権限境界を拡張しないでください。公開リポジトリへ秘密情報、個人データ、会話トランスクリプト、本番証跡を追加しないでください。
