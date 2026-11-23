# Metrics

This is a genomic-prediction project, so object-detection fields such as mAP and image size do not apply. This project uses the non-detection exception documented in `docs/workflow.md`.

`Pearson` is the correlation between measured and predicted Brix. Higher is better. `MSE` is mean squared prediction error. Lower is better.

| Run | Date | Model | Training -> Evaluation | Samples | SNPs | Repeats | Seed | Pearson Mean | Pearson SD | Spearman Mean | MSE Mean | Paper Reference | Notes |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| brix-gblup-001 | 2026-11-23 | GBLUP | 2022 -> 2022 | 1,935 | 1,822 | 10 | 42 | 0.4024 | 0.0327 | - | - | 0.41 | Within-year 80/20 splits; close reproduction |
| brix-gblup-002 | 2026-11-23 | GBLUP | 2021 -> 2022 | 1,019 | 1,822 | 10 | 42 | 0.3327 | 0.0677 | 0.2876 | 4.2978 | 0.35 | Samples matched across years by plant ID |

Detailed repeat-level metrics and predictions are committed under [`tables/`](tables/).
