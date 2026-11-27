# Metrics

This is a genomic-prediction project, so object-detection fields such as mAP and image size do not apply. This project uses the non-detection exception documented in `docs/workflow.md`.

`Pearson` is the correlation between measured and predicted trait values. Higher is better. `MSE` is mean squared prediction error. Lower is better.

| Run | Date | Model | Training -> Evaluation | Samples | SNPs | Repeats | Seed | Pearson Mean | Pearson SD | Spearman Mean | MSE Mean | Paper Reference | Notes |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| brix-gblup-001 | 2026-11-23 | GBLUP | 2022 -> 2022 | 1,935 | 1,822 | 10 | 42 | 0.4024 | 0.0327 | - | - | 0.41 | Within-year 80/20 splits; close reproduction |
| brix-gblup-002 | 2026-11-23 | GBLUP | 2021 -> 2022 | 1,019 | 1,822 | 10 | 42 | 0.3327 | 0.0677 | 0.2876 | 4.2978 | 0.35 | Samples matched across years by plant ID |
| brix-gblup-003 | 2026-11-26 | GBLUP + year fixed effect | 2020–2022 -> 2022 | 2,960 | 1,822 | 10 | 42 | 0.4201 | 0.0457 | 0.4118 | 4.1328 | 0.59 | 1,935 evaluation plants; paper value not reproduced under ID-safe split |
| brix-gblup-004 | 2026-11-26 | GBLUP | 2020–2022 mean -> mean | 2,960 | 1,822 | 10 | 42 | 0.4558 | 0.0320 | 0.4401 | 3.0580 | 0.46 | Author 1000-repeat mean 0.4555; close reproduction |
| acidity-gblup-001 | 2026-11-27 | GBLUP | 2022 -> 2022 | 1,894 | 1,822 | 10 | 42 | 0.4613 | 0.0269 | 0.4672 | 0.0452 | 0.4710 | Close reproduction |
| acidity-gblup-002 | 2026-11-27 | GBLUP | 2021 -> 2022 | 979 | 1,822 | 10 | 42 | 0.3749 | 0.0362 | 0.3789 | 0.0528 | 0.3554 | ID-matched samples; close reproduction |
| acidity-gblup-003 | 2026-11-27 | GBLUP + year fixed effect | 2020–2022 -> 2022 | 2,937 | 1,822 | 10 | 42 | 0.5044 | 0.0338 | 0.5193 | 0.0431 | 0.6449 | 1,894 evaluation plants; author split leakage confirmed |
| acidity-gblup-004 | 2026-11-27 | GBLUP | 2020–2022 mean -> mean | 2,937 | 1,822 | 10 | 42 | 0.5462 | 0.0229 | 0.5657 | 0.0296 | 0.5624 | Close reproduction |
| ph-gblup-001 | 2026-11-27 | GBLUP | 2022 -> 2022 | 1,911 | 1,822 | 10 | 42 | 0.4568 | 0.0559 | 0.4591 | 0.1285 | 0.4594 | Close reproduction |
| ph-gblup-002 | 2026-11-27 | GBLUP | 2021 -> 2022 | 1,004 | 1,822 | 10 | 42 | 0.3809 | 0.0464 | 0.3867 | 0.2274 | 0.3871 | ID-matched samples; close reproduction |
| ph-gblup-003 | 2026-11-27 | GBLUP + year fixed effect | 2020–2022 -> 2022 | 2,955 | 1,822 | 10 | 42 | 0.4824 | 0.0441 | 0.4859 | 0.1438 | 0.6082 | 1,911 evaluation plants; author split leakage confirmed |
| ph-gblup-004 | 2026-11-27 | GBLUP | 2020–2022 mean -> mean | 2,955 | 1,822 | 10 | 42 | 0.5596 | 0.0343 | 0.5650 | 0.1422 | 0.5685 | Close reproduction |

Detailed repeat-level metrics and predictions are committed under [`tables/`](tables/).
