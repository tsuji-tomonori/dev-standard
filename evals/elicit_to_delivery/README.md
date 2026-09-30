# Elicit-to-delivery 評価基盤

Phase A5 の是正はfake CLIによる機構検査までとし、モデル呼出しは行わない。Phase B で `gpt-6-luna` の聞き取り・実装品質を評価する。シナリオは架空の情報だけを含み、外部サービスを必要としない。モデル呼出し自体には Codex の認証とネットワークが必要である。

```bash
# Phase B: 監査役がsandbox外のシェルから起動する完全評価
cd <dev-standard repository root>
python evals/elicit_to_delivery/harness.py --scenario stock-web --variant context
python evals/elicit_to_delivery/harness.py --scenario csv-cli --variant context
python evals/elicit_to_delivery/harness.py --scenario booking-api --variant context

# 同じschema/シナリオ/上限で、傾聴やreadinessの指示を渡さない比較対照
python evals/elicit_to_delivery/harness.py --scenario stock-web --variant baseline
python evals/elicit_to_delivery/harness.py --scenario csv-cli --variant baseline
python evals/elicit_to_delivery/harness.py --scenario booking-api --variant baseline

# モデル呼出し無しの機構検査
python -m unittest discover -s tests -p test_elicit_delivery_eval.py -v
```

出力は gitignore 済みの `.devflow/run/elicit-to-delivery/<日時>-<scenario>-<variant>-<pid>-<UUID>/` に保存する。`result.json` が実行状態と集計、`transcript.json` が対話・各ターンのコマンド・製品ファイル増分（新規/変更/削除とSHA-256）、`judge.json` が要件別判定と傾聴採点、`provenance.json` がコピーしたcontextのSHA-256・既知host Skillの除外path・CLI設定と残る限界である。`*.events.jsonl` は CLI の session log、`*.stderr.txt` はエラー、`simulator-*.json` は開示IDと承認を含む評価側情報である。これらの監査用証拠だけをrun終了時に外部領域からコピーする。隠れscenario、再現用`*.prompt.json`、schema、raw envelopeは外部private領域に保持し、場所をresult/provenanceへ記録する。`judge.json`はharnessの証拠検査後の判定であり、降格前のraw出力は外部の`*-judge.last.json`に残る。`product/` に被験成果物、`judge/product/` に再実行用コピーと独立プローブを保存する。隠れシナリオ、対話、生ログ、実行結果を commit しない。

## 保存済みrunの再採点

judgeの時間切れ・証拠形式不備で判定できなかったrunは、監査役が `--rejudge <run_dir>` でjudgeだけを再実行できる。

```bash
# 2回目のcsv-cli / booking-api contextを再採点（モデルを呼ぶので監査役が実行）
for run_dir in .devflow/run/elicit-to-delivery/20260930-233630-{csv-cli,booking-api}-context-*; do
  python evals/elicit_to_delivery/harness.py --rejudge "$run_dir" \
    --judge-call-seconds 1800 --max-seconds 3600 || exit 1
done

# 修正後contextの新規3 run（再採点だけではSkillの効果を測れない）
for scenario in csv-cli booking-api stock-web; do
  python evals/elicit_to_delivery/harness.py --scenario "$scenario" --variant context \
    --call-seconds 300 --delivery-call-seconds 1800 --judge-call-seconds 1800 --max-seconds 3600 || exit 1
done
```

入力は元runの `transcript.json`・`product/` と、`result.json`の `private_workspace` にある `scenario.json`。対話・実装・simulatorは再実行せず、CLIの `--scenario`・`--variant`・`--evaluator-root` による入力置換や現在の公開scenarioの再読込みもしない。承認済みdeliveryがないrunやprivate scenarioが欠けるrunは、旧結果を変更せず起動前に拒否する。smokeの要件集合も保存されたprivate正本を使い、元のsmoke表示を維持する。

`result.pre-rejudge-<日時>-<UUID>.json` と（既存なら）`judge.pre-rejudge-<日時>-<UUID>.json`へ旧結果を保存してから `result.json`・`judge.json` を更新する。元のproduct・transcript・監査・critical/protocol違反・provenanceは保持する。retryの時間上限・calls・elapsedは `result.json`の`rejudges`配列へ追加し、元runの`limits`・`elapsed_seconds`は変更しない。失敗時は現行`judge.json`を残さず、旧集計を消したfailed結果を保存する。成功でもcoverageや聞き取りの違反を修復したとは扱わない。

