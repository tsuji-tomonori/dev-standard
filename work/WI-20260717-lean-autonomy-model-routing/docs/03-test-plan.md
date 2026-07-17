# テスト計画

| Test | Coverage | Pass |
|---|---|---|
| existing devflow 10 tests | single authorization、stale digest、migration、Fail、audit behavior | all pass |
| existing listening 5 tests | semantic preservation、non-sycophancy、skill wiring | all pass |
| model routing test | all 7 agents terra、bounded effort、low verbosity、prompt <=900 | pass |
| AI policy test | outcome/authority/models/validation contract/checklist | pass |
| repository validator | config、agents、policy、templates、hooks | pass |
| full verify | 1,740 catalog、tests、validator、audit | pass |
| GitHub Actions | remote environment regression | required check green |

Negative tests are configuration mutations detected by assertions: wrong model, max threads above 3, missing policy terms, oversized prompt, invalid effort.
