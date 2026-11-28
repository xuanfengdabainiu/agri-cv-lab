# Fruit Mass Reproduction

## Conclusion

The 2022-only and three-year-average fruit-mass setups closely reproduce the author's public 1000-repeat outputs. The cross-year run is a local supplemental result because no author 1000-repeat reference is available. The ID-safe three-year fixed-effect result is lower than the author reference, and the public design matrix again contains direct 2022-target leakage.

| Mode | This Reproduction | Author 1000-Repeat Mean | Difference | Status |
|---|---:|---:|---:|---|
| 2022 -> 2022 | 0.5973 | 0.5930 | +0.0044 | close |
| 2021 -> 2022 | 0.5612 | not reported | - | local supplemental result |
| 2020–2022 -> 2022, year fixed | 0.6317 | 0.7193 | -0.0876 | not reproduced under ID-safe split |
| 2020–2022 mean -> mean | 0.6666 | 0.6624 | +0.0041 | close |

## Setup

All runs use 1,822 SNP markers, 10 repeated 80/20 splits, seed 42, mean imputation, and `rrBLUP::kin.blup`.

| Mode | Model Genotypes | Evaluation Samples | Test Samples per Repeat |
|---|---:|---:|---:|
| 2022 -> 2022 | 1,846 | 1,846 | 369 |
| 2021 -> 2022 | 969 | 969 | 194 |
| Three-year fixed effect | 2,945 | 1,846 | 369 |
| Three-year average | 2,945 | 2,945 | 589 |

## Reproduction Metrics

| Mode | Pearson Mean | Pearson SD | Spearman Mean | MSE Mean | Heritability Mean |
|---|---:|---:|---:|---:|---:|
| 2022 -> 2022 | 0.5973 | 0.0416 | 0.5421 | 84.2294 | 0.6152 |
| 2021 -> 2022 | 0.5612 | 0.0434 | 0.4795 | 90.8891 | 0.7260 |
| Three-year fixed effect | 0.6317 | 0.0406 | 0.5919 | 79.3455 | 0.5969 |
| Three-year average | 0.6666 | 0.0143 | 0.6220 | 66.1570 | 0.6151 |

All 40 runs completed without missing predictive-ability values.

## Author Split Audit

| Audit Item | Count |
|---|---:|
| Total phenotype rows | 4,790 |
| Unique genotypes | 2,945 |
| Rows labelled test | 589 |
| Unique plant IDs labelled test | 522 |
| Test rows from 2020 | 192 |
| Test rows from 2021 | 193 |
| Test rows from 2022 | 204 |
| Test IDs retaining another training record | 379 |
| Test IDs retaining their 2022 fruit-mass target in training | 197 |

## Output Files

Repeat-level metrics, predictions, and assignments are committed under [`tables/`](tables/):

- `fruit-mass-within-2022-*`
- `fruit-mass-cross-year-*`
- `fruit-mass-3year-fixed-*`
- `fruit-mass-3year-average-*`
- `author-fruit-mass-3year-design-audit.csv`

The three available author 1000-repeat metric tables and public fruit-mass design matrix are committed under [`reference/`](reference/).

Original local runs remain under `D:\science-data\runs\blueberry-fruit-traits-genomic-prediction\fruit-mass-*-seed42`.
