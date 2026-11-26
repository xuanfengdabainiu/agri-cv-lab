# Blueberry Fruit-Trait Genomic Prediction

## Goal

Reproduce the paper's genomic-prediction experiments for blueberry fruit quality and ripening traits using SNP genotype data.

The completed first phase covers soluble solids (`Brix`), a sweetness proxy. The next phase expands the same reproducible pipeline to acidity, pH, and the Brix-to-acidity ratio.

## Paper

- Title: Genomic prediction enables selection for improved fruit ripening traits in northern highbush blueberry (Vaccinium corymbosum L.) breeding populations
- DOI: https://doi.org/10.1093/g3journal/jkag271
- Code and data: https://github.com/lilyhislop/BlueberryGenomicSelection_USDA-BI
- Local data path: `D:\science-data\datasets\blueberry-fruit-traits-genomic-prediction`
- Local run path: `D:\science-data\runs\blueberry-fruit-traits-genomic-prediction`

## Status

`reproducing`

The Brix phase is complete: four training setups were reproduced and the three-year fixed-effect split was audited. The broader fruit-trait project remains active.

## Progress

1. Minimal phenotype, genotype, and author-code inputs are prepared.
2. Four Brix prediction setups are complete with saved splits and outputs.
3. The author's three-year fixed-effect split has been audited.
4. Next traits: titratable acidity, pH, and Brix-to-acidity ratio.
5. Later traits: fruit mass, plant height, bloom timing, and ripening timing.
6. GWAS remains outside the current prediction-first scope.

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

The next reproduction phase will reuse the same data checks, fixed seeds, ID-safe splits, metrics, logging, and result-table storage for acidity, pH, and Brix-to-acidity ratio.

## Repository Rules

- Keep downloaded data under `D:\science-data\datasets`.
- Keep generated runs under `D:\science-data\runs`.
- Commit small CSV result tables so experiments can be reviewed from GitHub.
- Do not commit the full upstream repository or large generated files.
- Update `reproduction-log.md` and `results/metrics.md` for every run.
