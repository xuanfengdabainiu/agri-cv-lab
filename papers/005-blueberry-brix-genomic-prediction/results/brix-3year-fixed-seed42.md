# Three-Year Brix GBLUP With Year Fixed Effect

## Conclusion

The ID-safe three-year model reached a mean Pearson predictive ability of **0.4201**, below the paper's reported value of approximately **0.59**. Heritability was **0.4927**, which closely matches the paper's approximately **0.49**.

The predictive-ability gap is explained by the upstream split implementation. The author's public design matrix selects phenotype rows across all years, rather than selecting 2022 plant IDs. Some plants labelled as test still retain their 2022 Brix value in training.

## Setup

| Setting | Value |
|---|---|
| Model | GBLUP (`rrBLUP::kin.blup`) |
| Phenotype records | 4,849 |
| Model genotypes | 2,960 |
| 2022 evaluation plants | 1,935 |
| SNP markers | 1,822 |
| Fixed effect | Year |
| Split | 20% of 2022 plant IDs held out |
| Repeats | 10 |
| Seed | 42 |
| Training records per repeat | 4,462 |
| Test plants per repeat | 387 |

For a selected test plant, its 2022 Brix is always hidden. Its available 2020/2021 records remain in the model, matching the paper's repeated-record goal.

## Results

| Repeat | Pearson | Spearman | MSE | Heritability |
|---:|---:|---:|---:|---:|
| 1 | 0.4183 | 0.4077 | 4.0980 | 0.4975 |
| 2 | 0.3804 | 0.3833 | 4.1552 | 0.4984 |
| 3 | 0.3864 | 0.3764 | 3.9683 | 0.4945 |
| 4 | 0.4347 | 0.4348 | 4.0271 | 0.4963 |
| 5 | 0.4053 | 0.4005 | 4.5877 | 0.4893 |
| 6 | 0.4242 | 0.4055 | 4.4162 | 0.4894 |
| 7 | 0.4332 | 0.3950 | 3.9508 | 0.4888 |
| 8 | 0.4096 | 0.4031 | 4.0987 | 0.4841 |
| 9 | 0.3740 | 0.3726 | 4.1749 | 0.5081 |
| 10 | 0.5353 | 0.5386 | 3.8506 | 0.4807 |

| Summary | Mean | Standard Deviation | Minimum | Maximum |
|---|---:|---:|---:|---:|
| Pearson predictive ability | 0.4201 | 0.0457 | 0.3740 | 0.5353 |
| Spearman correlation | 0.4118 | 0.0480 | 0.3726 | 0.5386 |
| MSE | 4.1328 | 0.2218 | 3.8506 | 4.5877 |

All 10 repeats completed. The predictions table contains 3,870 rows and the assignments table contains 19,350 rows. No predictive-ability value is missing.

## Author Split Audit

The audit uses the author's public `Perm1` design matrix for the same three-year Brix setup.

| Audit Item | Count |
|---|---:|
| Total phenotype rows | 4,849 |
| Rows labelled test | 592 |
| Unique plant IDs labelled test | 535 |
| Test rows from 2020 | 178 |
| Test rows from 2021 | 170 |
| Test rows from 2022 | 244 |
| Test plant IDs retaining another training record | 405 |
| Test plant IDs retaining their 2022 Brix in training | 196 |

The final row is direct target leakage: a plant is represented in the test selection while its 2022 target remains available to the model. The upstream correlation code also indexes predictions and 2022 observations by row number even though one table is genotype-level and the other is record-level.

The author's public 10-repeat output has mean Pearson **0.5790** and mean Spearman **0.5740**, consistent with the paper's rounded 0.59 result. The ID-safe reproduction does not support that predictive-ability estimate.

## Output Files

Our result tables:

- [`tables/brix-3year-fixed-metrics.csv`](tables/brix-3year-fixed-metrics.csv)
- [`tables/brix-3year-fixed-predictions.csv`](tables/brix-3year-fixed-predictions.csv)
- [`tables/brix-3year-fixed-assignments.csv`](tables/brix-3year-fixed-assignments.csv)
- [`tables/author-3year-design-audit.csv`](tables/author-3year-design-audit.csv)

Author reference files:

- [`reference/author-3year-10perm-20pct-metrics.csv`](reference/author-3year-10perm-20pct-metrics.csv)
- [`reference/author-3year-design-perm1.csv`](reference/author-3year-design-perm1.csv)

The original local run remains at `D:\science-data\runs\blueberry-brix-genomic-prediction\brix-3year-fixed-seed42`.

SHA-256:

- Metrics: `D4AF1D2B060F9E580B9C2D60E7EFB64DE2A586A0A3808E812441BB1C01DEF778`
- Predictions: `DBA4BD16FB7B068F2DAA65A2A1E879737B95BA5E7AF273E8ED338DFBF10B79DE`
- Assignments: `6ED60057AEEB94AE7702DEA2ABF5A40336FF7FD029637EAF9F6A8BD83B8EF970`

## Compute Note

Peak observed R memory was approximately 2.9 GB, so the computer's 15.2 GB RAM is sufficient. This run was slower because `A.mat` attempted EM imputation on 2,960 genotypes before automatically falling back to mean imputation due to linear dependence.
