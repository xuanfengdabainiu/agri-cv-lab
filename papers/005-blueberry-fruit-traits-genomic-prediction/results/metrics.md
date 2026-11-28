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
| ratio-gblup-001 | 2026-11-27 | GBLUP | 2022 -> 2022 | 1,907 | 1,822 | 10 | 42 | 0.4634 | 0.0366 | 0.4760 | 218.6009 | - | Local supplemental result; author 1000-repeat reference unavailable |
| ratio-gblup-002 | 2026-11-27 | GBLUP | 2021 -> 2022 | 999 | 1,822 | 10 | 42 | 0.3713 | 0.0577 | 0.3821 | 245.1579 | - | ID-matched local supplemental result |
| ratio-gblup-003 | 2026-11-27 | GBLUP + year fixed effect | 2020–2022 -> 2022 | 2,954 | 1,822 | 10 | 42 | 0.4993 | 0.0353 | 0.5020 | 211.8349 | 0.5992 | Author split leakage confirmed |
| ratio-gblup-004 | 2026-11-27 | GBLUP | 2020–2022 mean -> mean | 2,954 | 1,822 | 10 | 42 | 0.5725 | 0.0318 | 0.5741 | 158.7508 | 0.4960 | Author SD 0.1013; point estimate differs but lies within one SD |
| fruit-mass-gblup-001 | 2026-11-27 | GBLUP | 2022 -> 2022 | 1,846 | 1,822 | 10 | 42 | 0.5973 | 0.0416 | 0.5421 | 84.2294 | 0.5930 | Close reproduction |
| fruit-mass-gblup-002 | 2026-11-27 | GBLUP | 2021 -> 2022 | 969 | 1,822 | 10 | 42 | 0.5612 | 0.0434 | 0.4795 | 90.8891 | - | ID-matched local supplemental result |
| fruit-mass-gblup-003 | 2026-11-27 | GBLUP + year fixed effect | 2020–2022 -> 2022 | 2,945 | 1,822 | 10 | 42 | 0.6317 | 0.0406 | 0.5919 | 79.3455 | 0.7193 | Author split leakage confirmed |
| fruit-mass-gblup-004 | 2026-11-27 | GBLUP | 2020–2022 mean -> mean | 2,945 | 1,822 | 10 | 42 | 0.6666 | 0.0143 | 0.6220 | 66.1570 | 0.6624 | Close reproduction |
| height-gblup-001 | 2026-11-28 | GBLUP | 2022 -> 2022 | 3,830 | 1,822 | 10 | 42 | 0.5897 | 0.0185 | 0.5839 | 332.9831 | 0.5668 | Close reproduction |
| height-gblup-002 | 2026-11-28 | GBLUP | 2021 -> 2022 | 3,604 | 1,822 | 10 | 42 | 0.4780 | 0.0305 | 0.4754 | 582.6515 | 0.4754 | ID-matched; close reproduction |
| height-gblup-003 | 2026-11-28 | GBLUP + year fixed effect | available years -> 2022 | 3,838 | 1,822 | 10 | 42 | 0.6294 | 0.0166 | 0.6226 | 365.6808 | 0.6860 | Only 2021–2022 available; author split leakage confirmed |
| height-gblup-004 | 2026-11-28 | GBLUP | available-years mean -> mean | 3,838 | 1,822 | 10 | 42 | 0.5906 | 0.0104 | 0.5848 | 258.8781 | 0.5845 | Close reproduction |

Detailed repeat-level metrics and predictions are committed under [`tables/`](tables/).
