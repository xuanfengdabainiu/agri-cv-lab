# Experiment Summary

## Brix Phase Status

Status: `done` for the Brix phase; project status is `reproducing` for the broader fruit-trait scope.

Three of four Brix experiments closely reproduce the paper. The corrected three-year fixed-effect experiment reproduces heritability but not predictive ability; an audit of the author's public split shows direct 2022-target leakage for 196 test-labelled plant IDs.

| Run | Training -> Evaluation | Reproduced Pearson | Paper Reference | Difference | Status |
|---|---|---:|---:|---:|---|
| brix-gblup-001 | 2022 -> 2022 | 0.4024 | 0.41 | -0.0076 | close |
| brix-gblup-002 | 2021 -> 2022 | 0.3327 | 0.35 | -0.0173 | close |
| brix-gblup-003 | 2020–2022 -> 2022, year fixed | 0.4201 | 0.59 | -0.1699 | not reproduced under ID-safe split |
| brix-gblup-004 | 2020–2022 mean -> mean | 0.4558 | 0.46 | -0.0042 | close |

## Interpretation

- The downloaded phenotype and SNP tables support stable GBLUP analysis.
- Cross-year prediction is harder than within-year prediction.
- Adding historical records gives only a small improvement over the 2022-only baseline when every selected 2022 target is correctly hidden.
- The paper's three-year predictive ability is sensitive to its record-level split and row-indexing implementation.
- The three-year heritability result is stable: reproduced 0.4927 versus approximately 0.49 in the paper.
- Averaging years gives a clean one-row-per-plant target and closely matches the author's 1000-repeat output.

## Next Scope

- The Brix prediction configurations are complete.
- The next reproduction group is acidity, pH, and Brix-to-acidity ratio.
- Fruit mass, plant height, bloom timing, and ripening timing follow after the fruit-quality group.
- Model improvements begin after the selected paper traits are reproduced.
