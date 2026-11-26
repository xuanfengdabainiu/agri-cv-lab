# Three-Year Averaged Brix GBLUP

## Conclusion

The three-year averaged Brix model reached mean Pearson predictive ability **0.4558**, closely matching the author's public 1000-repeat mean of **0.4555** and the paper's rounded value of **0.46**.

Mean heritability was **0.5073**, also matching the paper's approximately **0.51**.

## Setup

| Setting | Value |
|---|---|
| Model | GBLUP (`rrBLUP::kin.blup`) |
| Source phenotype records | 4,849 |
| Averaged plant values | 2,960 |
| SNP markers | 1,822 |
| Split | 80% train / 20% test |
| Repeats | 10 |
| Seed | 42 |
| Samples per repeat | 2,368 train / 592 test |
| Imputation | Mean |

Each plant has one target value: its mean Brix across all available 2020–2022 measurements. This removes the repeated-row alignment issue found in the three-year fixed-effect implementation.

## Results

| Repeat | Pearson | Spearman | MSE | Heritability |
|---:|---:|---:|---:|---:|
| 1 | 0.4356 | 0.4303 | 3.2051 | 0.5102 |
| 2 | 0.4892 | 0.4702 | 3.2779 | 0.5039 |
| 3 | 0.4529 | 0.4368 | 2.8996 | 0.5020 |
| 4 | 0.4612 | 0.4398 | 2.9386 | 0.4939 |
| 5 | 0.4249 | 0.4085 | 3.1266 | 0.5326 |
| 6 | 0.4646 | 0.4559 | 3.0639 | 0.4954 |
| 7 | 0.4605 | 0.4261 | 3.1758 | 0.5189 |
| 8 | 0.4935 | 0.4804 | 2.7139 | 0.4852 |
| 9 | 0.3904 | 0.3958 | 3.3410 | 0.5184 |
| 10 | 0.4856 | 0.4577 | 2.8374 | 0.5121 |

| Summary | Mean | Standard Deviation | Minimum | Maximum |
|---|---:|---:|---:|---:|
| Pearson predictive ability | 0.4558 | 0.0320 | 0.3904 | 0.4935 |
| Spearman correlation | 0.4401 | 0.0266 | 0.3958 | 0.4804 |
| MSE | 3.0580 | 0.2042 | 2.7139 | 3.3410 |
| Heritability | 0.5073 | 0.0141 | 0.4852 | 0.5326 |

All 10 repeats completed. The predictions table contains 5,920 rows and the assignments table contains 29,600 rows. No predictive-ability value is missing.

## Paper Comparison

| Source | Repeats | Pearson Mean | Heritability |
|---|---:|---:|---:|
| This reproduction | 10 | 0.4558 | 0.5073 |
| Author public output | 1,000 | 0.4555 | approximately 0.51 |
| Paper, rounded | - | 0.46 | 0.51 |

The small Pearson difference between this reproduction and the 1000-repeat author output is 0.0003.

## Output Files

Our result tables:

- [`tables/brix-3year-average-metrics.csv`](tables/brix-3year-average-metrics.csv)
- [`tables/brix-3year-average-predictions.csv`](tables/brix-3year-average-predictions.csv)
- [`tables/brix-3year-average-assignments.csv`](tables/brix-3year-average-assignments.csv)

Author reference:

- [`reference/author-3year-average-1000perm-metrics.csv`](reference/author-3year-average-1000perm-metrics.csv)

The original local run remains at `D:\science-data\runs\blueberry-brix-genomic-prediction\brix-3year-average-seed42`.

SHA-256:

- Metrics: `EBD7BF368682623BA559B11344A98EA038BB7AAA0FBB676B29290B638172481C`
- Predictions: `7E5D7ABA2FE43B9AECC4B46DD50616D01C456A18B5AF442BADE54A0A87D3510C`
- Assignments: `90B4BC63AFE306DE0778B8EBAA32D63F475386BED9B808619110645893690CCD`

## Compute Note

Direct mean imputation produced the same effective method that `A.mat` selected after EM fallback in earlier runs. The complete run took approximately 38 seconds and required no GPU.
