# Bloom 5% Timing Reproduction

## Conclusion

The 2022-only and averaged bloom-5% setups closely match the author references. The ID-matched cross-year result is lower, and the ID-safe fixed-effect result is substantially lower than the author reference. The public fixed-effect design matrix contains direct 2022-target leakage. Only 2021 and 2022 observations are available.

| Mode | This Reproduction | Author 1000-Repeat Mean | Difference | Status |
|---|---:|---:|---:|---|
| 2022 -> 2022 | 0.4963 | 0.4889 | +0.0075 | close |
| 2021 -> 2022 | 0.3178 | 0.3708 | -0.0530 | not close |
| Available years -> 2022, year fixed | 0.4862 | 0.6674 | -0.1812 | not reproduced under ID-safe split |
| Available-years mean -> mean | 0.4821 | 0.4734 | +0.0087 | close |

## Setup

All runs use 1,822 SNP markers, 10 repeated 80/20 splits, seed 42, mean imputation, and `rrBLUP::kin.blup`.

| Mode | Model Genotypes | Evaluation Samples | Test Samples per Repeat |
|---|---:|---:|---:|
| 2022 -> 2022 | 2,043 | 2,043 | 409 |
| 2021 -> 2022 | 859 | 859 | 172 |
| Available-years fixed effect | 2,715 | 2,043 | 409 |
| Available-years average | 2,715 | 2,715 | 543 |

## Reproduction Metrics

| Mode | Pearson Mean | Pearson SD | Spearman Mean | MSE Mean | Heritability Mean |
|---|---:|---:|---:|---:|---:|
| 2022 -> 2022 | 0.4963 | 0.0364 | 0.4889 | 29.1852 | 0.5494 |
| 2021 -> 2022 | 0.3178 | 0.0765 | 0.1747 | 36.6741 | 0.6339 |
| Available-years fixed effect | 0.4862 | 0.0428 | 0.4902 | 32.5530 | 0.4804 |
| Available-years average | 0.4821 | 0.0334 | 0.4810 | 21.3304 | 0.5339 |

All 40 runs completed without missing predictive-ability values.

## Author Split Audit

| Audit Item | Count |
|---|---:|
| Total phenotype rows | 3,574 |
| Unique genotypes | 2,715 |
| Rows labelled test | 543 |
| Unique plant IDs labelled test | 518 |
| Test rows from 2020 | 0 |
| Test rows from 2021 | 257 |
| Test rows from 2022 | 286 |
| Test IDs retaining another training record | 240 |
| Test IDs retaining their 2022 bloom-5% target in training | 112 |

## Output Files

Repeat-level outputs are committed under [`tables/`](tables/) with prefix `bloom5-`. Author references and the design matrix are under [`reference/`](reference/).

Original local runs remain under `D:\science-data\runs\blueberry-fruit-traits-genomic-prediction\bloom5-*-seed42`.
