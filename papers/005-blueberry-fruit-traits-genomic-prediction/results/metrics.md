# Metrics

This is a genomic-prediction project, so object-detection fields such as mAP and image size do not apply. This project uses the non-detection exception documented in `docs/workflow.md`.

`Pearson` is the correlation between measured and predicted Brix. Higher is better. `MSE` is mean squared prediction error. Lower is better.

| Run | Date | Model | Training -> Evaluation | Samples | SNPs | Repeats | Seed | Pearson Mean | Pearson SD | Spearman Mean | MSE Mean | Paper Reference | Notes |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| brix-gblup-001 | 2026-11-23 | GBLUP | 2022 -> 2022 | 1,935 | 1,822 | 10 | 42 | 0.4024 | 0.0327 | - | - | 0.41 | Within-year 80/20 splits; close reproduction |
| brix-gblup-002 | 2026-11-23 | GBLUP | 2021 -> 2022 | 1,019 | 1,822 | 10 | 42 | 0.3327 | 0.0677 | 0.2876 | 4.2978 | 0.35 | Samples matched across years by plant ID |
| brix-gblup-003 | 2026-11-26 | GBLUP + year fixed effect | 2020–2022 -> 2022 | 2,960 | 1,822 | 10 | 42 | 0.4201 | 0.0457 | 0.4118 | 4.1328 | 0.59 | 1,935 evaluation plants; paper value not reproduced under ID-safe split |
| brix-gblup-004 | 2026-11-26 | GBLUP | 2020–2022 mean -> mean | 2,960 | 1,822 | 10 | 42 | 0.4558 | 0.0320 | 0.4401 | 3.0580 | 0.46 | Author 1000-repeat mean 0.4555; close reproduction |

Detailed repeat-level metrics and predictions are committed under [`tables/`](tables/).
