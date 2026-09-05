# フロンティアモデルと最小ハーネス

確認日: 2026-09-05。比較対象はGPT-6 Astra、Claude Fable 5.1とClaude Codeの公式ガイド。正本はこのrepositoryの`spec/requirements/requirements.qnt`と`spec/skills/skills.qnt`であり、外部ガイドは改善根拠として扱う。

## 構成の判断

既定配布は会話入口と3本柱の4 Skillを維持する。要件はQuint、現在構造は実装由来の設計、完了証拠は変更に関係する検査で管理する。モデルが高性能になったことを理由に、権限・生成drift・改ざん・配布先の所有権の検査を外さない。

常時読む指示は結果、起動条件、権限境界、非自明な作業知識に絞る。詳細schema、asset一覧、digestは生成catalogへ集約する。任意runnerの内部仕様は、そのrunnerを選んだ場合だけ読む。補助14 Skillはfrontend、標準照合、独立review、具体的な監査義務等の用途があるため保持するが、通常開発へ追加工程として要求しない。`full`は任意の全機能配布であり、推奨の既定構成ではない。

このrepositoryはモデルAPIの会話履歴・thinking block・compactionを操作するagent loopを提供していない。その部分は利用hostの責務とし、モデル固有のAPI制約をportable Skillの必須工程へ持ち込まない。

## 公式根拠と適用範囲

| 資料 | 確認した指針 | このrepositoryでの判断 |
|---|---|---|
| [OpenAI: GPT-6 Astra model guidance](https://developers.openai.com/api/docs/guides/latest-model) | 指示への感度、不要な承認停止、過剰な検査を点検する | 有効な承認を再利用し、検査の拡大は具体的な失敗・riskに結び付ける |
| [Anthropic: Prompting Claude Fable 5.1](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1) | 完了までの継続、独立toolの一括実行、変更・testの範囲管理、effortの再評価 | 対象環境の設定を優先し、全reviewerの推論強度を固定しない。履歴のappend-only制約はAPI統合時の事項とする |
| [Anthropic: Prompting Claude Fable 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5) | 旧モデル向けの細かな手順が品質を下げ得る | 世代差の背景資料として使用。固定の会話手順や常時の計測記録を外す。5.1の挙動は5.1の資料で確認する |
| [Claude Code: Best practices](https://code.claude.com/docs/en/best-practices) | 起動時指示を短くし、検証方法を与え、用途固有の知識を必要時に読む | 契約全文の重複表示を削減し、検査commandと実行境界を保持する |
| [Anthropic: Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | 簡潔さ、適切な自由度、段階的な参照、実利用での評価 | 研究根拠の全件読込みを通常reviewの前提にせず、複雑なrunnerだけ参照を分離する |
| [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills) | 用途が明確なSkillと必要に応じた読込み | 会話入口から該当する柱だけを使用し、専門Skillの一律起動を避ける |

## 指摘と対応

| ID | 箇所 | 重大度 | 問題 | 根拠 | 影響 | 修正 | 確認方法 |
|---|---|---|---|---|---|---|---|
| F1 | 全SKILL.md、render_skills | Major | 詳細契約とdigestが各入口とcatalogで重複 | REQ-QUINT-003、上記Skill公式資料 | 読込み増加 | 入口は起動・実行境界、詳細は生成catalogへ集約 | 全field保存、binding/drift検査、両host配布test |
| F2 | authorize、chat-first | Major | 毎回approveを得る手順が既存承認の再利用と矛盾 | REQ-PORTABLE-003、Astra/Fable 5.1 | 不要な停止 | 有効な同一対象の承認は再利用。不足時だけ確認 | 承認あり・なし・失効・範囲外の境界照合 |
| F3 | inspect、right-size | Major | 任意runnerの内部仕様・停止digestが通常手順に混在 | REQ-QUALITY-004、REQ-EXEC-008 | 余分な記録と検査 | runner選択時だけ詳細参照 | runner回帰検査、通常変更のシナリオ確認 |
| F4 | .codex、validator、配布snippet | Minor | 未使用hooks、固定の3並列上限と推論強度 | モデル固有の評価根拠なし、Fable 5.1のeffort再評価指針 | hostの判断を固定 | 未使用設定と数値上限検査を削除。read-only reviewerは維持 | host生成、配布隔離test |
| F5 | review、listening、frontend test | Minor | 研究資料の先行読込み、固定会話手順、別Skillへの修正引継ぎが過剰 | 明示依頼の範囲、公式Skill指針 | 作業遅延 | 必要時の参照と既存実装権限内の修正へ整理 | 指示照合、対象シナリオ |
| F6 | CONTRIBUTING | Minor | 小変更にもmake verifyを一律要求 | AGENTS.md、3本目の柱 | 過剰な検証 | 全体契約の変更時だけmake verify | repository指示との照合 |

| F7 | chat-first frontmatter、validator | Major | descriptionの未引用colonがYAML構文エラーなのに行分割parserが受理 | Skill形式契約、公式Skill仕様 | hostが入口Skillを読めない可能性 | 有効なdescriptionへ修正し、実YAML parserで検証 | 引用colon・複数行の受理、不正colon・非文字列の拒否test |

## 検証と限界

形式検証は既存の探索範囲を保ち、契約のfield/type、3 blocker、4 default Skill、依存closure、digest、生成drift、host policyの非変更を確認する。任意runnerの実行・失敗・権限・改ざんに対する回帰検査も維持する。検査は権限や安全性のすべてを証明するものではない。

今回の調査は公式文書との整合確認であり、AstraとFable 5.1を同一課題で比較した実測benchmarkではない。入口の文字量削減を、token費用や成功率の改善率へ換算しない。採用host・モデルを変更する際は、代表的な小変更、複雑な変更、承認境界の課題で結果・不要停止・検証範囲を確認し、観測した問題だけを修正する。