新judge用コピー・probe・event・stderr・retryのprovenanceと結果は `rejudges/<日時>-<UUID>/`へ保存し、元の `judge/` とログは上書きしない。外部private領域にもretry固有のdirectoryを作り、prompt・schema・raw envelopeを保持する。元のprivate scenarioはrepositoryへコピーしない。probeの実argv・終了値・新規ファイルの照合基準は新規runと共通。judgeがproduct外へprobeを書けば従来通りunverifiedとなる。同じrunへの再採点は順次実行し、旧結果・新結果を監査してから集計する。

## 評価条件と証拠

| シナリオ | 主な観点 |
|---|---|
| `stock-web` | 備品台帳・貸出・返却、閲覧権限、在庫超過、名前の保持期限 |
| `csv-cli` | CSV月別集計、小数・返品・不正行、読取権限、保存禁止、性能 |
| `booking-api` | HTTP予約、時間境界・重複・並列、本人キャンセル、永続化・削除 |

各JSONの `requirements` は隠れ原子要件ID、観測できる受入条件、開示話題を持つ。`traps` はtrigger、自然な発言、修復後のresolutionを持つ。シミュレータがtriggerを適切に扱えたかも対話監査で確認する。同じtriggerでも発言が一度しか出ない保証や確率的再現性はない。

初回被験は専用の空の一時ディレクトリ（/tmp/elicit-subject-*）で始める。評価側は既定で`~/.cache/elicit-eval/<run>/`に置く。`--evaluator-root`で変更できるがrepository内、/tmp直下、被験cwdの祖先・配下・近くを拒否する。simulator/judgeの各呼出し直前にcwdと全祖先の`AGENTS.md`/`AGENTS.override.md`不在を検査し、継承が見つかったら起動せずfailedにする。context版は `elicit-to-delivery` と生成契約 `spec/skills/skills.json` のhard dependenciesによるSkillの依存closure（現在はcalibrated-collaborative-listeningだけ）を `.agents/skills/` にコピーする。optionalなfrontend/3本柱への文章上の参照はコピーしない。先に `python tools/quintflow.py generate` で契約を生成しておく。参照repository全体、CI、契約catalog、installer、quality portalを導入しない。AGENTSは新規ローカル開発のstandaloneモードだけを指定する。baselineにはSkillやAGENTSを置かず、context版と同じJSON応答schemaとそのフィールド説明だけを渡す。schemaの `phase` は測定用の形式であり、baselineへ確認の順番や実装停止条件を教えるものではない。baselineにも同じ計測形式を要求するため、「一切指示のない素のモデル」と完全に同一ではない。

被験は `codex exec -m gpt-6-luna`、利用者シミュレータは `gpt-6.1-sol` と read-only sandbox、独立judgeは `gpt-6.1-sol` と workspace-write sandboxで実行する。モデルはCLI引数で変更可能だが比較時は固定する。`codex exec resume <session_id>` と subprocess のcwdで各会話を継続する。現物の `exec resume --help` に `-s`/`-C` が無いため、sandboxは `-c sandbox_mode="..."` で指定する。ユーザー設定・exec rulesを読み込まず、承認は `never` とする。全roleで `features.multi_agent=false` とし、単体モデルの評価にsubagentを混ぜない。Apps/Plugins/Hooks/Memoriesも無効にして、既知のUSER/ADMIN/CODEX_HOMEのSkillを `skills.config` のpathとenabled=falseで除外する。この設定は当該実行のCLI引数だけに適用し、利用者のconfigは編集しない。承認を自動取得したり sandbox を解除したりしない。

シミュレータは外部private領域のsimulator/の空のcwdと独立した対話sessionを持ち、personaと隠れ要件を初回promptだけで受け取る。聞かれた話題だけを自然に回答し、未質問の話題を示唆・列挙しない。確認サマリには自分の既存発言との矛盾・誤りだけを訂正し、それがなければ未開示の隠れ要件が残っていても承認する。未開示のまま承認された要件はcoverageの欠落として記録する。approvedは「提示された要件サマリで実装・テストへ進むことを承認した」という意味で、実装完了の判定ではない。被験へ渡すのは `reply` だけで、開示IDと承認boolはharness側にとどめる。

