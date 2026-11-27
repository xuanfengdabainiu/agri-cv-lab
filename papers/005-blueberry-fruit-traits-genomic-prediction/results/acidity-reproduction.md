# Titratable Acidity Reproduction

## Conclusion

Three of four titratable-acidity prediction setups closely match the author's public 1000-repeat outputs. The ID-safe three-year fixed-effect result is lower than the paper, and the author's public design matrix shows the same direct target-leakage pattern found for Brix.

| Mode | This Reproduction | Author 1000-Repeat Mean | Difference | Status |
|---|---:|---:|---:|---|
| 2022 -> 2022 | 0.4613 | 0.4710 | -0.0097 | close |
| 2021 -> 2022 | 0.3749 | 0.3554 | +0.0194 | close |
| 2020–2022 -> 2022, year fixed | 0.5044 | 0.6449 | -0.1405 | not reproduced under ID-safe split |
| 2020–2022 mean -> mean | 0.5462 | 0.5624 | -0.0162 | close |

## Setup

All runs use 1,822 SNP markers, 10 repeated 80/20 splits, seed 42, mean imputation, and `rrBLUP::kin.blup`.

| Mode | Model Genotypes | Evaluation Samples | Test Samples per Repeat |
|---|---:|---:|---:|
| 2022 -> 2022 | 1,894 | 1,894 | 379 |
| 2021 -> 2022 | 979 | 979 | 196 |
| Three-year fixed effect | 2,937 | 1,894 | 379 |
| Three-year average | 2,937 | 2,937 | 587 |

## Reproduction Metrics

| Mode | Pearson Mean | Pearson SD | Spearman Mean | MSE Mean | Heritability Mean |
|---|---:|---:|---:|---:|---:|
| 2022 -> 2022 | 0.4613 | 0.0269 | 0.4672 | 0.0452 | 0.5390 |
| 2021 -> 2022 | 0.3749 | 0.0362 | 0.3789 | 0.0528 | 0.6988 |
| Three-year fixed effect | 0.5044 | 0.0338 | 0.5193 | 0.0431 | 0.5700 |
| Three-year average | 0.5462 | 0.0229 | 0.5657 | 0.0296 | 0.5821 |

All 40 runs completed without missing predictive-ability values.

## Author Split Audit

The author's public acidity `Perm1` design matrix contains:

| Audit Item | Count |
|---|---:|
| Total phenotype rows | 4,766 |
| Unique genotypes | 2,937 |
| Rows labelled test | 587 |
| Unique plant IDs labelled test | 528 |
| Test rows from 2020 | 193 |
| Test rows from 2021 | 176 |
| Test rows from 2022 | 218 |
| Test IDs retaining another training record | 382 |
| Test IDs retaining their 2022 acidity target in training | 201 |

The ID-safe reproduction always removes the selected plant's 2022 acidity value before fitting. Earlier-year records remain available in the repeated-record model.

## Output Files

Repeat-level metrics, predictions, and assignments are committed under [`tables/`](tables/):

- `acidity-within-2022-*`
- `acidity-cross-year-*`
- `acidity-3year-fixed-*`
- `acidity-3year-average-*`
- `author-acidity-3year-design-audit.csv`

Author 1000-repeat metrics and the public design matrix are committed under [`reference/`](reference/).

Original local runs remain under `D:\science-data\runs\blueberry-fruit-traits-genomic-prediction\acidity-*-seed42`.
