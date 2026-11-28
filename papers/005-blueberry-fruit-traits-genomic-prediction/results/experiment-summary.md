# Experiment Summary

## Brix Phase Status

Status: `done` for the core fruit-quality group, fruit mass, and plant height. Project status remains `reproducing` for bloom and ripening timing.

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

Fruit mass reproduces the two available non-leaky author references closely. The cross-year mode is a local supplemental result.

| Run | Training -> Evaluation | Reproduced Pearson | Author Reference | Difference | Status |
|---|---|---:|---:|---:|---|
| fruit-mass-gblup-001 | 2022 -> 2022 | 0.5973 | 0.5930 | +0.0044 | close |
| fruit-mass-gblup-002 | 2021 -> 2022 | 0.5612 | - | - | local supplemental |
| fruit-mass-gblup-003 | 2020–2022 -> 2022, year fixed | 0.6317 | 0.7193 | -0.0876 | not reproduced under ID-safe split |
| fruit-mass-gblup-004 | 2020–2022 mean -> mean | 0.6666 | 0.6624 | +0.0041 | close |

Plant height closely reproduces the clean author references. Only 2021 and 2022 height measurements are available.

| Run | Training -> Evaluation | Reproduced Pearson | Author Reference | Difference | Status |
|---|---|---:|---:|---:|---|
| height-gblup-001 | 2022 -> 2022 | 0.5897 | 0.5668 | +0.0229 | close |
| height-gblup-002 | 2021 -> 2022 | 0.4780 | 0.4754 | +0.0026 | close |
| height-gblup-003 | available years -> 2022, year fixed | 0.6294 | 0.6860 | -0.0566 | lower under ID-safe split |
| height-gblup-004 | available-years mean -> mean | 0.5906 | 0.5845 | +0.0061 | close |

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
- Fruit mass provides a fifth confirmation of the fixed-effect split problem while closely reproducing the clean within-year and averaged setups.
- Plant height provides a sixth confirmation of the fixed-effect split problem.

## Next Scope

- The Brix prediction configurations are complete.
- The core fruit-quality group is complete.
- Bloom timing is the next paper trait, followed by ripening timing.
- Model improvements begin after the selected paper traits are reproduced.
