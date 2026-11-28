# Bloom 50% Timing Reproduction

## Conclusion

The 2022-only, fixed-effect, and averaged bloom-50% setups closely match the author references. The ID-matched cross-year result is higher than the author reference. The available phenotype contains only 2021 and 2022 bloom observations. The public fixed-effect design matrix contains direct 2022-target leakage, although the ID-safe result remains close for this trait.

| Mode | This Reproduction | Author 1000-Repeat Mean | Difference | Status |
|---|---:|---:|---:|---|
| 2022 -> 2022 | 0.5720 | 0.5825 | -0.0105 | close |
| 2021 -> 2022 | 0.5351 | 0.4589 | +0.0763 | not close |
| Available years -> 2022, year fixed | 0.5730 | 0.5793 | -0.0063 | close despite author split leakage |
| Available-years mean -> mean | 0.4981 | 0.4789 | +0.0192 | close |

## Setup

All runs use 1,822 SNP markers, 10 repeated 80/20 splits, seed 42, mean imputation, and `rrBLUP::kin.blup`.

| Mode | Model Genotypes | Evaluation Samples | Test Samples per Repeat |
|---|---:|---:|---:|
| 2022 -> 2022 | 1,731 | 1,731 | 346 |
| 2021 -> 2022 | 1,155 | 1,155 | 231 |
| Available-years fixed effect | 3,145 | 1,731 | 346 |
| Available-years average | 3,145 | 3,145 | 629 |

## Reproduction Metrics

| Mode | Pearson Mean | Pearson SD | Spearman Mean | MSE Mean | Heritability Mean |
|---|---:|---:|---:|---:|---:|
| 2022 -> 2022 | 0.5720 | 0.0293 | 0.5739 | 41.7525 | 0.6322 |
| 2021 -> 2022 | 0.5351 | 0.0512 | 0.5072 | 63.0722 | 0.6280 |
| Available-years fixed effect | 0.5730 | 0.0280 | 0.5564 | 50.1075 | 0.4823 |
| Available-years average | 0.4981 | 0.0213 | 0.4588 | 22.0561 | 0.4964 |

All 40 runs completed without missing predictive-ability values.

## Author Split Audit

| Audit Item | Count |
|---|---:|
| Total phenotype rows | 4,300 |
| Unique genotypes | 3,145 |
| Rows labelled test | 629 |
| Unique plant IDs labelled test | 591 |
| Test rows from 2020 | 0 |
| Test rows from 2021 | 382 |
| Test rows from 2022 | 247 |
| Test IDs retaining another training record | 266 |
| Test IDs retaining their 2022 bloom-50% target in training | 133 |

## Output Files

Repeat-level metrics, predictions, and assignments are committed under [`tables/`](tables/):

- `bloom50-within-2022-*`
- `bloom50-cross-year-*`
- `bloom50-3year-fixed-*`
- `bloom50-3year-average-*`
- `author-bloom50-3year-design-audit.csv`

Author metric tables and the public bloom-50% design matrix are committed under [`reference/`](reference/).

Original local runs remain under `D:\science-data\runs\blueberry-fruit-traits-genomic-prediction\bloom50-*-seed42`.
