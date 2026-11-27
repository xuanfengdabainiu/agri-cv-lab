# Experiment Summary

## Brix Phase Status

Status: `done` for the core fruit-quality group: Brix, titratable acidity, pH, and Brix-to-acidity ratio. Project status remains `reproducing` for the broader fruit and ripening-trait scope.

Three of four Brix experiments closely reproduce the paper. The corrected three-year fixed-effect experiment reproduces heritability but not predictive ability; an audit of the author's public split shows direct 2022-target leakage for 196 test-labelled plant IDs.

| Run | Training -> Evaluation | Reproduced Pearson | Paper Reference | Difference | Status |
|---|---|---:|---:|---:|---|
| brix-gblup-001 | 2022 -> 2022 | 0.4024 | 0.41 | -0.0076 | close |
| brix-gblup-002 | 2021 -> 2022 | 0.3327 | 0.35 | -0.0173 | close |
| brix-gblup-003 | 2020–2022 -> 2022, year fixed | 0.4201 | 0.59 | -0.1699 | not reproduced under ID-safe split |
| brix-gblup-004 | 2020–2022 mean -> mean | 0.4558 | 0.46 | -0.0042 | close |

Three of four acidity experiments also closely reproduce the author outputs. The fixed-effect mismatch has the same split problem.

| Run | Training -> Evaluation | Reproduced Pearson | Author Reference | Difference | Status |
|---|---|---:|---:|---:|---|
| acidity-gblup-001 | 2022 -> 2022 | 0.4613 | 0.4710 | -0.0097 | close |
| acidity-gblup-002 | 2021 -> 2022 | 0.3749 | 0.3554 | +0.0194 | close |
| acidity-gblup-003 | 2020–2022 -> 2022, year fixed | 0.5044 | 0.6449 | -0.1405 | not reproduced under ID-safe split |
| acidity-gblup-004 | 2020–2022 mean -> mean | 0.5462 | 0.5624 | -0.0162 | close |

Three of four pH experiments closely reproduce the author outputs. The fixed-effect mismatch again follows the leaky author split.

| Run | Training -> Evaluation | Reproduced Pearson | Author Reference | Difference | Status |
|---|---|---:|---:|---:|---|
| ph-gblup-001 | 2022 -> 2022 | 0.4568 | 0.4594 | -0.0026 | close |
| ph-gblup-002 | 2021 -> 2022 | 0.3809 | 0.3871 | -0.0063 | close |
| ph-gblup-003 | 2020–2022 -> 2022, year fixed | 0.4824 | 0.6082 | -0.1258 | not reproduced under ID-safe split |
| ph-gblup-004 | 2020–2022 mean -> mean | 0.5596 | 0.5685 | -0.0089 | close |

The ratio phase has two author-referenced modes and two local supplemental modes.

| Run | Training -> Evaluation | Reproduced Pearson | Author Reference | Difference | Status |
|---|---|---:|---:|---:|---|
| ratio-gblup-001 | 2022 -> 2022 | 0.4634 | - | - | local supplemental |
| ratio-gblup-002 | 2021 -> 2022 | 0.3713 | - | - | local supplemental |
| ratio-gblup-003 | 2020–2022 -> 2022, year fixed | 0.4993 | 0.5992 | -0.0999 | not reproduced under ID-safe split |
| ratio-gblup-004 | 2020–2022 mean -> mean | 0.5725 | 0.4960 | +0.0765 | within broad author variability |

## Interpretation

- The downloaded phenotype and SNP tables support stable GBLUP analysis.
- Cross-year prediction is harder than within-year prediction.
- Adding historical records gives only a small improvement over the 2022-only baseline when every selected 2022 target is correctly hidden.
- The paper's three-year predictive ability is sensitive to its record-level split and row-indexing implementation.
- The three-year heritability result is stable: reproduced 0.4927 versus approximately 0.49 in the paper.
- Averaging years gives a clean one-row-per-plant target and closely matches the author's 1000-repeat output.
- The acidity phase independently confirms that the author's three-year fixed-effect split can inflate predictive ability.
- The pH phase provides a third independent confirmation of the same fixed-effect split issue.
- The ratio phase provides a fourth confirmation of fixed-effect target leakage.

## Next Scope

- The Brix prediction configurations are complete.
- The core fruit-quality group is complete.
- Fruit mass is the next paper trait, followed by plant height, bloom timing, and ripening timing.
- Model improvements begin after the selected paper traits are reproduced.
