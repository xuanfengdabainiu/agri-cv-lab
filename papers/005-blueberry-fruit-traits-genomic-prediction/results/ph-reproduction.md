# pH Reproduction

## Conclusion

Three of four pH prediction setups closely match the author's public 1000-repeat outputs. The ID-safe three-year fixed-effect result is lower than the author reference, and the public pH design matrix again contains direct 2022-target leakage.

| Mode | This Reproduction | Author 1000-Repeat Mean | Difference | Status |
|---|---:|---:|---:|---|
| 2022 -> 2022 | 0.4568 | 0.4594 | -0.0026 | close |
| 2021 -> 2022 | 0.3809 | 0.3871 | -0.0063 | close |
| 2020–2022 -> 2022, year fixed | 0.4824 | 0.6082 | -0.1258 | not reproduced under ID-safe split |
| 2020–2022 mean -> mean | 0.5596 | 0.5685 | -0.0089 | close |

## Setup

All runs use 1,822 SNP markers, 10 repeated 80/20 splits, seed 42, mean imputation, and `rrBLUP::kin.blup`.

| Mode | Model Genotypes | Evaluation Samples | Test Samples per Repeat |
|---|---:|---:|---:|
| 2022 -> 2022 | 1,911 | 1,911 | 382 |
| 2021 -> 2022 | 1,004 | 1,004 | 201 |
| Three-year fixed effect | 2,955 | 1,911 | 382 |
| Three-year average | 2,955 | 2,955 | 591 |

## Reproduction Metrics

| Mode | Pearson Mean | Pearson SD | Spearman Mean | MSE Mean | Heritability Mean |
|---|---:|---:|---:|---:|---:|
| 2022 -> 2022 | 0.4568 | 0.0559 | 0.4591 | 0.1285 | 0.5403 |
| 2021 -> 2022 | 0.3809 | 0.0464 | 0.3867 | 0.2274 | 0.7336 |
| Three-year fixed effect | 0.4824 | 0.0441 | 0.4859 | 0.1438 | 0.5592 |
| Three-year average | 0.5596 | 0.0343 | 0.5650 | 0.1422 | 0.5852 |

All 40 runs completed without missing predictive-ability values.

## Author Split Audit

| Audit Item | Count |
|---|---:|
| Total phenotype rows | 4,818 |
| Unique genotypes | 2,955 |
| Rows labelled test | 591 |
| Unique plant IDs labelled test | 531 |
| Test rows from 2020 | 191 |
| Test rows from 2021 | 170 |
| Test rows from 2022 | 230 |
| Test IDs retaining another training record | 410 |
| Test IDs retaining their 2022 pH target in training | 209 |

The ID-safe reproduction always removes the selected plant's 2022 pH before fitting. Earlier-year records remain available in the repeated-record model.

## Output Files

Repeat-level metrics, predictions, and assignments are committed under [`tables/`](tables/):

- `ph-within-2022-*`
- `ph-cross-year-*`
- `ph-3year-fixed-*`
- `ph-3year-average-*`
- `author-ph-3year-design-audit.csv`

Author 1000-repeat metrics and the public pH design matrix are committed under [`reference/`](reference/).

Original local runs remain under `D:\science-data\runs\blueberry-fruit-traits-genomic-prediction\ph-*-seed42`.
