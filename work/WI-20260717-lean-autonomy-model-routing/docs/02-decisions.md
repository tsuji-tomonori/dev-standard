# 意思決定記録

## ADR-1 Rootをpinしない

GPT-5.6はunderlying intentを推論でき、詳細手順が少ないほど効率が上がる。rootはtask難度に応じた選択を許し、独創性とquality escalationを保持する。

## ADR-2 Reviewerはterra

Codex manualが軽いsubagentへ`gpt-5.6-terra`を推奨するため採用。API guideの`luna`はhigh-volume API向けとして文書化するが、Codex custom agentへはpinしない。

## ADR-3 Checklistはpromptではなくvalidation contract

1,740項目をpromptへ複製せず、profile/current phaseで選択しdevflowに記録する。qualityは項目数削減でなくdeterministic inspectionとauditで維持する。
