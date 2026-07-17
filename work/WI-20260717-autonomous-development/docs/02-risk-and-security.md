# リスク・セキュリティ設計

## 保護対象

- ユーザーが明示した要求と権限境界
- requirements digestと初回承認者・判断
- checklist、証跡、events、approvalsの完全性
- GitHub main branchと公開リポジトリの秘密情報非混入
- skill利用者の自律性、事実境界、意味情報

| 資産 | 機密性 | 完全性 | 可用性 | 根拠 |
|---|---|---|---|---|
| 要件・実行計画 | 低 | 最高 | 高 | 公開可能だが、改変すると権限境界が変わる |
| 初回承認・events | 中 | 最高 | 高 | 人の判断と監査連鎖を保持する |
| checklist・証跡 | 低 | 高 | 高 | 品質判定の根拠になる |
| GitHub main | 低 | 最高 | 高 | 公開標準の正本である |
| skill意味規則 | 低 | 高 | 中 | 誤改変は利用者の意図や主体性を損なう |

## 脅威と対策

| ID | STRIDE | 対応要求 | 脅威 | 影響 | 対策 | 検証 |
|---|---|---|---|---|---|---|
| SEC-001 | S/E | AUT-003, AUT-010 | AIが人の承認を推測・捏造 | 無権限実装 | authorizeは明示されたrequester判断だけを記録 | 未承認gateテスト |
| SEC-002 | T/E | AUT-004, AUT-006 | 承認後に要件・計画を改変 | 権限の後付け拡張 | requirements digest失効、全後続advance/auditで再検査 | plan改変テスト |
| SEC-003 | T/R | AUT-007, NFR-002 | 先行工程を通過後に証跡を改変 | 品質の偽装・否認 | 各advanceで全先行gateを再計算しhash chainを監査 | 先行gate劣化・改ざんテスト |
| SEC-004 | S/E | AUT-011 | 旧承認を新workflowへ流用 | 承認対象の不一致 | schema検査、明示migrate、fresh authorization | legacy migrationテスト |
| SEC-005 | E | AUT-005, NFR-001 | Failを後続の人承認で受容 | 単一承認原則と品質低下 | schema 2のFailを常時blocking | fail blockingテスト |
| SEC-006 | T/E | AUT-010 | Stop hookが悪意ある内容を恒久化 | instruction poisoning | 改善候補はpendingのまま、自動適用commandを廃止 | hook・CLI検査 |
| SEC-007 | I | NFR-003 | PRへ秘密情報や会話transcriptを含める | 情報漏えい | SECURITY、差分検査、合成証跡のみ | staged diff検査 |
| SEC-008 | S | LIS-001〜LIS-004 | 傾聴が読心・診断・迎合へ崩れる | 誤誘導と主体性侵害 | 仮説校正、4層分離、critical failure rubric | 14評価ケース |
| SEC-009 | T | LIS-005〜LIS-008 | 短文化で否定・条件・例外を喪失 | 要件改変 | atomic meaning ledgerとsemantic checksum | 圧縮評価ケース |
| SEC-010 | D | AUT-008 | 自走が停止せず資源を消費する | 作業停滞・費用増加 | 計画の停止条件、ツールtimeout、CI再試行の有界化 | 実行ログ・CI確認 |

STRIDEの六分類を全て検討した。該当しない分類を捨てず、各脅威へS/T/R/I/D/Eを付与した。脅威、要求、対策、検証を同じ行で追跡する。

## 権限

- ローカルファイル変更、テスト、feature branch、PR、CI修正、squash mergeは初回計画で許可済みである。
- 本番環境、課金資源、秘密情報、第三者メッセージ、リポジトリ外データ削除は許可されていない。
- reviewerはread-onlyであり、合否の証跡を提供しても人の初回承認を代行しない。

## データ・プライバシー

個人データまたは顧客データを処理しない。ユーザー会話は要求原文の必要部分だけをwork itemへ保存し、認証情報、ローカルtranscript、非公開データを含めない。研究資料は要約と公開参照URLのみをskillへ収録する。

## 残留リスク

GitHub branch protectionが第三者reviewを強制する場合、エージェント単独ではmergeできない。この場合は無理に迂回せず、PRと成功CIを残して外部権限ブロッカーとして終了する。これは計画に明示済みである。

リスクをFailのまま受容する項目はない。残留リスクは停止条件として扱い、権限を迂回しない。