`confirmation` でシミュレータが承認した後、被験が `delivery` を返すまで被験へ手番を続け、シミュレータは呼ばない。途中のclarificationにも承認済み範囲で続行を求めるため、重大な新質問が出た評価は監査役が内容を確認する。同じ要件の再確認はprotocol_violationsへ記録しproduct_pass=falseにする。承認前の製品ファイル増分（作成・変更・削除）はphaseによらずcritical_failuresへ記録し停止する。スナップショットは呼出し前後なので、一時的に作成して戻した変更やsandboxに拒否された書込み意図はcommand eventの人による監査で補う。承認前のdelivery、未解決事項の残る承認、不正なJSON、CLI失敗、時間切れ、ターン上限は `status=failed` と理由を保存する。通常は16被験ターン、全体3600秒、対話・simulatorの1呼出し300秒、承認後の被験1呼出し1800秒、独立judgeの1呼出し1800秒。`--max-turns`、`--max-seconds`、`--call-seconds`、`--delivery-call-seconds`、`--judge-call-seconds`で変更できる。各呼出しの上限は全体の残り時間で切り詰める。`--smoke` は同じドメインの5要件へ縮約して罠を除き、8ターン・全体480秒・対話・承認後・judgeとも1呼出し90秒を上限とする。縮約後の正本は外部private領域のscenario.json、対象IDとsmoke=trueはresult.jsonへ記録する。通常の全12要件評価と混ぜて集計しない。タイムアウトはCLIプロセスグループを終了させ、部分ログを残す。smokeの時間切れは機構の成功や製品能力の失敗と断定せず、原因を区別して報告する。

judgeはSkill、Git管理情報、AGENTS.mdを除いた被験成果物のコピーを読み、productコピー内の固定directory `judge_probes/` へ独立したプローブファイルを新規作成し、そのpathを`probe_argv`へ含めて実行し、被験の完了報告にある全テストargvを実際に再実行する。隠れIDごとに `heard_correctly`、`implementation=pass/fail/unverified`、実コマンド・観測・ファイルを根拠として返す。未実行・環境不足はunverifiedとし、読み取りだけでpassにしない。passのprobe argvが終了値0のcompleted command eventの実argvへ直接一致し（CLIのbash/sh -c/-lc wrapperと先頭cd DIR &&だけを限定的に除去）、productコピー内の新しいプローブファイルを含むこと、全報告テストの再実行が実コマンドと終了値に一致することをharnessで検査する。各probeとtestは個別simple commandで実行させる。echo/printfでの言及、pipe、redirect、末尾command連結、shell展開等は実行証拠として認めず、複合commandの終了値を先行probeへ結び付けない。未対応formや新規probe fileの欠落は、該当するpass要件を理由付きunverifiedへ降格する。`evidence_errors`に要件IDと理由を保存し、他の要件を集計してstatus=completedとする。被験testの再実行証拠が欠ける場合もtests_verified=falseと証拠不足の理由を保存し、product_pass=falseにする。CLI失敗・時間切れ・不正なenvelopeなどの機構失敗だけをstatus=failedと区別する。実行証拠の照合基準は緩めない。この整合チェックはプローブの質を保証しないため、監査役がファイルと観測を照合する。

確認サマリに10観点の台帳が各1行あり、回答引用／既定値の値・根拠・誤った場合の影響／非該当理由が実発言と合うかをjudgeが評価する。空欄・未確認・根拠なし、既定値禁止類型の未処置、主要エンティティのCRUD・状態遷移の欠落、サマリ前の開いた否定的シナリオ質問1回の欠落はturn・引用・理由付きのviolationsに記録する。単一利用者でも他に閲覧・操作する人がいないかの確認を点検する。禁止類型は利用者が決める価値判断を対象とし、方針回答後の低リスクな実装細部を根拠付き既定値で示したことは許容する。未回答値を単一候補にした誘導、低リスク細部の個別確認、独立低負担項目の一問ずつの反復も違反欄で理由を点検する。概ね6〜8往復は再判断目安であり、超過だけで違反にしない。[専用rubric](../../.agents/skills/elicit-to-delivery/references/evaluation-rubric.md)をjudgeへ明示入力し、これらの違反0もproduct_passの条件とする。

聞き取りのcoverageは、確認サマリに意味と受入条件が正しく反映された隠れ要件の割合。ID表記そのものの一致は必要ない。質問数・被験ターン数、誤仮定、誘導・前提埋込・二重質問・尋問的負担・訂正無視・承認前実装の引用を採点する。既存 [evaluation-rubric.md](../../.agents/skills/calibrated-collaborative-listening/references/evaluation-rubric.md) の14次元を保持し、coverageと実装の観測を追加する。傾聴基準は22/28以上、Calibration / Clarification / Completeness / Faithfulness が各2、重大違反0を使う。少数の独立した低負担質問をまとめたこと自体は違反とせず、依存関係・負担・二重質問を文脈で評価する。

