# Brix-to-Acidity Ratio Reproduction

## Conclusion

The paper provides 1000-repeat references only for the three-year fixed-effect and three-year-average ratio setups. The ID-safe fixed-effect result is lower than the author reference, and the public design matrix contains direct 2022-target leakage. The averaged result is higher than the author mean but remains within one author-reported standard deviation because the author output is highly variable.

| Mode | This Reproduction | Author 1000-Repeat Mean | Difference | Status |
|---|---:|---:|---:|---|
| 2022 -> 2022 | 0.4634 | not reported | - | local supplemental result |
| 2021 -> 2022 | 0.3713 | not reported | - | local supplemental result |
| 2020–2022 -> 2022, year fixed | 0.4993 | 0.5992 | -0.0999 | not reproduced under ID-safe split |
| 2020–2022 mean -> mean | 0.5725 | 0.4960 | +0.0765 | point estimate differs; within author SD 0.1013 |

## Setup

All runs use 1,822 SNP markers, 10 repeated 80/20 splits, seed 42, mean imputation, and `rrBLUP::kin.blup`.

| Mode | Model Genotypes | Evaluation Samples | Test Samples per Repeat |
|---|---:|---:|---:|
| 2022 -> 2022 | 1,907 | 1,907 | 381 |
| 2021 -> 2022 | 999 | 999 | 200 |
| Three-year fixed effect | 2,954 | 1,907 | 381 |
| Three-year average | 2,954 | 2,954 | 591 |

## Reproduction Metrics

| Mode | Pearson Mean | Pearson SD | Spearman Mean | MSE Mean | Heritability Mean |
|---|---:|---:|---:|---:|---:|
| 2022 -> 2022 | 0.4634 | 0.0366 | 0.4760 | 218.6009 | 0.5376 |
| 2021 -> 2022 | 0.3713 | 0.0577 | 0.3821 | 245.1579 | 0.7267 |
| Three-year fixed effect | 0.4993 | 0.0353 | 0.5020 | 211.8349 | 0.5876 |
| Three-year average | 0.5725 | 0.0318 | 0.5741 | 158.7508 | 0.6007 |

All 40 runs completed without missing predictive-ability values.

## Author Split Audit

| Audit Item | Count |
|---|---:|
| Total phenotype rows | 4,813 |
| Unique genotypes | 2,954 |
| Rows labelled test | 591 |
| Unique plant IDs labelled test | 525 |
| Test rows from 2020 | 185 |
| Test rows from 2021 | 180 |
| Test rows from 2022 | 226 |
| Test IDs retaining another training record | 378 |
| Test IDs retaining their 2022 ratio target in training | 191 |

## Output Files

Repeat-level metrics, predictions, and assignments are committed under [`tables/`](tables/):

- `ratio-within-2022-*`
- `ratio-cross-year-*`
- `ratio-3year-fixed-*`
- `ratio-3year-average-*`
- `author-ratio-3year-design-audit.csv`

The two available author 1000-repeat metric tables and public ratio design matrix are committed under [`reference/`](reference/).

Original local runs remain under `D:\science-data\runs\blueberry-fruit-traits-genomic-prediction\ratio-*-seed42`.
