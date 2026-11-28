# Blueberry Fruit-Trait Genomic Prediction

## Goal

Reproduce the paper's genomic-prediction experiments for blueberry fruit quality and ripening traits using SNP genotype data.

The completed phases cover the core fruit-quality group, fruit mass, and plant height. The next phase moves to bloom timing.

## Paper

- Title: Genomic prediction enables selection for improved fruit ripening traits in northern highbush blueberry (Vaccinium corymbosum L.) breeding populations
- DOI: https://doi.org/10.1093/g3journal/jkag271
- Code and data: https://github.com/lilyhislop/BlueberryGenomicSelection_USDA-BI
- Local data path: `D:\science-data\datasets\blueberry-fruit-traits-genomic-prediction`
- Local run path: `D:\science-data\runs\blueberry-fruit-traits-genomic-prediction`

## Status

`reproducing`

The Brix, titratable-acidity, pH, ratio, fruit-mass, and height phases are complete with saved outputs and fixed-effect split audits. The broader project remains active.

## Progress

1. Minimal phenotype, genotype, and author-code inputs are prepared.
2. Four Brix prediction setups are complete with saved splits and outputs.
3. Titratable acidity is complete with four prediction setups.
4. pH is complete with four prediction setups.
5. Brix-to-acidity ratio is complete with four prediction setups.
6. The author's three-year fixed-effect split has been audited for all four core fruit-quality traits.
7. Fruit mass is complete with four prediction setups.
8. Plant height is complete with four prediction setups.
9. Next traits: bloom timing and ripening timing.
10. GWAS remains outside the current prediction-first scope.

## Quick Start

```powershell
$env:LC_ALL = "C"
D:\miniconda3\Scripts\conda.exe run -p D:\conda_envs\blueberry-gs Rscript `
  papers\005-blueberry-fruit-traits-genomic-prediction\scripts\run_brix_gblup.R `
  D:\science-data\datasets\blueberry-fruit-traits-genomic-prediction `
  D:\science-data\runs\blueberry-fruit-traits-genomic-prediction\brix-gblup-seed42 `
  10 42
```

See [`scripts/README.md`](scripts/README.md) for the inspection command and output descriptions.

## Brix Results

- Data inspection: [`results/data-inspection.md`](results/data-inspection.md)
- Brix GBLUP baseline: [`results/brix-gblup-seed42.md`](results/brix-gblup-seed42.md)
- 2021-to-2022 prediction: [`results/brix-2021-to-2022-seed42.md`](results/brix-2021-to-2022-seed42.md)
- Three-year model and split audit: [`results/brix-3year-fixed-seed42.md`](results/brix-3year-fixed-seed42.md)
- Three-year averaged Brix: [`results/brix-3year-average-seed42.md`](results/brix-3year-average-seed42.md)
- Current experiment summary: [`results/experiment-summary.md`](results/experiment-summary.md)
- Experiment metrics: [`results/metrics.md`](results/metrics.md)
- Repeat-level metrics and predictions: [`results/tables/`](results/tables/)
- Mean predictive ability: **0.4024**, close to the paper's approximately **0.41** result for its 2022 training set.
- ID-matched 2021-to-2022 predictive ability: **0.3327**, close to the paper's approximately **0.35** result.
- ID-safe three-year predictive ability: **0.4201**, below the paper's approximately **0.59**; the author split audit found direct 2022-target leakage.
- Three-year averaged predictive ability: **0.4558**, closely matching the author's 1000-repeat **0.4555** and paper's rounded **0.46**.

## Next Trait Phase

The next reproduction phase will reuse the same data checks, fixed seeds, ID-safe splits, metrics, logging, and result-table storage for bloom timing.

## Acidity Results

- Phase report: [`results/acidity-reproduction.md`](results/acidity-reproduction.md)
- 2022 -> 2022 Pearson: **0.4613** vs author **0.4710**
- 2021 -> 2022 Pearson: **0.3749** vs author **0.3554**
- ID-safe three-year fixed Pearson: **0.5044** vs author **0.6449**
- Three-year average Pearson: **0.5462** vs author **0.5624**

## pH Results

- Phase report: [`results/ph-reproduction.md`](results/ph-reproduction.md)
- 2022 -> 2022 Pearson: **0.4568** vs author **0.4594**
- 2021 -> 2022 Pearson: **0.3809** vs author **0.3871**
- ID-safe three-year fixed Pearson: **0.4824** vs author **0.6082**
- Three-year average Pearson: **0.5596** vs author **0.5685**

## Brix-to-Acidity Ratio Results

- Phase report: [`results/ratio-reproduction.md`](results/ratio-reproduction.md)
- 2022 -> 2022 Pearson: **0.4634**; author 1000-repeat reference unavailable
- 2021 -> 2022 Pearson: **0.3713**; author 1000-repeat reference unavailable
- ID-safe three-year fixed Pearson: **0.4993** vs author **0.5992**
- Three-year average Pearson: **0.5725** vs author **0.4960**; author SD **0.1013**

## Fruit Mass Results

- Phase report: [`results/fruit-mass-reproduction.md`](results/fruit-mass-reproduction.md)
- 2022 -> 2022 Pearson: **0.5973** vs author **0.5930**
- 2021 -> 2022 Pearson: **0.5612**; author 1000-repeat reference unavailable
- ID-safe three-year fixed Pearson: **0.6317** vs author **0.7193**
- Three-year average Pearson: **0.6666** vs author **0.6624**

## Plant Height Results

- Phase report: [`results/height-reproduction.md`](results/height-reproduction.md)
- 2022 -> 2022 Pearson: **0.5897** vs author **0.5668**
- 2021 -> 2022 Pearson: **0.4780** vs author **0.4754**
- ID-safe fixed-effect Pearson: **0.6294** vs author 10-repeat **0.6860**
- Available-years average Pearson: **0.5906** vs author **0.5845**

## Repository Rules

- Keep downloaded data under `D:\science-data\datasets`.
- Keep generated runs under `D:\science-data\runs`.
- Commit small CSV result tables so experiments can be reviewed from GitHub.
- Do not commit the full upstream repository or large generated files.
- Update `reproduction-log.md` and `results/metrics.md` for every run.
