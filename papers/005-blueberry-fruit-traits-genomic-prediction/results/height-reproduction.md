# Plant Height Reproduction

## Conclusion

The 2022-only, cross-year, and averaged height setups closely match the author references. The ID-safe fixed-effect result is lower than the author's public 10-repeat result, and the public design matrix contains direct 2022-target leakage. The available height phenotype contains only 2021 and 2022 measurements, so the author's `3y` label represents a two-year repeated-record model for this trait.

| Mode | This Reproduction | Author Reference | Difference | Status |
|---|---:|---:|---:|---|
| 2022 -> 2022 | 0.5897 | 0.5668 (1000 repeats) | +0.0229 | close |
| 2021 -> 2022 | 0.4780 | 0.4754 (1000 repeats) | +0.0026 | close |
| Available years -> 2022, year fixed | 0.6294 | 0.6860 (10 repeats) | -0.0566 | lower under ID-safe split |
| Available-years mean -> mean | 0.5906 | 0.5845 (1000 repeats) | +0.0061 | close |

## Setup

All runs use 1,822 SNP markers, 10 repeated 80/20 splits, seed 42, mean imputation, and `rrBLUP::kin.blup`.

| Mode | Model Genotypes | Evaluation Samples | Test Samples per Repeat |
|---|---:|---:|---:|
| 2022 -> 2022 | 3,830 | 3,830 | 766 |
| 2021 -> 2022 | 3,604 | 3,604 | 721 |
| Available-years fixed effect | 3,838 | 3,830 | 766 |
| Available-years average | 3,838 | 3,838 | 768 |

## Reproduction Metrics

| Mode | Pearson Mean | Pearson SD | Spearman Mean | MSE Mean | Heritability Mean |
|---|---:|---:|---:|---:|---:|
| 2022 -> 2022 | 0.5897 | 0.0185 | 0.5839 | 332.9831 | 0.5936 |
| 2021 -> 2022 | 0.4780 | 0.0305 | 0.4754 | 582.6515 | 0.6038 |
| Available-years fixed effect | 0.6294 | 0.0166 | 0.6226 | 365.6808 | 0.6540 |
| Available-years average | 0.5906 | 0.0104 | 0.5848 | 258.8781 | 0.6141 |

All 40 runs completed without missing predictive-ability values.

## Author Split Audit

| Audit Item | Count |
|---|---:|
| Total phenotype rows | 7,442 |
| Unique genotypes | 3,838 |
| Rows labelled test | 768 |
| Unique plant IDs labelled test | 697 |
| Test rows from 2020 | 0 |
| Test rows from 2021 | 379 |
| Test rows from 2022 | 389 |
| Test IDs retaining another training record | 585 |
| Test IDs retaining their 2022 height target in training | 307 |

## Output Files

Repeat-level metrics, predictions, and assignments are committed under [`tables/`](tables/):

- `height-within-2022-*`
- `height-cross-year-*`
- `height-3year-fixed-*`
- `height-3year-average-*`
- `author-height-3year-design-audit.csv`

Author metric tables and the public height design matrix are committed under [`reference/`](reference/).

Original local runs remain under `D:\science-data\runs\blueberry-fruit-traits-genomic-prediction\height-*-seed42`.
