# Brix GBLUP Baseline: Seed 42

## Conclusion

The 2022 Brix GBLUP baseline reached a mean predictive ability of **0.4024**, close to the paper's reported value of approximately **0.41** for its 2022 training set.

Predictive ability is the correlation between measured and predicted Brix. Higher is better, with 1 representing a perfect positive relationship.

## Setup

| Setting | Value |
|---|---|
| Model | GBLUP (`rrBLUP::kin.blup`) |
| Target | `Brix_2022` |
| Matched samples | 1,935 |
| SNP markers | 1,822 |
| Split | 80% train / 20% test |
| Repeats | 10 |
| Seed | 42 |
| Samples per repeat | 1,548 train / 387 test |

## Results

| Repeat | Predictive Ability |
|---:|---:|
| 1 | 0.3732 |
| 2 | 0.3796 |
| 3 | 0.4051 |
| 4 | 0.4474 |
| 5 | 0.4266 |
| 6 | 0.3906 |
| 7 | 0.4051 |
| 8 | 0.3701 |
| 9 | 0.3671 |
| 10 | 0.4590 |

| Summary | Value |
|---|---:|
| Mean | 0.4024 |
| Standard deviation | 0.0327 |
| Minimum | 0.3671 |
| Maximum | 0.4590 |

All 10 repeats completed. The prediction table contains 3,870 rows and no predictive-ability value is missing.

## Output Files

Small result tables are committed to GitHub:

- [`tables/brix-gblup-seed42-metrics.csv`](tables/brix-gblup-seed42-metrics.csv)
- [`tables/brix-gblup-seed42-predictions.csv`](tables/brix-gblup-seed42-predictions.csv)

The original run directory remains at `D:\science-data\runs\blueberry-brix-genomic-prediction\brix-gblup-seed42`.

SHA-256:

- Metrics: `09CB95EAEEE3A4F8EC6A90B383C4A18320FBF32237887D38C08D1131BB7C60F8`
- Predictions: `EA9C4488291C72921154C85BBF845F396ADEF54E3A843B27D6F304147681775B`

## Note

`rrBLUP` detected linear dependence among genotype rows and automatically used mean imputation instead of EM imputation. The run completed normally. This behavior is recorded because it changes the effective imputation method.