`status=completed` は聞き取り→承認→実装→独立評価の機構が完了したことを示す。`product_pass` はcoverage=1、全隠れ要件pass、傾聴基準達成、誤仮定・違反0、テスト再実行成功、既知隠れpathアクセス未検出の場合だけtrueとなる。CLIの終了値0は機構完了だけを表し、product_passは `result.json` で確認する。短いsmokeやfake CLIの成功からlunaの品質を主張しない。

隠れ要件の元ファイル・評価用privateディレクトリ・シミュレータcwd・judge workspaceは被験cwdの祖先・兄弟や/tmp直下を避け、repository外の`~/.cache/elicit-eval/<run>/`配下へ置く（judgeはjudge-workspace/product/）。外部private領域・simulator・judgeの既知pathも被験コマンド監査へ含める。隠れシナリオの元ファイルは評価fixtureとしてrepositoryにあるため、その既知pathも監査する。被験のcommand eventで既知pathやファイル名へのアクセスを検出した場合は `audit.status=violation`、広い探索・エンコード等は `inconclusive` とする。read-only sandboxは書込みを制限するだけで、読取りの機密隔離ではない。コマンドログ監査はツール記録の欠落、エンコードされた読取り、ホストのsession/global skill継承を完全に検出しない。`--ignore-user-config` 単独でglobal Skillの探索は止まらないため既知pathを明示除外するが、未知のbundled SYSTEM/managed Skillや管理指示が残る可能性はある。引数の設定だけで「このcontextのみがモデルへ見えた」とは断定せず、provenanceと実sessionメタデータを監査する。`no-known-path-access-detected` は未検出を表し、不正不存在の証明ではない。厳密な隔離評価には、被験から評価側ファイルや他sessionへアクセスできない別OSユーザーまたは別コンテナと独立CODEX_HOMEが必要である。workspace-writeも外部ネットワーク遮断を保証しない。Phase Bでは実コマンドと成果物を監査し、必要ならOS側でネットワークとfilesystemを隔離する。

前セッションのnested Codexでは `app-server socket directory must be a user-owned directory with mode 0700` により製品書込みができなかった。これは被験の実装能力の判定には使わない。Phase Bは監査役がsandbox外のシェルからharnessを起動し、各roleのworkspace-write/read-only sandboxは保持する。認証済みCLI、指定モデル、所有者とmode 0700を満たすsocket directoryが必要である。ソケットやsandboxの制限をharnessで回避しない。失敗時はresult.jsonとstderrを監査する。fake CLIはモデル呼出しなしでresume/承認/プローブ/再実行/失敗保存を検査する。

完全評価は既定で1 run上限60分、対話1呼出し上限5分、承認後の被験とjudgeは各1呼出し上限30分、16被験turn。上記context 3件＋baseline 3件は順次実行で最大約360分（起動・後処理を除く）。聞き取りに多くのroundが必要なら監査役が同条件で両variantの上限を調整する。実時間はモデル待ちと実装規模に依存し、見積りの保証はしない。

Codexの探索範囲とpath指定の無効化は [Build skills](https://learn.chatgpt.com/docs/build-skills)、skills.config と multi-agent/apps/hooks/memories等の設定は [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference) を確認した。使用CLIの `codex exec --help`、`codex exec resume --help`、`codex features list` でも対応オプションを確認している。


並列評価も可能である。同じ秒・同じPIDでもUUIDでrun directoryを分離し、外部private領域・CLI output・resume sessionもrunごとに持つ。harnessは共有lockやcounterを持たない。Codex自体のホスト資源・認証・quotaは共有されるため、比較時は同条件とし必要に応じて並列度を下げる。全6 runを起動して各終了値を確認する例:

```bash
pids=()
for variant in context baseline; do
  for scenario in stock-web csv-cli booking-api; do
    python evals/elicit_to_delivery/harness.py --scenario "$scenario" --variant "$variant" \
      --call-seconds 300 --delivery-call-seconds 1800 --judge-call-seconds 1800 --max-seconds 3600 &
    pids+=("$!")
  done
done
failed=0
for pid in "${pids[@]}"; do
  wait "$pid" || failed=1
done
# failedは機構失敗だけ。各result.jsonのproduct_pass・unverified・violationsを別途監査する。
test "$failed" -eq 0
```
